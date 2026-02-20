---
name: context-compress-map
description: Use when large repository context must be compressed into a navigable map of files, decisions, and next actions; When NOT to use: when task scope is already small and obvious from a single file; Trigger Keywords: [要約, コンテキスト, map, 全体像, 影響範囲].
---

# context-compress-map

## When to use

- 大規模変更の文脈を短く共有する必要がある場合。
- src/main、src/worker、src/common、build.sh の関係を俯瞰化する場合。

## When NOT to use

- 単一ファイルの局所修正で十分な場合。
- 詳細調査より実装優先で即時修正すべき場合。

## Trigger Keywords

- 要約
- コンテキスト
- map
- 全体像
- 影響範囲

## Procedure

1. 依頼文を読み、対象範囲と期待成果を明確化する。
2. 関連ファイルと既存規約を確認し、最小差分で実行する。
3. 検証コマンドの結果を記録し、結論と残課題を報告する。

## Examples

### Example 1

Input: 複数チーム向けに src 配下の改修全体像を共有したい。
Output: 変更点、依存、次アクションを1ページに圧縮して提示する。

### Example 2

Input: build.sh 更新の影響を短時間で説明したい。
Output: 実行フロー図と影響ファイル一覧を要約する。

### Example 3

Input: src/worker 障害対応の経緯を引き継ぎたい。
Output: 時系列と決定事項をコンパクトに整理する。
