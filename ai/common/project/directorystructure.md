# ディレクトリ構成（※本記載は記入例です-プロジェクトに合わせて内容を更新してください-）

以下のディレクトリ構造に従って実装を行ってください：

```
./
├── .git/                        # Gitリポジトリルート
├── AGENTS.md                    # AIエージェント運用ガイド（project層）
├── CLAUDE.md                    # Claude Code向け指示（project層）
├── .windsurfrules               # Windsurf互換用（`@AGENTS.md に従う`と記載）
├── directorystructure.md        # 本ファイル
├── technologystack.md           # 技術スタック説明
├── .github/                     # GitHub関連設定
│   ├── workflows/               # CI/CDワークフロー
│   ├── PULL_REQUEST_TEMPLATE.md # PRテンプレート
│   └── ISSUE_TEMPLATE/          # Issueテンプレート
├── .vscode/                     # VS Code設定
├── app/                         # Next.jsアプリケーションディレクトリ
│   ├── api/                     # APIエンドポイント
│   │   └── [endpoint]/
│   │       └── route.ts
│   ├── components/              # アプリケーションコンポーネント
│   │   ├── ui/                  # 基本UI（button, card等）
│   │   └── layout/              # レイアウト関連
│   ├── hooks/                   # カスタムフック
│   ├── lib/                     # ユーティリティ
│   │   ├── api/                 # API関連処理
│   │   │   ├── client.ts        # 変更禁止: AIモデル設定
│   │   │   ├── types.ts         # 変更禁止: 型定義
│   │   │   └── config.ts        # 変更禁止: 環境設定
│   │   └── utils/               # 共通関数
│   ├── styles/                  # スタイル定義
│   ├── favicon.ico              # ファビコン
│   ├── globals.css              # グローバルスタイル
│   ├── layout.tsx               # ルートレイアウト
│   └── page.tsx                 # ホームページ
├── public/                      # 静的ファイル
├── node_modules/                # 依存パッケージ
├── package.json                 # プロジェクト設定
├── package-lock.json            # 依存関係ロックファイル
├── tsconfig.json                # TypeScript設定
├── next-env.d.ts                # Next.js型定義
├── next.config.ts               # Next.js設定
├── postcss.config.mjs           # PostCSS設定
├── eslint.config.mjs            # ESLint設定
├── .gitignore                   # Git除外設定
├── .editorconfig                # エディタ設定
├── README.md                    # プロジェクトメイン説明
└── LICENSE                      # ライセンス
```

## ディレクトリ説明

### 重要な配置ルール

- UIコンポーネント → `app/components/ui/`
- APIエンドポイント → `app/api/[endpoint]/route.ts`
- 共通処理 → `app/lib/utils/`
- API関連処理 → `app/lib/api/`

### 変更禁止ファイル

以下のファイルは変更禁止です（変更が必要な場合は承認が必要）：

- `app/lib/api/client.ts` - AIモデルとAPI設定の中核
- `app/lib/api/types.ts` - 型定義の一元管理
- `app/lib/api/config.ts` - 環境設定の一元管理
