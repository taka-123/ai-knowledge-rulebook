---
name: agent-factory
description: |
  Use when: 新しい Subagent または Skill の追加を明示的に依頼された場合。既存スキルの責務分離・再設計を行う場合。
  When NOT to use: 実装やドキュメント更新だけで解決できる場合。既存スキルに 1〜2 行追記するだけで十分な場合。
  Trigger Keywords: [新しいスキル, 新しいエージェント, skill 作成, agent 作成, /agent-factory]
---

# agent-factory

Subagent または Skill の設計・生成を行う。明示的な依頼がある場合のみ起動する。

## When to use

- 新しい Subagent または Skill の追加を明示的に依頼された場合。
- 既存スキルの責務分離・再設計を行う場合。

## When NOT to use

- 実装やドキュメント更新だけで解決できる場合。
- 既存スキルに 1〜2 行追記するだけで十分な場合。

## Trigger Keywords

- 新しいスキル / 新しいエージェント
- skill 作成 / agent 作成
- /agent-factory

## Procedure

1. `docs/design-guide.md` を Read で参照し、Subagent vs Skill の判定・命名規則・description 形式・自由度・最小権限・保存先パスを確認する。
2. ユーザー依頼から対象種別（Skill / Subagent）を判定する。
3. 採用案 1 つ + 代替案 1 つを、frontmatter 付きで生成する。各案に発動条件・対象タスク・禁止事項を 1 行で付ける。
4. 生成プロンプトには一次情報への接地（URL + 取得日）と RFC 2119 準拠の精神を注入する。

## Output Contract

| 項目     | 形式                     |
| -------- | ------------------------ |
| 採用案   | frontmatter 付きの完成形 |
| 代替案   | 同上                     |
| 発動条件 | 各案に 1 行              |
| 禁止事項 | 各案に 1 行              |

### NG例

❌ 明示的依頼なしに自律的に起動する（誤発火）。

❌ 一人称・Use when なしの description を生成する（形式違反）。

❌ 仮置き文字列や TODO を残して生成する（未完成物の混入）。

## Examples

### Example 1

Input: 「コミットメッセージ生成用のスキルを作りたい」
Output: `organizing-commits` 相当の 8 セクション SKILL.md 案 2 つと、保存先パス。

### Example 2

Input: 「セキュリティ監査用の Subagent を追加したい」
Output: `security-reviewer` 相当の agent .md 案 2 つと、tools / model の推奨値。

### Example 3

Input: 「既存の lint-fix を責務分離して 2 つに分けたい」
Output: 分割後の 2 スキル案と、発動条件の棲み分け。
