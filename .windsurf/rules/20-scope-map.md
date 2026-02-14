# Windsurf Scope Map

## Root vs Subdir

- Root rules define shared behavior.
- Subdir rules are allowed only for local constraints and must not repeat root text.

## File-Aware Hints

- `.work/*.md` updates: apply `documentation-standards` and `format-lint-audit`.
- `scripts/*.mjs` updates: apply `task-planner` and `lint-fix`.
- `AGENTS.md` / `CLAUDE.md` updates: apply `docs-sync`.
- Canonical skill path: `.claude/skills/<name>/SKILL.md`.
