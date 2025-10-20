<!--
macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
Linux: ~/.config/Claude/claude_desktop_config.json
-->
<!--
  注意:
  - [参照を許可するパス1] などのプレースホルダーは実際のパスに置き換えてください
  - 例: "/Users/username/Desktop", "/Users/username/Documents" など絶対パスで指定
  - チルダ(~)は使用できません
-->

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
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
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
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
