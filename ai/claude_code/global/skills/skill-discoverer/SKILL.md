---
name: skill-discoverer
description: Use when the user asks what skills or agents are available, or when uncertain which specialist to delegate to; When NOT to use: when the target skill is already known; Trigger Keywords: [スキル一覧, 何ができる, available skills, help, 委任先].
---

# skill-discoverer

## When to use

- 利用可能な skill/agent を一覧化して案内したい場合。
- 委任先が未確定で最適な専門家を推薦したい場合。

## When NOT to use

- 使うべき skill が既に明確で探索が不要な場合。
- 単純実装で追加の委任判断が不要な場合。

## Trigger Keywords

- スキル一覧
- 何ができる
- available skills
- help
- 委任先

## Procedure

1. `~/.claude/agents/*.md` と `~/.claude/skills/*/SKILL.md` の frontmatter を全件読み取る（存在しない場合は `.claude/` を参照）。
2. name と description を一覧表示し、利用可能資産を可視化する。
3. ユーザー目的に最も適した候補を優先順位付きで推薦する。

## Output Contract

- 推奨は必ず1件に絞る。代替は最大2件まで。
- 各候補に「使う条件 / 返す成果 / 選定理由」を1行ずつ付ける。
- 一覧の羅列で終わらせず、次に実行する具体アクションを明記する。

## Examples

### Example 1

Input: どの agent が品質監査に向くか知りたい。
Output: `~/.claude/agents` の description を比較し、候補を優先推薦する。

### Example 2

Input: 改修で使える skills を一覧で見たい。
Output: `~/.claude/skills` の name/description を列挙し、候補を提示する。

### Example 3

Input: 不具合対応で最適な委任先がわからない。
Output: 目的に合う skill/agent 候補を2〜3件選び、選定理由を示す。
