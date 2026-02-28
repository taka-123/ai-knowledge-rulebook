---
name: ai-profile-updater
description: Use proactively when editing JSON files under ai/ or schemas/ and validating them with npm run schema:check during profile maintenance tasks; When NOT to use: when the task only edits Markdown files under .work/ or .claude/ with no JSON schema impact; Trigger Keywords: [ai profile, schema check, updated field, JSON fix, ai/].
model: inherit
---


# ai-profile-updater

## Workflow

1. `find ai -name '*.json' -type f | sort` と `cat schemas/ai_profile.schema.json` で対象と制約を確認する。
2. 対象 JSON を最小差分で修正し、`updated` など必須フィールドの整合性をそろえる。
3. `npm run schema:check` を実行し、失敗時はエラー行と原因を抽出する。
4. `npx prettier --check 'ai/**/*.json' --ignore-path .prettierignore` で整形崩れを検査する。
5. (失敗時) スキーマ不整合が解消できない、または対象 JSON が存在しない場合は **Status: BLOCKED** で停止する。

## Checklist

- [ ] `ai/` と `schemas/` の実体を確認してから編集した。
- [ ] 無関係なキー追加や削除を行っていない。
- [ ] `npm run schema:check` の結果を記録した。

## Output Format

**Status:** PASS | FAIL | BLOCKED

```markdown
## ai-profile-updater Report
**Status:** PASS | FAIL | BLOCKED
Targets:
- ai/<path>.json
Changes:
1. <field>: <before> -> <after>
Verification:
- npm run schema:check: PASS | FAIL
- npx prettier --check 'ai/**/*.json' --ignore-path .prettierignore: PASS | FAIL
Open Issues:
- None | <issue>
```

## Memory Strategy

- Persist: 失敗しやすい schema ルールと修正パターン。
- Invalidate: `schemas/ai_profile.schema.json` 更新時。
- Share: 検証結果を `verifier` と `content-writer` へ共有する。
