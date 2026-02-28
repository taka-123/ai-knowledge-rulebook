# scripts/

プロジェクト内の AI ツール設定をホームディレクトリへ同期するスクリプト群。

## sync-\*-to-home.sh の仕組み

### 共通ルール

- **退避**: 既存のディレクトリ/ファイルがある場合、`{パス}.bak.{YYYYMMDD-HHMMSS}` に退避してから上書き
- **MCP 設定**: デフォルトではコピー・退避しない（認証情報を含むため）。`--include-mcp` で含める
- **実行場所**: プロジェクト内のどこから実行しても、`scripts/` からの相対パスで正しく動作

### 各スクリプト

| スクリプト               | コピー元                                  | コピー先                                     | MCP 対象                   |
| ------------------------ | ----------------------------------------- | -------------------------------------------- | -------------------------- |
| sync-claude-to-home.sh   | ai/claude_code/global                     | ~/.claude                                    | claude.json                |
| sync-claude-to-home.sh   | ai/claude_code/claude.json                | ~/.claude.json                               | （同上）                   |
| sync-cursor-to-home.sh   | ai/cursor/global/agents                   | ~/.cursor/agents                             | mcp.json                   |
| sync-cursor-to-home.sh   | ai/cursor/global/mcp.json                 | ~/.cursor/mcp.json                           | （同上）                   |
| sync-codex-to-home.sh    | ai/openai_codex/global                    | ~/.codex                                     | （config.toml に注意表示） |
| sync-codex-to-home.sh    | ai/common/global/AGENTS.md                | ~/.codex/AGENTS.md                           | -                          |
| sync-windsurf-to-home.sh | ai/windsurf/global/mcp_config.json        | ~/.codeium/windsurf/mcp_config.json          | mcp_config.json            |
| sync-windsurf-to-home.sh | ai/common/global/AGENTS.md                | ~/.codeium/windsurf/memories/global_rules.md | -                          |
| sync-gemini-to-home.sh   | ai/antigravity/gemini/.../mcp_config.json | ~/.gemini/antigravity/mcp_config.json        | mcp_config.json            |

### sync-all-to-home.sh（総合版）

5 つの sync スクリプトを順に実行する。`--include-mcp` を渡すと各スクリプトにそのまま引き継ぐ。

```bash
# デフォルト（MCP スキップ）
./scripts/sync-all-to-home.sh

# MCP も含める
./scripts/sync-all-to-home.sh --include-mcp
```

完了後、skills の共通化ワンライナーを案内する（~/.claude/skills を他ツールからシンボリックリンクで参照）。

### 補足

- **sync-codex**: config.toml の [mcp_servers.*] にプレースホルダーがある場合、注意を表示
- **sync-claude**: 完了後に ai/claude_code/claude.json の MCP 設定を ~/.claude.json へ手動で反映する案内を表示
- **sync-cursor**: 完了後に ai/common/global/AGENTS.md を User Rule として設定する案内を表示
