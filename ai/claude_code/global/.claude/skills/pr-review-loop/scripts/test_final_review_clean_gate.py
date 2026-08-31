import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).with_name("final_review_clean_gate.py")
MODULE_SPEC = importlib.util.spec_from_file_location("final_review_clean_gate", MODULE_PATH)
gate = importlib.util.module_from_spec(MODULE_SPEC)
assert MODULE_SPEC.loader is not None
MODULE_SPEC.loader.exec_module(gate)

evaluate_review_clean = gate.evaluate_review_clean
eligible_codex_resolve_threads = gate.eligible_codex_resolve_threads
is_codex_review_request = gate.is_codex_review_request
is_codex_reviewer = gate.is_codex_reviewer
normalize_codex_completion_signals = gate.normalize_codex_completion_signals
normalize_issue_comments = gate.normalize_issue_comments
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
        "node_id": "PRRT_codex_or_bot",
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
    if "authors" not in overrides:
        item["authors"] = [item["author"]] if item.get("author") else []
    return item


def thumbs(**overrides):
    item = {
        "kind": "codex_thumbs_up",
        "id": "40",
        "author": "chatgpt-codex-connector[bot]",
        "author_association": "",
        "state": "",
        "commit_id": HEAD,
        "original_commit_id": "",
        "path": None,
        "line": None,
        "resolved": None,
        "outdated": None,
        "body": f"@codex review\nhead: {HEAD}",
        "url": "",
        "content": "+1",
        "request_id": "99",
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
                "id": "PRRT_kwtest",
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
    assert threads[0]["node_id"].startswith("PRRT_")
    assert threads[0]["authors"] == ["coderabbitai[bot]"]
    assert threads[0]["comment_ids"] == ["44"]


def test_current_head_codex_thumbs_up_is_clean():
    result = evaluate_review_clean(HEAD, [], [], [], [], [thumbs()])
    assert result["review_clean"] is True
    assert result["reason"] == "current_head_review_complete"
    assert result["proof"]["kind"] == "codex_thumbs_up"
    assert result["proof"]["commit_id"] == HEAD
    assert result["proof"]["author"] == "chatgpt-codex-connector[bot]"


def test_old_head_codex_thumbs_up_is_not_clean():
    result = evaluate_review_clean(HEAD, [], [], [], [], [thumbs(commit_id=OLD)])
    assert result["review_clean"] is False
    assert result["reason"] == "only_old_head_reviews"
    assert result["proof"] is None
    assert result["old_head_items"][0]["kind"] == "codex_thumbs_up"


def test_unrelated_reaction_is_not_codex_completion_proof():
    human_plus = thumbs(author="alice", content="+1")
    heart = thumbs(content="heart")
    result = evaluate_review_clean(HEAD, [], [], [], [], [human_plus, heart])
    assert result["review_clean"] is False
    assert result["proof"] is None
    assert result["reason"] == "no_current_head_review_proof"


def test_human_commented_review_is_not_codex_completion_proof():
    result = evaluate_review_clean(
        HEAD,
        [review(author="alice", author_association="MEMBER", body="Looks fine.")],
        [],
        [],
    )
    assert result["review_clean"] is False
    assert result["proof"] is None
    assert result["reason"] == "no_current_head_review_proof"
    assert result["actionable"] == []


def test_coderabbit_review_is_not_codex_completion_proof():
    result = evaluate_review_clean(
        HEAD,
        [review(author="coderabbitai[bot]", body="Looks good to me.")],
        [],
        [],
    )
    assert result["review_clean"] is False
    assert result["proof"] is None
    assert result["reason"] == "no_current_head_review_proof"


def test_codex_bot_unresolved_thread_blocks():
    result = evaluate_review_clean(
        HEAD,
        [review()],
        [],
        [thread(author="chatgpt-codex-connector[bot]", node_id="PRRT_codex1")],
    )
    assert result["review_clean"] is False
    assert result["reason"] == "actionable_review_on_current_head"
    assert result["unresolved_threads"][0]["author"] == "chatgpt-codex-connector[bot]"


def test_resolving_codex_bot_thread_after_fix_unblocks():
    open_thread = thread(author="chatgpt-codex-connector[bot]", node_id="PRRT_codex1")
    blocked = evaluate_review_clean(HEAD, [review()], [], [open_thread])
    assert blocked["review_clean"] is False
    eligible, rejected = eligible_codex_resolve_threads(
        [open_thread],
        requested_ids=["PRRT_codex1"],
        pushed_head_sha=HEAD,
        current_head_sha=HEAD,
    )
    assert rejected == []
    assert [item["node_id"] for item in eligible] == ["PRRT_codex1"]
    resolved = thread(
        author="chatgpt-codex-connector[bot]", node_id="PRRT_codex1", resolved=True
    )
    clean = evaluate_review_clean(HEAD, [review()], [], [resolved])
    assert clean["review_clean"] is True
    assert clean["unresolved_threads"] == []


def test_human_unresolved_thread_is_not_auto_resolved():
    human = thread(author="alice", author_association="MEMBER", node_id="PRRT_human")
    eligible, rejected = eligible_codex_resolve_threads(
        [human],
        requested_ids=["PRRT_human"],
        pushed_head_sha=HEAD,
        current_head_sha=HEAD,
    )
    assert eligible == []
    assert rejected[0]["author"] == "alice"
    result = evaluate_review_clean(HEAD, [review()], [], [human])
    assert result["review_clean"] is False
    assert result["unresolved_threads"][0]["author"] == "alice"


def test_resolve_requires_pushed_current_head():
    bot = thread(author="chatgpt-codex-connector[bot]", node_id="PRRT_codex1")
    with pytest.raises(ValueError, match="commit \\+ push"):
        eligible_codex_resolve_threads(
            [bot],
            requested_ids=["PRRT_codex1"],
            pushed_head_sha=OLD,
            current_head_sha=HEAD,
        )


def load_resolve_helper():
    path = Path(__file__).with_name("resolve_codex_threads.py")
    spec = importlib.util.spec_from_file_location("resolve_codex_threads", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_resolve_helper_does_not_resolve_human_threads(monkeypatch):
    helper = load_resolve_helper()
    human = thread(author="alice", node_id="PRRT_human")
    monkeypatch.setattr(
        helper.gate,
        "resolve_pr",
        lambda *a, **k: {
            "number": 8,
            "repo": "example/repo",
            "owner": "example",
            "name": "repo",
            "head_sha": HEAD,
            "url": "",
        },
    )
    monkeypatch.setattr(helper.gate, "fetch_review_threads", lambda *a, **k: [human])
    monkeypatch.setattr(helper.gate, "normalize_threads", lambda payload: payload)
    called = []
    monkeypatch.setattr(helper.gate, "resolve_review_thread", lambda nid: called.append(nid))
    code = helper.main(["--pr", "8", "--head", HEAD, "--thread-id", "PRRT_human"])
    assert code == 2
    assert called == []


def test_normalize_codex_thumbs_binds_request_head_sha():
    comments = normalize_issue_comments(
        [
            {
                "id": 99,
                "user": {"login": "cursor[bot]"},
                "body": f"@codex review\nhead: {HEAD}",
                "html_url": "https://example.test/99",
            }
        ],
        HEAD,
    )
    assert comments[0]["commit_id"] == HEAD
    signals = normalize_codex_completion_signals(
        comments,
        {
            "99": [
                {"id": 1, "content": "+1", "user": {"login": "chatgpt-codex-connector[bot]"}},
                {"id": 2, "content": "heart", "user": {"login": "chatgpt-codex-connector[bot]"}},
                {"id": 3, "content": "+1", "user": {"login": "alice"}},
            ]
        },
        HEAD,
    )
    assert len(signals) == 1
    assert signals[0]["commit_id"] == HEAD
    assert is_codex_reviewer(signals[0]["author"]) is True
    result = evaluate_review_clean(HEAD, [], [], [], comments, signals)
    assert result["review_clean"] is True


def test_is_codex_reviewer_accepts_graphql_login_without_bot_suffix():
    assert is_codex_reviewer("chatgpt-codex-connector[bot]") is True
    assert is_codex_reviewer("chatgpt-codex-connector") is True
    assert is_codex_reviewer("alice") is False
    assert is_codex_reviewer("coderabbitai[bot]") is False
    graphql_thread = thread(
        author="chatgpt-codex-connector",
        authors=["chatgpt-codex-connector"],
        node_id="PRRT_graphql_codex",
    )
    eligible, rejected = eligible_codex_resolve_threads(
        [graphql_thread], ["PRRT_graphql_codex"], HEAD, HEAD
    )
    assert rejected == []
    assert [item["node_id"] for item in eligible] == ["PRRT_graphql_codex"]


def test_codex_review_request_requires_explicit_review_word():
    assert is_codex_review_request("@codex review") is True
    assert is_codex_review_request(f"@codex review\nhead: {HEAD}") is True
    assert is_codex_review_request("@CODEX REVIEW") is True
    assert is_codex_review_request("@codex") is False
    assert is_codex_review_request("@codex address that feedback") is False
    assert is_codex_review_request("@codex fix this") is False


def test_non_review_comment_codex_thumbs_is_not_proof():
    comments = normalize_issue_comments(
        [
            {
                "id": 11,
                "user": {"login": "cursor[bot]"},
                "body": f"@codex\nhead: {HEAD}",
            },
            {
                "id": 12,
                "user": {"login": "cursor[bot]"},
                "body": f"@codex address that feedback\nhead: {HEAD}",
            },
            {
                "id": 13,
                "user": {"login": "cursor[bot]"},
                "body": f"@codex fix this\nhead: {HEAD}",
            },
        ],
        HEAD,
    )
    reactions = {
        "11": [{"id": 1, "content": "+1", "user": {"login": "chatgpt-codex-connector[bot]"}}],
        "12": [{"id": 2, "content": "+1", "user": {"login": "chatgpt-codex-connector[bot]"}}],
        "13": [{"id": 3, "content": "+1", "user": {"login": "chatgpt-codex-connector[bot]"}}],
    }
    signals = normalize_codex_completion_signals(comments, reactions, HEAD)
    assert signals == []
    result = evaluate_review_clean(HEAD, [], [], [], comments, signals)
    assert result["review_clean"] is False
    assert result["proof"] is None


def test_codex_only_thread_is_eligible_after_push():
    bot = thread(
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]"],
        node_id="PRRT_codex_only",
    )
    eligible, rejected = eligible_codex_resolve_threads(
        [bot], ["PRRT_codex_only"], HEAD, HEAD
    )
    assert rejected == []
    assert [item["node_id"] for item in eligible] == ["PRRT_codex_only"]


def test_codex_thread_with_later_human_is_not_eligible():
    mixed = thread(
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]", "alice"],
        node_id="PRRT_codex_then_human",
    )
    eligible, rejected = eligible_codex_resolve_threads(
        [mixed], ["PRRT_codex_then_human"], HEAD, HEAD
    )
    assert eligible == []
    assert rejected[0]["node_id"] == "PRRT_codex_then_human"


def test_human_then_codex_thread_is_not_eligible():
    mixed = thread(
        author="alice",
        authors=["alice", "chatgpt-codex-connector[bot]"],
        node_id="PRRT_human_then_codex",
    )
    eligible, rejected = eligible_codex_resolve_threads(
        [mixed], ["PRRT_human_then_codex"], HEAD, HEAD
    )
    assert eligible == []
    assert rejected[0]["authors"] == ["alice", "chatgpt-codex-connector[bot]"]


def test_human_only_thread_is_not_eligible():
    human = thread(author="alice", authors=["alice"], node_id="PRRT_human_only")
    eligible, rejected = eligible_codex_resolve_threads(
        [human], ["PRRT_human_only"], HEAD, HEAD
    )
    assert eligible == []
    assert rejected[0]["author"] == "alice"


def test_non_codex_bot_thread_is_not_eligible():
    rabbit = thread(
        author="coderabbitai[bot]",
        authors=["coderabbitai[bot]"],
        node_id="PRRT_rabbit",
    )
    eligible, rejected = eligible_codex_resolve_threads(
        [rabbit], ["PRRT_rabbit"], HEAD, HEAD
    )
    assert eligible == []
    assert rejected[0]["author"] == "coderabbitai[bot]"


def test_resolve_before_push_is_rejected():
    bot = thread(
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]"],
        node_id="PRRT_codex1",
    )
    with pytest.raises(ValueError, match="commit \\+ push"):
        eligible_codex_resolve_threads([bot], ["PRRT_codex1"], "", HEAD)


def test_resolve_head_mismatch_is_rejected():
    bot = thread(
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]"],
        node_id="PRRT_codex1",
    )
    with pytest.raises(ValueError, match="commit \\+ push"):
        eligible_codex_resolve_threads([bot], ["PRRT_codex1"], HEAD, OLD)


def test_normalize_threads_keeps_all_comment_authors():
    threads = normalize_threads(
        [
            {
                "id": "PRRT_mixed",
                "isResolved": False,
                "isOutdated": False,
                "comments": {
                    "nodes": [
                        {
                            "databaseId": 1,
                            "body": "Please fix.",
                            "path": "a.py",
                            "author": {"login": "chatgpt-codex-connector[bot]"},
                            "commit": {"oid": HEAD},
                            "originalCommit": {"oid": HEAD},
                        },
                        {
                            "databaseId": 2,
                            "body": "I agree, please fix.",
                            "path": "a.py",
                            "author": {"login": "alice"},
                            "commit": {"oid": HEAD},
                            "originalCommit": {"oid": HEAD},
                        },
                    ]
                },
            }
        ]
    )
    assert threads[0]["authors"] == ["chatgpt-codex-connector[bot]", "alice"]
    eligible, rejected = eligible_codex_resolve_threads(
        threads, ["PRRT_mixed"], HEAD, HEAD
    )
    assert eligible == []
    assert rejected[0]["authors"] == ["chatgpt-codex-connector[bot]", "alice"]


def test_extract_repo_from_pr_url_uses_base_repository():
    assert (
        gate.extract_repo_from_pr_url("https://github.com/base-owner/base-repo/pull/8")
        == "base-owner/base-repo"
    )
    assert gate.extract_repo_from_pr_url("https://github.com/base-owner/base-repo") == ""


def test_resolve_pr_prefers_url_base_repo_over_fork_head(monkeypatch):
    monkeypatch.setattr(
        gate,
        "gh_json",
        lambda args: {
            "number": 8,
            "url": "https://github.com/base-owner/base-repo/pull/8",
            "headRefOid": HEAD,
            "headRepositoryOwner": {"login": "fork-owner"},
            "headRepository": {"name": "fork-repo"},
        },
    )
    pr = gate.resolve_pr("8")
    assert pr["repo"] == "base-owner/base-repo"
    assert pr["owner"] == "base-owner"
    assert pr["name"] == "base-repo"
    assert pr["head_sha"] == HEAD


def test_unmarked_external_review_body_is_actionable():
    external = review(
        author="outside-reviewer",
        author_association="CONTRIBUTOR",
        body="Please keep the public API stable before merging.",
    )
    result = evaluate_review_clean(HEAD, [review(), external], [], [])
    assert result["review_clean"] is False
    assert result["reason"] == "actionable_review_on_current_head"
    assert result["actionable"][0]["author"] == "outside-reviewer"
    assert result["proof"]["author"] == "chatgpt-codex-connector[bot]"


def test_approval_only_review_body_is_not_actionable():
    result = evaluate_review_clean(
        HEAD,
        [review(), review(author="alice", author_association="MEMBER", body="Looks fine.")],
        [],
        [],
    )
    assert result["review_clean"] is True
    assert result["actionable"] == []


def test_codex_boilerplate_review_is_proof_not_actionable():
    result = evaluate_review_clean(
        HEAD,
        [
            review(
                body=(
                    "### Codex Review\n\nHere are some automated review suggestions "
                    "for this pull request.\nReviewed commit: newsha"
                )
            )
        ],
        [],
        [],
    )
    assert result["review_clean"] is True
    assert result["actionable"] == []
    assert result["proof"]["author"] == "chatgpt-codex-connector[bot]"


def test_resolved_thread_rest_comment_is_not_actionable():
    leftover = comment(
        id="3890915001",
        author="chatgpt-codex-connector[bot]",
        path="vendor/gh_pr_watch.py",
        body="![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat) already fixed",
    )
    resolved = thread(
        id="3890915001",
        node_id="PRRT_codex_fixed",
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]"],
        comment_ids=["3890915001"],
        resolved=True,
        path="vendor/gh_pr_watch.py",
        body=leftover["body"],
    )
    result = evaluate_review_clean(HEAD, [review()], [leftover], [resolved])
    assert result["review_clean"] is True
    assert result["actionable"] == []
    assert result["unresolved_threads"] == []
