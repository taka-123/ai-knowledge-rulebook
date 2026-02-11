---
name: git-helper
description: Guide safe commit/PR/release workflows. Auto-trigger keywords: commit, branch, PR, changelog, review, release.
---

# Git Helper

## ワークフロー

1. 変更範囲とブランチの状態を要約する。
2. 最小限のコミットグループと PR チェックリストを提案する。
3. リスクのある操作を明示し、確認を求める。
4. 非破壊的な git コマンドのみを提案する。

## 安全規約

- `git push --force` は実行禁止。
- <SCRUTINY_REQUIRED> push, merge, 履歴書き換えは承認必須。
