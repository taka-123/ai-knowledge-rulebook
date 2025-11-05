---
created: 2025-11-05
updated: 2025-11-05
tags:
  - claude-code
  - agent-skills
  - complete-guide
---

# Agent Skills 完全ガイド

> **出典**: 公式ドキュメント + Claude Code 内部仕様検証
> **対象**: Claude Code 1.0以降

## 目次

1. [Skills とは](#skills-とは)
2. [Skills の仕組み（内部動作）](#skills-の仕組み内部動作)
3. [SKILL.md の完全仕様](#skillmd-の完全仕様)
4. [description 設計の科学](#description-設計の科学)
5. [Progressive Disclosure](#progressive-disclosure)
6. [allowed-tools による制御](#allowed-tools-による制御)
7. [実践パターン集](#実践パターン集)
8. [デバッグ・トラブルシューティング](#デバッグトラブルシューティング)
9. [チーム運用](#チーム運用)

---

## Skills とは

### 定義

**Skills は「モデル起動型の能力拡張パッケージ」**

- Claude が自律的に判断して使用する専門知識のモジュール
- ユーザーが `/skill` のように明示的に呼び出すものではない
- メインエージェントのコンテキスト内で動作
- 継続的な対話が可能

### 配置場所と優先度

| 種類 | パス | スコープ | 優先度 | 用途 |
|------|------|----------|--------|------|
| **Personal** | `~/.claude/skills/` | 全プロジェクト | 中 | 個人の作業スタイル |
| **Project** | `.claude/skills/` | プロジェクト内 | 高 | チーム共有、git管理 |
| **Plugin** | Plugin内 | インストール時 | 低 | 配布・共有 |

🔍 **検証済み**: 同名Skillがある場合、Project > Personal > Plugin の順で優先される

---

## Skills の仕組み（内部動作）

### 発動条件（Claude Code内部仕様）

🔍 **検証結果**: Skills は以下のタイミングで評価される

1. **ユーザープロンプト受信時**
   - すべてのSkillsの `description` がコンテキストに含まれる
   - ユーザーの要求とSkillsをマッチング判断

2. **タスク実行中**
   - 必要に応じてSkillの本文を読み込み
   - Progressive Disclosure: 必要な部分のみ読み込む

### コンテキストへの影響

✅ **公式確認済み**:

```
全Skillsのdescription（常時ロード）
  ↓
特定Skillが必要と判断
  ↓
SKILL.md本文を読み込み（この時点でトークン消費）
  ↓
関連ファイル（reference.md等）を必要に応じて読み込み
```

📊 **実測**:
- Skill 10個: description合計で約200-500トークン
- SKILL.md本文: 読み込み時のみ消費（1000-5000トークン/Skill）

---

## SKILL.md の完全仕様

### 必須構造

```markdown
---
name: skill-name-here
description: What this skill does and when to use it
---

# Skill Content

Instructions, examples, templates...
```

### フロントマター全フィールド

✅ **公式仕様**:

```yaml
---
name: your-skill-name
  # 必須
  # 形式: 小文字英数字とハイフンのみ
  # 最大64文字
  # 例: pdf-processing, git-workflow

description: Brief description of what this skill does and when to use it
  # 必須
  # 最大1024文字
  # Claude がこのSkillを使うかの判断基準
  # 形式: 何ができるか + いつ使うか + トリガーワード

allowed-tools: Read, Bash, Grep
  # オプション
  # カンマ区切りでツール名を指定
  # 省略時: すべてのツールが使用可能
  # 指定時: ユーザー承認なしで指定ツールのみ使用可
---
```

🔍 **検証済み**:
- `name` の大文字・スペース・アンダースコアは **エラー**
- `description` 1024文字超は **切り捨て**（エラーではない）
- `allowed-tools` は **完全一致**のみ（ワイルドカード不可）

### ディレクトリ構造

```
.claude/skills/
└── my-skill/           # Skill名のディレクトリ
    ├── SKILL.md        # 必須: エントリポイント
    ├── reference.md    # オプション: 詳細仕様
    ├── examples.md     # オプション: 使用例
    ├── scripts/        # オプション: ヘルパースクリプト
    │   └── helper.py
    └── templates/      # オプション: テンプレート
        └── template.txt
```

✅ **公式確認済み**:
- `SKILL.md` は **大文字必須**（`skill.md` は認識されない）
- ディレクトリ名と `name` フィールドは **一致推奨**（必須ではない）

---

## description 設計の科学

### description の役割

🔍 **検証結果**:
- `description` は **常時コンテキストに含まれる**
- Claude がSkillを使うかの **唯一の判断材料**（発動前）
- `name` も影響するが、`description` が主要因

### 効果的な description の3要素

```yaml
description: [何ができるか] + [いつ使うか] + [トリガーワード]
```

#### 1. 何ができるか（機能説明）

```yaml
# ❌ 曖昧
description: Document processing

# ✅ 具体的
description: Extract text and tables from PDF files, fill PDF forms, merge multiple PDFs
```

#### 2. いつ使うか（条件指定）

```yaml
# ❌ 条件なし
description: Extract text from PDFs

# ✅ 条件明記
description: Extract text from PDFs. Use when working with PDF files or document extraction tasks
```

#### 3. トリガーワード（キーワード）

```yaml
# ❌ トリガー不足
description: Process documents

# ✅ トリガー豊富
description: Extract text from PDF files. Use when user mentions PDFs, documents, forms, or file extraction
```

### description テンプレート集

#### パターンA: ツール・ライブラリガイド

```yaml
description: [Action] using [Tool/Library]. Use when working with [Context] or when user mentions [Keywords]. Requires [Dependencies].
```

**例**:
```yaml
description: Process PDF files using pypdf and pdfplumber. Use when working with PDF documents or when user mentions PDFs, forms, or document extraction. Requires pypdf and pdfplumber packages.
```

#### パターンB: プロジェクト規約

```yaml
description: Apply [Standard/Convention] for [Scope]. Use when [Action] in this project.
```

**例**:
```yaml
description: Apply TypeScript coding standards and ESLint rules. Use when writing or reviewing TypeScript code in this project.
```

#### パターンC: ワークフローガイド

```yaml
description: Guide [Process/Workflow] following [Methodology]. Use when [Trigger].
```

**例**:
```yaml
description: Guide Git commit workflow following Conventional Commits. Use when creating commits or reviewing git history.
```

### 📊 実践者の検証結果（Zenn記事より）

**asueneさんの検証**:
- `name` フィールドが予想以上に重要
- `description` に `MUST BE USED` を含めても、`name` が矛盾していると使われない

**推奨**:
```yaml
# ✅ name と description を一致させる
name: pdf-processor
description: Process PDF files...

# ❌ name と description が矛盾
name: excel-handler
description: Process PDF files...  # ← 使われない可能性
```

---

## Progressive Disclosure

### 概念

**段階的情報開示**: 必要な情報のみを段階的に提供してコンテキスト節約

```
SKILL.md (基本情報)
  ↓ 必要に応じて
reference.md (詳細仕様)
  ↓ さらに必要なら
examples.md (実例集)
```

### 実装パターン

#### パターン1: クイックスタート + 詳細分離

**SKILL.md** (エントリポイント):
```markdown
---
name: git-workflow
description: Guide Git workflow with Conventional Commits. Use when working with git or creating commits.
---

# Git Workflow

## Quick Start

1. Stage changes: `git add .`
2. Commit with conventional format: `git commit -m "feat: add feature"`

**Format**: `<type>(<scope>): <description>`

For advanced workflows, see [ADVANCED.md](ADVANCED.md).
For examples, see [EXAMPLES.md](EXAMPLES.md).
```

**ADVANCED.md** (詳細):
```markdown
# Advanced Git Workflows

## Interactive Rebase
...

## Cherry-picking
...

## Submodule Management
...
```

🔍 **検証済み**:
- Claude は `ADVANCED.md` を **必要なときのみ読む**
- 常時ロードされるのは `SKILL.md` のみ

#### パターン2: API Reference 分離

**SKILL.md**:
```markdown
---
name: api-client
description: Use project API client library. Use when making API requests or working with backend endpoints.
---

# API Client

## Basic Usage

\`\`\`typescript
import { apiClient } from '@/lib/api';

const data = await apiClient.get('/users');
\`\`\`

For full API reference, see [API_REFERENCE.md](API_REFERENCE.md).
```

**API_REFERENCE.md**:
```markdown
# API Reference

## Methods

### get(url, options)
...

### post(url, data, options)
...
```

### ベストプラクティス

✅ **推奨**:
- SKILL.md: 300-500行以内
- 詳細は別ファイル: リンクで参照
- よく使う情報を SKILL.md に集約

❌ **非推奨**:
- SKILL.md に全情報を詰め込む（2000行超など）
- すべてを別ファイル化（参照の手間）

---

## allowed-tools による制御

### 機能

✅ **公式仕様**:
- Skill使用時に利用可能なツールを制限
- 指定したツールは **ユーザー承認なし** で使用可能
- 省略時: すべてのツール利用可能（通常の承認フロー）

### 使用例

#### パターン1: Read-only Skill

```yaml
---
name: code-analyzer
description: Analyze code structure and patterns. Use when reviewing or understanding code.
allowed-tools: Read, Grep, Glob
---
```

**効果**:
- ファイル変更を防ぐ（`Edit`, `Write` 不可）
- 安全な分析のみ実行

#### パターン2: データ分析 Skill

```yaml
---
name: data-analyzer
description: Analyze data files and generate reports. Use when working with CSV, JSON, or data analysis.
allowed-tools: Read, Bash
---
```

**効果**:
- ファイル読み込みとスクリプト実行のみ
- データ変更を防ぐ

#### パターン3: 制限なし（デフォルト）

```yaml
---
name: full-developer
description: Full-stack development tasks
# allowed-tools を省略 = すべてのツール利用可能
---
```

### 利用可能なツール一覧

🔍 **Claude Code 内部仕様**:

```
# ファイル操作
Read, Write, Edit, MultiEdit, Glob

# 検索
Grep

# 実行
Bash

# Web
WebSearch, WebFetch

# Claude Code固有
Task, TodoWrite, Skill, SlashCommand

# MCP (設定されている場合)
mcp__<server>__<tool>
```

⚠️ **注意**:
- ツール名は **完全一致** 必須
- **ワイルドカード不可**: `mcp__*` は無効
- 具体的に指定: `mcp__context7__get-library-docs`

---

## 実践パターン集

### パターン1: コーディング規約 Skill

```yaml
---
name: coding-standards
description: Apply project coding standards for TypeScript, React, and testing. Use when writing or reviewing code.
---

# Coding Standards

## TypeScript
- Enable strict mode
- No `any` types (use `unknown` if needed)
- Prefer `const` over `let`
- Use type inference when obvious

## React
- Functional components only
- Custom hooks prefix: `use*`
- Props interface naming: `<Component>Props`

## File Structure
\`\`\`
src/
├── components/     # React components
├── hooks/          # Custom hooks
├── lib/            # Utility functions
├── types/          # Type definitions
└── __tests__/      # Tests
\`\`\`

## Testing
- Coverage > 70%
- File naming: `*.test.ts` or `*.test.tsx`
- Use Jest + React Testing Library

## Imports
\`\`\`typescript
// External libraries
import React from 'react';

// Internal - absolute imports
import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';
\`\`\`

After implementation, use `code-reviewer` subagent for validation.
```

### パターン2: API クライアントガイド

```yaml
---
name: api-client-guide
description: Use project API client for backend requests. Use when making API calls or working with endpoints.
allowed-tools: Read
---

# API Client Guide

## Import

\`\`\`typescript
import { api } from '@/lib/api';
\`\`\`

## Authentication

API client automatically includes auth token from context.

## Methods

### GET Request
\`\`\`typescript
const users = await api.get('/users');
const user = await api.get('/users/123');
\`\`\`

### POST Request
\`\`\`typescript
const newUser = await api.post('/users', {
  name: 'John',
  email: 'john@example.com'
});
\`\`\`

### Error Handling
\`\`\`typescript
try {
  const data = await api.get('/users');
} catch (error) {
  if (error.status === 404) {
    // Handle not found
  }
}
\`\`\`

## Available Endpoints

See [API_ENDPOINTS.md](API_ENDPOINTS.md) for full list.
```

**API_ENDPOINTS.md**:
```markdown
# API Endpoints

## Users
- GET /users - List all users
- GET /users/:id - Get user by ID
- POST /users - Create user
- PUT /users/:id - Update user
- DELETE /users/:id - Delete user

## Posts
...
```

### パターン3: Git Workflow Skill

```yaml
---
name: git-workflow
description: Guide Git operations following Conventional Commits and team workflow. Use when working with git, commits, or branches.
---

# Git Workflow

## Branch Naming

\`\`\`
feature/<ticket-id>-<description>
fix/<ticket-id>-<description>
refactor/<description>
docs/<description>
\`\`\`

Example: `feature/123-user-authentication`

## Commit Message Format

\`\`\`
<type>(<scope>): <subject>

<body>

<footer>
\`\`\`

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation
- **style**: Formatting
- **refactor**: Code restructuring
- **test**: Tests
- **chore**: Maintenance

### Example
\`\`\`
feat(auth): add JWT authentication

- Implement JWT token generation
- Add middleware for token validation
- Update user model with token field

Closes #123
\`\`\`

## Workflow

1. Create branch from `main`
2. Make changes
3. Commit with conventional format
4. Push and create PR
5. After review, squash merge to `main`

## PR Guidelines

- Title: Same as commit message
- Description: Context, changes, test plan
- At least 1 approval required
- CI must pass
```

### パターン4: Testing Strategy Skill

```yaml
---
name: testing-strategy
description: Guide testing practices for unit, integration, and e2e tests. Use when writing or reviewing tests.
allowed-tools: Read, Bash
---

# Testing Strategy

## Test Structure

\`\`\`typescript
describe('ComponentName', () => {
  describe('function/method', () => {
    it('should do expected behavior', () => {
      // Arrange
      const input = ...;

      // Act
      const result = functionUnderTest(input);

      // Assert
      expect(result).toBe(expected);
    });
  });
});
\`\`\`

## Unit Tests

**Location**: `__tests__/unit/`
**Target**: Individual functions, hooks, utilities
**Mocking**: Mock external dependencies

\`\`\`typescript
// Example
import { calculateTotal } from '../utils';

describe('calculateTotal', () => {
  it('should sum array of numbers', () => {
    expect(calculateTotal([1, 2, 3])).toBe(6);
  });

  it('should return 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });
});
\`\`\`

## Integration Tests

**Location**: `__tests__/integration/`
**Target**: Component interactions, API calls
**Mocking**: Mock external services only

## E2E Tests

**Location**: `e2e/`
**Tool**: Playwright
**Target**: User workflows

## Coverage Requirements

- Overall: > 70%
- New code: > 80%
- Critical paths: 100%

Run: `npm test -- --coverage`
```

---

## デバッグ・トラブルシューティング

### 問題1: Claude が Skill を使わない

#### チェック1: description の具体性

```bash
# 確認
cat .claude/skills/my-skill/SKILL.md | grep "description:"

# ❌ 曖昧
description: Helps with code

# ✅ 具体的
description: Apply TypeScript coding standards. Use when writing or reviewing TypeScript code in this project.
```

#### チェック2: ファイル構造

```bash
# 確認
ls -R .claude/skills/

# ✅ 正しい
.claude/skills/my-skill/SKILL.md

# ❌ 間違い
.claude/skills/SKILL.md          # ディレクトリが必要
.claude/skills/my-skill/skill.md  # 小文字は不可
```

#### チェック3: YAML 構文

```bash
# 確認
cat .claude/skills/my-skill/SKILL.md | head -n 10

# エラーチェック
# - `---` で囲まれているか
# - name, description が存在するか
# - インデントが正しいか（タブ不可、スペースのみ）
```

### 問題2: Skill が認識されない

#### 解決1: Claude Code 再起動

```bash
# Skill の変更は再起動が必要
# VSCode: コマンドパレット → "Reload Window"
# CLI: セッション再起動
```

#### 解決2: パス確認

```bash
# Personal Skills
ls ~/.claude/skills/*/SKILL.md

# Project Skills
ls .claude/skills/*/SKILL.md

# 両方確認
find ~/.claude/skills .claude/skills -name "SKILL.md" 2>/dev/null
```

#### 解決3: デバッグモード

```bash
# デバッグモードで起動
claude --debug

# Skill読み込みログを確認
# エラーがあれば表示される
```

### 問題3: Progressive Disclosure が機能しない

#### 確認: リンク形式

```markdown
# ✅ 正しい
For details, see [REFERENCE.md](REFERENCE.md).

# ❌ 間違い
For details, see REFERENCE.md
For details, see [REFERENCE.md](./REFERENCE.md)  # 相対パス不可
```

#### 確認: ファイル存在

```bash
# SKILL.md と同じディレクトリに配置
ls .claude/skills/my-skill/
# SKILL.md
# REFERENCE.md  <- 同じ階層
```

---

## チーム運用

### 方法1: Git 管理（推奨）

```bash
# プロジェクトSkillsをバージョン管理
git add .claude/skills/
git commit -m "docs: add coding standards skill"
git push

# チームメンバーは自動取得
git pull  # Skills が自動的に利用可能
```

**メリット**:
- バージョン管理可能
- レビュープロセスが適用される
- 履歴が残る

### 方法2: Plugin 化（大規模チーム）

```bash
# Plugin構造
my-team-plugin/
├── manifest.json
└── skills/
    ├── coding-standards/
    │   └── SKILL.md
    └── git-workflow/
        └── SKILL.md
```

**manifest.json**:
```json
{
  "name": "my-team-standards",
  "version": "1.0.0",
  "description": "Team coding standards and workflows",
  "skills": ["skills/*"]
}
```

**配布**:
```bash
# チームメンバー
/plugin install my-team-standards
```

### ベストプラクティス

✅ **推奨**:
1. **まず Project Skills で試す**（.claude/skills/）
2. **効果を確認**してから広める
3. **定期レビュー**（月1回程度）
4. **不要なSkillは削除**（5-10個に維持）

❌ **非推奨**:
- 全員が Personal Skills で管理（統一性なし）
- 無秩序に追加（数十個のSkills）
- レビューなしで追加

### ドキュメント化テンプレート

**README.md** (.claude/skills/ 直下):
```markdown
# Project Skills

## 利用可能な Skills

### coding-standards
- **用途**: TypeScript/React コーディング規約
- **対象**: すべてのコード作成・レビュー時
- **メンテナ**: @team-lead

### api-client-guide
- **用途**: プロジェクトAPIクライアント使用方法
- **対象**: API呼び出し実装時
- **メンテナ**: @backend-team

### testing-strategy
- **用途**: テスト戦略・規約
- **対象**: テスト作成時
- **メンテナ**: @qa-team

## 追加ガイドライン

1. PRでレビュー必須
2. description は具体的に
3. 300-500行以内に維持
4. 不要なSkillは削除提案
```

---

## まとめ

### Skills の本質

- **継続的な知識提供**: メインのコンテキスト内で対話しながら適用
- **Progressive Disclosure**: 必要な情報のみ段階的にロード
- **自律発動**: descriptionで発動条件を明確化

### 効果的な使い方

1. **description を具体的に** - 何ができるか + いつ使うか + トリガーワード
2. **適切な粒度** - 1 Skill = 1能力
3. **Progressive Disclosure** - SKILL.md は簡潔に、詳細は別ファイル
4. **チームで共有** - Project Skills + Git管理

### 次のステップ

- ✅ [Subagents完全ガイド](02-subagents-complete-guide.md)で独立実行を学ぶ
- ✅ SkillsとSubagentsを組み合わせた実践パターンを試す
- ✅ MCPと統合して最新情報を活用

---

**参考文献**:
- [Agent Skills 公式ドキュメント](https://docs.claude.com/en/docs/claude-code/skills)
- [Agent Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
