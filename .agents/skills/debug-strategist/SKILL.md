---
name: debug-strategist
description: Diagnose errors with reproduce-isolate-fix flow. Auto-trigger keywords: debug, bug, error, stacktrace, flaky, failing test, CI failure.
---

# Debug Strategist

## Single Workflow

1. Reproduce the issue with the smallest command or scenario.
2. Isolate probable root cause using focused file/trace inspection.
3. Propose the smallest safe fix and expected impact.
4. Validate via relevant test/lint command.
5. Escalate if fix requires deploy/migration or destructive git actions.

## Safety

- `deploy`, `migrate`, `terraform apply`, `git push --force` require explicit approval.
