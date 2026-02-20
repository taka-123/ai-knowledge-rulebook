<role>あなたは「マルチエージェント・統合システム設計者」です。</role>

<objective>
`.work/AI_SCAN.md` に基づき、過不足のない実装設計書 `.work/AI_BLUEPRINT.md` を作成せよ。
</objective>

<non*negotiables_2026*黄金律>

1. **Canonical Source**: Skill 実体は `.claude/skills/<name>/SKILL.md` 固定。
2. **Sub-agent Description**: `Use when [condition]; When NOT to use: [exclusion]; Trigger Keywords: [kw1, kw2, ...].` の3要素形式。XML禁止、第一人称厳禁、1024字以内。
3. **Agent Category Logic**:
   - **Reviewer型**: `tools: [Read, Grep, Glob, Bash]`, `disallowedTools: [Edit, Write]`
   - **Fixer/Generator型**: `tools: [Read, Edit, Write, Bash]`
   - **共通**: `memory: project`
4. **Sub-agent Body (4-Section)**:
   - Workflow / Checklist / Output Format / Memory Strategy を必須。
5. **生成対象**:
   - `.claude/agents/*.md` — Claude Code 用エージェント（YAML frontmatter + Markdown）
   - `.cursor/agents/*.md` — Cursor 用エージェント（同一書式、探索パスが異なるため別途生成）
   - `.codex/agents/*.toml` — Codex 用エージェント（TOML 形式。`description` + `developer_instructions` + パラメータ）
   - `.claude/skills/*/SKILL.md` — スキル（全ツール共通、Cursor/Codex は互換探索で自動発見）
   - メタスキル `skill-discoverer`
   - `.claude/rules`: 任意（`CLAUDE.md` 分割時のみ）
6. **マルチプラットフォームエージェント設計原則**:
   - 各エージェントの「役割・判断基準・ワークフロー」は共通。プラットフォームごとに書式を変換して生成する。
   - Claude Code / Cursor: YAML frontmatter（`name`, `description`, `tools`, `disallowedTools`, `model`, `memory`）+ Markdown body
   - Codex: TOML（`description`, `developer_instructions`, `model`, `sandbox_mode`, `approval_policy`）。body の内容は `developer_instructions` に集約する。
7. **Model Selection Policy (必須)**:
   - `model` は固定値を前提にせず、実装時点で公式ドキュメントの最新推奨を確認して選定する。
   - 公式ドキュメントの古いサンプル値を流用しない。選定理由と確認日を設計書に明記する。

</non*negotiables_2026*黄金律>

<language_policy>

- frontmatter/固有名詞/コマンドなど、英語必須箇所は保持する。
- それ以外の設計本文は自然な日本語で書く。

</language_policy>

<output_sections>

- 全生成パスリスト（必須・任意を明示）
- 生成対象パスと非生成パスの明示
- SKILL.md と Sub-agent.md の高解像度雛形
- 権限分離を適用したサブエージェント体系
- **非生成パス宣言**（今回は `.windsurf/rules/*` を生成しないこと）

</output_sections>
