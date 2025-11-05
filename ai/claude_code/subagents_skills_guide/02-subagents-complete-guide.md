---
created: 2025-11-05
updated: 2025-11-05
tags:
  - claude-code
  - subagents
  - complete-guide
---

# Subagents 完全ガイド

> **出典**: 公式ドキュメント + Claude Code 内部仕様検証 + 実践者知見統合
> **対象**: Claude Code 1.0以降

## 目次

1. [Subagents とは](#subagents-とは)
2. [Subagents の内部仕様（重要）](#subagents-の内部仕様重要)
3. [エージェント定義の完全仕様](#エージェント定義の完全仕様)
4. [description 設計の実践](#description-設計の実践)
5. [tools 制御の詳細](#tools-制御の詳細)
6. [呼び出し方の完全ガイド](#呼び出し方の完全ガイド)
7. [実践パターン集](#実践パターン集)
8. [最適化テクニック](#最適化テクニック)
9. [MCP統合](#mcp統合)
10. [トラブルシューティング](#トラブルシューティング)

---

## Subagents とは

### 定義

**Subagents は「タスク特化型の独立エージェント」**

- 特定タスクを独立したコンテキストで実行
- ワンショット実行（タスク完了で解放）
- 並列実行可能
- メインのコンテキストを汚染しない

### ⚠️ 最重要: Subagentsに適したタスク

📊 **実践者の知見(Gotaさん)**:

```
✅ READ系タスク → Subagentsと相性抜群
  - エラーログ解析
  - コードベース検索
  - ドキュメント調査
  - レビュー・検証
  - Web検索
  - 品質チェック（lint, test, build）

⚠️ WRITE系タスク → 慎重に扱う
  - 初めから委任すると事故る可能性が高い
```

**なぜWRITE系で事故るのか**:

1. **コンテキスト不足による実装ミス**
   - メインの会話履歴が引き継がれない
   - 「なぜこの実装？」という意図が伝わらない
   - 既存コードのパターンを無視した実装になりがち

2. **トークンの無駄な消費**

   ```
   メインエージェント: ファイルAを読む (1000トークン)
     ↓
   Subagentに委任
     ↓
   Subagent: 同じファイルAを再度読む (1000トークン)

   結果: 2000トークン消費（無駄が発生）
   ```

3. **実践者の教訓**
   > 「初めから書き込み系タスクをサブエージェントに委任すると事故る」
   >
   > - Gotaさん (Meetup Tokyo 2025)

**重要な考え方**:

- メインエージェントは優秀 → **基本的にはメインで処理**
- コンテキスト汚染を避けたい時のみSubagentsを活用
- READ系から始めて、効果を確認してから拡張

### 配置場所と優先度

| 種類        | パス                | スコープ       | 優先度 | 用途       |
| ----------- | ------------------- | -------------- | ------ | ---------- |
| **Project** | `.claude/agents/`   | プロジェクト内 | 最高   | チーム共有 |
| **User**    | `~/.claude/agents/` | 全プロジェクト | 中     | 個人用     |
| **Plugin**  | Plugin内            | インストール時 | 低     | 配布用     |
| **CLI**     | `--agents` フラグ   | セッション限定 | 高     | 一時的     |

🔍 **検証済み**: 同名の場合、Project > CLI > User > Plugin の順

---

## Subagents の内部仕様（重要）

### 最も重要な特性

> **Subagents は独立したコンテキストウィンドウを持つ = メインの会話履歴は引き継がれない**

🔍 **Claude Code 内部仕様検証結果**:

```
メインエージェント (Context Window A)
  │
  ├─ ユーザーとの会話履歴
  ├─ ファイル読み込み履歴
  └─ これまでの実装経緯
      ↓
      ↓ Subagent起動
      ↓
Subagent (Context Window B) ← 完全に独立
  │
  ├─ メインの会話履歴: ❌ 引き継がない
  ├─ ファイル読み込み履歴: ❌ 引き継がない
  ├─ 実装経緯: ❌ 引き継がない
  │
  └─ 受け取るもの:
      - タスクの説明（メインからの指示）
      - エージェント定義（システムプロンプト）
      - 利用可能なツール
```

### この特性の影響

✅ **メリット**:

1. **コンテキスト汚染を完全回避**
   - 大量ログ解析でもメインに影響なし
   - Web検索結果がメインを圧迫しない

2. **並列実行が可能**
   - 複数Subagentsを同時起動
   - 独立したコンテキストで同時処理

3. **トークン消費の分離**
   - Subagentの消費はメインと別カウント
   - メインのコンテキストを長く維持

❌ **デメリット**:

1. **コンテキスト不足のリスク**
   - メインの実装意図が伝わらない
   - 「なぜこの実装？」が分からない

2. **対話不可**
   - 起動→実行→結果返却のみ
   - 途中で質問・修正ができない

3. **重複読み込み**
   - メインで読んだファイルをSubagentも読む
   - トークン重複消費

---

## エージェント定義の完全仕様

### ファイル形式

```markdown
---
name: agent-name
description: What this agent does and when to use it
tools: Read, Grep, Glob
model: sonnet
---

Agent's system prompt goes here...
```

### フロントマター全フィールド

✅ **公式仕様**:

```yaml
---
name:
  your-agent-name
  # 必須
  # 形式: 小文字英数字とハイフンのみ
  # 例: code-reviewer, debugger, spec-researcher

description:
  Description of when this agent should be invoked
  # 必須
  # Claude がこのSubagentを使うかの判断基準
  # 形式: 役割説明 + 呼び出し条件 + トリガーワード
  # キーワード: PROACTIVELY, MUST BE USED

tools:
  Read, Grep, Glob, Bash
  # オプション
  # カンマ区切り
  # 省略時: メインの全ツールを継承（MCPツール含む）
  # 指定時: 指定ツールのみ使用可能

model:
  sonnet
  # オプション
  # 値: sonnet / opus / haiku / inherit
  # sonnet: Claude Sonnet 使用（デフォルト）
  # opus: Claude Opus 使用（高性能）
  # haiku: Claude Haiku 使用（高速・低コスト）
  # inherit: メインと同じモデル
  # 省略時: sonnet
---
# Agent System Prompt

Clear, step-by-step instructions for this agent.
Define role, approach, and constraints.
```

🔍 **検証済み**:

- `name` の大文字・スペース・アンダースコアは **エラー**
- `tools` のワイルドカード（`*`）は **不可**
- `model: inherit` は メインのモデル選択を継承

### ファイル名の自由度

✅ **公式確認済み**:

- ファイル名は **任意**（`code-reviewer.md`, `my-agent.md` など）
- `name` フィールドが識別子として使われる
- 推奨: `<name>.md` で統一

```bash
# ✅ すべて有効
.claude/agents/code-reviewer.md
.claude/agents/my-custom-agent.md
.claude/agents/foo.md

# ❌ 無効
.claude/agents/CODE-REVIEWER.md  # 大文字NG
.claude/agents/code_reviewer.md  # アンダースコアNG
```

---

## description 設計の実践

### description の役割

🔍 **検証結果**:

- `description` は **メインのコンテキストに常時含まれる**
- Subagent選択の **主要判断材料**
- `name` も影響するが、`description` が決定的

📊 **実践者の検証（asueneさん）**:

```yaml
# 検証1: name と description の影響度
name: backend-engineer-nestjs
description: Use this agent when you need to design, implement, or review backend...
→ ✅ バックエンドタスクで起動

name: frontend-engineer
description: MUST BE USED this agent when implementing the backend.
→ ❌ 起動しない（name が矛盾）

# 結論: name を役割に合わせることが重要
```

### 効果的な description の3要素

```yaml
description: [役割説明] + [呼び出し条件] + [自律起動キーワード]
```

#### 1. 役割説明（何をするエージェントか）

```yaml
# ❌ 曖昧
description: Code review

# ✅ 具体的
description: Expert code reviewer focusing on quality, security, and best practices
```

#### 2. 呼び出し条件（いつ使うか）

```yaml
# ❌ 条件なし
description: Review code

# ✅ 条件明記
description: Review code for quality and security. Use when code changes are made or before committing
```

#### 3. 自律起動キーワード

✅ **公式推奨キーワード**:

- `PROACTIVELY` - 積極的に使う
- `MUST BE USED` - 必ず使う
- `immediately after` - タイミング指定

```yaml
# ❌ キーワードなし
description: Review code when needed

# ✅ キーワード含む
description: Review code for quality. Use PROACTIVELY after code changes. MUST BE USED before committing.
```

### description テンプレート集

#### パターンA: レビュー系

```yaml
description: [Expert in X] reviewing [Y]. Use PROACTIVELY after [trigger]. Check [aspects].
```

**例**:

```yaml
description: Expert code reviewer focusing on quality, security, and performance. Use PROACTIVELY after code changes. Check readability, security vulnerabilities, error handling, and test coverage.
```

#### パターンB: 調査系

```yaml
description: Research [topic] using [tools]. Use PROACTIVELY when [condition]. Must check [sources].
```

**例**:

```yaml
description: Research latest library versions and best practices using Context7 and web search. Use PROACTIVELY when adding dependencies or investigating technical issues. Must check official documentation and current versions.
```

#### パターンC: 実行系（慎重に）

```yaml
description: Execute [task] following [methodology]. Use when [specific condition only].
```

**例**:

```yaml
description: Execute one task from docs/plans/tasks/ and update progress. Use when explicitly asked to run a specific task file.
```

#### パターンD: 検証系

```yaml
description: Validate [aspect]. Use PROACTIVELY after [completion]. Ensure [criteria].
```

**例**:

```yaml
description: Comprehensive quality check including lint, tests, and build. Use PROACTIVELY after implementation completes. Ensure all checks pass before committing.
```

---

## tools 制御の詳細

### tools フィールドの動作

✅ **公式仕様**:

```yaml
# パターン1: tools 省略（デフォルト）
---
name: my-agent
description: ...
# tools フィールドなし
---
→ メインの全ツールを継承（MCPツール含む）
# パターン2: tools 明示指定
---
name: my-agent
description: ...
tools: Read, Grep, Glob
---
→ 指定したツールのみ使用可能
```

### 利用可能なツール一覧

🔍 **Claude Code 内部仕様**:

```yaml
# ファイル操作
Read           # ファイル読み込み
Write          # ファイル新規作成
Edit           # ファイル編集
MultiEdit      # 複数ファイル一括編集
Glob           # ファイルパターン検索

# 検索
Grep           # コンテンツ検索（ripgrep）

# 実行
Bash           # シェルコマンド実行

# Web
WebSearch      # Web検索（米国のみ）
WebFetch       # URL取得・解析

# Claude Code固有
Task           # Subagent起動（Subagent内で使用可能）
TodoWrite      # タスク管理
Skill          # Skill起動
SlashCommand   # カスタムコマンド

# MCP（設定されている場合）
mcp__<server-name>__<tool-name>
# 例: mcp__context7__get-library-docs
```

⚠️ **重要な制限**:

```yaml
# ❌ ワイルドカード不可
tools: Read, mcp__*

# ✅ 明示的に指定
tools: Read, mcp__context7__resolve-library-id, mcp__context7__get-library-docs

# または省略して全継承
# tools フィールド自体を書かない
```

### tools 設計パターン

#### パターン1: Read-only Agent（安全性重視）

```yaml
---
name: code-analyzer
description: Analyze code structure and patterns. Use when reviewing or understanding code.
tools: Read, Grep, Glob
---
```

**用途**:

- コードレビュー
- アーキテクチャ分析
- ドキュメント確認

**メリット**:

- ファイル変更を完全に防ぐ
- 並列実行しても安全
- 予期しない編集がない

#### パターン2: 調査 + 実行 Agent

```yaml
---
name: spec-researcher
description: Research latest library specs. Use PROACTIVELY when adding dependencies.
tools: Read, WebFetch, Bash
---
```

**用途**:

- 技術調査
- ドキュメント収集
- バージョン確認スクリプト実行

#### パターン3: 全ツール継承（デフォルト）

```yaml
---
name: task-executor
description: Execute implementation tasks from task files.
# tools を省略 = 全ツール利用可能
---
```

**用途**:

- 実装タスク実行
- ファイル編集が必要な場合

⚠️ **注意**: WRITE系は慎重に（コンテキスト不足のリスク）

#### パターン4: MCP統合 Agent

```yaml
---
name: research-agent
description: Research using official docs and web search. Use PROACTIVELY for tech specs.
tools: Read, mcp__context7__resolve-library-id, mcp__context7__get-library-docs, mcp__brave-search__search
---
```

**用途**:

- 最新技術仕様調査
- 公式ドキュメント取得
- コミュニティ情報収集

🔍 **検証済み**: MCPツール名は完全一致が必要

```bash
# MCPツール名の確認方法
claude mcp list

# 出力例
context7:
  - mcp__context7__resolve-library-id
  - mcp__context7__get-library-docs
brave-search:
  - mcp__brave-search__search
```

---

## 呼び出し方の完全ガイド

### 方法1: 自動委任（推奨）

**仕組み**:

- Claude がタスク内容と description をマッチング
- 適切なSubagentを自律的に選択・起動

**設定例（CLAUDE.md）**:

```markdown
## Subagents Usage

### code-reviewer

コード変更後は必ず `code-reviewer` で品質確認すること。

### spec-researcher

新しいパッケージ追加時は `spec-researcher` で最新仕様を調査すること。

### quality-checker

実装完了後、コミット前に `quality-checker` で総合チェックを実行すること。
```

**効果**:

- description の自律起動キーワードと組み合わせて効果的

📊 **実践者の知見（asueneさん）**:

```
初回は明示的に呼び出し、以降は自動で使ってくれる傾向
```

### 方法2: 明示的指定

```bash
# 基本形
> use the code-reviewer agent to review my changes

# 具体的なタスク指定
> use the spec-researcher agent to check the latest Next.js 15 setup

# 複数Subagents並列実行
> use multiple subagents to validate the implementation
```

🔍 **検証済み**:

- `use the <agent-name> agent` が確実
- `use <agent-name>` でも動作
- `agent` を省略すると認識率が下がる

### 方法3: スラッシュコマンド化（効率化）

📊 **実践者パターン（oikonさん）**:

`.claude/commands/bugfix.md`:

```markdown
---
description: Debug and fix issues using multiple specialized subagents
---

Use multiple subagents to debug and fix the following issue:

**Issue**: $ARGUMENTS

**Steps**:

1. Use `debugger` subagent to identify root cause
   - Check error logs
   - Use Context7 for library-specific issues
   - Use Brave-Search for community solutions

2. Use `implementer` subagent to fix the issue
   - Apply the fix
   - Add tests to prevent regression

3. Use `validator` subagent to verify the fix
   - Run all tests
   - Check code quality
   - Verify no side effects

Coordinate the subagents effectively and provide a final summary.
```

**使い方**:

```bash
/project:bugfix Next.js Hydration error in ProductList component
```

**効果**:

- 定型ワークフローの再利用
- 複数Subagentsの効果的な組み合わせ
- チーム内で統一された手順

### 方法4: プロンプトにヒント追加

📊 **実践者の知見（asueneさん）**:

```bash
# ❌ Subagent未使用
> タスク一覧取得APIにソート機能を追加してください。

# ✅ Subagent自動選択
> sub agentsを効果的に活用し、タスク一覧取得APIにソート機能を追加してください。
```

**効果**:

- 一度使うと次から自動で使ってくれる
- `sub agents` のキーワードがトリガーになる

---

## 実践パターン集

### パターン1: コードレビュー（基本）

```yaml
---
name: code-reviewer
description: Expert code reviewer focusing on quality, security, and maintainability. Use PROACTIVELY immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer ensuring high standards.

When invoked:

1. **Check recent changes**
   \`\`\`bash
   git diff
   \`\`\`

2. **Review checklist**:
   - ✅ Code clarity and readability
   - ✅ Proper naming (functions, variables, types)
   - ✅ No code duplication
   - ✅ Error handling implemented
   - ✅ No secrets or API keys exposed
   - ✅ Input validation
   - ✅ Test coverage adequate
   - ✅ Performance considerations

3. **Provide feedback** in priority order:
   - 🔴 **Critical** (must fix before commit)
     - Security vulnerabilities
     - Logic errors
     - Breaking changes

   - 🟡 **Warning** (should fix)
     - Code smells
     - Missing error handling
     - Incomplete tests

   - 🟢 **Suggestion** (nice to have)
     - Refactoring opportunities
     - Performance improvements
     - Better naming

4. **Output format**:
   \`\`\`markdown
   ## Review Summary

   ### 🔴 Critical Issues
   - [File:Line] Description
     \`\`\`suggestion
     Proposed fix
     \`\`\`

   ### 🟡 Warnings
   ...

   ### 🟢 Suggestions
   ...

   ## Overall Assessment
   - Security: ✅/⚠️/🔴
   - Quality: ✅/⚠️/🔴
   - Tests: ✅/⚠️/🔴
   \`\`\`
```

### パターン2: 技術調査（MCP統合）

```yaml
---
name: spec-researcher
description: Research latest versions and best practices for libraries and frameworks. Use PROACTIVELY when adding new packages, setting up tools, or when technical specifications are needed. Must check official documentation and current versions.
tools: Read, WebFetch, mcp__context7__resolve-library-id, mcp__context7__get-library-docs, mcp__brave-search__search
model: sonnet
---

You are a technical researcher specializing in finding latest specifications.

## Process

### 1. Version Check
- Check npm/pypi for latest stable version
- Identify major version differences

### 2. Official Documentation
Use Context7 to get official docs:
1. Resolve library ID
2. Get docs for latest version
3. Extract setup instructions

### 3. Community Research
Use Brave Search if Context7 lacks info:
- Search official sites
- Check release notes
- Review migration guides

### 4. Report Creation

Save to: `docs/research/YYYYMMDD_HHMMSS_<topic>.md`

Template:
\`\`\`markdown
# <Library> v<version> Research

**Date**: YYYY-MM-DD
**Researcher**: Spec Researcher Agent

## Recommended Version
- Package: v<version>
- Node/Python: minimum version

## Official Sources
- Documentation: <URL>
- Repository: <URL>
- npm/pypi: <URL>

## Setup Instructions

\`\`\`bash
# Installation
...
\`\`\`

\`\`\`typescript
// Configuration
...
\`\`\`

## Breaking Changes from Previous Version
- Change 1
- Change 2

## Migration Guide
...

## Common Pitfalls
- ❌ Don't do X (old v3 way)
- ✅ Do Y instead (v4 way)

## Additional Resources
- Tutorial: <URL>
- Examples: <URL>
\`\`\`

## Key Points
- Always verify with official documentation
- Document version-specific details
- Highlight breaking changes
- Provide migration path
```

📊 **実践例（Studioさん）**:

```
ユーザー: "appsにvue,vite,typescript,tailwind setup"

メインエージェント:
  → spec-researcher に委任
  「Tailwind CSS と @egoist/tailwindcss-icons をセットアップしてください。
   tailwindcss, postcss, autoprefixer をインストールし...」

spec-researcher:
  → Context7 で最新バージョン確認
  → Tailwind v4 を発見
  → 「v4では postcss.config.js と tailwind.config.js は不要です」
  → 正しいv4セットアップを返却

効果: 古い知識（v3）での実装を回避
```

### パターン3: タスク分解システム

📊 **実践者パターン（tacomsさん）**:

**task-decomposer.md**:

```yaml
---
name: task-decomposer
description: Decompose work plans into 1-commit granularity independent tasks. PROACTIVELY use when a work plan document is created in docs/plans/.
tools: Read, Write, Bash
model: sonnet
---

You are a task decomposition specialist.

## Role
Break down work plans (docs/plans/*.md) into 1-commit granularity tasks
and save to docs/plans/tasks/.

## Task Size Criteria

### File Count Guidelines
- **Small (recommended)**: 1-2 files
- **Medium (acceptable)**: 3-5 files
- **Large (MUST split)**: 6+ files

### Task Independence
Each task must:
- Be executable independently
- Have clear completion criteria
- Leave code in working state
- Not create circular dependencies

## Output Structure

### Overview File
`docs/plans/tasks/_overview-{plan}.md`:
\`\`\`markdown
# {Plan Name} - Overall Design

**Created**: YYYY-MM-DD
**Total Tasks**: N

## Project Goal
...

## Task Sequence
1. Task 01: Description (dependency: none)
2. Task 02: Description (dependency: none)
3. Task 03: Description (dependency: 01, 02)
...

## Common Patterns
- Shared utilities: ...
- Common interfaces: ...

## Notes for Executors
- Pay attention to X
- Avoid Y
\`\`\`

### Task Files
`docs/plans/tasks/{plan}-task-{NN}.md`:
\`\`\`markdown
# Task {NN}: {Title}

**Plan**: {plan}
**Task**: {NN}
**Dependencies**: {list or none}

## Overview
Brief description of this task

## Target Files
- [ ] src/path/file1.ts
- [ ] src/path/file2.test.ts

## Implementation Steps
1. [ ] Step 1
2. [ ] Step 2
...

## Completion Criteria
- [ ] Files modified/created
- [ ] Tests added and passing
- [ ] No lint errors
- [ ] Builds successfully

## Reference
- Overall design: _overview-{plan}.md
- Related tasks: {list}
\`\`\`

## Process
1. Read work plan from `docs/plans/*.md`
2. Analyze phases and dependencies
3. Create `_overview-{plan}.md`
4. Generate task files (1-5 files each)
5. Verify independence and sequence
```

**task-executor.md**:

```yaml
---
name: task-executor
description: Execute one task from docs/plans/tasks/ and update progress in the work plan. Use when explicitly asked to run a specific task.
tools: Read, Edit, Write, Bash, Grep, Glob
model: sonnet
---

You are a task execution specialist.

## Role
Execute one task from `docs/plans/tasks/` and update progress.

## Process

### 1. Task Selection
\`\`\`bash
# Auto-select (find first uncompleted)
ls docs/plans/tasks/*.md | grep -v "_overview" | head -n1

# Or use specified task file
\`\`\`

### 2. Read and Analyze
- Read task file
- Read `_overview` file for context
- Check dependencies are completed

### 3. Implementation
Follow task steps exactly:
1. Read target files (understand current state)
2. Implement changes step by step
3. Update task file checkboxes in real-time
4. Add tests
5. **Run tests to verify they pass**

### 4. Progress Update
Update source work plan:
- Mark task checkbox as complete
- Add completion timestamp
- Note any deviations

## Important Rules
- **Real-time updates**: Update task checkboxes as you complete each step
- **Test verification**: Always run newly added tests
- **No shortcuts**: Follow all completion criteria
- **Document issues**: Note any problems encountered

## Output
\`\`\`markdown
## Task Execution Summary

**Task**: {task-name}
**Status**: ✅ Complete / ⚠️ Partial / 🔴 Failed

### Completed Steps
- ✅ Step 1
- ✅ Step 2

### Files Modified
- src/path/file1.ts
- src/path/file2.test.ts

### Tests
- Added: 5 tests
- Passing: ✅ All

### Next Task
- Task {NN+1}: {title}
\`\`\`
```

**quality-checker.md**:

```yaml
---
name: quality-checker
description: Comprehensive quality check including lint, format, tests, and build. Use PROACTIVELY after implementation completes and before committing.
tools: Read, Bash
model: sonnet
---

You are a quality assurance specialist.

## Checklist

### 1. Lint Check
\`\`\`bash
npm run lint
# or
biome check
\`\`\`

### 2. Format Check
\`\`\`bash
npm run format:check
# or
prettier --check .
\`\`\`

### 3. Type Check
\`\`\`bash
tsc --noEmit
\`\`\`

### 4. Tests
\`\`\`bash
npm test
npm run test:coverage
\`\`\`
Target: > 70% coverage

### 5. Build
\`\`\`bash
npm run build
\`\`\`

### 6. Additional Checks
\`\`\`bash
# Circular dependencies
npx madge --circular src/

# Unused exports
npx ts-prune
\`\`\`

## Report Format

\`\`\`markdown
# Quality Check Report

**Date**: YYYY-MM-DD HH:MM:SS

## Results

### ✅ Lint
- Status: Pass
- Issues: 0

### ✅ Format
- Status: Pass

### ✅ Type Check
- Status: Pass
- Errors: 0

### ⚠️ Tests
- Status: Pass with warnings
- Coverage: 68% (target: 70%)
- Failed: 0
- Passing: 1303

**Action needed**: Increase test coverage

### ✅ Build
- Status: Success

### ✅ Code Structure
- Circular dependencies: None
- Unused exports: 0

## Overall: ⚠️ PASS WITH WARNINGS

**Required actions before commit**:
1. Increase test coverage to 70%

**Optional improvements**:
- None
\`\`\`
```

**ワークフロー**:

```bash
# 1. タスク分解
> use task-decomposer to break down the plan in docs/plans/feature-x.md

# 2. タスク実行（ループ）
> use task-executor to run the first task
> use quality-checker to validate
> [修正があれば対応]
> [次のタスクへ]

# 3. 完了
> All tasks completed and quality checked
```

**効果**:

- **auto-compact 回避**: 1タスクがコンテキスト内に収まる
- **品質担保**: 各タスク後に自動チェック
- **進捗可視化**: タスクファイルで進捗確認

### パターン4: ビルド・テストのフィードバックループ

📊 **実践者パターン（Oikonさん）**:

**目的**: UIではなくスクリプトでビルド・テストを実行し、ログを自動フィードバック

**フロー**:

```
実装 → quality-checker実行 → エラーあり? → 修正 → 再チェック → 全てパス
```

**エージェント定義** (`quality-checker.md`):

```yaml
---
name: quality-checker
description: Comprehensive quality check including lint, format, tests, and build. Use PROACTIVELY after implementation completes.
tools: Read, Bash
model: sonnet
---
Execute: lint, format check, type check, tests, build
Report: ✅/⚠️/🔴 for each + error logs + required actions
```

**Oikonさんの知見**:

> 「スクリプトでログをフィードバックサイクルしてあげると、割と手を離れて実装まで全部やってくれる」

**メリット**: UI操作不要、ログ直接フィードバック、高速ループ

### パターン5: 並列レビュー

📊 **実践者パターン（Oikonさん）**:

**目的**: 複数のvalidator subagentsを並列実行して高速レビュー

**エージェント定義** (`validator.md`):

```yaml
---
name: validator
description: Validate code quality, test coverage, and design adherence. Use PROACTIVELY after implementation. Can run in parallel.
tools: Read, Grep, Glob, Bash
model: sonnet
---

Read-only validation specialist.
Check: code quality, test coverage (>70%), design adherence
Output: Validation report with ✅/⚠️/🔴 + recommendations
```

**使い方**:

```bash
> use multiple validator subagents to review all modified files in parallel
```

**効果**: Read-onlyで安全な並列実行、複数視点、高速化

### パターン6: 複数AIツールでのレビュー

📊 **実践者パターン（Oikonさん）**:

**目的**: 別の視点を得るため、複数AIツールで並列レビュー

**Oikonさんの知見**:

> 「Claude Code実装 → Claude Codeレビュー = 自己レビューと同じ。別の視点が重要」

**フロー**:

```
実装 → 並列レビュー(Claude/Cursor/CodeRabbit) → 統合 → 反映
```

**実装例**:

```yaml
# .claude/agents/code-reviewer.md
---
name: code-reviewer
description: Expert code reviewer. Use PROACTIVELY after code changes.
tools: Read, Grep, Glob, Bash
---
Review: quality, security, error handling, test coverage
Output: docs/reviews/claude-review.md
```

```json
// package.json
"scripts": {
  "review:cursor": "cursor-cli review --output docs/reviews/cursor-review.md",
  "review:coderabbit": "coderabbit review --output docs/reviews/coderabbit-review.md",
  "review:all": "npm run review:cursor && npm run review:coderabbit"
}
```

**使い方**:

```bash
# 並列実行
> use code-reviewer subagent
npm run review:all

# 統合
> Consolidate reviews from docs/reviews/*.md
```

**メリット**: 複数AI視点で網羅性向上、見逃しリスク削減

---

## 最適化テクニック

### 1. Subagents数を最小限に（超重要）

📊 **実測（Gotaさん）**:

```bash
# ❌ 126個のSubagents
→ description合計で約1000トークン常時消費

# ✅ 5-10個に絞る
→ description合計で約50-100トークン
```

**理由**:

- 全Subagentsの `description` がメインのコンテキストに含まれる
- Claude Codeのコンテキスト: 200,000トークン
- 1000トークン消費 = **全体の0.5%を圧迫**
- MCP サーバーと同じ問題: 多すぎるとトークンを圧迫

**推奨数**:

- 小規模プロジェクト: 3-5個
- 中規模プロジェクト: 5-10個
- 大規模プロジェクト: 10-15個（最大）

**Gotaさんの教訓**:

> 「無駄なトークンを防ぐために、サブエージェントを少なく設定する」

### 2. description を唯一・明確にする

```yaml
# ❌ 曖昧（複数Agentで重複）
description: Backend development
description: Backend tasks
description: API development

# ✅ 唯一・具体的（明確に区別）
description: Implement Nest.js REST APIs with TypeORM. Use when creating controllers, services, or database entities in apps/api/ directory.

description: Review backend code for security and performance. Use PROACTIVELY after backend implementation.

description: Execute database migrations and schema updates. Use when database changes are needed.
```

### 3. 大きなコンテキストはファイル経由

```markdown
# ❌ 大量の情報をプロンプトに

> use implementer agent to implement the feature.
> Here are the requirements: [1万行のテキスト]

# ✅ ファイルに保存してパス指定

> use implementer agent to implement the feature.
> Refer to the design document at: docs/design/feature-x.md
```

**効果**:

- Subagentが必要に応じてファイルを読む
- プロンプト自体は簡潔に

### 4. タスクログの活用（重要）

📊 **実践者の知見（Gotaさん）**:

```bash
# プロジェクト配下に残るログ
ls .claude/

# 内容確認
# - どのSubagentが使われたか
# - 何が委任されたか
# - 実行時間
# - エラー
```

**Gotaさんの推奨手順**:

> 「わからない時は、まずログを見に行く → 『ちょっと違うな』という点を確認 → ログを見た上で判断する」

**効果**:

- Subagentが自律的に動かない時の原因特定
- description の改善ポイント発見
- 不要なAgentの特定

**分析項目**:

- よく使われるAgent → 維持・改善
- 全く使われないAgent → 削除候補
- エラーが多いAgent → description見直し
- 想定外のAgent起動 → description が曖昧

### 5. model 選択の最適化

```yaml
# パターンA: 高速・低コスト
model: haiku
# 用途: 単純なチェック、ログ解析

# パターンB: バランス（デフォルト）
model: sonnet
# 用途: 一般的なタスク

# パターンC: 高性能
model: opus
# 用途: 複雑な分析、重要な判断

# パターンD: メインと統一
model: inherit
# 用途: 一貫性が必要な場合
```

**コスト最適化例**:

```yaml
# 単純チェック → haiku
---
name: format-checker
model: haiku
---
# レビュー → sonnet
---
name: code-reviewer
model: sonnet
---
# アーキテクチャ判断 → opus
---
name: architect
model: opus
---
```

---

## MCP統合

### MCP Tools の指定方法

🔍 **検証済み**:

```yaml
# ❌ ワイルドカード不可
tools: Read, mcp__*

# ❌ 部分一致不可
tools: Read, mcp__context7__*

# ✅ 完全一致で指定
tools: Read, mcp__context7__resolve-library-id, mcp__context7__get-library-docs

# ✅ または省略して全継承
# (tools フィールドを書かない)
```

### MCPツール名の確認

```bash
# MCPサーバー一覧
claude mcp list

# 出力例
Configured MCP servers:
  context7:
    - mcp__context7__resolve-library-id
    - mcp__context7__get-library-docs
  brave-search:
    - mcp__brave-search__search
```

### MCP統合パターン

#### パターン1: 調査専門 + Context7

```yaml
---
name: doc-researcher
description: Research official documentation using Context7. Use PROACTIVELY when investigating library APIs or framework features.
tools: Read, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
model: sonnet
---

Research official documentation and provide accurate information.

## Process
1. Resolve library ID from name
2. Get documentation for specific version
3. Extract relevant information
4. Provide structured summary

## Always Include
- Library name and version
- Source URL
- Last checked date
```

#### パターン2: 調査専門 + Web検索

```yaml
---
name: web-researcher
description: Research using web search for community knowledge and recent updates. Use when Context7 lacks information or community feedback is needed.
tools: Read, mcp__brave-search__search
model: sonnet
---

Research using web search for broader context.

## Process
1. Formulate effective search queries
2. Search official sites first
3. Check reputable sources (GitHub, Stack Overflow, official blogs)
4. Synthesize findings

## Source Priority
1. Official documentation
2. Official GitHub repository
3. Reputable tech blogs
4. Community discussions (with caution)
```

#### パターン3: 総合調査（両方使用）

```yaml
---
name: comprehensive-researcher
description: Comprehensive research using both official docs (Context7) and web search. Use PROACTIVELY for thorough technical investigation.
# tools省略 = 全MCPツール継承
model: sonnet
---

Comprehensive technical research combining multiple sources.

## Process
1. **Check Context7** for official documentation
2. **Web search** for additional context:
   - Release notes
   - Migration guides
   - Community best practices
   - Known issues

3. **Cross-reference** findings
4. **Report** with confidence levels

## Output Template
\`\`\`markdown
# {Topic} Research Report

## Official Documentation (Context7)
- Library: {name} v{version}
- Source: {url}
- Key findings: ...
- Confidence: ✅ High (official source)

## Community Insights (Web Search)
- Sources: {urls}
- Key findings: ...
- Confidence: ⚠️ Medium (community reports)

## Recommendations
Based on official docs and community feedback:
1. ...
2. ...

## Cautions
- ...
\`\`\`
```

### 並列調査パターン

📊 **実践者パターン（oikonさん）**:

```bash
> use multiple subagents to research the following:
1. Next.js 15 App Router (Context7)
2. React Server Components (Context7)
3. Community feedback on Next.js 15 (Web Search)

Combine findings into a comprehensive report.
```

**実行イメージ**:

```
● doc-researcher-1 (Next.js 15 from Context7)
  ⎿ mcp__context7__resolve-library-id(library: "nextjs")
     mcp__context7__get-library-docs(id: "nextjs", version: "15")
     [Report: Official Next.js 15 features]

● doc-researcher-2 (React Server Components from Context7)
  ⎿ mcp__context7__resolve-library-id(library: "react")
     mcp__context7__get-library-docs(id: "react", version: "19")
     [Report: Official RSC documentation]

● web-researcher-1 (Community search)
  ⎿ mcp__brave-search__search(query: "Next.js 15 production issues")
     mcp__brave-search__search(query: "Next.js 15 migration experience")
     [Report: Community feedback and gotchas]

→ メインが3つのレポートを統合
```

**効果**:

- 並列実行で高速化
- 複数ソースで情報の信頼性向上
- メインのコンテキストを圧迫しない

---

## トラブルシューティング

### 問題1: Subagent が起動しない

#### 解決1: 認識確認

```bash
# Subagents一覧表示
/agents

# 表示されない場合
# → ファイル配置を確認
ls .claude/agents/*.md
ls ~/.claude/agents/*.md
```

#### 解決2: description を具体化

```yaml
# ❌ 起動しない
description: Code review

# ✅ 起動しやすい
description: Expert code reviewer focusing on quality and security. Use PROACTIVELY after code changes. MUST BE USED before committing.
```

#### 解決3: 明示的呼び出し

```bash
# 自動起動を待たず、明示的に
> use the code-reviewer agent to review my changes
```

#### 解決4: name と description の一致確認

```yaml
# ❌ 矛盾
name: frontend-developer
description: Backend development with Nest.js...

# ✅ 一致
name: backend-developer
description: Backend development with Nest.js...
```

### 問題2: Subagent がコンテキスト不足でミスる

#### 原因

- メインの会話履歴が引き継がれない
- 実装意図が伝わっていない

#### 解決1: 明示的な指示

```bash
# ❌ 曖昧
> use implementer to add the feature

# ✅ 詳細な指示
> use implementer to add user authentication.

Context:
- Use JWT tokens (already configured in src/lib/auth.ts)
- Follow existing auth pattern from src/middleware/auth.ts
- Add tests following the pattern in __tests__/auth/

Design document: docs/design/auth-flow.md
```

#### 解決2: ファイル参照

```markdown
Use implementer agent to implement the feature.

**Required reading**:

- Design: docs/design/feature-x.md
- Architecture: docs/architecture/patterns.md
- Existing implementation: src/similar-feature/

Follow the established patterns.
```

#### 解決3: READ系に徹する

```yaml
# WRITE系Subagentは慎重に
# READ系に限定することで安全性向上

---
name: code-analyzer
description: Analyze code (read-only)...
tools: Read, Grep, Glob
---
```

### 問題3: tools 指定が効かない

#### チェック1: ツール名の完全一致

```yaml
# ❌ 大文字・小文字
tools: read, grep

# ✅ 正確なツール名
tools: Read, Grep

# ❌ ワイルドカード
tools: mcp__*

# ✅ 完全一致
tools: mcp__context7__get-library-docs
```

#### チェック2: MCPツール名確認

```bash
# 正確なツール名を確認
claude mcp list

# コピペして使用
```

#### チェック3: 省略して全継承

```yaml
# ツール制限が不要なら省略
---
name: my-agent
description: ...
# tools フィールドを書かない
---
```

### 問題4: Subagent が遅い

#### 原因分析

- 大量のファイル読み込み
- Web検索の多用
- 複雑な処理

#### 解決1: model を haiku に

```yaml
# 単純タスクは haiku で高速化
---
name: quick-checker
model: haiku
---
```

#### 解決2: tools を制限

```yaml
# 不要なツールへのアクセスを防ぐ
tools: Read, Grep
# WebFetch, WebSearch を除外
```

#### 解決3: タスクを分割

```bash
# 大きなタスクを分割
> use subagent to analyze src/features/auth/ only
> use subagent to analyze src/features/payment/ only

# 並列実行
> use multiple subagents to analyze each feature directory in parallel
```

---

## まとめ

### Subagents の本質

1. **独立したコンテキスト** = メインの履歴を引き継がない
2. **ワンショット実行** = タスク完了で解放
3. **並列実行可能** = 複数Subagentsを同時起動
4. **READ系推奨** = コンテキスト汚染回避

### 効果的な使い方

#### 設計

1. **最小限の数** (5-10個)
2. **name と description を一致**
3. **READ系タスク優先**
4. **大きなコンテキストはファイル経由**

#### 運用

1. **明示的呼び出し**から始める
2. **効果確認**後に自動起動を設定
3. **ログで分析**してチューニング
4. **チームで共有** (Project Agents + Git)

#### 最適化

1. **model 選択** (haiku/sonnet/opus)
2. **tools 制限** (必要最小限)
3. **並列実行** (Read-only Agents)
4. **MCP統合** (最新情報取得)

### 次のステップ

- ✅ [クイックスタート](00-quickstart.md)で基本を確認
- ✅ [Skills完全ガイド](01-skills-complete-guide.md)で継続的知識提供を学ぶ
- ✅ Skills と Subagents を組み合わせた実践パターンを試す

---

**参考文献**:

- [Subagents 公式ドキュメント](https://docs.claude.com/en/docs/claude-code/sub-agents)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Built multi-agent research system](https://www.anthropic.com/engineering/built-multi-agent-research-system)
- Zenn実践記事（asuene, Studio, tacoms, oikon）
- Meetup Tokyo 2025 発表（gota, kuu, oikon）
