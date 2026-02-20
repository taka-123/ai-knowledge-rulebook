---
name: content-scaffold
description: Use when new repository documents or rule files must be scaffolded from standardized structures with validation commands; When NOT to use: when existing files only need small edits without structural scaffolding; Trigger Keywords: [新規ファイル, scaffold, テンプレート, 雛形, 初期化].
---

# content-scaffold

## When to use

- 新規ファイルを規約準拠テンプレートで作成する場合。
- src/main や src/worker の実装手順書をゼロから起票する場合。

## When NOT to use

- 既存ファイルへ数行追記するだけの場合。
- 生成後の検証コマンドを実行できない場合。

## Trigger Keywords

- 新規ファイル
- scaffold
- テンプレート
- 雛形
- 初期化

## Procedure

1. 依頼文を読み、対象範囲と期待成果を明確化する。
2. 関連ファイルと既存規約を確認し、最小差分で実行する。
3. 検証コマンドの結果を記録し、結論と残課題を報告する。

## Examples

### Example 1

Input: src/common の新規モジュール説明書を作りたい。
Output: 見出し構成、参照形式、検証コマンドを含む雛形を生成する。

### Example 2

Input: build.sh 改修の運用チェックシートを作りたい。
Output: 実行前提と合否条件を含む初期文書を作成する。

### Example 3

Input: src/main API 用の変更記録テンプレートがほしい。
Output: 再利用可能な章立てとサンプル記述を生成する。
