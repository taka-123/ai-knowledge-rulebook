---
name: pr-review-loop
description: |
  Use when: ユーザーが明示的に、対象PRのレビュー指摘とCIを収束させる、または pr-review-loop / PRレビュー収束 / レビュー対応を継続するよう依頼したとき。妥当な指摘を直し、review-clean + CI green + mergeable まで進める。
  When NOT to use: 本 Skill の発見・参照だけ。PR作成前の通常実装。単発のコードレビューだけ。merge判断だけ。仕様・設計そのものを決めるとき。
  Trigger Keywords: [pr-review-loop, PRレビュー収束, レビュー対応を継続, review-clean]
---

# pr-review-loop

## 目的

人間をレビュー結果の中継係にせず、actionable な指摘と branch 起因の CI 失敗を直して **review-clean + CI green + mergeable** まで進める。そこで止め、merge 判断を人間へ返す。merge はしない。

ユーザーが本 Skill を使って対象 PR を収束させるよう明示的に依頼した場合に限り、その PR の head branch への通常の commit と push を許可する。Skill の発見・参照だけでは許可しない。force push、default branch への push、Actions の手動 rerun は許可に含まない。

## 手順

1. 対象 PR を特定する。明示された URL / 番号を優先し、無ければ現在 branch から推定する。特定できなければ停止して確認する。
2. GitHub 操作は公式 GitHub MCP または `gh` で行う。一方が使えなければ他方を試す。merge / review 提出 / Actions 手動実行はしない。
3. 行動前に最新状態を取る: HEAD SHA、changed files、review comments / threads / decision、CI / checks、mergeability / conflict。
4. Cursor Cloud Agent で PR / CI Subscription が使えるなら、polling よりそれを使う。event 本文だけで判断せず、再開時は PR 全体を取り直す。使えない環境では継続監視できるふりをせず、取得できた最新状態まで処理して残りを返す。
5. 未対応の指摘と CI 失敗を `AUTO_FIX` / `ASK_HUMAN` / `IGNORE_WITH_REASON` に分類する。
6. `AUTO_FIX` だけを必要最小限で直す。関連する test / lint / build を実行する。
7. `AUTO_FIX` の変更があるときだけ、コミットメッセージは `commit-message-suggester` を Read して準用し、PR head branch にだけ commit + push する。
8. 新しい HEAD の review / CI を待つ、または再取得する。完了条件に達するか、非収束で `ASK_HUMAN` するまで繰り返す。push は完了ではない。reviewer 側に push-trigger の自動再レビューがある場合はそれを優先する。

上位の repository / tool policy を本手順より優先する。触るのは PR head branch だけ。同じ PR に複数の修正 Agent を並走させない。別の人・Agent が新しい commit を push したら、最新状態を読み直してから動く。

## AUTO_FIX

次をすべて満たすときだけ、再指示を待たず直す。

- 指摘が明確に妥当
- 現在の PR の目的・scope 内
- 修正が局所的で安全
- product / UX / architecture / policy の新しい意思決定を必要としない

典型: 明確な bug / regression、security 欠陥、race、stale state / error handling 漏れ、boundary / null / async 不具合、現在の変更が原因の test / build / lint 失敗、再現可能な false positive / false negative。

bot review の P0 / P1 / P2 等は参考値にする。修正要否は内容の妥当性で独立に判断する。妥当なら必要十分な修正をする。実害（secret leak、data loss、別入力の誤処理など）は severity が低くても重く扱う。無条件には従わない。

指摘のために無関係な refactor を広げない。新しい regression を作らない。再現可能な bug には、費用対効果がある範囲で回帰 test を足してよい。

## ASK_HUMAN

勝手に決めない。

- 仕様の複数解釈、product / UX、architecture、security policy / 権限境界、PR scope の大幅拡大
- 指摘の妥当性を判断しきれない
- destructive operation、merge
- 人間 reviewer への回答・交渉
- CI / dependency / infrastructure 自体の変更が current PR の scope 外
- branch と無関係な CI 失敗（flaky / runner / network / registry / 外部サービス）
  - terminal で CI green を阻害している
  - 上位 policy 上許可された回復・再実行手段がない
  - コードは変えない
- 下記の非収束

返すときは未確定点と推奨判断だけ示す。人間 reviewer のコメントへ返信せず、thread を resolve しない。

## IGNORE_WITH_REASON

コードを変えない。

- 最新 HEAD で解消済み、duplicate、outdated diff
- 指摘が事実として誤り
- PR の目的と無関係で、別 issue に分けるべき改善

## 非収束

次ではコードを足さず `ASK_HUMAN` する。固定の回数上限では止めない。

- 同じ原因の指摘が再発する
- 修正同士が打ち消し合う
- 修正が scope / architecture へ波及する
- 複数 round 連続で新規 actionable 指摘が出続け、収束傾向がない

## 完了

次をすべて満たしたら止める。PR が open でも「merge可能」と報告する。

- 現在 HEAD の CI が green
- 未対応の actionable review がない
- merge conflict がない
- PR が mergeable
- 人間判断待ちの blocker がない

報告は次だけ: 最終 HEAD、CI status、対応した指摘、未対応 / 人間判断待ち、mergeability、次の行動（通常は人間の merge 判断）。
