---
name: schema-guard
description: Use when JSON assets must conform to repository schemas and validation output must be interpreted into minimal corrective edits; When NOT to use: non-JSON tasks with no schema boundary; Trigger Keywords: schema, JSON検証, check-jsonschema, ajv, 型整合.
---

# schema-guard

## When to use

- JSON がスキーマ適合しているか検証する。
- 検証エラーを最小差分で直す。

## When NOT to use

- JSON を扱わない作業。
- スキーマ外の仕様議論。

## Trigger Keywords

- schema
- JSON検証
- check-jsonschema
- ajv
- 型整合

## Examples

### Example 1

Input: `notes/*.json` を schema に合わせて検証して。
Output: `npm run schema:check` の結果を解析し、違反キーのみ修正案を提示する。

### Example 2

Input: AI profile JSON の不整合を見つけて。
Output: `schemas/ai_profile.schema.json` との不一致点を行単位で列挙する。

### Example 3

Input: 検証失敗時の直し方を具体化して。
Output: 必須キー追加、型変換、不要キー削除の順で最小修正手順を示す。
