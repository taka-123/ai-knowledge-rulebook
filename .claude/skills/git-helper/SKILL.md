---
name: git-helper
description: Use when changes must be grouped into reviewable commits with safe rollback guidance and minimal diff noise; When NOT to use: unrelated design tasks without repository changes; Trigger Keywords: commit, branch, diff, PR, rollback.
---

# git-helper

## When to use

- 変更差分を論理単位で整理したい。
- レビューしやすいコミット分割が必要。

## When NOT to use

- コード未変更の相談。
- Git 操作が範囲外の依頼。

## Trigger Keywords

- commit
- branch
- diff
- PR
- rollback

## Examples

### Example 1

Input: この変更をレビューしやすい2コミットに分ける案を出して。
Output: 司令塔配線変更と skill 本体変更を分離したコミット計画を提示する。

### Example 2

Input: 失敗した修正を安全に戻す手順を教えて。
Output: `git restore` と `git revert` の使い分けを現在の状態に合わせて提示する。

### Example 3

Input: PR 説明文を差分中心で作りたい。
Output: 目的、主要変更、検証結果、リスクを短く整理した PR テンプレを出力する。

---

## 1. Workflow

1. **Intake**: Git 操作の目的（コミット分割 / ロールバック / PR 作成 / ブランチ整理）を確認する。
2. **State Analysis**: `git status`、`git diff`、`git log` で現在の状態を把握する。未ステージの変更、ステージ済みの変更、直近のコミット履歴を確認する。
3. **Strategy Design**: 目的に応じた操作計画を策定する。
   - コミット分割: 変更を論理単位でグループ化し、各コミットメッセージを提案する。
   - ロールバック: `git restore` / `git revert` の適切な選択を提案する。
   - PR 作成: 差分要約、検証結果、リスクを含む PR テンプレートを生成する。
4. **Execute**: 承認後、Git コマンドを Bash で実行する。破壊的操作（`--force`、`reset --hard`）は事前に明示的承認を取得する。
5. **Verify**: 操作後の状態を `git status` / `git log` で確認し、期待通りであることを報告する。

## 2. Checklist

### Pre-flight

- [ ] Git 操作の目的が明確である
- [ ] 現在のブランチと状態（clean / dirty）を把握済み
- [ ] 破壊的操作が含まれる場合は承認を取得済み

### Post-flight

- [ ] 操作後の Git 状態が期待通りである
- [ ] コミットメッセージが変更内容を正確に反映している
- [ ] 不要な差分ノイズ（空白変更等）が含まれていない
- [ ] PR テンプレート（該当時）に目的・変更・検証・リスクが記載されている

## 3. Output Format

```markdown
## git-helper Report

**Action**: COMMIT_SPLIT | ROLLBACK | PR_CREATE | BRANCH_CLEANUP
**Branch**: <current branch>
**State**: clean | dirty

### Operation Plan

| #   | Step               | Command                                        | Purpose              |
| --- | ------------------ | ---------------------------------------------- | -------------------- |
| 1   | Stage router files | `git add .cursor/rules/ .windsurf/rules/`      | Group router changes |
| 2   | Commit routers     | `git commit -m "fix: align router references"` | Logical unit 1       |

### PR Template (if applicable)

**Title**: <short title>
**Body**:

- Purpose: <1 line>
- Changes: <bullet list>
- Validation: `npm run format:check` → PASS
- Risk: <assessment>

### Post-Operation State

- Branch: <branch name>
- Last commit: <hash> <message>
- Working tree: clean
```

## 4. Memory Strategy

- **Persist**: プロジェクトのコミットメッセージ規約（prefix: fix/feat/docs/chore）と PR テンプレート構造をキャッシュし、次回の提案を高速化する。
- **Invalidate**: `.github/PULL_REQUEST_TEMPLATE.md` やコミット規約が変更された場合にキャッシュを無効化する。
- **Share**: PR テンプレートを `task-reviewer` Agent に提供し、レビュー時の品質基準とする。コミット計画を `task-planner` に提供し、実装計画との整合性を確認する。
