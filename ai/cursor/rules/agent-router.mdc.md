---
description: '依頼内容から最適な agent/skill を選ぶ規律 / Dispatch rules for agents & skills'
alwaysApply: true
---

# ルーティング規律 / Routing Policy

## 共通 / Common

- まず問題を 1 行で定義し、次に最短経路を選ぶ。
- “ついでのリファクタ” はしない（必要なら別タスク化）。

## 使い分け / When to use what

- 仕様・最新情報・CVE・互換性 → `tech-researcher`
- 全体像・影響範囲・どこを触るべきか → `codebase-explorer`
- diff/PR レビュー・品質ゲート → `task-reviewer`
- テスト失敗・CI 赤 → `test-runner`
- 認可/入力/秘密/攻撃面 → `security-reviewer`

## Skill 呼び出し / Skill triggers

- lint/format を通す → `lint-fix`
- diff/commit/PR を整える → `git-helper`
- どれを使うか迷う → `skill-discoverer`（提案のみ、実行は承認後）
