---
name: git-helper
description: Use when changes must be grouped into reviewable commits with safe rollback guidance and minimal diff noise; When NOT to use: unrelated design tasks without repository changes; Trigger Keywords: commit, branch, diff, PR, rollback.
---

# git-helper

## When to use

- 変更差分を論理単位で整理したい。
- レビューしやすいコミット分割が必要。

## When NOT to use

- コード未変更の相談。
- Git 操作が範囲外の依頼。

## Trigger Keywords

- commit
- branch
- diff
- PR
- rollback

## Examples

### Example 1

Input: この変更をレビューしやすい2コミットに分ける案を出して。
Output: 司令塔配線変更と skill 本体変更を分離したコミット計画を提示する。

### Example 2

Input: 失敗した修正を安全に戻す手順を教えて。
Output: `git restore` と `git revert` の使い分けを現在の状態に合わせて提示する。

### Example 3

Input: PR 説明文を差分中心で作りたい。
Output: 目的、主要変更、検証結果、リスクを短く整理した PR テンプレを出力する。
