---
name: schema-guard
description: Use when JSON assets must be validated against repository schemas and corrected with minimal diffs; When NOT to use: when no schema boundary exists or the task is non-JSON only; Trigger Keywords: [schema, JSON検証, check-jsonschema, ajv, 型整合].
---

# schema-guard

## When to use

- JSON 資産をスキーマ適合させる必要がある場合。
- src/common の設定 JSON を変更し schema check を通す必要がある場合。

## When NOT to use

- JSON を扱わない作業のみの場合。
- スキーマ定義が存在しない対象に対して検証を要求する場合。

## Trigger Keywords

- schema
- JSON検証
- check-jsonschema
- ajv
- 型整合

## Procedure

1. 依頼文を読み、対象範囲と期待成果を明確化する。
2. 関連ファイルと既存規約を確認し、最小差分で実行する。
3. 検証コマンドの結果を記録し、結論と残課題を報告する。

## Examples

### Example 1

Input: src/main で読む設定 JSON が schema check に失敗する。
Output: 不一致キーを特定し最小修正案を示す。

### Example 2

Input: src/worker ジョブ定義 JSON の型を見直したい。
Output: schema との差分を表で示し、修正順を提案する。

### Example 3

Input: build.sh 後の schema:check を安定化したい。
Output: 再現手順と再発防止の検証ポイントを提示する。
