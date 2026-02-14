# 技術スタック

## コア技術

- Node.js: >=18.0.0
- Shell Script (Bash)

## ドキュメント・設定形式

- Markdown (.md)
- YAML (.yml, .yaml)
- JSON (.json, .jsonc)

## フォーマッター

- Prettier: ^3.4.2
  - 対象: Markdown, YAML, JSON
  - 設定ファイル: `.prettierrc.json`, `.prettierignore`

## リンター（品質チェック）

- Markdownlint: ^0.36.0
  - CLI: markdownlint-cli2 ^0.15.0
  - 設定ファイル: `.markdownlint.jsonc`
- yamllint（Python製、`pip install yamllint` でインストール）
  - 設定ファイル: `.config/.yamllint.yml`

## JSON Schema検証

- check-jsonschema（Python製、`pip install check-jsonschema` でインストール）
  - AI プロファイル: `schemas/ai_profile.schema.json`
  - ノート: `schemas/notes.schema.json`

## 開発ツール

- npm: ^10.0.0（devDependencies管理）
- Git（バージョン管理）
- GitHub Actions（CI/CD）

## CI/CD

- GitHub Actions
  - ワークフロー: `.github/workflows/ci.yml`
  - チェック項目:
    - Prettier フォーマット検証
    - Markdown Lint
    - YAML Lint
    - JSON Schema 検証
    - Gitleaks（シークレットスキャン）

## フォーマット・検証スクリプト

- `format.sh`
  - モード: `check`（検証のみ）, `fix`（自動修正）
  - 実行: `./format.sh [check|fix]`
  - npm scripts: `npm run lint`, `npm run fix`
