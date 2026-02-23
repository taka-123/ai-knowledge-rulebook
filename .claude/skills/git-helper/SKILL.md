---
name: git-helper
description: Use when repository changes must be grouped into reviewable commits with safe rollback guidance; When NOT to use: when no file changes exist or version control operations are out of scope; Trigger Keywords: [commit, branch, diff, PR, rollback].
---

# git-helper

## When to use

- 複数ファイルの変更を意味単位でコミットに分割してレビューしやすくしたい場合。
- 変更を安全にロールバックできる形でまとめたい場合。

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

1. `git status --short` と `git diff --staged --name-only` で変更全体を可視化する。
2. 差分を「意図単位」でグルーピングする（機能追加 / バグ修正 / 整形 / ドキュメント）。
3. 各グループごとにコミットメッセージ案を作る（1コミット1意図、`feat:` / `fix:` / `docs:` 等の prefix を使う）。
4. PR 説明テンプレート（目的 / 変更点 / 検証方法 / ロールバック方針）を差分に合わせて埋める。
5. ロールバック手段（`git revert <SHA>` または対象コミット）を 1 行で示す。

## Output Contract

必ず以下の順で提示する：

1. **コミット分割案**: グループ名と含めるファイル一覧
2. **各コミットメッセージ案**: `type: 内容` 形式
3. **PR 本文案**: 目的・変更点・検証・ロールバック
4. **ロールバック方針**: `git revert` 対象を明記

### NG例

```
❌ 変更意図が異なるファイルを1コミットに混ぜる
❌ 変更していないファイルをコミット対象に含める
❌ force push 前提の運用を推奨する（main への force push は原則禁止）
❌ ロールバック方針を省略する
```

## Examples

### Example 1

Input: スキルファイルの改良とスクリプトの追加が混在している。
Output: スキル改良コミット + スクリプト追加コミットに分割案を示し、各メッセージと PR 本文案を提示する。

### Example 2

Input: ドキュメント更新と JSON 修正を整理してコミットしたい。
Output: `docs:` コミットと `fix:` コミットに分離し、`git revert` 対象を明示する。

### Example 3

Input: 誤ってコミットした変更を安全に巻き戻したい。
Output: `git revert <SHA>` コマンドと、revert コミットのメッセージ案を提示する。
