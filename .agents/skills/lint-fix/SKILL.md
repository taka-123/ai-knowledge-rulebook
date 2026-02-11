---
name: lint-fix
description: Resolve lint/format/schema failures with minimal edits. Auto-trigger keywords: lint, format, prettier, markdownlint, yamllint, schema, test, CI.
---

# Lint Fix

## Single Workflow

1. Identify failing lint/format/schema command.
2. Apply the smallest patch to satisfy the failing rule.
3. Re-run only the necessary verification command(s).
4. Report pass/fail with remaining risks.

## Safety

- Auto-fix commands that modify many files require user confirmation.
