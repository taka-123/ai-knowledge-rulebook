# Router Rule

Route by trigger keywords. If multiple match, prefer Tier 1 > Tier 2 > Tier 3.

## Tier 1 — Agents (delegate to AGENTS.md)

- `最新仕様` `API変更` `release` `changelog` `version` `依存更新` -> `tech-researcher`
- `調査` `影響範囲` `参照` `構造` `dependency map` -> `codebase-explorer`
- `review` `PR` `回帰` `品質` `レビュー` -> `task-reviewer`

## Tier 2 — Global Skills

- `lint` `format` `schema` `CI` `test` -> `lint-fix`
- `debug` `error` `再現` `stacktrace` `CI failure` -> `debug-strategist`
- `計画` `分解` `milestone` `roadmap` `実装手順` -> `task-planner`
- `UI` `CSS` `layout` `component` `accessibility` -> `ui-standardizer`
- `commit` `branch` `release` `changelog` -> `git-helper`
- `agent` `skill` `rule` `workflow` `template` -> `agent-factory`

## Tier 3 — Project Skills

- `ドキュメント作成` `notes` `clips` `ai profile` -> `documentation-standards`
- `技術情報` `仕様確認` `出典` `citation` -> `research-protocol`
- `新規ファイル` `テンプレート` `scaffold` `ノート作成` -> `content-scaffold`
- `json validation` `スキーマ検証` `ai profile json` -> `schema-guard`
- `format check` `lint error` `CI通過確認` `整形` -> `format-lint-audit`
- `README` `directory` `structure` `ドキュメント同期` -> `docs-sync`
- `要約` `圧縮` `map` `context` `サマリー` -> `context-compress-map`

## High-Risk Guard

<SCRUTINY_REQUIRED> `deploy` `migrate` `terraform apply` `git push --force` — 承認必須。
