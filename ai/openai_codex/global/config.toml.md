<!--
  注意:
  - filesystemは脆弱性修正版(≥0.6.4)を必須、serenaは企業非推奨／個人は強ハードニング下のみ。
  - OpenAI Codex の設定ファイルです
  - [参照を許可するパス] などは実際の絶対パスに置き換えてください
  - GitHub PATとNotion Tokenは実際の値に置き換えてください
  - セキュリティのため、環境変数の使用を推奨します
-->

```toml
# ~/.codex/config.toml

## デフォルトモデル
model = "gpt-5.3-codex"

## 推論コストと安定性のバランス。重いタスク時は都度 /model か --model_reasoning_effort で上げる運用が無難
model_reasoning_effort = "high"

## 常用する安全ライン（“実行責任付きAI”として使う前提）
sandbox_mode = "workspace-write"

## 必要なときだけ参照する想定。プロジェクトでは disabled に落とすことが多い
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

```
