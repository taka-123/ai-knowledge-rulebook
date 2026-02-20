---
name: skill-discoverer
description: >
  スキル/エージェントを探索して最適な呼び出し案を提示 / Discover the right skill/agent to use.
  Trigger: どのスキル, どのエージェント, routing, dispatch, 自動選定
---

# 目的 / Purpose

- 依頼内容から「どの agent / skill を使うと最短か」を提案する（実行はユーザー承認があってから）。

# 手順 / Steps

1. 依頼内容を 1 行で要約
2. 該当しそうな agent/skill を最大 3 つ提示（理由付き）
3. それぞれの “呼び出し文” を提示（コピペ可能）
4. 追加で作るべき skill/agent がある場合は 1 つだけ提案（過剰生成しない）

# 出力 / Output

- 推奨（1つ） / 代替（最大2つ）
- それぞれ「いつ使うか」「何を返すか」を短く
