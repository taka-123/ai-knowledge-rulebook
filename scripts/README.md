# scripts/

プロジェクト内の AI ツール設定をホームディレクトリへ同期するスクリプト群。

## sync-\*-to-home.sh の仕組み

### 共通ルール

- **退避**: コピー対象のサブディレクトリ/ファイル単位で `{パス}.bak.{YYYYMMDD-HHMMSS}` に退避してから上書き（親ディレクトリ丸ごとではなく、対象項目のみ退避）
- **MCP 設定**: デフォルトではコピー・退避しない（認証情報を含むため）。`--include-mcp` で含める
- **実行場所**: プロジェクト内のどこから実行しても、`scripts/` からの相対パスで正しく動作
- **グローバルルール**: `ai/common/global/AGENTS.md` が各ツール向けグローバルルールの単一ソース

### ソースディレクトリ構造

各ツールの `global/` 以下はホームディレクトリのドットディレクトリ構造をミラーしている。

```text
ai/claude_code/global/.claude/      → ~/.claude/
ai/claude_code/global/CLAUDE.md     → ~/.claude/CLAUDE.md
ai/claude_code/global/claude.json   → ~/.claude.json        (--include-mcp)
ai/cursor/global/.cursor/           → ~/.cursor/
ai/openai_codex/global/.codex/      → ~/.codex/
ai/windsurf/global/.codeium/        → ~/.codeium/
ai/antigravity/global/.gemini/      → ~/.gemini/
ai/gemini_cli/global/.gemini/       → ~/.gemini/
ai/common/global/AGENTS.md          → 各ツールのグローバルルールファイル
```

### 各スクリプト

#### sync-claude-to-home.sh

| コピー元                                | コピー先              | 備考                           |
| --------------------------------------- | --------------------- | ------------------------------ |
| `ai/claude_code/global/CLAUDE.md`       | `~/.claude/CLAUDE.md` | -                              |
| `ai/claude_code/global/.claude/` 内各項 | `~/.claude/` 内対応先 | サブディレクトリ・ファイル個別 |
| `ai/claude_code/global/claude.json`     | `~/.claude.json`      | `--include-mcp` 時のみ         |

- `.claude/` 内のサブディレクトリ（hooks/ 等）とファイル（settings.json 等）を個別に退避・コピー
- ユーザーデータ（plans/, memory/ 等）はソースに存在しないため保持される

#### sync-cursor-to-home.sh

| コピー元                            | コピー先             | 備考                   |
| ----------------------------------- | -------------------- | ---------------------- |
| `ai/cursor/global/.cursor/agents/`  | `~/.cursor/agents/`  | ディレクトリ単位で退避 |
| `ai/cursor/global/.cursor/mcp.json` | `~/.cursor/mcp.json` | `--include-mcp` 時のみ |

- 完了後に `ai/common/global/AGENTS.md` を Cursor の User Rule として手動設定する案内を表示

#### sync-codex-to-home.sh

| コピー元                                | コピー先             | 備考                           |
| --------------------------------------- | -------------------- | ------------------------------ |
| `ai/common/global/AGENTS.md`            | `~/.codex/AGENTS.md` | 常にコピー                     |
| `ai/openai_codex/global/.codex/` 内各項 | `~/.codex/` 内対応先 | サブディレクトリ・ファイル個別 |

- `.codex/` 内のサブディレクトリ（agents/, prompts/, rules/ 等）とファイル（config.toml 等）を個別に退避・コピー
- ユーザーデータ（sessions/, history.jsonl 等）は保持される
- config.toml の `[mcp_servers.*]` にプレースホルダーがある場合、注意を表示

#### sync-windsurf-to-home.sh

| コピー元                                               | コピー先                                       | 備考                   |
| ------------------------------------------------------ | ---------------------------------------------- | ---------------------- |
| `ai/common/global/AGENTS.md`                           | `~/.codeium/windsurf/memories/global_rules.md` | 常にコピー             |
| `ai/windsurf/global/.codeium/windsurf/mcp_config.json` | `~/.codeium/windsurf/mcp_config.json`          | `--include-mcp` 時のみ |

#### sync-antigravity-to-home.sh

| コピー元                                                    | コピー先                                | 備考                   |
| ----------------------------------------------------------- | --------------------------------------- | ---------------------- |
| `ai/common/global/AGENTS.md`                                | `~/.gemini/GEMINI.md`                   | 常にコピー             |
| `ai/antigravity/global/.gemini/antigravity/mcp_config.json` | `~/.gemini/antigravity/mcp_config.json` | `--include-mcp` 時のみ |

#### sync-geminicli-to-home.sh

| コピー元                                     | コピー先                  | 備考             |
| -------------------------------------------- | ------------------------- | ---------------- |
| `ai/common/global/AGENTS.md`                 | `~/.gemini/GEMINI.md`     | 常にコピー       |
| `ai/gemini_cli/global/.gemini/settings.json` | `~/.gemini/settings.json` | 存在する場合のみ |

- `--include-mcp` オプションなし（MCP 設定は antigravity 側で管理）

### sync-all-to-home.sh（総合版）

6 つの sync スクリプトを順に実行する。`--include-mcp` を渡すと各スクリプトにそのまま引き継ぐ。

```bash
# デフォルト（MCP スキップ）
./scripts/sync-all-to-home.sh

# MCP も含める
./scripts/sync-all-to-home.sh --include-mcp
```

実行順: claude → cursor → codex → windsurf → antigravity → geminicli

完了後、skills の共通化ワンライナーを案内する（~/.claude/skills を他ツールからシンボリックリンクで参照）。

### AGENTS.md ルーティング一覧

`ai/common/global/AGENTS.md` は各ツールのグローバルルールとして以下にコピーされる。

| ツール      | コピー先                                       | 方法         |
| ----------- | ---------------------------------------------- | ------------ |
| Codex       | `~/.codex/AGENTS.md`                           | 自動コピー   |
| Windsurf    | `~/.codeium/windsurf/memories/global_rules.md` | 自動コピー   |
| Antigravity | `~/.gemini/GEMINI.md`                          | 自動コピー   |
| Gemini CLI  | `~/.gemini/GEMINI.md`                          | 自動コピー   |
| Cursor      | User Rule として手動設定                       | 案内を表示   |
| Claude Code | `~/.claude/CLAUDE.md`（専用ファイル）          | 別ソースから |

※ Claude Code は `ai/claude_code/global/CLAUDE.md` を `~/.claude/CLAUDE.md` へコピーする（AGENTS.md ではない）。
