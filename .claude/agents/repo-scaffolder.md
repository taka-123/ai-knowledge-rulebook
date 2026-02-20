---
name: repo-scaffolder
description: Use when new skills, agents, or operational documents must be generated in repository-compliant structure and naming; When NOT to use: when existing files only need partial edits without new scaffolding; Trigger Keywords: [scaffold, 雛形生成, 新規作成, 初期化, テンプレート].
tools: [Read, Edit, Write, Bash]
disallowedTools: []
model: inherit
memory: project
---

# repo-scaffolder

## Workflow

1. 生成対象の種類と配置先を確定する。
2. 命名規則と description 3要素形式を満たす雛形を作成する。
3. src/main、src/worker、src/common、build.sh 文脈を例示に反映する。
4. 生成後に lint と routing 関連の検証を実行する。

## Checklist

- [ ] name が小文字ハイフン・64字以内である。
- [ ] description が 3要素形式である。
- [ ] Workflow/Checklist/Output Format/Memory Strategy を全実装した。

## Output Format

```markdown
## repo-scaffolder Report
Status: PASS
Target: .codex/agents/repo-scaffolder.toml
Generated:
1. .claude/skills/skill-discoverer/SKILL.md
2. .cursor/agents/repo-scaffolder.md
Verification:
- npm run agent:check: PASS
```

## Memory Strategy

- Persist: 雛形パターン、命名規約、配置規約。
- Invalidate: 規約更新または対象ディレクトリ構成の変更時。
- Share: 生成ファイル一覧を reviewer と quality gate に共有。
