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

## Precedence Rules

1. グローバル資産（`~/.claude/`）は汎用規律（探索・調査・検証）を提供する。
2. プロジェクト資産（`.claude/`）はリポジトリ固有のコマンド・テンプレート・規約を持つものだけ配置する。
3. 同名資産が両方に存在する場合、プロジェクト版が優先される。
4. グローバルで十分な機能はプロジェクトに複製しない（重複禁止）。

## Agent Boundaries

- `.claude/agents` はリポジトリ固有の調査・検証・記述に関する委任のみ定義する。
- 汎用的な探索・調査・品質監査はグローバルエージェント（`~/.claude/agents/`）に委任する。
- 実装手順の正典は AGENTS.md と Skill 本文を優先する。
