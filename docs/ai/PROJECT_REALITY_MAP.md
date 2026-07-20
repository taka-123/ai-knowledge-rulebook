# PROJECT_REALITY_MAP

最終確認: 2026-07-07（本セッションのファイル読取・コマンド実行に基づく）

この文書は **事実確認済みの実態** を記録する。設計の理想像や README の記述だけを根拠にしない。

## このプロジェクトが担う責務

| 責務                                                                                        | 根拠                                                                                                                        |
| ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 各 AI ツール向け設定テンプレートの **正本** を `ai/` に集約する                             | `README.md`「最重要ルール」、`AGENTS.md`「プロジェクト構造」、`ai/` 実在                                                    |
| `ai/` からホーム配下（`~/.claude` 等）へ **同期** する Shell スクリプトを提供する           | `scripts/sync-*-to-home.sh`、`scripts/README.md`                                                                            |
| Skill / Agent / Codex 配線 / レビュールーティングを **検証** する Node スクリプトを提供する | `package.json` `agent:check`、`scripts/validate-*.mjs`、`.claude/skills/codex-wiring-doctor/scripts/check-codex-wiring.mjs` |
| JSON Schema によるプロファイル・ノート構造検証の定義                                        | `schemas/`、`npm run schema:check`                                                                                          |
| 学習ノート・スニペット・この repo 自身の live AI 設定を保持する                             | `notes/`、`snippets/`、ルート `.claude/` `.cursor/` `.codex/`                                                               |

**性質**: デプロイ可能なアプリケーションではない。実行ロジックは Shell 同期と Node 検証に限定される（`src/`・`tests/`・`dist/` は存在しない）。

## このプロジェクトが担わない責務

| 非責務                                                           | 根拠                                                        |
| ---------------------------------------------------------------- | ----------------------------------------------------------- |
| AI ツール（Claude Code / Cursor / Codex 等）の起動・実行そのもの | ツールはホーム配下・各 IDE が担当                           |
| ユーザーのホームディレクトリを AI が自律的に更新すること         | `AGENTS.md`「エージェントが守ること」: 同期はユーザーが実行 |
| アプリケーションのビルド・デプロイ・本番運用                     | 該当スクリプト・CI ジョブなし                               |
| 他リポジトリのコード変更（テンプレート配布先 repo の実装）       | `ai/*/project/` は雛形のみ                                  |

## 主要な構成要素と依存方向

```text
┌─────────────────────────────────────────────────────────────┐
│  A: ai/<tool>/{global|multi_service_parent|project}/       │
│     テンプレート正本（通常の編集対象）                        │
└──────────────────────────┬──────────────────────────────────┘
                           │ scripts/sync-*-to-home.sh（ユーザー手動）
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  C: ~/.claude/ ~/.cursor/ ~/.codex/ ~/.gemini/ ~/.codeium/ │
│     マシン上の配布先（AI は明示依頼なしに編集しない）         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  B: ルート AGENTS.md / CLAUDE.md / .claude/ .cursor/ .codex/│
│     この repo 自身の live 設定（明示依頼時のみ編集）            │
└──────────────────────────┬──────────────────────────────────┘
                           │ npm run agent:check
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  scripts/validate-*.mjs + schemas/ + format.sh                │
│  構造・形式・配線の検証                                       │
└─────────────────────────────────────────────────────────────┘
```

**編集境界（3 区分）**: `AGENTS.md`「編集境界」、`CLAUDE.md`「編集境界」

| 区分 | 場所                                                 | デフォルト     |
| ---- | ---------------------------------------------------- | -------------- |
| A    | `ai/<tool>/{global\|multi_service_parent\|project}/` | 編集対象       |
| B    | ルート憲法・`.claude/` `.cursor/` `.codex/` 等       | 明示依頼時のみ |
| C    | `~/.claude/` 等ホーム配下                            | 編集しない     |

**`ai/` の 3 階層**: `global/`（マシン全体）、`multi_service_parent/`（モノレポ親）、`project/`（単一サービス）— `ai/README.md` L26 付近

**共有ルールの単一ソース**: `ai/common/global/AGENTS.md` が Codex / Windsurf / Antigravity / Gemini CLI 等のグローバル AGENTS にコピーされる — `scripts/README.md` L12

## データフロー

### テンプレート配布フロー

1. 開発者または AI が `ai/`（必要に応じて B の `.claude/skills/` 等）を編集
2. `npm run lint` および変更種別に応じた `*:check` を実行
3. ユーザーが `./scripts/sync-all-to-home.sh`（または個別 `sync-*-to-home.sh`）を実行
4. 各スクリプトが対象パスを `*.bak.{YYYYMMDD-HHMMSS}` に退避してから上書き — `scripts/README.md` L9
5. 各 AI ツール側で動作確認

**同期順序**（`sync-all-to-home.sh`）: claude → cursor → codex → windsurf → antigravity → geminicli — `scripts/sync-all-to-home.sh` L30–50 付近

### 検証フロー

| コマンド               | 検証対象                                                                                      | 根拠                           |
| ---------------------- | --------------------------------------------------------------------------------------------- | ------------------------------ |
| `npm run check`        | Prettier + markdownlint + yamllint + JSON + 埋め込み schema                                   | `package.json` L7、`format.sh` |
| `npm run agent:check`  | skills / global-skills / description / claude-agents / cursor-agents / codex-wiring / routing | `package.json` L26             |
| `npm run schema:check` | `ai/**/*profile*.json`、`notes/*.json`                                                        | `package.json` L18             |

## 状態遷移

| 状態                         | 遷移                                                   | 実行者                                    |
| ---------------------------- | ------------------------------------------------------ | ----------------------------------------- |
| テンプレート編集済み・未同期 | `sync-*-to-home.sh` 実行                               | ユーザー（AI は明示依頼なしに実行しない） |
| ホーム配下が旧版             | 退避（`.bak.*`）後に上書き                             | sync スクリプト                           |
| MCP 設定                     | デフォルト **コピーしない** → `--include-mcp` で含める | `scripts/README.md` L10                   |
| 検証失敗                     | コミット前に `lint:staged`（pre-commit）または手動修正 | `.husky/pre-commit`                       |

## 認可境界

| 境界               | 内容                                                  | 根拠                                                 |
| ------------------ | ----------------------------------------------------- | ---------------------------------------------------- |
| 秘密情報           | `.env` `.env.*` は gitignore。CI で Gitleaks スキャン | `.gitignore` L4–5、`.github/workflows/ci.yml` L28–31 |
| MCP / 認証ファイル | 同期デフォルト除外。`--include-mcp` 時のみ            | `scripts/README.md` L10–11                           |
| ホームディレクトリ | AI の自律編集対象外（C 区分）                         | `AGENTS.md` L51                                      |
| 同期スクリプト     | アーキテクチャ上バイパス禁止と明記                    | `CLAUDE.md`「アーキテクチャ不変条件」                |

## 外部システムとの接続点

| 接続先                          | 用途                           | 根拠                                       |
| ------------------------------- | ------------------------------ | ------------------------------------------ |
| GitHub Actions                  | PR/push で lint + Gitleaks     | `.github/workflows/ci.yml`                 |
| `anthropics/claude-code-action` | `@claude` コメントトリガー     | `.github/workflows/claude.yml`             |
| Claude Code review plugin       | PR 自動レビュー                | `.github/workflows/claude-code-review.yml` |
| ユーザーホーム `~/.claude` 等   | テンプレート配布先             | `scripts/README.md`                        |
| Python CLI                      | `check-jsonschema`、`yamllint` | `package.json` L18、`format.sh` L64–65     |
| npm / Node                      | 検証スクリプト実行             | `package.json` `engines.node >=20.17.0`    |

## 変更時に壊れやすい結合点

| 結合点                                                      | リスク                                                                             | 根拠                                                                                             |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Codex agent TOML ↔ config 参照                              | orphan / dangling で `codex-wiring:check` 失敗                                     | 本セッション `npm run agent:check` 出力                                                          |
| Claude / Cursor / Codex の agent 名・description            | プラットフォーム間ドリフト                                                         | `.claude/agents/` 11 件、`.cursor/agents/` 9 件、`.codex/agents/` 9 件（本セッション `ls` 確認） |
| Skill ミラー                                                | `.windsurf/skills/` `.agent/skills/` `.agents/skills/` が `.claude/skills/` と乖離 | `README.md` L36–37、ディレクトリ実在                                                             |
| レビュールーティング                                        | 必須ファイル欠落・トリガー文言 `レビューしてください` 欠如で `routing:check` 失敗  | `scripts/validate-routing.mjs` L7–15, L33–35                                                     |
| Skill frontmatter                                           | `description` に未クォートの `: ` で YAML エラー                                   | `README.md` L94–96                                                                               |
| `ai/common/global/AGENTS.md` 変更                           | 複数ツールのグローバルルールに波及                                                 | `scripts/README.md` L12                                                                          |
| グローバル skill（`ai/claude_code/global/.claude/skills/`） | 配布先全体に影響                                                                   | `README.md` L35                                                                                  |

## 実コードまたはテストで保証されている不変条件

### `.claude/skills/*/SKILL.md`（`scripts/validate-skills.mjs`）

- frontmatter は `name` と `description` のみ
- `description` は 3 要素形式（When NOT to use、Trigger Keywords 必須）
- 必須見出し: When to use / When NOT to use / Trigger Keywords / Procedure / Output Contract / Examples
- Procedure 4–6 ステップ、Examples ちょうど 3、NG 例 3–5、500 行以下
- 本セッション: **20 ファイル合格**（`npm run skills:check`）

### グローバル skill（`scripts/validate-global-skills.mjs`）

- `ai/claude_code/global/.claude/skills/` 配下。`markdown-line-length` はルール専用例外
- 本セッション: **11 ファイル合格**

### Claude agents（`scripts/validate-claude-agents.mjs`）

- frontmatter フィールド・許可色・必須見出し — 本セッション合格

### Cursor agents（`scripts/validate-cursor-agents.mjs`）

- 許可キーのみ: `name`, `description`, `model`, `readonly` — 本セッション合格

### Codex 配線（`check-codex-wiring.mjs`）

- orphan / dangling 参照なし — 本セッション PASS（9 agents）

### ルーティング（`scripts/validate-routing.mjs`）

- `CLAUDE.md`, `.claude/CLAUDE.md`, review 関連ファイル等の存在
- 自然言語トリガー `レビューしてください` の存在 — 本セッション 3 ファイル合格

### Pre-commit

- ステージ済みファイルに Prettier + markdownlint — `.husky/pre-commit` → `npm run lint:staged`

## 文書と実装が食い違う箇所

| 文書の記述                                                      | 実態                                                                                    | 根拠                                                  |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| README「検証: `npm run lint` / `schema:check` / `agent:check`」 | CI は `npm run check` のみ（`agent:check` 未実行）                                      | `.github/workflows/ci.yml` L27、`README.md` L66–69    |
| `ai/README.md` 最終更新 2025-10-21                              | 以降の大規模刷新あり（例: `3b66230 chore: AI 設定を全面刷新`）                          | `ai/README.md` L7、`git log`                          |
| README に `.work/` をディレクトリ概要として記載                 | `.work/` は `.gitignore` で Git 管理外                                                  | `README.md` L28、`.gitignore` L13                     |
| `engines.node >=20.17.0`                                        | CI は Node 22 を使用                                                                    | `package.json` L37–38、`.github/workflows/ci.yml` L18 |
| 全プラットフォームで agent 数が揃う想定に見える運用             | Claude 11 / Cursor 9 / Codex 9（`codebase-explorer`, `tech-researcher` は Claude のみ） | 本セッション `ls` カウント                            |

## 暗黙知だがコード・テスト・CI に強制されていないルール

| ルール                                                  | 出典                                                                           | 強制の有無                   |
| ------------------------------------------------------- | ------------------------------------------------------------------------------ | ---------------------------- |
| テンプレート（A）を B / C に逆流コピーしない            | `AGENTS.md`「エージェントが守ること」                                          | 検証なし                     |
| Skill 本文をルーターに複製しない                        | `CLAUDE.md`「プロジェクト固有ルール」、`.claude/CLAUDE.md`「Canonical Source」 | 検証なし                     |
| グローバル配布資産はツール中立にする                    | `CLAUDE.md`「プロジェクト固有ルール」                                          | 検証なし（手動レビュー依存） |
| 同期スクリプトはユーザー明示依頼時のみ AI が実行        | `AGENTS.md`「エージェントが守ること」                                          | 検証なし                     |
| 完了前に `format-lint-audit` スキルで品質ゲート         | `.claude/CLAUDE.md`「Routing Policy」                                          | スキル記述のみ               |
| `.work/AI_SCAN.md` / `AI_BLUEPRINT.md` は作業中間成果物 | `snippets/skill-agent-creator/` 参照、`.gitignore`                             | Git 管理外                   |

## 新しい開発者または AI が作業前に読むべきファイル

| 順序 | ファイル                                                   | 理由                          |
| ---- | ---------------------------------------------------------- | ----------------------------- |
| 1    | 本ファイル `docs/ai/PROJECT_REALITY_MAP.md`                | 実態の地図                    |
| 2    | `docs/ai/AI_OPERATING_GUIDE.md`                            | 作業フローと禁止事項          |
| 3    | `AGENTS.md` または `CLAUDE.md`                             | 編集境界・ハード制約          |
| 4    | `README.md`                                                | 同期コマンド・日常運用        |
| 5    | 作業種別に応じて `ai/README.md` または `scripts/README.md` | テンプレ設計 / 同期マッピング |
| 6    | `docs/ai/lessons/`                                         | 確認済みの落とし穴            |

## 現時点で不明なこと

| 不明点                                                                                       | 確認方法                                                             |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| 6 つの sync スクリプトが Linux / Windows 環境で同等に動作するか                              | 各 OS で `./scripts/sync-*-to-home.sh --help` とドライラン相当の確認 |
| Skill ミラー（`.windsurf/` `.agent/` `.agents/`）が常に `.claude/skills/` と同期されているか | `diff -r` またはリポジトリの更新手順の文書化状況を確認               |
| `claude.yml` / `claude-code-review.yml` が fork PR で正常動作するか                          | 実際の PR で Actions ログを確認                                      |
| `npm run check` 失敗時に CI が落ちるか（ローカル suggestions 問題は CI 非該当の可能性）      | CI ログと `.prettierignore` の対象範囲を比較                         |
| 配布先 repo でテンプレートを手動コピーした場合のドリフト検知                                 | 未実装 — 必要なら検証スクリプト追加を検討                            |

## 修正候補（本タスクでは未実施）

| 候補                                                         | 根拠                                                                        |
| ------------------------------------------------------------ | --------------------------------------------------------------------------- |
| CI に `npm run agent:check` を追加                           | README は agent:check を推奨するが CI 未実行                                |
| `.prettierignore` に `.claude/suggestions/` を追加           | gitignore 済みだが Prettier 対象のためローカル `npm run check` が失敗しうる |
| Claude 専用 agent 2 件の Cursor/Codex への意図的除外を文書化 | agent 数不一致                                                              |
