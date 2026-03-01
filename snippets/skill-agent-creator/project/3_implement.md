<role>あなたは「AI開発環境オートメーション・エンジニア」です。</role>

<objective>
**主目的**: プロジェクト単位で最高に有益なエージェント・スキルを作ること。

`.work/AI_BLUEPRINT.md` に基づき、Skills/エージェント/メタスキルを一括実装せよ。
</objective>

<generation_directives_hard_constraints>

- **Sub-agent 実装（マルチプラットフォーム）**:
  - **Claude Code** (`.claude/agents/*.md`): YAML frontmatter（`name`, `description`, `color`, `tools`, `disallowedTools`, `model`, `memory: project`）+ Markdown body。`color` は `Red | Blue | Green | Yellow | Purple | Orange | Pink | Cyan` から選び、各サブエージェントの役割イメージに一致させる。Reviewer/Fixer/Generator の権限分離を厳格適用。`model:` フィールドはバージョン固定せず**公式エイリアス**を使用する（通常の実装・レビュー系: `sonnet`、複雑な設計・推論系: `opus`、省略時は親会話を継承: `inherit`）。Body は Workflow / Checklist / Output Format / Memory Strategy の4セクションを必須実装。各セクションの要件:
    - **Workflow**: 最終ステップに「(失敗時) [条件] → **Status: XX** で停止する」を含める。推測で処理続行しない。
    - **Checklist**: 完了判定項目を3件以上。Reviewer型は `Edit`/`Write` 未使用確認を必須で含む。
    - **Output Format**: 先頭行に `**Status:** ENUM1 | ENUM2 | ...` を含める。
    - **Memory Strategy**: Persist / Invalidate / Share の3要素を記述する。
  - **Cursor** (`.cursor/agents/*.md`): CC と**同一の Body**（Workflow / Checklist / Output Format / Memory Strategy）を使用するが、**frontmatter は Cursor 固有の形式**で生成する。
    - 必須フィールド: `name`, `description`, `model: inherit`
    - Reviewer型のみ `readonly: true` を追加する（Fixer/Generator型は省略）
    - `model: fast` 等の環境依存な固定モデル名は禁止。未サポートモデルエラーを避けるため `inherit` を標準にする
    - `color` / `tools` / `disallowedTools` / `memory` は **Cursor 未対応のため記載しない**
    - 生成手順: 対応する CC エージェントを Read → frontmatter を Cursor 仕様に変換 → Body はそのままコピー → `.cursor/agents/{name}.md` に Write
    - 既存 `.cursor/agents/*.md` に旧式フィールド（`color` / `tools` / `disallowedTools` / `memory`）がある場合は、同時に削除して正規化する
  - **Codex** (`.codex/agents/*.toml`): TOML 形式で生成。Claude Code 版と同一の役割・判断基準を以下のキーに変換する:
    - `description` = 3要素形式の description をそのまま使用
    - `developer_instructions` = Markdown body の4セクション内容を平文で集約
    - `model`, `sandbox_mode`（Reviewer型は `"read-only"`, Fixer型は省略）, `approval_policy`
    - **`model` の決定方法**: WebSearch で「Codex CLI current recommended model」を検索し、現時点の推奨モデル名を取得する。検索結果が不明瞭な場合はプロジェクト内の既存 `.codex/agents/*.toml` を Read して使用中のモデル名を踏襲する。`gpt-4o` 等の明らかに古い汎用モデルは選ばない（Codex 専用モデルが存在する場合はそちらを優先）。
  - **Codex 配線（必須）**:
    - `.codex/agents/*.toml` の生成後に、`/.codex/config.toml` の `[agents]` を更新し、実行に使う role を `config_file = "./.codex/agents/<name>.toml"` で配線する。
    - レビュー主体プロジェクトでは、`review_model` と `developer_instructions` に自然文レビュー依頼ルーティングを明記する。
    - 必要時は `[features] multi_agent = true` を有効化し、preset 側にも同じ方針を反映する。
    - role 枠より agent が多い場合は、`/.codex/config.preset.*.toml` を用途別に生成し、`/.codex/use-preset.sh` を作成または更新する。
    - 参照先不在（dangling）と未配線（orphan）が残る場合は完了報告せず、修正または理由明記のうえ **Status: BLOCKED** とする。
  - **自然文レビュー依頼ルーティング資産（必要時）**:
    - CC: `CLAUDE.local.md`, `.claude/commands/*.md`
    - Cursor: `.cursor/rules/*.mdc`, `.cursor/commands/*.md`（Bugbot 運用時のみ `BUGBOT.md`）
    - Codex: `config.toml` / `config.preset.*.toml` / `.codex/REVIEW_PLAYBOOK.md`
    - reviewer 系を生成する場合は、上記のうち必要資産を同一ターンで更新する（agent ファイル単体更新で終わらせない）。
    - ルーティングは description-first を原則とし、静的マッピングは例外ケース（曖昧衝突回避）に限定する。
  - **サブエージェント失敗時フォールバック（必須）**:
    - reviewer 系の一部が失敗・タイムアウトしても、親エージェントが残り観点を実施してレビューを完遂する手順を rules/commands/instructions に明記する。
    - 最終レポートで「失敗したサブエージェント」と「親が代替した観点」を必ず示す。
- **SKILL.md 実装（品質基準: 必須）**:
  - 各 SKILL.md は以下の全セクションを必須実装する。1つでも欠落したら不合格:
    1. **frontmatter**: `name`（ディレクトリ名と一致。gerund 形推奨: `processing-pdfs`, `reviewing-code` 等。`helper`/`utils`/`tools`/`documents` は使用禁止。フィールドは `name` と `description` のみ — それ以外は非標準フィールドとして禁止）, `description`（3要素形式: `Use when ...; When NOT to use: ...; Trigger Keywords: [...].`。英語三人称、1024 字以内）
       - **description `[condition]` の実装ルール（必須）**: `Use when` の直後に続く `[condition]` は、具体的なファイルパス・ディレクトリ名・タスク種別を含める。抽象的な技術名（フレームワーク名・言語名のみ）は不十分。
         - 実装・修正・自動検証系: 冒頭を `Use proactively when editing any file under [具体パス]/...` の形式にする
         - 明示依頼待ち系: `Use when the user explicitly asks for [...]` の形式にする
         - ❌ `Use when editing framework code` → ✅ `Use proactively when editing any file under {target_repo}/src/ or {target_repo}/tests/`
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
    - `.work/AI_BLUEPRINT.md` のバンドル設計に従う。設計でバンドルが必要と判定されたスキルのみ、**スキル内**の `docs/` と `scripts/` を生成する。SKILL.md のみで事足りるスキルは作成しない。配置先は `.claude/skills/<name>/docs/` および `.claude/skills/<name>/scripts/`。
    - **`docs/<topic>.md`**: スキルフォルダ内に配置。特定サブタスクでのみ必要な参照データ。SKILL.md の Procedure から「`.claude/skills/<name>/docs/topic.md` を Read ツールで読み込む」と明示する。100 行超のファイルには冒頭に目次を設ける。
    - **`scripts/<name>`**: スキルフォルダ内に配置。再現性が必要な実行スクリプト。エラーハンドリングを明示的に実装し、マジックナンバーを避ける（定数名と理由をコメントで明記）。SKILL.md の Procedure から「`.claude/skills/<name>/scripts/validate.sh` を Bash ツールで実行」と明示する。
    - **サイズ上限**: SKILL.md 本文は **500 行以内**。超過する場合は最もアクセス頻度の低いコンテンツをスキル内 `docs/` に移動する。
    - **参照深さ**: 1 段階まで（SKILL.md → docs/_.md または scripts/_。それ以上の入れ子禁止）。
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
- **リネーム連鎖更新（必須）**:
  - エージェント/スキル名を変更した場合、`.claude/` `.cursor/` `.codex/` の対応ファイル、ならびに関連文書内参照（例: Memory Strategy の Share 先、実装結果セクション）を同一ターンで更新する。
  - 1箇所でも旧名が残る場合は完了報告せず、修正を完了させる。
- **禁止コマンドの扱い（必須）**:
  - `CLAUDE.md` / `AGENTS.md` に「AI実行禁止」「ユーザー手動実行」と定義されたコマンドは AI が実行しない。
  - agent/skill の Workflow/Procedure には「ユーザーへ実行依頼する手順」を明示し、代替の自動実行手順を作らない。
- **コマンド互換性（必須）**:
  - Workflow / Procedure / rules / commands に `git --no-stat` を含めない。
  - 差分取得は `--stat`（要約）と `-p`（本文）を使い分ける。
  - 互換性が不明なオプションを使う場合は、代替コマンドとフォールバックを併記する。

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
   - 任意の `.claude/agents/*.md` から frontmatter 抜粋を表示し、`color` が許可値であることを示す。
3. メタスキル `skill-discoverer` の SKILL.md 全文表示。
4. Codex TOML エージェントの1ファイル全文表示（変換が正しいことの証明）。WebSearch で選定したモデル名と確認日も併記する。
5. 非生成/削除したパスの明示。
6. **SKILL.md 品質チェックリスト**（全スキルについて以下を表で報告）:
   | スキル名 | Procedure 手順数 | Output Contract | NG例 | Examples | 実在パス使用 |
   各列は ✅/❌ で判定。❌ が1件でもあれば修正してから完了報告する。
7. **クロスプラットフォーム整合チェック**（全エージェントについて最低1回は検証結果を報告）:
   - `.claude/` `.cursor/` `.codex/` で name/description が一致していること
   - Cursor frontmatter に非対応フィールド（`color`, `tools`, `disallowedTools`, `memory`）が残っていないこと
   - 改名実施時に旧名参照が残っていないこと
8. **symlink コマンドの提示**:
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
9. **Codex 配線検証（必須）**:
   - `/.codex/config.toml` の `role -> config_file` 対応表を提示する。
   - `/.codex/agents/*.toml` のうち、`config.toml` または `config.preset.*.toml` のいずれにも載っていない未配線ファイル一覧を提示する（理想は空）。
   - `config_file` が実在しない参照一覧（dangling）を提示する（理想は空）。
10. **レビュー発動・互換性検証（必須）**:
   - 通常レビュー依頼文（例: `この修正でOKかレビューしてください`）で reviewer 系へルーティングされる設計根拠を提示する。
   - `--no-stat` が生成ファイル群に含まれないことを検索結果で提示する。
11. **マッピング依存・速度検証（必須）**:
   - 静的マッピングの件数と、description-first で成立する経路を提示する（LOW 依存を目標）。
   - 可能な範囲で旧運用と新運用の所要時間・指摘件数を比較し、速度/精度の差分を示す。
12. **モデル適合検証（必須）**:
   - Cursor agent で `model: fast` 等の固定名が残っていないことを検索結果で提示する。
   - モデル未サポートエラー発生時のフォールバック（`model: inherit` へ修正し再実行）を実施記録として残す。

</final_report_requirements>
