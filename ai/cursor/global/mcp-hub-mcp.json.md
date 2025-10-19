<!--
macOS/Linux: ~/.cursor/mcp-hub-mcp.json
Windows: %USERPROFILE%\.cursor\mcp-hub-mcp.json
-->
<!--
  注意:
  - filesystemは脆弱性修正版(≥0.6.4)を必須、serenaは企業非推奨／個人は強ハードニング下のみ。
  - このファイルは mcp-hub-mcp が管理する実際のMCPサーバー定義です
  - [参照を許可するパス] などは実際の値に置き換えてください
  - 環境変数は ${env:VARIABLE_NAME} 形式で参照可能です
-->

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "serena": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/oraios/serena",
        "serena",
        "start-mcp-server",
        "--context",
        "ide-assistant",
        "--enable-web-dashboard",
        "false"
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
      "args": ["-y", "@playwright/mcp@latest"]
    },
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest", "--isolated=true"]
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "$[ここに自身のNotion Integration Tokenを入れる]"
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
