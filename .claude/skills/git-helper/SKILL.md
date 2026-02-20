---
name: git-helper
description: Use when repository changes must be grouped into reviewable commits with safe rollback guidance; When NOT to use: when no file changes exist or version control operations are out of scope; Trigger Keywords: [commit, branch, diff, PR, rollback].
---

# git-helper

## When to use

- 差分を意味単位で分割してレビューしやすくしたい場合。
- src/main と src/worker の変更を安全にロールバックできる形でまとめたい場合。

## When NOT to use

- 実ファイル変更がなくコミット対象がない場合。
- Git 操作を伴わない単なる相談の場合。

## Trigger Keywords

- commit
- branch
- diff
- PR
- rollback

## Procedure

1. 依頼文を読み、対象範囲と期待成果を明確化する。
2. 関連ファイルと既存規約を確認し、最小差分で実行する。
3. 検証コマンドの結果を記録し、結論と残課題を報告する。

## Examples

### Example 1

Input: src/main と src/common の変更を別コミットに分けたい。
Output: コミット分割案と各コミットの検証観点を提示する。

### Example 2

Input: build.sh とドキュメント更新を同時に含む差分を整理したい。
Output: 実装変更と運用文書変更を分離する順序を示す。

### Example 3

Input: src/worker の不具合修正を安全に巻き戻したい。
Output: revert 前提のコミットメッセージ方針を提示する。
