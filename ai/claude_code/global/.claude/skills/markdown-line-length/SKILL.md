---
name: markdown-line-length
description: "Apply proactively when creating or editing Markdown (.md, .mdx, .mdc). Max 80 chars; break at sentence boundaries; list items: nest/shorten or 4-space continuation—never single newline mid-sentence. When NOT: non-Markdown; read-only. Trigger Keywords: [markdown, line length, 行の長さ, 折り返し, 読みやすさ]."
---

# markdown-line-length

Markdown 作成・編集時に行長の上限を守る。基準は **80 文字**（Google / Prettier / markdownlint の標準）。

## When to use

- `.md` / `.mdx` / `.mdc` の作成・編集時は常に適用する。
- 既存の Markdown で行が長く読みにくいと指摘されたとき。

## When NOT to use

- Markdown 以外の編集、または Markdown を読むだけのとき。

## Trigger Keywords

- markdown, line length, 行の長さ, 折り返し, 読みやすさ

## Rule

- **最大行長**: 1 行は原則 80 文字以内。プロジェクトで 100/120 の場合はそれに従う。
- **例外**: URL・表・コードブロック・見出しは超過可。
- **平文**: 句点（。 . ? !）の直後で改行。単一改行はソフトブレークのため表示は変わらない。
- **箇条書き**:
  - インデントなしの単純改行は入れない（リスト継続が崩れる）。
  - 長いときは次のいずれかを使う。
    - ネストで子項目に分ける
    - 文言を短くして 1 行に収める
    - 次行を 4 スペースインデントで継続行にする
- **コードブロック・表**: 中身は対象外。本文のみ行長を守る。
- **見出し**: 短ければ 1 行のまま。極端に長いときだけ語の区切りで改行するか短くする。

## Output

編集結果は上記ルールを満たすこと。超過があれば句点・ネスト・短縮・4 スペース継続で修正する。

## 補足

行長を機械的に強制するには Prettier の `printWidth` や markdownlint の MD013 を有効にする。
