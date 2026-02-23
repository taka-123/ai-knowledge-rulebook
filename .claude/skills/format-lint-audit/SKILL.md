---
name: format-lint-audit
description: Use when final quality gates must confirm format and lint checks with explicit pass or fail evidence; When NOT to use: when implementation is still exploratory and files are not ready for final verification; Trigger Keywords: [quality gate, format:check, lint, CI, 検証].
---

# format-lint-audit

## When to use

- 変更完了後、コミット・PR 前の最終品質ゲートを通したい場合。
- CI が落ちた原因を特定して再現・修正したい場合。

## When NOT to use

- 作業途中で設計がまだ変わる段階の場合。
- 実行環境が未整備で検証コマンドを走らせられない場合。

## Trigger Keywords

- quality gate
- format:check
- lint
- CI
- 検証

## このリポジトリの検証コマンド

| コマンド | 検証内容 |
|---|---|
| `npm run format:check` | Markdown / YAML / JSON の整形チェック |
| `npm run schema:check` | `ai/` `notes/` JSON のスキーマ検証 |
| `npm run agent:check` | スキル構造・ルーティング整合性 |
| `npm run lint:md` | Markdown Lint のみ個別実行 |
| `npm run lint:yaml` | YAML Lint のみ個別実行 |

## Procedure

1. 今回変更したファイル一覧を `git diff --staged --name-only` で確定する。
2. `npm run format:check` を実行して終了コードを記録する。
3. JSON ファイルの変更がある場合は `npm run schema:check` を追加実行する。
4. SKILL.md の変更がある場合は `npm run agent:check` を実行する。
5. 個別 lint が必要な場合（エラーの特定）は `npm run lint:md` / `npm run lint:yaml` を個別実行する。
6. 全コマンドの結果を表形式で報告する。

## Output Contract

結果は必ず以下の表形式で出す：

| コマンド | exit code | 結果 | 補足 |
|---|---|---|---|
| npm run format:check | 0 | PASS | - |
| npm run schema:check | 1 | FAIL | notes/2025.json L12: required field missing |

- FAIL が 1 件でもあれば完了扱いにしない。
- 監査対象外の既知警告（tmp/ 配下等）は「対象外」と明記して FAIL と混在させない。

### NG例

```
❌ コマンドを実行せず「問題ないはずです」と報告する
❌ tmp/ の既知警告を FAIL として報告する（対象外と明記する）
❌ format:check が FAIL のまま「後で直す」として完了扱いにする
❌ 変更していないファイルの lint 結果を検証対象に混ぜる
```

## Examples

### Example 1

Input: スキルファイルを複数編集したので PR 前に品質確認したい。
Output: `format:check` と `agent:check` を実行し、全 PASS の表を報告する。

### Example 2

Input: CI で `format:check` が落ちたので原因を特定したい。
Output: ローカルで `npm run format:check` を実行してエラー行を特定し、修正後に再実行で exit 0 を確認する。

### Example 3

Input: JSON ファイルを追加したので schema:check を確認したい。
Output: `npm run schema:check` を実行し、PASS または失敗フィールドを表で報告する。
