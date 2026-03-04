# ai-knowledge-rulebook

AI エージェント設定・運用ルール・学習ノートを管理するリポジトリです。

## 最重要ルール（先にここだけ）

- Canonical Source（正本）は `./ai/` 配下です。
- `~/.claude` `~/.cursor` `~/.codex` `~/.gemini` `~/.codeium` は配布先です。
- 配布先を直接編集せず、`./ai/` を編集して `./scripts/sync-*-to-home.sh` で反映します。

## このリポジトリで管理しているもの

- AI ツール別のグローバル設定テンプレート
- 共通ルール（`AGENTS.md` など）
- スキル/エージェント定義
- ノート・スニペット・検証スクリプト

## ディレクトリ概要

| Path              | 役割                                     |
| ----------------- | ---------------------------------------- |
| `ai/`             | 正本。各ツール向け設定のソース           |
| `scripts/`        | `ai/` からホーム配下へ同期するスクリプト |
| `.claude/skills/` | リポジトリ内で使う Skill 定義            |
| `notes/`          | 学習ノート                               |
| `snippets/`       | テンプレート/雛形                        |
| `schemas/`        | JSON Schema                              |
| `.work/`          | 作業用ドキュメント                       |

## `ai/` 配下の考え方

- `ai/<tool>/global/` は各ツールのグローバル設定ソースです。
- `ai/<tool>/project/` はプロジェクト単位の設定雛形です。
- `ai/common/global/AGENTS.md` は複数ツールで共有する共通ルールです。
- `ai/claude_code/global/.claude/skills` は Claude Code 側の canonical skill ソースです。

## 同期コマンド（canonical -> home）

| 対象         | 実行コマンド                            |
| ------------ | --------------------------------------- |
| 全ツール一括 | `./scripts/sync-all-to-home.sh`         |
| Claude Code  | `./scripts/sync-claude-to-home.sh`      |
| Cursor       | `./scripts/sync-cursor-to-home.sh`      |
| Codex        | `./scripts/sync-codex-to-home.sh`       |
| Windsurf     | `./scripts/sync-windsurf-to-home.sh`    |
| Gemini CLI   | `./scripts/sync-geminicli-to-home.sh`   |
| Antigravity  | `./scripts/sync-antigravity-to-home.sh` |

MCP/認証系ファイルも同期する場合は `--include-mcp` を付けます。

```bash
./scripts/sync-all-to-home.sh --include-mcp
```

## セットアップ

```bash
npm install
pip install check-jsonschema yamllint
```

## 検証コマンド

```bash
npm run lint
npm run schema:check
npm run agent:check
```

個別チェックを行う場合:

```bash
npm run skills:check
npm run global-skills:check
npm run claude-agents:check
npm run cursor-agents:check
npm run codex-wiring:check
npm run routing:check
```

## 日常運用フロー

1. `./ai/`（必要に応じて `.claude/skills/` など）を編集する。
2. `npm run lint` と必要な検証コマンドを実行する。
3. `./scripts/sync-all-to-home.sh` でホーム配下へ同期する。
4. 各ツール側で起動確認する。

## トラブルシュート

- `MCP client for github failed to start: GITHUB_PAT ... is not set`
  - `GITHUB_PAT` 未設定が原因です。環境変数を設定してから再起動してください。
- `invalid YAML: mapping values are not allowed in this context`
  - `SKILL.md` frontmatter の `description` が未クォートで `: ` を含むと発生します。
  - `description: "..."` もしくは `description: |` を使ってください。

## セキュリティ

- API キーや個人情報をコミットしないでください。
- 認証情報を含むファイルは `--include-mcp` 利用時のみ扱ってください。
- 共有時はプレースホルダー（例: `<API_KEY>`）へ置換してください。

## ライセンス

MIT License（`LICENSE` を参照）。
