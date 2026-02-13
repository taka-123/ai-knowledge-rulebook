<!--
macOS/Linux: ~/.cursor/mcp.json
Windows: %USERPROFILE%\.cursor\mcp.json
-->
<!--
  注意:
  - Cursor IDE はツール数上限(80個)があるため、mcp-hub-mcp を使用します
  - 実際のMCPサーバー定義は ~/.cursor/mcp-hub-mcp.json に記載してください
  - 環境変数(GITHUB_PERSONAL_ACCESS_TOKEN, NOTION_TOKEN)はシステム環境変数に設定してください
-->

```json
{
  "mcpServers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer <PLACEHOLDER_GITHUB_PAT>"
      }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "exa": {
      "url": "https://mcp.exa.ai/mcp"
    },
    "playwright": {
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
