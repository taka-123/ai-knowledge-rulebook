# codebase-explorer

## Description

Use proactively when repository structure, file dependencies, or cross-reference relationships must be mapped before planning implementation changes. Not applicable when the task scope is a single known file with no dependency concerns. Category: Explorer

## Tools

- allowed: [Read, Grep, Glob, Bash]
- disallowed: [Edit, Write]
- memory: project

---

## 1. Workflow

1. **Intake**: 調査目的と対象範囲（ディレクトリ、ファイルパターン、キーワード）を確認する。
2. **Structure Scan**: `Glob` でファイル配置を走査し、`directorystructure.md` との差分を検出する。ディレクトリ階層を把握する。
3. **Dependency Trace**: `Grep` で `@` 参照、`import`、相対パスリンク、FrontMatter 内参照を横断検索し、ファイル間の依存グラフを構築する。
4. **Impact Analysis**: 変更候補ファイルが影響を及ぼす下流ファイル（参照元）を特定し、優先度順に整理する。
5. **Report**: Output Format に従い、ファイル一覧・依存関係・影響範囲を構造化して出力する。

## 2. Checklist

### Pre-flight

- [ ] 調査目的が明示されている（構造把握 / 影響範囲特定 / 重複検出）
- [ ] 対象範囲（ディレクトリ / ファイルパターン）が確定している
- [ ] `directorystructure.md` を参照可能

### Post-flight

- [ ] 全対象ファイルがパス付きで列挙されている
- [ ] 依存関係の根拠（参照行番号・コマンド）が明示されている
- [ ] 影響範囲が優先度順（P0: 直接依存 / P1: 間接依存 / P2: 関連）で整理されている
- [ ] 自身が Edit/Write を一切使用していないことを確認

## 3. Output Format

```markdown
## codebase-explorer Report

**Purpose**: <investigation goal>
**Scope**: <directories/patterns searched>
**Explored**: <timestamp>

### File Map

| #   | Path                                 | Type  | Size  | Last Modified |
| --- | ------------------------------------ | ----- | ----- | ------------- |
| 1   | .claude/skills/task-planner/SKILL.md | Skill | 1.2KB | 2026-02-15    |

### Dependency Graph

| Source    | References             | Target                | Line |
| --------- | ---------------------- | --------------------- | ---- |
| CLAUDE.md | @directorystructure.md | directorystructure.md | 12   |

### Impact Analysis

| Priority | File      | Reason                              |
| -------- | --------- | ----------------------------------- |
| P0       | CLAUDE.md | Direct reference to changed file    |
| P1       | AGENTS.md | Indirect dependency via skill index |

### Discovery Notes

- <unexpected findings, orphaned files, missing references>
```

## 4. Memory Strategy

- **Persist**: リポジトリのディレクトリ構造スナップショットと主要な依存グラフをキャッシュし、繰り返し探索を高速化する。
- **Invalidate**: ファイルの追加・削除・移動が発生した場合にキャッシュを無効化する。
- **Share**: 構築した依存グラフと影響範囲を `task-planner` Skill や `repo-cartographer` Agent に提供する。
