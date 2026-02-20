---
name: lint-fix
description: >
  lint/format を最小差分で通す / Make lint/format pass with minimal diffs.
  Trigger: lint, format, eslint, prettier, ruff, black, gofmt
---

# 目的

- 挙動を変えずに lint/format を通す。

# 手順

1. ログ確認
2. formatter → 再lint
3. ルール修正は最小差分
