---
name: documentation-standards
description: Enforces repo documentation standards for notes/clips/ai/policy/snippets. Use when writing docs, reviews, or when the user mentions documentation standards, notes, clips, ai profile.
disable-model-invocation: true
---

# Documentation Standards

## Scope

- `notes/`: FrontMatter 必須、H1 は 1 つのみ
- `clips/`: 引用元 URL と取得日が必須
- `ai/`: スキーマ適合と既存スタイル踏襲
- `policy/`: 既存スタイル維持、最小変更
- `snippets/`: 見出し構造とコードブロックの言語指定

## Required Checks

- 見出し階層の整合
- 外部リンクに取得日があること
- 推測と事実の区別が明確であること
- 機密情報や個人情報が含まれないこと

## Output Format

対象:
FrontMatter:

- ...
  見出し:
- ...
  リンク:
- ...
  禁止事項:
- ...

## Verification

- Write 後は `./format.sh check` の結果を添える。
