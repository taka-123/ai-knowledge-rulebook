# 外部サービス安全運用（AWS / GitHub）

AI エージェントから AWS・GitHub を使うときの推奨構成。
クライアント設定だけで安全を作らず、サービス側の境界を最優先にする。

## 層構造

| 層                           | 役割                             | 信頼度 |
| ---------------------------- | -------------------------------- | ------ |
| AWS IAM/SCP・GitHub Rulesets | 本当のセキュリティ境界           | 最重要 |
| MCP の機能制限               | AI に危険な道具を見せない        | 重要   |
| Hooks・Permissions・Rules    | 誤操作・迂回の抑止               | 補助   |
| `AGENTS.md` / `CLAUDE.md`    | 行動規範（境界そのものではない） | 補助   |

人間はこれまでどおり `aws` / `gh` を使う。AI は MCP 経由に寄せる。

## AWS

### 方針

- AI は AWS MCP Server（Agent Toolkit）経由のみ。
- raw `aws` CLI / SDK / 絶対パス迂回は禁止（テンプレートの deny・hook で抑止）。
- 状態変更は原則しない。変更案はユーザーへ提示する。
- 最終境界は AWS 側。同じ Developer Role を使い、MCP 経由だけ弱くする。
  - 人間の直接 CLI/API → 通常権限
  - AI の AWS MCP → `aws:CalledViaAWSMCP` 条件で参照中心

AI 専用の弱い IAM User をメンバーごとに作る必要はない。

### IAM と SCP

| 規模                         | どこに書くか              |
| ---------------------------- | ------------------------- |
| 1 アカウント・個人           | IAM Role / Permission Set |
| 複数人チーム                 | 共通 Permission Set       |
| Organizations 全体で絶対守る | SCP へ昇格                |

`mcp.json` では権限は決まらない。AWS 側の設定が本命。

IAM Identity Center 利用時は、各アカウントの `AWSReservedSSO_...` Role を直接いじらず、Permission Set に inline policy を足す。

### IAM/SCP（fail-closed 例）

`Deny + NotAction` は「NotAction 以外を MCP 経由で明示 Deny」する。NotAction に残した操作も、元 Role 側で Allow されている必要がある。

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonApprovedActionsViaAWSMCP",
      "Effect": "Deny",
      "NotAction": [
        "sts:GetCallerIdentity",
        "ec2:Describe*",
        "rds:Describe*",
        "rds:ListTagsForResource",
        "elasticloadbalancing:Describe*",
        "autoscaling:Describe*",
        "ecs:Describe*",
        "ecs:List*",
        "ecr:Describe*",
        "ecr:ListImages",
        "cloudwatch:Describe*",
        "cloudwatch:Get*",
        "cloudwatch:List*",
        "logs:Describe*",
        "logs:Get*",
        "logs:FilterLogEvents"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:CalledViaAWSMCP": "aws-mcp.amazonaws.com"
        }
      }
    }
  ]
}
```

初期から入れない例: `secretsmanager:GetSecretValue`、`ssm:GetParameter(s)`、`kms:Decrypt`、強い Role への `sts:AssumeRole`、広範な `s3:GetObject`。必要になったものだけ後から足す。

### 導入

1. 資格情報を用意する（`aws login` 等）。
2. 推奨: `aws configure agent-toolkit`（CLI 2.35+）。
3. Claude Code は `/plugin install aws-core@claude-plugins-official` **または** テンプレートの `aws-mcp` のどちらか一方。
4. 他ツールは各 MCP 設定の `aws-mcp`（SigV4 + `mcp-proxy-for-aws`）。`AWS_REGION` を環境に合わせ、**`--read-only` を付ける**（書込み Tool をエージェントから隠す）。IAM/SCP と二重化する。
5. ホーム反映は明示時のみ `./scripts/sync-*-to-home.sh --include-mcp`。

### GitHub 資格情報

GitHub MCP 用は可能な限り Fine-grained PAT（または同等の最小権限トークン）を使い、対象 Repository と Permission を必要最小限に限定する。`X-MCP-Tools` で能力を絞っても、トークン自体が広いと別経路での被害が大きくなる。

## GitHub

### 方針

- AI は公式 GitHub MCP。`gh` は直接使わない。
- 明示依頼があれば自動: Issue/PR/CI 参照、Issue 作成・通常編集、コメント、PR 作成・通常編集、feature branch の通常 push。
- 既存 Issue の更新は明示依頼時のみ。依頼のない close / 状態変更 / 大幅本文変更はしない。
- 既存 PR も同様。明示依頼のない close、base 変更、draft/ready 変更、reviewer 変更はしない（`update_pull_request` はそれらも可能なため）。
- Tool 自体を渡さない: `merge_pull_request`、`pull_request_review_write`、`actions_run_trigger`、`create_or_update_file`、`push_files`、`delete_file`、`create_repository`、`update_pull_request_branch`。
- 勝手な close 等が実害になったら、その時点で Hook 化する（初期は ask しない）。

### MCP Tool Allowlist

```text
get_me,issue_read,list_issues,search_issues,issue_write,add_issue_comment,
pull_request_read,list_pull_requests,search_pull_requests,create_pull_request,
update_pull_request,actions_list,actions_get,get_job_logs
```

不足したら候補: `get_commit` / `list_commits`、別 repo 調査が頻発するなら `get_file_contents` / `search_code`。Release / Org 管理は原則追加しない。

### Rulesets（最終防衛線）

default branch に最低限: PR 必須、approvals、status checks、force push 禁止、削除禁止、bypass を不用意に与えない。

## テンプレート配置

| 種別             | 場所                                                                                         |
| ---------------- | -------------------------------------------------------------------------------------------- |
| 方針             | `ai/common/global/AGENTS.md`、`ai/claude_code/global/CLAUDE.md`                              |
| Claude deny/hook | `ai/claude_code/global/.claude/`（project / multi_service_parent も同趣旨）                  |
| MCP              | 各ツール `global` の MCP 設定（同期は `--include-mcp`）                                      |
| Codex            | `ai/openai_codex/global/.codex/config.toml`、`rules/default.rules`（`.rules.md` は案内のみ） |
| Cursor hooks     | `ai/cursor/global/.cursor/hooks.json`（Shell のみ。MCP 制限は `X-MCP-Tools`）                |
| Windsurf hooks   | `ai/windsurf/project/.windsurf/`（`tool_info.command_line` を読む）                          |

## 反映手順

1. AWS IAM（必要なら SCP）と GitHub Rulesets を先に整える。
2. `ai/` テンプレートを使う。
3. 明示依頼時のみ `./scripts/sync-*-to-home.sh`（MCP もなら `--include-mcp`）。
4. AWS Region・PAT・プラグイン重複を確認して再起動。

## 一次情報

- [Agent Toolkit for AWS](https://github.com/aws/agent-toolkit-for-aws)
- [AWS MCP Server IAM](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/security_iam_service-with-iam.html)
- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [GitHub Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Codex MCP](https://developers.openai.com/codex/mcp)
- [Cursor Hooks](https://cursor.com/docs/hooks)
- [OpenAI Codex 安全運用](https://openai.com/index/running-codex-safely/)
