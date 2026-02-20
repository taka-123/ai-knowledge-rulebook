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

1. `.claude/agents/*.md` と `.claude/skills/*/SKILL.md` の frontmatter を全件読み取る。
2. name と description を一覧表示し、利用可能資産を可視化する。
3. ユーザー目的に最も適した候補を優先順位付きで推薦する。

## Examples

### Example 1

Input: どの agent が src/main の品質監査に向くか知りたい。
Output: .claude/agents の description を比較し、doc-validator と repo-cartographer を優先推薦する。

### Example 2

Input: build.sh 改修で使える skills を一覧で見たい。
Output: .claude/skills の name/description を列挙し、task-planner と format-lint-audit を提示する。

### Example 3

Input: src/worker 不具合対応で最適な委任先がわからない。
Output: 目的に合う skill/agent 候補を2〜3件選び、選定理由を示す。
