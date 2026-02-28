---
name: schema-guard
description: Use proactively when editing JSON files under ai/ or notes/ and validating them against schemas/ai_profile.schema.json or schemas/notes.schema.json; When NOT to use: when the task only touches non-JSON files with no schema boundary; Trigger Keywords: [schema, JSON検証, check-jsonschema, ajv, 型整合].
---

# schema-guard

## When to use

- `npm run schema:check` の結果を確認し、JSON の適合性を監査するとき。
- `ai/claude_code/project/.claude/settings.json` の変更がスキーマ境界に影響しないか確認するとき。
- `schemas/ai_profile.schema.json` / `schemas/notes.schema.json` の適用範囲を文書化するとき。

## When NOT to use

- JSON 以外のファイルのみを扱うとき。
- スキーマ定義が存在しない対象へ推測でルールを適用するとき。
- lint 修正だけでスキーマ検証を必要としないとき。

## Trigger Keywords

- schema
- JSON検証
- check-jsonschema
- ajv
- 型整合

## Procedure

1. `npm run schema:check` を実行して違反の有無を確認する。完了条件: コマンド結果が取得済み。
2. 対象 JSON と対応スキーマ（`schemas/ai_profile.schema.json`, `schemas/notes.schema.json`）を照合する。完了条件: 対応関係が確定。
3. 違反フィールドのみ最小差分で修正する。完了条件: 追加修正が必要最小限。
4. `npm run schema:check` を再実行し、PASS/FAIL を記録する。完了条件: 検証結果が確定。
5. 修正内容をファイル単位で一覧化する。完了条件: 追跡可能なレポート完成。

## Output Contract

| 項目        | 形式                              |
| ----------- | --------------------------------- |
| Target JSON | `path/to/file.json`               |
| Schema      | `schemas/*.json`                  |
| Violation   | `required/type/enum` など         |
| Fix         | 変更フィールドの説明              |
| Re-check    | `npm run schema:check: PASS/FAIL` |

### NG例

❌ スキーマを読まずにフィールドを推測で追加する（再発リスク）。

❌ エラーと無関係なキーをまとめて変更する（差分過大）。

❌ 再検証を行わずに終了する（品質未確定）。

## Examples

### Example 1

Input: `npm run schema:check` を実行し、現在の JSON 適合状況を確認したい。
Output: コマンド結果と対象スキーマ一覧の表。

### Example 2

Input: `ai/claude_code/project/.claude/settings.json` の更新が schema チェックへ影響するか確認したい。
Output: 影響有無の判定と必要対応のチェックリスト。

### Example 3

Input: `schemas/notes.schema.json` の必須項目を確認して運用手順へ反映したい。
Output: 必須項目一覧と `npm run schema:check` 実行結果。
