---
name: schema-guard
description: Use when JSON assets must be validated against repository schemas and corrected with minimal diffs; When NOT to use: when no schema boundary exists or the task is non-JSON only; Trigger Keywords: [schema, JSON検証, check-jsonschema, ajv, 型整合].
---

# schema-guard

## When to use

- `npm run schema:check` が失敗していて、どの JSON の何が違反しているか特定したい場合。
- `ai/` または `notes/` 配下の JSON ファイルを編集した後にスキーマ適合性を確認したい場合。

## When NOT to use

- JSON を扱わない作業のみの場合。
- `schemas/` にスキーマ定義が存在しない対象に対して検証を要求する場合。

## Trigger Keywords

- schema
- JSON検証
- check-jsonschema
- ajv
- 型整合

## このリポジトリのスキーマ構成

| 検証対象 | スキーマファイル |
|---|---|
| `ai/**/*.json` | `schemas/ai_profile.schema.json` |
| `notes/**/*.json` | `schemas/notes.schema.json` |

検証コマンド: `npm run schema:check`

## Procedure

1. `npm run schema:check` を実行してエラー出力全体を取得する。
2. エラーメッセージから「どのファイル」「どのフィールド」が違反しているかを特定する。
3. 対応するスキーマファイル（`schemas/*.json`）を読み、**required フィールド・型・enum 値**を確認する。
4. 違反フィールドのみを最小差分で修正する（スキーマに定義されていない余分なフィールドは追加しない）。
5. `npm run schema:check` を再実行し、exit 0 を確認する。

## Output Contract

| 項目 | 内容 |
|---|---|
| 失敗ファイル | `ai/foo/profile.json` |
| 違反フィールド | `required: ["title"]` が未定義 |
| 修正内容 | `"title": "..."` を追加 |
| 再実行結果 | exit 0 (PASS) |

- 複数ファイルが失敗している場合は、全件を上記表形式で列挙してから一括修正する。
- 修正が複数フィールドにまたがる場合も、1 回の再実行で全件 PASS を目指す。

### NG例

```
❌ エラーメッセージを読まずにフィールドを推測で追加する
❌ スキーマに定義されていないフィールドを追加する（別のバリデーションエラーになる）
❌ JSON の構造（配列↔オブジェクト）をスキーマ確認なしで変える
❌ 修正後に schema:check を再実行しない
```

## Examples

### Example 1

Input: `npm run schema:check` が `ai/profiles/gpt4.json` で失敗している。
Output: エラー内容から不足フィールドを特定し、`schemas/ai_profile.schema.json` を確認して最小追記を行い、再実行で exit 0 を確認する。

### Example 2

Input: `notes/2025/q1.json` に型違反がある（string を期待しているフィールドに number が入っている）。
Output: 対象フィールドのみ型を修正し、他のフィールドは触らずに `npm run schema:check` が PASS することを確認する。

### Example 3

Input: 新規に `ai/profiles/new-model.json` を追加したい。
Output: `schemas/ai_profile.schema.json` の required フィールドを全て含む最小構成 JSON を生成し、`npm run schema:check` が exit 0 であることを確認する。
