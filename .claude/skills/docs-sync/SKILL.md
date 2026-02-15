---
name: docs-sync
description: Use when README, directory structure, and technology stack documents must be synchronized with current repository reality; When NOT to use: isolated feature work without documentation impact; Trigger Keywords: README, directorystructure, technologystack, 同期, 実態反映.
---

# docs-sync

## When to use

- 主要ドキュメントを実態と同期したい。
- 構成変更に伴って説明を更新する。

## When NOT to use

- ドキュメント非対象の作業。
- 実態差分が無い場合。

## Trigger Keywords

- README
- directorystructure
- technologystack
- 同期
- 実態反映

## Examples

### Example 1

Input: 新しい rules ディレクトリ追加をドキュメントへ反映して。
Output: `directorystructure.md` の該当ツリーを更新し、README の参照を整合させる。

### Example 2

Input: 実行コマンドが変わったので説明を同期して。
Output: `package.json` の scripts と一致するように運用手順を更新する。

### Example 3

Input: 技術スタックのバージョン表記を実態に合わせたい。
Output: `technologystack.md` を現行 `package.json`/実行環境に合わせて修正する。

---

## 1. Workflow

1. **Intake**: 同期対象ドキュメント（`README.md`、`directorystructure.md`、`technologystack.md`）と変更トリガー（ファイル追加/削除、コマンド変更、バージョン更新）を確認する。
2. **Reality Scan**: Glob でリポジトリの実ディレクトリ構造を取得し、`package.json` の scripts とバージョンを読み取る。
3. **Diff Detection**: 実態とドキュメント記述の差分を検出する。差分がない場合は「同期済み」を報告して終了する。
4. **Apply Sync**: 差分箇所のみ Edit で修正する。既存の記述スタイル（インデント、ツリー表記、表形式）を踏襲する。
5. **Verify**: `npm run lint:md` で構文チェックし、内部参照（`@` 参照）の実在性を Glob で確認する。

## 2. Checklist

### Pre-flight

- [ ] 同期対象ドキュメントを特定済み
- [ ] 変更トリガー（何が変わったか）を把握済み
- [ ] `package.json` の現行 scripts を確認済み

### Post-flight

- [ ] ドキュメントの記述が実態と一致している
- [ ] 既存スタイル（ツリー表記、表形式）を維持している
- [ ] `npm run lint:md` が exit 0
- [ ] 全 `@` 参照が実在ファイルを指している

## 3. Output Format

```markdown
## docs-sync Report

**Action**: SYNC | NO_CHANGE
**Targets**: README.md, directorystructure.md, technologystack.md
**Trigger**: <変更内容の要約>

### Diffs Applied

| #   | Document              | Section         | Change                      | Lines |
| --- | --------------------- | --------------- | --------------------------- | ----- |
| 1   | directorystructure.md | .claude/skills/ | Added context-compress-map/ | 45-46 |

### Verification

| Check         | Command           | Result             |
| ------------- | ----------------- | ------------------ |
| Markdown Lint | `npm run lint:md` | PASS               |
| References    | Glob check        | 8 checked, 8 valid |

### Remaining Gaps

- <ドキュメント側で未反映の実態差分があれば記載>
```

## 4. Memory Strategy

- **Persist**: 3 つの主要ドキュメントの構造スナップショット（セクション見出し、ツリー記法パターン）をキャッシュし、差分検出を高速化する。
- **Invalidate**: 対象ドキュメント自体が編集された場合、またはリポジトリ構造（ファイル追加/削除）が変更された場合にキャッシュを無効化する。
- **Share**: 同期完了後のドキュメントパスを `documentation-standards` Skill に提供し、品質検証の入力とする。
