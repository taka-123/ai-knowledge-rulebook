<!-- ~/claude.json -->

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "--root",
        "/Users/tf/work"
      ],
      "env": {}
    },
    "context7": {
      "args": [
        "-y",
        "@upstash/context7-mcp@latest"
      ],
      "command": "npx",
      "env": {},
      "type": "stdio"
    },
    "serena": {
      "type": "stdio",
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
      ],
      "env": {}
    },
    "playwright": {
      "args": [
        "-y",
        "@playwright/mcp@latest"
      ],
      "command": "npx",
      "env": {},
      "type": "stdio"
    }
  }
}

```
