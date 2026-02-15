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

---

## 1. Workflow

1. **Intake**: 検証対象の JSON ファイルパスと適用スキーマ（`schemas/ai_profile.schema.json` または `schemas/notes.schema.json`）を特定する。
2. **Run Validation**: `npm run schema:check` を実行し、エラー出力を収集する。
3. **Parse Errors**: エラーをファイル・キーパス・違反種別（必須キー欠落、型不一致、不要キー、enum 不一致）に分類する。
4. **Generate Fixes**: 違反種別ごとに最小修正案を生成する。修正順序: 必須キー追加 → 型変換 → 不要キー削除 → enum 修正。
5. **Apply & Verify**: Edit で修正を適用し、`npm run schema:check` を再実行して exit 0 を確認する。

## 2. Checklist

### Pre-flight

- [ ] 対象 JSON ファイルのパスを特定済み
- [ ] 適用スキーマ（ai_profile / notes）を把握済み
- [ ] `check-jsonschema` がインストール済み

### Post-flight

- [ ] `npm run schema:check` が exit 0
- [ ] 修正差分が最小（違反箇所のみ変更）
- [ ] スキーマ自体は変更していない（意図的変更を除く）

## 3. Output Format

```markdown
## schema-guard Report

**Verdict**: PASS | FAIL
**Target**: <file path(s)>
**Schema**: <schema file path>

### Violations

| #   | File                   | Key Path           | Violation | Expected | Actual  |
| --- | ---------------------- | ------------------ | --------- | -------- | ------- |
| 1   | ai/claude/profile.json | $.metadata.version | required  | present  | missing |

### Fixes Applied

| #   | File                   | Key Path           | Action | Detail  |
| --- | ---------------------- | ------------------ | ------ | ------- |
| 1   | ai/claude/profile.json | $.metadata.version | ADD    | "1.0.0" |

### Verification

| Command                | Exit Code | Status |
| ---------------------- | --------- | ------ |
| `npm run schema:check` | 0         | PASS   |
```

## 4. Memory Strategy

- **Persist**: スキーマの必須フィールド一覧と頻出違反パターンをキャッシュし、エラー解析を高速化する。
- **Invalidate**: `schemas/` 配下のスキーマファイルが変更された場合、または `.config/jsonschema.conf.yaml` が変更された場合にキャッシュを無効化する。
- **Share**: 検証結果を `content-writer` Agent に提供し、JSON 書き込み時のバリデーション基準とする。FAIL 結果を `lint-fix` に提供し、自動修正の入力とする。
