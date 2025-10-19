<!--
  注意:
  - filesystemは脆弱性修正版(≥0.6.4)を必須、serenaは企業非推奨／個人は強ハードニング下のみ。
  - OpenAI Codex の設定ファイルです
  - [参照を許可するパス] などは実際の絶対パスに置き換えてください
  - GitHub PATとNotion Tokenは実際の値に置き換えてください
  - セキュリティのため、環境変数の使用を推奨します
-->

```toml
notify = ["bash", "-lc", "afplay /System/Library/Sounds/Glass.aiff"]

model = "gpt-5-codex"
model_reasoning_effort = "high"
sandbox_mode = "workspace-write"
approval_policy = "on-request"

[tools]
web_search = true

[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp@latest"]

[mcp_servers.serena]
command = "uvx"
args = ["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "codex"]

[mcp_servers.github]
command = "docker"
args = ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"]
env = { GITHUB_PERSONAL_ACCESS_TOKEN = "[ここに自身のGitHub PATを入れる]" }

[mcp_servers.playwright]
command = "npx"
args = ["-y", "@playwright/mcp@latest"]

[mcp_servers.chrome-devtools]
command = "npx"
args = ["chrome-devtools-mcp@latest", "--isolated=true"]

[mcp_servers.notion]
command = "npx"
args = ["-y", "@notionhq/notion-mcp-server"]
env = { NOTION_TOKEN = "[ここに自身のNotion Integration Tokenを入れる]" }

[mcp_servers.filesystem]
command = "npx"
args = [
  "-y",
  "@modelcontextprotocol/server-filesystem",
  "[参照を許可するパス1]",
  "[参照を許可するパス2]"
]

```
