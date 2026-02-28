# Description Condition Patterns

## Required starts

- 実装・修正・検証系: `Use proactively when editing any file under ...`
- 明示依頼待ち系: `Use when the user explicitly asks ...`

## Required elements

1. 具体的なパスまたはディレクトリ名（例: `.claude/agents/`, `.codex/config.toml`, `notes/topics/`）。
2. タスク種別（例: implementation, review, validation, scaffolding）。
3. 3要素形式（Use when / When NOT to use / Trigger Keywords）。

## Anti-patterns

- `Use when editing framework code`（抽象的で発火率が低い）
- `Use when needed`（条件不明）
- Trigger Keywords だけで条件を表現する description
