---
name: content-scaffold
description: Applies repo templates for new notes/clips/ai/snippets files. Use when the user mentions 新規ファイル, テンプレート, scaffold, ノート作成, clips, or AIプロファイル.
disable-model-invocation: true
---

# Content Scaffold

## Templates

### notes/

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - tag
---

# タイトル

本文
```

### clips/

```markdown
# 記事タイトル

**引用元**: [URL]
**取得日**: YYYY-MM-DD

## 要約

要約本文

## キーポイント

- 要点1
- 要点2
```

### ai/ (profile)

1. `schemas/ai_profile.schema.json` を読み、必須フィールドを確認する。
2. 既存の ai/ プロファイルのスタイルを踏襲する。
3. 生成後に `npm run schema:check` を実行する。

### snippets/

```markdown
# スニペット名

## 目的

用途

## コンテンツ

本文
```

## Rules

- 命名は既存ファイルに合わせる。
- H1 は 1 つのみ。
- 外部リンクは取得日を付与する。

## Verification

- 作成後に `./format.sh check` を実行する。
