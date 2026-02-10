---
name: codex-intelligence-maintainer
description: Project intelligence maintenance for Codex設定, .agents/skills, .codex/rules, and プロジェクト知能 tasks. Use when designing or evolving project-local skills and rules without duplicating global assets.
---

# Codex Intelligence Maintainer

## 手順

1. グローバル資産とプロジェクト資産を棚卸しし、重複を検出する。
2. 追加対象を「プロジェクト固有の反復作業」に限定する。
3. `./.agents/skills/` と `./.codex/rules/` の変更案を最小差分で設計する。
4. ルール案に allow/prompt/forbidden を分離し、危険操作の扱いを明示する。
5. 変更後に整合性チェック（命名、発火キーワード、安全規律）を実施する。

## Safety

- `~/.codex/*` と `~/.agents/*` は読み取り専用として扱い、変更しない。
- 危険操作（`git push` `deploy` `migrate` `infra` `db`）は提案のみとし、承認後に実行する。
- 既存ファイルがある場合は上書きせず、最小パッチで更新する。

## 継承

- `codebase-explorer` の網羅調査と `task-reviewer` の規律準拠確認を継承する。
