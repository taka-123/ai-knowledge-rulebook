# 技術スタック（※本記載は記入例です-プロジェクトに合わせて内容を更新してください-）

## コア技術

### 言語・ランタイム

- TypeScript: ^5.0.0
- Node.js: ^20.0.0
- **AIモデル: claude-3-7-sonnet-20250219 (Anthropic Messages API 2023-06-01) ← バージョン変更禁止**

### フレームワーク

- Next.js: ^15.1.3
- React: ^19.0.0

## フロントエンド

- Tailwind CSS: ^3.4.17
- shadcn/ui: ^2.1.8

## バックエンド

- SQLite: ^3.0.0
- Prisma: ^5.0.0

## ドキュメント・設定形式

- Markdown (.md)
- YAML (.yml, .yaml)
- JSON (.json, .jsonc)

## 開発ツール

### パッケージマネージャ

- npm: ^10.0.0

### リンター（品質チェック）

- ESLint: ^9.0.0
- 設定ファイル: `eslint.config.mjs`

### その他

- TypeScript: ^5.0.0
- PostCSS: 最新版（Next.js同梱）

## バージョン管理・CI/CD

### バージョン管理

- Git（バージョン管理）
- GitHub（ホスティング）

### CI/CD

- GitHub Actions
- ワークフロー: `.github/workflows/`
- チェック項目:
  - Lint実行
  - 型チェック
  - ビルド検証

## API バージョン管理

### 重要な制約事項

- APIクライアントは `app/lib/api/client.ts` で一元管理
- AI モデルのバージョンは client.ts 内で厳密に管理
- これらのファイルは変更禁止（変更が必要な場合は承認が必要）：
  - `client.ts` - AIモデルとAPI設定の中核
  - `types.ts` - 型定義の一元管理
  - `config.ts` - 環境設定の一元管理

### 実装規則

- AIモデルのバージョンは client.ts でのみ定義
- 型定義は必ず types.ts を参照
- 環境変数の利用は config.ts 経由のみ許可

## 開発・ビルドスクリプト

- `npm run dev`: 開発サーバー起動
- `npm run build`: プロダクションビルド
- `npm run lint`: Lint実行
- `npm run start`: プロダクションサーバー起動
