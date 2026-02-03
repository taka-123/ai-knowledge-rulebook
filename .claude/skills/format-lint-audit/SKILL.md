---
name: format-lint-audit
description: プロジェクトのformat/lint検証を実行し結果を報告するスキル。キーワード「format」「lint」「整形」「検証」「prettier」「markdownlint」「yamllint」「lint error」で自動検出。
user-invocable: true
allowed-tools: Read, Bash
disable-model-invocation: true
---

# Format/Lint Audit

プロジェクトのフォーマット・Lint チェックを実行し、結果を整理して報告する。

## 実行手順

1. `./format.sh check` を実行する。
2. 変更したファイルの種類に応じて個別チェックを追加する：
   - Markdown: `npm run lint:md`
   - YAML: `npm run lint:yaml`
   - JSON: `npm run lint:json`
3. 結果を pass/fail で報告し、失敗時は次の手を提示する。

## 判定ルール

- 明示的な指示がない場合は自動修正を実行しない。
- 新しい依存関係を `npm install` で追加してはならない。
- コマンドが失敗した場合は、エラーを捕捉して最小限の修正を提示する。

## 出力形式

```markdown
## Format/Lint Audit 結果

- **コマンド**: [実行したコマンド]
- **結果**: pass / fail
- **問題**: [エラー・警告の詳細]
- **次の手**: [推奨アクション]
```

## 制約

- 実行したコマンドと結果を正確に報告する。
- 既存の警告で本タスク対象外のものは「対象外」と明記する。
