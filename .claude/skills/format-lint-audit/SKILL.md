---
name: format-lint-audit
description: Use when final quality gates must run repository formatting and lint checks with explicit pass or fail reporting; When NOT to use: exploratory drafting before files are finalized; Trigger Keywords: quality gate, format:check, lint, CI, 検証.
---

# format-lint-audit

## When to use

- 変更後の最終検証を実施する。
- CI 相当の品質ゲートを確認する。

## When NOT to use

- 実装前の草案段階。
- 編集中で結果が安定しない段階。

## Trigger Keywords

- quality gate
- format:check
- lint
- CI
- 検証

## Examples

### Example 1

Input: 変更後に品質ゲートを一括で確認したい。
Output: `npm run format:check` と `npm run schema:check` を実行し、結果を要約する。

### Example 2

Input: markdownlint だけ再検証して。
Output: 対象ファイルに `npx markdownlint-cli2` を実行し、合否を明示する。

### Example 3

Input: CI 前のチェックリストを作って。
Output: 実行コマンド、期待結果、失敗時の修正先を1表にまとめる。

---

## 1. Workflow

1. **Intake**: 検証対象（全体 / 特定ファイル / 特定形式）を確認する。
2. **Run Gates**: 以下のコマンドを順次実行し、各結果を記録する。
   - `npm run format:check`（Prettier + Markdownlint + yamllint）
   - `npm run lint:md`（Markdown 個別）
   - `npm run lint:yaml`（YAML 個別）
   - `npm run lint:json`（JSON 個別）
   - `npm run schema:check`（JSON Schema 適合、JSON 変更時）
3. **Parse Results**: 各コマンドの exit code とエラー行を抽出し、PASS / FAIL / WARN に分類する。
4. **Report**: Output Format に従い、結果を構造化して出力する。FAIL 項目には修正候補コマンドを付記する。

## 2. Checklist

### Pre-flight

- [ ] 検証対象のファイル形式（md / yaml / json）を把握済み
- [ ] `node_modules` がインストール済み（`npm install`）
- [ ] Python 依存（yamllint, check-jsonschema）がインストール済み

### Post-flight

- [ ] 全コマンドの exit code が記録されている
- [ ] FAIL 項目に修正候補コマンドが付記されている
- [ ] 最終判定（ALL PASS / HAS FAILURES）が 1 行で明示されている

## 3. Output Format

```markdown
## format-lint-audit Report

**Verdict**: ALL PASS | HAS FAILURES
**Scope**: <対象ファイル数 / ディレクトリ>
**Checked**: <timestamp>

### Gate Results

| #   | Gate         | Command                | Exit Code | Status | Errors       |
| --- | ------------ | ---------------------- | --------- | ------ | ------------ |
| 1   | Prettier     | `npm run format:check` | 0         | PASS   | -            |
| 2   | Markdownlint | `npm run lint:md`      | 1         | FAIL   | 3 violations |

### Failure Details

| #   | File             | Line | Rule  | Message                | Fix Command      |
| --- | ---------------- | ---- | ----- | ---------------------- | ---------------- |
| 1   | notes/2025-01.md | 12   | MD032 | Blank line around list | `npm run fix:md` |

### Summary

- PASS: <N> | FAIL: <N> | Total Gates: <N>
```

## 4. Memory Strategy

- **Persist**: 各ゲートの実行結果履歴をキャッシュし、前回との差分レポートを可能にする。
- **Invalidate**: `package.json` の scripts、`.markdownlint.jsonc`、`.prettierrc.json`、`.config/.yamllint.yml` が変更された場合にキャッシュを無効化する。
- **Share**: FAIL 結果を `lint-fix` Skill に提供し、自動修正の入力とする。PASS 結果を `task-reviewer` Agent に提供し、品質監査の根拠とする。
