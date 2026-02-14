# Project Constitution for Claude Code

## Canonical Source

- Skill 実体は `.claude/skills/<name>/SKILL.md` に限定する。
- ルーターや補助設定には Skill 本文を複製しない。

## Routing Policy

1. 依頼文に Trigger Keywords が含まれる場合、該当 Skill を優先起動する。
2. 複数候補がある場合は次の順序で選ぶ:
   - `task-planner` -> `debug-strategist` -> `lint-fix`
3. 完了前に `format-lint-audit` で品質ゲートを確認する。

## Repository Commands

- `npm run format:check`
- `npm run schema:check`
- `npm run lint:md`
- `npm run lint:yaml`
- `npm run lint:json`

## Agent Boundaries

- `.claude/agents` は調査・検証・記述に関する委任のみ定義する。
- 実装手順の正典は AGENTS.md と Skill 本文を優先する。
