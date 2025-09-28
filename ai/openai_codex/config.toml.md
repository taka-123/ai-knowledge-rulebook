<!-- ~/.codex/config.toml -->

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

[mcp_servers.playwright]
command = "npx"
args = ["@playwright/mcp@latest"]

```
