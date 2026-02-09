<!-- 下記1-4（優先度順に記載）にて、汎用的に使用可能。 -->
<!-- プロジェクト固有は、 `./claude/`にて追記推奨 -->
<!-- 1. (managed-settings.json) -->
<!--    macOS: /Library/Application Support/ClaudeCode/managed-settings.json -->
<!--    Windows: %ProgramData%\ClaudeCode\managed-settings.json -->
<!--    Linux: /etc/claude-code/managed-settings.json -->
<!-- 2. `./claude/settings.json` -->
<!-- 3. `./claude/settings.local.json` -->
<!-- 4. (settings.json) -->
<!--    macOS/Linux: ~/.claude/settings.json -->
<!--    Windows: %USERPROFILE%\.claude\settings.json -->

```json
{
  "cleanupPeriodDays": 30,
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "0",
    "DISABLE_TELEMETRY": "1"
  },
  "includeCoAuthoredBy": false,
  "permissions": {
    "allow": [
      "WebSearch",
      "WebFetch(domain:anthropic.mintlify.app)",
      "WebFetch(domain:docs.claude.com)",
      "WebFetch(domain:developer.mozilla.org)",
      "WebFetch(domain:github.com)",
      "WebFetch(domain:npmjs.com)",
      "WebFetch(domain:pypi.org)",
      "WebFetch(domain:laravel.com)",
      "WebFetch(domain:vuejs.org)",
      "Read(README*)",
      "Read(package.json)",
      "Read(pyproject.toml)",
      "Read(Cargo.toml)",
      "Read(go.mod)",
      "Read(.gitignore)",
      "Read(LICENSE*)",
      "Read(CHANGELOG*)",
      "Read(**/package-lock.json)",
      "Read(composer.json)",
      "Read(composer.lock)",
      "Grep(**)",
      "Glob(**)",
      "Bash(ls)",
      "Bash(pwd)",
      "Bash(whoami)",
      "Bash(which git)",
      "Bash(which node)",
      "Bash(which npm)",
      "Bash(which php)",
      "Bash(node -v)",
      "Bash(npm -v)",
      "Bash(yarn -v)",
      "Bash(pnpm -v)",
      "Bash(python --version)",
      "Bash(which python)",
      "Bash(which pip)",
      "Bash(go version)",
      "Bash(which go)",
      "Bash(rustc --version)",
      "Bash(which cargo)",
      "Bash(cat package.json)",
      "Bash(cat pyproject.toml)",
      "Bash(cat Cargo.toml)",
      "Bash(cat go.mod)",
      "Bash(git status)",
      "Bash(git status:*)",
      "Bash(git branch)",
      "Bash(git log)",
      "Bash(git log:*)",
      "Bash(git show:*)",
      "Bash(git diff)",
      "Bash(git diff:*)",
      "Bash(git describe:*)",
      "Bash(git rev-parse:*)",
      "Bash(git ls-files:*)",
      "Bash(git ls-remote:*)",
      "Bash(git -C * status)",
      "Bash(git -C * status:*)",
      "Bash(git -C * branch)",
      "Bash(git -C * log)",
      "Bash(git -C * log:*)",
      "Bash(git -C * show:*)",
      "Bash(git -C * diff)",
      "Bash(git -C * diff:*)",
      "Bash(git -C * describe:*)",
      "Bash(git -C * rev-parse:*)",
      "Bash(git -C * ls-files:*)",
      "Bash(git -C * ls-remote:*)",
      "mcp__chrome-devtools__take_snapshot",
      "mcp__chrome-devtools__take_screenshot",
      "mcp__chrome-devtools__list_console_messages",
      "mcp__chrome-devtools__navigate_page",
      "mcp__chrome-devtools__click",
      "mcp__chrome-devtools__fill",
      "mcp__chrome-devtools__handle_dialog",
      "mcp__chrome-devtools__evaluate_script",
      "mcp__chrome-devtools__list_pages",
      "mcp__chrome-devtools__select_page",
      "mcp__chrome-devtools__hover",
      "mcp__chrome-devtools__list_network_requests",
      "mcp__chrome-devtools__get_network_request",
      "mcp__chrome-devtools__resize_page",
      "mcp__chrome-devtools__navigate_page_history",
      "mcp__chrome-devtools__wait_for"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Edit(./.env*)",
      "Write(./.env*)",
      "Read(~/.ssh/**)",
      "Write(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Write(~/.aws/**)",
      "Read(~/.gcp/**)",
      "Write(~/.gcp/**)",
      "Read(**/config/database*)",
      "Write(**/config/database*)",
      "Read(.npmrc)",
      "Write(.npmrc)",
      "Read(.pypirc)",
      "Write(.pypirc)",
      "Read(**/*key*)",
      "Read(**/*token*)",
      "Bash(sudo:*)",
      "Bash(rm -rf:*)",
      "Bash(dd:*)",
      "Bash(mkfs:*)",
      "Bash(killall:*)",
      "Bash(pkill:*)",
      "Bash(systemctl:*)",
      "Bash(service:*)",
      "Bash(crontab:*)",
      "Bash(chmod 777:*)",
      "Bash(chown:*)",
      "Bash(find * -delete:*)",
      "Bash(find / :*)",
      "Bash(grep -r *password*:*)",
      "Bash(grep -r *secret*:*)",
      "Bash(cat /etc/passwd)",
      "Bash(cat /etc/shadow)",
      "Bash(env)",
      "Bash(printenv)",
      "Bash(set | grep :*)",
      "Bash(psql:*)",
      "Bash(mysql:*)",
      "Bash(mongod:*)",
      "mcp__supabase__execute_sql",
      "Bash(php artisan tinker:*)",
      "Bash(php artisan db:*)",
      "Bash(php artisan seed:*)",
      "Bash(php artisan key:generate:*)",
      "Bash(php artisan config:cache:*)",
      "Bash(php artisan config:clear:*)",
      "Bash(php artisan cache:clear:*)",
      "Bash(php artisan optimize:*)",
      "Bash(php artisan down:*)",
      "Bash(php artisan up:*)",
      "Bash(php artisan queue:*)",
      "Bash(php artisan migrate:fresh:*)",
      "Bash(php artisan migrate:reset:*)",
      "Bash(php artisan storage:link:*)",
      "Bash(npm uninstall:*)",
      "Bash(npm remove:*)",
      "Bash(yarn remove:*)",
      "Bash(git push --force:*)",
      "Bash(git push -f:*)",
      "Bash(git reset --hard:*)",
      "Bash(git rebase:*)",
      "Bash(git clean -fdx:*)",
      "Bash(git checkout -f:*)",
      "Bash(git tag -d:*)",
      "Bash(git branch -D:*)",
      "Bash(git config --global:*)",
      "Bash(git -C * push --force:*)",
      "Bash(git -C * push -f:*)",
      "Bash(git -C * reset --hard:*)",
      "Bash(git -C * rebase:*)",
      "Bash(git -C * clean -fdx:*)",
      "Bash(git -C * checkout -f:*)",
      "Bash(git -C * tag -d:*)",
      "Bash(git -C * branch -D:*)",
      "Bash(git -C * config --global:*)",
      "Bash(docker system prune:*)",
      "Bash(docker volume rm:*)",
      "Bash(docker run --privileged:*)",
      "Bash(docker run -v /:/host:*)",
      "Bash(aws cloudformation delete-stack:*)",
      "Bash(aws s3 rm:*)",
      "Bash(aws s3api delete:*)",
      "Bash(aws ec2 terminate-instances:*)",
      "Bash(aws rds delete-db-instance:*)",
      "Bash(aws rds delete-db-cluster:*)",
      "Bash(aws iam delete:*)",
      "Bash(aws lambda delete-function:*)",
      "Bash(aws dynamodb delete-table:*)",
      "Bash(aws route53 delete:*)",
      "Bash(aws logs delete:*)",
      "Bash(aws secretsmanager delete-secret:*)",
      "Bash(aws elasticache delete:*)",
      "Bash(aws elbv2 delete:*)",
      "Bash(aws autoscaling delete:*)",
      "Bash(gcloud compute instances delete:*)",
      "Bash(gcloud sql instances delete:*)",
      "Bash(gcloud container clusters delete:*)",
      "Bash(gcloud projects delete:*)",
      "Bash(az vm delete:*)",
      "Bash(az group delete:*)",
      "Bash(az sql server delete:*)"
    ],
    "ask": [
      "Write(**)",
      "Edit(**)",
      "Bash(npm install:*)",
      "Bash(npm update:*)",
      "Bash(yarn add:*)",
      "Bash(yarn remove:*)",
      "Bash(yarn install:*)",
      "Bash(pnpm install:*)",
      "Bash(composer install:*)",
      "Bash(composer update:*)",
      "Bash(docker run:*)",
      "Bash(docker exec:*)",
      "Bash(git push:*)",
      "Bash(git -C * push:*)"
    ],
    "defaultMode": "default",
    "disableBypassPermissionsMode": "disable"
  },
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Sosumi.aiff"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Glass.aiff"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Ping.aiff"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r 'if .tool_input.command | test(\"rm -rf|dd if=|:(\\\\)\\\\{ :\\\\|:& \\\\};:\") then {\"decision\": \"block\", \"reason\": \"危険なコマンドは実行できません。別の方法を検討してください。\"} else empty end'"
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
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if [ -x \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py\" ]; then python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py\"; elif [ -x \"$HOME/.claude/hooks/validate-bash.py\" ]; then python3 \"$HOME/.claude/hooks/validate-bash.py\"; else echo 'skip validate-bash (no script)'; fi",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "WebFetch",
        "hooks": [
          {
            "type": "command",
            "command": "if [ -x \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-webfetch.sh\" ]; then \"$CLAUDE_PROJECT_DIR/.claude/hooks/validate-webfetch.sh\"; elif [ -x \"$HOME/.claude/hooks/validate-webfetch.sh\" ]; then \"$HOME/.claude/hooks/validate-webfetch.sh\"; else echo 'skip validate-webfetch (no script)'; fi",
            "timeout": 5
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
            "command": "echo '✅ 変更完了：出典URLと絶対日付の記載を確認してください'",
            "timeout": 5
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'checkpoint marker (PreCompact)'"
          }
        ]
      }
    ]
  }
}
```

---

## 上位キー

- **cleanupPeriodDays**（会話保持日数）
  ローカルのチャット記録を最終アクティビティ基準で何日保持するか（既定30日）。([anthropic.mintlify.app][1])

- **env**（環境変数）
  すべてのセッションに適用される環境変数。例として `CLAUDE_CODE_ENABLE_TELEMETRY` 等が公式例に掲載。([anthropic.mintlify.app][1])

- **includeCoAuthoredBy**（共同署名挿入）
  Gitコミット/PRに「co-authored-by Claude」を含めるか（既定true）。([anthropic.mintlify.app][1])

- **permissions**（権限制御）
  ツール使用の可否を**allow / ask / deny** で宣言するブロック。詳細は下記。([anthropic.mintlify.app][1])

## permissions の内訳と優先

- **allow**
  許可する操作のルール配列。Bash だけは**正規表現ではなく接頭辞マッチ**（`Bash(git diff:*)` 等）。([anthropic.mintlify.app][1])
- **ask**
  実行前に確認するルール配列。**ask は allow より優先**。
- **deny**
  拒否（完全に不可視化も含む）。**deny は ask/allow より優先**。Bashは接頭辞マッチで**回避可能性**ありの注意書きが公式にある。([anthropic.mintlify.app][1])
- **追加の書式要点**
  - **Bash**: `Bash(cmd:*)` は前方一致。
  - **Read/Edit/Write**: パスは `.gitignore` 互換パターン（`**`, `*` 等）。
  - **WebFetch**: `WebFetch(domain:example.com)` の**ドメイン単位**指定が仕様。パスワイルドカードの記法はリファレンスに無い。
  - **MCPツール**: `mcp__server` / `mcp__server__tool` で指名（ワイルドカード不可）。

> 補足: 権限モードの関連オプションとして `defaultMode`（起動デフォルト）と `disableBypassPermissionsMode` もある（必要に応じて追加可能）。([anthropic.mintlify.app][1])

## ツール名の正確性（一覧）

Claude Codeの組み込みツールは **Bash / Edit / Glob / Grep / NotebookEdit / NotebookRead / Read / SlashCommand / Task / TodoWrite / WebFetch / WebSearch / Write**。
提示JSON中の **`List(*)`** は**公式一覧に無い名称**なので、意図が `Glob`（ファイル探索）や `Bash(ls …)` なら書き換え推奨。([anthropic.mintlify.app][1])

---

**参照**

- Claude Code settings（Available settings / Permission settings / Precedence）([anthropic.mintlify.app][1])
- Identity and Access Management（precedence/優先・ルール記法・WebFetch/MCPの指定方法）
- Tools available to Claude（公式ツール一覧）([anthropic.mintlify.app][1])

[1]: https://anthropic.mintlify.app/en/docs/claude-code/settings 'Claude Code settings - Claude Docs'
