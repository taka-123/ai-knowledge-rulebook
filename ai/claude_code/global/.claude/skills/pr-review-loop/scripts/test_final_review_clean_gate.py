import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("final_review_clean_gate.py")
MODULE_SPEC = importlib.util.spec_from_file_location("final_review_clean_gate", MODULE_PATH)
gate = importlib.util.module_from_spec(MODULE_SPEC)
assert MODULE_SPEC.loader is not None
MODULE_SPEC.loader.exec_module(gate)

evaluate_review_clean = gate.evaluate_review_clean
normalize_review_comments = gate.normalize_review_comments
normalize_reviews = gate.normalize_reviews
normalize_threads = gate.normalize_threads
pending_review_ids = gate.pending_review_ids


HEAD = "newsha"
OLD = "oldsha"


def review(**overrides):
    item = {
        "kind": "review",
        "id": "10",
        "author": "chatgpt-codex-connector[bot]",
        "author_association": "NONE",
        "state": "COMMENTED",
        "commit_id": HEAD,
        "original_commit_id": "",
        "path": None,
        "line": None,
        "resolved": None,
        "outdated": None,
        "body": "No issues found.",
        "url": "",
    }
    item.update(overrides)
    return item


def comment(**overrides):
    item = {
        "kind": "review_comment",
        "id": "20",
        "author": "coderabbitai[bot]",
        "author_association": "NONE",
        "state": "",
        "commit_id": HEAD,
        "original_commit_id": HEAD,
        "path": "src/app.py",
        "line": 4,
        "resolved": False,
        "outdated": False,
        "body": "Please rename this.",
        "url": "",
    }
    item.update(overrides)
    return item


def thread(**overrides):
    item = {
        "kind": "review_thread",
        "id": "30",
        "author": "coderabbitai[bot]",
        "author_association": "",
        "state": "",
        "commit_id": HEAD,
        "original_commit_id": HEAD,
        "path": "src/app.py",
        "line": None,
        "resolved": False,
        "outdated": False,
        "body": "Please rename this.",
        "url": "",
    }
    item.update(overrides)
    return item


def test_empty_reviews_are_not_review_clean():
    result = evaluate_review_clean(HEAD, [], [], [], [])
    assert result["review_clean"] is False
    assert result["reason"] == "no_current_head_review_proof"
    assert result["proof"] is None


def test_old_head_no_issues_is_not_used_for_new_head():
    result = evaluate_review_clean(
        HEAD,
        [review(commit_id=OLD, body="No issues found.")],
        [],
        [],
    )
    assert result["review_clean"] is False
    assert result["reason"] == "only_old_head_reviews"
    assert result["old_head_items"][0]["commit_id"] == OLD
    assert result["current_head_items"] == []


def test_coderabbit_walkthrough_only_is_not_proof():
    walkthrough = {
        "kind": "issue_comment",
        "id": "1",
        "author": "coderabbitai[bot]",
        "author_association": "NONE",
        "state": "",
        "commit_id": "",
        "original_commit_id": "",
        "path": None,
        "line": None,
        "resolved": None,
        "outdated": None,
        "body": "Walkthrough\n<!-- This is an auto-generated comment: summarize by coderabbit.ai -->",
        "url": "",
    }
    result = evaluate_review_clean(HEAD, [], [], [], [walkthrough])
    assert result["review_clean"] is False
    assert result["reason"] == "no_current_head_review_proof"
    assert result["actionable"] == []


def test_coderabbit_actionable_on_current_head_blocks():
    result = evaluate_review_clean(
        HEAD,
        [review()],
        [comment()],
        [],
    )
    assert result["review_clean"] is False
    assert result["reason"] == "actionable_review_on_current_head"
    assert result["actionable"][0]["author"] == "coderabbitai[bot]"
    assert result["actionable"][0]["commit_id"] == HEAD


def test_contributor_external_reviewer_is_not_dropped():
    external = comment(
        author="outside-reviewer",
        author_association="CONTRIBUTOR",
        body="This breaks the public API.",
    )
    result = evaluate_review_clean(HEAD, [review()], [external], [])
    assert result["review_clean"] is False
    assert result["actionable"][0]["author"] == "outside-reviewer"
    assert result["actionable"][0]["author_association"] == "CONTRIBUTOR"


def test_pending_review_and_its_comments_are_ignored():
    raw_reviews = [
        {"id": 99, "state": "PENDING", "commit_id": HEAD, "user": {"login": "human"}, "body": "draft"}
    ]
    raw_comments = [
        {
            "id": 100,
            "pull_request_review_id": 99,
            "commit_id": HEAD,
            "user": {"login": "human"},
            "path": "a.py",
            "line": 1,
            "body": "draft comment",
        }
    ]
    pending = pending_review_ids(raw_reviews)
    reviews = normalize_reviews(raw_reviews)
    comments = normalize_review_comments(raw_comments, pending)
    result = evaluate_review_clean(HEAD, reviews, comments, [])
    assert reviews == []
    assert comments == []
    assert result["review_clean"] is False
    assert result["reason"] == "no_current_head_review_proof"


def test_unresolved_live_thread_blocks_even_for_filtered_bots():
    result = evaluate_review_clean(HEAD, [review()], [], [thread()])
    assert result["review_clean"] is False
    assert result["reason"] == "actionable_review_on_current_head"
    assert result["unresolved_threads"][0]["author"] == "coderabbitai[bot]"


def test_outdated_unresolved_thread_does_not_prove_or_block_alone():
    result = evaluate_review_clean(
        HEAD,
        [],
        [],
        [thread(outdated=True, commit_id=OLD, original_commit_id=OLD)],
    )
    assert result["review_clean"] is False
    assert result["reason"] == "no_current_head_review_proof"
    assert result["unresolved_threads"] == []


def test_coderabbit_walkthrough_review_on_head_is_not_proof():
    result = evaluate_review_clean(
        HEAD,
        [
            review(
                author="coderabbitai[bot]",
                body="Walkthrough\n<!-- This is an auto-generated comment: summarize by coderabbit.ai -->",
            )
        ],
        [],
        [],
    )
    assert result["review_clean"] is False
    assert result["reason"] == "no_current_head_review_proof"
    assert result["proof"] is None
    result = evaluate_review_clean(HEAD, [review()], [], [])
    assert result["review_clean"] is True
    assert result["reason"] == "current_head_review_complete"
    assert result["proof"]["commit_id"] == HEAD
    assert result["proof"]["author"] == "chatgpt-codex-connector[bot]"


def test_codex_about_footer_is_still_current_head_proof():
    result = evaluate_review_clean(
        HEAD,
        [
            review(
                body="No issues found.\n\nAbout Codex in GitHub\nhttps://github.com/features/codex"
            )
        ],
        [],
        [],
    )
    assert result["review_clean"] is True
    assert result["reason"] == "current_head_review_complete"
    assert result["proof"]["commit_id"] == HEAD


def test_coderabbit_changes_requested_on_current_head_blocks():
    result = evaluate_review_clean(
        HEAD,
        [
            review(
                author="coderabbitai[bot]",
                state="CHANGES_REQUESTED",
                body="Found issues that must be fixed.",
            )
        ],
        [],
        [],
    )
    assert result["review_clean"] is False
    assert result["reason"] == "actionable_review_on_current_head"
    assert result["actionable"][0]["author"] == "coderabbitai[bot]"
    assert result["actionable"][0]["commit_id"] == HEAD


def test_normalize_keeps_commit_ids():
    reviews = normalize_reviews(
        [
            {
                "id": 7,
                "state": "COMMENTED",
                "commit_id": HEAD,
                "user": {"login": "octocat"},
                "author_association": "CONTRIBUTOR",
                "body": "Looks good",
                "html_url": "https://example.test/7",
            }
        ]
    )
    assert reviews[0]["commit_id"] == HEAD
    comments = normalize_review_comments(
        [
            {
                "id": 8,
                "pull_request_review_id": 7,
                "commit_id": HEAD,
                "original_commit_id": OLD,
                "user": {"login": "octocat"},
                "path": "x.py",
                "line": 3,
                "body": "nit",
            }
        ],
        set(),
    )
    assert comments[0]["commit_id"] == HEAD
    assert comments[0]["original_commit_id"] == OLD


def test_normalize_threads_keeps_commit_and_unresolved():
    threads = normalize_threads(
        [
            {
                "isResolved": False,
                "isOutdated": False,
                "comments": {
                    "nodes": [
                        {
                            "databaseId": 44,
                            "body": "Fix this race.",
                            "path": "src/a.py",
                            "author": {"login": "coderabbitai[bot]"},
                            "commit": {"oid": HEAD},
                            "originalCommit": {"oid": OLD},
                        }
                    ]
                },
            }
        ]
    )
    assert threads[0]["commit_id"] == HEAD
    assert threads[0]["original_commit_id"] == OLD
    assert threads[0]["resolved"] is False
