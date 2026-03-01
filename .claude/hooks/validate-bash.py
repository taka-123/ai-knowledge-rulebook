#!/usr/bin/env python3
import json, re, subprocess, sys, os, pathlib


def read_lines(p):
    try:
        return [
            l.strip()
            for l in pathlib.Path(p).read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.strip().startswith("#")
        ]
    except Exception:
        return []


PROTECTED_BRANCHES = {
    "main", "master", "develop", "development",
    "deploy", "production", "release",
}


def current_branch():
    try:
        r = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, timeout=5,
        )
        return r.stdout.strip()
    except Exception:
        return ""


def deny(reason):
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
    )
    sys.exit(0)


data = json.load(sys.stdin)
cmd = (data.get("tool_input") or {}).get("command", "")
root = os.environ.get("CLAUDE_PROJECT_DIR", ".")
deny_extra = read_lines(os.path.join(root, ".claude/hooks/validate-bash.deny"))
allow_extra = read_lines(os.path.join(root, ".claude/hooks/validate-bash.allow"))
deny_patterns = [
    (r"(^|\s)sudo\b", "sudo は使用禁止です。"),
    (r"\brm\s+-rf\s+(/|\S+)", "rm -rf は危険なため禁止です。"),
    (r"\bmkfs\b|\bdd\b", "mkfs / dd はディスク破壊につながるため禁止です。"),
    (
        r"\b(chown|chmod)\s+777\b",
        "chmod/chown 777 は権限昇格の危険があるため禁止です。",
    ),
    (r"\b(systemctl|service|crontab)\b", "サービス操作コマンドは禁止です。"),
    (r"\b(find\s+/?\s+-delete|find\s+/\s)", "find による一括削除は禁止です。"),
    (
        r"\bgit\s+add\s+(-A|--all|\.(\s|$))",
        "git add -A / git add . は禁止です。追加するファイルを明示的に指定してください。",
    ),
    (
        r"\bgit\s+reset\s+--hard\b|\bgit\s+clean\s+-fdx\b|\bgit\s+rebase\b",
        "破壊的な git 操作は禁止です。",
    ),
    (
        r"\bdocker\s+run\s+--privileged\b|\bdocker\s+run\s+-v\s+/:/host\b",
        "特権モードでの docker run は禁止です。",
    ),
    (r"\b(bash|sh|zsh)\s+-c\b", "シェルコマンドインジェクション（-c オプション）は禁止です。"),
    (r"^(env|printenv)(\s|$)", "環境変数の表示は機密情報漏洩につながるため禁止です。"),
    (r"\b(curl|wget).*\|\s*(sh|bash)\b", "パイプ経由のスクリプト実行は禁止です。"),
    (r"\bpsql\b|\bmysql\b|\bmongo(d|sh)\b", "DB への直接接続は禁止です。"),
    (r"\baws\s+.*\b(delete|terminate|rm)\b", "AWS リソースの削除操作は禁止です。"),
    (
        r"\bgcloud\s+.*\bdelete\b|\baz\s+.*\bdelete\b",
        "クラウドリソースの削除操作は禁止です。",
    ),
] + [(p, "deny リストにより禁止されています。") for p in deny_extra]
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
if re.search(r"\bgit\s+push\b", cmd, re.IGNORECASE):
    branch = current_branch()
    if not branch or branch in PROTECTED_BRANCHES:
        deny(f"保護ブランチ '{branch or '不明'}' への git push は禁止です。ユーザーに依頼してください。")

for pat, reason in deny_patterns:
    if re.search(pat, cmd, re.IGNORECASE):
        deny(reason)
print("ok")
sys.exit(0)
