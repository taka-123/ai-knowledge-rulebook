description: Run repository quality checks (format, lint, schema) and summarize results
allowed-tools: Bash(./format.sh check), Bash(npm run format:check), Bash(npm run lint:md), Bash(npm run lint:yaml), Bash(npm run lint:json), Bash(npm run schema:check)

---

## Execute Checks

- Format script: !`./format.sh check`
- Markdown lint: !`npm run lint:md`
- YAML lint: !`npm run lint:yaml`
- JSON lint: !`npm run lint:json`
- Schema validation: !`npm run schema:check`

## Reporting

1. それぞれのコマンド結果を ✅/⚠️/🔴 で整理してください（失敗時はログの要約を併記）。
2. 失敗や警告があれば、原因候補と対処方針を提案してください。
3. 追加で手動確認すべき項目があれば列挙してください（例: 特定のコードテスト、追加の linters）。
