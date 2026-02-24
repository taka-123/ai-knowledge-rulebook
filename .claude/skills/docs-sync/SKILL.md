---
name: docs-sync
description: Use when README or operational documents must be synchronized with current repository structure and executable commands; When NOT to use: when changes are isolated and do not affect documented facts; Trigger Keywords: [README, directorystructure, technologystack, 同期, 実態反映].
---

# docs-sync

## When to use

- `.claude/skills/README.md` のスキル一覧が `.claude/skills/*/SKILL.md` 実体とずれたとき。
- `.work/AI_SCAN.md` や `.work/AI_BLUEPRINT.md` のコマンド記述を実態へ合わせるとき。
- `package.json` scripts 更新後にドキュメントの手順を同期するとき。

## When NOT to use

- 実装差分が文書に影響しない軽微な修正だけのとき。
- 仕様が未確定で、文書を確定更新できないとき。
- 外部情報の真偽確認が主目的で、文書同期ではないとき。

## Trigger Keywords

- README
- 同期
- 実態反映
- コマンド更新
- docs-sync

## Procedure

1. `git diff --name-only` で変更ファイルを抽出し、文書更新対象を決める。完了条件: 対象ファイルが確定。
2. `cat package.json` と `find .claude/skills -mindepth 2 -maxdepth 2 -name SKILL.md` で実体を確認する。完了条件: 参照元データ取得。
3. 文書内の古い記述を実体に合わせて最小差分で更新する。完了条件: 変更が対象節に限定。
4. `npx markdownlint-cli2 .claude/skills/README.md` を実行する。完了条件: 0 error。
5. 更新箇所と根拠コマンドをレポート化する。完了条件: 根拠付きで説明可能。

## Output Contract

| 項目            | 形式                             |
| --------------- | -------------------------------- |
| Updated Docs    | `- path` 箇条書き                |
| Source of Truth | 参照したコマンド/ファイル        |
| Diff Summary    | `1. before -> after`             |
| Verification    | `npx markdownlint-cli2 ...` 結果 |

### NG例

❌ 実体確認なしで記憶だけで書き換える（誤情報混入）。

❌ 関係ない章までまとめて書き直す（差分過大）。

❌ 根拠コマンドを記録しない（追跡不能）。

## Examples

### Example 1

Input: `.claude/skills/README.md` に未実在スキル名が残っている。
Output: 実体一覧に合わせた修正版 README と修正差分表。

### Example 2

Input: `package.json` の scripts 更新後に `.work/AI_BLUEPRINT.md` のコマンド記述を同期したい。
Output: scripts 節の更新と `cat package.json` 根拠を含む報告。

### Example 3

Input: `.claude/skills/skill-discoverer/SKILL.md` 追加後に関連ドキュメントへ反映したい。
Output: 反映済みファイル一覧と `npx markdownlint-cli2` PASS 記録。
