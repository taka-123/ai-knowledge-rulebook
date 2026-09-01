# 一発実装指示：AI 向け AWS / GitHub 安全設定（配布用）

使い方: 対象プロジェクトを開き、この文書を省略せず全文貼る。実装者はこの文書だけを読む。他のメモ・調査ノート・過去会話・別リポジトリ・配布元のファイルは開かない。必要な方針・JSON・スクリプト・IAM・禁止事項はすべて以下に書いてある。

目的は、AI エージェントが AWS を参照でき、GitHub を限定的に書け、更新・削除・本番破壊をサービス側と補助制御で止めること。試行錯誤せず、完成形を一度で入れる。

実装してよいのは、このプロジェクトのリポジトリ内だけ。ホームディレクトリ（`~/.cursor`、`~/.claude`、`~/.codex` 等）への書き込み、IAM コンソール操作、GitHub Rulesets の実設定、PAT の発行はユーザー作業なので実行しない。同じ内容を完了報告と、リポジトリ内の運用説明ファイルへ残す。

commit / push / PR は明示依頼がなければしない。

リポジトリへのコード反映だけでは目的は完成しない。コードは「AI に raw `aws` を使わせない」「GitHub の危険操作（merge / review 提出 / Actions 手動実行 / repo 管理 / 認証情報の表示変更）を止める」ところまでである。AWS 参照を通すには各ツールへ AWS MCP を登録する。GitHub は GitHub MCP でも認証済み `gh` でもよい。更新削除を止めるには既存 IAM へポリシーを足す。default / protected branch は、同等の Rulesets または branch protection があることをユーザーが確認する。これらは実装者が実行せず、完了報告の必須項目としてユーザーへ渡す。

作業リージョンの既定は東京 `ap-northeast-1`。ユーザーが別リージョンを明示したら、`--metadata AWS_REGION` だけをその値にする。MCP 接続 URL の `us-east-1` は変えない。`env.AWS_REGION` は必須ではない。

---

## 1. 背景と完成条件

人間の `aws` / `gh` はこれまでどおり広い権限で使う。禁止しない。

AI には次を同時に満たさせる。

- AWS のリソース設定、CloudWatch、ログなど参照はできる
- AWS の作成・更新・削除・起動停止・デプロイ・権限変更はしない（間違って消さない）
- GitHub は Issue / PR / CI の参照、Issue 作成、コメント、PR 作成、feature branch の通常 push まで
- PR merge、review 提出、`main` / `master` / `develop` / `deploy` への直接 push、force push、Actions 手動起動・rerun、Ruleset 変更は禁止
- Agent 直下の `gh workflow run` / `gh run rerun` は禁止。例外は公式 babysit-pr watcher による current PR の flaky/unrelated failed checks の bounded rerun（最大 3 cycle）のみ
- GitHub は公式 MCP または `gh` を使ってよい。一方が使えなければ他方を試す。GitHub MCP を必須経路にしない
- raw `aws` CLI / SDK / 絶対パス迂回は使わない。AWS 公式 MCP を使う

クライアント設定だけで安全は作れない。層は次で固定する。

| 層                                 | 役割                    | 信頼度 |
| ---------------------------------- | ----------------------- | -----: |
| AWS IAM/SCP・GitHub Rulesets       | 本当のセキュリティ境界  | 最重要 |
| GitHub 側 credential 権限          | Cloud / CI では特に重要 |   重要 |
| MCP tool 制限 / Agent command deny | 危険な能力を減らす      |   補助 |
| AGENTS.md / CLAUDE.md              | 行動規範。境界ではない  |   補助 |

AI 専用の弱い IAM User は作らない。今使っている Developer Role / Permission Set に「MCP 経由のときだけ Write を Deny」するポリシーを足す。Identity Center なら各アカウントの `AWSReservedSSO_...` を直接いじらず、Permission Set の inline policy に書く。

### 人が CLI したときと、AI が MCP したとき

同じ IAM 主体でも、条件キー `aws:CalledViaAWSMCP` が付く MCP 経路だけ Deny が効く。人の `aws` CLI は今までどおり。

| やりたいこと                                                           | 人の `aws` / `gh` / `git` | AI（必要なユーザー作業完了後）   |
| ---------------------------------------------------------------------- | ------------------------- | -------------------------------- |
| EC2 / RDS / ELB / ASG / ECS / ECR の参照                               | 今までどおり              | MCP でできる                     |
| CloudWatch・ログの参照                                                 | 今までどおり              | MCP でできる                     |
| `sts:GetCallerIdentity`                                                | 今までどおり              | MCP でできる                     |
| AWS の作成・更新・削除・起動停止・デプロイ・権限変更                   | 今までどおりできる        | IAM でできない                   |
| S3 オブジェクト取得、Secrets Manager、SSM Parameter、KMS Decrypt       | Role 次第                 | 初期 IAM ではできない            |
| シェルの `aws`                                                         | 使う                      | hook / deny で止める             |
| シェルの日常的な `gh`（view / list / create / comment 等）             | 使う                      | 使ってよい                       |
| Issue / PR / CI 参照、Issue 作成、コメント、PR 作成・通常編集          | できる                    | 明示依頼があれば MCP または `gh` |
| feature branch の通常 `git push`                                       | できる                    | できる                           |
| PR merge、review 提出、Actions 手動実行、repo 管理、認証情報の表示変更 | 権限があればできる        | hook / 憲法 / Rulesets で止める  |
| `main` / `master` / `develop` / `deploy` / force push                  | Rulesets が最終防衛       | hook で止める                    |

IAM を付けるまで、AI の MCP `run_script` は Role が許す範囲で更新・削除も呼べる。

---

## 2. 省略するな・余計にするな

見た目で判断して削ったり足したりしない。

| 判断しがちなこと                                                    | 実際                                          | 理由                                                                      |
| ------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------- |
| `--read-only` を付ければ参照専用になる                              | **付けるな**                                  | 参照に使う `aws___run_script` まで消える。参照専用は IAM で作る           |
| AWS が MCP 経由を最初から参照専用にしてくれる                       | **しない。ポリシーを自分で作って付ける**      | AWS が自動で付けるのは条件キーだけ。Deny は自分で書く                     |
| IAM 例や「ユーザーがやること」はコードと無関係だから文書に書かない  | **書け**                                      | コードだけでは参照も Write 抑止も完成しない                               |
| hook だけで十分。憲法の外部サービス節は重複                         | **両方書け**                                  | hook は CLI の補助。MCP の tool は hook を通らない                        |
| GitHub は default toolset でよい                                    | **allowlist だけ。既存の広い toolset は除去** | 併用すると加算される。最終的に見える tool が allowlist だけになるまで直す |
| GitHub MCP にも read-only を付ければ安全                            | **付けるな**                                  | write tool が全部消え、Issue/PR 作成まで使えなくなる                      |
| `X-MCP-Tools` があるから PAT は広くてよい                           | **PAT も最小**                                | allowlist は MCP 経路だけ                                                 |
| URL の `us-east-1` を作業リージョンに変える                         | **変えるな**                                  | MCP サーバーの接続先                                                      |
| `env.AWS_REGION` は `--metadata` と必ず同値にしろ                   | **するな。metadata だけ必須**                 | metadata はリモートの作業リージョン。env は手元プロキシ用で必須ではない   |
| ホームの MCP までリポジトリに実トークンで書く                       | **書くな**                                    | 秘密を git に入れない                                                     |
| Cursor User Rules に「GitHub は MCP のみ」または「`gh` のみ」と残す | **両方可に直せ**                              | 経路は競合しない。同じ安全ポリシーに従う                                  |
| `AGENTS.md` から `CLAUDE.md` を読め（またはその逆）                 | **するな**                                    | 平行憲法。同じ本質を各自に自己完結で書く。重複は問題にしない              |

### AWS MCP に `--read-only` を付けない

`mcp-proxy-for-aws` の `--read-only` は「読み取り API だけ残す」ではない。書ける tool を丸ごと隠す。アカウントの EC2 / RDS / CloudWatch を読む入口は `aws___run_script`（旧 `aws___call_aws`）であり、Describe も Delete も同じ tool である。`--read-only` を付けるとドキュメント・リージョン情報だけが残り、リソース参照ができなくなる。

参照を可能にするには `--read-only` を付けない。更新・削除を止めるのは IAM の `aws:CalledViaAWSMCP` である。

### hook で引用符を剥がして `aws ` / `gh ` を探さない

`tr -d "'\""` したあと部分一致すると、`rg 'gh '` や `echo 'aws s3 ls'` まで落ちる。コマンド位置（先頭、または `;|&` `$()` backtick の直後）だけを見る。パス末尾の `aws` は止める。`gh` はコマンド位置の危険サブコマンドだけ止める。`echo aws` やコミットメッセージ内の言及は止めない。

### hook を本丸だと思わない

SDK、boto3、未列挙ラッパは hook では止まない。コメントに「絶対パス迂回も止める」と書かない。best-effort と明記する。

### 秘密をリポジトリに置かない

PAT、AWS 鍵、実トークンはプレースホルダのまま。ユーザーのホーム MCP をプレースホルダで上書きしない。ホームへは書き込まない。

---

## 3. AWS の完成形

### 3.1 経路

```text
人間 ─ aws CLI ─────────────→ 通常権限
AI   ─ AWS MCP Server のみ ─→ IAM が MCP 経由だけ参照中心
```

AI から直接やってはならないもの:

- `aws ...`
- `/opt/homebrew/bin/aws` など絶対パス
- `python` + boto3、AWS SDK を使った独自スクリプト
- その他の迂回

状態変更が必要なら実行せず、変更案だけ出す。

### 3.2 MCP 接続（SigV4 + プロキシ）

作業リージョンは既定で東京 `ap-northeast-1`。MCP サーバー接続先 URL の `us-east-1` は変えない。これは AWS が MCP サーバーを置いている場所であり、自分の EC2 の場所ではない。公式が提供する接続先は `us-east-1` と `eu-central-1` だけである。

`--metadata AWS_REGION=ap-northeast-1` はリモート MCP が AWS API を操作する既定リージョンである。公式の設定例はこれだけを置く。`env.AWS_REGION` は手元プロキシ / botocore の region provider であり、作業リージョンではない。必須にしない。`aws login` 後に `NoRegionError` が出たときだけ、ユーザーがホーム設定へ足してよい。その値を作業リージョンと揃えろ、とはしない。metadata の値は変えない。

資格情報は JSON に書かない。人間が先に `aws login` し、boto3 チェーンで拾う。`uvx` が必要。

Claude Code は次のどちらか一方。両方は入れない。

- `/plugin install aws-core@claude-plugins-official`
- 下記 `aws-mcp` ブロック

実装者はホームの MCP を編集しない。次の完成形を運用説明と完了報告にそのまま載せる。既存の context7 / exa / playwright / drawio 等は消さない。AWS MCP に `--read-only` は付けない。GitHub MCP に read-only モードも付けない。

GitHub MCP を使う場合の完成は「設定に allowlist が書いてある」ではない。エージェントに見えている GitHub MCP tool が、下記 14 個だけであること。既存の `X-MCP-Toolsets`、default toolset、URL で tool を足す指定は除去する。`X-MCP-Tools` を足すだけでは、広い toolset は残る。使わない場合は、この完成条件は適用しない。

Cursor / Windsurf 向け（秘密はプレースホルダ）:

```json
{
  "mcpServers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer <PLACEHOLDER_GITHUB_PAT>",
        "X-MCP-Tools": "get_me,issue_read,list_issues,search_issues,issue_write,add_issue_comment,pull_request_read,list_pull_requests,search_pull_requests,create_pull_request,update_pull_request,actions_list,actions_get,get_job_logs"
      }
    },
    "aws-mcp": {
      "command": "uvx",
      "args": [
        "mcp-proxy-for-aws==1.6.4",
        "https://aws-mcp.us-east-1.api.aws/mcp",
        "--metadata",
        "AWS_REGION=ap-northeast-1"
      ]
    }
  }
}
```

Claude のユーザー設定は GitHub を `Bearer ${GITHUB_PAT}` にする（環境変数）。AWS ブロックは上と同じ（`--read-only` なし、`--metadata` の作業リージョン。`env.AWS_REGION` は必須ではない）。type が要るなら GitHub は `http`、AWS は `stdio`。

Codex の `~/.codex/config.toml` 例:

```toml
[mcp_servers.github]
url = "https://api.githubcopilot.com/mcp/"
bearer_token_env_var = "GITHUB_PAT"
http_headers = { "X-MCP-Tools" = "get_me,issue_read,list_issues,search_issues,issue_write,add_issue_comment,pull_request_read,list_pull_requests,search_pull_requests,create_pull_request,update_pull_request,actions_list,actions_get,get_job_logs" }
enabled_tools = [
  "get_me",
  "issue_read",
  "list_issues",
  "search_issues",
  "issue_write",
  "add_issue_comment",
  "pull_request_read",
  "list_pull_requests",
  "search_pull_requests",
  "create_pull_request",
  "update_pull_request",
  "actions_list",
  "actions_get",
  "get_job_logs",
]
default_tools_approval_mode = "auto"

[mcp_servers.aws-mcp]
command = "uvx"
args = [
  "mcp-proxy-for-aws==1.6.4",
  "https://aws-mcp.us-east-1.api.aws/mcp",
  "--metadata",
  "AWS_REGION=ap-northeast-1",
]
default_tools_approval_mode = "writes"
```

### 3.3 IAM（ユーザーがコンソールで行う。リポジトリの運用説明に次をそのまま書く）

AWS に「MCP は参照専用」というデフォルト設定はない。MCP 経由のリクエストには条件キー `aws:CalledViaAWSMCP`（値: `aws-mcp.amazonaws.com`）が自動で付くだけである。その印を見て Deny するポリシーは、自分で作って、AI が使っているのと同じ IAM 主体に付ける。新しい IAM ユーザーやロールは作らない。

実装者はコンソールを操作しない。特定のアカウント名・ユーザー名・グループ名・既存ポリシー名は書かない。

`aws sts get-caller-identity` は、今どの identity で動いているかを特定する材料である。返ってきた Arn にポリシーを付けない。AssumedRole / SSO の session ARN（`arn:aws:sts::...:assumed-role/...`）は添付先ではない。下にある IAM Role、または Identity Center の Permission Set を特定してそこに付ける。

**ポリシー名（推奨）:** `DenyWriteViaAWSMCP`

**説明（推奨）:** IAM の説明は日本語と括弧は使えない。英数字・スペース・`+=,.@-` は使える。空欄でもよい。入れるなら次。

```text
Deny non-read actions when CalledViaAWSMCP. Does not affect direct CLI.
```

**作成手順（IAM コンソール）**

1. IAM → ポリシー → ポリシーを作成
2. JSON タブを選び、下記をそのまま貼る。ビジュアルエディタで「全サービス拒否」から作り直さない（参照まで落ちる）
3. 確認画面でサービス数が多く見えても、JSON に `NotAction` と `"aws:CalledViaAWSMCP": "aws-mcp.amazonaws.com"` が残っていればよい。条件値が `mcp.amazonaws.com` だけに短縮されていたら JSON を直す
4. 名前と説明を上記どおり入れて作成する
5. 付ける先を決める。新しい主体は作らない。`get-caller-identity` の Arn が session なら、Role 名または Permission Set まで辿る
   - IAM ユーザーでログインしている → そのユーザー、または開発者グループ
   - IAM Role を Assume している → その Role
   - IAM Identity Center → 各アカウントの予約ロール（`AWSReservedSSO_...`）は触らず、Permission Set に足す（その Set を使うメンバー全員に効く）
6. 「ポリシーをアタッチ」する。既存の広い Allow（管理者相当を含む）は外さなくてよい。Deny の方が強い。条件が付くのは MCP 経由のときだけなので、人間の `aws` CLI は今までどおり

チーム: ポリシーはアカウントに1つ作り、各自の主体または共通 Permission Set / グループに付ける。

同じ Role に Deny + NotAction を足す。許可した参照以外の MCP 経由を拒否する fail-closed。NotAction に残した操作は、元 Role 側でも Allow されている必要がある。

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

初期から入れない: `secretsmanager:GetSecretValue`、`ssm:GetParameter(s)`、`kms:Decrypt`、強い Role への `sts:AssumeRole`、広範な `s3:GetObject`。必要になってから足す。

規模:

- 1 アカウント・個人: IAM Role / Permission Set
- 複数人: 共通 Permission Set または開発者グループ
- Organizations 全体で絶対守る: SCP へ昇格

MCP の JSON では権限は決まらない。

---

## 4. GitHub の完成形

### 4.1 経路

人間は `gh` を使ってよい。AI も公式 GitHub MCP または `gh` を使ってよい。一方が使えなければ他方を試す。GitHub MCP を必須経路にしない。GitHub MCP 未登録だけでは GitHub 操作不可とはしない。

`git` は禁止しない。`status` / `diff` / `add` / `commit` / `switch` / 通常 `push` は使ってよい。`git push --force`、`--force-with-lease`、`-f`、`+branch` は禁止。`main` / `master` / `develop` / `deploy` への直接 push と、それらのブランチ上からの push も禁止。

### 4.2 操作境界

明示依頼があれば自動でよい:

- Issue / PR / CI 参照
- Issue 作成・通常編集
- Issue / PR コメント
- PR 作成・通常編集
- feature branch の通常 push

明示依頼のない既存 Issue の close・状態変更・大幅本文変更はしない。既存 PR の close、base 変更、draft/ready 変更、reviewer 変更もしない（`update_pull_request` はそれらも可能なため）。

禁止:

- PR merge
- PR review 提出
- `main` / `master` / `develop` / `deploy` への直接 push
- force push
- protected branch の削除
- Actions workflow の手動実行・rerun
- Repository / Ruleset / Branch Protection の変更
- GitHub 認証情報の表示・変更

GitHub MCP を使う場合、review 提出の機械的境界は `pull_request_review_write` を渡さないことである。`gh` では `gh pr review` を hook / deny で止める。Fine-grained PAT に Pull requests: Write があると、REST では review 提出が権限上可能なので、憲法でも禁止する。トークン経路まで絶対に封じるなら credential 隔離が別途必要である。

### 4.3 MCP Tool Allowlist（GitHub MCP を使う場合）

GitHub MCP は任意である。使う場合だけ、default toolset を丸ごと有効にしない。GitHub MCP の read-only モードも付けない（許可した Issue/PR の write まで消える）。次の 14 個だけを `X-MCP-Tools`（および Codex の `enabled_tools`）に書く。既存の `X-MCP-Toolsets` や default / URL 修飾子は除去する。完成条件は、GitHub MCP を使うとき、エージェントに見えている GitHub MCP tool がこの集合と一致することである。

```text
get_me,issue_read,list_issues,search_issues,issue_write,add_issue_comment,pull_request_read,list_pull_requests,search_pull_requests,create_pull_request,update_pull_request,actions_list,actions_get,get_job_logs
```

渡さない:

```text
merge_pull_request
pull_request_review_write
actions_run_trigger
create_or_update_file
push_files
delete_file
create_repository
update_pull_request_branch
```

`issue_write` は create と update の両方を1 tool で扱う。Allowlist だけでは「作成だけ可・既存更新は不可」を表現できない。初期は憲法で「既存 Issue の更新は明示依頼時のみ」とする。勝手な close が実害になったらその時点で Hook 化する。初期から ask しない。

不足したら後から足してよい候補: `get_commit` / `list_commits`。別 repo 調査が頻発するなら `get_file_contents` / `search_code`。Release / Org 管理は原則足さない。

PAT を使うなら Fine-grained で対象 repo と権限を最小にする。Issues Read and write、Pull requests Read and write、Actions Read-only。Contents / Administration / Secrets は付けない。`X-MCP-Tools` で絞っても、トークンが広いと別経路の被害が大きい。Cursor は OAuth（MCP のブラウザ認証）でもよい。その場合 JSON の Authorization はプレースホルダのままでよい。

### 4.4 Rulesets（ユーザーが GitHub で行う。実装者は触らない）

既存保護があることを仮定しない。ユーザーが default / protected branch に、次と同等の Rulesets または branch protection があることを確認する。無ければユーザーが設定する。

- Require a pull request
- Require approvals
- Require status checks
- Block force pushes
- Block deletion
- AI や通常開発者を不用意に bypass にしない

これなら `git push origin main` が hook を抜けても GitHub 側で拒否される。hook は `--all` / `--mirror` など、ブランチ名がコマンドに出ない入力は止めない。

---

## 5. 憲法に書く文（自己完結。相手の憲法ファイル名で委譲しない）

プロジェクトルートの `AGENTS.md` と `CLAUDE.md` は常設する。今 Claude を使っていなくても両方置く。無いファイルは作成する。次のブロックを**それぞれ自己完結で**入れる。片方を省略しない。同じ本質の重複は問題にしない。一方から他方を「読め / に従え」と書かない。毎ターン読む憲法本文に、相手のファイル名も出さない。

既存ファイルがあるときは、既存の見出し構成を壊さず「外部サービスの操作」を追加または置換する。ファイル全体を無関係な内容で上書きしない。同じファイル内の別節に `aws` / `gh` / GitHub API の競合指示（例: 「GitHub は MCP のみ」「`gh` は使うな」）があれば、その競合部分だけ直す。

```markdown
## 外部サービスの操作

### AWS

- AWS へのアクセスは AWS MCP Server を使う。
- AWS CLI、AWS SDK、絶対パス・相対パスでの AWS CLI 実行、その他の迂回経路は使わない。
- リソースの作成・更新・削除・起動停止・デプロイ・権限変更など状態変更はしない。必要な変更は実行せずユーザーへ提示する。

### GitHub

- GitHub 操作には、公式 GitHub MCP Server または GitHub CLI（`gh`）を使用してよい。一方が利用できない場合は、可能であれば他方を試す。
- 明示依頼があれば自動で行ってよい: Issue / PR / CI の参照、Issue 作成・通常編集、Issue・PR へのコメント、PR 作成・通常編集、feature branch の通常 push。
- 既存 Issue の更新は、ユーザーから明示的に依頼された場合のみ行う。依頼されていない Issue の close、状態変更、大幅な本文変更は行わない。
- 既存 PR についても同様。明示依頼のない close、base 変更、draft/ready 変更、reviewer 変更は行わない。
- 禁止: PR merge、PR review 提出、`main` / `master` / `develop` / `deploy` への直接 push、force push、protected branch の削除、Actions workflow の手動実行・rerun、Repository / Ruleset / Branch Protection の変更。
- GitHub 認証情報の表示・変更は行わない。
```

Claude 向け `CLAUDE.md` では AWS の先頭を次にしてよい。

```markdown
- AWS へのアクセスは AWS MCP Server を使う（プラグインまたは MCP 設定のどちらか一方）。
```

運用説明ファイル（後述）には、層構造、IAM JSON、`--read-only` を付けない理由、GitHub allowlist、ユーザー作業を同じ内容で書く。`--read-only` を推奨とは書かない。

---

## 6. ツール別の補助制御

Cloud エージェントはユーザーのホームを読めない。hook・憲法・Cursor rules はリポジトリ内に置く。ホームだけに置かない。command パスはプロジェクト相対にする。AWS MCP 接続はこの文書ではホーム設定を案内する。GitHub は GitHub MCP がなくても認証済み `gh` があれば操作できる。Cloud 側に account / project MCP を置ける製品ならユーザーが AWS MCP（必要なら GitHub MCP）をそこで登録する。実装者はホームにも Cloud 設定にも書き込まない。

標準は全クライアント対応を常設する。Cursor / Claude / Windsurf の hook と、`AGENTS.md` / `CLAUDE.md` は、今そのツールを使っていなくても全部置く。第 9 節のテストが三系統を見る。Codex の rules だけ、使う場合に足す。既存の `.claude/settings.json` があるときは deny と PreToolUse をマージする。同じガードを二重登録しない。

### 6.1 Claude Code

既存の `.claude/settings.json` があるなら、`permissions.deny` に `Bash(aws *)` と危険な `gh` サブコマンド（merge / review / workflow run / run rerun / repo 管理 / auth）を足し、PreToolUse が下記ガードを呼ぶようにする。既存の deny / allow / sandbox / 他 hook は消さない。`Bash(gh *)` は付けない。

無いなら次を置く。`ask` に `mcp__github__issue_write` は初期は付けない。ホームの `$HOME/.claude/hooks/...` にはしない。JSON パース失敗は exit 2。

```json
{
  "permissions": {
    "deny": [
      "Bash(aws *)",
      "Bash(gh pr merge)",
      "Bash(gh pr merge *)",
      "Bash(gh pr review)",
      "Bash(gh pr review *)",
      "Bash(gh workflow run)",
      "Bash(gh workflow run *)",
      "Bash(gh run rerun)",
      "Bash(gh run rerun *)",
      "Bash(gh repo delete)",
      "Bash(gh repo delete *)",
      "Bash(gh repo archive)",
      "Bash(gh repo archive *)",
      "Bash(gh repo edit)",
      "Bash(gh repo edit *)",
      "Bash(gh auth token)",
      "Bash(gh auth token *)",
      "Bash(gh auth login)",
      "Bash(gh auth login *)",
      "Bash(gh auth logout)",
      "Bash(gh auth logout *)",
      "Bash(gh auth refresh)",
      "Bash(gh auth refresh *)",
      "Bash(git push --force)",
      "Bash(git push --force *)",
      "Bash(git push -f)",
      "Bash(git push -f *)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/pretooluse_guard.sh"
          }
        ]
      }
    ]
  }
}
```

### 6.2 Codex

使う場合のみ。既存の `.codex/rules` に次を足す。infra の prompt リストに `aws` が入っていたら外し、単独の forbidden にする。

```python
prefix_rule(
    pattern = ["aws"],
    decision = "forbidden",
    justification = "Use AWS MCP Server instead of aws CLI.",
)

prefix_rule(
    pattern = ["gh", "pr", "merge"],
    decision = "forbidden",
    justification = "PR merge is reserved for humans.",
)

prefix_rule(
    pattern = ["gh", "pr", "review"],
    decision = "forbidden",
    justification = "PR review submission is reserved for humans.",
)

prefix_rule(
    pattern = ["gh", "workflow", "run"],
    decision = "forbidden",
    justification = "Manual Actions dispatch is forbidden.",
)

prefix_rule(
    pattern = ["gh", "run", "rerun"],
    decision = "forbidden",
    justification = "Actions rerun is forbidden.",
)

prefix_rule(
    pattern = ["gh", "repo", ["delete", "archive", "edit"]],
    decision = "forbidden",
    justification = "Repository admin operations are forbidden.",
)

prefix_rule(
    pattern = ["gh", "auth", ["token", "login", "logout", "refresh"]],
    decision = "forbidden",
    justification = "GitHub credential display or mutation is forbidden.",
)

prefix_rule(
    pattern = ["git", "push", "--force"],
    decision = "forbidden",
    justification = "Force push is forbidden for safety.",
)

prefix_rule(
    pattern = ["git", "push", "--force-with-lease"],
    decision = "forbidden",
    justification = "Force push is forbidden for safety.",
)

prefix_rule(
    pattern = ["git", "push", "-f"],
    decision = "forbidden",
    justification = "Force push is forbidden for safety.",
)
```

Codex Cloud の本線は repo の `AGENTS.md`。`.codex/rules` は Cloud 防御に数えない、と運用説明に書く。

### 6.3 Cursor

`.cursor/hooks.json`:

```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      {
        "command": "bash .cursor/hooks/check-external-services.sh",
        "failClosed": true
      }
    ]
  }
}
```

`.cursor/rules/external-services-safety.mdc`（alwaysApply）:

```markdown
---
description: AWS/GitHub 操作の安全方針（Cloud Agent 含む）
alwaysApply: true
---

# 外部サービス安全

- AWS は AWS MCP Server 経由のみ。raw `aws` CLI / SDK は使わない。状態変更はしない。
- GitHub 操作には公式 GitHub MCP または `gh` を使ってよい。一方が使えなければ他方を試す。
- 明示依頼があれば: Issue/PR/CI 参照、Issue 作成・通常編集、コメント、PR 作成・通常編集、feature branch の通常 push。
- 明示依頼のない既存 Issue/PR の close・状態変更・大幅本文変更・base/reviewer 変更はしない。
- 禁止: PR merge、review 提出、`main` / `master` / `develop` / `deploy` 直接 push、force push、Actions 手動起動・rerun、Ruleset/設定変更、認証情報の表示・変更。
- Agent 直下の `gh workflow run` / `gh run rerun` は禁止。例外は公式 babysit-pr watcher による current PR の flaky/unrelated failed checks の bounded rerun（最大 3 cycle）のみ。
```

`.cursor/permissions.json` は使わない。

### 6.4 Windsurf

`pre_run_command` と `pre_mcp_tool_use` の両方に同じスクリプトを繋ぐ。スクリプトは `command_line` だけ見る。MCP イベントは command が空なので通過する。MCP 制限は `X-MCP-Tools` 側。パース失敗は exit 2。

```json
{
  "hooks": {
    "pre_run_command": [
      {
        "command": "bash .windsurf/hooks/check-external-services.sh",
        "show_output": true
      }
    ],
    "pre_mcp_tool_use": [
      {
        "command": "bash .windsurf/hooks/check-external-services.sh",
        "show_output": true
      }
    ]
  }
}
```

### 6.5 Gemini / Antigravity（使う場合のみ。ユーザーのホーム作業）

MCP JSON は Cursor と同じ（`--read-only` なし、`--metadata` の作業リージョン。`env.AWS_REGION` は必須ではない）。置き場は `~/.gemini/antigravity/mcp_config.json`。実装者はホームへ書かない。完了報告に載せる。

---

## 7. hook スクリプトの完成形

3 系統とも同じ判定にする。入出力だけ変える。実行ビットを付ける。

共通判定:

- 引用符は剥がさない（aws/gh/git 判定）
- `cli_command name`: `(^|[;|&]|$(|backtick))` のあと任意のパス末尾、そのあと `name`、そのあと空白 / `;|&` / 終端
- `gh_subcmd`: コマンド位置の `gh` に続く危険サブコマンドだけ止める。日常的な `gh pr view` 等は通す
- `git push` も同じコマンド位置
- force: `--force` / `--force-with-lease`（`=` 付き含む）。`-f` は `git push` の引数だけ（`git push && ls -f` は落とさない）。`+branch` も force
- 保護ブランチ: コマンドに `main|master|develop|deploy` が明示、または `refs/heads/...`、または cwd の HEAD がそれら（空リポジトリでは `symbolic-ref --short HEAD` を先に使う）
- jq 失敗は deny / exit 2。空コマンドは allow（Windsurf の MCP イベント用）

### 7.1 Cursor（`.cursor/hooks/check-external-services.sh`）

```bash
#!/usr/bin/env bash
# Cursor beforeShellExecution guard (project / Cloud Agent 向け)。
# プロジェクトルート相対で実行される。stdin: Cursor hook JSON。
# stdout: {"permission":"allow"|"deny"|"ask","user_message":"..."}
# CLI 起動の best-effort 抑止。SDK・未列挙ラッパは対象外（IAM / Rulesets が本丸）。
set -euo pipefail

input="$(cat)"

deny() {
  jq -n --arg msg "$1" '{permission:"deny",user_message:$msg}'
  exit 0
}

allow() {
  echo '{"permission":"allow"}'
  exit 0
}

cmd="$(jq -r '.command // .tool_input.command // empty' <<<"$input")" || deny "hook input parse failed"
cwd="$(jq -r '.cwd // empty' <<<"$input")" || cwd=""

[[ -z "$cmd" ]] && allow

cmd_scan="$(printf '%s' "$cmd" | tr -d "'\"")"

# fork bomb
if grep -Eq ':\(\)[[:space:]]*\{[[:space:]]*:[[:space:]]*\|[[:space:]]*:[[:space:]]*&[[:space:]]*\}[[:space:]]*;[[:space:]]*:' <<<"$cmd_scan"; then
  deny "Fork bomb pattern is forbidden for AI agents."
fi

# 危険な rm -rf 対象
if grep -Eq '(^|[[:space:];|&])(command[[:space:]]+rm|/usr/bin/rm|/bin/rm|/sbin/rm|/usr/local/bin/rm|/opt/homebrew/bin/rm|rm)[[:space:]]+' <<<"$cmd_scan"; then
  if grep -Eq '(^|[[:space:]])(--force|--recursive|-rf|-fr|-r[[:space:]]+-f|-f[[:space:]]+-r)([[:space:]]|$)' <<<"$cmd_scan"; then
    if grep -Eq '(^|[[:space:]])(/|/\*|~|~/?\*|\$HOME|\$HOME/?\*|\.|\.\/|\.\.|\.\.\/)([[:space:]]|$)' <<<"$cmd_scan"; then
      deny "Destructive rm target is forbidden for AI agents."
    fi
    if grep -Eq '(^|[[:space:]])/(etc|bin|sbin|usr|var|System|Library|Applications|opt/homebrew)(/|\*|[[:space:]]|$)' <<<"$cmd_scan"; then
      deny "Destructive rm system path is forbidden for AI agents."
    fi
    if grep -Eq '(^|[[:space:]])(~/(Desktop|Documents|Downloads|Library|\.ssh|\.aws|\.gcp|\.docker|\.kube|\.gnupg)(/|\*|[[:space:]]|$)|\$HOME/(Desktop|Documents|Downloads|Library|\.ssh|\.aws|\.gcp|\.docker|\.kube|\.gnupg)(/|\*|[[:space:]]|$))' <<<"$cmd_scan"; then
      deny "Destructive rm protected home path is forbidden for AI agents."
    fi
  fi
fi

if grep -Eq '(^|[[:space:];|&])dd([[:space:]]|$).*([[:space:]]if=|[[:space:]]of=)' <<<"$cmd_scan"; then
  deny "dd if/of pattern is forbidden for AI agents."
fi

if grep -Eq '(^|[[:space:];|&])(curl|wget)([[:space:]]|$).*?\|[[:space:]]*(sh|bash|zsh)([[:space:]]|$)' <<<"$cmd_scan"; then
  deny "Download piped to shell is forbidden for AI agents."
fi

if grep -Eq '(^|[[:space:];|&])(sh|bash|zsh)[[:space:]]+-c([[:space:]]|$)' <<<"$cmd_scan"; then
  if grep -Eq '\$\([[:space:]]*(curl|wget)([[:space:]]|$)' <<<"$cmd_scan"; then
    deny "Shell -c with download substitution is forbidden for AI agents."
  fi
fi

# コマンド位置（先頭、または ;|&(){} $() backtick の直後）。引用符は剥がさない。
cli_command() {
  local name="$1"
  grep -Eq "(^|[;|&({]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?${name}([[:space:]|;|&]|$)" <<<"$cmd"
}

git_push_command() {
  grep -Eq "(^|[;|&({]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?git[[:space:]]+push([[:space:]|;|&]|$)" <<<"$cmd"
}

gh_subcmd() {
  local sub="$1"
  grep -Eq "(^|[;|&({]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?gh[[:space:]]+${sub}([[:space:]|;|&]|$)" <<<"$cmd"
}

gh_api_has_field_flag() {
  grep -Eq '(^|[[:space:]])(-f[[:space:]]|--field|--raw-field|-F[[:space:]])([[:space:]|=]|$)' <<<"$cmd" ||
    grep -Eq '(^|[[:space:]])-f[^[:space:]-]' <<<"$cmd"
}

gh_api_has_explicit_get() {
  grep -Eqi '(^|[[:space:]])(-X|--method)[[:space:]]+GET($|[[:space:];&)])' <<<"$cmd"
}

if cli_command aws; then
  deny "Use AWS MCP Server instead of aws CLI."
fi

if cli_command gh; then
  if gh_subcmd 'pr[[:space:]]+(merge|review)'; then
    deny "Forbidden gh command: pr merge/review."
  fi
  if gh_subcmd 'workflow[[:space:]]+run'; then
    deny "Forbidden gh command: workflow run."
  fi
  if gh_subcmd 'run[[:space:]]+rerun'; then
    deny "Forbidden gh command: run rerun."
  fi
  if gh_subcmd 'repo[[:space:]]+(delete|archive|edit)'; then
    deny "Forbidden gh command: repository admin."
  fi
  if gh_subcmd 'auth[[:space:]]+(token|login|logout|refresh)'; then
    deny "Forbidden gh command: auth token/login/logout/refresh."
  fi
  if gh_subcmd 'api'; then
    if grep -Eqi '(^|[[:space:]])(-X|--method)[[:space:]]+(POST|PUT|PATCH|DELETE)([[:space:]]|$)' <<<"$cmd"; then
      deny "Mutating gh api is forbidden."
    fi
    if grep -Eq '(^|[[:space:]])(--input)([[:space:]|=]|$)' <<<"$cmd"; then
      deny "Mutating gh api is forbidden."
    fi
  # -f/--field on explicit GET are query params (official babysit-pr watcher).
    if gh_api_has_field_flag && ! gh_api_has_explicit_get; then
      deny "Mutating gh api is forbidden."
    fi
  fi
fi

if git_push_command; then
  if grep -Eq '(^|[[:space:]])(--force|--force-with-lease)(=|[[:space:]]|$)' <<<"$cmd"; then
    deny "Force push is forbidden for AI agents."
  fi
  if grep -Eq 'git[[:space:]]+push[[:space:]]([^;&|]*[[:space:]])?-f([[:space:]|=]|$)' <<<"$cmd"; then
    deny "Force push is forbidden for AI agents."
  fi
  if grep -Eq 'git[[:space:]]+push[[:space:]][^;&|]*\+[A-Za-z0-9._/-]+' <<<"$cmd"; then
    deny "Force push is forbidden for AI agents."
  fi
  if grep -Eq '(^|[[:space:]]|:)(main|master|develop|deploy)([[:space:]]|$)' <<<"$cmd"; then
    deny "Push to protected branch is forbidden for AI agents."
  fi
  if grep -Eq 'refs/heads/(main|master|develop|deploy)([[:space:]:^~]|$)' <<<"$cmd"; then
    deny "Push to protected branch is forbidden for AI agents."
  fi
  if [[ -n "$cwd" ]] && git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    branch="$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null || git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
    if [[ "$branch" =~ ^(main|master|develop|deploy)$ ]]; then
      deny "Push from protected branch '$branch' is forbidden for AI agents."
    fi
  fi
fi

allow
```

### 7.2 Windsurf（`.windsurf/hooks/check-external-services.sh`）

判定は Cursor と同じ。stdout JSON ではなく `echo "Blocked: ..." >&2; exit 2`。stdin は `.tool_info.command_line`。cwd は `.cwd // .tool_info.cwd`。jq 失敗は exit 2。空コマンドは exit 0。

```bash
#!/usr/bin/env bash
# Windsurf pre_run_command / pre_mcp_tool_use guard.
# Exit 2 blocks the action. Exit 0 allows.
# Windsurf stdin: tool_info.command_line / tool_info.mcp_* （公式 Cascade Hooks）
# CLI 起動の best-effort 抑止。SDK・未列挙ラッパは対象外（IAM / Rulesets が本丸）。
# pre_mcp_tool_use は command_line が空なので通過する。MCP 制限は X-MCP-Tools 側。
set -euo pipefail

input="$(cat)"

block() {
  echo "Blocked: $1" >&2
  exit 2
}

cmd="$(jq -r '.tool_info.command_line // empty' <<<"$input")" || block "hook input parse failed"
cwd="$(jq -r '.cwd // .tool_info.cwd // empty' <<<"$input")" || cwd=""

[[ -z "$cmd" ]] && exit 0

cmd_scan="$(printf '%s' "$cmd" | tr -d "'\"")"

if grep -Eq ':\(\)[[:space:]]*\{[[:space:]]*:[[:space:]]*\|[[:space:]]*:[[:space:]]*&[[:space:]]*\}[[:space:]]*;[[:space:]]*:' <<<"$cmd_scan"; then
  block "fork bomb pattern"
fi

if grep -Eq '(^|[[:space:];|&])(command[[:space:]]+rm|/usr/bin/rm|/bin/rm|/sbin/rm|/usr/local/bin/rm|/opt/homebrew/bin/rm|rm)[[:space:]]+' <<<"$cmd_scan"; then
  if grep -Eq '(^|[[:space:]])(--force|--recursive|-rf|-fr|-r[[:space:]]+-f|-f[[:space:]]+-r)([[:space:]]|$)' <<<"$cmd_scan"; then
    if grep -Eq '(^|[[:space:]])(/|/\*|~|~/?\*|\$HOME|\$HOME/?\*|\.|\.\/|\.\.|\.\.\/)([[:space:]]|$)' <<<"$cmd_scan"; then
      block "destructive rm target"
    fi
    if grep -Eq '(^|[[:space:]])/(etc|bin|sbin|usr|var|System|Library|Applications|opt/homebrew)(/|\*|[[:space:]]|$)' <<<"$cmd_scan"; then
      block "destructive rm system path"
    fi
    if grep -Eq '(^|[[:space:]])(~/(Desktop|Documents|Downloads|Library|\.ssh|\.aws|\.gcp|\.docker|\.kube|\.gnupg)(/|\*|[[:space:]]|$)|\$HOME/(Desktop|Documents|Downloads|Library|\.ssh|\.aws|\.gcp|\.docker|\.kube|\.gnupg)(/|\*|[[:space:]]|$))' <<<"$cmd_scan"; then
      block "destructive rm protected home path"
    fi
  fi
fi

if grep -Eq '(^|[[:space:];|&])dd([[:space:]]|$).*([[:space:]]if=|[[:space:]]of=)' <<<"$cmd_scan"; then
  block "dd if/of pattern"
fi

if grep -Eq '(^|[[:space:];|&])(curl|wget)([[:space:]]|$).*?\|[[:space:]]*(sh|bash|zsh)([[:space:]]|$)' <<<"$cmd_scan"; then
  block "download piped to shell"
fi

if grep -Eq '(^|[[:space:];|&])(sh|bash|zsh)[[:space:]]+-c([[:space:]]|$)' <<<"$cmd_scan"; then
  if grep -Eq '\$\([[:space:]]*(curl|wget)([[:space:]]|$)' <<<"$cmd_scan"; then
    block "shell -c with download substitution"
  fi
fi

cli_command() {
  local name="$1"
  grep -Eq "(^|[;|&({]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?${name}([[:space:]|;|&]|$)" <<<"$cmd"
}

git_push_command() {
  grep -Eq "(^|[;|&({]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?git[[:space:]]+push([[:space:]|;|&]|$)" <<<"$cmd"
}

gh_subcmd() {
  local sub="$1"
  grep -Eq "(^|[;|&({]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?gh[[:space:]]+${sub}([[:space:]|;|&]|$)" <<<"$cmd"
}

gh_api_has_field_flag() {
  grep -Eq '(^|[[:space:]])(-f[[:space:]]|--field|--raw-field|-F[[:space:]])([[:space:]|=]|$)' <<<"$cmd" ||
    grep -Eq '(^|[[:space:]])-f[^[:space:]-]' <<<"$cmd"
}

gh_api_has_explicit_get() {
  grep -Eqi '(^|[[:space:]])(-X|--method)[[:space:]]+GET($|[[:space:];&)])' <<<"$cmd"
}

if cli_command aws; then
  block "aws CLI (use AWS MCP Server)"
fi

if cli_command gh; then
  if gh_subcmd 'pr[[:space:]]+(merge|review)'; then
    block "dangerous gh command (pr merge/review)"
  fi
  if gh_subcmd 'workflow[[:space:]]+run'; then
    block "dangerous gh command (workflow run)"
  fi
  if gh_subcmd 'run[[:space:]]+rerun'; then
    block "dangerous gh command (run rerun)"
  fi
  if gh_subcmd 'repo[[:space:]]+(delete|archive|edit)'; then
    block "dangerous gh command (repo admin)"
  fi
  if gh_subcmd 'auth[[:space:]]+(token|login|logout|refresh)'; then
    block "dangerous gh command (auth)"
  fi
  if gh_subcmd 'api'; then
    if grep -Eqi '(^|[[:space:]])(-X|--method)[[:space:]]+(POST|PUT|PATCH|DELETE)([[:space:]]|$)' <<<"$cmd"; then
      block "mutating gh api"
    fi
    if grep -Eq '(^|[[:space:]])(--input)([[:space:]|=]|$)' <<<"$cmd"; then
      block "mutating gh api"
    fi
    if gh_api_has_field_flag && ! gh_api_has_explicit_get; then
      block "mutating gh api"
    fi
  fi
fi

if git_push_command; then
  if grep -Eq '(^|[[:space:]])(--force|--force-with-lease)(=|[[:space:]]|$)' <<<"$cmd"; then
    block "force push"
  fi
  if grep -Eq 'git[[:space:]]+push[[:space:]]([^;&|]*[[:space:]])?-f([[:space:]|=]|$)' <<<"$cmd"; then
    block "force push"
  fi
  if grep -Eq 'git[[:space:]]+push[[:space:]][^;&|]*\+[A-Za-z0-9._/-]+' <<<"$cmd"; then
    block "force push"
  fi
  if grep -Eq '(^|[[:space:]]|:)(main|master|develop|deploy)([[:space:]]|$)' <<<"$cmd"; then
    block "push to protected branch"
  fi
  if grep -Eq 'refs/heads/(main|master|develop|deploy)([[:space:]:^~]|$)' <<<"$cmd"; then
    block "push to protected branch"
  fi
  if [[ -n "$cwd" ]] && git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    branch="$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null || git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
    if [[ "$branch" =~ ^(main|master|develop|deploy)$ ]]; then
      block "push from protected branch '$branch'"
    fi
  fi
fi

exit 0
```

### 7.3 Claude（`.claude/hooks/pretooluse_guard.sh`）

`tool_name` が `Bash` のときだけ見る。既存の危険コマンド検査があるなら残し、aws / 危険な gh サブコマンド / git push は上記と同じ関数にする。無ければ次を置く。fork bomb / 危険な rm / dd / curl|sh は `cmd_scan`（引用符除去）で見てよい。aws/gh/git は引用符を剥がさない `cmd` で見る。

```bash
#!/usr/bin/env bash
set -euo pipefail

input="$(cat)"
if ! tool="$(jq -r '.tool_name // ""' <<<"$input")" \
  || ! cmd="$(jq -r '.tool_input.command // ""' <<<"$input")" \
  || ! cwd="$(jq -r '.cwd // ""' <<<"$input")"; then
  echo "Blocked: hook parse failed" >&2
  exit 2
fi
cmd_scan="$(printf '%s' "$cmd" | tr -d "'\"")"

[[ "$tool" == "Bash" ]] || exit 0
[[ -n "$cmd" ]] || exit 0

block() {
  echo "Blocked: $1" >&2
  echo "Command: $cmd" >&2
  exit 2
}

# fork bomb
if grep -Eq ':\(\)[[:space:]]*\{[[:space:]]*:[[:space:]]*\|[[:space:]]*:[[:space:]]*&[[:space:]]*\}[[:space:]]*;[[:space:]]*:' <<<"$cmd_scan"; then
  block "fork bomb pattern"
fi

# rm -rf / rm -fr / rm --recursive --force のうち、危険な削除対象だけ止める。
# プロジェクト内の rm -rf ./dist, ./build, ./node_modules, ./.claude/skills/foo などは sandbox に任せる。
if grep -Eq '(^|[[:space:];|&])(command[[:space:]]+rm|/usr/bin/rm|/bin/rm|/sbin/rm|/usr/local/bin/rm|/opt/homebrew/bin/rm|rm)[[:space:]]+' <<<"$cmd_scan"; then
  if grep -Eq '(^|[[:space:]])(--force|--recursive|-rf|-fr|-r[[:space:]]+-f|-f[[:space:]]+-r)([[:space:]]|$)' <<<"$cmd_scan"; then
    if grep -Eq '(^|[[:space:]])(/|/\*|~|~/?\*|\$HOME|\$HOME/?\*|\.|\.\/|\.\.|\.\.\/)([[:space:]]|$)' <<<"$cmd_scan"; then
      block "destructive rm target"
    fi
    if grep -Eq '(^|[[:space:]])/(etc|bin|sbin|usr|var|System|Library|Applications|opt/homebrew)(/|\*|[[:space:]]|$)' <<<"$cmd_scan"; then
      block "destructive rm system path"
    fi
    if grep -Eq '(^|[[:space:]])(~/(Desktop|Documents|Downloads|Library|\.ssh|\.aws|\.gcp|\.docker|\.kube|\.gnupg)(/|\*|[[:space:]]|$)|\$HOME/(Desktop|Documents|Downloads|Library|\.ssh|\.aws|\.gcp|\.docker|\.kube|\.gnupg)(/|\*|[[:space:]]|$))' <<<"$cmd_scan"; then
      block "destructive rm protected home path"
    fi
  fi
fi

# dd if= / of= はディスク破壊・大量上書きリスクが高いので止める
if grep -Eq '(^|[[:space:];|&])dd([[:space:]]|$).*([[:space:]]if=|[[:space:]]of=)' <<<"$cmd_scan"; then
  block "dd if/of pattern"
fi

# curl/wget piped to shell
if grep -Eq '(^|[[:space:];|&])(curl|wget)([[:space:]]|$).*?\|[[:space:]]*(sh|bash|zsh)([[:space:]]|$)' <<<"$cmd_scan"; then
  block "download piped to shell"
fi

# sh -c "$(curl ...)" / bash -c "$(wget ...)" 系
if grep -Eq '(^|[[:space:];|&])(sh|bash|zsh)[[:space:]]+-c([[:space:]]|$)' <<<"$cmd_scan"; then
  if grep -Eq '\$\([[:space:]]*(curl|wget)([[:space:]]|$)' <<<"$cmd_scan"; then
    block "shell -c with download substitution"
  fi
fi

# コマンド位置の aws を抑止。gh は危険サブコマンドだけ止める（引用符は剥がさない。SDK は対象外）
cli_command() {
  local name="$1"
  grep -Eq "(^|[;|&({]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?${name}([[:space:]|;|&]|$)" <<<"$cmd"
}

git_push_command() {
  grep -Eq "(^|[;|&({]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?git[[:space:]]+push([[:space:]|;|&]|$)" <<<"$cmd"
}

gh_subcmd() {
  local sub="$1"
  grep -Eq "(^|[;|&({]|\\$\\(|\`)[[:space:]]*([^[:space:]\"']*/)?gh[[:space:]]+${sub}([[:space:]|;|&]|$)" <<<"$cmd"
}

gh_api_has_field_flag() {
  grep -Eq '(^|[[:space:]])(-f[[:space:]]|--field|--raw-field|-F[[:space:]])([[:space:]|=]|$)' <<<"$cmd" ||
    grep -Eq '(^|[[:space:]])-f[^[:space:]-]' <<<"$cmd"
}

gh_api_has_explicit_get() {
  grep -Eqi '(^|[[:space:]])(-X|--method)[[:space:]]+GET($|[[:space:];&)])' <<<"$cmd"
}

if cli_command aws; then
  block "aws CLI (use AWS MCP Server)"
fi

if cli_command gh; then
  if gh_subcmd 'pr[[:space:]]+(merge|review)'; then
    block "dangerous gh command (pr merge/review)"
  fi
  if gh_subcmd 'workflow[[:space:]]+run'; then
    block "dangerous gh command (workflow run)"
  fi
  if gh_subcmd 'run[[:space:]]+rerun'; then
    block "dangerous gh command (run rerun)"
  fi
  if gh_subcmd 'repo[[:space:]]+(delete|archive|edit)'; then
    block "dangerous gh command (repo admin)"
  fi
  if gh_subcmd 'auth[[:space:]]+(token|login|logout|refresh)'; then
    block "dangerous gh command (auth)"
  fi
  if gh_subcmd 'api'; then
    if grep -Eqi '(^|[[:space:]])(-X|--method)[[:space:]]+(POST|PUT|PATCH|DELETE)([[:space:]]|$)' <<<"$cmd"; then
      block "mutating gh api"
    fi
    if grep -Eq '(^|[[:space:]])(--input)([[:space:]|=]|$)' <<<"$cmd"; then
      block "mutating gh api"
    fi
    # -f/--field on explicit GET are query params (official babysit-pr watcher).
    if gh_api_has_field_flag && ! gh_api_has_explicit_get; then
      block "mutating gh api"
    fi
  fi
fi

if git_push_command; then
  if grep -Eq '(^|[[:space:]])(--force|--force-with-lease)(=|[[:space:]]|$)' <<<"$cmd"; then
    block "force push"
  fi
  if grep -Eq 'git[[:space:]]+push[[:space:]]([^;&|]*[[:space:]])?-f([[:space:]|=]|$)' <<<"$cmd"; then
    block "force push"
  fi
  if grep -Eq 'git[[:space:]]+push[[:space:]][^;&|]*\+[A-Za-z0-9._/-]+' <<<"$cmd"; then
    block "force push"
  fi
  if grep -Eq '(^|[[:space:]]|:)(main|master|develop|deploy)([[:space:]]|$)' <<<"$cmd"; then
    block "push to protected branch (explicit)"
  fi
  if grep -Eq 'refs/heads/(main|master|develop|deploy)([[:space:]:^~]|$)' <<<"$cmd"; then
    block "push to protected branch (refspec)"
  fi
  if [[ -n "$cwd" ]] && git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    branch="$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null || git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
    if [[ "$branch" =~ ^(main|master|develop|deploy)$ ]]; then
      block "push from protected branch '$branch'"
    fi
  fi
fi

exit 0
```

---

## 8. このプロジェクトへ置くファイル

秘密入り MCP はリポジトリに置かない。次をプロジェクトルート基準で置く。既存ファイルはマージする。

| ファイル                                     | 内容                                                                        |
| -------------------------------------------- | --------------------------------------------------------------------------- |
| `AGENTS.md`                                  | 第 5 節の外部サービス節                                                     |
| `CLAUDE.md`                                  | 同じ本質（Claude 向け一文を足してよい）。常設                               |
| `docs/AI_EXTERNAL_SERVICES.md`               | 第 1・3・4 節と第 11 節のユーザー作業を、この文書の本文どおり写す           |
| `.claude/settings.json`                      | deny に `Bash(aws *)` と危険な `gh` サブコマンド、PreToolUse がガードを呼ぶ |
| `.claude/hooks/pretooluse_guard.sh`          | 第 7.3 節                                                                   |
| `.cursor/hooks.json`                         | 第 6.3 節                                                                   |
| `.cursor/hooks/check-external-services.sh`   | 第 7.1 節                                                                   |
| `.cursor/rules/external-services-safety.mdc` | 第 6.3 節                                                                   |
| `.codex/rules/` 配下                         | 使う場合のみ第 6.2 節                                                       |
| `.windsurf/hooks.json`                       | 第 6.4 節                                                                   |
| `.windsurf/hooks/check-external-services.sh` | 第 7.2 節                                                                   |
| `scripts/validate-external-service-hooks.sh` | 第 9 節                                                                     |

`docs/AI_EXTERNAL_SERVICES.md` にも「他のファイルを読め」とは書かない。IAM JSON、MCP JSON、allowlist、ホームの置き場を本文に含める。

---

## 9. hook の自動テスト

`scripts/validate-external-service-hooks.sh` を次の内容で置く。テストランナーのコマンドラインに `aws` / `gh` を出さない（stdin JSON で hook を叩く）。`jq --arg` は名前と値を別引数にする。`--arg cwd="$cwd"` は使わない（JSON が `null` になり、deny 検証が壊れる）。`package.json` があるなら `"hooks:check": "bash scripts/validate-external-service-hooks.sh"` を足す。無いなら完了時に `bash scripts/validate-external-service-hooks.sh` を実行する。

```bash
#!/usr/bin/env bash
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
allow_all "gh api repos/owner/repo/actions/runs -X GET -fhead_sha=abc -fper_page=100"
allow_all "gh api repos/owner/repo/actions/runs -X GET -if head_sha=abc"
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
deny_all 'gh api repos/owner/repo/pulls/1/reviews -f event=APPROVE < <(gh api repos/owner/repo/pulls/1 -X GET )'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -f event=APPROVE >(gh api repos/owner/repo/pulls/1 -X GET)'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X GET -X "$m" -f event=APPROVE'
deny_all 'm=POST; gh api repos/owner/repo/pulls/1/reviews -X GET -X "$m" -f event=APPROVE'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X GET --method="$m" -f event=APPROVE'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X GET -X"$m" -f event=APPROVE'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X "$m" -f event=APPROVE'
deny_all 'gh api repos/owner/repo/pulls/1/reviews --method GET --method=POST -f event=APPROVE'
deny_all '(gh api repos/owner/repo/pulls/1/reviews -f event=APPROVE; gh api repos/owner/repo/pulls/1 -X GET)'
deny_all '{ gh api repos/owner/repo/pulls/1/reviews -f event=APPROVE; gh api repos/owner/repo/pulls/1 -X GET; }'
deny_all 'm=-; m+=X; n=POST; gh api repos/owner/repo/pulls/1/reviews -f event=APPROVE -X GET $m $n'
deny_all 'm=-; m+=X; set -- "$m" POST; gh api repos/owner/repo/pulls/1/reviews -X GET -f event=APPROVE "$@"'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X GET -f event=APPROVE $*'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X GET -f event=APPROVE $1'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X GET -f event=APPROVE -\X P\O\S\T'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X GET -f event=APPROVE --\method POST'
deny_all "gh api repos/owner/repo/pulls/1/reviews -X GET -'X' POST -f event=APPROVE"
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X GET -"X" POST -f event=APPROVE'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X GET ?X POST -f event=APPROVE'
deny_all 'gh api repos/owner/repo/pulls/1/reviews -X GET *X POST -f event=APPROVE'
deny_all "gh api repos/owner/repo/pulls/1/reviews -X GET -\$'X' POST -f event=APPROVE"
deny_all "gh api repos/owner/repo/pulls/1/reviews -fevent=APPROVE"
deny_all "gh api repos/owner/repo/pulls/1/reviews -Fevent=APPROVE"
deny_all "gh api repos/owner/repo/pulls/1/reviews -if event=APPROVE"
deny_all "gh api repos/owner/repo/pulls/1/reviews -iF event=APPROVE"
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
```

---

## 10. 検証

- `bash scripts/validate-external-service-hooks.sh`（または `npm run hooks:check`）
- 触った Markdown / JSON の format と lint（プロジェクトにコマンドがある場合）

jq と bash が必要。無い検証は「未検証」とコマンドを報告する。成功と書かない。

---

## 11. 完了報告で必ず伝えること（コード完了 ≠ 目的完了）

実装者は IAM もホーム MCP も GitHub Rulesets も触らない。完了報告の先頭近くに、次の3項目をそれぞれ **未完 / 確認済み** で書く。

### 今のコードだけで起きること

- AI は raw `aws` を使えない（hook・deny・憲法）
- AI の日常的な `gh`（view / list / create / comment 等）は通る。merge / review 提出 / Actions 手動実行 / repo 管理 / 認証情報の表示変更 / mutating `gh api` は止まる
- AWS MCP が未登録なら AWS 参照はできない。GitHub は GitHub MCP がなくても認証済み `gh` があれば操作できる
- IAM 未設定なら、MCP 登録後の `run_script` は Role が許す範囲で更新・削除も呼べる
- Rulesets 未確認なら、hook を抜けた `main` / `master` / `develop` / `deploy` / force 系 push を GitHub 側で止められないことがある

### 1. 参照を通す（MCP 登録）— ユーザー作業

AWS 参照には、使う AI ツールごとに AWS MCP を通す。GitHub MCP は任意。使うなら第 4.3 節の allowlist を設定する。`gh` が認証済みなら GitHub MCP なしでも GitHub 操作は可能。リポジトリに実トークンを埋め込まない。既存の他 MCP は消さない。GitHub MCP を使う場合は、最終的に見えている tool が第 4.3 節の 14 個だけになるまで、既存の広い toolset を除去する。AWS / GitHub ともに read-only モードは付けない。

**Local**

- Cursor: `~/.cursor/mcp.json`。GitHub MCP を使うなら OAuth 再認証、またはホーム側だけ PAT
- Claude Code: プラグインかユーザー設定の `aws-mcp` のどちらか一方。GitHub MCP を使うなら `GITHUB_PAT` を環境変数で入れる
- Codex: `~/.codex/config.toml` の `[mcp_servers.aws-mcp]`。GitHub MCP を使うなら `[mcp_servers.github]` と `GITHUB_PAT`
- Windsurf: `~/.codeium/windsurf/mcp_config.json`。Cursor と同じ JSON（`--read-only` なし、`--metadata` の作業リージョン。`env.AWS_REGION` は必須ではない）
- `aws login` と `aws sts get-caller-identity`、`uvx` の導入、ツール再起動
- GitHub MCP を使う場合、再起動後にエージェントに見えている GitHub MCP tool が allowlist と一致することを確認する

Local の AWS MCP が終わるまで、ローカル AI に「東京の EC2 を見て」と頼んでも届かない。

**Cloud**

hook・憲法はリポジトリにあるので危険操作の禁止は効く。AWS MCP 接続はホーム設定では届かない。製品が account / project MCP を持てるならユーザーがそこで AWS MCP（`--read-only` なし、`--metadata` の作業リージョン）を登録する。GitHub MCP は任意。持てない環境では、その Cloud agent では AWS MCP は利用不可と報告する。GitHub は `gh` が使えれば続行できる。

PAT を環境変数へ置く構成では、エージェントのシェルからトークンが見えることがある。MCP に review / merge / file write を渡さなくても、REST 直叩きは hook では止まない。憲法と危険な `gh` deny で禁止する。絶対隔離が必要なら別途設計する。

### 2. 更新・削除を止める（IAM）— ユーザー作業

AWS は MCP を最初から参照専用にしない。第 3.3 節の手順でポリシー `DenyWriteViaAWSMCP` を作り、`get-caller-identity` で特定した IAM User / Role / Permission Set に付ける。session ARN には付けない。新しいユーザーやロールは作らない。

### 3. GitHub の最終防衛（Rulesets）— ユーザー作業

第 4.4 節と同等の保護が default / protected branch にあることをユーザーが確認する。無ければユーザーが設定する。実装者は触らない。既存保護を仮定しない。

### 確認用の聞き方（Local の MCP 登録後）

「今の AWS アカウントの東京リージョンについて、動いている EC2 と RDS を名前と状態だけ教えて。」
成功: シェルの `aws` を使わず、実データ（0 件でもよい）が返る。失敗: ドキュメントだけ、または `aws ec2 describe-instances` をシェル実行しようとする。

---

## 12. 編集時の注意

- 既存の formatter / 命名 / インデントに合わせる
- 依頼範囲外のリファクタをしない
- 表を直したら Prettier が通る列幅にする
- Markdown を行長のために途中改行しない
- 憲法同士を相互参照しない

完了報告: 変更ファイル、検証結果、ユーザー作業（MCP / IAM / Rulesets）の未完または確認済み、残リスク（hook は補助、IAM 未設定なら MCP 経由の Write が通る、Cloud は MCP 未登録なら参照不可）。
