---
name: ui-standardizer
description: Use when UI or CSS updates must follow repository visual conventions and accessibility checks across app surfaces; When NOT to use: when tasks are backend-only and have no presentation layer impact; Trigger Keywords: [UI, CSS, レイアウト, accessibility, a11y].
---

# ui-standardizer

## When to use

- UI 実装の見た目とアクセシビリティを同時に整えたい場合。
- src/main 側の表示と src/common デザイン定数を統一したい場合。

## When NOT to use

- バックエンド処理のみで UI 変更が発生しない場合。
- デザイン方針が未確定で規約適用ができない場合。

## Trigger Keywords

- UI
- CSS
- レイアウト
- accessibility
- a11y

## Procedure

1. 依頼文を読み、対象範囲と期待成果を明確化する。
2. 関連ファイルと既存規約を確認し、最小差分で実行する。
3. 検証コマンドの結果を記録し、結論と残課題を報告する。

## Examples

### Example 1

Input: src/main/components/dashboard.css の余白ルールを統一したい。
Output: 既存変数に寄せた spacing 指針と修正順を提示する。

### Example 2

Input: src/common/theme.ts の色定義を画面全体へ反映したい。
Output: 利用箇所を列挙し、段階的な置換計画を提示する。

### Example 3

Input: build.sh 後の UI 回帰確認を短時間で実施したい。
Output: 主要画面チェックリストと a11y 観点を提示する。
