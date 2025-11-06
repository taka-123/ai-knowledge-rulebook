---
name: documentation-standards
description: Apply documentation standards for this AI knowledge rulebook project. Use when writing or reviewing Markdown documents, YAML files, or JSON files.
allowed-tools: Read, Grep
---

# Documentation Standards

このプロジェクトのドキュメント作成・編集時の規約です。

## ファイル構造

```
ai-knowledge-rulebook/
├── ai/          # AI関連の技術ドキュメント
├── notes/       # 個人ノート・メモ
├── clips/       # クリップ・引用
├── snippets/    # コードスニペット
├── policy/      # ポリシー・規約
└── schemas/     # JSONスキーマ定義
```

## Markdown 規約

### FrontMatter (notes/ 配下)

**必須フィールド**:

```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - tag1
  - tag2
---
```

### 見出し構造

- H1 (`#`) はファイルに1つのみ
- H2以降は階層的に使用
- 見出しの前後に空行を入れる

### リンク

- 内部リンク: 相対パスで記載
- 外部リンク: 必ず出典・取得日を明記
  ```markdown
  [公式ドキュメント](https://example.com)
  (出典: 2025-01-05 取得)
  ```

## フォーマット自動化

### 使用可能なコマンド

```bash
# 全ファイル整形
./format.sh fix

# チェックのみ（CI同様）
./format.sh check

# 個別実行
npm run lint:md     # Markdown Lint
npm run lint:yaml   # YAML Lint
npm run lint:json   # JSON Lint
npm run fix:md      # Markdown 自動修正
```

## 品質基準

### 必須チェック項目

- ✅ Prettier でフォーマット統一
- ✅ Markdownlint でルール準拠
- ✅ JSONスキーマで構造検証 (AI プロファイル、ノート)
- ✅ 外部リンクに出典・日付

### 禁止事項

- ❌ 個人情報・機密情報の記載
- ❌ 未検証の技術情報を「確定」として記載
- ❌ 推測と事実の混同

## 参照

詳細は以下を参照:

- [CLAUDE.md](../../CLAUDE.md) - プロジェクト固有ルール
- [directorystructure.md](../../directorystructure.md) - ディレクトリ構造
- [technologystack.md](../../technologystack.md) - 技術スタック
