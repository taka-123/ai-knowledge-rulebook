# Agent Factory 設計ガイド

## Step 1: Subagent vs Skill の判定

| 観点     | Subagent                           | Skill                               |
| -------- | ---------------------------------- | ----------------------------------- |
| 実行環境 | 独立したツール・権限セットが必要   | 既存環境の知識・手順を拡張          |
| 完結性   | 独立したタスクを完結させる         | Claude の文脈に手順・知識を注入する |
| 代表例   | `security-reviewer`, `test-runner` | `organizing-commits`, `lint-fix`    |

## Step 2: 命名規則

- Skill: **gerund 形**を推奨（`processing-pdfs`, `reviewing-code`, `creating-agents`）
- 避けるべき語: `helper`, `utils`, `tools`, `documents`
- 制約: 最大 64 文字、小文字英数字とハイフンのみ

## Step 3: description の書き方

**三人称**で「何をするか」+ 3要素形式（Use when / When NOT to use / Trigger Keywords）を必ず含める。

## Step 4: 自由度（Degrees of Freedom）の設定

| 自由度 | 形式                         | 使いどころ                     |
| ------ | ---------------------------- | ------------------------------ |
| High   | テキスト指示のみ             | 複数アプローチが有効なとき     |
| Medium | 疑似コード                   | 好まれるパターンが存在するとき |
| Low    | 特定スクリプトの実行コマンド | 操作が脆弱・一貫性が必須のとき |

## Step 5: 最小権限の原則

- 調査系: `tools: Read, Grep, WebSearch`
- 実装系: `tools: Read, Edit, Bash`
- 不必要な Full Access を避け、`model: sonnet` を推奨。

## Step 6: 保存先パス

| 用途                             | パス                                                                   |
| -------------------------------- | ---------------------------------------------------------------------- |
| グローバル（全プロジェクト共通） | `~/.claude/skills/<name>/SKILL.md` または `~/.claude/agents/<name>.md` |
| プロジェクト固有                 | `.claude/skills/<name>/SKILL.md` または `.claude/agents/<name>.md`     |
