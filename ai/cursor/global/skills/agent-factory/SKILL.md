---
name: agent-factory
description: ユーザーの要求に基づき、新しい Subagent または Skill を設計・生成する。Subagent/Skill の新規作成を依頼されたとき、または /agent-factory で手動起動する。
disable-model-invocation: true
---

# Skill: Agent Factory

## 目的

プロジェクト固有、あるいは特定の高度なタスクに特化した Subagent/Skill の設定ファイルを自動生成する。

## 生成プロトコル

1. **要求分析**: ユーザーが求めているのが「独立した作業環境（Subagent）」か「再利用可能な知識（Skill）」かを判定せよ。
2. **規律の継承**: 生成されるプロンプトには、必ず「一次情報への接地（URL+取得日）」「RFC 2119 準拠」の精神を注入せよ。
3. **ツール・権限**: Cursor 用なら `context7` の利用可否を、Claude Code 用なら `allowed-tools` 制限を含めたテンプレートを提示せよ。不必要な Full Access は避ける。

## テンプレート（Subagent の場合）

```markdown
---
name: [エージェント名]
description: [明確な発動条件を含む説明]
---

あなたは [役割] です。以下のプロトコルに従い、[目標] を達成せよ。

- ...
```

## テンプレート（Skill の場合）

```markdown
---
name: [スキル名]
description: [何をするか]。[いつ使うか] に使用。
---

# [スキル名]

## いつ使うか
- ...

## 手順
1. ...
```
