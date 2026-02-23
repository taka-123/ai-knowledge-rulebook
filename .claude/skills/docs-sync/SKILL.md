---
name: docs-sync
description: Use when README and structure documents must be synchronized with actual repository layout and commands; When NOT to use: when changes are isolated and documentation truth remains unchanged; Trigger Keywords: [README, directorystructure, technologystack, 同期, 実態反映].
---

# docs-sync

## When to use

- コード・スキル・スクリプトの変更後に README や AGENTS.md が実態と乖離した場合。
- ディレクトリ構成・コマンド一覧・スキル一覧が実ファイルと合わなくなった場合。

## When NOT to use

- 変更が文書に記載されていない範囲のみで、文書の真実性が保たれている場合。
- 構成が未確定で確定版文書を更新できない場合。

## Trigger Keywords

- README
- directorystructure
- technologystack
- 同期
- 実態反映

## Procedure

1. `git diff --name-only HEAD` または `git diff --staged --name-only` で変更ファイルを列挙する。
2. 変更ファイルが参照されている文書箇所を `grep -r` または Grep ツールで特定する（README.md, AGENTS.md, `.claude/CLAUDE.md` 等）。
3. 実態（`ls`, `cat package.json` 等）を確認し、文書の記載と差分を特定する。
4. **変更箇所のみ**を最小差分で更新する（関係ない段落を書き直さない）。
5. `npm run lint:md` を実行して Markdown 整合性を確認する。

## Output Contract

- 更新した文書パスと変更行番号を報告する。
- 「実態 vs 文書の差分」を Before/After で示す。
- 確認に使ったコマンドと結果を添える。

### NG例

```
❌ 変更されていない段落を「ついでに」書き直す（差分が広がる）
❌ 実態確認コマンドを実行せず記憶で文書を更新する
❌ lint:md を通さず整形崩れを混入させる
❌ README 全体を書き直す（最小差分を守る）
```

## Examples

### Example 1

Input: 新しいスキルを追加したので README のスキル一覧が古くなった。
Output: `ls .claude/skills/` の結果と README の一覧を比較し、追加分のみ README に反映する。

### Example 2

Input: `package.json` に新しい npm script を追加したが CLAUDE.md のコマンド一覧が古い。
Output: `cat package.json | jq '.scripts'` の結果を確認し、CLAUDE.md の該当セクションを最小差分で更新する。

### Example 3

Input: `schemas/` に新しいスキーマファイルを追加したが README に記載がない。
Output: README の該当セクションにファイル名と用途を1行追記し、`npm run lint:md` パスを確認する。
