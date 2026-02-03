---
name: format-lint-audit
description: Runs project format/lint checks and reports results. Use when the user mentions format, lint, 整形, 検証, prettier, markdownlint, yamllint, or lint errors.
disable-model-invocation: true
---

# Format/Lint Audit

## Quick Start

1. Run `./format.sh check`.
2. If the change touches specific types, run the minimal extra checks:
   - Markdown: `npm run lint:md`
   - YAML: `npm run lint:yaml`
   - JSON: `npm run lint:json`
3. Report pass/fail and next actions succinctly.

## Decision Rules

- Do not auto-fix unless explicitly requested.
- Do not install new dependencies.
- If a command fails, capture the error and propose the smallest fix.

## Output Format

検証:

- コマンド: ...
  結果: pass/fail
  問題:
- ...
  次の手:
- ...

## Verification

- Always include the exact commands executed and their outcomes.
