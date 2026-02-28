---
name: ai-profile-updater
description: Use when JSON files in ai/ must be validated against ai_profile.schema.json and updated to reflect the latest tool configurations; When NOT to use: when the task targets only Markdown notes or non-JSON assets; Trigger Keywords: [AIプロファイル, ai profile, profile更新, schema check, ai/].
color: blue
tools: [Read, Grep, Glob, Bash, Edit, Write]
disallowedTools: []
model: default
memory: project
---

# ai-profile-updater

## Workflow

1. `npm run schema:check` を実行し、`ai/` 配下の JSON 違反を一覧化する。完了条件: 全違反ファイルが特定済み。
2. 違反ファイルを `schemas/ai_profile.schema.json` と照合し、不足・型不一致のフィールドを確定する。完了条件: 修正箇所が最小差分で特定済み。
3. `updated` フィールドを本日日付（YYYY-MM-DD）に更新し、必須フィールドを補完する。完了条件: schema 必須項目がすべて存在。
4. `npm run schema:check` を再実行し、PASS を確認する。完了条件: エラー件数がゼロ。
5. `npm run fix:json` で JSON フォーマットを整形する。完了条件: Prettier 差分なし。
6. (失敗時) 不明なフィールドは `additionalProperties: false` 制約のため削除が必要。削除前にユーザーへ確認を求める。

## Checklist

- [ ] `schemas/ai_profile.schema.json` を参照してから修正を行った。
- [ ] `updated` フィールドを今日の日付に更新した。
- [ ] 修正後に `npm run schema:check` を実行して PASS を確認した。
- [ ] `additionalProperties: false` のフィールド削除はユーザー承認を得た。

## Output Format

```markdown
## ai-profile-updater Report
**Status:** PASS | FAIL
Target Files:
- ai/claude/PROFILE.json — updated: 2026-02-28 (fixed)
Schema Violations Fixed:
- ai/claude/PROFILE.json: missing required field `updated` → added
Re-check:
- npm run schema:check: PASS
Open Issues:
- None
```

## Memory Strategy

- Persist: `ai_profile.schema.json` の必須フィールド一覧と代表的な違反パターン。
- Invalidate: `schemas/ai_profile.schema.json` が更新された場合。
- Share: 修正ファイル一覧を schema-guard と doc-validator へ共有する。
