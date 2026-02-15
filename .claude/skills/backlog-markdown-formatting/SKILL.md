---
name: backlog-markdown-formatting
description: Use when markdown must be normalized for Backlog-friendly structure, heading consistency, and checklist readability; When NOT to use: plain prose edits without formatting requirements; Trigger Keywords: Backlog, markdown整形, 見出し, checklist, issue.
---

# backlog-markdown-formatting

## When to use

- Backlog 貼り付け向けに Markdown を整形する。
- 見出し・箇条書き・チェックリストの一貫性が必要。

## When NOT to use

- 単なる内容レビュー。
- プレーンテキストの短文回答。

## Trigger Keywords

- Backlog
- markdown整形
- 見出し
- checklist
- issue

## Examples

### Example 1

Input: この作業メモを Backlog 用の Markdown に整形して。
Output: 見出し階層を統一し、タスクをチェックリスト化して出力する。

### Example 2

Input: 混在した箇条書きを読みやすくしたい。
Output: 番号付き手順と補足を分離し、冗長な空行を削除する。

### Example 3

Input: リスクと対応策を Backlog テンプレに合わせて再構成して。
Output: `結論 -> 根拠 -> 対応策` の順に並べた Markdown を生成する。

---

## 1. Workflow

1. **Intake**: 整形対象のテキスト（作業メモ、課題記述、レポート）と出力先（Backlog Issue / Wiki / コメント）を確認する。
2. **Structure Analysis**: 入力テキストの構造（見出し、箇条書き、チェックリスト、表）を解析し、Backlog Markdown との互換性を検証する。
3. **Normalize**: 以下の規則で整形する。
   - 見出し: `##` から開始（`#` は Backlog が自動付与するため不使用）
   - チェックリスト: `- [ ]` 形式に統一
   - 箇条書き: 番号付き手順と補足を分離
   - 空行: 見出し前後に 1 行、連続空行は 1 行に圧縮
   - 結論先行: `結論 → 根拠 → 補足` の順序を強制
4. **Output**: 整形済み Markdown を出力する。
5. **Verify**: `npm run lint:md` で構文チェックし、Backlog 互換性を確認する。

## 2. Checklist

### Pre-flight

- [ ] 入力テキストが提供されている
- [ ] 出力先（Issue / Wiki / コメント）が確定している
- [ ] Backlog 固有の Markdown 制約を把握済み

### Post-flight

- [ ] 見出し階層が `##` から開始している
- [ ] チェックリストが `- [ ]` 形式で統一されている
- [ ] 結論先行の構成になっている
- [ ] 連続空行が圧縮されている
- [ ] `npm run lint:md` が exit 0

## 3. Output Format

```markdown
## backlog-markdown-formatting Report

**Action**: FORMAT
**Target**: <input description>
**Output For**: Backlog Issue | Wiki | Comment

### Formatting Changes

| #   | Change           | Before           | After            |
| --- | ---------------- | ---------------- | ---------------- |
| 1   | Heading level    | `# Title`        | `## Title`       |
| 2   | Checklist format | `* task`         | `- [ ] task`     |
| 3   | Structure        | Background first | Conclusion first |

### Formatted Output

<formatted markdown content>

### Verification

| Check             | Result               |
| ----------------- | -------------------- |
| Heading hierarchy | `##` start confirmed |
| Checklist format  | `- [ ]` unified      |
| Markdown Lint     | PASS                 |
```

## 4. Memory Strategy

- **Persist**: Backlog Markdown の整形ルール（見出し開始レベル、チェックリスト形式、空行ルール）をキャッシュし、次回の整形を高速化する。
- **Invalidate**: Backlog の Markdown 仕様が変更された場合にキャッシュを無効化する。
- **Share**: 整形結果を `documentation-standards` Skill の規約チェックに提供し、プロジェクト規約との整合性を確認する。
