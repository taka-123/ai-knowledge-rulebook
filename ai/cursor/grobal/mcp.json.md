<!-- ~/.cursor/mcp.json -->
<!--
  注意:
  - Cursor IDE はツール数上限(80個)があるため、mcp-hub-mcp を使用します
  - 実際のMCPサーバー定義は ~/.cursor/mcp-hub-mcp.json に記載してください
  - 環境変数(GITHUB_PERSONAL_ACCESS_TOKEN, NOTION_TOKEN)はシステム環境変数に設定してください
-->

```json
{
  "mcpServers": {
    "mcp-hub": {
      "command": "npx",
      "args": ["-y", "mcp-hub-mcp@latest", "~/.cursor/mcp-hub-mcp.json"]
    }
  }
}

```
