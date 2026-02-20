---
name: docs-sync
description: Use when README and structure documents must be synchronized with actual repository layout and commands; When NOT to use: when changes are isolated and documentation truth remains unchanged; Trigger Keywords: [README, directorystructure, technologystack, 同期, 実態反映].
---

# docs-sync

## When to use

- リポジトリ実態に合わせて文書を同期する場合。
- src/main、src/worker、src/common、build.sh の説明差分を反映する場合。

## When NOT to use

- 実装差分が文書に影響しない場合。
- 構造が未確定で確定版文書を更新できない場合。

## Trigger Keywords

- README
- directorystructure
- technologystack
- 同期
- 実態反映

## Procedure

1. 依頼文を読み、対象範囲と期待成果を明確化する。
2. 関連ファイルと既存規約を確認し、最小差分で実行する。
3. 検証コマンドの結果を記録し、結論と残課題を報告する。

## Examples

### Example 1

Input: src/main 新規エントリ追加後に README を同期したい。
Output: ディレクトリ説明と起動手順を実態に合わせて更新する。

### Example 2

Input: build.sh の引数変更を運用文書へ反映したい。
Output: 旧手順を置換し確認コマンドを追記する。

### Example 3

Input: src/common の共有モジュール整理を文書へ反映したい。
Output: 構造図と説明文を同時更新する。
