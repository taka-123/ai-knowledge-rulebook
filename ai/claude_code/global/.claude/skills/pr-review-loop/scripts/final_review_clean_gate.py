#!/usr/bin/env python3
"""Final review-clean gate for pr-review-loop.

Official babysit-pr is the monitoring source of truth and stays unmodified.
This gate runs only immediately before completion. It re-fetches published
reviews from GitHub, including bots and external reviewers that the official
watcher may omit, and binds them to current HEAD via commit_id.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from urllib.parse import urlparse

SUMMARY_MARKERS = (
    "walkthrough",
    "auto-generated comment: summarize",
    "auto-generated comment: skip review",
    "review skipped",
    "codex-pull-request-review-summary",
)
FINDING_BADGE_MARKERS = (
    "![p0 badge]",
    "![p1 badge]",
    "![p2 badge]",
    "![p3 badge]",
)
BLOCKING_FINDING_BADGE_MARKERS = (
    "![p0 badge]",
    "![p1 badge]",
)
NON_BLOCKING_FINDING_BADGE_MARKERS = (
    "![p2 badge]",
    "![p3 badge]",
)
CHANGES_REQUESTED_MARKER = "changes requested"
ACTIONABLE_MARKERS = (*BLOCKING_FINDING_BADGE_MARKERS, CHANGES_REQUESTED_MARKER)
PENDING = "PENDING"
DISMISSED = "DISMISSED"
VALID_PROOF_REVIEW_STATES = {"COMMENTED", "APPROVED"}
COMPLETION_ONLY_KINDS = frozenset({"issue_comment", "codex_thumbs_up"})
THUMBS_UP = {"+1", "THUMBS_UP", "thumbs_up"}
CODEX_REVIEW_REQUEST_RE = re.compile(r"@codex\s+review\b", re.IGNORECASE)
HEAD_FIELD_RE = re.compile(r"(?im)(?:^|\b)head\s*[:=]\s*([0-9a-f]{7,40})\b")
REVIEWED_COMMIT_RE = re.compile(
    r"(?im)reviewed\s+commit[^0-9a-f\n]{0,40}([0-9a-f]{7,40})"
)
ISSUE_COMMENT_NO_FINDING_RE = re.compile(
    r"(?i)(?::\+1:|👍|didn't find any (?:major )?issues|no blocking findings)"
)
SHA_RE = re.compile(r"\b([0-9a-f]{7,40})\b", re.IGNORECASE)
REVIEW_ORIGIN_KINDS = frozenset({"review_comment", "review_thread"})
APPROVAL_ONLY_RE = re.compile(
    r"^\s*(?:lgtm|looks\s+(?:good|fine)(?:\s+to\s+me)?|approved|no issues found)"
    r"(?:\s*[.!]*)?\s*$",
    re.IGNORECASE,
)
THREAD_PAGE_LIMIT = 50
COMMENT_PAGE_LIMIT = 100
THREADS_QUERY = """
query($owner: String!, $name: String!, $number: Int!, $after: String) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      reviewThreads(first: 100, after: $after) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          id
          isResolved
          isOutdated
          comments(first: %d) {
            pageInfo {
              hasNextPage
            }
            nodes {
              id
              databaseId
              replyTo { databaseId }
              body
              path
              author { login }
              originalCommit { oid }
              commit { oid }
            }
          }
        }
      }
    }
  }
}
""" % COMMENT_PAGE_LIMIT
RESOLVE_THREAD_MUTATION = """
mutation($id: ID!) {
  resolveReviewThread(input: {threadId: $id}) {
    thread { id isResolved }
  }
}
"""
REPLY_THREAD_MUTATION = """
mutation($id: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {pullRequestReviewThreadId: $id, body: $body}) {
    comment { id databaseId }
  }
}
"""
UPDATE_REVIEW_COMMENT_MUTATION = """
mutation($id: ID!, $body: String!) {
  updatePullRequestReviewComment(input: {pullRequestReviewCommentId: $id, body: $body}) {
    pullRequestReviewComment { id databaseId }
  }
}
"""
DISPOSITION_IGNORE = "IGNORE_WITH_REASON"
DISPOSITION_AUTO_FIX = "AUTO_FIX"
DISPOSITION_MARKER_RE = re.compile(
    r"<!--\s*pr-review-loop:disposition=(IGNORE_WITH_REASON|AUTO_FIX)([^>]*)-->",
    re.IGNORECASE,
)
DISPOSITION_ATTR_RE = re.compile(r"\b(fingerprint|head)=([0-9a-f]+)", re.IGNORECASE)
IGNORE_REPLY_PREFIX = "AIエージェントによる対応: "
FINDING_BADGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")


class GhCommandError(RuntimeError):
    pass


def gh_text(args):
    cmd = ["gh", *args]
    try:
        proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError as err:
        raise GhCommandError("`gh` command not found") from err
    except subprocess.CalledProcessError as err:
        stdout = (err.stdout or "").strip()
        stderr = (err.stderr or "").strip()
        raise GhCommandError(f"GitHub CLI command failed: {' '.join(cmd)}\n{stdout}\n{stderr}") from err
    return proc.stdout


def gh_json(args):
    raw = gh_text(args).strip()
    if not raw:
        return None
    return json.loads(raw)


def gh_api_list(endpoint):
    items = []
    page = 1
    while True:
        sep = "&" if "?" in endpoint else "?"
        payload = gh_json(["api", f"{endpoint}{sep}per_page=100&page={page}", "-X", "GET"])
        if payload is None:
            break
        if not isinstance(payload, list):
            raise GhCommandError(f"Unexpected list payload from {endpoint}")
        items.extend(payload)
        if len(payload) < 100:
            break
        page += 1
    return items


def extract_login(user_obj):
    if isinstance(user_obj, dict):
        return str(user_obj.get("login") or "")
    return ""


def parse_pr_spec(pr_spec):
    if pr_spec == "auto":
        return {"mode": "auto"}
    if str(pr_spec).isdigit():
        return {"mode": "number", "value": str(pr_spec)}
    parsed = urlparse(str(pr_spec))
    if parsed.scheme and parsed.netloc and "/pull/" in parsed.path:
        return {"mode": "url", "value": str(pr_spec)}
    raise ValueError("--pr must be 'auto', a PR number, or a PR URL")


def extract_repo_from_pr_url(pr_url):
    parsed = urlparse(str(pr_url or ""))
    parts = [item for item in parsed.path.split("/") if item]
    if len(parts) >= 4 and parts[2] == "pull":
        return f"{parts[0]}/{parts[1]}"
    return ""


def split_repo(repo):
    raw = str(repo or "")
    if "/" not in raw:
        return "", ""
    owner, name = raw.split("/", 1)
    return owner, name


def resolve_pr(pr_spec, repo_override=None, head_override=None):
    spec = parse_pr_spec(pr_spec)
    args = ["pr", "view", "--json", "number,url,headRefOid,headRepository,headRepositoryOwner,author"]
    if spec["mode"] == "number":
        args.insert(2, spec["value"])
    elif spec["mode"] == "url":
        args.insert(2, spec["value"])
    if repo_override:
        args.extend(["-R", repo_override])
    data = gh_json(args)
    if not isinstance(data, dict):
        raise GhCommandError("Unexpected PR payload from `gh pr view`")
    pr_url = str(data.get("url") or "")
    repo = repo_override or extract_repo_from_pr_url(pr_url)
    if repo and "/" in repo:
        owner, name = split_repo(repo)
    else:
        owner = ((data.get("headRepositoryOwner") or {}).get("login")) or ""
        name = ((data.get("headRepository") or {}).get("name")) or ""
        repo = f"{owner}/{name}" if owner and name else ""
    actual_head = str(data.get("headRefOid") or "")
    if head_override and head_override != actual_head:
        raise GhCommandError(
            f"--head {head_override} does not match current PR HEAD {actual_head}"
        )
    author_login = ((data.get("author") or {}).get("login")) or ""
    return {
        "number": int(data.get("number")),
        "repo": repo,
        "owner": owner,
        "name": name,
        "head_sha": actual_head,
        "url": pr_url,
        "author": author_login,
    }


# REST uses chatgpt-codex-connector[bot] / codex[bot]; GraphQL omits [bot]
# only for chatgpt-codex-connector. Do not partial-match other *codex* actors.
CODEX_REVIEWER_IDENTITIES = {
    ("chatgpt-codex-connector", False),
    ("chatgpt-codex-connector", True),
    ("codex", True),
}


def normalize_reviewer_login(login):
    lower = str(login or "").strip().lower()
    if lower.endswith("[bot]"):
        return lower[: -len("[bot]")], True
    return lower, False


def is_codex_reviewer(login):
    identity = normalize_reviewer_login(login)
    if not identity[0]:
        return False
    return identity in CODEX_REVIEWER_IDENTITIES


def canonical_github_login(login):
    return normalize_reviewer_login(login)[0]


def same_github_actor(left, right):
    a = canonical_github_login(left)
    b = canonical_github_login(right)
    return bool(a) and bool(b) and a == b


def fetch_authenticated_login():
    try:
        data = gh_json(["api", "user", "-X", "GET"])
    except GhCommandError:
        return ""
    if not isinstance(data, dict):
        return ""
    return extract_login(data)


def is_trusted_disposition_author(login, gh_user=""):
    return same_github_actor(login, gh_user)


def has_ignore_reply_prefix(body):
    return str(body or "").lstrip().startswith(IGNORE_REPLY_PREFIX)


def is_codex_review_request(body):
    return bool(CODEX_REVIEW_REQUEST_RE.search(body or ""))


def canonicalize_sha(value, head_sha=""):
    raw = str(value or "").strip()
    head = str(head_sha or "").strip()
    if not raw:
        return ""
    if head and (raw.lower() == head.lower() or (len(raw) >= 7 and head.lower().startswith(raw.lower()))):
        return head
    return raw.lower()


def extract_bound_sha(body, head_sha=""):
    text = body or ""
    field = HEAD_FIELD_RE.search(text) or REVIEWED_COMMIT_RE.search(text)
    if field:
        return canonicalize_sha(field.group(1), head_sha)
    if head_sha and head_sha.lower() in text.lower():
        return head_sha
    matches = SHA_RE.findall(text)
    full = [item for item in matches if len(item) == 40]
    if len(full) == 1:
        return canonicalize_sha(full[0], head_sha)
    return ""


def extract_reviewed_commit_sha(body, head_sha=""):
    match = REVIEWED_COMMIT_RE.search(body or "")
    if not match:
        return ""
    return canonicalize_sha(match.group(1), head_sha)


def has_explicit_no_finding_marker(body):
    return bool(ISSUE_COMMENT_NO_FINDING_RE.search(body or ""))


def is_summary_only(body, path=None):
    if path:
        return False
    lower = (body or "").lower()
    return any(marker in lower for marker in SUMMARY_MARKERS)


def is_approval_only(body):
    return bool(APPROVAL_ONLY_RE.match((body or "").strip()))


def has_finding_badge(body):
    lower = (body or "").lower()
    return any(marker in lower for marker in FINDING_BADGE_MARKERS)


def has_blocking_finding_badge(body):
    lower = (body or "").lower()
    return any(marker in lower for marker in BLOCKING_FINDING_BADGE_MARKERS)


def has_non_blocking_finding_badge(body):
    lower = (body or "").lower()
    return any(marker in lower for marker in NON_BLOCKING_FINDING_BADGE_MARKERS)


def has_changes_requested_marker(body):
    return CHANGES_REQUESTED_MARKER in (body or "").lower()


def has_actionable_marker(body):
    return has_blocking_finding_badge(body) or has_changes_requested_marker(body)


def is_actionable_text(
    body,
    path=None,
    review_state=None,
    kind=None,
    author=None,
    gh_user="",
    in_reply_to_id="",
):
    if str(kind or "") in COMPLETION_ONLY_KINDS:
        return False
    if (
        kind == "review_comment"
        and str(in_reply_to_id or "")
        and is_codex_reviewer(author)
    ):
        return False
    if is_disposition_reply(body) and is_trusted_disposition_author(author, gh_user):
        return False
    state = str(review_state or "").upper()
    if state == "CHANGES_REQUESTED":
        return True
    if has_blocking_finding_badge(body):
        return True
    if state == "APPROVED":
        return False
    if has_changes_requested_marker(body):
        return True
    if is_summary_only(body, path):
        return False
    # REVIEW.md: P2 / P3 only are ready; do not block review-clean on those badges.
    if has_non_blocking_finding_badge(body) and not has_blocking_finding_badge(body):
        return False
    if path:
        return True
    if kind != "review" or is_codex_reviewer(author):
        return False
    text = (body or "").strip()
    if not text or is_approval_only(text):
        return False
    return True


def extract_finding_title(body):
    lines = normalize_finding_lines(body)
    return lines[0][:200] if lines else ""


def normalize_finding_lines(body):
    text = FINDING_BADGE_RE.sub("", body or "")
    text = re.sub(r"</?[^>]+>", " ", text)
    text = re.sub(r"[*_#`]+", "", text)
    lines = []
    for line in text.splitlines():
        cleaned = " ".join(line.split()).strip()
        if not cleaned:
            continue
        if cleaned.lower() in {"p0 badge", "p1 badge", "p2 badge", "p3 badge"}:
            continue
        if cleaned.lower().startswith("useful?"):
            continue
        lines.append(cleaned.lower())
    return lines


def finding_fingerprint(item):
    path = str((item or {}).get("path") or "").strip().lower()
    text = "\n".join(normalize_finding_lines((item or {}).get("body") or ""))
    raw = f"{path}\n{text}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def parse_disposition_marker(body):
    match = DISPOSITION_MARKER_RE.search(body or "")
    if not match:
        return None
    attrs = {
        key.lower(): value.lower()
        for key, value in DISPOSITION_ATTR_RE.findall(match.group(2) or "")
    }
    return {
        "disposition": match.group(1).upper(),
        "fingerprint": attrs.get("fingerprint", ""),
        "head": attrs.get("head", ""),
    }


def is_disposition_reply(body):
    return parse_disposition_marker(body) is not None


def format_ignore_reply(reason, fingerprint, head_sha):
    text = " ".join(str(reason or "").split()).strip()
    if not text:
        raise ValueError("IGNORE_WITH_REASON requires a concrete reason")
    fp = str(fingerprint or "").strip().lower()
    if not fp:
        raise ValueError("IGNORE_WITH_REASON requires a finding fingerprint")
    head = str(head_sha or "").strip()
    if not head:
        raise ValueError("IGNORE_WITH_REASON requires current HEAD")
    visible = text if text.startswith(IGNORE_REPLY_PREFIX) else f"{IGNORE_REPLY_PREFIX}{text}"
    marker = (
        f"<!-- pr-review-loop:disposition={DISPOSITION_IGNORE} "
        f"fingerprint={fp} head={head} -->"
    )
    return f"{visible}\n\n{marker}"


def ignore_reply_visible_text(body):
    text = str(body or "").strip()
    match = DISPOSITION_MARKER_RE.search(text)
    if match:
        return text[: match.start()].strip()
    return text.split("\n\n", 1)[0].strip()


def normalize_ignore_reason(reason):
    text = " ".join(str(reason or "").split()).strip()
    if text.startswith(IGNORE_REPLY_PREFIX):
        text = text[len(IGNORE_REPLY_PREFIX) :].strip()
    return text


def rebind_ignore_reply(existing_body, reason, fingerprint, head_sha):
    desired = format_ignore_reply(reason, fingerprint, head_sha)
    existing_reason = normalize_ignore_reason(ignore_reply_visible_text(existing_body))
    if existing_reason and existing_reason == normalize_ignore_reason(reason):
        visible = ignore_reply_visible_text(existing_body)
        parsed = parse_disposition_marker(desired)
        marker = (
            f"<!-- pr-review-loop:disposition={DISPOSITION_IGNORE} "
            f"fingerprint={parsed['fingerprint']} head={parsed['head']} -->"
        )
        return f"{visible}\n\n{marker}"
    return desired


def trusted_ignore_replies_on_thread(thread, fingerprint, gh_user=""):
    matches = []
    if not isinstance(thread, dict) or not gh_user:
        return matches
    bodies = thread.get("comment_bodies") or []
    authors = thread.get("comment_authors")
    node_ids = thread.get("comment_node_ids") or []
    db_ids = thread.get("comment_ids") or []
    if not isinstance(bodies, list) or not isinstance(authors, list):
        return matches
    if len(authors) != len(bodies):
        return matches
    wanted_fp = str(fingerprint or "").strip().lower()
    if not wanted_fp:
        return matches
    for index, (author, body) in enumerate(zip(authors, bodies)):
        if not is_trusted_disposition_author(author, gh_user):
            continue
        if not has_ignore_reply_prefix(body):
            continue
        parsed = parse_disposition_marker(body)
        if not parsed or parsed["disposition"] != DISPOSITION_IGNORE:
            continue
        if (parsed.get("fingerprint") or "") != wanted_fp:
            continue
        node_id = node_ids[index] if index < len(node_ids) else ""
        db_id = db_ids[index] if index < len(db_ids) else ""
        matches.append(
            {
                "index": index,
                "author": author,
                "body": body,
                "comment_node_id": str(node_id or ""),
                "comment_id": str(db_id or ""),
                "marker_head": parsed.get("head") or "",
            }
        )
    return matches


def trusted_ignore_fingerprints_from_thread(thread, gh_user="", head_sha=""):
    fingerprints = set()
    if not isinstance(thread, dict):
        return fingerprints
    if thread.get("comments_complete") is False:
        return fingerprints
    if not gh_user or not head_sha:
        return fingerprints
    bodies = thread.get("comment_bodies") or []
    authors = thread.get("comment_authors")
    if not isinstance(bodies, list) or not isinstance(authors, list):
        return fingerprints
    if len(authors) != len(bodies):
        return fingerprints
    participants = [str(login) for login in authors if str(login or "")]
    if not participants:
        return fingerprints
    if not all(
        is_codex_reviewer(login) or is_trusted_disposition_author(login, gh_user)
        for login in participants
    ):
        return fingerprints
    thread_fp = finding_fingerprint(thread)
    current_head = canonicalize_sha(head_sha, head_sha)
    for author, body in zip(authors, bodies):
        if not is_trusted_disposition_author(author, gh_user):
            continue
        if not has_ignore_reply_prefix(body):
            continue
        parsed = parse_disposition_marker(body)
        if not parsed or parsed["disposition"] != DISPOSITION_IGNORE:
            continue
        marker_fp = parsed.get("fingerprint") or ""
        marker_head = canonicalize_sha(parsed.get("head") or "", head_sha)
        if marker_fp == thread_fp and marker_head == current_head:
            fingerprints.add(thread_fp)
    return fingerprints


def collect_ignore_fingerprints(threads, comments=None, gh_user="", head_sha=""):
    del comments
    fingerprints = set()
    for item in threads or []:
        fingerprints |= trusted_ignore_fingerprints_from_thread(
            item, gh_user=gh_user, head_sha=head_sha
        )
    return fingerprints


def item_identity_ids(item):
    ids = thread_ids(item)
    for comment_id in item.get("comment_ids") or []:
        if comment_id not in (None, ""):
            ids.add(str(comment_id))
    return ids


def matching_threads_for_item(item, threads):
    ids = item_identity_ids(item)
    matched = []
    for thread in threads or []:
        if ids & item_identity_ids(thread):
            matched.append(thread)
    return matched


def ignore_fingerprints_for_item(item, threads, gh_user="", head_sha=""):
    fingerprints = set()
    for thread in matching_threads_for_item(item, threads):
        fingerprints |= trusted_ignore_fingerprints_from_thread(
            thread, gh_user=gh_user, head_sha=head_sha
        )
    return fingerprints


def normalize_reviews(payload):
    out = []
    for item in payload or []:
        if not isinstance(item, dict):
            continue
        state = str(item.get("state") or "").upper()
        if state in {PENDING, DISMISSED}:
            continue
        out.append(
            {
                "kind": "review",
                "id": str(item.get("id") or ""),
                "author": extract_login(item.get("user")),
                "author_association": str(item.get("author_association") or ""),
                "state": state,
                "commit_id": str(item.get("commit_id") or ""),
                "original_commit_id": "",
                "path": None,
                "line": None,
                "resolved": None,
                "outdated": None,
                "body": str(item.get("body") or ""),
                "url": str(item.get("html_url") or ""),
                "submitted_at": str(item.get("submitted_at") or ""),
            }
        )
    return latest_reviews_per_reviewer_commit(out)


def _review_recency_key(item, index):
    submitted = str((item or {}).get("submitted_at") or "")
    try:
        review_id = int(str((item or {}).get("id") or "0"))
    except ValueError:
        review_id = 0
    return (submitted, review_id, index)


CHANGES_REQUESTED_CLEARED_BY = {"APPROVED", "DISMISSED", "CHANGES_REQUESTED"}


def latest_reviews_per_reviewer_commit(reviews):
    chosen = {}
    passthrough = []
    for index, item in enumerate(reviews or []):
        author = canonical_github_login((item or {}).get("author"))
        commit_id = str((item or {}).get("commit_id") or "")
        if not author or not commit_id:
            passthrough.append(item)
            continue
        key = (author, commit_id)
        prev = chosen.get(key)
        if prev is None:
            chosen[key] = (item, index)
            continue
        if _review_recency_key(item, index) <= _review_recency_key(prev[0], prev[1]):
            continue
        prev_state = str((prev[0] or {}).get("state") or "").upper()
        new_state = str((item or {}).get("state") or "").upper()
        if prev_state == "CHANGES_REQUESTED" and new_state not in CHANGES_REQUESTED_CLEARED_BY:
            continue
        if prev_state == "COMMENTED" and new_state == "COMMENTED":
            passthrough.append(item)
            continue
        if new_state in CHANGES_REQUESTED_CLEARED_BY:
            passthrough = [
                kept_item
                for kept_item in passthrough
                if (
                    canonical_github_login((kept_item or {}).get("author")),
                    str((kept_item or {}).get("commit_id") or ""),
                )
                != key
            ]
        chosen[key] = (item, index)
    kept = [pair[0] for pair in sorted(chosen.values(), key=lambda pair: pair[1])]
    return kept + passthrough


def normalize_review_comments(payload, pending_review_ids):
    out = []
    for item in payload or []:
        if not isinstance(item, dict):
            continue
        review_id = str(item.get("pull_request_review_id") or "")
        if review_id and review_id in pending_review_ids:
            continue
        out.append(
            {
                "kind": "review_comment",
                "id": str(item.get("id") or ""),
                "in_reply_to_id": str(item.get("in_reply_to_id") or ""),
                "author": extract_login(item.get("user")),
                "author_association": str(item.get("author_association") or ""),
                "state": "",
                "commit_id": str(item.get("commit_id") or ""),
                "original_commit_id": str(item.get("original_commit_id") or ""),
                "path": item.get("path"),
                "line": item.get("line") if item.get("line") is not None else item.get("original_line"),
                "resolved": None,
                "outdated": item.get("position") is None,
                "body": str(item.get("body") or ""),
                "url": str(item.get("html_url") or ""),
            }
        )
    return out


def normalize_issue_comments(payload, head_sha=""):
    out = []
    for item in payload or []:
        if not isinstance(item, dict):
            continue
        body = str(item.get("body") or "")
        author = extract_login(item.get("user"))
        bind = is_codex_review_request(body) or (
            is_codex_reviewer(author) and bool(REVIEWED_COMMIT_RE.search(body))
        )
        commit_id = extract_bound_sha(body, head_sha) if bind else ""
        out.append(
            {
                "kind": "issue_comment",
                "id": str(item.get("id") or ""),
                "author": author,
                "author_association": str(item.get("author_association") or ""),
                "state": "",
                "commit_id": commit_id,
                "original_commit_id": "",
                "path": None,
                "line": None,
                "resolved": None,
                "outdated": None,
                "body": body,
                "url": str(item.get("html_url") or ""),
                "created_at": str(item.get("created_at") or ""),
                "updated_at": str(item.get("updated_at") or ""),
            }
        )
    return out


def normalize_threads(payload):
    out = []
    for thread in payload or []:
        if not isinstance(thread, dict):
            continue
        comments_payload = thread.get("comments")
        comments_complete = True
        if isinstance(comments_payload, dict):
            comments = comments_payload.get("nodes") or []
            page_info = comments_payload.get("pageInfo") or {}
            if isinstance(page_info, dict) and page_info.get("hasNextPage"):
                comments_complete = False
        elif isinstance(comments_payload, list):
            comments = comments_payload
        else:
            comments = []
        first = comments[0] if comments else {}
        author = first.get("author") if isinstance(first, dict) else {}
        commit = first.get("commit") if isinstance(first, dict) else {}
        original = first.get("originalCommit") if isinstance(first, dict) else {}
        authors = []
        comment_ids = []
        comment_node_ids = []
        comment_reply_to_ids = []
        comment_bodies = []
        comment_authors = []
        for comment in comments:
            if not isinstance(comment, dict):
                comments_complete = False
                continue
            login = extract_login(comment.get("author"))
            if login:
                authors.append(login)
            else:
                comments_complete = False
            comment_id = comment.get("databaseId")
            if comment_id not in (None, ""):
                comment_ids.append(str(comment_id))
            comment_node_ids.append(str(comment.get("id") or ""))
            reply_to = comment.get("replyTo") or {}
            comment_reply_to_ids.append(str(reply_to.get("databaseId") or ""))
            comment_bodies.append(str(comment.get("body") or ""))
            comment_authors.append(login)
        first_id = str((first or {}).get("databaseId") or "")
        if first_id and first_id not in comment_ids:
            comment_ids.insert(0, first_id)
        out.append(
            {
                "kind": "review_thread",
                "id": first_id,
                "node_id": str(thread.get("id") or ""),
                "author": extract_login(author),
                "authors": authors,
                "comment_ids": comment_ids,
                "comment_node_ids": comment_node_ids,
                "comment_reply_to_ids": comment_reply_to_ids,
                "comment_bodies": comment_bodies,
                "comment_authors": comment_authors,
                "comments_complete": comments_complete,
                "author_association": "",
                "state": "",
                "commit_id": str((commit or {}).get("oid") or ""),
                "original_commit_id": str((original or {}).get("oid") or ""),
                "path": (first or {}).get("path"),
                "line": None,
                "resolved": bool(thread.get("isResolved")),
                "outdated": bool(thread.get("isOutdated")),
                "body": str((first or {}).get("body") or ""),
                "url": "",
            }
        )
    return out


def request_comment_is_immutable(comment):
    """Edited @codex review requests are not completion proof (no timestamp races)."""
    created = str((comment or {}).get("created_at") or "")
    updated = str((comment or {}).get("updated_at") or "")
    return not (created and updated and updated > created)


def normalize_codex_completion_signals(issue_comments, reactions_by_comment_id, head_sha=""):
    out = []
    for comment in issue_comments or []:
        if not isinstance(comment, dict):
            continue
        body = str(comment.get("body") or "")
        if not is_codex_review_request(body):
            continue
        if not request_comment_is_immutable(comment):
            continue
        comment_id = str(comment.get("id") or "")
        bound = extract_bound_sha(body, head_sha) or str(comment.get("commit_id") or "")
        for reaction in reactions_by_comment_id.get(comment_id, []) or []:
            if not isinstance(reaction, dict):
                continue
            content = str(reaction.get("content") or "")
            author = extract_login(reaction.get("user")) or str(reaction.get("author") or "")
            if content not in THUMBS_UP:
                continue
            if not is_codex_reviewer(author):
                continue
            out.append(
                {
                    "kind": "codex_thumbs_up",
                    "id": str(reaction.get("id") or ""),
                    "author": author,
                    "author_association": "",
                    "state": "",
                    "commit_id": bound,
                    "original_commit_id": "",
                    "path": None,
                    "line": None,
                    "resolved": None,
                    "outdated": None,
                    "body": body,
                    "url": str(comment.get("url") or comment.get("html_url") or ""),
                    "content": "+1",
                    "request_id": comment_id,
                }
            )
    return out


def pending_review_ids(raw_reviews):
    ids = set()
    for item in raw_reviews or []:
        if not isinstance(item, dict):
            continue
        if str(item.get("state") or "").upper() == PENDING and item.get("id") not in (None, ""):
            ids.add(str(item.get("id")))
    return ids


def item_review_sha(item):
    """SHA that identifies which review this item belongs to.

    GitHub retargets review_comment.commit_id onto later commits while the
    commented line still exists. original_commit_id is the reviewed commit.
    """
    original = str((item or {}).get("original_commit_id") or "")
    current = str((item or {}).get("commit_id") or "")
    if str((item or {}).get("kind") or "") in REVIEW_ORIGIN_KINDS and original:
        return original
    return current


def bound_to_head(item, head_sha):
    return bool(head_sha) and item_review_sha(item) == head_sha


def is_codex_completion_proof(item, head_sha):
    if not bound_to_head(item, head_sha):
        return False
    if not is_codex_reviewer(item.get("author")):
        return False
    kind = item.get("kind")
    body = item.get("body")
    if kind == "review":
        state = str(item.get("state") or "").upper()
        if state not in VALID_PROOF_REVIEW_STATES:
            return False
        if is_summary_only(body, item.get("path")):
            return False
        return True
    if kind == "codex_thumbs_up" and str(item.get("content") or "") in THUMBS_UP:
        return True
    if kind == "issue_comment":
        if is_codex_review_request(body):
            return False
        if is_summary_only(body):
            return False
        if has_blocking_finding_badge(body):
            return False
        if extract_reviewed_commit_sha(body, head_sha) != head_sha:
            return False
        return has_explicit_no_finding_marker(body)
    return False


def thread_ids(item):
    return {
        str(item.get("node_id") or ""),
        str(item.get("id") or ""),
        str(item.get("database_id") or ""),
    } - {""}


def thread_authors(item):
    raw = item.get("authors")
    if not isinstance(raw, list):
        return []
    return [str(login) for login in raw if str(login or "")]


def is_codex_only_thread(item):
    if item.get("comments_complete") is False:
        return False
    authors = thread_authors(item)
    return bool(authors) and all(is_codex_reviewer(login) for login in authors)


def is_codex_or_helper_thread(item, gh_user=""):
    if item.get("comments_complete") is False:
        return False
    authors = thread_authors(item)
    if not authors:
        return False
    return all(
        is_codex_reviewer(login) or is_trusted_disposition_author(login, gh_user)
        for login in authors
    )


def eligible_codex_resolve_threads(threads, requested_ids, pushed_head_sha, current_head_sha):
    if not pushed_head_sha or pushed_head_sha != current_head_sha:
        raise ValueError("resolve Codex threads only after commit + push of current HEAD")
    wanted = {str(item) for item in requested_ids or [] if str(item)}
    if not wanted:
        raise ValueError("resolve Codex threads requires explicit --thread-id values")
    eligible = []
    rejected = []
    for item in threads or []:
        ids = thread_ids(item)
        if not (ids & wanted):
            continue
        if item.get("resolved") is True:
            continue
        if item.get("comments_complete") is False:
            rejected.append(item)
            continue
        if is_codex_only_thread(item):
            eligible.append(item)
        else:
            rejected.append(item)
    return eligible, rejected


def eligible_codex_ignore_threads(
    threads, requested_ids, current_head_sha, expected_head_sha, gh_user=""
):
    if not expected_head_sha or expected_head_sha != current_head_sha:
        raise ValueError("IGNORE_WITH_REASON requires --head to match current PR HEAD")
    wanted = {str(item) for item in requested_ids or [] if str(item)}
    if not wanted:
        raise ValueError("IGNORE_WITH_REASON requires explicit --thread-id values")
    eligible = []
    rejected = []
    for item in threads or []:
        ids = thread_ids(item)
        if not (ids & wanted):
            continue
        if item.get("comments_complete") is False:
            rejected.append(item)
            continue
        if is_codex_or_helper_thread(item, gh_user):
            eligible.append(item)
        else:
            rejected.append(item)
    return eligible, rejected


def evaluate_review_clean(
    head_sha,
    reviews,
    comments,
    threads,
    issue_comments=None,
    completion_signals=None,
    gh_user="",
):
    issue_comments = issue_comments or []
    completion_signals = completion_signals or []
    reviews = latest_reviews_per_reviewer_commit(reviews)
    current = []
    old = []
    unbound = []
    for item in [*reviews, *comments, *issue_comments, *completion_signals]:
        bind_sha = item_review_sha(item)
        if bound_to_head(item, head_sha):
            current.append(item)
        elif bind_sha:
            old.append(item)
        else:
            unbound.append(item)

    live_unresolved = [
        item
        for item in threads
        if item.get("resolved") is False and item.get("outdated") is not True
    ]
    actionable = []
    ignored = []
    for item in [*current, *live_unresolved]:
        if item.get("kind") in COMPLETION_ONLY_KINDS:
            continue
        if is_disposition_reply(item.get("body")) and is_trusted_disposition_author(
            item.get("author"), gh_user
        ):
            continue
        fingerprint = finding_fingerprint(item)
        item_ignored = ignore_fingerprints_for_item(
            item, threads, gh_user=gh_user, head_sha=head_sha
        )
        if fingerprint and fingerprint in item_ignored:
            ignored.append(
                {
                    "fingerprint": fingerprint,
                    "disposition": DISPOSITION_IGNORE,
                    "id": item.get("id"),
                    "kind": item.get("kind"),
                    "path": item.get("path"),
                }
            )
            continue
        if is_actionable_text(
            item.get("body"),
            item.get("path"),
            item.get("state"),
            item.get("kind"),
            item.get("author"),
            gh_user,
            item.get("in_reply_to_id"),
        ):
            actionable.append(item)

    proof = next((item for item in current if is_codex_completion_proof(item, head_sha)), None)

    if actionable:
        reason = "actionable_review_on_current_head"
        review_clean = False
    elif proof is None:
        if old:
            reason = "only_old_head_reviews"
        else:
            reason = "no_current_head_review_proof"
        review_clean = False
    else:
        reason = "current_head_review_complete"
        review_clean = True

    return {
        "head_sha": head_sha,
        "review_clean": review_clean,
        "reason": reason,
        "proof": proof,
        "current_head_items": current,
        "old_head_items": old,
        "unbound_items": unbound,
        "unresolved_threads": live_unresolved,
        "actionable": actionable,
        "ignored": ignored,
    }


def _review_threads_connection(payload):
    return (
        (((payload or {}).get("data") or {}).get("repository") or {}).get("pullRequest") or {}
    ).get("reviewThreads") or {}


def fetch_review_threads(owner, name, number):
    nodes = []
    after = None
    for _ in range(THREAD_PAGE_LIMIT):
        args = [
            "api",
            "graphql",
            "-f",
            f"query={THREADS_QUERY}",
            "-f",
            f"owner={owner}",
            "-f",
            f"name={name}",
            "-F",
            f"number={int(number)}",
        ]
        if after:
            args.extend(["-f", f"after={after}"])
        payload = gh_json(args)
        connection = _review_threads_connection(payload)
        batch = connection.get("nodes") or []
        if not isinstance(batch, list):
            raise GhCommandError("Unexpected reviewThreads payload")
        nodes.extend(batch)
        page_info = connection.get("pageInfo") or {}
        if not page_info.get("hasNextPage"):
            return nodes
        after = page_info.get("endCursor")
        if not after:
            raise GhCommandError("reviewThreads pageInfo.hasNextPage without endCursor")
    raise GhCommandError(f"reviewThreads exceeded {THREAD_PAGE_LIMIT} pages")


def fetch_head_sha(pr):
    args = ["pr", "view", str(pr["number"]), "--json", "headRefOid"]
    repo = pr.get("repo")
    if repo:
        args.extend(["-R", repo])
    data = gh_json(args)
    if not isinstance(data, dict):
        raise GhCommandError("Unexpected PR payload from `gh pr view`")
    return str(data.get("headRefOid") or "")


def require_current_head(pr, expected_head):
    expected = str(expected_head or "")
    latest = fetch_head_sha(pr)
    if not expected or latest != expected:
        raise GhCommandError(f"PR HEAD changed before mutation: expected {expected} got {latest}")
    return latest


def load_live_threads(pr):
    return normalize_threads(fetch_review_threads(pr["owner"], pr["name"], pr["number"]))


def require_fresh_resolve_thread(pr, thread_id, expected_head):
    require_current_head(pr, expected_head)
    threads = load_live_threads(pr)
    # Recheck HEAD after thread fetch; pagination can race with a new push.
    require_current_head(pr, expected_head)
    eligible, rejected = eligible_codex_resolve_threads(
        threads, [thread_id], expected_head, expected_head
    )
    if rejected or not eligible:
        raise GhCommandError(
            "thread participants changed before mutation or thread is no longer Codex-only"
        )
    return eligible[0]


def require_fresh_ignore_thread(pr, thread_id, expected_head, gh_user=""):
    require_current_head(pr, expected_head)
    threads = load_live_threads(pr)
    # Recheck HEAD after thread fetch; pagination can race with a new push.
    require_current_head(pr, expected_head)
    eligible, rejected = eligible_codex_ignore_threads(
        threads, [thread_id], expected_head, expected_head, gh_user=gh_user
    )
    if rejected or not eligible:
        raise GhCommandError(
            "thread participants changed before mutation or thread is no longer eligible"
        )
    return eligible[0]


def resolve_review_thread(node_id):
    if not node_id:
        raise GhCommandError("missing GraphQL thread id")
    return gh_json(
        [
            "api",
            "graphql",
            "-f",
            f"query={RESOLVE_THREAD_MUTATION}",
            "-f",
            f"id={node_id}",
        ]
    )


def reply_review_thread(node_id, body):
    if not node_id:
        raise GhCommandError("missing GraphQL thread id")
    if not str(body or "").strip():
        raise GhCommandError("missing IGNORE_WITH_REASON reply body")
    return gh_json(
        [
            "api",
            "graphql",
            "-f",
            f"query={REPLY_THREAD_MUTATION}",
            "-f",
            f"id={node_id}",
            "-f",
            f"body={body}",
        ]
    )


def update_review_comment(comment_node_id, body):
    if not comment_node_id:
        raise GhCommandError("missing GraphQL review comment id")
    if not str(body or "").strip():
        raise GhCommandError("missing IGNORE_WITH_REASON reply body")
    return gh_json(
        [
            "api",
            "graphql",
            "-f",
            f"query={UPDATE_REVIEW_COMMENT_MUTATION}",
            "-f",
            f"id={comment_node_id}",
            "-f",
            f"body={body}",
        ]
    )


def fetch_comment_reactions(repo, comment_id):
    return gh_api_list(f"repos/{repo}/issues/comments/{comment_id}/reactions") or []


def collect_gate_inputs(pr):
    repo = pr["repo"]
    number = pr["number"]
    head_sha = pr["head_sha"]
    raw_reviews = gh_api_list(f"repos/{repo}/pulls/{number}/reviews")
    raw_comments = gh_api_list(f"repos/{repo}/pulls/{number}/comments")
    raw_issue_comments = gh_api_list(f"repos/{repo}/issues/{number}/comments")
    raw_threads = fetch_review_threads(pr["owner"], pr["name"], number)
    pending = pending_review_ids(raw_reviews)
    reactions_by_comment_id = {}
    for item in raw_issue_comments or []:
        if not isinstance(item, dict):
            continue
        body = str(item.get("body") or "")
        comment_id = str(item.get("id") or "")
        if comment_id and is_codex_review_request(body):
            reactions_by_comment_id[comment_id] = fetch_comment_reactions(repo, comment_id)
    issue_comments = normalize_issue_comments(raw_issue_comments, head_sha)
    return {
        "reviews": normalize_reviews(raw_reviews),
        "comments": normalize_review_comments(raw_comments, pending),
        "issue_comments": issue_comments,
        "threads": normalize_threads(raw_threads),
        "completion_signals": normalize_codex_completion_signals(
            issue_comments, reactions_by_comment_id, head_sha
        ),
    }


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Final current-HEAD review-clean gate")
    parser.add_argument("--pr", default="auto", help="auto, PR number, or PR URL")
    parser.add_argument("--repo", help="Optional OWNER/REPO override")
    parser.add_argument("--head", help="Current HEAD SHA; default is PR headRefOid")
    parser.add_argument("--json", action="store_true", help="JSON output (default)")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        pr = resolve_pr(args.pr, repo_override=args.repo, head_override=args.head)
        gh_user = fetch_authenticated_login()
        fetched = collect_gate_inputs(pr)
        latest_head = fetch_head_sha(pr)
        if latest_head != pr["head_sha"]:
            raise GhCommandError(
                f"PR HEAD changed during gate fetch: {pr['head_sha']} -> {latest_head}"
            )
        result = evaluate_review_clean(
            pr["head_sha"],
            fetched["reviews"],
            fetched["comments"],
            fetched["threads"],
            fetched["issue_comments"],
            fetched["completion_signals"],
            gh_user=gh_user,
        )
        result["pr"] = {"number": pr["number"], "repo": pr["repo"], "url": pr["url"]}
    except (GhCommandError, ValueError, json.JSONDecodeError) as err:
        sys.stderr.write(f"final_review_clean_gate.py error: {err}\n")
        return 2
    sys.stdout.write(json.dumps(result, sort_keys=True) + "\n")
    return 0 if result["review_clean"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
