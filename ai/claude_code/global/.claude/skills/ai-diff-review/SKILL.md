---
name: ai-diff-review
description: "Use when the user explicitly asks to review code changes via git diff; When NOT to use: when reviewing documentation quality rather than code logic (use prepare-review instead); Trigger Keywords: [ai-diff-review, コードレビュー, diff review, レビューして, review diff, 差分レビュー]."
---

# ai-diff-review

Git diff を対象に、4つの観点でコードレビューを行う。

## When to use

- コード変更のリスクをレビューしたいとき。

## When NOT to use

- ドキュメント品質のレビュー → `prepare-review`
- Lint・フォーマット修正のみ → `lint-fix`

## Trigger Keywords

- ai-diff-review, コードレビュー, diff review, レビューして, review diff, 差分レビュー

## Diff Mode Selection

| ユーザー指示           | コマンド                                      |
| ---------------------- | --------------------------------------------- |
| 指示なし (デフォルト)  | `git diff $(git merge-base origin/HEAD HEAD)` |
| コミット済みのみ       | `git diff origin/HEAD...HEAD`                 |
| 未ステージ分のみ       | `git diff`                                    |
| ステージ済みのみ       | `git diff --cached`                           |
| 直近コミットのみ       | `git diff HEAD~1 HEAD`                        |
| 任意範囲 (SHA, branch) | ユーザー指定をそのまま使用                    |

### 未追跡ファイルの扱い

`git diff` は追跡済みファイルの変更しか検出しない。
デフォルト・未ステージ・ステージ済みモードでは `git ls-files --others --exclude-standard` を併用し、未追跡ファイルもレビュー対象に含める。
直近コミット・コミット済みのみ・任意範囲など確定済みスコープでは、未追跡ファイルは対象外とする。

### 補足

- `origin/HEAD` 未設定時は `git remote set-head origin --auto` で設定する。

## Procedure

1. ユーザー指示から diff モードを決定する。
2. 対応する `git diff` と未追跡ファイル検出（「未追跡ファイルの扱い」参照）を実行する。`origin/HEAD` 未設定エラー時は `git remote set-head origin --auto` 後にリトライ。
3. 差分も未追跡ファイルもなければ「変更なし」と報告して終了。
4. 4 criteria で分析し、重大な問題を最大5件抽出する:
   - **Correctness**: エッジケース、境界値、例外ハンドリング
   - **Security**: OWASP 準拠（インジェクション、認可漏れ、機密データ）
   - **Performance**: ボトルネック、リソースリーク、非効率なクエリ/ループ
   - **Maintainability**: 高結合、DRY 違反、テスト容易性
5. 出力フォーマットに従い結果を報告する。

## Output Contract

```markdown
## レビューサマリー

- **Diff モード**: [使用した diff コマンド]
- **リスクレベル**: ✅ None / 🟢 Low / 🟡 Medium / 🟠 High / 🔴 Critical（指摘なしなら None）
- **概要**: [3行以内]

## 指摘事項

（最大5件。なければ「🎉 重大な指摘事項なし」のみ）

### ⚠️ [タイトル]

- **カテゴリ**: Correctness / Security / Performance / Maintainability
- **深刻度**: 🔴 High / 🟡 Medium / 🟢 Low
- **該当箇所**: diff からコード引用
- **説明**: リスクのメカニズム
- **推奨対応**: 修正方針
- **確信度**: High / Medium / Low（Low の場合は理由を併記）
```

### 出力制約

- Linter 検知可能な軽微指摘（インデント・命名規約等）は除外
- 指摘事項は最大5件

## Examples

### デフォルト実行

Input: `/ai-diff-review`
→ `git diff $(git merge-base origin/HEAD HEAD)` でフォーク点から現在の作業状態までの全差分をレビュー。

### スコープ指定

Input: `ステージ済みの変更をレビューして`
→ `git diff --cached` でステージ済み差分のみをレビュー。

### 任意範囲

Input: `main...feature/foo の差分をレビューして`
→ `git diff main...feature/foo` をそのまま使用。

### 仕様付きレビュー

Input: `/ai-diff-review`＋仕様テキスト
→ Correctness の判定に仕様を参照（仕様はオプション）。
