---
name: content-scaffold
description: Use when new repository documents, skills, or agent files must be scaffolded with required sections and validation steps; When NOT to use: when the task is a minor edit to existing files without scaffolding; Trigger Keywords: [新規ファイル, scaffold, テンプレート, 雛形, 初期化].
---

# content-scaffold

## When to use

- `.claude/skills/skill-discoverer/SKILL.md` のような新規 SKILL.md を規約準拠で追加するとき。
- `.claude/agents/*.md` と `.cursor/agents/*.md` を同じ設計で新規作成するとき。
- `.codex/agents/*.toml` を Markdown agent から変換して新規作成するとき。

## When NOT to use

- 既存ファイルへ 1〜2 行追記するだけで済むとき。
- 配置先や命名が未確定で雛形の責務が定義できないとき。
- 実体パス確認なしに大量生成を行うとき。

## Trigger Keywords

- scaffold
- 新規ファイル
- テンプレート
- 雛形
- 初期化

## Procedure

1. `find .claude/skills .claude/agents .cursor/agents .codex/agents -maxdepth 2 -type f` で既存実体を確認する。完了条件: 重複名がない。
2. 生成対象のファイル種別を決め、必須セクション（Skill:8 / Agent:4）を定義する。完了条件: セクション仕様が確定。
3. 実在コマンド（`npm run agent:check`, `npm run format:check` など）を組み込んだ本文を作成する。完了条件: 架空コマンドがない。
4. 生成後に `npm run agent:check` を実行して整合性を確認する。完了条件: exit 0。
5. 生成ファイル一覧と検証結果を報告する。完了条件: すべての生成物に結果が付く。

## Output Contract

| 項目 | 形式 |
| --- | --- |
| Generated Files | `- path` 箇条書き |
| Applied Template | Skill / Agent / TOML の別 |
| Validation | `npm run agent:check: PASS/FAIL` |
| Follow-up | 必要な追補タスク |

### NG例

❌ 仮置き文字列や未確定メモを残して生成する（未完成物の混入）。

❌ 既存と同名パスへ意図不明の上書きを行う（衝突）。

❌ 検証を省略して生成完了とする（品質保証不足）。

## Examples

### Example 1

Input: `.claude/skills/skill-discoverer/SKILL.md` を新規追加したい。
Output: 8セクション実装済み SKILL.md と `npm run agent:check` 結果。

### Example 2

Input: `.claude/agents/repo-scaffolder.md` と `.cursor/agents/repo-scaffolder.md` を同仕様で再生成したい。
Output: 4セクション統一済み 2 ファイルと差分一覧。

### Example 3

Input: `.codex/agents/doc-validator.toml` を Markdown agent 仕様から再構成したい。
Output: `description` と `developer_instructions` を反映した TOML と検証結果。
