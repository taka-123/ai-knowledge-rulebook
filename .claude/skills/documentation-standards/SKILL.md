---
name: documentation-standards
description: Use when repository documents must follow consistent Japanese technical style, citations, and file reference conventions; When NOT to use: when the task is code-only and no documentation output is required; Trigger Keywords: [ドキュメント, 記述規約, 文章品質, 参照, 構成].
---

# documentation-standards

## When to use

- SKILL.md・README・AGENTS.md・ルールドキュメントの文章品質を規約準拠にしたい場合。
- 記述スタイルがファイル間でばらついているので統一したい場合。

## When NOT to use

- コードのみの変更で文書更新が発生しない場合。
- 一次情報がなく推測記述しかできない場合。

## Trigger Keywords

- ドキュメント
- 記述規約
- 文章品質
- 参照
- 構成

## このリポジトリの記述規約

- **本文**: 日本語。コマンド・ファイルパス・固有名詞は英語のまま残す。
- **見出し**: `#` 形式（下線形式は使わない）。
- **箇条書き**: `-` を使う（`*` は使わない。backlog-markdown-formatting 適用時のみ `*`）。
- **ファイル参照**: `` `.claude/skills/foo/SKILL.md` `` のようにバッククォートで囲む。
- **URL**: 裸 URL は禁止。`[タイトル](URL)` 形式のリンクにする。
- **コードブロック**: 言語名を明記する（` ```bash `, ` ```json ` 等）。
- **結論先行**: 「何をするか」を最初に書き、理由・背景は後に続ける。

## Procedure

1. 対象ドキュメントのタイプを確認する（SKILL.md・README・AGENTS.md・ルールドキュメント）。
2. 同種の既存ファイルを 1〜2 件読んで、実際に使われているパターンを把握する。
3. 上記規約に照らして違反箇所を列挙する（裸 URL・下線見出し・混在スタイル等）。
4. 違反箇所のみを最小差分で修正する（文体を大きく書き直さない）。
5. `npm run lint:md` を実行して構造エラーがないことを確認する。

## Output Contract

- 修正箇所を「違反パターン / 修正内容」の形でリストアップする。
- lint:md の結果（exit code）を添える。
- 規約に該当しない箇所は変更しない。

### NG例

```
❌ 裸 URL をそのまま残す（markdownlint MD034 違反）
❌ 英語と日本語の文体を混在させる（片方に統一する）
❌ 「〜と思います」「〜かもしれません」等の推測表現で技術事実を述べる
❌ 見出しの前後に空行を入れない（markdownlint 違反）
❌ 規約修正と関係ない内容の追記・削除を同時に行う
```

## Examples

### Example 1

Input: SKILL.md の Examples に裸 URL が含まれている。
Output: `[タイトル](URL)` 形式に変換し、`npm run lint:md` が exit 0 であることを確認する。

### Example 2

Input: README のコマンド例に言語指定なしのコードブロックが複数ある。
Output: ` ```bash ` / ` ```json ` を付けて言語明記し、lint をパスさせる。

### Example 3

Input: 新規 SKILL.md の文体が英語散文になっている（他ファイルは日本語）。
Output: 日本語散文に統一し、コマンド・パス・固有名詞のみ英語を保持する。
