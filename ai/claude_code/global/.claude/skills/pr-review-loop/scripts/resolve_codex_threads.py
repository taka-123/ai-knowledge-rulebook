#!/usr/bin/env python3
"""Resolve Codex bot review threads after AUTO_FIX + commit + push.

Human reviewer threads are refused. This helper only calls
resolveReviewThread for Codex bot threads whose IDs were given explicitly
and whose PR HEAD already matches --head. It does not submit reviews,
reply, merge, or resolve other authors.
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
    parser = argparse.ArgumentParser(description="Resolve AUTO_FIX'd Codex bot review threads")
    parser.add_argument("--pr", required=True, help="auto, PR number, or PR URL")
    parser.add_argument("--repo", help="Optional OWNER/REPO override")
    parser.add_argument("--head", required=True, help="Pushed current HEAD SHA")
    parser.add_argument(
        "--thread-id",
        action="append",
        required=True,
        help="GraphQL review thread id (repeatable). Human threads are refused.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        pr = gate.resolve_pr(args.pr, repo_override=args.repo)
        current_head = pr["head_sha"]
        raw_threads = gate.fetch_review_threads(pr["owner"], pr["name"], pr["number"])
        threads = gate.normalize_threads(raw_threads)
        eligible, rejected = gate.eligible_codex_resolve_threads(
            threads, args.thread_id, args.head, current_head
        )
        if rejected:
            authors = ", ".join(sorted({str(item.get("author") or "") for item in rejected}))
            raise gate.GhCommandError(
                f"refusing to resolve non-Codex review thread(s) (authors: {authors})"
            )
        if not eligible:
            raise gate.GhCommandError("no eligible Codex bot threads for the given --thread-id")
        resolved = []
        for item in eligible:
            node_id = str(item.get("node_id") or "")
            gate.require_current_head(pr, args.head)
            gate.resolve_review_thread(node_id)
            resolved.append({"node_id": node_id, "author": item.get("author")})
    except (gate.GhCommandError, ValueError, json.JSONDecodeError) as err:
        sys.stderr.write(f"resolve_codex_threads.py error: {err}\n")
        return 2
    sys.stdout.write(json.dumps({"resolved": resolved, "head_sha": args.head}, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
