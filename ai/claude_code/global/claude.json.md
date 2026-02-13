<!--
macOS/Linux: ~/claude.json
Windows: %USERPROFILE%\claude.json
-->
<!--
  注意:
  - filesystemは脆弱性修正版(≥0.6.4)を必須、serenaは企業非推奨／個人は強ハードニング下のみ。
  - Claude Code の MCP 設定ファイルです
  - [参照を許可するパス] などは実際の絶対パスに置き換えてください
  - GitHub PATとNotion Tokenは実際の値に置き換えてください
  - 各サーバーには "type": "stdio" が必要です
-->

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PAT}"
      }
    },
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "exa": {
      "type": "http",
      "url": "https://mcp.exa.ai/mcp"
    },
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "drawio": {
      "command": "npx",
      "args": ["-y", "@drawio/mcp"]
    }
  }
}
```
