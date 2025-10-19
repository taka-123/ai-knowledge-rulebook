## Claude Code: 最小プロジェクトテンプレート（Subagents → Plugins → Hooks → MCP → SDK → Slash → Actions → Checkpoint）

> そのままコピペで骨格が作れる**最小構成**。必要に応じて各断片を追記してください。

```
.
├─ .claude/
│  ├─ settings.json
│  ├─ agents/
│  │  ├─ code-reviewer.md
│  │  └─ test-planner.md
│  ├─ skills/
│  │  └─ pdf-analyzer/
│  │     ├─ SKILL.md
│  │     └─ extract.py
│  ├─ commands/
│  │  └─ security-review.md
│  └─ hooks/
│     └─ validate-bash.py
├─ .mcp.json
├─ plugins/
│  └─ my-security-plugin/
│     ├─ plugin.json
│     └─ commands/approve.md
└─ .github/workflows/ai-ci.yml
```

---

### 1) Subagents（サブエージェント）

`.claude/agents/code-reviewer.md`

```markdown
---
name: code-reviewer
description: 変更差分のセキュリティ/性能/可読性を横断レビュー。PR発生時は優先して使用。
tools: Read, Grep, Glob, Bash
model: inherit
---
あなたはシニアコードレビューア。脆弱性（OWASP Top 10）、N+1、メモリフットプリント、例外処理、I/O境界を重点に、ファイル:行を明記。
```

`.claude/agents/test-planner.md`

```markdown
---
name: test-planner
description: 変更影響に基づくテスト計画作成（単体/統合/E2E）と優先度付け
tools: Read, Grep, Glob
model: inherit
---
対象機能・依存・回帰範囲を列挙し、観測指標と失敗時の切り分け手順を具体化。
```

* 配置とファイル形式（YAMLフロントマター）、CLIによる動的定義は公式仕様通りです。([Claude Docs][1])

---

### 2) Agent Skills（エージェントスキル最小構成）

`.claude/skills/pdf-analyzer/SKILL.md`

```markdown
---
name: PDF Analyzer
description: PDFから構造化データを抽出し分析。PDFファイル処理時に使用。
allowed-tools: Read, Bash
---

# PDF Analyzer

## 概要

PDFファイルからテキスト・テーブル・メタデータを抽出し、構造化データとして出力します。

## クイックスタート

対象PDFファイルを指定してください：

\`\`\`bash
python .claude/skills/pdf-analyzer/extract.py <input.pdf> <output.json>
\`\`\`

出力されたJSONを確認し、必要に応じて分析を進めます。

## 利用可能なツール

- **Read**: ファイル読込み
- **Bash**: スクリプト実行

## 注意点

- プリインストールライブラリ（pypdf等）を使用。API環境では追加パッケージ不可。
- Claude.ai環境では動的パッケージインストール可能。
```

`.claude/skills/pdf-analyzer/extract.py`

```python
#!/usr/bin/env python3
"""
Extract text and metadata from PDF files.
Usage: python extract.py <input.pdf> <output.json>
"""
import sys, json
from pypdf import PdfReader

def main():
    if len(sys.argv) != 3:
        print("Usage: python extract.py <input.pdf> <output.json>")
        sys.exit(1)
    
    input_pdf, output_json = sys.argv[1], sys.argv[2]
    reader = PdfReader(input_pdf)
    
    data = {
        "pages": len(reader.pages),
        "metadata": dict(reader.metadata) if reader.metadata else {},
        "text": [page.extract_text() for page in reader.pages]
    }
    
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(data['pages'])} pages to {output_json}")

if __name__ == "__main__":
    main()
```

**ポイント**

* **段階的開示**：Claude は `name`/`description` でスキルを発見し、必要時に `SKILL.md` 本体を読込み。([Claude Docs][18])
* **実行環境差異**：API（ネットワーク遮断、プリインストールライブラリのみ）/ Claude.ai（ネットワーク可、動的インストール可）/ Claude Code（ローカル実行、制限なし）。([Kyutaro note][19])
* **ツール制限**：`allowed-tools` で権限を最小化。セキュリティ境界を明確に。
* **共有**：`.claude/skills/` 配下をGit管理でチーム共有。API利用時は `/v1/skills` エンドポイントで管理。

---

### 3) Plugins（プラグイン最小骨格）

`plugins/my-security-plugin/plugin.json`

```json
{
  "name": "my-security-plugin",
  "version": "0.1.0",
  "description": "セキュリティ補助",
  "commandsDir": "commands",
  "agentsDir": "agents",
  "hooks": {},
  "mcpServers": {}
}
```

`plugins/my-security-plugin/commands/approve.md`

```markdown
---
description: 危険操作の人手承認ワークフローを開始
---
対象の操作を要約し、承認テンプレートを作成。否決時の代替案も提示。
```

* プラグインがコマンド/エージェント/フック/MCPを束ねる構造はリファレンス準拠。([Claude Docs][2])

---

### 4) Hooks（危険Bashブロックの最小例）

`.claude/settings.json`（抜粋）

```json
{
  "permissions": {
    "allow": ["Bash(git status:*)", "Bash(git diff:*)"],
    "ask":   ["Bash(git push:*)"],
    "deny":  ["Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)"]
  },
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "python .claude/hooks/validate-bash.py",
        "timeout": 5
      }]
    }],
    "PreCompact": [{
      "hooks": [{ "type": "command", "command": "echo 'checkpoint saved'" }]
    }]
  }
}
```

`.claude/hooks/validate-bash.py`

```python
#!/usr/bin/env python3
import json, re, sys
inp = json.load(sys.stdin)
cmd = inp.get("tool_input", {}).get("command", "")
blocked = [r"rm\s+-rf\s+/", r"\|\s*sh\b", r"curl\s+.*\|\s*bash"]
if any(re.search(p, cmd, re.I) for p in blocked):
    print("危険なBashコマンドを検出しました。実行をブロックします。", file=sys.stderr)
    sys.exit(2)  # Exit code 2: ブロック
print("OK", file=sys.stdout); sys.exit(0)
```

* 設定ファイルの権限モデル（allow/ask/deny）と`settings.json`の場所・優先順位、Hookのイベント群/入出力と**Exit code 2=ブロック**挙動は公式定義に一致。([Claude Docs][3])

---

### 5) MCP（ツール接続の最小例：GitHub + 変数展開）

`.mcp.json`

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": { "Authorization": "Bearer ${GITHUB_TOKEN}" }
    }
  }
}
```

* `.mcp.json`の配置と**スコープ（local/project/user）**、環境変数展開（`${VAR}`/`${VAR:-default}`）は公式通り。([Claude Docs][4])

---

### 6) SDK（最小ストリーミング骨格：TypeScript）

> SDKは「設定ファイルを自動読込しない」ため、必要に応じて`settingSources`等を明示。
> `tools/dev/query.ts`

```ts
import { query } from '@anthropic-ai/claude-agent-sdk';
const stream = query({
  prompt: "変更差分から回帰リスクを抽出して要約して",
  options: {
    cwd: process.cwd(),
    allowedTools: ["Read", "Grep"],
    settingSources: ["project"],   // .claude/settings.json を読む
    systemPrompt: { type: "preset", preset: "claude_code" }
  }
});
for await (const ev of stream) {
  if (ev.type === "tool_use") console.log("tool:", ev.tool_name);
  if (ev.type === "result" && ev.subtype === "success") console.log(ev.output);
}
```

* Agent SDKの移行点（名称・`settingSources`・`systemPrompt`プリセット）は移行/TSリファレンスに記載。([Claude Docs][5])

---

### 7) Slash commands（プロジェクトコマンド）

`.claude/commands/security-review.md`

```markdown
---
allowed-tools: Read, Grep
argument-hint: [path-or-pr]
description: セキュリティ観点のレビュー
---
対象: $ARGUMENTS を中心に、OWASP Top 10/認可欠陥/秘匿情報露出を確認。
```

* コマンド配置・引数（`$ARGUMENTS`/`$1..`）・frontmatter（allowed-tools等）は仕様準拠。([Claude Docs][6])

---

### 8) GitHub Actions（PRレビュー/失敗E2Eの原因分析/リリースノート草案）

`.github/workflows/ai-ci.yml`

```yaml
name: AI CI (Claude Code)

on:
  pull_request:
    types: [opened, synchronize, reopened]
  workflow_run:
    workflows: ["E2E Tests"]
    types: [completed]
  push:
    branches: [main]

jobs:
  pr_review:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    permissions: { contents: read, pull-requests: write }
    steps:
      - uses: actions/checkout@v4
      - name: Claude PR Review
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          prompt: |
            このPRをセキュリティ/性能/可読性でレビュー。必ず行番号を引用。
          claude_args: "--model claude-sonnet-4-5-20250929 --max-turns 20"

  e2e_triage:
    if: github.event_name == 'workflow_run' && github.event.workflow_run.conclusion == 'failure'
    runs-on: ubuntu-latest
    permissions: { contents: read, pull-requests: write }
    steps:
      - uses: actions/checkout@v4
      - name: Triage failed E2E with logs
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          prompt: |
            直近のE2E失敗ログと関連差分から原因候補と修正案を3件以内で提案。
          claude_args: "--model claude-sonnet-4-5-20250929 --max-turns 16"

  release_notes:
    if: github.event_name == 'push' && startsWith(github.ref, 'refs/heads/main')
    runs-on: ubuntu-latest
    permissions: { contents: write }
    steps:
      - uses: actions/checkout@v4
      - name: Draft release notes
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          prompt: |
            直近のコミットから変更点を分類し、破壊的変更/移行手順を強調したリリースノート草案を生成。
          claude_args: "--model claude-sonnet-4-5-20250929 --max-turns 18"
```

* 公式Actionsガイド（インストール手順・最小ワークフロー）および`anthropics/claude-code-action@v1`のREADME/Usageに整合。モデル指定は設定ガイド例の形式に合わせています。([Claude Docs][7])

---

### 9) Checkpoint（簡易：Compact前の痕跡保存）

* すでに`PreCompact`で最小ログを出す設定を追加済み（上のHooks参照）。公式のチェックポイント/コンパクト機能の参照はこちら。([Claude Docs][8])

---

## 使い方の目安

* **まず`settings.json`の`permissions`を厳しめに**→ 誤操作を抑制（`ask`活用）。([Claude Docs][3])
* **Subagentsを役割で分割**→ メイン文脈の汚染を防ぎ、並列で思考させやすい。([Claude Docs][1])
* **Skillsでノウハウをパッケージ化**→ `description`で発見可能性を上げ、段階的開示で効率化。([Claude Docs][18])
* **危険BashはHookでブロック**（Exit code 2）。([Claude Docs][9])
* **外部SaaSはMCPで接続し`.mcp.json`を共有**（projectスコープ）。([Claude Docs][4])
* **CIは`claude-code-action`でPR/E2E/リリースの3点を自動化**。([Claude Docs][7])

---

※ すべて一次情報（Claude Docs/公式GitHub）を基に最小テンプレ化しています。必要に応じて**モデル名/権限/トークン**を環境に合わせて調整してください。

[1]: https://docs.claude.com/en/docs/claude-code/sub-agents "Subagents - Claude Docs"
[2]: https://docs.claude.com/en/docs/claude-code/plugins-reference "Plugins reference - Claude Docs"
[3]: https://docs.claude.com/en/docs/claude-code/settings "Claude Code settings - Claude Docs"
[4]: https://docs.claude.com/en/docs/claude-code/mcp "Connect Claude Code to tools via MCP - Claude Docs"
[5]: https://docs.claude.com/en/docs/claude-code/sdk/migration-guide "Migrate to Claude Agent SDK - Claude Docs"
[6]: https://docs.claude.com/en/docs/claude-code/slash-commands "Slash commands - Claude Docs"
[7]: https://docs.claude.com/en/docs/claude-code/github-actions "Claude Code GitHub Actions - Claude Docs"
[8]: https://docs.claude.com/en/docs/claude-code/checkpointing "Checkpointing - Claude Docs"
[9]: https://docs.claude.com/en/docs/claude-code/hooks "Hooks reference - Claude Docs"
[18]: https://docs.claude.com/en/docs/claude-code/skills "Agent Skills - Claude Docs"
[19]: https://note.com/kyutaro15/n/nfcc15522626f "Claudeを“育てる”新常識！ Agent Skills徹底解説"
