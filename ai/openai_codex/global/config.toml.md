<!-- ~/.codex/config.toml に記載 -->

```toml
## デフォルトモデル
model = "gpt-5.3-codex"
model_reasoning_effort = "high"

## 安全寄りのデフォルト
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"

## 通知音
notify = ["bash", "-lc", "afplay /System/Library/Sounds/Glass.aiff"]

## MCPサーバー
[mcp_servers.openaiDeveloperDocs]
url = "https://developers.openai.com/mcp"

[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

[mcp_servers.github]
url = "https://api.githubcopilot.com/mcp/"
bearer_token_env_var = "GITHUB_PAT"

[mcp_servers.playwright]
command = "npx"
args = ["@playwright/mcp@latest"]

[mcp_servers.drawio]
command = "npx"
args = ["-y", "@drawio/mcp"]

# マルチエージェント
[features]
multi_agent = true

[agents]
max_threads = 6

## 役割（role）:
[agents.default]
description = "汎用実装・修正 / General purpose coding helper."

[agents.explorer]
description = "探索・読解特化 / Fast read-heavy exploration."
config_file = "agents/explorer.toml"

[agents.reviewer]
description = "品質レビュー（安全性・正しさ・保守性） / Review for correctness & maintainability."
config_file = "agents/reviewer.toml"

[agents.test_runner]
description = "テスト実行と失敗収束 / Run tests and fix failures."
config_file = "agents/test_runner.toml"

[agents.security_reviewer]
description = "セキュリティ監査 / Security review for code and config."
config_file = "agents/security_reviewer.toml"

[sandbox_workspace_write]
network_access = true
```
