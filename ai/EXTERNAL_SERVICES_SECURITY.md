# 外部サービス安全運用（AWS / GitHub）

AI エージェントから AWS・GitHub を使うときの推奨構成。
クライアント設定だけで安全を作らず、サービス側の境界を最優先にする。

## 層構造

| 層                                 | 役割                             | 信頼度 |
| ---------------------------------- | -------------------------------- | ------ |
| AWS IAM/SCP・GitHub Rulesets       | 本当のセキュリティ境界           | 最重要 |
| GitHub 側 credential 権限          | Cloud / CI では特に重要          | 重要   |
| MCP tool 制限 / Agent command deny | 危険な能力を減らす               | 補助   |
| `AGENTS.md` / `CLAUDE.md` / Skill  | 行動規範（境界そのものではない） | 補助   |

人間はこれまでどおり `aws` / `gh` を使う。
AWS は AI を MCP 経由に限定する。GitHub は MCP と `gh` のどちらも使ってよい。GitHub MCP を使うこと自体はセキュリティ境界ではない。

## AWS

### 方針

- AI は AWS MCP Server（Agent Toolkit）経由のみ。
- raw `aws` CLI / SDK / 絶対パス迂回は禁止。CLI 起動は deny・hook で抑止し、SDK は IAM が止める。
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
4. 他ツールは各 MCP 設定の `aws-mcp`（SigV4 + `mcp-proxy-for-aws`）。作業リージョンは `--metadata` と `env.AWS_REGION` を揃える。**`--read-only` は付けない**（`run_script` が消え、CloudWatch 等の参照ができなくなる）。更新・削除は IAM/SCP の `aws:CalledViaAWSMCP` で止める。
5. ホーム反映は明示時のみ `./scripts/sync-*-to-home.sh --include-mcp`。

### GitHub 資格情報

GitHub MCP を使う場合は、可能な限り Fine-grained PAT（または同等の最小権限トークン）を使い、対象 Repository と Permission を必要最小限に限定する。`X-MCP-Tools` で能力を絞っても、トークン自体が広いと別経路での被害が大きくなる。
ローカルの対話型 Agent では、人間用と AI 専用の `gh` credential を必須分離しない。既存の `gh auth` を使ってよい。Cloud / CI / 無人実行では人間のローカル credential を共有せず、GitHub App / 製品連携 / Fine-grained PAT 等の machine 向け資格情報を使う。

## GitHub

### 方針

- GitHub 操作には公式 GitHub MCP または `gh` を使ってよい。一方が使えなければ他方を試す。GitHub MCP 未登録だけでは GitHub 操作不可とはしない。
- 明示依頼があれば自動: Issue/PR/CI 参照、Issue 作成・通常編集、コメント、PR 作成・通常編集、feature branch の通常 push。
- 既存 Issue の更新は明示依頼時のみ。依頼のない close / 状態変更 / 大幅本文変更はしない。
- 既存 PR も同様。明示依頼のない close、base 変更、draft/ready 変更、reviewer 変更はしない（`update_pull_request` はそれらも可能なため）。
- 禁止: PR merge、PR review 提出、default / protected branch への直接 push、force push、Actions 手動実行・rerun、Repository / Ruleset / Branch Protection の変更、認証情報の表示・変更。
- GitHub MCP を使う場合は、次の tool を渡さない: `merge_pull_request`、`pull_request_review_write`、`actions_run_trigger`、`create_or_update_file`、`push_files`、`delete_file`、`create_repository`、`update_pull_request_branch`。
- `gh` では同等の危険操作（`gh pr merge`、`gh pr review`、`gh workflow run`、`gh run rerun`、`gh repo delete/archive/edit`、`gh auth token/login/logout/refresh`、mutating `gh api`）を hook / deny で止める。
- 勝手な close 等が実害になったら、その時点で Hook 化する（初期は ask しない）。

### MCP Tool Allowlist（GitHub MCP を使う場合）

```text
get_me,issue_read,list_issues,search_issues,issue_write,add_issue_comment,
pull_request_read,list_pull_requests,search_pull_requests,create_pull_request,
update_pull_request,actions_list,actions_get,get_job_logs
```

不足したら候補: `get_commit` / `list_commits`、別 repo 調査が頻発するなら `get_file_contents` / `search_code`。Release / Org 管理は原則追加しない。

### Rulesets（最終防衛線）

default branch に最低限: PR 必須、approvals、status checks、force push 禁止、削除禁止、bypass を不用意に与えない。

## テンプレート配置（global + project）

**方針**: Local は global、Cloud でも必要な方針・実行制御は project にも置く。秘密情報は repo に置かない。

| 種別                 | Local (global)                    | Cloud / portable (project)                                                       |
| -------------------- | --------------------------------- | -------------------------------------------------------------------------------- |
| 共通方針             | `ai/common/global/AGENTS.md`      | `ai/common/project/AGENTS.md`（→ 各 repo の `AGENTS.md`）                        |
| Claude 方針          | `ai/claude_code/global/CLAUDE.md` | `ai/claude_code/project/CLAUDE.md`                                               |
| Claude deny/hook     | `~/.claude/` 同期                 | repo `.claude/settings.json` + `.claude/hooks/pretooluse_guard.sh`               |
| Cursor hooks         | `~/.cursor/hooks.json`            | repo `.cursor/hooks.json` + `.cursor/hooks/*.sh`                                 |
| Cursor rules         | User Rules                        | repo `.cursor/rules/external-services-safety.mdc`                                |
| Codex rules / config | `~/.codex/`（Local のみ）         | Cloud の本線は repo `AGENTS.md`。`.codex/rules` は Cloud 防御に数えない          |
| Windsurf hooks       | Local/Cascade 用                  | `.windsurf/hooks.json` は Local 用。Cloud 保証は `AGENTS.md` まで                |
| MCP 認証             | ホーム / 環境変数 / dashboard     | **PAT・AWS鍵を repo に置かない**。Cloud は各製品の Secrets / OAuth / GitHub 連携 |

### Cloud 向け最小コピー例

```bash
# 方針（必須寄り）
cp ai/common/project/AGENTS.md /path/to/repo/AGENTS.md

# Cursor Cloud
mkdir -p /path/to/repo/.cursor/hooks /path/to/repo/.cursor/rules
cp ai/cursor/project/.cursor/hooks.json /path/to/repo/.cursor/
cp ai/cursor/project/.cursor/hooks/check-external-services.sh /path/to/repo/.cursor/hooks/
cp ai/cursor/project/.cursor/rules/external-services-safety.mdc /path/to/repo/.cursor/rules/

# Claude Cloud
cp ai/claude_code/project/CLAUDE.md /path/to/repo/CLAUDE.md
cp -R ai/claude_code/project/.claude /path/to/repo/.claude
```

Anthropic-hosted Claude Cloud に長期 AWS credential を渡して AWS MCP を使うのは推奨しない。AWS 操作は Local か、組織管理の self-hosted 環境へ寄せる。

## 反映手順

1. AWS IAM（必要なら SCP）と GitHub Rulesets を先に整える。
2. Local: `ai/*/global` を使い、明示時のみ `./scripts/sync-*-to-home.sh`（MCP もなら `--include-mcp`）。
3. Cloud 利用 repo: 上記 project 資産を実体コピーして commit。
4. AWS Region・PAT・プラグイン重複を確認して再起動。

## 一次情報

- [Agent Toolkit for AWS](https://github.com/aws/agent-toolkit-for-aws)
- [AWS MCP Server IAM](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/security_iam_service-with-iam.html)
- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [GitHub Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Codex MCP](https://developers.openai.com/codex/mcp)
- [Cursor Hooks](https://cursor.com/docs/hooks)
- [OpenAI Codex 安全運用](https://openai.com/index/running-codex-safely/)
