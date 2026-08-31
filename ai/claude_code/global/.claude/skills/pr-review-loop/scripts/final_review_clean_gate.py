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
THREADS_QUERY = """
query($owner: String!, $name: String!, $number: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      reviewThreads(first: 100) {
        nodes {
          isResolved
          isOutdated
          comments(first: 20) {
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
    owner = ((data.get("headRepositoryOwner") or {}).get("login")) or ""
    name = ((data.get("headRepository") or {}).get("name")) or ""
    if repo_override and "/" in repo_override:
        owner, name = repo_override.split("/", 1)
    return {
        "number": int(data.get("number")),
        "repo": f"{owner}/{name}",
        "owner": owner,
        "name": name,
        "head_sha": head_override or str(data.get("headRefOid") or ""),
        "url": str(data.get("url") or ""),
    }


def is_summary_only(body, path=None):
    if path:
        return False
    lower = (body or "").lower()
    return any(marker in lower for marker in SUMMARY_MARKERS)


def is_actionable_text(body, path=None, review_state=None):
    if is_summary_only(body, path):
        return False
    if path:
        return True
    if str(review_state or "").upper() == "CHANGES_REQUESTED":
        return True
    lower = (body or "").lower()
    return any(marker in lower for marker in ACTIONABLE_MARKERS)


def normalize_reviews(payload):
    out = []
    for item in payload or []:
        if not isinstance(item, dict):
            continue
        state = str(item.get("state") or "").upper()
        if state == PENDING:
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


def normalize_issue_comments(payload):
    out = []
    for item in payload or []:
        if not isinstance(item, dict):
            continue
        out.append(
            {
                "kind": "issue_comment",
                "id": str(item.get("id") or ""),
                "author": extract_login(item.get("user")),
                "author_association": str(item.get("author_association") or ""),
                "state": "",
                "commit_id": "",
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


def normalize_threads(payload):
    out = []
    for thread in payload or []:
        if not isinstance(thread, dict):
            continue
        comments = thread.get("comments")
        if isinstance(comments, dict):
            comments = comments.get("nodes") or []
        first = comments[0] if comments else {}
        author = first.get("author") if isinstance(first, dict) else {}
        commit = first.get("commit") if isinstance(first, dict) else {}
        original = first.get("originalCommit") if isinstance(first, dict) else {}
        out.append(
            {
                "kind": "review_thread",
                "id": str((first or {}).get("databaseId") or ""),
                "author": extract_login(author),
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


def evaluate_review_clean(head_sha, reviews, comments, threads, issue_comments=None):
    issue_comments = issue_comments or []
    current = []
    old = []
    unbound = []
    for item in [*reviews, *comments, *issue_comments]:
        commit_id = str(item.get("commit_id") or "")
        if bound_to_head(item, head_sha):
            current.append(item)
        elif commit_id:
            old.append(item)
        else:
            unbound.append(item)

    live_unresolved = [
        item
        for item in threads
        if item.get("resolved") is False and item.get("outdated") is not True
    ]
    actionable = []
    for item in [*current, *live_unresolved]:
        if is_actionable_text(item.get("body"), item.get("path"), item.get("state")):
            actionable.append(item)

    current_reviews = [
        item
        for item in current
        if item.get("kind") == "review" and not is_summary_only(item.get("body"), item.get("path"))
    ]
    proof = current_reviews[0] if current_reviews else None

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


def fetch_review_threads(owner, name, number):
    payload = gh_json(
        [
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
    )
    nodes = (
        (((payload or {}).get("data") or {}).get("repository") or {}).get("pullRequest") or {}
    ).get("reviewThreads") or {}
    return nodes.get("nodes") or []


def collect_gate_inputs(pr):
    repo = pr["repo"]
    number = pr["number"]
    raw_reviews = gh_api_list(f"repos/{repo}/pulls/{number}/reviews")
    raw_comments = gh_api_list(f"repos/{repo}/pulls/{number}/comments")
    raw_issue_comments = gh_api_list(f"repos/{repo}/issues/{number}/comments")
    raw_threads = fetch_review_threads(pr["owner"], pr["name"], number)
    pending = pending_review_ids(raw_reviews)
    return {
        "reviews": normalize_reviews(raw_reviews),
        "comments": normalize_review_comments(raw_comments, pending),
        "issue_comments": normalize_issue_comments(raw_issue_comments),
        "threads": normalize_threads(raw_threads),
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
        result = evaluate_review_clean(
            pr["head_sha"],
            fetched["reviews"],
            fetched["comments"],
            fetched["threads"],
            fetched["issue_comments"],
        )
        result["pr"] = {"number": pr["number"], "repo": pr["repo"], "url": pr["url"]}
    except (GhCommandError, ValueError, json.JSONDecodeError) as err:
        sys.stderr.write(f"final_review_clean_gate.py error: {err}\n")
        return 2
    sys.stdout.write(json.dumps(result, sort_keys=True) + "\n")
    return 0 if result["review_clean"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
