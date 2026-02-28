# Review Request Command (Cursor)

## Trigger

次の自然文依頼で起動:

- レビューしてください
- この修正でOKか
- 見てほしい

## Procedure

1. `git diff --stat` と `git diff -p` で差分取得。
2. `cross-service-reviewer` を起点にレビュー実行。
3. `requirements.md` + `直近コミット` がある場合は `code-reviewer -> security-reviewer -> verifier` に展開。
4. reviewer 失敗時は `cross-service-reviewer` が観点を補完。

## Output

- **Status:** PASS | FAIL | PARTIAL | BLOCKED
- Failed Sub-agents
- Parent Fallback Coverage
