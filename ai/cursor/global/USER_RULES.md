# Cursor Settings > Rules & Memories > User Rules

[../../common/global/AGENTS.md](../../common/global/AGENTS.md)に記載のものを添付

## Global Reasoning Protocol

### 探索対象

- Skills: `~/.cursor/skills/<skill>/SKILL.md` / `.cursor/skills/<skill>/SKILL.md`
- Subagents: `~/.cursor/agents/*.md` / `.cursor/agents/*.md`

### 運用ルール

- 複雑な依頼では、推論前に `~/.cursor/` と `./.cursor/` の Skills/Subagents を確認する。
- 該当する専門家がいる場合、メイン窓での長い推論を避けて即座に委任する。
- スキル名に言及がある場合は、該当 `SKILL.md` を JIT でロードする。

### 優先ロードトリガー

- CSS・Tailwind・UIコンポーネントの編集・追加時 → `ui-standardizer`
- 「バックログ用のmd記法で」等の依頼時 → `backlog-markdown-formatting`
