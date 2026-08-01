# Portable Kit（任意プロジェクトへコピーしてよい global 資産）

Cloud Agent や「この repo 単体でも同じ手順を使いたい」ときに、
`ai/*/global` の汎用 Skills / Agents を **対象プロジェクトへ実体コピー**するための一覧。

正本は常にこの rulebook。他プロジェクトからコピーしてこない。

## 使い方

```bash
# 一覧
./scripts/copy-portable-to-project.sh --list

# Cloud 連続作業向け（人間対話・チャット整形は含まない）
./scripts/copy-portable-to-project.sh /path/to/project --preset cloud-basic

# 引き継ぎ成果物向け（HTML / グラレコ）
./scripts/copy-portable-to-project.sh /path/to/project --preset cloud-handoff

# 個別指定
./scripts/copy-portable-to-project.sh /path/to/project \
  --skill document-authoring --skill backlog-markdown-formatting \
  --agent codebase-explorer
```

コピー後は対象プロジェクトで **git commit** する（未コミットだと Cloud は見ない）。

## 置き場の選び方

| 手段                               | いつ使うか                                                |
| ---------------------------------- | --------------------------------------------------------- |
| **global**                         | Local 専用。対話型・個人運用・リポジトリに載せないもの    |
| **コピー（Portable Kit）**         | Cloud で使うために対象 repo へ実体を置く。正本は rulebook |
| **multi_service_parent / project** | 親ディレクトリや各プロジェクトの初期同梱としてよいもの    |

- リポジトリに載せない資産は、その repo の Cloud では使えない。
- コピーしたら global 同名は使わないか、別名（`my-*`）にする。

## 同名ポリシー

- global（`~/.claude/skills` 等）と project に **同名を恒久並存させない**（推奨）。
- Claude Code Skills は公式上 personal が project より優先される。同名だと Local と Cloud で別物が動き得る。
- `/` 一覧に同名が二重表示されることもある。
- ホームを指す symlink で配布しない。

## プリセット基準

- **cloud-basic**: 無人連続作業で成果物（文書・整形・調査）を残すもの。ライブ対話・チャット貼り付けは含めない。
- **cloud-handoff**: 人間への引き継ぎ成果物（HTML / グラレコ）。必要時だけ追加。
- **含めない（個別追加可）**: `grill-me`、`chatwork-formatter`、コミット系。

## キット一覧

### Skills（正本: `ai/claude_code/global/.claude/skills/`）

コピー先: `<project>/.claude/skills/<name>/`  
（Cursor は互換で `.claude/skills` も探索する）

| 名前                          | cloud-basic | cloud-handoff | 備考                         |
| ----------------------------- | ----------- | ------------- | ---------------------------- |
| document-authoring            | yes         | no            | ドキュメント作成             |
| ai-instruction-authoring      | yes         | no            | AI 指示文書向け              |
| backlog-markdown-formatting   | yes         | no            | Backlog 整形（記法変換）     |
| conversation-visualizer       | no          | yes           | HTML 可視化                  |
| conversation-graphic-recorder | no          | yes           | グラレコ                     |
| grill-me                      | no          | no            | ライブ対話。個別追加可       |
| diff-quality-gate             | no          | no            | 個別追加可                   |
| diff-review-commit            | no          | no            | 個別追加可（依存スキルあり） |
| commit-message-suggester      | no          | no            | 個別追加可                   |
| prompt-evolution              | no          | no            | 個別追加可                   |
| markdown-line-length          | no          | no            | 個別追加可                   |
| chatwork-formatter            | no          | no            | チャット貼付。キット外でも可 |

### Agents — Claude（正本: `ai/claude_code/global/.claude/agents/`）

コピー先: `<project>/.claude/agents/<name>.md`

| 名前              | cloud-basic | cloud-handoff |
| ----------------- | ----------- | ------------- |
| codebase-explorer | yes         | no            |
| tech-researcher   | yes         | no            |

### Agents — Cursor（正本: `ai/cursor/global/.cursor/agents/`）

コピー先: `<project>/.cursor/agents/<name>.md`

| 名前              | cloud-basic | cloud-handoff |
| ----------------- | ----------- | ------------- |
| codebase-explorer | yes         | no            |
| tech-researcher   | yes         | no            |
| security-reviewer | no          | no            |
| task-reviewer     | no          | no            |
| test-runner       | no          | no            |

## キットに含めないもの

- `ai/*/project` の契約ハーネス（`spec-audit`、`implementer`、`adversarial-e2e` 等）— プロジェクトテンプレから別途導入
- `ai/claude_code/multi_service_parent/.claude/skills/backlog-intake-planner` — マルチレポ親向け。親ディレクトリへ直接配置
- 親ディレクトリ専用スキル（例: `pr-self-reviewer`）— 親 repo の正本から
- MCP / 秘密情報を含む設定

## コピー時のパス

- スキル間参照は **名前** を使う（パスで結ばない）。
- スキル内の `docs/`・`assets/`・`scripts/` はスキルディレクトリ相対。ディレクトリごとコピーすれば維持される。
