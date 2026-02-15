---
name: lint-fix
description: Use when lint or formatting checks fail and deterministic fixes must be applied with repository commands; When NOT to use: feature design or architecture discussions without failing checks; Trigger Keywords: lint, format, markdownlint, prettier, yamllint.
---

# lint-fix

## When to use

- `npm run format:check` が失敗した。
- Markdown/YAML/JSON の整形不整合を解消したい。

## When NOT to use

- ロジック設計だけを相談している段階。
- 失敗ログが提示されていない段階。

## Trigger Keywords

- lint
- format
- markdownlint
- prettier
- yamllint

## Examples

### Example 1

Input: `.work/AI_BLUEPRINT.md` の markdownlint エラーを直して。
Output: `npx markdownlint-cli2 .work/AI_BLUEPRINT.md` で再現し、該当行のみ修正して再チェックする。

### Example 2

Input: JSON の整形崩れを一括修正したい。
Output: `npm run fix:json` を実行し、`npm run lint:json` で結果を検証する。

### Example 3

Input: YAML の lint だけ落ちているので最小修正で通して。
Output: `.config/.yamllint.yml` を尊重しつつ対象 YAML を修正し、`npm run lint:yaml` を通す。

---

## 1. Workflow

1. **Intake**: 失敗ログまたは対象ファイルを受け取り、エラー種別（Markdown / YAML / JSON / Prettier）を判別する。
2. **Reproduce**: `npm run format:check`（= `./format.sh check`）を実行し、全カテゴリのエラーを一括再現する。特定カテゴリのみ確認する場合は `npm run lint:md` / `npm run lint:yaml` / `npm run lint:json` を個別実行する。
3. **Auto-Fix**: `npm run format`（= `./format.sh fix`）を実行し、全カテゴリを一括自動修正する。一括修正で解消しない場合は手動修正を Edit で適用する。
4. **Verify**: `npm run format:check` を再実行し、exit 0 を確認する。残存エラーがあれば Step 3 に戻る。
5. **Report**: Output Format に従い、修正内容と検証結果を出力する。

## 2. Checklist

### Pre-flight

- [ ] エラーログまたは対象ファイルが明示されている
- [ ] エラー種別（md / yaml / json / prettier）が判別済み
- [ ] 該当する設定ファイル（`.markdownlint.jsonc` 等）を確認済み

### Post-flight

- [ ] 全エラーが解消されている（lint コマンド exit 0）
- [ ] 修正差分が最小（エラー箇所のみ変更）
- [ ] 設定ファイル自体は変更していない（意図的変更を除く）

## 3. Output Format

```markdown
## lint-fix Report

**Action**: AUTO-FIX | MANUAL-FIX | MIXED
**Target**: <file path(s)>
**Error Type**: Markdownlint | yamllint | Prettier | JSON

### Fixes Applied

| #   | File             | Line | Rule  | Before             | After            |
| --- | ---------------- | ---- | ----- | ------------------ | ---------------- |
| 1   | notes/2025-01.md | 12   | MD032 | missing blank line | added blank line |

### Verification

| Command                | Exit Code | Status |
| ---------------------- | --------- | ------ |
| `npm run lint:md`      | 0         | PASS   |
| `npm run format:check` | 0         | PASS   |
```

## 4. Memory Strategy

- **Persist**: ファイル形式ごとの頻出エラーパターンと修正コマンドをキャッシュし、次回の修正を高速化する。
- **Invalidate**: lint 設定ファイル（`.markdownlint.jsonc`、`.prettierrc.json`、`.config/.yamllint.yml`）が変更された場合にキャッシュを無効化する。
- **Share**: 修正完了後のファイルパスを `format-lint-audit` に提供し、最終品質ゲートの再実行に活用する。
