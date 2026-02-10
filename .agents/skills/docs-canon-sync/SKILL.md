---
name: docs-canon-sync
description: Canonical docs synchronization for README同期, directorystructure更新, technologystack更新, and 地図化 tasks. Use when asked to align docs with actual repository state.
---

# Docs Canon Sync

## 手順

1. `README.md` `directorystructure.md` `technologystack.md` と実ファイル構造を突合する。
2. 不整合を「不足」「過剰」「記述ずれ」に分類する。
3. 変更候補を最小差分で提案し、対象セクションを明示する。
4. `@参照` と相対リンク、コマンド表記の整合性を確認する。
5. 更新後は関連ドキュメント間で同じ事実が維持されているか再チェックする。

## Safety

- 大量置換や全面書き換えは行わない。承認されたセクションのみ変更する。
- 運用リスクのある操作（`git push` `deploy` `migrate` `infra` `db`）は提案止まりにし、承認後に実行する。

## 継承

- `codebase-explorer` の構造抽出と `task-reviewer` の要件照合を継承する。
