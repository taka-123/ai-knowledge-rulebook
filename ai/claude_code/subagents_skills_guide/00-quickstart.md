---
created: 2025-11-05
updated: 2025-11-05
tags:
  - claude-code
  - subagents
  - agent-skills
  - quickstart
---

# Claude Code Subagents & Skills クイックスタート

> **目標**: 5分で理解し、今日から使える最小構成を提供

## 結論ファースト：何を使うべきか

```
対話しながら継続的に参照する知識 → Skills
独立実行でコンテキスト汚染を避けたい → Subagents
```

---

## 最小構成で今すぐ始める

### パターン1: コードレビューを自動化（Subagent）

**所要時間**: 2分

```bash
# 1. ディレクトリ作成
mkdir -p .claude/agents

# 2. ファイル作成
cat > .claude/agents/code-reviewer.md << 'EOF'
---
name: code-reviewer
description: Review code for quality, security, and best practices. Use PROACTIVELY after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer. When invoked:

1. Run `git diff` to see recent changes
2. Review for:
   - Code clarity and readability
   - Security vulnerabilities
   - Error handling
   - Test coverage
   - Performance issues

Provide feedback in priority order:
- 🔴 Critical (must fix)
- 🟡 Warning (should fix)
- 🟢 Suggestion (nice to have)
EOF

# 3. 動作確認
# コードを変更後、以下を実行
```

**使い方**:

```bash
# 明示的に呼び出す
> use code-reviewer to review my changes

# 自動起動させる（CLAUDE.md に記載）
コード変更後は必ず code-reviewer で品質確認すること。
```

**期待される挙動** 🔍:
- `git diff` を実行してコード変更を確認
- レビュー結果を優先度別に報告
- メインのコンテキストを汚染しない（独立実行）

---

### パターン2: プロジェクト規約を常時適用（Skill）

**所要時間**: 3分

```bash
# 1. ディレクトリ作成
mkdir -p .claude/skills/coding-standards

# 2. ファイル作成
cat > .claude/skills/coding-standards/SKILL.md << 'EOF'
---
name: coding-standards
description: Apply project coding standards. Use when writing or reviewing code in this project.
---

# Coding Standards

## TypeScript
- Strict mode enabled
- No `any` types
- Prefer `const` over `let`

## Testing
- Test coverage > 70%
- Unit tests in `__tests__/` directory
- Use Jest for testing

## Formatting
- Prettier (line length: 100)
- 2 spaces indentation
- Single quotes for strings

## Git
- Conventional Commits format
- Branch naming: `feature/`, `fix/`, `refactor/`

After coding, run code-reviewer subagent for validation.
EOF

# 3. 動作確認
# Claude Code を再起動後、コードを書かせる
```

**使い方**:

Claude が自動的に参照します（明示的な呼び出し不要）。

**期待される挙動** 🔍:
- コード作成時、自動的にこの規約に従う
- メインのコンテキスト内で継続的に参照
- 対話しながら適用可能

---

## Skills と Subagents の違い（1分で理解）

| 項目 | Skills | Subagents |
|------|--------|-----------|
| **配置** | `.claude/skills/` | `.claude/agents/` |
| **ファイル名** | `SKILL.md` | 任意（例: `code-reviewer.md`） |
| **起動方法** | 自動判断のみ | 自動 or 明示的 |
| **コンテキスト** | メインと共有 | **独立** |
| **対話** | ✅ 可能 | ❌ ワンショット |
| **用途** | 継続的な知識提供 | 独立タスク実行 |

---

## どちらを使うべきか（判断フロー）

```
Q1: このタスクはメインとの対話が必要？
  YES → Skills を使う
  NO  → Q2へ

Q2: コンテキストを汚染したくない？
     （大量ログ、検索結果、レビューなど）
  YES → Subagents を使う
  NO  → Skills を使う
```

### 具体例

| タスク | 選択 | 理由 |
|--------|------|------|
| プロジェクトのコーディング規約 | **Skills** | 常に参照、対話しながら適用 |
| エラーログ解析（1000行） | **Subagents** | コンテキスト汚染を回避 |
| PDF処理ライブラリの使い方 | **Skills** | 継続的に参照する知識 |
| 4ファイルの並列レビュー | **Subagents** | 並列実行＋独立検証 |
| Git コミットメッセージ生成 | **Skills** | 対話しながら履歴確認 |
| 最新ライブラリ仕様調査 | **Subagents** | Web検索でコンテキスト消費 |

---

## よくある質問

### Q1: Subagent が使われない

**A**: description を具体的にし、明示的に呼び出す

```bash
# ❌ 曖昧
description: Code review

# ✅ 具体的
description: Review code for quality, security, and best practices. Use PROACTIVELY after code changes.

# 明示的呼び出し
> use code-reviewer to review my changes
```

### Q2: Skill が認識されない

**A**: ファイル構造とYAML構文を確認

```bash
# ファイル構造確認
ls -R .claude/skills/

# 正しい構造
.claude/skills/
└── my-skill/
    └── SKILL.md  # ← ディレクトリ内にSKILL.md

# YAML確認
cat .claude/skills/my-skill/SKILL.md | head -n 10
```

### Q3: どちらを先に試すべき？

**A**: Subagent から

1. **code-reviewer** subagent（上記の例）
2. **coding-standards** skill（上記の例）
3. 効果を確認しながら追加

---

## 次のステップ

### 初心者向け（今すぐ）
- ✅ 上記の2つ（code-reviewer + coding-standards）を設定
- ✅ 実際に使って挙動を確認

### 中級者向け（1週間後）
- 📖 [01-skills-complete-guide.md](01-skills-complete-guide.md) を読む
- 📖 [02-subagents-complete-guide.md](02-subagents-complete-guide.md) を読む
- プロジェクト固有のSkill/Subagentを追加

### 上級者向け（1ヶ月後）
- MCP統合（Context7, Brave-Search）
- 複数Subagentsの並列実行
- タスク分解システムの構築

---

## トラブルシューティング

### Subagentが起動しない

```bash
# 1. 認識確認
/agents

# 2. ログ確認
ls .claude/

# 3. デバッグモード
claude --debug
```

### Skillが機能しない

```bash
# 1. ファイル確認
ls ~/.claude/skills/*/SKILL.md    # Personal
ls .claude/skills/*/SKILL.md      # Project

# 2. YAML検証
cat .claude/skills/my-skill/SKILL.md | head -n 15

# 3. Claude Code再起動
# 変更後は再起動が必要
```

---

## チートシート

### Skills

```yaml
# .claude/skills/my-skill/SKILL.md
---
name: my-skill
description: What it does. Use when <trigger condition>.
allowed-tools: Read, Bash  # オプション
---

# Skill Content

Instructions, examples, templates...
```

### Subagents

```yaml
# .claude/agents/my-agent.md
---
name: my-agent
description: What it does. Use PROACTIVELY when <condition>.
tools: Read, Grep, Glob  # オプション（省略時は全継承）
model: sonnet  # sonnet/opus/haiku/inherit
---

System prompt for this agent...
```

### 呼び出し方

```bash
# Subagent明示的呼び出し
> use the code-reviewer agent

# 複数Subagents並列実行
> use multiple subagents to review all modified files

# Skillは自動（明示的呼び出し不可）
# → descriptionを具体的に書くことで自動発動を促す
```

---

**所要時間**: このページの理解 5分 + 設定 5分 = **合計10分で即実践可能**

詳細は [Skills完全ガイド](01-skills-complete-guide.md) と [Subagents完全ガイド](02-subagents-complete-guide.md) へ。
