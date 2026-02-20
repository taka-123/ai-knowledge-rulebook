<role>あなたは「AI開発環境オートメーション・エンジニア」です。</role>

<objective>
`.work/AI_BLUEPRINT.md` に基づき、Skills/エージェント/メタスキルを一括実装せよ。
</objective>

<generation_directives_hard_constraints>

- **Sub-agent 実装（マルチプラットフォーム）**:
  - **Claude Code** (`.claude/agents/*.md`): YAML frontmatter（`name`, `description`, `tools`, `disallowedTools`, `model`, `memory: project`）+ Markdown body。Reviewer/Fixer/Generator の権限分離を厳格適用。Body は Workflow / Checklist / Output Format / Memory Strategy の4セクションを必須実装。
  - **Cursor** (`.cursor/agents/*.md`): Claude Code と同一書式で生成。内容は同じだが探索パスが異なるため別ファイルとして配置する。
  - **Codex** (`.codex/agents/*.toml`): TOML 形式で生成。Claude Code 版と同一の役割・判断基準を以下のキーに変換する:
    - `description` = 3要素形式の description をそのまま使用
    - `developer_instructions` = Markdown body の4セクション内容を平文で集約
    - `model`, `sandbox_mode`（Reviewer型は `"read-only"`, Fixer型は省略）, `approval_policy`
    - `model` は実装当日の公式情報で選定する。旧値を惰性的に使わず、確認したモデル名と確認日を最終レポートに記載する。
    - 実装当日に推奨がある場合はそれを使う。別モデルを使う場合は、速度・コスト・可用性の具体理由を必須で記載する。
- **SKILL.md 実装**:
  - 各 skill に 3〜5 個の具体的 Examples を必須実装。
  - プロジェクト実コード（`src/main`, `src/worker`, `src/common`, `build.sh`）に基づく具体文脈を必須反映。
- **メタスキル `skill-discoverer` の生成（必須）**:
  - `.claude/skills/skill-discoverer/SKILL.md` を生成する。
  - 目的: `.claude/agents/` と `.claude/skills/` を動的にスキャンし、利用可能なスキル/エージェントの一覧と各 description を提示する。
  - description の3要素形式: `Use when the user asks what skills or agents are available, or when uncertain which specialist to delegate to; When NOT to use: when the target skill is already known; Trigger Keywords: スキル一覧, 何ができる, available skills, help, 委任先.`
  - Body は以下のプロシージャを含む: (1) `.claude/agents/*.md` と `.claude/skills/*/SKILL.md` の frontmatter を全件読み取り (2) name / description を一覧表示 (3) ユーザーの目的に最適な候補を推薦。
- **`.claude/rules` の扱い**:
  - `CLAUDE.md` 分割が必要な場合のみ任意作成。
  - config別用途の別系統ファイルとしては扱わない。
- **サボり防止**:
  - プレースホルダ禁止（`TODO`, `TBD`, `<...>` などを残さない）。
  - 「提案のみ」で止まらず、実ファイルへ反映する。

</generation_directives_hard_constraints>

<language_policy>

- 必須英語は保持:
  - frontmatter の `description: Use when [condition]; When NOT to use: [exclusion]; Trigger Keywords: [kw1, kw2, ...].`
  - ツール名、コマンド名、固有名詞
- 上記以外の本文は自然な日本語を優先する。

</language_policy>

<final_report_requirements>

1. 生成・修正パスの tree。
2. 制約遵守の証明:
   - 少なくとも1つのエージェントの Body 全文（4セクション充足）を表示。
   - 任意の SKILL.md から Description 抜粋を表示（3要素形式 / XMLなし）。
3. メタスキル `skill-discoverer` の SKILL.md 全文表示。
4. Codex TOML エージェントの1ファイル全文表示（変換が正しいことの証明）。
5. 非生成/削除したパスの明示（`.windsurf/rules/*` など）。
6. **symlink コマンドの提示**:
   - 次のコマンドをそのまま最終レポートに出力する:
     ```bash
     ln -snf ../.claude/skills .agents/skills && \
     ln -snf ../.claude/skills .cursor/skills && \
     ln -snf ../.claude/skills .windsurf/skills && \
     ln -snf ../.claude/skills .agent/skills
     ```
   - `.agents` / `.cursor` / `.windsurf` / `.agent` が存在しない可能性がある場合のみ、事前に次を併記する:
     ```bash
     mkdir -p .agents .cursor .windsurf .agent
     ```

</final_report_requirements>
