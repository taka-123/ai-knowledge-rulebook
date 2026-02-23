---
name: lint-fix
description: Use when lint or format checks fail and deterministic repository commands are needed to resolve violations; When NOT to use: when no failing lint signal exists or the task is pure design discussion; Trigger Keywords: [lint, format, markdownlint, prettier, yamllint].
---

# lint-fix

## When to use

- `npm run format:check` が FAIL し、修正対象ファイルが明確なとき。
- `npm run lint:md` / `npm run lint:json` / `npm run lint:yaml` の失敗を収束させるとき。
- `.work/AI_BLUEPRINT.md` など文書更新後に lint 違反を最小差分で直すとき。

## When NOT to use

- 失敗ログがなく、どこが壊れているか不明なとき。
- 実装方針検討だけで、修正作業に入らないとき。
- 大規模リファクタを同時に行う必要があるとき。

## Trigger Keywords

- lint
- format
- markdownlint
- prettier
- yamllint

## Procedure

1. `npm run format:check` を実行して失敗箇所を取得する。完了条件: 失敗ログが保存済み。
2. 対象に応じて `npm run lint:md` / `npm run lint:json` / `npm run lint:yaml` を実行し、違反カテゴリを確定する。完了条件: 違反種別が分類済み。
3. 該当ファイルのみを最小差分で修正する。完了条件: 無関係差分がない。
4. 同じコマンドを再実行して違反が解消したか確認する。完了条件: 失敗件数 0 または残件明示。
5. 修正内容と未解決項目をレポート化する。完了条件: 再現可能な記録がある。

## Output Contract

| 項目 | 形式 |
| --- | --- |
| Failed Command | `npm run ...` |
| Fixed Files | `- path` 箇条書き |
| Re-run Result | PASS / FAIL |
| Remaining Issues | `None` または番号付き |

### NG例

❌ 失敗ログを取らずに推測で修正する（原因不明）。

❌ 関係ないファイルまで自動整形する（差分肥大）。

❌ 再実行せずに「修正完了」と報告する（検証不足）。

## Examples

### Example 1

Input: `npm run format:check` で `.work/AI_BLUEPRINT.md` が警告対象になった。
Output: 対象ファイル修正後の再実行結果表。

### Example 2

Input: `npm run lint:md` が `.claude/skills/skill-discoverer/SKILL.md` で失敗した。
Output: 規約違反修正後の PASS 記録。

### Example 3

Input: `npm run lint:yaml` で `.github/workflows/ci.yml` 警告を確認した。
Output: 警告内容の整理と必要修正の一覧。
