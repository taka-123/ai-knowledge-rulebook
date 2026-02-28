# Local Review Routing Overlay

## Natural-language review routing

- 入力に `レビューしてください` / `この修正でOKか` / `見てほしい` が含まれる場合は `cross-service-reviewer` を最優先で起動する。
- 入力に `requirements.md` と `直近コミット` の両方が含まれる場合、以下の順序でレビューする。
  1. `cross-service-reviewer`
  2. `code-reviewer`
  3. `security-reviewer`（必要時）
  4. `verifier`

## Fallback

- reviewer 系サブエージェントが失敗・タイムアウトした場合は、`cross-service-reviewer` が不足観点を代替する。
- 最終レポートに「失敗したサブエージェント」「親が代替した観点」を必ず記載する。

## Compatibility

- no-stat 系の非互換オプションは使用しない。
- 差分確認は `git diff --stat` と `git diff -p` を使用する。
