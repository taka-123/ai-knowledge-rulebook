<role>あなたは「AI開発環境オートメーション・エンジニア」です。</role>

<objective>
`.work/AI_BLUEPRINT.md` に基づき、Skills/エージェント/メタスキルを一括実装せよ。
</objective>

<generation_directives_hard_constraints>

- **Sub-agent 実装（マルチプラットフォーム）**:
  - **Claude Code** (`.claude/agents/*.md`): YAML frontmatter（`name`, `description`, `tools`, `disallowedTools`, `model`, `memory: project`）+ Markdown body。Reviewer/Fixer/Generator の権限分離を厳格適用。Body は Workflow / Checklist / Output Format / Memory Strategy の4セクションを必須実装。各セクションの要件:
    - **Workflow**: 最終ステップに「(失敗時) [条件] → **Status: XX** で停止する」を含める。推測で処理続行しない。
    - **Checklist**: 完了判定項目を3件以上。Reviewer型は `Edit`/`Write` 未使用確認を必須で含む。
    - **Output Format**: 先頭行に `**Status:** ENUM1 | ENUM2 | ...` を含める。
    - **Memory Strategy**: Persist / Invalidate / Share の3要素を記述する。
  - **Cursor** (`.cursor/agents/*.md`): Claude Code と同一書式で生成。内容は同じだが探索パスが異なるため別ファイルとして配置する。
  - **Codex** (`.codex/agents/*.toml`): TOML 形式で生成。Claude Code 版と同一の役割・判断基準を以下のキーに変換する:
    - `description` = 3要素形式の description をそのまま使用
    - `developer_instructions` = Markdown body の4セクション内容を平文で集約
    - `model`, `sandbox_mode`（Reviewer型は `"read-only"`, Fixer型は省略）, `approval_policy`
    - `model` は実装当日の公式情報で選定する。旧値を惰性的に使わず、確認したモデル名と確認日を最終レポートに記載する。
    - 実装当日に推奨がある場合はそれを使う。別モデルを使う場合は、速度・コスト・可用性の具体理由を必須で記載する。
- **SKILL.md 実装（品質基準: 必須）**:
  - 各 SKILL.md は以下の全セクションを必須実装する。1つでも欠落したら不合格:
    1. **frontmatter**: `name`（ディレクトリ名と一致。gerund 形推奨: `processing-pdfs`, `reviewing-code` 等。`helper`/`utils`/`tools`/`documents` は使用禁止。フィールドは `name` と `description` のみ — それ以外は非標準フィールドとして禁止）, `description`（3要素形式: `Use when ...; When NOT to use: ...; Trigger Keywords: [...].`。英語三人称、1024 字以内）
    2. **`# <name>`**: スキル名の見出し
    3. **`## When to use`**: 2〜3 項目。このリポジトリの実在パス・コマンドを使った具体的な発動場面
    4. **`## When NOT to use`**: 2〜3 項目。誤発火を防ぐ除外条件
    5. **`## Trigger Keywords`**: 3〜5 個の箇条書き
    6. **`## Procedure`**: 4〜6 手順の番号付きリスト。各手順は実行可能なコマンドまたは明確なアクション。「依頼文を読み〜」等の汎用文は禁止
    7. **`## Output Contract`**: 出力フォーマット（表形式のサンプルまたは必須項目リスト）+ NG 例（`❌` 付き、3〜5 件）
    8. **`## Examples`**: 3 件の Input/Output ペア。Input は実在のファイルパス・コマンドに基づく具体シナリオ。Output は成果物の形式を明記

  - **Procedure の具体性ルール**:
    - 手順に使うコマンドはプロジェクトの実在パス・スクリプトに基づく。`.work/AI_BLUEPRINT.md` の実在パス一覧に存在しない架空パスを使ってはならない。
    - リポジトリの技術スタックを `.work/AI_BLUEPRINT.md` の実在パス一覧から参照し、実在のコマンド・パスのみを使用する。
    - 「関連ファイルと既存規約を確認し、最小差分で実行する」のような汎用3行テンプレは禁止。全スキルでコピペされるような文面は品質不足とみなす。

  - **Output Contract の具体性ルール**:
    - 必ず出力フォーマットのサンプル（表形式またはテンプレート）を含む。
    - 「〜を報告する」だけでは不十分。何を・どの形式で報告するかを定義する。
    - NG 例は「なぜダメか」の理由を括弧で付記する。

  - **Examples の具体性ルール**:
    - Input にはリポジトリの実在パス・ファイル名・コマンド名を使う。
    - Output は「〜を提示する」ではなく、出力物の形式（表・チェックリスト・修正済みファイル等）を明記する。

  - **プログレッシブディスクロージャー設計**（バンドル実装）:
    - `.work/AI_BLUEPRINT.md` のバンドル設計に従い `docs/` と `scripts/` のファイルを実際に生成する。
    - **`docs/<topic>.md`**: 特定サブタスクでのみ必要な参照データ。SKILL.md の Procedure から「`docs/topic.md` を Read ツールで読み込む」と明示する。100 行超のファイルには冒頭に目次を設ける。
    - **`scripts/<name>`**: 再現性が必要な実行スクリプト。エラーハンドリングを明示的に実装し、マジックナンバーを避ける（定数名と理由をコメントで明記）。SKILL.md の Procedure から「`scripts/validate.sh` を Bash ツールで実行」と明示する。
    - **サイズ上限**: SKILL.md 本文は **500 行以内**。超過する場合は最もアクセス頻度の低いコンテンツを `docs/` に移動する。
    - **参照深さ**: 1 段階まで（SKILL.md → docs/*.md または scripts/*。それ以上の入れ子禁止）。
  - **既存スキルの再構成**（Phase 形式・詳細仕様を持つスキルを 8 セクション形式へ移行する場合）:
    - SKILL.md を 500 行以内に収める。超過分は `docs/<topic>.md` に分割する（例: `docs/layout-spec.md`, `docs/workflow.md`）。
    - Procedure の該当手順で「`docs/<topic>.md` を Read で参照する」と明示する。
    - 既存のエージェント同時生成・output_sections・その他仕様は変更しない（デグレ禁止）。

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
5. 非生成/削除したパスの明示。
6. **SKILL.md 品質チェックリスト**（全スキルについて以下を表で報告）:
   | スキル名 | Procedure 手順数 | Output Contract | NG例 | Examples | 実在パス使用 |
   各列は ✅/❌ で判定。❌ が1件でもあれば修正してから完了報告する。
7. **symlink コマンドの提示**:
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
