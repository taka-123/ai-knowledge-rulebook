---
name: content-scaffold
description: Use when new repository documents or rule files must be scaffolded from standardized structures with validation commands; When NOT to use: when existing files only need small edits without structural scaffolding; Trigger Keywords: [新規ファイル, scaffold, テンプレート, 雛形, 初期化].
---

# content-scaffold

## When to use

- 新しいスキル（SKILL.md）を規約準拠の構造で作成したい場合。
- `ai/` や `notes/` 配下に新しい JSON ファイルをスキーマ準拠で作成したい場合。

## When NOT to use

- 既存ファイルへ数行追記するだけで完了する場合。
- ファイル種別が不明で適用テンプレートを特定できない場合。

## Trigger Keywords

- 新規ファイル
- scaffold
- テンプレート
- 雛形
- 初期化

## Procedure

### SKILL.md を作成する場合

1. `ls .claude/skills/` または `ls ai/claude_code/global/skills/` で既存スキルを一覧して命名衝突がないか確認する。
2. 配置先ディレクトリを決定する（プロジェクト固有 → `.claude/skills/<name>/`、グローバル → `ai/claude_code/global/skills/<name>/`）。
3. 以下の必須セクションを含む `SKILL.md` を生成する：frontmatter（name・description）、When to use、When NOT to use、Trigger Keywords、Procedure、Output Contract、Examples（3件）。
4. `npm run agent:check` を実行してフロントマター・構造・ルーティング整合性を確認する。

### JSON ファイルを作成する場合

1. `schemas/` 配下の該当スキーマ（`ai_profile.schema.json` または `notes.schema.json`）を読んで必須フィールドを把握する。
2. 既存の同種 JSON を 1 件読んで形式を確認する。
3. 必須フィールドを全て含む最小構成の JSON を生成する。
4. `npm run schema:check` を実行してゼロエラーを確認する。

## Output Contract

- 生成ファイルのパスを先頭に明示する（例: `.claude/skills/ci-runner/SKILL.md`）。
- 検証コマンドの実行結果（exit code）を必ず添える。
- 検証が通らない場合は完了扱いにしない。

### NG例

```
❌ frontmatter なしで SKILL.md を作成する（agent:check に失敗する）
❌ JSON の必須フィールドを省略する（schema:check に失敗する）
❌ 既存スキルと同名のディレクトリを作成する（ルーティング衝突）
❌ 検証コマンドを実行せずに完了報告する
```

## Examples

### Example 1

Input: プロジェクト用に `ci-runner` スキルを新規作成したい。
Output: `.claude/skills/ci-runner/SKILL.md` を標準テンプレートで生成し、`npm run agent:check` が exit 0 であることを確認して報告する。

### Example 2

Input: `ai/` 配下に新しい AI プロファイル JSON を追加したい。
Output: `schemas/ai_profile.schema.json` の必須フィールドを確認し、最小構成の JSON を生成後、`npm run schema:check` が exit 0 であることを確認する。

### Example 3

Input: グローバルスキルとして `deploy-guard` を追加したい。
Output: `ai/claude_code/global/skills/deploy-guard/SKILL.md` を標準テンプレートで生成し、`npm run agent:check` が exit 0 であることを確認する。
