## プロジェクト構造規約

root/
├── .codeiuminogre # Codeium 用除外パターン
├── .cursorinogre # Cursor 用除外パターン
├── .claude/ # Claude AI 設定
├── .config/ # Lint・検証設定
│ ├── jsonschema.conf.yaml # JSON Schema 検証設定
│ └── .yamllint.yml # YAML Lint 設定
├── .github/ # GitHub 関連設定
│ ├── workflows/ # CI/CD ワークフロー
│ ├── ISSUE_TEMPLATE/ # Issue テンプレート
│ └── PULL_REQUEST_TEMPLATE/ # PR テンプレート
├── .vscode/ # VS Code 設定
├── .windsurfrules # Windsurf ルール（互換用）
├── ai/ # AI アシスタントプロファイル
│ ├── chatgpt/ # ChatGPT 用設定
│ ├── claude/ # Claude 用設定（Claude Code 含む）
│ ├── common/ # 共通ルール（グローバル/プロジェクト）
│ ├── cursor/ # Cursor 用設定
│ ├── gemini/ # Gemini 用設定
│ ├── openai_codex/ # OpenAI Codex 用設定
│ ├── prompts/ # AI 共通プロンプト補助
│ └── windsurf/ # Windsurf 用設定
├── clips/ # 記事要約・引用
├── CLAUDE.md # Claude Code 向け指示
├── notes/ # 日次ログ・テーマ別ノート
├── policy/ # リポジトリ運用指針
├── schemas/ # JSON Schema 雛形
├── snippets/ # プロンプト・スクリプトメモ
├── tools/ # 生成補助・整形・同期スクリプト
│ ├── gen/ # 生成系スクリプト
│ └── sync/ # 同期系スクリプト
├── tmp/ # 一時ファイル置き場（Git 管理対象）
├── node_modules/ # npm 依存パッケージ
├── .editorconfig # エディタ設定
├── .gitignore # Git 除外設定
├── .markdownlint.jsonc # Markdown Lint 設定
├── .prettierignore # Prettier 除外設定
├── .prettierrc.json # Prettier 設定
├── AGENTS.md # AI エージェント運用ガイド
├── directorystructure.md # プロジェクト構造説明
├── format.sh # フォーマット実行スクリプト
├── LICENSE # MIT ライセンス
├── package.json # npm 依存関係
├── package-lock.json # npm ロックファイル
├── README.md # プロジェクトメイン説明
└── technologystack.md # 技術スタック説明
