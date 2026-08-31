import importlib.util
import json
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).with_name("final_review_clean_gate.py")
MODULE_SPEC = importlib.util.spec_from_file_location("final_review_clean_gate", MODULE_PATH)
gate = importlib.util.module_from_spec(MODULE_SPEC)
assert MODULE_SPEC.loader is not None
MODULE_SPEC.loader.exec_module(gate)

evaluate_review_clean = gate.evaluate_review_clean
is_actionable_text = gate.is_actionable_text
eligible_codex_ignore_threads = gate.eligible_codex_ignore_threads
eligible_codex_resolve_threads = gate.eligible_codex_resolve_threads
finding_fingerprint = gate.finding_fingerprint
is_codex_only_thread = gate.is_codex_only_thread
is_codex_review_request = gate.is_codex_review_request
is_codex_reviewer = gate.is_codex_reviewer
normalize_codex_completion_signals = gate.normalize_codex_completion_signals
normalize_issue_comments = gate.normalize_issue_comments
normalize_review_comments = gate.normalize_review_comments
normalize_reviews = gate.normalize_reviews
normalize_threads = gate.normalize_threads
pending_review_ids = gate.pending_review_ids


HEAD = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
OLD = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"


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
    if "comment_bodies" not in item:
        item["comment_bodies"] = [item["body"]] if item.get("body") else []
    if "comments_complete" not in item:
        item["comments_complete"] = True
    if "comment_ids" not in item and item.get("id"):
        item["comment_ids"] = [str(item["id"])]
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


def test_dismissed_codex_review_is_not_proof():
    raw = [
        {
            "id": 88,
            "state": "DISMISSED",
            "commit_id": HEAD,
            "user": {"login": "chatgpt-codex-connector[bot]"},
            "body": "No issues found.",
        }
    ]
    reviews = normalize_reviews(raw)
    result = evaluate_review_clean(HEAD, reviews, [], [])
    assert reviews == []
    assert result["review_clean"] is False
    assert result["proof"] is None
    assert result["reason"] == "no_current_head_review_proof"


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


def test_changes_requested_beats_summary_markers():
    body = "Walkthrough\nPlease fix the public API before merge."
    assert is_actionable_text(body, review_state="CHANGES_REQUESTED", kind="review") is True
    assert is_actionable_text(body, review_state="COMMENTED", kind="review") is False
    result = evaluate_review_clean(
        HEAD,
        [
            review(),
            review(
                id="11",
                author="human-reviewer",
                state="CHANGES_REQUESTED",
                body=body,
            ),
        ],
        [],
        [],
    )
    assert result["review_clean"] is False
    assert result["reason"] == "actionable_review_on_current_head"
    assert result["actionable"][0]["state"] == "CHANGES_REQUESTED"
    assert result["actionable"][0]["author"] == "human-reviewer"


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
                "user": {"login": "agent-operator"},
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
    assert is_codex_reviewer("codex[bot]") is True
    assert is_codex_reviewer("codex") is False
    assert is_codex_reviewer("alice") is False
    assert is_codex_reviewer("coderabbitai[bot]") is False
    assert is_codex_reviewer("my-codex-helper[bot]") is False
    assert is_codex_reviewer("notcodex[bot]") is False
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


def _thread_page(ids, has_next=False, cursor=""):
    return {
        "data": {
            "repository": {
                "pullRequest": {
                    "reviewThreads": {
                        "nodes": [{"id": item} for item in ids],
                        "pageInfo": {"hasNextPage": has_next, "endCursor": cursor},
                    }
                }
            }
        }
    }


def test_fetch_review_threads_follows_graphql_cursors(monkeypatch):
    calls = []

    def fake_gh_json(args):
        calls.append(list(args))
        after = None
        for index, item in enumerate(args):
            if item == "-f" and index + 1 < len(args) and args[index + 1].startswith("after="):
                after = args[index + 1].split("=", 1)[1]
        if after is None:
            return _thread_page(["t1"], has_next=True, cursor="c1")
        if after == "c1":
            return _thread_page(["t2"], has_next=False, cursor="c2")
        raise AssertionError(f"unexpected after={after}")

    monkeypatch.setattr(gate, "gh_json", fake_gh_json)
    nodes = gate.fetch_review_threads("o", "n", 8)
    assert [item["id"] for item in nodes] == ["t1", "t2"]
    assert any(
        index + 1 < len(call) and call[index + 1] == "after=c1"
        for call in calls
        for index, item in enumerate(call)
        if item == "-f"
    )


def test_main_fails_if_pr_head_changes_during_fetch(monkeypatch, capsys):
    monkeypatch.setattr(
        gate,
        "resolve_pr",
        lambda *a, **k: {
            "number": 8,
            "repo": "o/r",
            "owner": "o",
            "name": "r",
            "head_sha": HEAD,
            "url": "",
        },
    )
    monkeypatch.setattr(
        gate,
        "collect_gate_inputs",
        lambda pr: {
            "reviews": [],
            "comments": [],
            "threads": [],
            "issue_comments": [],
            "completion_signals": [],
        },
    )
    monkeypatch.setattr(gate, "fetch_head_sha", lambda pr: OLD)
    code = gate.main(["--pr", "8", "--head", HEAD])
    assert code == 2
    assert "PR HEAD changed during gate fetch" in capsys.readouterr().err


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
                "user": {"login": "agent-operator"},
                "body": f"@codex\nhead: {HEAD}",
            },
            {
                "id": 12,
                "user": {"login": "agent-operator"},
                "body": f"@codex address that feedback\nhead: {HEAD}",
            },
            {
                "id": 13,
                "user": {"login": "agent-operator"},
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
    assert threads[0]["comments_complete"] is True
    eligible, rejected = eligible_codex_resolve_threads(
        threads, ["PRRT_mixed"], HEAD, HEAD
    )
    assert eligible == []
    assert rejected[0]["authors"] == ["chatgpt-codex-connector[bot]", "alice"]


def test_incomplete_comment_page_is_not_codex_only():
    threads = normalize_threads(
        [
            {
                "id": "PRRT_truncated",
                "isResolved": False,
                "isOutdated": False,
                "comments": {
                    "pageInfo": {"hasNextPage": True},
                    "nodes": [
                        {
                            "databaseId": 1,
                            "body": "Please fix.",
                            "path": "a.py",
                            "author": {"login": "chatgpt-codex-connector[bot]"},
                            "commit": {"oid": HEAD},
                            "originalCommit": {"oid": HEAD},
                        }
                    ],
                },
            }
        ]
    )
    assert threads[0]["authors"] == ["chatgpt-codex-connector[bot]"]
    assert threads[0]["comments_complete"] is False
    assert is_codex_only_thread(threads[0]) is False
    eligible, rejected = eligible_codex_resolve_threads(
        threads, ["PRRT_truncated"], HEAD, HEAD
    )
    assert eligible == []
    assert rejected[0]["node_id"] == "PRRT_truncated"


def test_list_comments_payload_defaults_to_complete():
    threads = normalize_threads(
        [
            {
                "id": "PRRT_list",
                "isResolved": False,
                "isOutdated": False,
                "comments": [
                    {
                        "databaseId": 1,
                        "body": "Please fix.",
                        "path": "a.py",
                        "author": {"login": "chatgpt-codex-connector[bot]"},
                        "commit": {"oid": HEAD},
                        "originalCommit": {"oid": HEAD},
                    }
                ],
            }
        ]
    )
    assert threads[0]["comments_complete"] is True
    eligible, rejected = eligible_codex_resolve_threads(
        threads, ["PRRT_list"], HEAD, HEAD
    )
    assert rejected == []
    assert [item["node_id"] for item in eligible] == ["PRRT_list"]


def test_threads_query_requests_comment_page_info():
    assert f"comments(first: {gate.COMMENT_PAGE_LIMIT})" in gate.THREADS_QUERY
    assert "pageInfo" in gate.THREADS_QUERY
    assert "hasNextPage" in gate.THREADS_QUERY


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


def test_resolve_pr_rejects_stale_head_override(monkeypatch):
    monkeypatch.setattr(
        gate,
        "gh_json",
        lambda args: {
            "number": 8,
            "url": "https://github.com/base-owner/base-repo/pull/8",
            "headRefOid": HEAD,
            "headRepositoryOwner": {"login": "base-owner"},
            "headRepository": {"name": "base-repo"},
        },
    )
    with pytest.raises(gate.GhCommandError, match="does not match current PR HEAD"):
        gate.resolve_pr("8", head_override=OLD)
    matched = gate.resolve_pr("8", head_override=HEAD)
    assert matched["head_sha"] == HEAD


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
                    f"for this pull request.\nReviewed commit: {HEAD}"
                )
            )
        ],
        [],
        [],
    )
    assert result["review_clean"] is True
    assert result["actionable"] == []
    assert result["proof"]["author"] == "chatgpt-codex-connector[bot]"


def test_resolved_thread_without_ignore_marker_is_still_actionable():
    leftover = comment(
        id="3890915001",
        author="chatgpt-codex-connector[bot]",
        path="vendor/gh_pr_watch.py",
        body="![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat) Include non-Codex reviewers",
    )
    resolved = thread(
        id="3890915001",
        node_id="PRRT_codex_resolved_only",
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]"],
        comment_ids=["3890915001"],
        resolved=True,
        path="vendor/gh_pr_watch.py",
        body=leftover["body"],
    )
    result = evaluate_review_clean(HEAD, [review()], [leftover], [resolved])
    assert result["review_clean"] is False
    assert result["reason"] == "actionable_review_on_current_head"
    assert result["actionable"][0]["id"] == "3890915001"
    assert result["ignored"] == []
    assert result["unresolved_threads"] == []


VENDOR_WATCHER = (
    "ai/claude_code/global/.claude/skills/pr-review-loop/vendor/"
    "openai-codex-babysit-pr/scripts/gh_pr_watch.py"
)
VENDOR_P1_REVIEWERS = (
    "![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)\n"
    "Include non-Codex reviewers such as CodeRabbit and CONTRIBUTOR"
)
VENDOR_P1_COMMIT_ID = (
    "![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)\n"
    "Keep commit_id for current-HEAD review-clean"
)


HELPER_LOGIN = "claude[bot]"
HELPER_LOGIN_GRAPHQL = "claude"
LOCAL_OPERATOR = "local-operator"
VENDOR_IGNORE_REASON = (
    "OpenAI公式の babysit-pr はvendorとして未改変で保持しています。"
    "current HEADのreview-clean判定に必要な commit_id はwrapper側で保持・確認しています。"
)


def _ignore_marker(fingerprint, head_sha=HEAD, reason=VENDOR_IGNORE_REASON):
    return gate.format_ignore_reply(reason, fingerprint, head_sha)


def _helper_thread(leftover, helper=HELPER_LOGIN, fingerprint=None, head_sha=HEAD, **overrides):
    fingerprint = fingerprint or finding_fingerprint(leftover)
    item = thread(
        id=leftover.get("id") or "3890915001",
        node_id="PRRT_codex_ignored",
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]", helper],
        comment_ids=[str(leftover.get("id") or "3890915001"), "3890999999"],
        comment_bodies=[leftover["body"], _ignore_marker(fingerprint, head_sha=head_sha)],
        comment_authors=["chatgpt-codex-connector[bot]", helper],
        resolved=True,
        path=leftover.get("path") or VENDOR_WATCHER,
        body=leftover["body"],
    )
    item.update(overrides)
    return item


def test_explicit_ignore_marker_excludes_matching_fingerprint():
    leftover = comment(
        id="3890915001",
        author="chatgpt-codex-connector[bot]",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    fingerprint = finding_fingerprint(leftover)
    ignored_thread = _helper_thread(leftover, fingerprint=fingerprint)
    result = evaluate_review_clean(
        HEAD, [review()], [leftover], [ignored_thread], gh_user=HELPER_LOGIN
    )
    assert result["review_clean"] is True
    assert result["actionable"] == []
    assert result["ignored"][0]["fingerprint"] == fingerprint
    assert result["ignored"][0]["disposition"] == gate.DISPOSITION_IGNORE


def test_unresolved_ignored_fingerprint_is_not_actionable():
    open_finding = thread(
        id="3890915001",
        node_id="PRRT_codex_open_ignored",
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]"],
        path=VENDOR_WATCHER,
        body=VENDOR_P1_COMMIT_ID,
        resolved=False,
    )
    fingerprint = finding_fingerprint(open_finding)
    open_finding["comment_bodies"] = [
        open_finding["body"],
        _ignore_marker(fingerprint),
    ]
    open_finding["comment_authors"] = ["chatgpt-codex-connector[bot]", HELPER_LOGIN]
    open_finding["authors"] = ["chatgpt-codex-connector[bot]", HELPER_LOGIN]
    result = evaluate_review_clean(HEAD, [review()], [], [open_finding], gh_user=HELPER_LOGIN)
    assert result["review_clean"] is True
    assert result["actionable"] == []
    assert [item["fingerprint"] for item in result["ignored"]] == [fingerprint]


def test_auto_fix_marker_does_not_exclude_finding():
    leftover = comment(
        id="21",
        author="chatgpt-codex-connector[bot]",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    fingerprint = finding_fingerprint(leftover)
    auto_fix_thread = thread(
        id="21",
        node_id="PRRT_auto_fix_marker",
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]"],
        comment_ids=["21"],
        comment_bodies=[
            leftover["body"],
            f"<!-- pr-review-loop:disposition=AUTO_FIX fingerprint={fingerprint} -->",
        ],
        resolved=True,
        path=VENDOR_WATCHER,
        body=leftover["body"],
    )
    result = evaluate_review_clean(HEAD, [review()], [leftover], [auto_fix_thread])
    assert result["review_clean"] is False
    assert result["reason"] == "actionable_review_on_current_head"
    assert result["ignored"] == []
    assert result["actionable"][0]["id"] == "21"


def test_fingerprint_includes_normalized_finding_body():
    first = comment(path=VENDOR_WATCHER, body=VENDOR_P1_REVIEWERS)
    restyled = comment(
        id="98",
        path=VENDOR_WATCHER,
        body=(
            "![P1 Badge](https://img.shields.io/badge/P1-red?style=flat)\n"
            "Include non-Codex reviewers such as CodeRabbit and CONTRIBUTOR"
        ),
    )
    later = comment(
        id="99",
        path=VENDOR_WATCHER,
        body=(
            "![P1 Badge](https://img.shields.io/badge/P1-orange?style=flat)\n"
            "Include non-Codex reviewers such as CodeRabbit and CONTRIBUTOR\n\n"
            "Also require requested reviewers, not a bot-name allowlist."
        ),
    )
    other = comment(id="100", path=VENDOR_WATCHER, body=VENDOR_P1_COMMIT_ID)
    assert finding_fingerprint(first) == finding_fingerprint(restyled)
    assert finding_fingerprint(first) != finding_fingerprint(later)
    assert finding_fingerprint(first) != finding_fingerprint(other)


def test_same_finding_reappearance_matches_fingerprint():
    first = comment(path=VENDOR_WATCHER, body=VENDOR_P1_REVIEWERS)
    fingerprint = finding_fingerprint(first)
    previous = _helper_thread(
        first,
        fingerprint=fingerprint,
        id="1",
        node_id="PRRT_old_ignore",
    )
    reappeared = thread(
        id="99",
        node_id="PRRT_new_repeat",
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]"],
        path=VENDOR_WATCHER,
        body=first["body"],
        resolved=False,
    )
    result = evaluate_review_clean(
        HEAD, [review()], [first], [previous, reappeared], gh_user=HELPER_LOGIN
    )
    assert result["review_clean"] is True
    assert result["actionable"] == []
    assert fingerprint in {item["fingerprint"] for item in result["ignored"]}


def test_authenticated_helper_without_product_login_is_honored():
    leftover = comment(
        id="3890915001",
        author="chatgpt-codex-connector[bot]",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    fingerprint = finding_fingerprint(leftover)
    ignored_thread = _helper_thread(
        leftover, helper=LOCAL_OPERATOR, fingerprint=fingerprint
    )
    result = evaluate_review_clean(
        HEAD, [review()], [leftover], [ignored_thread], gh_user=LOCAL_OPERATOR
    )
    assert result["review_clean"] is True
    assert result["ignored"][0]["fingerprint"] == fingerprint


def test_graphql_bot_suffix_matches_authenticated_helper():
    leftover = comment(
        id="3890915001",
        author="chatgpt-codex-connector[bot]",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    fingerprint = finding_fingerprint(leftover)
    ignored_thread = _helper_thread(
        leftover, helper=HELPER_LOGIN_GRAPHQL, fingerprint=fingerprint
    )
    result = evaluate_review_clean(
        HEAD, [review()], [leftover], [ignored_thread], gh_user=HELPER_LOGIN
    )
    assert result["review_clean"] is True
    assert result["ignored"][0]["fingerprint"] == fingerprint


def test_pr_author_ignore_marker_is_not_honored():
    leftover = comment(
        id="3890915001",
        author="chatgpt-codex-connector[bot]",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    fingerprint = finding_fingerprint(leftover)
    ignored_thread = _helper_thread(
        leftover, helper="taka-123", fingerprint=fingerprint
    )
    result = evaluate_review_clean(
        HEAD, [review()], [leftover], [ignored_thread], gh_user=HELPER_LOGIN
    )
    assert result["review_clean"] is False
    assert result["ignored"] == []
    assert result["actionable"][0]["id"] == "3890915001"


def test_untrusted_author_ignore_marker_is_not_honored():
    leftover = comment(
        id="3890915001",
        author="chatgpt-codex-connector[bot]",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    fingerprint = finding_fingerprint(leftover)
    spoofed = thread(
        id="3890915001",
        node_id="PRRT_spoofed_ignore",
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]", "alice"],
        comment_ids=["3890915001", "3890999999"],
        comment_bodies=[leftover["body"], _ignore_marker(fingerprint)],
        comment_authors=["chatgpt-codex-connector[bot]", "alice"],
        resolved=True,
        path=VENDOR_WATCHER,
        body=leftover["body"],
    )
    result = evaluate_review_clean(
        HEAD, [review()], [leftover], [spoofed], gh_user=HELPER_LOGIN
    )
    assert result["review_clean"] is False
    assert result["ignored"] == []
    assert result["actionable"][0]["id"] == "3890915001"


def test_ignore_marker_without_comment_authors_is_not_honored():
    leftover = comment(
        id="3890915001",
        author="chatgpt-codex-connector[bot]",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    fingerprint = finding_fingerprint(leftover)
    incomplete = thread(
        id="3890915001",
        node_id="PRRT_marker_no_authors",
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]"],
        comment_bodies=[leftover["body"], _ignore_marker(fingerprint)],
        resolved=True,
        path=VENDOR_WATCHER,
        body=leftover["body"],
    )
    result = evaluate_review_clean(HEAD, [review()], [leftover], [incomplete])
    assert result["review_clean"] is False
    assert result["ignored"] == []


def test_format_ignore_reply_keeps_natural_text_and_hidden_marker():
    body = gate.format_ignore_reply(
        "OpenAI公式の babysit-pr はvendorとして未改変で保持しています。",
        "abc123def4567890",
        HEAD,
    )
    visible, marker = body.split("\n\n", 1)
    assert visible.startswith(gate.IGNORE_REPLY_PREFIX)
    assert visible == (
        "AIエージェントによる対応: OpenAI公式の babysit-pr はvendorとして未改変で保持しています。"
    )
    assert (
        "<!-- pr-review-loop:disposition=IGNORE_WITH_REASON "
        f"fingerprint=abc123def4567890 head={HEAD} -->"
    ) in marker
    parsed = gate.parse_disposition_marker(body)
    assert parsed["disposition"] == gate.DISPOSITION_IGNORE
    assert parsed["fingerprint"] == "abc123def4567890"
    assert parsed["head"] == HEAD


def test_format_ignore_reply_does_not_duplicate_prefix():
    body = gate.format_ignore_reply(
        "AIエージェントによる対応: 既存の理由",
        "abc123def4567890",
        HEAD,
    )
    visible = body.split("\n\n", 1)[0]
    assert visible == "AIエージェントによる対応: 既存の理由"


def test_fingerprint_mismatch_is_not_honored():
    leftover = comment(
        id="3890915001",
        author="chatgpt-codex-connector[bot]",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    other_fp = finding_fingerprint({"path": VENDOR_WATCHER, "body": VENDOR_P1_COMMIT_ID})
    spoofed = _helper_thread(leftover, fingerprint=other_fp)
    result = evaluate_review_clean(
        HEAD, [review()], [leftover], [spoofed], gh_user=HELPER_LOGIN
    )
    assert result["review_clean"] is False
    assert result["ignored"] == []
    assert result["actionable"][0]["id"] == "3890915001"


def test_head_mismatch_is_not_honored():
    leftover = comment(
        id="3890915001",
        author="chatgpt-codex-connector[bot]",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    fingerprint = finding_fingerprint(leftover)
    old_head = _helper_thread(leftover, fingerprint=fingerprint, head_sha=OLD)
    result = evaluate_review_clean(
        HEAD, [review()], [leftover], [old_head], gh_user=HELPER_LOGIN
    )
    assert result["review_clean"] is False
    assert result["ignored"] == []
    assert result["actionable"][0]["id"] == "3890915001"


def test_empty_authenticated_user_is_fail_closed():
    leftover = comment(
        id="3890915001",
        author="chatgpt-codex-connector[bot]",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    ignored_thread = _helper_thread(leftover)
    result = evaluate_review_clean(HEAD, [review()], [leftover], [ignored_thread], gh_user="")
    assert result["review_clean"] is False
    assert result["ignored"] == []


def test_owner_association_does_not_trust_arbitrary_participant():
    leftover = comment(
        id="3890915001",
        author="chatgpt-codex-connector[bot]",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    fingerprint = finding_fingerprint(leftover)
    spoofed = _helper_thread(leftover, helper="repo-owner", fingerprint=fingerprint)
    spoofed["comment_associations"] = ["NONE", "OWNER"]
    spoofed["author_association"] = "OWNER"
    result = evaluate_review_clean(
        HEAD, [review()], [leftover], [spoofed], gh_user=HELPER_LOGIN
    )
    assert result["review_clean"] is False
    assert result["ignored"] == []


def test_ignore_marker_without_ai_prefix_is_not_honored():
    leftover = comment(
        id="3890915001",
        author="chatgpt-codex-connector[bot]",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    fingerprint = finding_fingerprint(leftover)
    marker_only = (
        f"<!-- pr-review-loop:disposition=IGNORE_WITH_REASON "
        f"fingerprint={fingerprint} head={HEAD} -->"
    )
    spoofed = thread(
        id="3890915001",
        node_id="PRRT_marker_no_prefix",
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]", HELPER_LOGIN],
        comment_bodies=[leftover["body"], marker_only],
        comment_authors=["chatgpt-codex-connector[bot]", HELPER_LOGIN],
        resolved=True,
        path=VENDOR_WATCHER,
        body=leftover["body"],
    )
    result = evaluate_review_clean(
        HEAD, [review()], [leftover], [spoofed], gh_user=HELPER_LOGIN
    )
    assert result["review_clean"] is False
    assert result["ignored"] == []


def test_same_github_actor_is_product_agnostic():
    assert gate.same_github_actor("claude[bot]", "claude") is True
    assert gate.same_github_actor("codex[bot]", "codex") is True
    assert gate.same_github_actor(LOCAL_OPERATOR, LOCAL_OPERATOR) is True
    assert gate.same_github_actor("claude[bot]", "alice") is False
    assert gate.same_github_actor("", "claude[bot]") is False
    assert gate.is_trusted_disposition_author("claude[bot]", gh_user="claude") is True
    assert gate.is_trusted_disposition_author("alice", gh_user="claude[bot]") is False


def test_disposition_reply_body_is_not_actionable():
    fingerprint = finding_fingerprint(
        {"path": VENDOR_WATCHER, "body": VENDOR_P1_REVIEWERS}
    )
    reply = comment(
        id="reply1",
        author="taka-123",
        path=VENDOR_WATCHER,
        body=_ignore_marker(fingerprint),
    )
    result = evaluate_review_clean(HEAD, [review()], [reply], [])
    assert result["review_clean"] is True
    assert result["actionable"] == []


def test_incomplete_thread_comments_are_not_eligible_for_ignore_or_resolve():
    truncated = thread(
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]"],
        node_id="PRRT_truncated",
        comments_complete=False,
    )
    ignore_eligible, ignore_rejected = eligible_codex_ignore_threads(
        [truncated], ["PRRT_truncated"], HEAD, HEAD
    )
    resolve_eligible, resolve_rejected = eligible_codex_resolve_threads(
        [truncated], ["PRRT_truncated"], HEAD, HEAD
    )
    assert ignore_eligible == []
    assert ignore_rejected[0]["node_id"] == "PRRT_truncated"
    assert resolve_eligible == []
    assert resolve_rejected[0]["node_id"] == "PRRT_truncated"


def test_codex_only_thread_is_eligible_for_ignore_without_push():
    bot = thread(
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]"],
        node_id="PRRT_codex_ignore",
        resolved=False,
    )
    eligible, rejected = eligible_codex_ignore_threads(
        [bot], ["PRRT_codex_ignore"], HEAD, HEAD
    )
    assert rejected == []
    assert [item["node_id"] for item in eligible] == ["PRRT_codex_ignore"]


def test_helper_reignore_is_eligible_on_previous_helper_thread():
    previous = thread(
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]", LOCAL_OPERATOR],
        node_id="PRRT_codex_reignore",
        resolved=False,
    )
    eligible, rejected = eligible_codex_ignore_threads(
        [previous], ["PRRT_codex_reignore"], HEAD, HEAD, gh_user=LOCAL_OPERATOR
    )
    assert rejected == []
    assert [item["node_id"] for item in eligible] == ["PRRT_codex_reignore"]
    other_operator, other_rejected = eligible_codex_ignore_threads(
        [previous], ["PRRT_codex_reignore"], HEAD, HEAD, gh_user=HELPER_LOGIN
    )
    assert other_operator == []
    assert other_rejected[0]["node_id"] == "PRRT_codex_reignore"


def test_human_thread_is_not_eligible_for_ignore_or_resolve():
    human = thread(author="alice", authors=["alice"], node_id="PRRT_human_ask")
    ignore_eligible, ignore_rejected = eligible_codex_ignore_threads(
        [human], ["PRRT_human_ask"], HEAD, HEAD
    )
    resolve_eligible, resolve_rejected = eligible_codex_resolve_threads(
        [human], ["PRRT_human_ask"], HEAD, HEAD
    )
    assert ignore_eligible == []
    assert ignore_rejected[0]["author"] == "alice"
    assert resolve_eligible == []
    assert resolve_rejected[0]["author"] == "alice"
    result = evaluate_review_clean(HEAD, [review()], [], [human])
    assert result["review_clean"] is False
    assert result["actionable"][0]["author"] == "alice"


def test_coderabbit_thread_is_not_eligible_for_ignore_or_resolve():
    rabbit = thread(
        author="coderabbitai[bot]",
        authors=["coderabbitai[bot]"],
        node_id="PRRT_rabbit_ignore",
    )
    ignore_eligible, ignore_rejected = eligible_codex_ignore_threads(
        [rabbit], ["PRRT_rabbit_ignore"], HEAD, HEAD
    )
    resolve_eligible, resolve_rejected = eligible_codex_resolve_threads(
        [rabbit], ["PRRT_rabbit_ignore"], HEAD, HEAD
    )
    assert ignore_eligible == []
    assert ignore_rejected[0]["author"] == "coderabbitai[bot]"
    assert resolve_eligible == []
    assert resolve_rejected[0]["author"] == "coderabbitai[bot]"


def test_mixed_human_codex_thread_is_not_eligible_for_ignore():
    mixed = thread(
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]", "alice"],
        node_id="PRRT_mixed_ignore",
    )
    eligible, rejected = eligible_codex_ignore_threads(
        [mixed], ["PRRT_mixed_ignore"], HEAD, HEAD
    )
    assert eligible == []
    assert rejected[0]["authors"] == ["chatgpt-codex-connector[bot]", "alice"]


def test_mixed_human_codex_thread_ignore_marker_is_not_honored():
    leftover = comment(
        id="3890915001",
        author="chatgpt-codex-connector[bot]",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    fingerprint = finding_fingerprint(leftover)
    mixed = thread(
        id="3890915001",
        node_id="PRRT_mixed_marker",
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]", "alice", HELPER_LOGIN],
        comment_bodies=[
            leftover["body"],
            "Why is this ignored?",
            _ignore_marker(fingerprint),
        ],
        comment_authors=["chatgpt-codex-connector[bot]", "alice", HELPER_LOGIN],
        resolved=False,
        path=VENDOR_WATCHER,
        body=leftover["body"],
    )
    result = evaluate_review_clean(
        HEAD, [review()], [leftover], [mixed], gh_user=HELPER_LOGIN
    )
    assert result["review_clean"] is False
    assert result["ignored"] == []
    assert result["actionable"][0]["id"] == "3890915001"


def test_coderabbit_mixed_thread_ignore_marker_is_not_honored():
    leftover = comment(
        id="21",
        author="coderabbitai[bot]",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    fingerprint = finding_fingerprint(leftover)
    mixed = thread(
        id="21",
        node_id="PRRT_rabbit_mixed_marker",
        author="coderabbitai[bot]",
        authors=["coderabbitai[bot]", HELPER_LOGIN],
        comment_bodies=[leftover["body"], _ignore_marker(fingerprint)],
        comment_authors=["coderabbitai[bot]", HELPER_LOGIN],
        resolved=False,
        path=VENDOR_WATCHER,
        body=leftover["body"],
    )
    result = evaluate_review_clean(
        HEAD, [review()], [leftover], [mixed], gh_user=HELPER_LOGIN
    )
    assert result["review_clean"] is False
    assert result["ignored"] == []
    assert result["actionable"][0]["id"] == "21"


def load_ignore_helper():
    path = Path(__file__).with_name("ignore_codex_threads.py")
    spec = importlib.util.spec_from_file_location("ignore_codex_threads", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _patch_pr(monkeypatch, helper, threads, gh_user=HELPER_LOGIN):
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
    monkeypatch.setattr(helper.gate, "fetch_review_threads", lambda *a, **k: threads)
    monkeypatch.setattr(helper.gate, "normalize_threads", lambda payload: payload)
    monkeypatch.setattr(helper.gate, "fetch_authenticated_login", lambda: gh_user)


def test_ignore_helper_replies_on_codex_only_thread(monkeypatch, capsys):
    helper = load_ignore_helper()
    bot = thread(
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]"],
        node_id="PRRT_codex_ignore_helper",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_REVIEWERS,
    )
    _patch_pr(monkeypatch, helper, [bot])
    replies = []
    resolved = []
    monkeypatch.setattr(
        helper.gate,
        "reply_review_thread",
        lambda nid, body: replies.append((nid, body)),
    )
    monkeypatch.setattr(helper.gate, "resolve_review_thread", lambda nid: resolved.append(nid))
    code = helper.main(
        [
            "--pr",
            "8",
            "--head",
            HEAD,
            "--reason",
            VENDOR_IGNORE_REASON,
            "--thread-id",
            "PRRT_codex_ignore_helper",
        ]
    )
    assert code == 0
    assert replies[0][0] == "PRRT_codex_ignore_helper"
    assert replies[0][1].startswith(gate.IGNORE_REPLY_PREFIX)
    assert VENDOR_IGNORE_REASON in replies[0][1]
    assert "pr-review-loop:disposition=IGNORE_WITH_REASON" in replies[0][1]
    assert f"head={HEAD}" in replies[0][1]
    assert resolved == ["PRRT_codex_ignore_helper"]
    payload = json.loads(capsys.readouterr().out)
    assert payload["ignored"][0]["replied"] is True
    assert payload["ignored"][0]["resolved"] is True
    assert payload["ignored"][0]["disposition"] == gate.DISPOSITION_IGNORE


def test_ignore_helper_does_not_reply_on_human_or_coderabbit(monkeypatch):
    helper = load_ignore_helper()
    human = thread(author="alice", authors=["alice"], node_id="PRRT_human_helper")
    rabbit = thread(
        author="coderabbitai[bot]",
        authors=["coderabbitai[bot]"],
        node_id="PRRT_rabbit_helper",
    )
    for item in (human, rabbit):
        _patch_pr(monkeypatch, helper, [item])
        replies = []
        resolved = []
        monkeypatch.setattr(
            helper.gate,
            "reply_review_thread",
            lambda nid, body: replies.append((nid, body)),
        )
        monkeypatch.setattr(
            helper.gate, "resolve_review_thread", lambda nid: resolved.append(nid)
        )
        code = helper.main(
            [
                "--pr",
                "8",
                "--head",
                HEAD,
                "--reason",
                "out of scope",
                "--thread-id",
                item["node_id"],
            ]
        )
        assert code == 2
        assert replies == []
        assert resolved == []


def test_ignore_helper_keeps_reply_if_resolve_is_forbidden(monkeypatch, capsys):
    helper = load_ignore_helper()
    bot = thread(
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]"],
        node_id="PRRT_codex_resolve_forbidden",
        path=VENDOR_WATCHER,
        body=VENDOR_P1_COMMIT_ID,
    )
    _patch_pr(monkeypatch, helper, [bot])
    replies = []
    monkeypatch.setattr(
        helper.gate,
        "reply_review_thread",
        lambda nid, body: replies.append((nid, body)),
    )

    def boom(_nid):
        raise helper.gate.GhCommandError("Resource not accessible by personal access token")

    monkeypatch.setattr(helper.gate, "resolve_review_thread", boom)
    code = helper.main(
        [
            "--pr",
            "8",
            "--head",
            HEAD,
            "--reason",
            "wrapper は current HEAD の review-clean 判定に必要な commit_id を保持しています。",
            "--thread-id",
            "PRRT_codex_resolve_forbidden",
        ]
    )
    assert code == 0
    assert replies
    payload = json.loads(capsys.readouterr().out)
    assert payload["ignored"][0]["replied"] is True
    assert payload["ignored"][0]["resolved"] is False
    assert "Resource not accessible" in payload["ignored"][0]["resolve_error"]


def test_auto_fix_helper_still_does_not_call_reply(monkeypatch):
    helper = load_resolve_helper()
    bot = thread(
        author="chatgpt-codex-connector[bot]",
        authors=["chatgpt-codex-connector[bot]"],
        node_id="PRRT_codex_auto_fix",
    )
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
    monkeypatch.setattr(helper.gate, "fetch_review_threads", lambda *a, **k: [bot])
    monkeypatch.setattr(helper.gate, "normalize_threads", lambda payload: payload)
    replies = []
    resolved = []
    monkeypatch.setattr(
        helper.gate,
        "reply_review_thread",
        lambda nid, body: replies.append((nid, body)),
    )
    monkeypatch.setattr(helper.gate, "resolve_review_thread", lambda nid: resolved.append(nid))
    code = helper.main(["--pr", "8", "--head", HEAD, "--thread-id", "PRRT_codex_auto_fix"])
    assert code == 0
    assert replies == []
    assert resolved == ["PRRT_codex_auto_fix"]


def test_fetch_authenticated_login_reads_gh_user(monkeypatch):
    seen = []

    def fake_gh_json(args):
        seen.append(list(args))
        return {"login": HELPER_LOGIN}

    monkeypatch.setattr(gate, "gh_json", fake_gh_json)
    assert gate.fetch_authenticated_login() == HELPER_LOGIN
    assert seen[0][:2] == ["api", "user"]
    assert "-X" in seen[0] and "GET" in seen[0]


def test_fetch_authenticated_login_is_empty_when_unauthenticated(monkeypatch):
    def boom(_args):
        raise gate.GhCommandError("HTTP 401")

    monkeypatch.setattr(gate, "gh_json", boom)
    assert gate.fetch_authenticated_login() == ""


def test_main_passes_authenticated_login_to_evaluate(monkeypatch):
    captured = {}

    def fake_evaluate(*args, **kwargs):
        captured["gh_user"] = kwargs.get("gh_user")
        return {
            "head_sha": HEAD,
            "review_clean": True,
            "reason": "current_head_review_complete",
            "proof": review(),
            "current_head_items": [],
            "old_head_items": [],
            "unbound_items": [],
            "unresolved_threads": [],
            "actionable": [],
            "ignored": [],
        }

    monkeypatch.setattr(
        gate,
        "resolve_pr",
        lambda *a, **k: {
            "number": 8,
            "repo": "o/r",
            "owner": "o",
            "name": "r",
            "head_sha": HEAD,
            "url": "https://example.test/o/r/pull/8",
            "author": "taka-123",
        },
    )
    monkeypatch.setattr(
        gate,
        "collect_gate_inputs",
        lambda pr: {
            "reviews": [review()],
            "comments": [],
            "threads": [],
            "issue_comments": [],
            "completion_signals": [],
        },
    )
    monkeypatch.setattr(gate, "fetch_head_sha", lambda pr: HEAD)
    monkeypatch.setattr(gate, "fetch_authenticated_login", lambda: HELPER_LOGIN)
    monkeypatch.setattr(gate, "evaluate_review_clean", fake_evaluate)
    code = gate.main(["--pr", "8", "--head", HEAD])
    assert code == 0
    assert captured["gh_user"] == HELPER_LOGIN
