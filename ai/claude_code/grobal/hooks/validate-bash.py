#!/usr/bin/env python3
# ~/.claude/hooks/validate-bash.py
import json, re, sys, os, pathlib


def read_lines(p):
    try:
        return [
            l.strip()
            for l in pathlib.Path(p).read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.strip().startswith("#")
        ]
    except Exception:
        return []


data = json.load(sys.stdin)
cmd = (data.get("tool_input") or {}).get("command", "")
root = os.environ.get("CLAUDE_PROJECT_DIR", ".")
deny_extra = read_lines(os.path.join(root, ".claude/hooks/validate-bash.deny"))
allow_extra = read_lines(os.path.join(root, ".claude/hooks/validate-bash.allow"))
deny_patterns = [
    r"(^|\\s)sudo\\b",
    r"\\brm\\s+-rf\\s+(/|\\S+)",
    r"\\bmkfs\\b|\\bdd\\b",
    r"\\b(chown|chmod)\\s+777\\b",
    r"\\b(systemctl|service|crontab)\\b",
    r"\\b(find\\s+/?\\s+-delete|find\\s+/\\s)",
    r"\\b(git\\s+push\\s+--force|git\\s+push\\s+-f|git\\s+reset\\s+--hard|git\\s+clean\\s+-fdx|git\\s+rebase\\b)",
    r"\\bdocker\\s+run\\s+--privileged\\b|\\bdocker\\s+run\\s+-v\\s+/:/host\\b",
    r"\\b(curl|wget).*\\|\\s*(sh|bash)\\b",
    r"\\bpsql\\b|\\bmysql\\b|\\bmongo(d|sh)\\b",
    r"\\baws\\s+.*\\b(delete|terminate|rm)\\b",
    r"\\bgcloud\\s+.*\\bdelete\\b|\\baz\\s+.*\\bdelete\\b",
] + deny_extra
allow_prefixes = [
    "git status",
    "git branch",
    "git log",
    "git show",
    "git diff",
    "git describe",
    "git rev-parse",
    "git ls-files",
    "git ls-remote",
    "git -C ",
    "ls",
    "pwd",
    "whoami",
    "which ",
    "node -v",
    "npm -v",
    "yarn -v",
    "pnpm -v",
    "python --version",
    "go version",
    "rustc --version",
    "cat package.json",
    "cat pyproject.toml",
    "cat Cargo.toml",
    "cat go.mod",
] + allow_extra
if any(cmd.startswith(p) for p in allow_prefixes):
    print("ok")
    sys.exit(0)
for pat in deny_patterns:
    if re.search(pat, cmd, re.IGNORECASE):
        print(f"blocked: {cmd}", file=sys.stderr)
        sys.exit(2)
print("ok")
sys.exit(0)
