#!/usr/bin/env python3
"""Reply with IGNORE_WITH_REASON on Codex-only threads, then resolve.

Idempotent for the same review thread + finding fingerprint: HEAD changes
re-validate, then update the existing helper reply instead of posting another.
AUTO_FIX does not use this helper and must not post a review reply.
Human, CodeRabbit, mixed, and truncated threads are refused. ASK_HUMAN
findings must not be passed in.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


def load_gate():
    path = Path(__file__).with_name("final_review_clean_gate.py")
    spec = importlib.util.spec_from_file_location("final_review_clean_gate", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


gate = load_gate()


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="IGNORE_WITH_REASON Codex-only review threads")
    parser.add_argument("--pr", required=True, help="auto, PR number, or PR URL")
    parser.add_argument("--repo", help="Optional OWNER/REPO override")
    parser.add_argument("--head", required=True, help="Current HEAD SHA")
    parser.add_argument("--reason", required=True, help="Short concrete reason shown on GitHub")
    parser.add_argument(
        "--thread-id",
        action="append",
        required=True,
        help="GraphQL review thread id (repeatable). Human threads are refused.",
    )
    parser.add_argument(
        "--no-resolve",
        action="store_true",
        help="Reply only; skip resolveReviewThread",
    )
    return parser.parse_args(argv)


def ensure_ignore_reply(fresh, fingerprint, reason, head_sha, gh_user):
    """Create or rebind one human-facing IGNORE reply for this thread."""
    desired = gate.format_ignore_reply(reason, fingerprint, head_sha)
    existing = gate.trusted_ignore_replies_on_thread(fresh, fingerprint, gh_user=gh_user)
    if existing:
        target = existing[0]
        if not target.get("comment_node_id"):
            raise gate.GhCommandError(
                "existing IGNORE reply is missing GraphQL comment id; refusing duplicate reply"
            )
        rebound = gate.rebind_ignore_reply(target["body"], reason, fingerprint, head_sha)
        if rebound == target["body"]:
            return {"created": False, "updated": False, "body": rebound}
        gate.update_review_comment(target["comment_node_id"], rebound)
        return {"created": False, "updated": True, "body": rebound}
    gate.reply_review_thread(str(fresh.get("node_id") or ""), desired)
    return {"created": True, "updated": False, "body": desired}


def main(argv=None):
    args = parse_args(argv)
    try:
        pr = gate.resolve_pr(args.pr, repo_override=args.repo, head_override=args.head)
        raw_threads = gate.fetch_review_threads(pr["owner"], pr["name"], pr["number"])
        threads = gate.normalize_threads(raw_threads)
        gh_user = gate.fetch_authenticated_login()
        eligible, rejected = gate.eligible_codex_ignore_threads(
            threads, args.thread_id, pr["head_sha"], args.head, gh_user=gh_user
        )
        if rejected:
            authors = ", ".join(sorted({str(item.get("author") or "") for item in rejected}))
            raise gate.GhCommandError(
                f"refusing IGNORE_WITH_REASON on non-Codex or incomplete thread(s) (authors: {authors})"
            )
        if not eligible:
            raise gate.GhCommandError("no eligible Codex-only threads for the given --thread-id")
        ignored = []
        for item in eligible:
            node_id = str(item.get("node_id") or "")
            fresh = gate.require_fresh_ignore_thread(pr, node_id, args.head, gh_user=gh_user)
            fingerprint = gate.finding_fingerprint(fresh)
            gate.require_current_head(pr, args.head)
            mutation = ensure_ignore_reply(
                fresh, fingerprint, args.reason, args.head, gh_user
            )
            resolved = bool(fresh.get("resolved"))
            resolve_error = None
            if not args.no_resolve and not resolved:
                try:
                    fresh = gate.require_fresh_ignore_thread(
                        pr, node_id, args.head, gh_user=gh_user
                    )
                    gate.require_current_head(pr, args.head)
                    gate.resolve_review_thread(str(fresh.get("node_id") or node_id))
                    resolved = True
                except gate.GhCommandError as err:
                    resolve_error = str(err)
                    resolved = False
            record = {
                "node_id": node_id,
                "author": item.get("author"),
                "fingerprint": fingerprint,
                "disposition": gate.DISPOSITION_IGNORE,
                "replied": True,
                "created": mutation["created"],
                "updated": mutation["updated"],
                "resolved": resolved,
            }
            if resolve_error:
                record["resolve_error"] = resolve_error
            ignored.append(record)
    except (gate.GhCommandError, ValueError, json.JSONDecodeError) as err:
        sys.stderr.write(f"ignore_codex_threads.py error: {err}\n")
        return 2
    sys.stdout.write(
        json.dumps({"ignored": ignored, "head_sha": args.head}, sort_keys=True) + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
