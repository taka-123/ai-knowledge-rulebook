# Windsurf Router

Canonical skill source is `.claude/skills`.

## Priority

1. Planning -> `task-planner`
2. Debugging -> `debug-strategist`
3. Lint/Format fixes -> `lint-fix`
4. Final gate -> `format-lint-audit`

## Guardrails

- Do not duplicate skill body in Windsurf rules.
- Use root rules as primary and subdir rules only for minimal overrides.
