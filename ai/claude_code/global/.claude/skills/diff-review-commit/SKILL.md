---
name: diff-review-commit
description: |
  Use when: ユーザーがスラッシュまたは明示で、未コミット差分の妥当性確認のうえコミットまで行うよう頼んだとき。
  When NOT to use: 品質チェックだけでコミットしないとき（diff-quality-gate）。メッセージ案だけ（commit-message-suggester）。PR前の受け入れ条件レビュー。差分がないとき。amend / rebase / push が主目的のとき。
  Trigger Keywords: [diff-review-commit, 差分確認してコミット, チェックしてコミット, 妥当ならコミット, レビューしてコミット]
---

# diff-review-commit

未コミット差分を品質ゲート通過後にコミットする。

依存は **各 SKILL.md を Read して準用**する（内容は再掲しない）:

- 品質ゲート: `diff-quality-gate`
- メッセージ形式・意図分割・git コミット手順: `commit-message-suggester`

## Procedure

1. `git status` で差分の有無を確認し、無ければ「差分なし」と報告して終了する（コミットしない）。
2. `diff-quality-gate` の SKILL.md を Read し、その手順に従う。
3. 不合格のとき:
   - **軽微かつ依頼範囲内** → 直してゲートを**もう一度だけ**再適用する。
   - **判断が要る・範囲外・再適用後も不合格** → 指摘だけ出してコミットしない。
4. 合格ならゲート結果を短く述べ、`commit-message-suggester` の SKILL.md を Read してメッセージを決め、**コミットを実行する**（このスキルの呼び出し自体がコミットの明示依頼にあたる）。分割が必要なら順にコミットする。
5. push / amend はしない。
