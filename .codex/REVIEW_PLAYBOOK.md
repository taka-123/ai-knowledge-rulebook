# Codex Review Playbook

## Natural Language Routing

- ユーザーが `この修正でOKかレビューしてください` のように自然文で依頼した場合は、`cross-service-reviewer` を起点にする。
- `requirements.md` と `直近コミット` が両方含まれる場合、固定順序は以下:
  1. `cross-service-reviewer`
  2. `code-reviewer`
  3. `security-reviewer`（セキュリティリスクがある場合）
  4. `verifier`

## Fallback Rule

- `code-reviewer` または `security-reviewer` が失敗・タイムアウトした場合、`cross-service-reviewer` が不足観点を代替実施する。
- 最終レポートには必ず次を含める:
  - 失敗したサブエージェント名
  - 親が代替した観点

## Compatibility Gate

- no-stat 系の非互換オプションは禁止。
- 差分確認は `git diff --stat` と `git diff -p` を使う。
