# Windsurf Scope Map

## Root vs Subdir

- Root rules define shared behavior.
- Subdir rules are allowed only for local constraints and must not repeat root text.

## File-Aware Hints

- `AGENTS.md`, `CLAUDE.md` edits: apply `documentation-standards` then `format-lint-audit`.
- `package.json`, `format.sh`, `scripts/*.mjs` edits: apply `task-planner` and `lint-fix`.
- `.work/*.md` reports: apply `content-scaffold` and `documentation-standards`.
- Canonical skill path: `.claude/skills/<name>/SKILL.md`.
