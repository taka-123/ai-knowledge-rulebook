---
name: cross-platform-agent-sync
description: Use proactively when editing any file under .claude/agents/, .cursor/agents/, or .codex/agents/ to keep name, description, and role semantics aligned across platforms; When NOT to use: when the change is intentionally platform-specific and documented as an exception; Trigger Keywords: [agent sync, description sync, cross platform, rename chain, parity].
---

# cross-platform-agent-sync

## When to use

- `.claude/agents/*.md` を更新し、`.cursor/agents` と `.codex/agents` へ反映が必要なとき。
- agent 名の改名や廃止で rename 連鎖整合を担保したいとき。
- description の意味差分を機械的に検出して同期したいとき。

## When NOT to use

- 変更が `.claude/skills/*/SKILL.md` のみに限定されるとき。
- 特定プラットフォーム専用 agent を意図的に分岐させるとき。
- 対象 agent 実体が欠落していて同期元が確定できないとき。

## Trigger Keywords

- agent sync
- description sync
- cross platform
- rename chain
- parity

## Procedure

1. `find .claude/agents .cursor/agents .codex/agents -maxdepth 1 -type f | sort` で対象 agent 一覧を確認する。
2. `node .claude/skills/cross-platform-agent-sync/scripts/sync-agent-description.mjs` を実行し、不一致を抽出する。
3. 修正が必要な場合は `node .claude/skills/cross-platform-agent-sync/scripts/sync-agent-description.mjs --apply` で同期する。
4. `.claude/skills/cross-platform-agent-sync/docs/platform-field-map.md` を参照し、frontmatter 仕様差を確認する。
5. `rg -n "^description" .claude/agents .cursor/agents .codex/agents` で最終一致を再確認する。

## Output Contract

| 項目            | 形式                                        |
| --------------- | ------------------------------------------- |
| Status          | `PASS / FAIL / BLOCKED`                     |
| Compared Agents | `- name`                                    |
| Mismatches      | `name: claude/cursor/codex` の差分一覧      |
| Applied Updates | `- path`                                    |
| Verification    | `node ...sync-agent-description.mjs` の結果 |

### NG例

❌ `.claude` だけ更新して `.cursor` と `.codex` を放置する（連鎖更新違反）。

❌ 改名後の旧ファイル参照を残したまま完了報告する（旧名残存）。

❌ 仕様差（Cursor unsupported fields）を無視して同一frontmatterを流用する（仕様違反）。

## Examples

### Example 1

Input: `.claude/agents/code-reviewer.md` の description を更新した。
Output: 3プラットフォームの description 一致レポート。

### Example 2

Input: 旧 reviewer を廃止し `code-reviewer` へ移行した。
Output: rename 連鎖更新結果と旧名残存チェック。

### Example 3

Input: `.codex/agents/security-reviewer.toml` の説明だけ古い疑いがある。
Output: mismatch 検出結果と `--apply` 適用ログ。
