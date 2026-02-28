---
name: description-condition-enforcer
description: Use proactively when editing any file under .claude/skills/*/SKILL.md to enforce concrete path-based description conditions and proactive or explicit trigger patterns; When NOT to use: when skill frontmatter is unchanged and no description quality check is required; Trigger Keywords: [description condition, proactive rule, explicit ask, trigger keywords, skill quality].
---

# description-condition-enforcer

## When to use

- `SKILL.md` の description を更新し、抽象条件の混入を防ぎたいとき。
- `Use proactively when ...` と `Use when the user explicitly asks ...` の使い分けを検査したいとき。
- 3要素形式は満たすが path 具体性が不足している疑いがあるとき。

## When NOT to use

- skill frontmatter を一切変更していないとき。
- syntax チェックのみで description 品質判定が不要なとき。
- `.claude/skills` 外のドキュメントに対する文体修正のみを行うとき。

## Trigger Keywords

- description condition
- proactive rule
- explicit ask
- trigger keywords
- skill quality

## Procedure

1. `find .claude/skills -mindepth 2 -maxdepth 2 -name SKILL.md | sort` で対象 SKILL を取得する。
2. `node .claude/skills/description-condition-enforcer/scripts/enforce-description-condition.mjs` を実行する。
3. 失敗時は `.claude/skills/description-condition-enforcer/docs/condition-patterns.md` を読み、該当 description を修正する。
4. `node scripts/validate-skills.mjs` を再実行して 3要素形式と examples を検証する。
5. 抽象 condition が残る場合は BLOCKED として停止する。

## Output Contract

| 項目 | 形式 |
| --- | --- |
| Status | `PASS / FAIL / BLOCKED` |
| Checked Skills | `- .claude/skills/<name>/SKILL.md` |
| Violations | `name: reason` |
| Fixed Descriptions | `name: before -> after` |
| Verification | `node scripts/validate-skills.mjs` |

### NG例

❌ path を含まない抽象 description を許容する（発火精度低下）。

❌ proactive が必要なスキルを explicit で書く（自動起動不能）。

❌ Trigger Keywords のみを条件として扱う（description-first 破壊）。

## Examples

### Example 1

Input: `.claude/skills/lint-fix/SKILL.md` の description に path が含まれていない。
Output: 修正後 description と再検証 PASS。

### Example 2

Input: 明示依頼スキルが `Use proactively` で始まっている。
Output: `Use when the user explicitly asks ...` へ修正した差分。

### Example 3

Input: 複数 SKILL を一括更新したので condition 品質を確認したい。
Output: violation 一覧表と fix 済み一覧。
