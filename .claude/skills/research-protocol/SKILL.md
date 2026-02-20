---
name: research-protocol
description: Use when external specifications need source-grounded verification with dated citations and explicit fact boundaries; When NOT to use: when the task is fully local and does not depend on external facts; Trigger Keywords: [最新, 仕様確認, 出典, citation, 検証].
---

# research-protocol

## When to use

- 外部仕様の最新版確認が必要な場合。
- src/main や build.sh の依存先バージョンを一次情報で検証する場合。

## When NOT to use

- ローカル変更のみで外部情報を参照しない場合。
- 出典日付を提示できない調査結果しかない場合。

## Trigger Keywords

- 最新
- 仕様確認
- 出典
- citation
- 検証

## Procedure

1. 依頼文を読み、対象範囲と期待成果を明確化する。
2. 関連ファイルと既存規約を確認し、最小差分で実行する。
3. 検証コマンドの結果を記録し、結論と残課題を報告する。

## Examples

### Example 1

Input: src/main で使う SDK バージョン上限を確認したい。
Output: 公式ドキュメント URL と確認日を添えて確定情報を提示する。

### Example 2

Input: build.sh 内コマンドの推奨フラグが変わったか確認したい。
Output: 一次情報に基づき旧仕様との差分を報告する。

### Example 3

Input: src/worker の外部 API 制限値を検証したい。
Output: 事実と推測を分離した監査結果を提示する。
