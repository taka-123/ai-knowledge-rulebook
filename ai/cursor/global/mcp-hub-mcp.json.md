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
    }
  }
}
```
