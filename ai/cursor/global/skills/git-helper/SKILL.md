---
name: git-helper
description: 変更内容を分析し、Conventional Commits 形式のメッセージと高品質な PR 説明文を生成。
disable-model-invocation: true
---

1. **差分分析**: `git diff --cached` を読み、変更の「Why（なぜ）」と「What（何を）」を言語化せよ。
2. **メッセージ生成**: Conventional Commits 形式で 3 つの候補を提示せよ。
3. **PR/Issue連携**: GitHub CLI (`gh`) が利用可能な場合、関連Issueを紐づけた PR draft を作成せよ。
