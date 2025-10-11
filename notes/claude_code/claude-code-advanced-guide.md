## Claude Code 応用実践ガイド（エキスパート向け）

### 概要

Claude Code（Sonnet 4.5想定）の**高度機能**を、一次情報に基づいて「何ができる」「どこで設定」「どう使う」を短距離で把握できるよう整理。対象は**Subagents/Plugins/Hooks/MCP/SDK/GitHub Actions/Slash Commands/Checkpoints（実装状況含む）/その他運用Tips**。記述は公式Docs/公式GitHubの範囲に限定し、各節末に出典を付す。

---

## 設計原則（共通）

* **設定の階層**：ユーザー `~/.claude/*`、プロジェクト `.claude/*`、エンタープライズ管理ポリシーで上書き。CLIフラグと組み合わせて挙動を固定化。([anthropic.mintlify.app][1])
* **権限制御**：`allowedTools/deniedTools` 相当は設定/SDK/CLIで制御。非対話（print/CI）では `--permission-mode` などでゲートを明示。([anthropic.mintlify.app][2])
* **ストリーミング前提**：SDKは**イベントストリーム**（tool_use/result等）を扱う。UI/ログへ逐次反映する設計が基本。([anthropic.mintlify.app][3])

---

## Subagents（サブエージェント）

**何ができる**

* 専門化したエージェントを複数定義し、メインから委譲。ツール/モデル/プロンプトをエージェント単位で切替え、コンテキストを分離。([Qiita][4])

**どこで設定**

* プロジェクト/ユーザー配下の設定・定義ファイル、またはCLIから動的注入（`--agents`）。([anthropic.mintlify.app][2])

**どう使う（実践）**

* 役割ごとに `description` を明確化（発火条件のヒント）。**継承**（親のツール/モデル）と**制限**（セキュアな最小権限）を併用。**オーケストレーション**は「親が要約統合」前提で設計。([Qiita][4])

---

## Plugins（プラグイン）

**何ができる**

* Claude Codeに**再利用可能な機能パッケージ**を追加。Hook/Slash Command 連携も可能（プラグイン側のフックは自動マージ）。([anthropic.mintlify.app][5])

**どこで設定**

* プラグインのフック定義（例：`hooks.json`）はユーザー/プロジェクト設定と統合。**公式ChangelogでPlugin System公開が告知**。([anthropic.mintlify.app][5])

**どう使う（実践）**

* **セキュリティ境界**：プラグインが追加するフック/コマンドは実行権限・入出力を監査。**最小権限＋明示的許可**で運用。([anthropic.mintlify.app][5])

---

## Hooks（フック）

**何ができる**

* ライフサイクルイベントで**決定論的に**シェルコマンドを実行（例：PreToolUseでブロック、PostToolUseで整形/通知）。MCPツール名は特別な命名でマッチ可能。([anthropic.mintlify.app][1])

**主なイベント**

* `PreToolUse` / `PostToolUse` / `UserPromptSubmit` / `Notification` / `Stop` / `SubagentStop` / `PreCompact` / `SessionStart` / `SessionEnd`。**`SubagentStart` は存在しない。**([anthropic.mintlify.app][1])

**どこで設定**

* `~/.claude/settings.json` / `.claude/settings.json` / `.claude/settings.local.json`（非コミット）/ エンタープライズ管理ポリシー。マッチャー（ツール名/正規表現）＋コマンド。([anthropic.mintlify.app][1])

**実践コード（最小例）**

* 危険Bashを事前ブロック：`PreToolUse` で検査し、**exit 2** で中止（ブロックエラー）。([anthropic.mintlify.app][6])

---

## MCP（Model Context Protocol）連携

**何ができる**

* Claude Codeに**外部ツール/データソース**を接続（Jira/Slack/GitHub/DB/SaaS）。MCPサーバを追加し、ツールをエージェントから直接呼ぶ。([anthropic.mintlify.app][7])

**どこで設定**

* 追加方法（HTTP/SSE/stdio）、**スコープ（ローカル/プロジェクト/ユーザー）階層と優先**、認証、`.mcp.json` の環境変数展開を公式ガイドが網羅。([anthropic.mintlify.app][8])

**高度トピック**

* **Messages APIのMCPコネクタ**（βヘッダ要）：API直結でリモートMCPツールを使う（**ツールコールのみ対応**）。([anthropic.mintlify.app][9])

---

## SDK（Claude Agent SDK）

**要点**

* **名称変更**：Claude Code SDK → **Claude Agent SDK**（TS/Python）。移行ガイドあり。([anthropic.mintlify.app][10])
* **TS/Py共通**：`query()` は**非同期イテレータ**を返し、**イベントストリーミング**を逐次処理。長対話や割り込みはクラスAPI（Pythonの `ClaudeSDKClient` 等）で。([anthropic.mintlify.app][3])

**設定と実装Tips**

* **設定ソース**はオプトイン（プロジェクト設定を読むかは明示指定）／**許可モード**・**ツール制限**はOptions/フラグで固定。([anthropic.mintlify.app][11])
* **独自MCPツール**：Pythonは `@tool`＋`create_sdk_mcp_server()` で**インプロセスMCPサーバ**を組込み、`allowed_tools` で露出制御。([anthropic.mintlify.app][12])

---

## GitHub Actions 連携（CI/CD）

**何ができる**

* PR/Issueで **@claude メンション**やワークフロー発火に応じて、解析・実装・修正・PR作成を自動化。App/Action/ベースActionを提供。([anthropic.mintlify.app][13])

**どう設定**

* 公式Action `anthropics/claude-code-action` をworkflowに組み込み（Anthropic直API/Bedrock/Vertexをサポート）。v1 GAのリリース有り。([GitHub][14])

**レシピ指針**

* **失敗E2Eの根因解析**や**影響範囲テスト計画**、**リリースノート下書き**は、ワークフローで**明示のプロンプト**＋`--max-turns` 等のCLI引数を渡す。([anthropic.mintlify.app][13])

---

## Slash Commands（スラッシュコマンド）

**何ができる**

* セッション制御・設定編集・MCP/Hook操作・ファイル添付等を**対話的に**。**カスタムスラッシュコマンド**も定義可（引数/ステップ駆動）。

**活用例**

* `/hooks` でGUIライクにフック登録、`/ide` でIDE統合、`/compact` でコンテキスト圧縮。**カスタムコマンド**は運用プロトコルの定着に有効。

---

## Checkpoints（チェックポイント）

**現状整理**

* VS Code拡張のページに**「未実装（Not Yet Implemented）」としてCheckpoints**が記載。CLIの**Compact/Rewind関連**はHooksの `PreCompact` 等と併せて運用。([anthropic.mintlify.app][15])

---

## その他：出力スタイル／インタラクティブ運用／CLI

* **出力スタイル**：Claude Codeを**非コード用途**に適応（core機能を保持したまま出力様式を切替）。([anthropic.mintlify.app][16])
* **バックグラウンドBash**：長時間コマンドを非同期実行しつつ対話継続。出力は後で取得。([anthropic.mintlify.app][17])
* **CLIフラグ**：`--output-format json|stream-json`（機械可読）、`--permission-mode`、`--max-turns`、`--model`、`--agents` など。([anthropic.mintlify.app][2])

---

## 実践チェックリスト

* [ ] Subagents：役割・許可を**最小権限**で分割し、親で**統合要約**
* [ ] Plugins：導入前に**フック/権限差分**と実行ユーザーの境界を監査
* [ ] Hooks：`PreToolUse` を**ブロックゲート**に、`PostToolUse` を**整形・通知**に
* [ ] MCP：**スコープ階層**（ローカル/プロジェクト/ユーザー）を合意して接続
* [ ] SDK：**ストリーミング**前提でUI/ログ配線、Pythonは `ClaudeSDKClient` で長対話
* [ ] Actions：**@claude** と **明示プロンプト**を分け、`--max-turns` 等で収束性を担保
* [ ] Slash：**/hooks /compact /ide** を日常運用コマンドに昇格

---

## 主要出典（一次情報）

* Subagents（構成と連携）: Subagents - Claude Docs（英語）. ([Qiita][4])
* Plugins（統合・フック自動マージ）: 公式発表（2025-10-09）, Hooks reference（Plugin hooks節）, Changelog（Plugin System Released）. ([Anthropic News](https://www.anthropic.com/news/claude-code-plugins)) ([anthropic.mintlify.app][5])
* Hooks（イベント/設定/Exit挙動/ガイド）: Hooks reference / Hooks guide（英/日）. ([anthropic.mintlify.app][1])
* MCP（接続/スコープ/実例）: Connect Claude Code to tools via MCP（英/日）, MCP overview, MCP connector(API). ([anthropic.mintlify.app][7])
* SDK（概要/TS/Py/移行）: Agent SDK overview / TypeScript reference / Python reference / Migration guide. ([anthropic.mintlify.app][11])
* GitHub Actions（製品ページ/Action/リリース）: Docs（英/日）, `anthropics/claude-code-action`（README/Release）。 ([anthropic.mintlify.app][13])
* Slash Commands（組込み/カスタム）: Slash commands - Claude Docs（英）.
* 出力スタイル/インタラクティブ/CLI：Output styles / Interactive mode / CLI reference（英/日）。 ([anthropic.mintlify.app][16])
* IDE（Checkpointsの実装状況）: VS Code integration - Claude Docs. ([anthropic.mintlify.app][15])

---

### 付記（不確実性の注記）

* **Pluginsの詳細仕様ページ**はDocs内で随所に記載（Hooks/Slashとの統合言及）が見つかる一方、専用ページの索引性は限定的。運用は**Hooks/Slash/MCPとの接合点**を一次情報として参照。([anthropic.mintlify.app][5])

---
