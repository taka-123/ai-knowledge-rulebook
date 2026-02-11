# Output Format Rule

- 応答は簡潔で実行指向にする。
- 実装タスクの報告には: 変更パス、ファイルごとの目的（1 行）、検証結果を含める。
- 事実と推測を明確に区別する。
- 不明点は `不明` と明示する。
- <SCRUTINY_REQUIRED> 破壊的操作（`deploy`, `migrate`, `terraform apply`, `git push --force`）は明示的なユーザー承認を必須とする。
- ファイル変更後は `./format.sh check` を実行し、結果を報告に含める。
