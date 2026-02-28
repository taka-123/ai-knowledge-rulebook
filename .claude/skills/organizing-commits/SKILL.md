---
name: organizing-commits
description: Use when the user explicitly asks to organize git changes under .claude/, .cursor/, .codex/, scripts/, or .work/ into reviewable commit units; When NOT to use: when there are no file changes or git planning is out of scope; Trigger Keywords: [organizing commits, commit, diff, PR, rollback].
---

# organizing-commits

## When to use

- `.claude/skills/*/SKILL.md` と agent 定義の複数差分を意図単位で整理したいとき。
- レビュー前に `git diff` を読みやすい粒度へ分割したいとき。
- ロールバックしやすいコミット構成を設計したいとき。

## When NOT to use

- 変更ファイルが存在せずコミット対象がないとき。
- Git 操作そのものが禁止されるタスク条件のとき。
- 履歴改変（rebase など）を要求されていないとき。

## Trigger Keywords

- organizing commits
- commit
- diff
- PR
- rollback

## Procedure

1. `git status --short` で作業ツリーの全差分を確認する。完了条件: 変更一覧を把握。
2. `git diff --name-only` と `git diff` で意図ごとに差分を分類する。完了条件: グループ分け完了。
3. 各グループのコミットメッセージ候補を作成する。完了条件: 1コミット1意図の草案完成。
4. ロールバック時の最小単位を明示し、順序を提案する。完了条件: 逆順適用手順が説明可能。
5. レビュー向けに差分サマリを出力する。完了条件: 変更目的と範囲が明確。

## Output Contract

| 項目          | 形式                                                |
| ------------- | --------------------------------------------------- |
| Change Groups | `1. skill-update: .claude/skills/lint-fix/SKILL.md` |
| Commit Plan   | `feat/docs/chore` などの候補                        |
| Rollback Unit | コミット単位の戻し方                                |
| Review Notes  | リスクと確認ポイント                                |

### NG例

❌ 意図が異なる変更を 1 コミットに混在させる（レビュー困難）。

❌ ロールバック手順を示さない（運用リスク）。

❌ 差分確認なしでコミット案を提示する（根拠不足）。

## Examples

### Example 1

Input: `.claude/skills/lint-fix/SKILL.md` と `.claude/skills/schema-guard/SKILL.md` を同時更新した。
Output: skill品質修正コミットとして 1 グループ化した計画表。

### Example 2

Input: `.claude/agents/content-writer.md` と `.cursor/agents/content-writer.md` を同期更新した。
Output: プラットフォーム整合コミット案とレビュー観点。

### Example 3

Input: `.codex/agents/code-reviewer.toml` のみ更新した。
Output: Codex設定更新専用コミット案とロールバック単位。
