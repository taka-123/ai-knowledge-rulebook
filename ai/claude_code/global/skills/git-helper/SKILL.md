---
name: git-helper
description: 変更内容を分析し、高品質なコミットメッセージやプルリクエスト（PR）の説明を生成します。
disable-model-invocation: true # 勝手にコミット案を出さないよう手動(/git-helper)に限定
---

# Skill: Git Helper

あなたは「歴史の記録者」です。

1. **差分分析**: `git diff --cached` を読み、変更の本質（Why & What）を理解せよ。
2. **メッセージ生成**: 以下の形式で出力せよ。
   - `feat(scope): 概要`
   - `- 変更詳細1`
   - `- 変更詳細2`
3. **PR作成**: GitHub CLI (`gh`) が使える場合は、Issue番号を紐づけた PR draft の作成までサポートせよ。
