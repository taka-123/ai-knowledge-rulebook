# Platform Field Map

| Platform | Required Frontmatter/Keys | Forbidden or Unsupported |
| --- | --- | --- |
| Claude | `name`, `description`, `color`, `tools`, `disallowedTools`, `model`, `memory` | なし |
| Cursor | `name`, `description`, `model`, `readonly?(reviewer)` | `color`, `tools`, `disallowedTools`, `memory` |
| Codex TOML | `description`, `developer_instructions`, `model`, `approval_policy`, `sandbox_mode?(reviewer)` | Markdown frontmatter |

## Sync Rule

1. description の canonical は Claude 版。
2. Cursor/Codex は Claude 版 description を同期反映する。
3. Body は Claude と Cursor を一致、Codex は `developer_instructions` へ変換する。
