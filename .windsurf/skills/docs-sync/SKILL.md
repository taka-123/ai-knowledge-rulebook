---
name: docs-sync
description: Sync README/directorystructure/technologystack with actual repo state. Auto-trigger keywords: README, directory, structure, tech stack, ドキュメント同期, 構成変更.
---

# Docs Sync

## ワークフロー

1. `README.md`, `directorystructure.md`, `technologystack.md` を実際のファイルツリーと比較する。
2. 不整合を「不足」「過剰」「記述ずれ」に分類する。
3. 確認済みの事実のみで最小限の編集を適用する。
4. `./format.sh check` を実行し結果を報告する。
