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
    // serena, filesystem, github はセキュリティや必要性の観点から除外
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "env": {}
    },
    "chrome-devtools": {
      "type": "stdio",
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"],
      "env": {}
    },
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"],
      "env": {}
    },
    "notion": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "[ここに自身のNotion Integration Tokenを入れる]"
      }
    },
    "codex": {
      "type": "stdio",
      "command": "[which codex の結果]",
      "args": ["mcp-server"],
      "env": {}
    }
  }
}
```
