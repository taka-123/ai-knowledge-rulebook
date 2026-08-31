#!/usr/bin/env bash
# Fixture checks for AWS/GitHub CLI and git-push guards.
# stdin JSON で hook を直接叩く（コマンドラインに aws/gh を出さない）。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CURSOR_HOOK="$ROOT/.cursor/hooks/check-external-services.sh"
CLAUDE_HOOK="$ROOT/.claude/hooks/pretooluse_guard.sh"
WINDSURF_HOOK="$ROOT/.windsurf/hooks/check-external-services.sh"
FAILED=0

tmp_feature="$(mktemp -d)"
tmp_main="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_feature" "$tmp_main"
}
trap cleanup EXIT
git -C "$tmp_feature" init -q -b feature-x
git -C "$tmp_main" init -q -b main

fail() {
  echo "FAIL: $*" >&2
  FAILED=1
}

cursor_perm() {
  local cmd="$1" cwd="${2:-$tmp_feature}"
  jq -n --arg c "$cmd" --arg cwd "$cwd" '{command:$c, cwd:$cwd}' \
    | bash "$CURSOR_HOOK" \
    | jq -r '.permission'
}

claude_code() {
  local cmd="$1" cwd="${2:-$tmp_feature}"
  local json code
  json="$(jq -n --arg c "$cmd" --arg cwd "$cwd" '{tool_name:"Bash", tool_input:{command:$c}, cwd:$cwd}')"
  set +e
  printf '%s' "$json" | bash "$CLAUDE_HOOK" >/dev/null 2>&1
  code=$?
  set -e
  printf '%s' "$code"
}

windsurf_code() {
  local cmd="$1" cwd="${2:-$tmp_feature}"
  local json code
  json="$(jq -n --arg c "$cmd" --arg cwd "$cwd" '{tool_info:{command_line:$c, cwd:$cwd}, cwd:$cwd}')"
  set +e
  printf '%s' "$json" | bash "$WINDSURF_HOOK" >/dev/null 2>&1
  code=$?
  set -e
  printf '%s' "$code"
}

expect_cursor() {
  local want="$1" cmd="$2" cwd="${3:-$tmp_feature}"
  local got
  got="$(cursor_perm "$cmd" "$cwd")"
  if [[ "$got" != "$want" ]]; then
    fail "cursor want=$want got=$got :: $cmd"
  fi
}

expect_claude() {
  local want="$1" cmd="$2" cwd="${3:-$tmp_feature}"
  local got
  got="$(claude_code "$cmd" "$cwd")"
  if [[ "$got" != "$want" ]]; then
    fail "claude want=$want got=$got :: $cmd"
  fi
}

expect_windsurf() {
  local want="$1" cmd="$2" cwd="${3:-$tmp_feature}"
  local got
  got="$(windsurf_code "$cmd" "$cwd")"
  if [[ "$got" != "$want" ]]; then
    fail "windsurf want=$want got=$got :: $cmd"
  fi
}

# deny: cursor=deny, claude/windsurf=exit 2
# allow: cursor=allow, claude/windsurf=exit 0
deny_all() {
  local cmd="$1" cwd="${2:-$tmp_feature}"
  expect_cursor deny "$cmd" "$cwd"
  expect_claude 2 "$cmd" "$cwd"
  expect_windsurf 2 "$cmd" "$cwd"
}

allow_all() {
  local cmd="$1" cwd="${2:-$tmp_feature}"
  expect_cursor allow "$cmd" "$cwd"
  expect_claude 0 "$cmd" "$cwd"
  expect_windsurf 0 "$cmd" "$cwd"
}

allow_all "echo hello"
deny_all "aws s3 ls"
deny_all "/usr/bin/aws s3 ls"
deny_all "/opt/homebrew/opt/awscli/bin/aws s3 ls"
deny_all "./aws s3 ls"
deny_all "aws;"
deny_all '$(aws s3 ls)'
deny_all "true && aws s3 ls"
allow_all "gh pr view 1"
allow_all "/usr/local/bin/gh issue list"
allow_all "gh pr checks 1"
allow_all "gh api repos/owner/repo/pulls/1"
allow_all "gh api repos/owner/repo/actions/runs -X GET -f head_sha=abc -f per_page=100"
allow_all "gh api repos/owner/repo/actions/runs/1/jobs -X GET -f per_page=100"
allow_all "gh repo view owner/repo"
allow_all "gh auth status"
allow_all "python3 scripts/run-gh-pr-watch.py --pr 1 --retry-failed-now"
deny_all "gh pr merge 1"
deny_all "gh pr review 1 --approve"
deny_all "gh workflow run build.yml"
deny_all "gh run rerun 123"
deny_all "gh run rerun 123 --failed"
deny_all "gh repo edit owner/repo"
deny_all "gh auth token"
deny_all "gh api repos/owner/repo/pulls/1 -X DELETE"
deny_all "gh api graphql -f query=foo"
deny_all "gh api repos/owner/repo/pulls/1/reviews -f event=APPROVE ; gh api repos/owner/repo/pulls/1 -X GET"
deny_all "gh api repos/owner/repo/pulls/1/reviews -f event=APPROVE && gh api repos/owner/repo/pulls/1 -X GET"
deny_all 'gh api repos/owner/repo/pulls/1/reviews -f event=APPROVE $(gh api repos/owner/repo/pulls/1 -X GET)'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -f event=APPROVE `gh api repos/owner/repo/pulls/1 -X GET`'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X GET -X "$m" -f event=APPROVE'
deny_all 'm=POST; gh api repos/owner/repo/pulls/1/reviews -X GET -X "$m" -f event=APPROVE'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X GET --method="$m" -f event=APPROVE'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X GET -X"$m" -f event=APPROVE'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X "$m" -f event=APPROVE'
deny_all "gh api repos/owner/repo/issues/1/comments -X POST -f body=hi"
deny_all "gh api repos/owner/repo/pulls/1 --input payload.json"
allow_all "rg 'gh '"
allow_all "echo 'aws s3 ls'"
allow_all 'git commit -m "use aws cli"'
allow_all "echo aws"
allow_all "command -v aws"

allow_all "git push origin HEAD" "$tmp_feature"
deny_all "git push origin main" "$tmp_feature"
deny_all "git push origin HEAD" "$tmp_main"
deny_all "git push --force origin HEAD" "$tmp_feature"
deny_all "git push --force-with-lease=main origin HEAD" "$tmp_feature"
deny_all "git push -f origin HEAD" "$tmp_feature"
deny_all "git push origin +main" "$tmp_feature"
allow_all "git push origin HEAD && ls -f" "$tmp_feature"
allow_all "git status"

if [[ "$FAILED" -ne 0 ]]; then
  echo "hooks:check failed" >&2
  exit 1
fi
echo "hooks:check passed"
