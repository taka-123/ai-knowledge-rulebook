---
name: agent-factory
description: Create or update one agent/skill/rule/workflow at a time with minimal scaffolding. Auto-trigger keywords: agent, skill, rule, workflow, template, scaffold, router.
---

# Agent Factory

## ワークフロー

1. 対象ツールと配置パスを確認する。
2. 既存の正規名（`tech-researcher`, `codebase-explorer` 等）を再利用し、重複を避ける。
3. 1ファイル＝1目的で最小限のファイルを生成する。
4. description に発火キーワードを含め、自動検出を有効にする。
5. deploy/migrate/push --force が関わる場合は承認必須と明記する。

## 出力規約

- 作成・編集したパスのみ報告する。
- 各ファイルの役割を1行で説明する。
