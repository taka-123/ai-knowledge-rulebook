---
name: documentation-standards
description: Use when repository documents must follow consistent Japanese technical writing style, file references, and verification notes; When NOT to use: code-only refactors with no documentation output; Trigger Keywords: ドキュメント, 記述規約, 文章品質, 参照, 構成.
---

# documentation-standards

## When to use

- 技術文書の体裁を統一する。
- 参照パスと検証記述を明確化する。

## When NOT to use

- ドキュメント更新が発生しない修正。
- 内部検証のみの一時作業。

## Trigger Keywords

- ドキュメント
- 記述規約
- 文章品質
- 参照
- 構成

## Examples

### Example 1

Input: AI_SCAN の報告書を規約準拠に整えて。
Output: 結論先行、根拠明示、ファイル参照付きの構成へ修正する。

### Example 2

Input: 手順書が冗長なので簡潔化したい。
Output: 重複説明を除去し、実行コマンドと判定基準を分離して整理する。

### Example 3

Input: パス表記を統一して読みやすくして。
Output: すべてのファイル参照をコード形式へ統一し、曖昧参照を削除する。

---

## 1. Workflow

1. **Intake**: 対象ドキュメントを Read で取得し、現行の文体・構成パターンを把握する。
2. **Convention Check**: 以下の規約への準拠を検証する。
   - 結論先行の日本語技術文体（結論 → 根拠 → 補足の順）
   - ファイル参照はコードスパン形式（`` `path/to/file` `` または `@` 参照）
   - 実行コマンドはコードブロック内に記載
   - 推測を含む記述には `（推測）` 注記
   - FrontMatter（該当時）はスキーマ準拠
3. **Violation Report**: 規約違反箇所を行番号付きで列挙する。
4. **Fix Proposal**: 違反箇所ごとに修正案を提示する。修正は既存スタイル（インデント、改行パターン、見出しレベル）を踏襲する。
5. **Verify**: 修正適用後、`npm run lint:md` で構文チェックし、参照の実在性を Glob で確認する。

## 2. Checklist

### Pre-flight

- [ ] 対象ドキュメントのパスが特定済み
- [ ] 現行の文体パターン（結論先行 / 手順型）を把握済み
- [ ] FrontMatter スキーマ要件を確認済み（該当時）

### Post-flight

- [ ] 全ファイル参照がコードスパン形式に統一されている
- [ ] 実行コマンドがコードブロック内に記載されている
- [ ] 推測記述に `（推測）` 注記が付与されている
- [ ] `npm run lint:md` が exit 0
- [ ] 既存の見出しレベル・改行パターンが維持されている

## 3. Output Format

```markdown
## documentation-standards Report

**Action**: REVIEW | FIX
**Target**: <file path(s)>
**Violations**: <N> found

### Convention Violations

| #   | File              | Line | Rule             | Current          | Expected         |
| --- | ----------------- | ---- | ---------------- | ---------------- | ---------------- |
| 1   | notes/ai-tools.md | 15   | Reference format | plain text path  | code span `path` |
| 2   | clips/article.md  | 8    | Conclusion-first | Background first | Conclusion first |

### Fixes Applied

| #   | File              | Line | Change Description        |
| --- | ----------------- | ---- | ------------------------- |
| 1   | notes/ai-tools.md | 15   | Wrapped path in code span |

### Verification

| Check         | Command           | Result             |
| ------------- | ----------------- | ------------------ |
| Markdown Lint | `npm run lint:md` | PASS               |
| References    | Glob check        | 5 checked, 5 valid |
```

## 4. Memory Strategy

- **Persist**: プロジェクトの文体規約（結論先行パターン、参照形式、FrontMatter 構造）をキャッシュし、次回の検証を高速化する。
- **Invalidate**: 規約自体が変更された場合（本 SKILL.md の更新、または AGENTS.md の記述規約セクション変更時）にキャッシュを無効化する。
- **Share**: 規約違反リストを `content-writer` Agent に提供し、書き込み時の品質基準とする。修正結果を `doc-validator` Agent に提供し、最終検証の入力とする。
