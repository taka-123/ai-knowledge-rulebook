# Project Constitution for Claude Code

## Canonical Source

- Skill 実体は `.claude/skills/<name>/SKILL.md` に限定する。
- ルーターや補助設定には Skill 本文を複製しない。

## Routing Policy

- 各 agent/skill の description 内の Trigger Keywords で自動マッチする。
- 同名資産がグローバルとプロジェクトに存在する場合、プロジェクト版が優先。
- 完了前に `format-lint-audit` で品質ゲートを確認する。

## Repository Commands

- `npm run format:check`
- `npm run schema:check`
- `npm run lint:md` / `npm run lint:yaml` / `npm run lint:json`
