---
name: debug-strategist
description: Use when failures require hypothesis-driven debugging with reproducible steps, logs, and narrowed root cause candidates; When NOT to use: routine formatting tasks with obvious fixes; Trigger Keywords: debug, 不具合, 再現, stacktrace, root cause.
---

# debug-strategist

## When to use

- 原因不明の失敗を再現可能な形で切り分ける必要がある。
- ログと期待値の差分から根本原因を特定したい。

## When NOT to use

- フォーマットのみの単純修正。
- 再現手順が不要な既知エラー。

## Trigger Keywords

- debug
- 不具合
- 再現
- stacktrace
- root cause

## Examples

### Example 1

Input: `schema:check` が時々失敗する原因を調べて。
Output: 入力データを固定し、失敗条件を最小再現して、候補原因を優先度順で提示する。

### Example 2

Input: ルール適用が環境によって変わる不具合を切り分けたい。
Output: 読み込みパスと階層差分を収集し、再現条件を明示した上で修正案を示す。

### Example 3

Input: CI では落ちるがローカルでは通る理由を調査して。
Output: 実行コマンド、バージョン差、パス依存を比較し、検証ログ付きで根本原因候補を提示する。

---

## 1. Workflow

1. **Intake**: エラー現象（ログ、stacktrace、CI 出力）を収集し、再現条件を整理する。
2. **Hypothesis Generation**: 現象から候補原因を 3 つ以内に絞り、各仮説に検証手段を付与する。
3. **Reproduce**: 最も可能性の高い仮説から順に、最小再現手順を Bash で実行する。入力データを固定し、環境差分を排除する。
4. **Root Cause Isolation**: 再現結果をもとに原因を特定する。特定できない場合は仮説を更新して Step 3 に戻る。
5. **Report**: Output Format に従い、根本原因と修正案を構造化して出力する。

## 2. Checklist

### Pre-flight

- [ ] エラー現象（ログ / stacktrace / CI 出力）が提供されている
- [ ] 再現環境（ローカル / CI / 両方）が特定されている
- [ ] 期待動作が明文化されている

### Post-flight

- [ ] 根本原因が特定されている（または候補が優先度順で列挙されている）
- [ ] 再現手順が具体的コマンドで示されている
- [ ] 修正案が最小差分で提示されている
- [ ] 修正後の検証コマンドが明示されている

## 3. Output Format

```markdown
## debug-strategist Report

**Status**: ROOT_CAUSE_FOUND | INVESTIGATING
**Symptom**: <エラー現象の 1 行要約>
**Environment**: <local / CI / both>

### Hypotheses

| #   | Hypothesis       | Likelihood | Verification Command                            | Result    |
| --- | ---------------- | ---------- | ----------------------------------------------- | --------- |
| 1   | パス解決の環境差 | HIGH       | `node -e "console.log(require.resolve('...'))"` | Confirmed |

### Root Cause

- **Cause**: <根本原因の説明>
- **Evidence**: <再現ログ / 差分の要約>

### Fix Proposal

| #   | Action   | Target               | Command      |
| --- | -------- | -------------------- | ------------ |
| 1   | パス修正 | scripts/validate.mjs | Edit line 12 |

### Verification

- `npm run schema:check` → exit 0
```

## 4. Memory Strategy

- **Persist**: 過去のデバッグセッションで特定した原因パターン（環境差分、パス解決、バージョン不一致）をキャッシュし、類似障害の仮説生成を高速化する。
- **Invalidate**: プロジェクトの実行環境（Node.js バージョン、CI ワークフロー）が変更された場合にキャッシュを無効化する。
- **Share**: 特定した根本原因を `lint-fix` に提供し、修正の自動適用に活用する。再現手順を `task-planner` に提供し、修正計画の入力とする。
