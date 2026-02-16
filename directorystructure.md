# ディレクトリ構成

以下のディレクトリ構造に従って実装を行ってください：

./
├── .codeiumignore # Codeium 用除外パターン
├── .cursorignore # Cursor 用除外パターン
├── .cursor/ # Cursor 用設定（rules/agents/skills/commands）
│ ├── agents/ # Cursor 専用サブエージェント
│ │ ├── content-writer.md # 調査結果の規約準拠書き込み
│ │ ├── doc-validator.md # ドキュメント品質検証（読み取り専用）
│ │ ├── external-fact-guardian.md # 外部仕様の書き込み前事実確認
│ │ ├── repo-cartographer.md # リポジトリ構造・参照関係の地図化
│ │ └── repo-scaffolder.md # 新規ファイルのテンプレート適用・生成
│ ├── rules/ # Cursor ルール（.mdc）
│ ├── skills -> ../.claude/skills # シンボリックリンク（Canonical Source 参照）
│ └── commands/ # Cursor コマンド
├── .claude/ # Claude AI 設定
│ ├── agents/ # プロジェクト専用サブエージェント
│ │ ├── content-writer.md # 調査結果の規約準拠書き込み
│ │ ├── doc-validator.md # ドキュメント品質検証（読み取り専用）
│ │ └── external-fact-guardian.md # 外部仕様の書き込み前事実確認
│ │ ├── repo-cartographer.md # リポジトリ構造・参照関係の地図化
│ │ ├── repo-scaffolder.md # 新規ファイルのテンプレート適用・生成
│ ├── skills/ # Canonical Source — 全ツール共通スキル定義
│ │ ├── backlog-markdown-formatting/ # バックログ用 Markdown 整形
│ │ ├── content-scaffold/ # 新規ファイルテンプレート適用・バリデーション
│ │ ├── context-compress-map/ # コンテキスト圧縮マップ生成
│ │ ├── debug-strategist/ # デバッグ戦略策定
│ │ ├── docs-sync/ # 主要ドキュメントの実態同期
│ │ ├── documentation-standards/ # 記述規約強制チェック
│ │ ├── format-lint-audit/ # Format/Lint チェック実行と結果報告
│ │ ├── git-helper/ # Git 操作補助
│ │ ├── lint-fix/ # Lint 自動修正
│ │ ├── research-protocol/ # 技術調査の出典・不確実性プロトコル強制
│ │ ├── schema-guard/ # JSON スキーマ適合検証
│ │ ├── task-planner/ # タスク計画・分解
│ │ └── ui-standardizer/ # UI/UX 規約チェック
│ ├── commands/ # カスタムコマンド（ci-check, format-fix 等）
│ ├── hooks/ # Bash・WebFetch 検証スクリプト
│ ├── settings.json # Claude Code 権限・hooks設定
│ └── settings.local.json # ローカル追加設定
├── .config/ # Lint・検証設定
│ ├── jsonschema.conf.yaml # JSON Schema 検証設定
│ └── .yamllint.yml # YAML Lint 設定
├── .github/ # GitHub 関連設定
│ ├── workflows/ # CI/CD ワークフロー
│ ├── PULL_REQUEST_TEMPLATE.md # PR テンプレート
│ └── ISSUE_TEMPLATE/ # Issue テンプレート
├── .windsurf/ # Windsurf 用設定
│ ├── rules/ # Windsurf ルール（.md）
│ └── skills -> ../.claude/skills # シンボリックリンク（Canonical Source 参照）
├── .agent/ # Agent 互換設定
│ └── skills -> ../.claude/skills # シンボリックリンク（Canonical Source 参照）
├── .agents/ # Agents 互換設定
│ └── skills -> ../.claude/skills # シンボリックリンク（Canonical Source 参照）
├── .vscode/ # VS Code 設定
├── ai/ # AI アシスタントプロファイル
│ ├── chatgpt/ # ChatGPT 用設定
│ ├── claude/ # Claude 用設定
│ ├── claude_code/ # Claude Code 用設定
│ ├── common/ # 共通ルール（グローバル/プロジェクト）
│ ├── cursor/ # Cursor 用設定
│ ├── gemini/ # Gemini 用設定
│ ├── openai_codex/ # OpenAI Codex 用設定
│ └── windsurf/ # Windsurf 用設定
├── clips/ # 記事要約・引用
├── CLAUDE.md # Claude Code 向け指示
├── notes/ # 日次ログ・テーマ別ノート
├── policy/ # リポジトリ運用指針
├── schemas/ # JSON Schema 雛形
├── scripts/ # 検証スクリプト（validate-skills.mjs, validate-routing.mjs）
├── snippets/ # プロンプト・スクリプトメモ（editor/ 含む）
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
