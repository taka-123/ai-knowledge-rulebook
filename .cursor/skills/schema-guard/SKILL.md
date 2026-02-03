---
name: schema-guard
description: Validates JSON schema for ai/ and notes/ using npm run schema:check. Use when the user mentions schema, json validation, ai profile, or notes json.
disable-model-invocation: true
---

# Schema Guard

## Quick Start

1. Run `npm run schema:check`.
2. If failures occur, identify the exact file and field from the output.
3. Propose the smallest correction and re-run the check.

## Decision Rules

- Do not modify schema files unless the user explicitly asks.
- Prefer fixing data files over relaxing schemas.

## Output Format

検証:

- コマンド: npm run schema:check
  結果: pass/fail
  問題:
- ...
  修正方針:
- ...
  再検証:
- 実施/未実施

## Verification

- Always report the command output summary and whether re-check passed.
