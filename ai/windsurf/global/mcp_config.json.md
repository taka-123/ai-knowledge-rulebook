<!--
macOS/Linux: ~/.codeium/windsurf/mcp_config.json
Windows: %APPDATA%\Codeium\windsurf\mcp_config.json
-->
<!--
  注意:
  - Windsurf の 100 ツール制限を回避するため mcp-hub-mcp を使用しています
  - 実際の MCP サーバー定義は ~/.codeium/windsurf/mcp-hub-mcp.json に記載
  - mcp-hub-mcp が全ての MCP サーバーを統合管理します
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
