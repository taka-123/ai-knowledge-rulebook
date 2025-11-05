---
description: Repository-wide format fix and documentation validation workflow prior to review or commit
---

# Format & Validate Documentation Workflow

標準化された整形とドキュメント品質検証を 1 コマンドで実施するためのワークフローです。Claude Code メインエージェントのコンテキストを保持しつつ、READ 系 Subagent（doc-validator）で検証を実行します。

## 前提条件

- リポジトリ直下で実行すること
- `./format.sh` が最新のプロジェクト整形ルールに同期済みであること
- `doc-validator` Subagent が `.claude/agents/doc-validator.md` に配置されていること

## 実行手順

1. **整形を適用**
   - `./format.sh fix`
   - Markdown / YAML / JSON を一括で Prettier + Markdownlint 対応に揃えます
   - 変更量が大きい場合は `./format.sh check` で確認してからコミットしてください
2. **ドキュメント検証を実行**
   - メインエージェント上で以下を実行  
     ```
     > use the doc-validator agent to run full documentation validation
     ```
   - doc-validator は READ 専用で、整形・FrontMatter・Schema・一次情報リンクの有無をチェックします
3. **結果を集約**
   - 整形による変更概要（ファイル種別 / 件数）を整理
   - doc-validator のレポートを確認し、残件があれば ⚠️ / 🔴 として列挙
   - 必要に応じて修正タスクを作成、または CI へのフィードバックに活用

## レポートテンプレート

```markdown
# Format & Validation Report

## Formatting
✅ Fixed: <Markdown files> Markdown, <YAML files> YAML, <JSON files> JSON

## Validation (doc-validator)
✅ Format: ...
✅ FrontMatter: ...
⚠️ Content Quality: ...
✅ Schema: ...

## Action Required
- [フォローアップ項目]（例: notes/example.md:42 に出典日付を追加）
```

## 利用タイミング

- コミット前の最終確認
- 複数のドキュメントを更新した直後
- Lint / Schema チェックでエラーが検出されたとき
- リリースノートやガイドラインの大幅改訂時

## コマンド呼び出し

```bash
/project:docs-format-validate
```

## メリット

- **コンテキストの健全性**: メインエージェントは履歴を保持し、Subagent が READ のみで検証
- **自動化された品質基準**: プロジェクト規約（一次情報リンク、FrontMatter 必須項目）を doc-validator が網羅
- **再利用性**: Slash コマンド化でチーム全体が同一フローを即時再現可能
