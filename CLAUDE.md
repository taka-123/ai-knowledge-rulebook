## プロジェクト概要

- 何を作っているか: AI エージェント設定、運用ルール、学習ノートの正本。
- 主要利用者: 複数 AI ツールを横断して運用する開発者と AI Coding Agent。
- コアバリュー: 正本を `ai/` に集約し、ツール別配布先へ安全に同期する。
- ランタイム / パッケージマネージャ: Node.js 18 以上 / npm。

## 参照先

- 全体概要: `README.md`
- 技術スタック: `package.json`
- ディレクトリ構造: `README.md`

実態とドキュメントが食い違う場合は、実ディレクトリ、設定ファイル、テスト、依存関係マニフェストを優先し、必要に応じてドキュメント更新を提案する。

## プロジェクト構造

- `ai/`: 各 AI ツール向け設定・ルールの正本。
- `.claude/skills/`: このリポジトリ内で使う Skill 定義。
- `scripts/`: `ai/` からホーム配下へ同期するスクリプトと検証スクリプト。
- `schemas/`: `ai/` と `notes/` 向け JSON Schema。
- `notes/`: 学習ノート。
- `snippets/`: テンプレート / 雛形。
- `.work/`: 作業用ドキュメント。
- 生成物: `node_modules/` や検証・出力用の一時ディレクトリは編集対象にしない。
- 直接編集してはいけないもの: `~/.claude`、`~/.cursor`、`~/.codex`、`~/.gemini`、`~/.codeium` などの配布先。

## アーキテクチャ不変条件

- レイヤー / モジュール責務: `ai/` が正本、`scripts/` が同期・検証、`schemas/` が構造検証を担う。
- 依存方向: 配布先の変更を正本へ逆流させず、正本から同期スクリプトで反映する。
- データ境界 / 入力検証地点: JSON は `schemas/`、Agent / Skill は `scripts/validate-*.mjs` で検証する。
- バイパス禁止コンポーネント: `scripts/sync-*-to-home.sh` と `npm run agent:check`。

設計ルール:

- 既存パターンを優先し、並行する抽象を新設しない。
- factory、registry、plugin system、config-driven dispatch は、実呼び出し箇所が 2 つ以上揃ってから検討する。
- アーキテクチャ違反が必要な変更は、編集前に停止してトレードオフを提示する。

## ハード制約（commitments, not preferences）

- 秘密情報、トークン、`.env*` を git に入れない。
- 依頼範囲外のリファクタや整形を行わない。
- 既存実装を確認せず新しいランタイム依存を追加しない。
- 同期先契約や Agent / Skill の自動マッチ条件を変える場合は、対応する検証とドキュメント更新を伴う。
- 失敗テスト、lint、型エラーを、無効化や回避で「通った」ことにしない。
- 生成ファイル（`dist/`、`build/` 等）は直接編集しない。lockfile を変更する場合は理由を明示する。
- commit、reset、rebase、force-push、branch 削除、PR 作成は、明示依頼なしに行わない。

## プロジェクト固有ルール

- `ai/` を正本として編集し、ホーム配下への反映は `scripts/sync-*-to-home.sh` を使う。
- `.claude/skills/<name>/SKILL.md` が Skill 本文の置き場。ルーターや補助設定に本文を複製しない。
- Agent / Skill の description と Trigger Keywords は自動マッチに使われるため、責務や対象パスを具体的に書く。
- JSON、YAML、Markdown は既存の formatter / linter / schema に合わせ、検証を弱めて通さない。

## 環境とコマンド

- Install: `npm install`、`pip install check-jsonschema yamllint`
- Test (focus): 変更対象に応じて `npm run schema:check` または個別の `*:check`
- Test (full): `npm run agent:check`
- Lint: `npm run lint`
- その他: `./scripts/sync-all-to-home.sh`、必要に応じて `./scripts/sync-*-to-home.sh`

検証手順:

1. 変更箇所に対応する最小のテストから実行する。
2. 共有ルール、Agent、Skill、schema、同期スクリプトに触れた場合は、より広い検証を実行する。
3. 実行したコマンドと、失敗した場合の正確な出力を報告する。

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

## テストと検証

- ルール修正: 対象の Markdown lint / format check を行う。
- Agent / Skill 修正: 対応する `*:check` を実行し、必要に応じて `npm run agent:check` まで広げる。
- JSON / YAML 修正: format check、schema check、または対象 validation を実行する。
- 検証できない場合は、未検証の理由と、ユーザーが実行すべきコマンドを示す。

## 外部情報

外部 SDK、フレームワーク、クラウドサービス、CLI、API 仕様、バージョン依存の挙動に関わる場合は、内部知識だけで判断しない。

- まず、このリポジトリの `package.json`、lockfile、設定、import、既存使用例、型定義を確認する。
- ライブラリ・フレームワークの仕様確認は、`context7` など一次情報系 MCP サーバーが利用可能ならそれを活用する。
- 不足する場合に WebFetch / WebSearch で公式ドキュメント、公式リポジトリ、changelog を確認する。
- 根拠にした情報源（URL、ファイルパス、コミット）と、必要に応じて確認日・対象バージョンを簡潔に示す。

## コンテキスト衛生

- 大規模調査、依存追跡、セキュリティ確認、横断 grep は subagent に委任し、メインに集約結果のみ取り込む。
- 繰り返し手順や長いチェックリストは `.claude/skills/<name>/SKILL.md` に分離する。
- 個人専用の上書きは `CLAUDE.local.md`（git 管理外）。

## Shell

- Shell ツール使用時は、**常に** 絶対パスの `working_directory` を指定する。
- `cd` を前提にしたコマンド連鎖は使わない。
- 一時ファイルは完了時に削除するか、削除を提案する。

## 完了報告

- 何を変えたか
- なぜ変えたか
- 実行した検証コマンドと結果
- 未検証事項と残リスク
- 検証が失敗した、または実施できなかった場合に「成功」と報告しない。
