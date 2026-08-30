import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

SKILL_ROOT = Path(__file__).resolve().parent.parent
LAUNCHER = Path(__file__).resolve().parent / "run-gh-pr-watch.py"
VENDOR_WATCHER = SKILL_ROOT / "vendor" / "openai-codex-babysit-pr" / "scripts" / "gh_pr_watch.py"
VENDOR_OFFICIAL_TEST = (
    SKILL_ROOT / "vendor" / "openai-codex-babysit-pr" / "scripts" / "test_gh_pr_watch.py"
)
WRAPPER_SKILL = SKILL_ROOT / "SKILL.md"
UPSTREAM = SKILL_ROOT / "UPSTREAM.md"
OFFICIAL_SKILL = SKILL_ROOT / "vendor" / "openai-codex-babysit-pr" / "SKILL.md"

PINNED_SHA = "a770e5b8470d3320eb53a56a286ea4a0a70a1f59"


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


launcher = load_module(LAUNCHER, "run_gh_pr_watch")
gh_pr_watch = load_module(VENDOR_WATCHER, "vendored_gh_pr_watch")


def sample_pr(**overrides):
    pr = {
        "number": 123,
        "url": "https://github.com/example/repo/pull/123",
        "repo": "example/repo",
        "head_sha": "abc123",
        "head_branch": "feature",
        "state": "OPEN",
        "merged": False,
        "closed": False,
        "mergeable": "MERGEABLE",
        "merge_state_status": "CLEAN",
        "review_decision": "",
    }
    pr.update(overrides)
    return pr


def sample_checks(**overrides):
    checks = {
        "pending_count": 0,
        "failed_count": 0,
        "passed_count": 12,
        "all_terminal": True,
    }
    checks.update(overrides)
    return checks


def test_launcher_resolves_vendored_watcher():
    assert launcher.watcher_path() == VENDOR_WATCHER
    assert VENDOR_WATCHER.is_file()


def test_launcher_does_not_reimplement_watcher():
    text = LAUNCHER.read_text(encoding="utf-8")
    assert "recommend_actions" not in text
    assert "retry_failed_now" not in text
    assert "fetch_new_review_items" not in text
    assert "os.execv" in text


def test_upstream_files_are_unpatched():
    official = OFFICIAL_SKILL.read_text(encoding="utf-8")
    assert "python3 .codex/skills/babysit-pr/scripts/gh_pr_watch.py" in official
    assert PINNED_SHA in UPSTREAM.read_text(encoding="utf-8")
    wrapper = WRAPPER_SKILL.read_text(encoding="utf-8")
    assert "scripts/run-gh-pr-watch.py" in wrapper
    assert "python3 .codex/skills/babysit-pr/scripts/gh_pr_watch.py --pr auto --watch" not in wrapper


def test_idle_pending_checks_are_not_a_stop():
    actions = gh_pr_watch.recommend_actions(
        sample_pr(),
        sample_checks(pending_count=3, all_terminal=False, passed_count=0),
        [],
        [],
        [],
        0,
        3,
    )
    assert actions == ["idle"]
    assert "stop_pr_closed" not in actions
    assert "ready_to_merge" not in actions


def test_empty_reviews_with_pending_ci_is_not_review_clean_ready():
    assert not gh_pr_watch.is_pr_ready_to_merge(
        sample_pr(),
        sample_checks(pending_count=4, all_terminal=False, passed_count=0),
        [],
    )


def test_retry_budget_is_per_head_sha():
    state = {}
    gh_pr_watch.set_retry_count(state, "oldsha", 3)
    assert gh_pr_watch.current_retry_count(state, "oldsha") == 3
    assert gh_pr_watch.current_retry_count(state, "newsha") == 0


def test_retry_failed_now_skips_when_new_head_has_no_failed_runs(monkeypatch, tmp_path):
    snapshot = {
        "pr": sample_pr(head_sha="newsha"),
        "checks": sample_checks(failed_count=1),
        "failed_runs": [],
        "failed_jobs": [],
        "new_review_items": [],
        "retry_state": {"current_sha_retries_used": 0, "max_flaky_retries": 3},
    }
    monkeypatch.setattr(
        gh_pr_watch,
        "collect_snapshot",
        lambda args: (snapshot, tmp_path / "state.json"),
    )
    called = []
    monkeypatch.setattr(gh_pr_watch, "gh_text", lambda *a, **k: called.append((a, k)))

    result = gh_pr_watch.retry_failed_now(
        type("Args", (), {"pr": "1", "repo": None, "state_file": None, "max_flaky_retries": 3})()
    )
    assert result["reason"] == "no_failed_runs"
    assert called == []
    assert result["rerun_attempted"] is False


def test_wrapper_policy_strings():
    text = WRAPPER_SKILL.read_text(encoding="utf-8")
    required = [
        "vendor/openai-codex-babysit-pr/SKILL.md",
        "scripts/run-gh-pr-watch.py",
        "一時的な `idle`",
        "review-clean と判定しない",
        "過去 HEAD の review 結果を新 HEAD へ流用しない",
        "branch 起因ならコードを直す",
        "merge可能。最終merge判断は人間。",
        "人間 reviewer のコメントへ返信せず",
        "gh workflow run",
        "retry_failed_checks",
        "@codex review",
        "AUTO_FIX",
        "ASK_HUMAN",
    ]
    missing = [item for item in required if item not in text]
    assert missing == []
    assert "gh pr merge" not in text


def test_babysit_pr_is_not_a_top_level_global_skill():
    global_skills = SKILL_ROOT.parent
    assert not (global_skills / "babysit-pr" / "SKILL.md").exists()


def test_official_unit_tests_are_present():
    assert VENDOR_OFFICIAL_TEST.is_file()
    assert "test_pending_review_feedback_surfaces_only_after_publication" in VENDOR_OFFICIAL_TEST.read_text(
        encoding="utf-8"
    )
