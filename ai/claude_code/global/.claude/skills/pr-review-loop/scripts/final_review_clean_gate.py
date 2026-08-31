#!/usr/bin/env python3
"""Final review-clean gate for pr-review-loop.

Official babysit-pr is the monitoring source of truth and stays unmodified.
This gate runs only immediately before completion. It re-fetches published
reviews from GitHub, including bots and external reviewers that the official
watcher may omit, and binds them to current HEAD via commit_id.
"""

from __future__ import annotations

import argparse
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
)
ACTIONABLE_MARKERS = (
    "![p0 badge]",
    "![p1 badge]",
    "![p2 badge]",
    "changes requested",
)
PENDING = "PENDING"
DISMISSED = "DISMISSED"
VALID_PROOF_REVIEW_STATES = {"COMMENTED", "APPROVED"}
THUMBS_UP = {"+1", "THUMBS_UP", "thumbs_up"}
CODEX_REVIEW_REQUEST_RE = re.compile(r"@codex\s+review\b", re.IGNORECASE)
HEAD_FIELD_RE = re.compile(r"(?im)(?:^|\b)head\s*[:=]\s*([0-9a-f]{7,40})\b")
SHA_RE = re.compile(r"\b([0-9a-f]{7,40})\b", re.IGNORECASE)
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
              databaseId
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
    args = ["pr", "view", "--json", "number,url,headRefOid,headRepository,headRepositoryOwner"]
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
    return {
        "number": int(data.get("number")),
        "repo": repo,
        "owner": owner,
        "name": name,
        "head_sha": actual_head,
        "url": pr_url,
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
    field = HEAD_FIELD_RE.search(text)
    if field:
        return canonicalize_sha(field.group(1), head_sha)
    if head_sha and head_sha.lower() in text.lower():
        return head_sha
    matches = SHA_RE.findall(text)
    full = [item for item in matches if len(item) == 40]
    if len(full) == 1:
        return canonicalize_sha(full[0], head_sha)
    return ""


def is_summary_only(body, path=None):
    if path:
        return False
    lower = (body or "").lower()
    return any(marker in lower for marker in SUMMARY_MARKERS)


def is_approval_only(body):
    return bool(APPROVAL_ONLY_RE.match((body or "").strip()))


def is_actionable_text(body, path=None, review_state=None, kind=None, author=None):
    if is_summary_only(body, path):
        return False
    if path:
        return True
    if str(review_state or "").upper() == "CHANGES_REQUESTED":
        return True
    lower = (body or "").lower()
    if any(marker in lower for marker in ACTIONABLE_MARKERS):
        return True
    if kind != "review" or is_codex_reviewer(author):
        return False
    text = (body or "").strip()
    if not text or is_approval_only(text):
        return False
    return True


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
            }
        )
    return out


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
        commit_id = extract_bound_sha(body, head_sha) if is_codex_review_request(body) else ""
        out.append(
            {
                "kind": "issue_comment",
                "id": str(item.get("id") or ""),
                "author": extract_login(item.get("user")),
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
        for comment in comments or []:
            if not isinstance(comment, dict):
                continue
            login = extract_login(comment.get("author"))
            if login:
                authors.append(login)
            comment_id = comment.get("databaseId")
            if comment_id not in (None, ""):
                comment_ids.append(str(comment_id))
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


def normalize_codex_completion_signals(issue_comments, reactions_by_comment_id, head_sha=""):
    out = []
    for comment in issue_comments or []:
        if not isinstance(comment, dict):
            continue
        body = str(comment.get("body") or "")
        if not is_codex_review_request(body):
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


def bound_to_head(item, head_sha):
    commit_id = str(item.get("commit_id") or "")
    return bool(head_sha) and commit_id == head_sha


def is_codex_completion_proof(item, head_sha):
    if not bound_to_head(item, head_sha):
        return False
    if not is_codex_reviewer(item.get("author")):
        return False
    kind = item.get("kind")
    if kind == "review":
        state = str(item.get("state") or "").upper()
        if state not in VALID_PROOF_REVIEW_STATES:
            return False
        if is_summary_only(item.get("body"), item.get("path")):
            return False
        return True
    if kind == "codex_thumbs_up" and str(item.get("content") or "") in THUMBS_UP:
        return True
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
        if is_codex_only_thread(item):
            eligible.append(item)
        else:
            rejected.append(item)
    return eligible, rejected


def evaluate_review_clean(
    head_sha, reviews, comments, threads, issue_comments=None, completion_signals=None
):
    issue_comments = issue_comments or []
    completion_signals = completion_signals or []
    current = []
    old = []
    unbound = []
    for item in [*reviews, *comments, *issue_comments, *completion_signals]:
        commit_id = str(item.get("commit_id") or "")
        if bound_to_head(item, head_sha):
            current.append(item)
        elif commit_id:
            old.append(item)
        else:
            unbound.append(item)

    resolved_ids = set()
    for item in threads or []:
        if item.get("resolved") is not True:
            continue
        for comment_id in item.get("comment_ids") or []:
            if comment_id not in (None, ""):
                resolved_ids.add(str(comment_id))
        thread_comment_id = str(item.get("id") or "")
        if thread_comment_id:
            resolved_ids.add(thread_comment_id)

    live_unresolved = [
        item
        for item in threads
        if item.get("resolved") is False and item.get("outdated") is not True
    ]
    current_unresolved = [
        item
        for item in current
        if not (item.get("kind") == "review_comment" and str(item.get("id") or "") in resolved_ids)
    ]
    actionable = []
    for item in [*current_unresolved, *live_unresolved]:
        if is_actionable_text(
            item.get("body"),
            item.get("path"),
            item.get("state"),
            item.get("kind"),
            item.get("author"),
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
        )
        result["pr"] = {"number": pr["number"], "repo": pr["repo"], "url": pr["url"]}
    except (GhCommandError, ValueError, json.JSONDecodeError) as err:
        sys.stderr.write(f"final_review_clean_gate.py error: {err}\n")
        return 2
    sys.stdout.write(json.dumps(result, sort_keys=True) + "\n")
    return 0 if result["review_clean"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
