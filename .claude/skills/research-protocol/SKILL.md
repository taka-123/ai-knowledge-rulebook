---
name: research-protocol
description: Technical research protocol emphasizing official documentation and primary sources. Use when researching AI tools, frameworks, APIs, or technical specifications.
allowed-tools: Read, WebSearch, WebFetch
---

# Technical Research Protocol

技術情報の調査・ドキュメント化における厳格なプロトコルです。

## 🎯 基本原則

**グローバルルール準拠**: `~/.claude/CLAUDE.md` の「技術文書作成時の必須プロトコル」を遵守

### 1. 情報収集の厳格化

#### 優先順位

```
1. context7 (フレームワーク/ライブラリ/SDK)
   ↓
2. 公式ドキュメント
   ↓
3. 公式 GitHub リポジトリ
   ↓
4. WebSearch (公式発表・リリースノート)
   ↓
5. 信頼できるコミュニティ (最後の手段)
```

#### 重要な原則

- **そのまま引用**: 「理解して要約」ではなく「確認してそのまま引用」
- **解釈禁止**: 推測が必要な場合は明示的に注記（例: 「未確認」「推測」）

### 2. 出典と検証

**すべての技術的記述に必須**:

```markdown
**出典**: [公式ドキュメント](https://example.com/docs)
**取得日**: 2025-01-05
**バージョン**: v1.2.3
```

### 3. 不確実性の明示

確信度が80%未満の場合:

```markdown
⚠️ **未確認**: 公式ドキュメントに明記なし（推測）
```

## 📊 実践手順

### ステップ1: 情報源の特定

```bash
# 1. context7 で確認（フレームワーク・ライブラリの場合）
> Check context7 for [library-name] latest version

# 2. 公式ドキュメント検索
> WebSearch: "[library-name] official documentation"

# 3. 公式 GitHub 確認
> WebFetch: https://github.com/[org]/[repo]/blob/main/README.md
```

### ステップ2: 原文確認

```markdown
# ❌ 誤り（推測で記載）
環境変数 `HOOK_INPUT` から取得可能

# ✅ 正しい（公式確認後）
stdinからJSON取得（公式Hooks Referenceより）
```

### ステップ3: 出典付与

すべての仕様に **URL + 日付** を付与:

```markdown
## API仕様

**認証方式**: Bearer Token

**出典**: [Authentication - Official Docs](https://api.example.com/docs/auth)
**取得日**: 2025-01-05
**確認バージョン**: API v2.1
```

### ステップ4: クロスチェック

重要な仕様は **複数ソース** で確認:

```markdown
**一次情報**: 公式ドキュメント
**裏付け**: 公式 GitHub の実装例
**コミュニティ**: Stack Overflow の公式回答
```

## 🚨 NG パターン

### ❌ 推測での記載

```markdown
# 悪い例
Claude Code では環境変数でフック入力を取得できます。

# 良い例
Claude Code では stdin から JSON 形式でフック入力を取得します。
（出典: Claude Code Hooks Reference, 2025-01-05）
```

### ❌ 古い情報の混在

```markdown
# 悪い例
Tailwind CSS はpostcss.config.jsが必要です。

# 良い例
⚠️ バージョン注意: Tailwind CSS v4 では postcss.config.js は不要です。
（v3 以前は必要でした）
（出典: Tailwind CSS v4 Migration Guide, 2025-01-05）
```

### ❌ 不確実性の隠蔽

```markdown
# 悪い例
このフックは実行時に自動的に発火します。

# 良い例
⚠️ 未確認: フックの自動発火タイミングは公式ドキュメントに明記なし。
検証が必要です。
```

## ✅ 推奨パターン

### テンプレート

```markdown
# [技術名] 調査結果

**調査日**: 2025-01-05
**対象バージョン**: v1.2.3

## 公式情報

**出典**: [公式ドキュメント](https://example.com)
**取得日**: 2025-01-05

### 主要仕様

[原文からの引用または正確な要約]

## 検証結果

- ✅ 確認済み: [項目]
- ⚠️ 未確認: [項目]
- ❌ 誤り: [訂正内容]

## 更新推奨時期

**鮮度確認**: 月1回推奨（API仕様変更の可能性あり）
```

## 参照

- グローバルルール: `~/.claude/CLAUDE.md` - 技術文書作成時の必須プロトコル
- プロジェクトルール: [CLAUDE.md](../../CLAUDE.md)
