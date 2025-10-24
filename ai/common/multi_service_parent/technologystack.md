# 技術スタック（※本記載は記入例です-プロジェクトに合わせて内容を更新してください-）

## 共通ツール

### バージョン管理

- Git（各サービスは独立リポジトリとして管理）
- GitHub（ホスティング）
- [プロジェクト固有のバージョン管理ルールを追記してください]

### 共通CI/CD

- GitHub Actions（全サービス共通）
- [共通のCI/CD設定ファイルパスを記載してください]

### 共通開発環境

- Docker Desktop: ^4.0.0
- Docker Compose: ^2.0.0
- [環境変数管理方法を記載してください（例: .env.local, AWS Secrets Manager等）]

### ドキュメント・設定形式

- Markdown (.md)
- YAML (.yml, .yaml)
- JSON (.json, .jsonc)

## サービス固有の技術スタック

各サービスの詳細な技術スタックは、各サービスディレクトリの `technologystack.md` を参照してください：

### admin-dashboard（管理者用ダッシュボード）

- 詳細: `admin-dashboard/technologystack.md` を参照

### customer-app（利用者用アプリ）

- 詳細: `customer-app/technologystack.md` を参照

### backend-api（バックエンドAPI）

- 詳細: `backend-api/technologystack.md` を参照
