---
name: natural-language-review-router
description: "Use proactively when editing CLAUDE.local.md, .claude/commands/, .cursor/rules/, .cursor/commands/, or .codex/REVIEW_PLAYBOOK.md to route natural-language review requests; When NOT to use: when reviewer routing already works and only agent internals are being modified; Trigger Keywords: [レビューしてください, routing, review request, natural language, fallback]."
---

# natural-language-review-router

## When to use

- `レビューしてください` のような自然文依頼を reviewer 系へ確実にルーティングしたいとき。
- `requirements.md` と `直近コミット` の同時入力時に固定パイプラインを適用したいとき。
- reviewer 失敗時フォールバックルールを rules/commands に埋め込みたいとき。

## When NOT to use

- ルーティングではなく reviewer 本体ロジックだけを修正するとき。
- 自然文レビュー依頼の導線がすでに正常動作しているとき。
- 単一プラットフォームのみで運用する一時作業のとき。

## Trigger Keywords

- レビューしてください
- routing
- review request
- natural language
- fallback

## Runtime routing (reference)

レビュー依頼は **発話で分けず、コンテキストで自動ルーティング**する。差分取得後、小さい（約 400 LOC 未満・ファイル数少なめ）かつリスク領域でない → **ai-diff-review**（単一パス）。大きい or リスク領域 → **cross-service-reviewer** 起点のパイプライン。オーバーライド: 「しっかり」「full」→ パイプライン強制。「軽く」「quick」→ 単一パス強制。詳細は `.codex/REVIEW_PLAYBOOK.md` および `.cursor/rules/review-routing.mdc` を参照。

## Procedure

1. `cat CLAUDE.local.md`、`cat .claude/commands/review-request.md`、`cat .cursor/rules/review-routing.mdc` を読み現行ルールを確認する。
2. 自然文トリガー語（レビューしてください/この修正でOKか/見てほしい）を description-first で reviewer に接続する。
3. `requirements.md + 直近コミット` 条件の固定パイプラインを `cross-service-reviewer -> code-reviewer -> security-reviewer -> verifier` で記述する。
4. reviewer 失敗時に親が代替し、失敗エージェント名と代替観点を報告する要件を明記する。
5. `rg -n "レビューしてください|requirements.md|直近コミット|fallback" CLAUDE.local.md .claude/commands .cursor/rules .cursor/commands .codex/REVIEW_PLAYBOOK.md` で反映を検証する。

## Output Contract

| 項目                  | 形式                               |
| --------------------- | ---------------------------------- |
| Status                | `PASS / FAIL / BLOCKED`            |
| Updated Routing Files | `- path`                           |
| Trigger Coverage      | `自然文トリガー -> agent` の対応表 |
| Fallback Rule         | `失敗agent` と `親の代替観点`      |
| Verification          | `rg -n ...` の結果要約             |

### NG例

❌ slash command だけに依存し自然文導線を作らない（要件未達）。

❌ 失敗時フォールバックを未記述で終了する（レビュー完遂性がない）。

❌ 静的マッピングを大量追加して description-first を壊す（保守負債が増える）。

## Examples

### Example 1

Input: `CLAUDE.local.md` と `.claude/commands/review-request.md` を使って `この修正でOKかレビューしてください` を reviewer へ流したい。
Output: ルーティング定義とトリガー対応表。

### Example 2

Input: `.cursor/rules/review-routing.mdc` で `requirements.md` と `直近コミット` を含む依頼を処理したい。
Output: 固定パイプライン定義と実行順チェックリスト。

### Example 3

Input: `.codex/REVIEW_PLAYBOOK.md` に `security-reviewer` タイムアウト時の挙動を定義したい。
Output: 親代替ルールを含むフォールバック手順書。
