---
name: git-helper
description: Use when repository changes must be grouped into reviewable commits with safe rollback guidance; When NOT to use: when no file changes exist or version control operations are out of scope; Trigger Keywords: [commit, branch, diff, PR, rollback].
---

# git-helper

## When to use

- 差分を意味単位で分割してレビューしやすくしたい場合。
- 複数モジュールの変更を安全にロールバックできる形でまとめたい場合。

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

1. `git status --short` と `git diff --name-only` で変更全体を可視化する。
2. 差分を「意図単位」でグルーピングする（機能追加/修正/整形/ドキュメント）。
3. 各グループごとにコミットメッセージ案を作る（1コミット1意図）。
4. PR説明テンプレート（目的/変更点/検証/リスク）を差分に合わせて埋める。
5. ロールバック手段（revert対象コミット）を 1 行で示す。

## Output Contract

- 必ず「コミット分割案 / 各メッセージ案 / PR本文案 / ロールバック方針」を出す。
- 変更のないファイルをコミット対象へ混ぜない。
- force push 前提の運用は推奨しない。

## Examples

### Example 1

Input: アプリケーション本体と共通ライブラリの変更を別コミットに分けたい。
Output: コミット分割案と各コミットの検証観点を提示する。

### Example 2

Input: ビルドスクリプトとドキュメント更新を同時に含む差分を整理したい。
Output: 実装変更と運用文書変更を分離する順序を示す。

### Example 3

Input: バックグラウンドジョブの不具合修正を安全に巻き戻したい。
Output: revert 前提のコミットメッセージ方針を提示する。
