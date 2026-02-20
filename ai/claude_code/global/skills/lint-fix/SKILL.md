---
name: lint-fix
description: >
  lint/format を最小差分で通す / Make lint/format pass with minimal diffs.
  Trigger: lint, format, prettier, eslint, ruff, black, gofmt
---

# 目的 / Purpose

- lint/format を通しつつ、挙動を変えない（最小差分）。

# 手順 / Steps

1. 失敗コマンドとログを確認
2. 自動修正（formatter）→ 再lint
3. ルール由来の修正は “意図” を明記して最小修正
4. 再実行で緑化確認

# 注意 / Notes

- リファクタは禁止（必要なら別PR/別タスク化）
