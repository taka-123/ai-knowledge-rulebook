# ディレクトリ構成（※本記載は記入例です-プロジェクトに合わせて内容を更新してください-）

以下のディレクトリ構造に従って実装を行ってください：

```
./
├── AGENTS.md                    # AIエージェント運用ガイド（multi_service_parent層）
├── CLAUDE.md                    # Claude Code向け指示（multi_service_parent層）
├── .windsurfrules               # Windsurf互換用（`@AGENTS.md に従う`と記載）
├── directorystructure.md        # 本ファイル
├── technologystack.md           # 技術スタック説明
├── admin-dashboard/             # 管理者用ダッシュボード（独立Gitリポジトリ）
├── customer-app/                # 利用者用アプリ（独立Gitリポジトリ）
└── backend-api/                 # バックエンドAPI（独立Gitリポジトリ）
```

## ディレクトリ説明

### 各サービスディレクトリ

#### admin-dashboard/（管理者用ダッシュボード）

- 管理者向けのダッシュボードアプリケーション
- 各サービス内部の詳細構造は `admin-dashboard/directorystructure.md` を参照

#### customer-app/（利用者用アプリ）

- エンドユーザー向けのアプリケーション
- 各サービス内部の詳細構造は `customer-app/directorystructure.md` を参照

#### backend-api/（バックエンドAPI）

- 共通バックエンドAPIサーバー
- 各サービス内部の詳細構造は `backend-api/directorystructure.md` を参照
