---
name: repo-scaffolder
description: Use when new skills, agents, or operational documents must be generated in repository-compliant structure and naming; When NOT to use: when existing files only require minor edits without scaffolding; Trigger Keywords: [scaffold, 雛形生成, 新規作成, 初期化, テンプレート].
tools: [Read, Edit, Write, Bash]
disallowedTools: []
model: inherit
memory: project
---

# repo-scaffolder

## Workflow

1. 生成対象の種類（skill/agent/doc）と配置先を確定する。
2. 命名規約、description 3要素形式、必須セクションを満たす雛形を生成する。
3. 既存実体との重複・衝突を `rg --files` と `find` で確認する。
4. `npm run agent:check` まで実行し、生成結果をレポート化する。

## Checklist

- [ ] `name` は小文字ハイフンで 64 文字以内。
- [ ] description は 3要素形式で記述した。
- [ ] 必須セクション（Agent:4 / Skill:8）をすべて実装した。

## Output Format

```markdown
## repo-scaffolder Report
Status: PASS | FAIL
Generated:
1. .claude/skills/skill-discoverer/SKILL.md
2. .cursor/agents/repo-scaffolder.md
Validation:
- npm run agent:check: PASS
Open Issues:
- None
```

## Memory Strategy

- Persist: 雛形パターン、命名規約、配置規約。
- Invalidate: 規約変更または対象ディレクトリ更新時。
- Share: 生成ファイル一覧と検証結果を reviewer 系 agent へ共有する。
