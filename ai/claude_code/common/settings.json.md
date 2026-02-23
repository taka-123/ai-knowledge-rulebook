<!-- 下記 1-4（優先度順）で利用可能 -->
<!-- 1. (managed-settings.json) -->
<!--    macOS: /Library/Application Support/ClaudeCode/managed-settings.json -->
<!--    Windows: C:\Program Files\ClaudeCode\managed-settings.json -->
<!--    Linux: /etc/claude-code/managed-settings.json -->
<!-- 2. ./.claude/settings.json -->
<!-- 3. ./.claude/settings.local.json -->
<!-- 4. (settings.json) -->
<!--    macOS/Linux: ~/.claude/settings.json -->
<!--    Windows: %USERPROFILE%\.claude\settings.json -->

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "cleanupPeriodDays": 30,
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "0",
    "DISABLE_TELEMETRY": "1"
  },
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "allowUnsandboxedCommands": false,
    "excludedCommands": ["docker", "docker-compose", "docker compose"],
    "network": {
      "allowedDomains": [
        "github.com",
        "api.github.com",
        "registry.npmjs.org",
        "*.npmjs.org",
        "pypi.org",
        "files.pythonhosted.org",
        "*.rds.amazonaws.com",
        "*.bing.com"
      ]
    }
  },
  "permissions": {
    "defaultMode": "acceptEdits",
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Read(**/.env)",
      "Read(**/.env.*)",
      "Edit(.env)",
      "Edit(.env.*)",
      "Edit(**/.env)",
      "Edit(**/.env.*)",
      "Write(.env)",
      "Write(.env.*)",
      "Write(**/.env)",
      "Write(**/.env.*)",
      "Read(secrets/**)",
      "Read(**/secrets/**)",
      "Edit(secrets/**)",
      "Edit(**/secrets/**)",
      "Write(secrets/**)",
      "Write(**/secrets/**)",
      "Read(~/.ssh/**)",
      "Write(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Write(~/.aws/**)",
      "Read(~/.gcp/**)",
      "Write(~/.gcp/**)",
      "Read(**/*.pem)",
      "Read(**/*.key)",
      "Bash(curl *)",
      "Bash(wget *)",
      "Bash(rm *)",
      "Bash(sudo *)",
      "Bash(ssh *)",
      "Bash(scp *)",
      "Bash(aws *)",
      "Bash(terraform *)",
      "Bash(kubectl *)",
      "Bash(git push --force *)",
      "Bash(git push -f *)",
      "Bash(git reset --hard *)",
      "Bash(git clean -fdx *)"
    ],
    "ask": [
      "Bash(git push *)",
      "Bash(git checkout *)",
      "Bash(git merge *)",
      "Bash(psql *)",
      "Bash(mysql *)",
      "Bash(docker compose *)",
      "Bash(docker-compose *)"
    ],
    "allow": [
      "WebSearch",
      "WebFetch(domain:code.claude.com)",
      "WebFetch(domain:docs.claude.com)",
      "WebFetch(domain:github.com)",
      "WebFetch(domain:api.github.com)",
      "WebFetch(domain:registry.npmjs.org)",
      "WebFetch(domain:pypi.org)",
      "Read(./**)",
      "Edit(./**)",
      "Write(./**)",
      "Grep(**)",
      "Glob(**)",
      "Bash(ls *)",
      "Bash(pwd)",
      "Bash(whoami)",
      "Bash(which *)",
      "Bash(node *)",
      "Bash(npm *)",
      "Bash(yarn *)",
      "Bash(pnpm *)",
      "Bash(python *)",
      "Bash(pytest *)",
      "Bash(make *)",
      "Bash(git status *)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(git pull)",
      "Bash(git branch *)",
      "Bash(trash *)",
      "Bash(gomi *)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r 'if .tool_input.command | test(\"rm -rf|dd if=|:(\\\\)\\\\{ :\\\\|:& \\\\};:\") then {\"decision\": \"block\", \"reason\": \"危険なコマンドは実行できません\"} else empty end'"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"[$(date)] $USER: $(jq -r '.tool_input.command')\" >> ~/.claude/command_history.log"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo '✅ 変更完了'"
          }
        ]
      }
    ]
  }
}
```

---

## 運用メモ

- 体験優先の中核は `sandbox.enabled=true` + `autoAllowBashIfSandboxed=true`。
- ルール優先順位は `deny -> ask -> allow`（最初に一致したルールが適用）。
- `defaultMode: "acceptEdits"` で編集確認を最小化。
- `.env` / `secrets/**` は `Read/Edit/Write` をすべて deny。
- Bash パターンは `*` 記法を利用。
