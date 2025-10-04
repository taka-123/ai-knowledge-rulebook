<!-- ~/.codeium/windsurf/mcp-hub-mcp.json -->
<!--
  注意:
  - このファイルは mcp-hub が管理する実際のMCPサーバー定義です
  - Windsurf の 100 ツール制限を回避するため mcp-hub-mcp を使用しています
  - [参照を許可するパス] などは実際の値に置き換えてください
  - Apple Silicon (ARM64) 環境で serena を動作させるため arch -arm64 を使用
  - 環境変数は各自で設定してください（GitHub PAT, Notion Token など）
-->

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": [
        "-y",
        "@upstash/context7-mcp@latest"
      ]
    },
    "serena": {
      "command": "arch",
      "args": [
        "-arm64",
        "uvx",
        "--from",
        "git+https://github.com/oraios/serena",
        "serena",
        "start-mcp-server",
        "--context",
        "ide-assistant"
      ]
    },
    "github": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "[ここに自身のGitHub PATを入れる]"
      }
    },
    "playwright": {
      "command": "npx",
      "args": [
        "-y",
        "@playwright/mcp@latest"
      ]
    },
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--isolated=true"
      ]
    },
    "notion": {
      "command": "npx",
      "args": [
        "-y",
        "@notionhq/notion-mcp-server"
      ],
      "env": {
        "NOTION_TOKEN": "[ここに自身のNotion Integration Tokenを入れる]"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "[参照を許可するパス1]",
        "[参照を許可するパス2]"
      ]
    }
  }
}
```
