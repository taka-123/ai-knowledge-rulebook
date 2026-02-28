---
name: cursor-agent-schema-guard
description: Use proactively when editing any file under .cursor/agents/ to enforce Cursor frontmatter constraints and remove unsupported fields; When NOT to use: when no Cursor agent file is modified in the current task; Trigger Keywords: [cursor schema, frontmatter guard, readonly, unsupported fields, cursor agents].
---

# cursor-agent-schema-guard

## When to use

- `.cursor/agents/*.md` を新規作成または更新したとき。
- `color/tools/disallowedTools/memory` の混入を検知・除去したいとき。
- reviewer 型 agent の `readonly: true` を検証したいとき。

## When NOT to use

- Cursor agent を一切変更していないとき。
- Claude/Codex のみを対象にした更新のとき。
- frontmatter を持たない補助 markdown の検査だけが目的のとき。

## Trigger Keywords

- cursor schema
- frontmatter guard
- readonly
- unsupported fields
- cursor agents

## Procedure

1. `find .cursor/agents -maxdepth 1 -name '*.md' -type f | sort` で対象ファイルを固定する。
2. `node .claude/skills/cursor-agent-schema-guard/scripts/validate-cursor-agent-frontmatter.mjs` を実行する。
3. 失敗したファイルの frontmatter を `name/description/model/readonly` のみへ修正する。
4. `node scripts/validate-cursor-agents.mjs` を実行して再検証する。
5. `rg -n "color:|tools:|disallowedTools:|memory:" .cursor/agents` で禁止フィールドが 0 件であることを確認する。

## Output Contract

| 項目          | 形式                                      |
| ------------- | ----------------------------------------- |
| Status        | `PASS / FAIL / BLOCKED`                   |
| Scanned Files | `- .cursor/agents/<name>.md`              |
| Violations    | `file: key` 一覧                          |
| Fixes         | `- file: removed key`                     |
| Verification  | `node scripts/validate-cursor-agents.mjs` |

### NG例

❌ `model: inherit` を削除してしまう（必須フィールド欠落）。

❌ reviewer 型で `readonly: true` を消す（権限分離が崩れる）。

❌ 禁止フィールド検査を省略して完了扱いにする（仕様違反が再発）。

## Examples

### Example 1

Input: `.cursor/agents/code-reviewer.md` を追加した。
Output: frontmatter 検証結果と違反ゼロ証明。

### Example 2

Input: 既存ファイルに `tools:` が残っている。
Output: 除去済みファイル一覧と再検証 PASS。

### Example 3

Input: reviewer agent の `readonly` 付与漏れを点検したい。
Output: 対象ファイルの `readonly` 判定表。
