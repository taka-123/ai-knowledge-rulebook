---
name: pr-review-loop
description: |
  Use when: ユーザーが明示的に、対象PRのレビュー指摘とCIを収束させる、または pr-review-loop / PRレビュー収束 / レビュー対応を継続するよう依頼したとき。妥当な指摘を直し、review-clean + CI green + mergeable まで進める。
  When NOT to use: 本 Skill の発見・参照だけ。PR作成前の通常実装。単発のコードレビューだけ。merge判断だけ。仕様・設計そのものを決めるとき。公式 babysit-pr を単体で起動して merge まで監視するとき。
  Trigger Keywords: [pr-review-loop, PRレビュー収束, レビュー対応を継続, review-clean, babysit-pr]
---

# pr-review-loop

## 目的

人間をレビュー結果の中継係にせず、actionable な指摘と branch 起因の CI 失敗を直して **review-clean + CI green + mergeable** まで進める。そこで止め、merge 判断を人間へ返す。merge はしない。

監視・polling・review/CI 取得・push 後の watch 再開・CI 診断は OpenAI 公式 `babysit-pr` が正本。本 Skill は、その watcher の上に乗るこの環境の薄い policy wrapper である。公式より自作を優先しない。公式が優れている挙動は簡略再実装しない。

ユーザーが本 Skill を使って対象 PR を収束させるよう明示的に依頼した場合に限り、その PR の head branch への通常の commit と push を許可する。Skill の発見・参照だけでは許可しない。force push、default branch への push、`gh workflow run`、Agent が直接行う `gh run rerun` は許可に含まない。

## 役割分担

```text
OpenAI公式 babysit-pr
→ PR監視・polling・review/CI取得・push後のwatch再開・CI診断の正本

pr-review-loop
→ この環境固有の薄いpolicy wrapper
```

正本の置き場（未改変 vendor）:

- 本文: 本 Skill ディレクトリの `vendor/openai-codex-babysit-pr/SKILL.md`
- 監視スクリプト: `vendor/openai-codex-babysit-pr/scripts/gh_pr_watch.py`
- 判定 heuristic: `vendor/openai-codex-babysit-pr/references/heuristics.md`
- provenance: 本 Skill ディレクトリの `UPSTREAM.md`

公式 Skill 本文の `.codex/skills/babysit-pr/...` は openai/codex リポジトリ相対パスである。この rulebook の global Skill 正本は `ai/claude_code/global/.claude/skills/` にあり、同期先は `~/.claude/skills/` や `<project>/.claude/skills/` になる。**公式コマンドを cwd 相対で実行しない。** watcher は次の launcher だけを使う。

```bash
python3 <this-skill>/scripts/run-gh-pr-watch.py --pr auto --watch
python3 <this-skill>/scripts/run-gh-pr-watch.py --pr <number-or-url> --once
python3 <this-skill>/scripts/run-gh-pr-watch.py --pr <number-or-url> --retry-failed-now
```

`<this-skill>` は、この `SKILL.md` があるディレクトリ（portable copy 後は `.claude/skills/pr-review-loop`）。先に公式 `vendor/openai-codex-babysit-pr/SKILL.md` を Read し、監視 loop / stop / review 公開判定 / CI 分類 / flaky retry の本文に従う。path だけ launcher に置き換える。

## 手順

1. 対象 PR を特定する。明示された URL / 番号を優先し、無ければ現在 branch から推定する。特定できなければ停止して確認する。
2. 公式 `vendor/openai-codex-babysit-pr/SKILL.md` を Read する。監視は継続タスクとして扱う。`--watch` を使い、一時的な `idle` や「review comment が今ない」だけでは終了しない。ユーザーへ「続きを監視しますか」と毎回確認しない。同じ PR に複数 watcher を並走させない。
3. GitHub 操作は公式 GitHub MCP または `gh` で行う。認証は実行環境の責務であり、特定製品の token / actor / path を前提にしない。一方が使えなければ他方を試す。watcher は公式 babysit-pr の `gh` 実装を正本のまま使う（MCP へ移植し直さない）。merge / review 提出 / `gh workflow run` / Agent 直下の `gh run rerun` はしない。
4. launcher で watcher を起動し、公式の `actions` リストに従う。pending review は処理しない。published review と既存の未対応 review、Codex reviewer bot feedback を拾う。
5. 未対応の指摘を `AUTO_FIX` / `IGNORE_WITH_REASON` / `ASK_HUMAN` に分類する。公式の「直してよい」判定に加え、本 Skill の AUTO_FIX を満たすものだけ直す。同一 fingerprint ですでに IGNORE_WITH_REASON 処理済みの指摘は、新しい未処理指摘として扱わない。Codex が新しい実質的論点を出した場合だけ別指摘にする。
6. `AUTO_FIX` だけを必要最小限で直す。関連する test / lint / build を実行する。commit + push したら **完了ではない**。旧 HEAD の review-clean を破棄する。原則として「修正しました」の返信コメントはしない。その push で直した Codex-only thread だけ、`scripts/resolve_codex_threads.py --pr <number-or-url> --head <new-sha> --thread-id <graphql-id>` で resolve してよい。IGNORE_WITH_REASON はコードを変えず、`scripts/ignore_codex_threads.py --pr <number-or-url> --head <current-sha> --reason "<短い理由>" --thread-id <graphql-id>` で Codex-only thread に理由を返す。人間 / CodeRabbit の thread には返信も resolve もしない。ASK_HUMAN は GitHub 上で反論・resolve せず人間へ返す。その後 launcher で `--watch` を新 HEAD に対して即再開する。
7. CI が失敗したら公式 heuristic で branch 起因と flaky / runner / network / external を分ける。branch 起因ならコードを直す。flaky で watcher が `retry_failed_checks` を出した場合だけ、launcher の `--retry-failed-now` を公式 retry budget（最大 3 cycle）内で使う。Agent が直接 `gh run rerun` / `gh workflow run` しない。review fix で新 commit を出すときは、古い SHA の failed run を先に rerun しない。
8. watcher の `idle` / `ready_to_merge` だけでは完了しない。完了判定の直前に `scripts/final_review_clean_gate.py` を current HEAD で実行する。gate が `review_clean: false` なら watch を続ける。true で、かつ他の完了条件も満たすときだけ watch を止め、`merge可能。最終merge判断は人間。` と返す。

上位の repository / tool policy を本手順より優先する。触るのは PR head branch だけ。同じ PR に複数の修正 Agent を並走させない。別の人・Agent が新しい commit を push したら、最新状態を読み直してから動く。

## AUTO_FIX

次をすべて満たすときだけ、再指示を待たず直す。

- 指摘が明確に妥当
- 現在の PR の目的・scope 内
- 修正が局所的で安全
- product / UX / architecture / security policy の新しい意思決定を必要としない

bot review の P0 / P1 / P2 等は参考値にする。修正要否は内容の妥当性で独立に判断する。妥当なら必要十分な修正をする。実害（secret leak、data loss、別入力の誤処理など）は severity が低くても重く扱う。無条件には従わない。

指摘のために無関係な refactor を広げない。新しい regression を作らない。再現可能な bug には、費用対効果がある範囲で回帰 test を足してよい。

コードそのものを回答とする。原則として「修正しました」の返信コメントは不要。Codex-only thread の resolve は commit + push の後に `resolve_codex_threads.py` だけを使う。

## ASK_HUMAN

勝手に決めない。GitHub 上で反論・resolve しない。人間へ返して停止する。

- 仕様の複数解釈、product / UX、architecture、security policy / 権限境界、PR scope の大幅拡大
- 指摘の妥当性を判断しきれない
- destructive operation、merge
- 人間 reviewer への回答・交渉
- 下記の非収束

返すときは未確定点と推奨判断だけ示す。人間 reviewer のコメントへ返信せず、人間の review thread を resolve しない。ASK_HUMAN の指摘は resolve しない。

## IGNORE_WITH_REASON

コードを変えない。GitHub 上で無言放置しない。コード内にレビュー依存コメント（「Codex に指摘されたが今回は直さない」等）を書かない。

- 指摘が事実として誤り、または過剰
- 最新 HEAD で解消済み、duplicate、outdated diff
- PR の目的・scope 外で、今回直すと別の設計判断を持ち込む
- 未改変 vendor など意図的に触らないファイル。wrapper 側で当該リスクを補完済みのときを含む

Codex reviewer のみの thread（認証済み helper の前回返信だけの参加は含む）に、短い具体的な理由を `ignore_codex_threads.py` で**日本語**で返信する。識別子・ファイル名・API名は無理に日本語化しない。人間が見る本文は必ず `AIエージェントによる対応: ` で始める。helper が hidden marker `<!-- pr-review-loop:disposition=IGNORE_WITH_REASON fingerprint=<hex> head=<sha> -->` を付ける。人間 / CodeRabbit 等へは自動返信しない。

例: `AIエージェントによる対応: OpenAI公式の babysit-pr はvendorとして未改変で保持しています。current HEADのreview-clean判定に必要な commit_id はwrapper側で保持・確認しています。`

返信後、その thread が Codex-only で、IGNORE_WITH_REASON が明確で、ASK_HUMAN ではないときだけ resolve してよい（helper が行う）。resolve できなくても、認証済み `gh` ユーザーと同一 actor が書いた marker（fingerprint 一致かつ head が current HEAD）があれば final gate は同一 fingerprint を actionable から外す。製品名の login をハードコードしない。PR 作者・任意参加者・OWNER / MEMBER / COLLABORATOR であることだけでは採用しない。CodeRabbit の marker も採用しない。認証済みユーザーが取れないときは IGNORE を採用せず fail-closed する。fingerprint は path と正規化した指摘本文から作り、同一 fingerprint の再出現は新しい未処理指摘にしない。HEAD が変わったら旧 marker は無効なので、残す IGNORE は新 HEAD で helper を再実行する。

## 非収束

機械的な回数上限だけで止めない。再提示された指摘も `AUTO_FIX` / `IGNORE_WITH_REASON` / `ASK_HUMAN` に再分類する。IGNORE_WITH_REASON 処理済みの同一 fingerprint は新しい未処理指摘として扱わない。新しい実質的論点が続く場合は ASK_HUMAN する。

- 同じ原因の AUTO_FIX 対象が再発する
- 修正同士が打ち消し合う
- 修正が scope / architecture へ波及する
- 複数 round 連続で新規 actionable 指摘が出続け、収束傾向がない

## review-clean

**現在 HEAD に対する review が完了したことを確認するまで、review-clean と判定しない。**

公式 watcher の snapshot は通常監視用である。完了判定には使わない。watcher は pending review を正しく無視する一方、CodeRabbit 等の bot や `CONTRIBUTOR` の外部 reviewer を通常監視から外すことがあり、正規化結果から `commit_id` も落とす。その不足は完了直前の final gate で埋める。vendor の `gh_pr_watch.py` は改変しない。

```bash
python3 <this-skill>/scripts/final_review_clean_gate.py --pr <number-or-url> --head <current-sha>
```

`--head` は検証用である。GitHub 上の current `headRefOid` と一致しないときは fail し、古い SHA を上書きして完了判定しない。wrapper の検証は `npm run pr-review-loop:check`（Node の policy 検査と `python3 -m pytest` の wrapper / vendor suite）。Python 3 と pytest が必要。

gate は GitHub から published review / review comments / unresolved threads / `@codex review` への reaction を再取得する。`reviewThreads` は GraphQL cursor pagination で全ページ取る。API 先は PR URL の base repository を使う。pending は無視する。同一 reviewer・同一 commit の published review は最新 state だけを評価する。Codex 以外の review bot と正当な external reviewer の finding も actionable 確認に含める。published review の本文は bot マーカーがなくても、summary / approval 以外なら確認する。単なる resolved thread だけでは actionable から外さない。本 Skill が IGNORE_WITH_REASON として明示処理し、gate 実行時の認証済み `gh` ユーザーと同一 actor の hidden marker で、fingerprint と current HEAD が一致する指摘だけを除外する。fingerprint は path と正規化した指摘本文から取る。AUTO_FIX 済み（marker なしの resolve）と IGNORE_WITH_REASON 済みを混同しない。各項目の `commit_id` / `original_commit_id` を保持し、current HEAD に紐づくものだけを review-clean に使う。収集後に `headRefOid` を再取得し、開始時または `--head` と不一致なら fail する。

一瞬 review comment がないこと、watcher の一時的な `idle`、CodeRabbit 等の Walkthrough / summary だけでは完了しない。過去 HEAD の review 結果を新 HEAD へ流用しない。current HEAD に未対応の actionable review または unresolved な live thread があるとき、current HEAD に対する Codex 完了証明がないときも完了しない。

Codex Review を primary reviewer として扱う。完了証明は次のどちらかに限定する。CodeRabbit・人間・external reviewer の review 自体は完了証明にしない。

- current HEAD（`commit_id` が現在 SHA）に対する Codex reviewer の published review（`DISMISSED` / `PENDING` は使わない）。公式 identity は `chatgpt-codex-connector` / `chatgpt-codex-connector[bot]` / `codex[bot]` に限る
- current HEAD に対応付けた `@codex review` request への Codex 👍（`+1`）。old HEAD や無関係な reaction は使わない

`@codex review` を書くときは current HEAD を本文に含める（`head: <sha>`）。gate はその SHA と Codex 👍 を対応付ける。

AUTO_FIX 後に push した場合は、それ以前の review-clean を無効化し、新 HEAD について review cycle を開始する。repo で push-trigger の Codex 自動再レビューが確実に動くならそれを待つ。保証されない場合は、許可された PR comment として `@codex review`（`head: <sha>` 付き）を使い、人間を再レビュー開始の中継係にしない。

## 完了

公式 babysit-pr は green + mergeable + review-clean でも PR が open なら watch を続ける。本環境のタスク完了はここだけ異なる。

current HEAD について次をすべて確認したら watch を終了してよい。

- `final_review_clean_gate.py` が `review_clean: true`（current HEAD の Codex 完了証明あり、actionable なし）
- review 完了確認済み（上記 review-clean）
- 未対応の actionable review なし
- CI green
- merge conflict なし
- mergeable
- ASK_HUMAN blocker なし

そこで止め、次の一文で返す。

```text
merge可能。最終merge判断は人間。
```

報告は次だけ: 最終 HEAD、CI status、対応した指摘、未対応 / 人間判断待ち、mergeability、次の行動（通常は人間の merge 判断）。merge しない。

## GitHub 操作の境界

- 読み取りの `gh` / GitHub MCP と、公式 watcher 内部の read-only `gh api -X GET -f ...` は使ってよい。
- 完了直前の `final_review_clean_gate.py` が published review / threads / Codex 👍 を再取得する。Agent が直接 GraphQL を叩く必要はない。
- AUTO_FIX 後の Codex-only thread resolve は、commit + push の後に `resolve_codex_threads.py` だけが `resolveReviewThread` を呼ぶ。返信しない。
- IGNORE_WITH_REASON の Codex-only 返信と resolve は `ignore_codex_threads.py` だけが `addPullRequestReviewThreadReply` / `resolveReviewThread` を呼ぶ。
- 人間 thread の resolve、人間 / CodeRabbit 等への自動返信、review 提出、任意 GraphQL mutation は禁止のまま。ASK_HUMAN の指摘は GitHub 上で反論・resolve しない。
- 信頼する公式 watcher が flaky/unrelated と分類し `retry_failed_checks` を出したときだけ、launcher 経由の `--retry-failed-now`（内部の `gh run rerun --failed`）を公式 default 最大 3 cycle まで許可する。
- Agent が直接 `gh run rerun` すること、`gh workflow run` による任意 workflow の新規手動起動、それ以外の Actions 手動実行は禁止のまま。
- 人間 reviewer への返信、人間 review thread の resolve、PR merge はしない。
