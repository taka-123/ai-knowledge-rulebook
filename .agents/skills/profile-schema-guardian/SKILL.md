---
name: profile-schema-guardian
description: Schema guardian for AIプロファイル, notes JSON, Schema適合, and キー名検証 tasks. Use when requests mention JSON schema checks or profile validation.
---

# Profile Schema Guardian

## 手順

1. 対象 JSON を `ai/` と `notes/` から抽出する。
2. `schemas/ai_profile.schema.json` と `schemas/notes.schema.json` を基準に検証する。
3. 不一致をキー名、型、必須属性ごとに列挙する。
4. 最小修正案を提示し、互換性影響を明記する。
5. 修正後に `npm run schema:check` を再実行して通過を確認する。

## Safety

- スキーマ自体の変更は自動実施しない。提案して承認を得る。
- `db` `migrate` `infra` を含む高リスク操作は提案のみとし、承認なしで実行しない。

## 継承

- `task-reviewer` の検証義務と `tech-researcher` のキー名厳密性を継承する。
