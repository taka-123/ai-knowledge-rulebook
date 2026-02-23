### Antigravity 設定メモ（2026/02/23）

**SECURITY**

- Strict Mode: **OFF**

**ARTIFACT**

- Review Policy: **Agent Decides**

**TERMINAL**

- Terminal Command Auto Execution: **Request Review**
- Enable Terminal Sandbox: **ON**
- Sandbox Allow Network: **ON**
- Enable Shell Integration: **ON**
- **Allow List Terminal Commands**
  `npm *`
  `yarn *`
  `pnpm *`
  `make *`
  `git status *`
  `git diff *`
  `git log *`
  `git add *`
  `git commit *`
  `git pull`
  `git branch *`
  `ls *`
  `pwd`
  `whoami`
  `which *`
  `node *`
  `python *`
  `pytest *`
  `go *`
  `cargo *`
  `trash *`
  `gomi *`
- **Deny List Terminal Commands**
  `rm *`
  `sudo *`
  `curl *`
  `wget *`
  `ssh *`
  `scp *`
  `aws *`
  `terraform *`
  `kubectl *`
  `git push --force *`
  `git push -f *`
  `git reset --hard *`
  `git clean -fdx *`

**FILE ACCESS**

- Agent Gitignore Access: **ON**
- Agent Non-Workspace File Access: **OFF**
- Auto-Open Edited Files: **ON**

**AUTOMATION**

- Agent Auto-Fix Lints: **ON**
- Auto-Continue: **OFF**

**HISTORY**

- Conversation History: **ON**
- Knowledge: **ON**

**GENERAL**

- Explain and Fix in Current Conversation: **OFF**

**BROWSER**

- **Browser URL Allowlist**（Advanced Settings → Browserセクションを開く）
  ファイル `~/.gemini/antigravity/browserAllowlist.txt` が開くので、以下を1行ずつ追加:
  `github.com`
  `api.github.com`
  `registry.npmjs.org`
  `*.npmjs.org`
  `pypi.org`
  `files.pythonhosted.org`
  `*.rds.amazonaws.com`
