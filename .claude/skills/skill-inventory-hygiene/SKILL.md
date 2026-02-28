---
name: skill-inventory-hygiene
description: Use proactively when editing any file under .claude/skills/ to remove empty skill directories, stale artifacts, and inventory drift before validation; When NOT to use: when the task does not modify skill inventory or canonical skill structure; Trigger Keywords: [skill inventory, hygiene, empty dirs, cleanup, canonical skills].
---

# skill-inventory-hygiene

## When to use

- `.claude/skills` 配下で新規追加・削除を行った後に実体一覧を正規化したいとき。
- 空ディレクトリや `.DS_Store` が混入して検証ノイズになっているとき。
- Canonical Source を `SKILL.md` 実体だけに保ちたいとき。

## When NOT to use

- skill 構成を変更していないとき。
- 読み取り専用の監査のみでファイル削除を行わないとき。
- `.claude/skills` 以外の領域を掃除したいとき。

## Trigger Keywords

- skill inventory
- hygiene
- empty dirs
- cleanup
- canonical skills

## Procedure

1. `find .claude/skills -mindepth 1 -maxdepth 1 -type d | sort` で skill ディレクトリ一覧を取得する。
2. `bash .claude/skills/skill-inventory-hygiene/scripts/prune-empty-skill-dirs.sh` を実行する。
3. `find .claude/skills -mindepth 2 -maxdepth 2 -name SKILL.md | sort` で実体一覧を再取得する。
4. `node scripts/validate-skills.mjs` を実行し、検証エラーがないことを確認する。
5. 実体なしディレクトリが残る場合は BLOCKED として停止する。

## Output Contract

| 項目                 | 形式                               |
| -------------------- | ---------------------------------- |
| Status               | `PASS / FAIL / BLOCKED`            |
| Removed Artifacts    | `- path`                           |
| Remaining Skill Dirs | `- .claude/skills/<name>`          |
| Verification         | `node scripts/validate-skills.mjs` |

### NG例

❌ `SKILL.md` があるディレクトリを誤削除する（実体喪失）。

❌ `.claude/skills` 以外を掃除してしまう（対象逸脱）。

❌ cleanup 後に inventory を再確認しない（状態不明）。

## Examples

### Example 1

Input: `.claude/skills/agent-factory/` が空ディレクトリとして残っている。
Output: 削除済みパス一覧と再スキャン結果。

### Example 2

Input: `.claude/skills/.DS_Store` が残っている。
Output: 削除ログと validator 実行結果。

### Example 3

Input: skill 大量更新後に実体一覧を確定したい。
Output: `SKILL.md` 実体一覧の確定表。
