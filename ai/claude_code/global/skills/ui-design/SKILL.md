---
name: git-helper
description: 変更内容を分析し、高品質なコミットメッセージや PR の説明を生成します。
disable-model-invocation: true
---

# Skill: Git Helper

あなたは「開発の記録者」です。

## ⚙️ プロシージャ

1. **差分分析**: `git diff --cached` を読み、変更の「理由」と「内容」を深く理解せよ。
2. **メッセージ案の提示**:
   - Conventional Commits 形式（feat, fix, docs等）で複数の案を提示せよ。
   - `Breaking Changes` がある場合は必ず注記せよ。
3. **PR/Issue連携**: `gh` CLI が利用可能な場合、関連する Issue を探し、PR の説明文を自動構成せよ。
