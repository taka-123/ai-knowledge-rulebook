# Project Intelligence Guidelines

## 2026 Constitution (Canonical)

- Skill の正典は `.claude/skills/<name>/SKILL.md` に限定する。
- ルーティング変更時は `npm run agent:check` を実行して、Name/Description/Examples 制約と参照整合性を検証する。
- プロジェクト固有の Claude 規約は `.claude/CLAUDE.md` を一次参照とし、本ファイルは司令塔として境界と優先順位を定義する。

Note: 本ファイルはグローバル原則を継承し、プロジェクト固有の指示を優先します。

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

- コードレビュー: AGENTS.md `## コードレビュー` に準拠
- セキュリティ: パイプ・リダイレクトを用いた Deny 回避を厳禁。

</development_rules>

<agent_skill_policy>

## 委任ポリシー

各 agent/skill の description に発動条件と Trigger Keywords が定義されている。
CLAUDE.md にマッピングを複製せず、以下の原則のみ遵守する。

### 優先順位

1. 同名資産がグローバル（`~/.claude/`）とプロジェクト（`.claude/`）の両方に存在する場合、プロジェクト版が優先される。
2. 複数候補がマッチした場合: agents > skills の順で選択する。
3. 破壊的操作（`deploy`, `migrate`, `git push --force`）は承認必須。

### 品質ゲート

- 完了報告前に品質監査を実行せよ。
- コード編集後は `format-lint-audit` または `lint-fix` で整合性を確認せよ。

</agent_skill_policy>
