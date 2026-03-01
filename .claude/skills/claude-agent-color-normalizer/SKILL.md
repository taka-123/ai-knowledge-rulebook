---
name: claude-agent-color-normalizer
description: Use proactively when editing any file under .claude/agents/ to normalize color values to the allowed set Red, Blue, Green, Yellow, Purple, Orange, Pink, or Cyan; When NOT to use: when the task does not touch Claude agent frontmatter; Trigger Keywords: [color normalize, claude agent color, allowed colors, frontmatter, policy].
---

# claude-agent-color-normalizer

## When to use

- `.claude/agents/*.md` の `color` が小文字や非許可値で保存されているとき。
- 新規 agent 追加後に color policy 適合を確認したいとき。
- `magenta` など許可外値を一括正規化したいとき。

## When NOT to use

- `.claude/agents` を変更していないとき。
- Cursor/Codex の frontmatter だけを調整するとき。
- color 以外の仕様違反を主題にするとき。

## Trigger Keywords

- color normalize
- claude agent color
- allowed colors
- frontmatter
- policy

## Procedure

1. `rg -n "^color:" .claude/agents/*.md` で現在の color 値を確認する。
2. `node .claude/skills/claude-agent-color-normalizer/scripts/normalize-claude-agent-colors.mjs` を実行する。
3. `node scripts/validate-claude-agents.mjs` で許可値判定を再検証する。
4. 変換結果を `Agent -> before -> after` 形式でまとめる。
5. 許可外値が残る場合は BLOCKED として停止する。

## Output Contract

| 項目              | 形式                                      |
| ----------------- | ----------------------------------------- |
| Status            | `PASS / FAIL / BLOCKED`                   |
| Changed Agents    | `name: before -> after`                   |
| Unresolved Colors | `None` または一覧                         |
| Verification      | `node scripts/validate-claude-agents.mjs` |

### NG例

❌ 許可色以外を新たに導入する（policy 違反）。

❌ color 行の位置を description より上に移動する（規約順序違反）。

❌ normalize 実行後に validator を回さない（検証不足）。

## Examples

### Example 1

Input: `.claude/agents/repo-scaffolder.md` が `color: magenta` になっている。
Output: `Purple` へ変換した結果と検証 PASS。

### Example 2

Input: `.claude/agents/` 配下の全 agent（`code-reviewer.md`, `security-reviewer.md`, `verifier.md` 等）の color を一括監査したい。
Output: `code-reviewer: Green (ok)`, `security-reviewer: Red (ok)`, `verifier: Blue (ok)` 等の変換一覧表（変更なし含む）。

### Example 3

Input: `.claude/agents/new-agent.md` を新規追加した後に color policy を確認したい。
Output: `new-agent: Orange (ok)` の適合確認結果と、全 agent の color 一覧表。
