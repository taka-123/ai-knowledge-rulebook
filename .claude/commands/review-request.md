---
description: Route natural-language review requests to reviewer agents with fallback handling
allowed-tools: Bash(git diff --stat), Bash(git diff -p), Bash(rg --files .claude .cursor .codex)
---

## Trigger

以下の自然文を受けた場合に実行する:

- レビューしてください
- この修正でOKか
- 見てほしい

## Routing Steps

1. `git diff --stat` と `git diff -p` で差分を固定する。
2. まず `cross-service-reviewer` を起点にレビュー計画を作成する。
3. `requirements.md` と `直近コミット` の両方が入力にある場合、`code-reviewer -> security-reviewer(必要時) -> verifier` の順で実施する。
4. reviewer 失敗時は `cross-service-reviewer` が残り観点を代替し、代替観点を報告する。

## Output Contract

- **Status:** PASS | FAIL | PARTIAL | BLOCKED
- Failed Sub-agents
- Parent Fallback Coverage
