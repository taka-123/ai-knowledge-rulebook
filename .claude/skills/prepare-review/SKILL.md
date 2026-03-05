---
name: prepare-review
description: "Use when the user explicitly asks to prepare review notes for current documentation changes; When NOT to use: when reviewing code logic rather than documentation quality; Trigger Keywords: [prepare-review, review notes, review prep, doc review, change summary]."
---

# prepare-review

Prepare focused review notes for current documentation changes. Captures working tree state, classifies changes, and generates a checklist.

## When to use

- ドキュメント変更のレビュー観点を整理したいとき。
- PR 前に変更分類とチェックリストを作成したいとき。
- FrontMatter・リンク・スキーマ整合性を一括確認したいとき。

## When NOT to use

- コードロジックのレビューが主目的のとき（`code-reviewer` が適切）。
- 変更がまだ作業中で確定していないとき。
- ドキュメント以外のファイルのみが変更対象のとき。

## Trigger Keywords

- prepare-review
- review notes
- review prep
- doc review
- change summary

## Procedure

1. `git status --short` と `git diff --stat` で変更範囲を確認する。完了条件: 変更ファイル一覧が確定。
2. `git diff --unified=0 -- '*.md' '*.mdx' '*.json' '*.yaml' '*.yml'` でドキュメント差分を取得する。完了条件: 差分内容を把握。
3. 変更を用途別（ガイド/リファレンス/設定ファイル等）に分類する。完了条件: 分類が完了。
4. 各分類でレビューチェックリストを作成する:
   - 出典の有無（URL + 取得日）
   - FrontMatter 必須項目（`created`, `updated`, `tags`）
   - スキーマ整合性（JSON Schema 準拠）
   - リンク切れの確認
   - コードブロックの言語指定
5. 各項目のステータスを判定し、リスクをまとめる。完了条件: チェックリスト完成。

## Output Contract

| Item                  | Format                       |
| --------------------- | ---------------------------- |
| Change Classification | 用途別のファイル分類表       |
| Review Checklist      | `- [ ]` 形式のチェックリスト |
| Status                | 各項目に PASS / WARN / FAIL  |
| Risks                 | 想定リスクと追加確認事項     |

### NG例

- 差分を確認せずにチェックリストを作る（根拠不足）。
- コードファイルの変更をドキュメントレビューに混ぜる（責務外）。
- ステータス判定なしでチェックリストだけ返す（判断不能）。

## Examples

### Example 1

Input: `/prepare-review`
Output: 現在の変更全体を分類し、チェックリスト付きレビューノートを生成。

### Example 2

Input: `.claude/skills/` 配下の SKILL.md を複数更新した後にレビュー準備したい。
Output: スキル定義変更に特化したチェックリスト（description 品質、examples 有無等）。

### Example 3

Input: `notes/topics/` に新規ノートを追加した後にレビュー準備したい。
Output: FrontMatter 準拠とスキーマ整合性に重点を置いたチェックリスト。
