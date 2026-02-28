# Codex Wiring Rules

## Scope

- 対象は `.codex/agents/*.toml`, `.codex/config.toml`, `.codex/config.preset.*.toml`。
- `config_file` は `./.codex/agents/<name>.toml` 形式で統一する。

## Quality Gate

1. Orphan 0 件（agent 実体がどの config にも載っていない状態を禁止）。
2. Dangling 0 件（config_file 参照先が実在しない状態を禁止）。
3. reviewer 系 agent は `sandbox_mode = "read-only"` を必須にする。
4. Fixer/Generator 系は `sandbox_mode` を省略し、親 config の `workspace-write` を継承する。

## Preset Rule

- role 枠を超える場合は `config.preset.*.toml` で用途分割する。
- `use-preset.sh` で `config.toml` を置換し、運用を一本化する。
