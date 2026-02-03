---
name: content-scaffold
description: 新規ファイル生成時のテンプレート適用と必須バリデーションを行うスキル。キーワード「新規ファイル」「テンプレート」「scaffold」「ノート作成」「新規追加」で自動検出。repo-scaffolder エージェントの知識を再利用可能なスキルとして提供する。
user-invocable: true
allowed-tools: Read, Glob, Bash
disable-model-invocation: false
---

# Content Scaffold Skill

新規ファイル生成時に適切なテンプレートを自動適用し、必須フィールドの欠落を防止するスキルです。

## 対象と テンプレート

対象ディレクトリに応じてテンプレートを切り替える。

### notes/

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - [tag]
---

# [タイトル]

[本文]
```

**バリデーション**:

- `created` と `updated` は本日の日付
- `tags` は1つ以上
- H1は1つのみ

### clips/

```markdown
# [記事タイトル]

**引用元**: [URL]
**取得日**: YYYY-MM-DD

## 要約

[要約本文]

## キーポイント

- [要点1]
- [要点2]
```

**バリデーション**:

- 引用元URLが存在すること
- 取得日が付与されていること

### ai/ プロファイル

生成前に必ず以下を実行：

1. `schemas/ai_profile.schema.json` を読み込み、必須フィールドと型を確認する。
2. 既存プロファイルのサンプルを読み込み、スタイルを把握する。
3. スキーマに適合する構造で生成する。

**バリデーション**:

- 生成後に `npm run schema:check` で適合性を確認する。

### snippets/

```markdown
# [スニペット名]

## 目的

[何のために使うか]

## コンテンツ

[本文]
```

**バリデーション**:

- コードブロックには言語指定を付与すること

## 命名規則

新規ファイル名は**既存ファイルの命名規則に合わせる**。勝手な命名は禁止。生成前に対象ディレクトリの既存ファイル一覧を確認し、パターンを特定する。

## 生成後の検証

ファイル生成後に必ず以下を実行し、結果を報告する：

```bash
./format.sh check
```

JSON の場合は追加で：

```bash
npm run schema:check
```

## 報告形式

```markdown
## Scaffold 結果

**生成ファイル**: [パス]
**適用テンプレート**: [notes / clips / ai / snippets]
**バリデーション**: ✅ / ⚠️ [詳細]
**検証コマンド結果**: [./format.sh check の結果サマリー]
```
