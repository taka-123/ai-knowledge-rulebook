---
name: documentation-standards
description: Use when repository documents must follow consistent Japanese technical style, citations, and file reference conventions; When NOT to use: when the task is code-only and no documentation output is required; Trigger Keywords: [ドキュメント, 記述規約, 文章品質, 参照, 構成].
---

# documentation-standards

## When to use

- 技術文書を規約準拠で更新する必要がある場合。
- src/main、src/worker、src/common への参照表記を統一したい場合。

## When NOT to use

- コードのみの変更で文書更新が不要な場合。
- 一次情報がなく推測記述しかできない場合。

## Trigger Keywords

- ドキュメント
- 記述規約
- 文章品質
- 参照
- 構成

## Procedure

1. 依頼文を読み、対象範囲と期待成果を明確化する。
2. 関連ファイルと既存規約を確認し、最小差分で実行する。
3. 検証コマンドの結果を記録し、結論と残課題を報告する。

## Examples

### Example 1

Input: src/main の API 変更を README に追記したい。
Output: 結論先行で変更理由、影響範囲、検証結果を定型で記述する。

### Example 2

Input: build.sh の実行手順を運用ガイドへ反映したい。
Output: 前提条件、コマンド、失敗時対処を規約フォーマットで整理する。

### Example 3

Input: src/common 設定値の説明を統一したい。
Output: 用語定義と参照パス表記を揃えた文章へ修正する。
