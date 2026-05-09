# Review Request Command

レビュー依頼は発話の種類で分けず、まず差分を取得し、コンテキスト（差分量・ファイル数・リスク）で単一パスかパイプラインかを自動決定する。ユーザーは「レビューして」「レビューしてください」のどちらでもよい。

## Trigger

- レビューして / レビューしてください
- この修正でOKか
- 見てほしい
- 差分レビュー / review diff

## Procedure

1. `git diff --stat` と `git diff -p` でスコープを把握する。
2. 小さい差分（目安: 約 400 LOC 未満・ファイル数少なめ）かつリスク領域でない場合は単一パスでレビューする。
3. 大きい差分、または auth/security/infra/依存更新などのリスク領域を含む場合は `cross-service-reviewer -> code-reviewer -> security-reviewer -> verifier` のパイプラインを使う。
4. `requirements.md` と `直近コミット` が含まれる場合はパイプラインを推奨する。
5. reviewer が失敗・タイムアウトした場合は親が不足観点を補完し、失敗したサブエージェント名と親の代替観点を最終レポートに明記する。

## Output

- **Status:** PASS | FAIL | PARTIAL | BLOCKED
- Findings first, then fallback coverage when a pipeline was used.
