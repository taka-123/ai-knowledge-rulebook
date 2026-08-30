# AI向け AWS / GitHub 安全設定：前回版からの訂正点

## 1. 結論

前回版からの主要な訂正は、**GitHub CLI（`gh`）をAIから全面禁止する方針を撤回すること**。

AWSについては、従来どおり **AIはAWS MCP経由に限定し、人間のAWS CLIは通常利用する** 方針を維持する。

最終的な考え方は次のとおり。

```text
AWS
- AI: AWS MCPを使用
- 人間: aws CLIを通常利用
- MCP経由のAWS操作だけIAMで参照中心に制限
- AIからのraw aws CLI / SDKは引き続き禁止

GitHub
- AI: GitHub MCP / gh CLI の両方を利用可能
- 人間: gh CLI / GitHub Webを通常利用
- GitHub MCPを必須経路にはしない
- gh CLIも全面禁止しない
- 本当に危険な操作だけAgent側で禁止
- 最終防衛線はGitHub Rulesets
```

---

## 2. AWSについては基本的に変更しない

前回版のAWS方針は維持する。

### 維持する内容

- AIはAWS MCP Serverを使用する
- AIからraw `aws` CLIを実行しない
- AIからAWS SDK / boto3等を使った迂回をしない
- AWS MCPに`--read-only`は付けない
- MCP経由であることを`aws:CalledViaAWSMCP`で識別する
- 同じDeveloper Role / Permission Setでも、MCP経由だけ参照中心に制限する
- 人間の直接`aws` CLI利用にはMCP用Denyを適用しない
- IAM / SCPをAWS側の最終セキュリティ境界とする

したがって、

```text
人間 ─ aws CLI ─────────────→ 通常権限
AI   ─ AWS MCP Server ─────→ MCP経由だけIAMで参照中心
```

という構成は変更しない。

AWSにはMCP経由だけを区別して制限できる仕組みがあるため、AIにAWS CLIも自由に使わせる構成へ変更する必要はない。

---

## 3. GitHubの「MCPのみ・gh禁止」を撤回する

### 前回

```text
AI → GitHub MCPのみ
AI → gh禁止
```

### 訂正後

```text
AI
├─ GitHub MCP
└─ gh CLI

どちらも利用可能
```

GitHub MCPと`gh` CLIは競合する手段ではなく、タスクに適した方を使用してよい。

一方が利用できない場合に、もう一方で実行可能か確認する。

### 方針文の例

```markdown
- GitHub操作には、公式GitHub MCP ServerまたはGitHub CLI（`gh`）を使用してよい。
- タスクに適した方を選択する。一方が利用できない場合は、可能であれば他方を試す。
- MCP / `gh` のどちらを利用しても、同じGitHub安全ポリシーに従う。
```

「なるべくMCPを使う」まで強制する必要はない。

---

## 4. `gh` CLIの全面denyを撤回する

前回版にある次のような全面禁止は削除する。

```text
Bash(gh *)
```

```text
gh CLI (use GitHub MCP Server)
```

Codex等にある、

```python
prefix_rule(
    pattern = ["gh"],
    decision = "forbidden",
)
```

も撤回する。

---

## 5. AIに許可する代表的な`gh`操作

以下のような日常的・低リスクな操作はAIに許可してよい。

```text
gh pr view
gh pr list
gh pr diff
gh pr checks

gh issue view
gh issue list
gh issue create

gh pr create
gh pr comment

gh run view
gh run list

gh api <GET系endpoint>
```

PRレビュー・CI監視・Issue/PR操作など、coding agentが日常的に使う範囲は`gh`でも実行可能にする。

OpenAI公式の`babysit-pr`等、既存の信頼できるworkflowが`gh`を前提としている場合も、不必要にMCPへ再実装しない。

---

## 6. `gh`で禁止するのは高危険操作に限定する

全面禁止の代わりに、AIによる以下の操作を禁止する。

### Merge

```text
gh pr merge
```

mergeは人間の最終判断として残す。

### Review提出

```text
gh pr review
```

特にapprove / request-changes等をAgentが勝手に行わない。

### Actionsの手動実行・rerun

```text
gh workflow run
gh run rerun
```

Agent が直接行う `gh workflow run` と `gh run rerun` は禁止のまま。
例外は、信頼する OpenAI 公式 babysit-pr watcher が current PR の failed checks を flaky/unrelated と分類し、公式 retry budget（最大 3 cycle）内で rerun する場合だけ。
一般的な Actions 手動実行権限は広げない。

### Repository管理操作

例:

```text
gh repo delete
gh repo archive
gh repo edit
```

Repository設定、Rulesets、Branch Protection等の管理変更は行わない。

### 認証情報の表示・変更

例:

```text
gh auth token
gh auth login
gh auth logout
gh auth refresh
```

Agent自身に認証状態を変更させたり、tokenを標準出力へ表示させたりしない。

### mutating `gh api`

GET中心の参照は許可する。次は禁止する。

```text
-X POST
-X PUT
-X PATCH
-X DELETE
--input
```

`-f` / `--field` は、明示的な `-X GET` / `--method GET` の query パラメータなら許可する（OpenAI 公式 babysit-pr watcher が使う）。
method 未指定の `-f`（`gh api graphql -f` 等）と `--input` は禁止のまま。

必要なwrite操作は、明示的に許可している高水準の`gh`コマンドまたはGitHub MCP toolを使用する。

---

## 7. `git push`に関する既存制限は維持する

`gh` CLIを解禁しても、Gitそのものの安全境界は変更しない。

引き続き禁止する。

```text
git push --force
git push --force-with-lease
git push -f
+refspec

main
master
develop
deploy
```

feature branchへの通常pushは許可する。

最終防衛線としてGitHub Rulesetsを維持する。

---

## 8. GitHub MCPは「必須」ではなく「利用可能な安全な選択肢」に変更する

前回版ではGitHub MCPの14 tool allowlistを事実上必須としていた。

訂正後は、

> GitHub MCPを利用する場合には、このallowlistを適用する

という位置付けに変更する。

つまり、

```text
GitHub MCPを使う
→ tool allowlistで能力を絞る

ghを使う
→ Agent側ポリシー + Rulesetsに従う
```

とする。

GitHub MCPを使う場合の既存allowlist自体はそのまま利用してよい。

---

## 9. GitHub MCPが使えないことを失敗扱いにしない

前回版では、GitHub MCPが未登録・利用不能な場合、

```text
GitHub操作不可
```

となる設計だった。

訂正後は、

```text
GitHub MCPがない
↓
gh CLIが利用可能か確認
↓
利用可能ならghで続行
```

とする。

逆に`gh`が利用できずGitHub MCPがある場合はMCPを使う。

Agentが一方の手段を使えないだけで「GitHub操作はできない」と判断しないようにする。

---

## 10. ローカル利用で「AI専用gh credential」を必須にしない

前回検討した、

```text
人間用gh credential
AI専用gh credential
```

という分離は、ローカルで対話的に利用するAI Agentの必須構成にはしない。

通常のローカル環境では、既存の`gh auth`をAgentから利用してよい。

安全性は主に、

```text
GitHub Rulesets
+
Agent側の危険操作deny
+
行動ポリシー
```

で確保する。

### 例外

Cloud Agent、CI、無人実行環境については、人間のローカルcredentialを共有せず、

- GitHub App installation token
- 製品側GitHub integration
- Fine-grained PAT
- Cloud Agent Secrets

等のmachine / Agent向けcredentialを利用する。

これはローカル対話型Agentとは分けて考える。

---

## 11. GitHubの安全境界の優先順位を修正する

訂正後のGitHub側の層構造は次のようにする。

```text
1. GitHub Rulesets / Branch Protection
   └─ 最終防衛線

2. GitHub側credential permissions
   └─ Cloud / CI等では特に重要

3. MCP tool制限 / Agent command deny
   └─ 危険な能力を減らす

4. AGENTS.md / CLAUDE.md / Skill
   └─ 行動規範
```

「GitHub MCPを使うこと」自体をセキュリティ境界とは扱わない。

`gh`を利用可能にした時点で、MCP tool allowlistだけではGitHub全体の能力を制限できないためである。

---

## 12. 憲法・ルール文書のGitHub節を変更する

前回版の、

```markdown
- GitHub API 操作は公式 GitHub MCP Server を使う。GitHub CLI（`gh`）は直接使わない。
```

を削除し、例えば以下へ変更する。

```markdown
### GitHub

- GitHub操作には、公式GitHub MCP ServerまたはGitHub CLI（`gh`）を使用してよい。一方が利用できない場合は、可能であれば他方を試す。
- 明示依頼があれば自動で行ってよい: Issue / PR / CI の参照、Issue 作成・通常編集、Issue・PRへのコメント、PR作成・通常編集、feature branchへの通常push。
- 既存Issue / PRのclose、base変更、draft/ready変更、reviewer変更等は明示依頼がある場合のみ行う。
- 禁止: PR merge、PR review提出、default / protected branchへの直接push、force push、protected branch削除、Actions workflowの手動実行・rerun、Repository / Ruleset / Branch Protectionの変更。
- GitHub認証情報の表示・変更は行わない。
```

Cursor Rules等も同じ趣旨へ変更する。

---

## 13. Hook / Permissionsの変更

### 削除する制御

各クライアントから、

```text
ghを見つけたら無条件deny
```

する処理を削除する。

### 残す・追加する制御

AI Agentについては、少なくとも次を止める。

```text
gh pr merge
gh pr review

gh workflow run
gh run rerun

gh repo delete
gh repo edit
その他repository管理操作

gh auth token
gh auth login
gh auth logout
gh auth refresh

mutating gh api
```

既存のGit force push / protected branch push防止は維持する。

AWSの`aws` CLI全面denyは維持する。

---

## 14. Hookの自動テストを変更する

前回版では次をdenyとしていた。

```text
gh pr view 1
/usr/local/bin/gh issue list
```

これはallowへ変更する。

代表的な期待値:

```text
gh pr view 1
→ allow

gh pr checks 1
→ allow

gh issue list
→ allow

gh api repos/owner/repo/pulls/1
→ allow

gh pr merge 1
→ deny

gh pr review 1 --approve
→ deny

gh workflow run build.yml
→ deny

gh run rerun 123
→ deny

gh repo edit owner/repo
→ deny

gh auth token
→ deny

gh api ... -X DELETE
→ deny
```

AWS側の、

```text
aws s3 ls
→ deny
```

等は変更しない。

---

## 15. 完了条件・ユーザー作業の説明も修正する

前回版の、

> GitHubを使うには各AIツールへGitHub MCPを登録する必要がある

という記述は撤回する。

訂正後は、

```text
GitHub MCP
→ 任意。使うならallowlistを設定

gh CLI
→ 認証済みなら利用可能
```

とする。

したがって、GitHub MCP未登録でも`gh`が利用可能ならGitHub操作は可能。

AWSについては従来どおり、AWS MCP登録が必要。

---

# 変更しない重要方針

今回の訂正は「AIへGitHubの全権限を与える」という変更ではない。

以下は引き続き維持する。

- mergeは人間
- force push禁止
- protected / default branch直接push禁止
- Actions手動実行禁止
- Repository / Rulesets等の管理変更禁止
- 不要なreview提出禁止
- GitHub Rulesetsを最終防衛線とする
- AWSはMCP経由のみ
- AWSの状態変更はIAMでMCP経由だけ拒否する

今回変更するのは、

> **GitHub操作の安全性を作るために`gh` CLIそのものを全面禁止する必要はない**

という点である。
