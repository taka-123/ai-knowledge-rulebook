# Cursor Settings > Rules & Memories > User Rules

[../../common/global/AGENTS.md](../../common/global/AGENTS.md)に記載のものを添付

## Cursor 固有アダプタ

### 探索対象

- Skills: `~/.cursor/skills/<skill>/SKILL.md` / `.cursor/skills/<skill>/SKILL.md`
- Subagents: `~/.cursor/agents/*.md` / `.cursor/agents/*.md`

### 運用ルール

- タスク開始時に、関連する Skills/Subagents の有無だけ先に確認する。
- スキル名・エージェント名が明示された場合は、該当定義を JIT ロードして優先適用する。
