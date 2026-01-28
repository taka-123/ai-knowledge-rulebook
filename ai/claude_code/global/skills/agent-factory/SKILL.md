---
name: agent-factory
description: ユーザーの要求に基づき、新しい Subagent または Skill を設計・生成します。
disable-model-invocation: true # 重要：Claudeが勝手にエージェントを作らないよう、ユーザー起動(/agent-factory)に限定
---

# Skill: Agent Factory

## 🎯 目的

プロジェクト固有、あるいは特定の高度なタスクに特化した Subagent/Skill の設定ファイルを自動生成する。

## ⚙️ 生成プロトコル

1. **要求分析**: ユーザーが求めているのが「独立した作業環境（Subagent）」か「再利用可能な知識（Skill）」かを判定せよ。
2. **規律の継承**: 生成されるプロンプトには、必ず `tech-researcher` 由来の「一次情報への接地（URL+取得日）」「RFC 2119 準拠」の精神を注入せよ。
3. **最小権限の原則**:
   - 調査系なら `tools: Read, Grep, WebSearch`
   - 実装系なら `tools: Read, Edit, Bash`
   - 不必要な `Full Access` は避け、モデルは `sonnet` を推奨せよ。

## 📝 テンプレート（Subagentの場合）

```markdown
---
name: [エージェント名]
description: [明確な発動条件を含む説明]
tools: [必要最小限のツール]
model: sonnet
---

あなたは [役割] です。以下のプロトコルに従い、[目標] を達成せよ。

- ...
```
