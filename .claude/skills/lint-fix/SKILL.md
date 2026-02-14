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
