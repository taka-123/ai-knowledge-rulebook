# Review Request Command (Cursor)

レビュー依頼は **発話の種類で分けず**、まず差分を取得し **コンテキスト（差分量・ファイル数・リスク）で単一パス vs パイプラインを自動決定**する。ユーザーは「レビューして」「レビューしてください」のどちらでもよい。

## Trigger

次のいずれかの自然文で起動:

- レビューして / レビューしてください
- この修正でOKか
- 見てほしい
- 差分レビュー / review diff 等

## Procedure

1. **差分取得**: `git diff --stat` と `git diff -p` でスコープを把握する。
2. **ルート決定**:
   - 小さい（目安: 約 400 LOC 未満・ファイル数少なめ）かつリスク領域でない → **単一パス**: ai-diff-review 手順を現コンテキストで実行（または 1 サブエージェントでスキル実行）。
   - 大きい or リスク領域 → **パイプライン**: cross-service-reviewer を起点に code-reviewer →（必要時）security-reviewer → verifier。
   - ユーザーが「しっかり」「full」等 → パイプライン強制。「軽く」「quick」等 → 単一パス強制。
3. `requirements.md` + `直近コミット` が含まれる場合はパイプラインを推奨。
4. reviewer 失敗時は cross-service-reviewer が観点を補完。

## Output

ユーザー向けは **統一レポート形式**（レビューサマリー・指摘事項の絵文字表現。ai-diff-review の Output Contract に準拠）。パイプライン通過時は加えて:

- **Status:** PASS | FAIL | PARTIAL | BLOCKED
- Failed Sub-agents
- Parent Fallback Coverage
