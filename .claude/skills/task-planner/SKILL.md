---
name: task-planner
description: Use when implementation requires an explicit step plan with file targets, validation commands, and completion criteria; When NOT to use: tiny edits that can be completed safely without planning; Trigger Keywords: 計画, 分解, roadmap, milestone, 実装手順.
---

# task-planner

## When to use

- 変更が複数ファイルにまたがる。
- 実装前に影響範囲の分解が必要。

## When NOT to use

- 1ファイル内の軽微な文言修正。
- 既存手順が明確で追加分解が不要。

## Trigger Keywords

- 計画
- 分解
- roadmap
- milestone
- 実装手順

## Examples

### Example 1

Input: schema チェック失敗を直す前に実装計画を作って。
Output: `schemas/` と `notes/` の対象を分離し、`npm run schema:check` を終点にした4ステップ計画を提示する。

### Example 2

Input: ルール衝突を最小差分で解消する順序を決めたい。
Output: `AGENTS.md` → `CLAUDE.md` → `.cursor/rules` の順で修正し、各ステップの完了条件を提示する。

### Example 3

Input: ドキュメント更新と lint 修正を同時に進める手順を設計して。
Output: 並列可能タスクと逐次タスクを分離し、`npm run format:check` で統合検証する計画を提示する。

---

## 1. Workflow

1. **Intake**: ユーザー指示からゴール・制約・依存関係を抽出する。不明点があれば即質問する。
2. **Scope Analysis**: 対象ファイルを Glob/Grep で特定し、変更が及ぶ範囲（直接変更 / 参照元 / CI 影響）を列挙する。
3. **Step Decomposition**: 変更を論理単位に分解し、各ステップに「対象ファイル」「実行コマンド」「完了条件」を付与する。並列可能なステップと逐次ステップを明示する。
4. **Risk Annotation**: 各ステップにリスク（参照切れ、スキーマ不整合、CI 失敗）を付記し、ロールバック手段を提示する。
5. **Plan Output**: Output Format に従い、計画を構造化して出力する。承認後に実装フェーズへ移行する。

## 2. Checklist

### Pre-flight

- [ ] ゴールが 1 文で明文化されている
- [ ] 対象ファイル一覧が Glob で確認済み
- [ ] 依存関係（参照元・CI ワークフロー）を把握済み

### Post-flight

- [ ] 全ステップに対象ファイル・コマンド・完了条件が記載されている
- [ ] 並列 / 逐次の区分が明示されている
- [ ] リスクとロールバック手段が各ステップに付記されている
- [ ] `npm run format:check` を最終検証として含んでいる

## 3. Output Format

```markdown
## task-planner Plan

**Goal**: <1 文のゴール>
**Scope**: <対象ディレクトリ / ファイル数>
**Steps**: <N> (parallel: <M>, sequential: <K>)

### Step Table

| #   | Action | Target Files | Command | Done Criteria | Risk | Rollback          |
| --- | ------ | ------------ | ------- | ------------- | ---- | ----------------- |
| 1   | ...    | ...          | ...     | ...           | ...  | `git restore ...` |

### Dependency Graph

- Step 2 depends on Step 1 (output file used as input)
- Steps 3-4 can run in parallel

### Final Validation

- `npm run format:check` → exit 0
- `npm run schema:check` → exit 0 (if JSON changed)
```

## 4. Memory Strategy

- **Persist**: 直前の計画テンプレート（ステップ構成パターン、頻出コマンド）をキャッシュし、類似タスクの計画生成を高速化する。
- **Invalidate**: プロジェクトの検証コマンド（`package.json` scripts）が変更された場合にキャッシュを無効化する。
- **Share**: 生成した計画を `lint-fix`・`format-lint-audit` に提供し、検証ステップの自動実行に活用する。
