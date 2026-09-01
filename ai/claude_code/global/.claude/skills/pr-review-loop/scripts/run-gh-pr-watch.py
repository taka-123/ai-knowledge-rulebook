#!/usr/bin/env python3
"""Launch the vendored OpenAI gh_pr_watch.py from any install location.

Official babysit-pr documents repo-relative `.codex/skills/babysit-pr/...`.
This rulebook syncs the skill to `ai/.../skills/pr-review-loop/` (and copies
to `~/.claude/skills/` or `<project>/.claude/skills/`). Resolve the watcher
from this launcher file so discovery path does not rewrite upstream files.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

LAUNCHER = Path(__file__).resolve()
VENDOR_WATCHER = (
    LAUNCHER.parent.parent
    / "vendor"
    / "openai-codex-babysit-pr"
    / "scripts"
    / "gh_pr_watch.py"
)


RETRY_OPTION = "--retry-failed-now"


def watcher_path() -> Path:
    return VENDOR_WATCHER


def is_retry_mode_arg(arg: str) -> bool:
    if arg == RETRY_OPTION:
        return True
    # argparse unique prefixes: --retry-f / --retry-failed-n / --ret ...
    return arg.startswith("--ret") and RETRY_OPTION.startswith(arg)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if any(is_retry_mode_arg(arg) for arg in args):
        sys.stderr.write(
            "refusing --retry-failed-now: vendor does not verify flaky/unrelated classification\n"
        )
        return 2
    watcher = watcher_path()
    if not watcher.is_file():
        sys.stderr.write(f"vendored gh_pr_watch.py not found: {watcher}\n")
        return 2
    os.execv(sys.executable, [sys.executable, str(watcher), *args])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
