---
name: git-helper
description: Prepare safe git workflows for commit/PR/review/release tasks. Auto-trigger keywords: commit, branch, PR, rebase, changelog, release, review.
---

# Git Helper

## Single Workflow

1. Summarize changed scope and branch context.
2. Propose minimal commit grouping and PR checklist.
3. Highlight risky operations and require confirmation.
4. Provide non-destructive git command suggestions.

## Safety

- Never run `git push --force`.
- Any push, merge, or history rewrite needs explicit approval.
