# Project Intelligence Guidelines

Note: 本ファイルはグローバル原則を継承し、プロジェクト固有の指示を優先します。

<project_context>

- Overview: @README.md
- Architecture: @directorystructure.md
- Tech Stack: @technologystack.md

</project_context>

<development_commands>

## フォーマット・検証

```bash
# 全ファイル整形（Prettier + Markdownlint + yamllint）
./format.sh fix

# 整形チェックのみ（CI と同じ）
./format.sh check
```

## npm scripts

```bash
# Lint チェック（整形確認のみ）
npm run lint

# 自動修正
npm run fix

# 個別実行
npm run lint:md        # Markdown Lint
npm run lint:yaml      # YAML Lint
npm run lint:json      # JSON Lint
npm run fix:md         # Markdown 自動修正
npm run fix:yaml       # YAML 自動整形
npm run fix:json       # JSON 自動整形

# JSON Schema 検証（AI プロファイル・ノート）
npm run schema:check
```

## 検証プロトコル

このプロジェクトには単体テストがないため、変更後は以下で検証せよ：

1. `./format.sh check` を実行し、全チェックがパスすることを確認
2. 変更したファイル形式に応じて `npm run lint:md` 等を個別実行
3. JSON 変更時は `npm run schema:check` でスキーマ適合性を確認

</development_commands>

<development_rules>

## 🤖 自律動作プロトコル（境界線の定義）

**1. 自律実行の境界 (Boundaries)**:

- **自律 OK (No Confirmation)**:
  - 単一ファイルの編集、新規ファイル生成、非破壊的な Read/Search/Task。
- **要確認 (Must Confirm)**:
  - 複数ファイルにまたがる破壊的な Edit、ファイル/ディレクトリの削除。
  - ただし、`git worktree` 等の隔離環境下での一括作業を命じられた場合は、計画提示後に一括承認を得れば、個別確認は不要とする。
- **`--dangerously-skip-permissions` 指定時の制約**:
  - 機密情報へのアクセスおよび破壊的操作（削除/force push）は引き続き禁止。

**2. 検証の義務化 (Verification First)**:
報告前に必ず「動くことの証明」を行え。

- 既存テストがある場合は必ず実行し、結果を報告に含めること。
- テストがない場合、CLI での直接実行（ワンライナー）または一時的な検証スクリプトを作成して確認せよ。
- **重要**: 一時ファイルは検証後に必ず削除し、リポジトリを汚さないこと。

**3. 完了の定義 (Definition of Done)**:

- [ ] 意図した変更が反映されている
- [ ] 既存のテストがパスしている（または自律検証済み）
- [ ] 関連ドキュメント（README等）が更新されている
- [ ] 変更内容をユーザーに報告し、確認を求めている

---

## 固有規約

- コードレビュー: @AGENTS.md `## コードレビュー` に準拠
- セキュリティ: パイプ・リダイレクトを用いた Deny 回避を厳禁。

</development_rules>

<agent_routing>

## 🤖 エージェント・スキルルーター（司令塔）

### Always Scan First

タスク実行の前に、以下2つのディレクトリを確認し、最適な専門家を召喚する：

- `~/.claude/agents/` · `~/.claude/skills/`（グローバル資産）
- `./.claude/agents/` · `./.claude/skills/`（プロジェクト固有資産）

召喚の根拠は下記 **Hierarchy of Intelligence** に従う。

---

### Hierarchy of Intelligence（委任の基準）

| タスク類型                                            | 委任先                                        | 理由                                   |
| ----------------------------------------------------- | --------------------------------------------- | -------------------------------------- |
| 技術仕様の調査・接地                                  | グローバル `tech-researcher`                  | 一次情報への接地は汎用規律             |
| コードベース全体の構造探索                            | グローバル `codebase-explorer`                | 大規模探索は汎用規律                   |
| 実装後の品質・完遂監査                                | グローバル `task-reviewer`                    | 検証義務は汎用規律                     |
| Lint・フォーマッター自動修正                          | グローバル `lint-fix` スキル                  | ツール検知は汎用規律                   |
| **ドキュメント品質検証**（FrontMatter・リンク整合性） | プロジェクト `doc-validator`                  | リポジトリ固有の検証ルールに基づく     |
| **調査結果のリポジトリへの書き込み**                  | プロジェクト `content-writer`                 | 書き込み規約はリポジトリ固有           |
| **新規ファイルのスキャフォルド生成**                  | プロジェクト `repo-scaffolder`                | テンプレートはリポジトリ固有           |
| **リポジトリ構造・参照関係の地図化**                  | プロジェクト `repo-cartographer`              | ドキュメント構造の把握はリポジトリ固有 |
| **外部仕様・時事情報の書き込み前事実確認**            | プロジェクト `external-fact-guardian`         | 一次情報ゲートはリポジトリ固有         |
| **記述規約の強制チェック**                            | プロジェクト `documentation-standards` スキル | 規約はリポジトリ固有                   |
| **技術調査の書き込み前ゲーティング**                  | プロジェクト `research-protocol` スキル       | 出典・不確実性注記はリポジトリ固有規約 |
| **新規ファイル時のテンプレート適用**                  | プロジェクト `content-scaffold` スキル        | テンプレートはリポジトリ固有           |
| **JSON スキーマ適合検証**                             | プロジェクト `schema-guard` スキル            | スキーマ定義はリポジトリ固有           |
| **Format/Lint チェック実行**                          | プロジェクト `format-lint-audit` スキル       | 検証コマンドはリポジトリ固有           |
| **主要ドキュメントの実態同期**                        | プロジェクト `docs-sync` スキル               | 対象ドキュメントはリポジトリ固有       |
| **コンテキスト圧縮マップ生成**                        | プロジェクト `context-compress-map` スキル    | 情報密度維持のためのプロジェクト規律   |

---

### プロジェクト資産一覧

**Agents** (`.claude/agents/`):

- `doc-validator` — ドキュメント品質検証（読み取り専用）
- `content-writer` — 調査結果の規約準拠書き込み
- `repo-scaffolder` — 新規ファイルのテンプレート適用・生成（Claude Code のみ）
- `repo-cartographer` — リポジトリ構造・参照関係の地図化
- `external-fact-guardian` — 外部仕様の書き込み前事実確認

**Skills** (`.claude/skills/`):

- `documentation-standards` — 記述規約強制チェック
- `research-protocol` — 技術調査の出典・不確実性プロトコル強制
- `content-scaffold` — 新規ファイルテンプレート適用・バリデーション
- `schema-guard` — JSON スキーマ適合検証
- `format-lint-audit` — Format/Lint チェック実行と結果報告
- `docs-sync` — 主要ドキュメント（README・directorystructure・technologystack）の実態同期
- `context-compress-map` — コンテキスト圧縮マップ生成

</agent_routing>

<project_intelligence_router_minimal>

## Minimal Router Addendum (Cross-Tool Name Alignment)

- 依頼文に以下の語が含まれる場合、同名の専門家へ優先委任する:
  - `最新仕様` `release` `互換性` `API変更` -> `tech-researcher`
  - `調査` `影響範囲` `参照` `構造` -> `codebase-explorer`
  - `レビュー` `回帰` `品質` `PR` -> `task-reviewer`
  - `lint` `format` `schema` `CI` -> `lint-fix`
  - `debug` `不具合` `再現` `エラー` -> `debug-strategist`
  - `計画` `分解` `見積り` -> `task-planner`
  - `UI` `CSS` `レイアウト` -> `ui-standardizer`
  - `commit` `branch` `PR作成` -> `git-helper`
  - `agent` `skill` `rule` `workflow` `テンプレート` -> `agent-factory`

- 破壊的操作（`deploy` `migrate` `terraform apply` `git push --force` など）は必ず事前承認を取る。
- 既存の同名グローバル資産がある場合は再定義せず、必要時のみ薄いプロキシを使う。

</project_intelligence_router_minimal>
