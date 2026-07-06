## プロジェクト概要

- 何を作っているか: AI エージェント設定、運用ルール、学習ノートの正本。
- 主要利用者: 複数 AI ツールを横断して運用する開発者と AI Coding Agent。
- コアバリュー: 設定テンプレートの正本を `ai/` に集約し、配布先（ホームや各 repo）へ安全に同期する。
- ランタイム / パッケージマネージャ: Node.js 20.17 以上 / npm。

## 参照先

- 全体概要: `README.md`
- テンプレート設計・3 階層: `ai/README.md`
- 同期マッピング: `scripts/README.md`
- 技術スタック: `package.json`

実態とドキュメントが食い違う場合は、実ディレクトリ、設定ファイル、テスト、依存関係マニフェストを優先し、必要に応じてドキュメント更新を提案する。

## 編集境界（デフォルト）

| 区分                       | 場所                                                                    | 役割                     | デフォルト     |
| -------------------------- | ----------------------------------------------------------------------- | ------------------------ | -------------- |
| **A テンプレート正本**     | `ai/<tool>/{global\|multi_service_parent\|project}/`                    | コピー配布する推奨設定   | **編集対象**   |
| **B リポジトリ生ファイル** | ルート直下（`CLAUDE.md`、`AGENTS.md`、`.claude/`、`.cursor/` 等）       | この repo 自身の運用設定 | 明示依頼時のみ |
| **C ホーム生ファイル**     | `~/.claude/`、`~/.cursor/`、`~/.codex/`、`~/.gemini/`、`~/.codeium/` 等 | マシン上の配布先         | 明示依頼時のみ |

- 依頼対象が特定階層・ツールに紐づかなければ、まず `ai/` 配下のテンプレートを Read で探し、そこを編集する。
- B / C には書き込まず、配布先の変更を A へ逆流させない。反映は `./scripts/sync-*-to-home.sh` をユーザーが実行する。
- ユーザーが「ルートの `CLAUDE.md` を直して」等と B / C を明示した場合のみ、そこを編集する。
- `ai/` の 3 階層: `global/` = マシン / ユーザー全体、`multi_service_parent/` = モノレポ親、`project/` = 単一サービス。

詳細は `ai/README.md`（テンプレート設計）と `scripts/README.md`（配布先マッピング）。

## プロジェクト構造

- `ai/`: 各 AI ツール向けの **設定テンプレート正本**。
- `scripts/`: `ai/` からホーム配下へ同期するスクリプトと検証スクリプト。
- `schemas/`: `ai/` と `notes/` 向け JSON Schema。
- `notes/`: 学習ノート。
- `snippets/`: テンプレート / 雛形。
- `.work/`: 作業用ドキュメント。
- ルート直下と `~/.claude` 等の配布先は **生きた設定**。編集ポリシーは「編集境界」を参照。
- 生成物（`node_modules/` 等）は編集対象にしない。

## アーキテクチャ不変条件

- レイヤー / モジュール責務: `ai/` がテンプレート正本、`scripts/` が同期・検証、`schemas/` が構造検証を担う。
- データ境界 / 入力検証地点: JSON は `schemas/`、Agent / Skill は `scripts/validate-*.mjs` で検証する。
- バイパス禁止コンポーネント: `scripts/sync-*-to-home.sh` と `npm run agent:check`。

設計ルール:

- 既存パターンを優先し、並行する抽象を新設しない。
- アーキテクチャ違反が必要な変更は、編集前に停止してトレードオフを提示する。

## ハード制約（commitments, not preferences）

- 秘密情報、トークン、`.env*` を git に入れない。
- 依頼範囲外のリファクタや整形を行わない。
- 既存実装を確認せず新しいランタイム依存を追加しない。
- 同期先契約や Agent / Skill の自動マッチ条件を変える場合は、対応する検証とドキュメント更新を伴う。
- 失敗テスト、lint、型エラーを、無効化や回避で「通った」ことにしない。
- 失敗を隠すための暫定コード、ダミー値、不要な TODO、デバッグ出力、コメントアウトされたコードを残さない。
- 生成ファイル（`dist/`、`build/` 等）は直接編集しない。lockfile を変更する場合は理由を明示する。
- commit、reset、rebase、force-push、branch 削除、PR 作成は、明示依頼なしに行わない。

## プロジェクト固有ルール

- Skill 本文の置き場は、テンプレートなら `ai/claude_code/global/.claude/skills/<name>/SKILL.md`、この repo 自身の運用なら `.claude/skills/<name>/SKILL.md`。ルーターや補助設定に本文を複製しない。
- Agent / Skill の description と Trigger Keywords は自動マッチに使われるため、責務や対象パスを具体的に書く。
- JSON、YAML、Markdown は既存の formatter / linter / schema に合わせ、検証を弱めて通さない。
- Skill / Agent / ルールなど AI 向け指示文書の作成・編集は、`instruction-authoring` スキルの記述規約と刈り込み判定に従う。
- グローバル配布資産（`ai/*/global/`、`ai/common/`）はツール中立にする。特定ツールのルールファイル名（CLAUDE.md / AGENTS.md 等）や固有資産名に依存する記述をしない。

## 環境とコマンド

- Install: `npm install`、`pip install check-jsonschema yamllint`
- Test (focus): 変更対象に応じて `npm run schema:check` または個別の `*:check`
- Test (full): `npm run agent:check`
- Lint: `npm run lint`
- その他: `./scripts/sync-all-to-home.sh`、必要に応じて `./scripts/sync-*-to-home.sh`

## テストと検証

1. 変更箇所に対応する最小の `*:check` から実行する（ルール: `lint:md` / Agent・Skill: `skills:check` 等 / JSON・YAML: `schema:check` または対象 lint）。
2. 共有ルール、Agent、Skill、schema、同期スクリプトに触れた場合は `npm run agent:check` まで広げる。
3. 実行コマンドと、失敗時の正確な出力を報告する。検証できない場合は理由と、ユーザーが実行すべきコマンドを示す。
4. `scripts/validate-*.mjs` は検証対象 0 件のとき fail させる（「passed (0 files)」を合格と扱わない）。

## 自律範囲

自律実行してよい:

- ローカルかつ可逆な変更。
- 既存パターンが明確に適用できる変更。
- ローカルで検証コマンドが実行できる場合。
- 本番データ、秘密情報、外部副作用が絡まない場合。

停止して確認・選択肢提示:

- 要件が矛盾する場合。
- セキュリティ、認証、秘密情報、配布先の破壊的変更、同期先契約に影響する場合。
- コード・テスト・ドキュメントから正解を推定できない場合。
- ローカルで検証できない場合。

## タスク契約

非自明な変更では、実装前に短く整理する。

1. Goal — 何を変えるか
2. Scope — 触る可能性が高いファイル、モジュール、API、画面
3. Constraints — 互換性、設計、セキュリティ、性能、スタイル上の制約
4. Done when — 何が通れば完了か

誤った解釈のコストが高い場合は確認する。そうでなければ、前提を明記して進める。

## 外部情報

外部 SDK、フレームワーク、CLI、API 仕様、バージョン依存の挙動に関わる場合は内部知識だけで判断しない。

- まず `package.json`、lockfile、設定、import、既存使用例、型定義を確認する。
- 必要なら `context7` 等の一次情報系 MCP、または WebFetch / WebSearch で公式ドキュメント・changelog を確認する。
- 根拠（URL、ファイルパス、コミット）と、必要に応じて確認日・対象バージョンを示す。

## コンテキスト衛生

- 大規模調査、依存追跡、セキュリティ確認、横断 grep は subagent に委任し、メインに集約結果のみ取り込む。
- 繰り返し手順や長いチェックリストは `.claude/skills/<name>/SKILL.md` に分離する。
- 個人専用の上書きは `CLAUDE.local.md`（git 管理外）。

## Shell

- Shell 実行時は絶対パスの `working_directory` を指定し、`cd` を前提にしたコマンド連鎖は使わない。
- 一時ファイルは完了時に削除するか、削除を提案する。

## 完了報告

- 何を変えたか
- なぜ変えたか
- 実行した検証コマンドと結果
- 未検証事項と残リスク
- 検証が失敗した、または実施できなかった場合に「成功」と報告しない。
