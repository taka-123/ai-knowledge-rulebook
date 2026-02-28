---
name: documentation-standards
description: Use proactively when editing Markdown files under .work/, .claude/, or .cursor/ to enforce document style, link format, and heading consistency; When NOT to use: when the task is code-only and produces no documentation output; Trigger Keywords: [ドキュメント, 記述規約, 文章品質, 参照, 構成].
---

# documentation-standards

## When to use

- `.work/AI_SCAN.md` や `.work/AI_BLUEPRINT.md` の最終報告を規約準拠で整えるとき。
- `.claude/skills/*/SKILL.md` の表現を統一し、参照記法を正規化するとき。
- `markdownlint` ルールに合わせて文章構造を見直すとき。

## When NOT to use

- コード実装のみで文書生成が発生しないとき。
- 外部仕様調査が主目的で、文書校正を行わないとき。
- ユーザーが厳密な原文保持を要求し、文体変更を許可していないとき。

## Trigger Keywords

- ドキュメント
- 記述規約
- 文章品質
- 参照
- 構成

## Procedure

1. 対象文書を `cat .work/AI_BLUEPRINT.md` などで確認し、見出し構造と参照書式を抽出する。完了条件: 違反候補を列挙。
2. ファイル参照を `` `path/to/file` `` 形式へ統一し、裸 URL を Markdown リンク化する。完了条件: 参照書式の不一致がない。
3. 箇条書き、表、コードブロックをルールに合わせて整形する。完了条件: 可読性と一貫性が向上。
4. `npx markdownlint-cli2 .work/AI_BLUEPRINT.md` を実行して違反を確認する。完了条件: 0 error。
5. 修正点を「構造」「表記」「参照」の3分類で報告する。完了条件: 変更意図が明確。

## Output Contract

| 項目            | 形式                                                     |
| --------------- | -------------------------------------------------------- |
| Target          | `path`                                                   |
| Structure Fixes | `- item`                                                 |
| Reference Fixes | `- item`                                                 |
| Verification    | `npx markdownlint-cli2 .work/AI_BLUEPRINT.md: PASS/FAIL` |

### NG例

❌ 裸 URL をそのまま残す（MD034 違反）。

❌ 見出し階層を飛ばして追加する（構造不整合）。

❌ 修正理由を書かずに結果だけ返す（説明責任不足）。

## Examples

### Example 1

Input: `.work/AI_BLUEPRINT.md` に裸 URL が含まれている。
Output: Markdown リンクへ修正した差分と lint 結果。

### Example 2

Input: `.work/AI_SCAN.md` の見出し階層が不統一。
Output: 見出しを再構成した修正版と変更分類表。

### Example 3

Input: `.claude/skills/README.md` の参照表記を統一したい。
Output: 参照記法統一済み README と検証ログ。
