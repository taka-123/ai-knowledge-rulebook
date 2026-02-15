---
name: context-compress-map
description: Use when large repository context must be compressed into a navigable map of files, decisions, and next actions without losing traceability; When NOT to use: short single-file tasks with obvious scope; Trigger Keywords: 要約, コンテキスト, map, 全体像, 影響範囲.
---

# context-compress-map

## When to use

- 大量情報を圧縮して共有したい。
- 影響範囲を短時間で把握したい。

## When NOT to use

- スコープが明白な単一ファイル作業。
- 要約不要な短い回答。

## Trigger Keywords

- 要約
- コンテキスト
- map
- 全体像
- 影響範囲

## Examples

### Example 1

Input: このリポジトリの AI ルール構成を3分で理解できる形にして。
Output: ルール階層、Skill配置、検証コマンドを図式化した要約を作成する。

### Example 2

Input: 変更候補ファイルを優先度付きで整理して。
Output: P0/P1/P2 の優先度でファイル一覧と理由を提示する。

### Example 3

Input: 次の実装フェーズへ引き継ぐための圧縮メモを作って。
Output: 完了項目、未完項目、再開コマンドを含む再開マップを生成する。

---

## 1. Workflow

1. **Intake**: 圧縮対象（リポジトリ全体 / 特定ディレクトリ / 作業セッション）とユースケース（構造把握 / 引き継ぎ / 影響分析）を確認する。
2. **Information Gathering**: Glob でファイル一覧を取得し、Grep で主要な参照関係を抽出する。変更履歴がある場合は `git log` で直近の変更を収集する。
3. **Prioritization**: 情報を P0（必須理解）/ P1（推奨理解）/ P2（参考）に分類する。
4. **Compression**: 各カテゴリの情報を、ファイルパス・役割・依存関係の 3 要素に圧縮する。冗長な説明を排除し、1 行 1 情報を原則とする。
5. **Map Output**: Output Format に従い、ナビゲーション可能なマップを出力する。

## 2. Checklist

### Pre-flight

- [ ] 圧縮対象の範囲が確定している
- [ ] ユースケース（構造把握 / 引き継ぎ / 影響分析）が明示されている
- [ ] 対象ディレクトリのファイル一覧を取得済み

### Post-flight

- [ ] P0 情報が漏れなく含まれている
- [ ] 各エントリにファイルパス・役割・依存関係が記載されている
- [ ] 冗長な説明が排除されている（1 行 1 情報）
- [ ] 再開コマンド（該当時）が具体的に記載されている

## 3. Output Format

```markdown
## context-compress-map

**Scope**: <対象範囲>
**Use Case**: Structure Overview | Handoff | Impact Analysis
**Entries**: <N> files mapped

### P0 — Must Understand

| #   | Path      | Role                 | Dependencies                 |
| --- | --------- | -------------------- | ---------------------------- |
| 1   | CLAUDE.md | Router / entry point | AGENTS.md, .claude/CLAUDE.md |

### P1 — Should Understand

| #   | Path                                 | Role           | Dependencies              |
| --- | ------------------------------------ | -------------- | ------------------------- |
| 1   | .claude/skills/task-planner/SKILL.md | Planning skill | Referenced by all routers |

### P2 — Reference

| #   | Path                           | Role                   |
| --- | ------------------------------ | ---------------------- |
| 1   | schemas/ai_profile.schema.json | JSON validation schema |

### Action Items (if handoff)

- [ ] `git checkout <branch> && npm install`
- [ ] 未完了: <task description>
- [ ] 次のステップ: <action>
```

## 4. Memory Strategy

- **Persist**: 直前のマップ生成結果（ファイル分類、優先度付け）をキャッシュし、差分更新を可能にする。
- **Invalidate**: リポジトリ構造の変更（ファイル追加/削除/移動）が発生した場合にキャッシュを無効化する。
- **Share**: 生成したマップを `task-planner` に提供し、計画策定時のスコープ把握に活用する。引き継ぎマップを次のセッションのコンテキストとして提供する。
