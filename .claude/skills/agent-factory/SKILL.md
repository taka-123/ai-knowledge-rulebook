---
name: agent-factory
description: Use when new agents or skills must be designed with non-overlapping responsibilities, clear triggers, and validation gates; When NOT to use: single-file bug fixes without routing impact; Trigger Keywords: agent, skill, router, workflow, trigger.
---

# agent-factory

## When to use

- 新規エージェントやスキルを設計する。
- 役割重複を避けたルーティング体系を作る。

## When NOT to use

- 単発の軽微修正。
- 既存配線を変えない依頼。

## Trigger Keywords

- agent
- skill
- router
- workflow
- trigger

## Examples

### Example 1

Input: ドキュメント監査専用エージェントを追加したい。
Output: 目的、入力、禁止事項、完了条件を定義したエージェント仕様を作る。

### Example 2

Input: 既存 skill の重複を解消して。
Output: 重複領域を表で可視化し、統合先と削除候補を最小差分で提案する。

### Example 3

Input: ルーターの発火精度を上げる trigger 設計をして。
Output: キーワード群を衝突回避しつつ、優先順位付きで再定義する。

---

## 1. Workflow

1. **Intake**: 設計対象（新規 Agent / 新規 Skill / 既存の重複解消 / ルーター最適化）と目的を確認する。
2. **Existing Inventory**: `.claude/agents/` と `.claude/skills/` の全エントリを Glob で列挙し、名前・カテゴリ・Trigger Keywords を一覧化する。
3. **Overlap Detection**: 既存エントリとの責務重複・Trigger Keywords 衝突を検出する。重複がある場合は統合案を提示する。
4. **Design**: 2026 Constitution に準拠した仕様を設計する。
   - Agent: Description（"Use proactively when..."）、Tools（allowed/disallowed）、4-Section Body
   - Skill: frontmatter（name, description）、When to use / NOT to use、Trigger Keywords、Examples、4-Section Body
   - Category Logic: Reviewer（Read-only）/ Fixer（full access）/ Explorer（Read-only）/ Researcher（Read + Web）
5. **Router Registration**: 設計した Agent/Skill を CLAUDE.md、`.cursor/rules/10-skill-map.mdc`、`.windsurf/rules/10-skill-map.md` に登録する計画を提示する。
6. **Validate**: `npm run agent:check` で制約検証（Name/Description/Examples）を実行する。

## 2. Checklist

### Pre-flight

- [ ] 設計対象の目的が明確である
- [ ] 既存 Agent/Skill の一覧を取得済み
- [ ] Category Logic（Reviewer/Fixer/Explorer/Researcher）を把握済み

### Post-flight

- [ ] 責務重複が解消されている（または報告されている）
- [ ] Trigger Keywords が既存エントリと衝突していない
- [ ] Description が "Use proactively when..." で始まっている（Agent の場合）
- [ ] 4-Section Body（Workflow/Checklist/Output Format/Memory Strategy）が完備している
- [ ] ルーター登録計画が全ツール（Claude/Cursor/Windsurf）を網羅している
- [ ] `npm run agent:check` が PASS

## 3. Output Format

```markdown
## agent-factory Report

**Action**: CREATE_AGENT | CREATE_SKILL | RESOLVE_OVERLAP | OPTIMIZE_ROUTER
**Target**: <name>
**Category**: Reviewer | Fixer | Explorer | Researcher

### Design Specification

- **Name**: <lowercase-hyphen, max 64 chars>
- **Description**: <max 1024 chars, starts with "Use proactively when..." for Agent>
- **Category**: <type>
- **Tools**: allowed: [...], disallowed: [...]
- **Trigger Keywords**: <list>

### Overlap Analysis

| Existing Entry | Overlap Area    | Resolution                                                      |
| -------------- | --------------- | --------------------------------------------------------------- |
| lint-fix       | format commands | Separate by: lint-fix = auto-fix, format-lint-audit = reporting |

### Router Registration Plan

| Router   | File                            | Action                 |
| -------- | ------------------------------- | ---------------------- |
| Claude   | CLAUDE.md                       | Add to Hierarchy table |
| Cursor   | .cursor/rules/10-skill-map.mdc  | Add trigger entry      |
| Windsurf | .windsurf/rules/10-skill-map.md | Add trigger entry      |

### Validation

| Check       | Command               | Result |
| ----------- | --------------------- | ------ |
| Constraints | `npm run agent:check` | PASS   |
```

## 4. Memory Strategy

- **Persist**: 現在の Agent/Skill 一覧、Category 分類、Trigger Keywords マップをキャッシュし、重複検出を高速化する。
- **Invalidate**: `.claude/agents/` または `.claude/skills/` 配下のファイルが追加・削除・変更された場合にキャッシュを無効化する。
- **Share**: 設計仕様を `repo-cartographer` Agent に提供し、発火率マトリクスの更新に活用する。ルーター登録計画を `content-writer` Agent に提供し、ルーターファイルの更新に活用する。
