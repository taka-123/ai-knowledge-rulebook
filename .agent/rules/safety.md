# Safety

- 変更は最小限かつ可逆的に保つ。
- 不明点は `不明` と明示し、推測で断定しない。
- 以下の破壊的・外部影響操作は実行前に明示的な承認を必須とする:
  - `deploy`
  - `migrate`
  - `terraform apply`
  - `git push --force`
  - 本番環境の設定変更
