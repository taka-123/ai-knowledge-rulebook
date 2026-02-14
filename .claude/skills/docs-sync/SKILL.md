---
name: docs-sync
description: Use when README, directory structure, and technology stack documents must be synchronized with current repository reality; When NOT to use: isolated feature work without documentation impact; Trigger Keywords: README, directorystructure, technologystack, 同期, 実態反映.
---

# docs-sync

## When to use

- 主要ドキュメントを実態と同期したい。
- 構成変更に伴って説明を更新する。

## When NOT to use

- ドキュメント非対象の作業。
- 実態差分が無い場合。

## Trigger Keywords

- README
- directorystructure
- technologystack
- 同期
- 実態反映

## Examples

### Example 1

Input: 新しい rules ディレクトリ追加をドキュメントへ反映して。
Output: `directorystructure.md` の該当ツリーを更新し、README の参照を整合させる。

### Example 2

Input: 実行コマンドが変わったので説明を同期して。
Output: `package.json` の scripts と一致するように運用手順を更新する。

### Example 3

Input: 技術スタックのバージョン表記を実態に合わせたい。
Output: `technologystack.md` を現行 `package.json`/実行環境に合わせて修正する。
