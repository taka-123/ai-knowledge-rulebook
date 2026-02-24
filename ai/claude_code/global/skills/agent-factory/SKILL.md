---
name: agent-factory
description: Designs and generates Subagent or Skill config files for new capabilities. Use when the user requests a new skill, new agent, or invokes /agent-factory explicitly. Do not invoke automatically without explicit user request.
---

# Skill: Agent Factory

<!-- 意図: 明示的な依頼（/agent-factory、「新しいスキルを作りたい」等）がある場合のみ起動。Claude が自律的に新規作成を判断して起動しない。 -->

## When to use

- 新しい Subagent または Skill の追加を明示的に依頼された場合。
- 既存スキルの責務分離・再設計を行う場合。

## When NOT to use

- 実装やドキュメント更新だけで解決できる場合。
- 既存スキルに 1〜2 行追記するだけで十分な場合。

## Trigger Keywords

- 新しいスキル / 新しいエージェント
- skill 作成 / agent 作成
- /agent-factory

---

## Step 1: Subagent vs Skill の判定

| 観点     | Subagent                           | Skill                               |
| -------- | ---------------------------------- | ----------------------------------- |
| 実行環境 | 独立したツール・権限セットが必要   | 既存環境の知識・手順を拡張          |
| 完結性   | 独立したタスクを完結させる         | Claude の文脈に手順・知識を注入する |
| 代表例   | `security-reviewer`, `test-runner` | `git-helper`, `lint-fix`            |

## Step 2: 命名規則

- Skill: **gerund 形**を推奨（`processing-pdfs`, `reviewing-code`, `creating-agents`）
- 避けるべき語: `helper`, `utils`, `tools`, `documents`
- 制約: 最大 64 文字、小文字英数字とハイフンのみ

## Step 3: description の書き方

**三人称**で「何をするか」+ 「Use when...」を必ず含める。

```
# Good
description: Generates commit messages by analyzing git diffs.
             Use when the user asks for help writing commit messages or reviewing staged changes.

# Bad
description: I can help you write commit messages.
description: コミットメッセージを書くのに使います。（一人称・Use when なし）
```

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

---

## Output Contract

- 生成物は**そのまま保存可能な frontmatter 付き**で返す。
- 「採用案 1つ + 代替案 1つ」の 2案を提示し、各案に「発動条件・対象タスク・禁止事項」を各 1 行で付ける。
- 生成プロンプトには一次情報への接地（URL + 取得日）と RFC 2119 準拠の精神を注入する。

---

## 📝 テンプレート: Skill

```markdown
---
name: [gerund-form-name]
description: [三人称で何をするか]. Use when [トリガー条件].
---

# Skill: [Name]

## When to use

- ...

## When NOT to use

- ...

## Trigger Keywords

- ...

## Procedure

1. ...

## Output Contract

- ...
```

保存先: `~/.claude/skills/[name]/SKILL.md` または `.claude/skills/[name]/SKILL.md`

## 📝 テンプレート: Subagent

```markdown
---
name: [agent-name]
description: [三人称で役割と発動条件]. Use when [トリガー条件].
tools: [必要最小限のツールリスト]
model: sonnet
---

あなたは [役割] です。以下のプロトコルに従い、[目標] を達成せよ。

## 責務

- ...

## 禁止事項

- ...
```

保存先: `~/.claude/agents/[name].md` または `.claude/agents/[name].md`
