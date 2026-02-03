---
name: agent-factory
description: ユーザーの要求に基づき、新しい Subagent または Skill を設計・生成します。
disable-model-invocation: true
---

1. 要求分析: Subagent(環境分離)か Skill(知識)かを判定。
2. 規律注入: 生成物に「URL付与義務」と「RFC準拠」を必ず含める。
3. ツール選択: Cursor用なら `context7` を、CC用なら `allowed-tools` 制限を含めたテンプレートを提供せよ。
