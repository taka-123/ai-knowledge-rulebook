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
# --retry-failed-now は launcher が拒否する（vendor は flaky 分類を検証しない）
```

`<this-skill>` は、この `SKILL.md` があるディレクトリ（portable copy 後は `.claude/skills/pr-review-loop`）。先に公式 `vendor/openai-codex-babysit-pr/SKILL.md` を Read し、監視 loop / stop / review 公開判定 / CI 分類 / flaky retry の本文に従う。path だけ launcher に置き換える。

## 手順

1. 対象 PR を特定する。明示された URL / 番号を優先し、無ければ現在 branch から推定する。特定できなければ停止して確認する。
2. 公式 `vendor/openai-codex-babysit-pr/SKILL.md` を Read する。監視は継続タスクとして扱う。`--watch` を使い、一時的な `idle` や「review comment が今ない」だけでは終了しない。ユーザーへ「続きを監視しますか」と毎回確認しない。同じ PR に複数 watcher を並走させない。
3. GitHub 操作は公式 GitHub MCP または `gh` で行う。認証は実行環境の責務であり、特定製品の token / actor / path を前提にしない。一方が使えなければ他方を試す。watcher は公式 babysit-pr の `gh` 実装を正本のまま使う（MCP へ移植し直さない）。merge / review 提出 / `gh workflow run` / Agent 直下の `gh run rerun` はしない。
4. launcher で watcher を起動し、公式の `actions` リストに従う。pending review とその inline は処理しない。current HEAD の Codex 完了証明が出るまで、Codex の途中 finding を確定扱いせず、同じ HEAD へ新たな `@codex review` も出さない。途中の Codex コメントをレビューの全部とみなして push しない。CI 失敗の修正と、人間 / CodeRabbit の既知指摘は待たない。watch を続ける。
5. Codex 完了証明が出たら、その HEAD の未対応の指摘をまとめて `AUTO_FIX` / `IGNORE_WITH_REASON` / `ASK_HUMAN` に分類する。公式の「直してよい」判定に加え、本 Skill の AUTO_FIX を満たすものだけ直す。current HEAD に bind 済みの同一 fingerprint は新しい未処理指摘として扱わない。旧 HEAD の IGNORE marker だけでは処理済みにしない。Codex が新しい実質的論点を出した場合だけ別指摘にする。
6. `AUTO_FIX` だけを必要最小限で直す。関連する test / lint / build を実行する。commit 前に `commit-message-suggester` Skill が利用可能か確認し、存在する場合はその `SKILL.md` を Read する。利用可能な場合は staged を含む未コミット差分全体を確認し、その Skill の自律作業モードに従ってコミットメッセージを決定する。利用できない場合も `<prefix>: <日本語1行>` の形式で差分全体を一つの意図として扱う。commit + push したら **完了ではない**。旧 HEAD の review-clean を破棄する。原則として「修正しました」の返信コメントはしない。その push で直した Codex-only thread だけ、`scripts/resolve_codex_threads.py --pr <number-or-url> --head <new-sha> --thread-id <graphql-id>` で resolve してよい。IGNORE_WITH_REASON はコードを変えず、`scripts/ignore_codex_threads.py --pr <number-or-url> --head <current-sha> --reason "<短い理由>" --thread-id <graphql-id>` で Codex-only thread に理由を返す。同一 thread と同一 fingerprint なら既存の helper 返信を更新し、人間向け返信を増やさない。人間 / CodeRabbit の thread には返信も resolve もしない。ASK_HUMAN は GitHub 上で反論・resolve せず人間へ返す。その後 launcher で `--watch` を新 HEAD に対して即再開する。
7. CI が失敗したら公式 heuristic で branch 起因と flaky / runner / network / external を分ける。branch 起因ならコードを直す。launcher は `--retry-failed-now` を拒否する。vendor の `retry_failed_checks` は flaky 分類を検証しない。Agent が直接 `gh run rerun` / `gh workflow run` しない。review fix で新 commit を出すときは、古い SHA の failed run を先に rerun しない。
8. watcher の `idle` / `ready_to_merge` だけでは完了しない。監視の待ちは公式 `--watch` に任せる。`final_review_clean_gate.py` を sleep ループの代替にしない。watcher が新しい published review または Codex 完了シグナルを出したら、完了判定の直前に gate を current HEAD で一度実行する。gate が `review_clean: false` なら `--watch` に戻る。true で、かつ他の完了条件も満たすときだけ watch を止め、`merge可能。最終merge判断は人間。` と返す。

上位の repository / tool policy を本手順より優先する。repository に `REVIEW.md` があれば PR review 時は Read し、指摘の分類・優先度・非収束方針に従う。触るのは PR head branch だけ。同じ PR に複数の修正 Agent を並走させない。別の人・Agent が新しい commit を push したら、最新状態を読み直してから動く。

## AUTO_FIX

次をすべて満たすときだけ、再指示を待たず直す。Codex の P1 ラベルだけで機械的に AUTO_FIX しない。`REVIEW.md` の P1 定義と整合する具体的 root cause を優先する。

- current HEAD / proof / thread / disposition / CI 判定の実バグ
- review_clean を誤って true / false にする問題
- unresolved finding の取りこばし
- human thread の誤 resolve
- hard security boundary の破壊
- 通常の Agent 操作で自然に踏む canonical な guardrail 穴
- `REVIEW.md` で P1 に相当する具体的な問題
- 指摘が明確に妥当で、現在の PR の目的・scope 内
- 修正が局所的で安全
- product / UX / architecture / security policy の新しい意思決定を必要としない

bot review の P0 / P1 / P2 等は参考値にする。修正要否は内容の妥当性で独立に判断する。妥当なら必要十分な修正をする。実害（secret leak、data loss、別入力の誤処理など）は severity が低くても重く扱う。無条件には従わない。

指摘のために無関係な refactor を広げない。新しい regression を作らない。再現可能な bug には、費用対効果がある範囲で回帰 test を足してよい。

コードそのものを回答とする。原則として「修正しました」の返信コメントは不要。Codex-only thread の resolve は commit + push の後に `resolve_codex_threads.py` だけを使う。

## ASK_HUMAN

勝手に決めない。GitHub 上で反論・resolve しない。人間へ返して停止する。

- threat model の変更
- credential 権限変更
- Rulesets / Branch Protection 変更
- 新しい sandbox / MCP architecture
- 仕様・architecture / security policy の新しい判断
- 仕様の複数解釈、product / UX、architecture、security policy / 権限境界、PR scope の大幅拡大
- 指摘の妥当性を判断しきれない
- destructive operation、merge
- 人間 reviewer への回答・交渉
- review budget を使い切っても完了条件を満たさない場合
- 下記の非収束

返すときは未確定点と推奨判断だけ示す。人間 reviewer のコメントへ返信せず、人間の review thread を resolve しない。ASK_HUMAN の指摘は resolve しない。

## IGNORE_WITH_REASON

コードを変えない。GitHub 上で無言放置しない。コード内にレビュー依存コメント（「Codex に指摘されたが今回は直さない」等）を書かない。

- 指摘が事実として誤り、または過剰
- 最新 HEAD で解消済み、duplicate、outdated diff
- PR の目的・scope 外で、今回直すと別の設計判断を持ち込む
- 未改変 vendor など意図的に触らないファイル。wrapper 側で当該リスクを補完済みのときを含む
- best-effort hook に対する adversarial Shell syntax variant（同じ root cause の構文違い）
- hard boundary を破らない理論的 bypass
- `REVIEW.md` の threat model 上、意図的に受容している残余リスク

例: `AIエージェントによる対応: このhookは通常のAI Agentによる典型的な誤操作を防ぐbest-effort guardrailです。敵対的なShell構文変形を完全に防ぐsecurity boundaryとはしておらず、絶対禁止が必要な操作はcredential・sandbox・GitHub側保護等で制御する方針のため、このsyntax variantには追加対応しません。`

同じ root cause の syntax variant を新しい AUTO_FIX として無限に扱わない。

Codex reviewer のみの thread（認証済み helper の前回返信だけの参加は含む）に、短い具体的な理由を `ignore_codex_threads.py` で**日本語**で返信する。識別子・ファイル名・API名は無理に日本語化しない。人間が見る本文は必ず `AIエージェントによる対応: ` で始める。helper が hidden marker `<!-- pr-review-loop:disposition=IGNORE_WITH_REASON fingerprint=<hex> head=<sha> -->` を付ける。人間 / CodeRabbit 等へは自動返信しない。

例: `AIエージェントによる対応: OpenAI公式の babysit-pr はvendorとして未改変で保持しています。current HEADのreview-clean判定に必要な commit_id はwrapper側で保持・確認しています。`

返信後、その thread が Codex-only で、IGNORE_WITH_REASON が明確で、ASK_HUMAN ではないときだけ resolve してよい（helper が行う）。resolve できなくても、認証済み `gh` ユーザーと同一 actor が書いた marker（fingerprint 一致かつ head が current HEAD）があれば final gate は **その thread に属する item** だけを actionable から外す。指摘本文に disposition marker を埋め込んだだけでは除外しない。製品名の login をハードコードしない。PR 作者・任意参加者・OWNER / MEMBER / COLLABORATOR であることだけでは採用しない。CodeRabbit の marker も採用しない。認証済みユーザーが取れないときは IGNORE を採用せず fail-closed する。fingerprint は path と正規化した指摘本文から作り、同一 thread の同一 fingerprint 再出現は新しい未処理指摘にしない。別 thread の同一 fingerprint は別 finding として扱う。HEAD が変わったら旧 marker は無効なので、残す IGNORE は新 HEAD で helper を再実行する。helper は同一 thread と同一 fingerprint の既存返信を更新して current HEAD に再bindし、人間向け返信を増やさない。理由が同じなら本文は維持し hidden marker の head だけ更新する。IGNORE が妥当でなくなった旧 marker は current HEAD の proof にしない。

## 非収束

指摘の分類を、固定回数だけで打ち切らない。再提示された指摘も `AUTO_FIX` / `IGNORE_WITH_REASON` / `ASK_HUMAN` に再分類する。current HEAD に bind 済みの同一 fingerprint は新しい未処理指摘として扱わない。新しい実質的論点が続く場合は ASK_HUMAN する。自動 review cycle の総量は下記 Review budget に従う。

- 同じ原因の AUTO_FIX 対象が再発する
- 修正同士が打ち消し合う
- 修正が scope / architecture へ波及する
- 複数 round 連続で新規 actionable 指摘が出続け、収束傾向がない

## Review budget

自動で行う reviewer の review cycle は、初回を含め原則最大 3 回とする。現在の primary reviewer は Codex Review だが、本予算は reviewer 非依存である。

1 cycle は、1つの HEAD に対して開始した review と、その完了確認までを一まとまりとして数える。同一 HEAD に複数の completion proof がある場合や、状態確認・polling を繰り返した場合も 1 cycle のままとする。push-trigger の自動 review も cycle に含める。

- 最初に review する HEAD を 1 cycle 目とする。
- `AUTO_FIX` で HEAD が変わり、新 HEAD に対して review を開始した場合は次の 1 cycle とする。
- 同一 HEAD に対する重複 review request は行わず、cycle も増やさない。
- `IGNORE_WITH_REASON` のみでコード変更がない場合は、新しい review cycle を開始しない。

3 回は「問題を無視して merge-ready にする」上限ではない。3 cycle 終了時点で完了条件を満たしていなければ `ASK_HUMAN` で停止する。budget 超過を理由に未解決の finding を無視したり、review-clean と判定したりしない。

P2 / P3 の扱いは `REVIEW.md` の既存方針に従う。P0 や重大な hard security boundary の問題が残る場合も、自動で無限継続せず人間へ返す。ユーザーが明示的に継続を指示した場合のみ、追加 cycle を実行してよい。

`REVIEW.md` の「同一 root cause の blocking review は原則最大 3 round」とは別物である。

- `REVIEW.md`: 同一 root cause を無限追跡しないための制限
- 本 Skill の review budget: PR 全体として自動レビューを無限継続しないための総量制限

## review-clean

**現在 HEAD に対する review が完了したことを確認するまで、review-clean と判定しない。**

公式 watcher の snapshot は通常監視用である。完了判定には使わない。watcher は pending review を正しく無視する一方、CodeRabbit 等の bot や `CONTRIBUTOR` の外部 reviewer を通常監視から外すことがあり、正規化結果から `commit_id` も落とす。その不足は完了直前の final gate で埋める。vendor の `gh_pr_watch.py` は改変しない。

```bash
python3 <this-skill>/scripts/final_review_clean_gate.py --pr <number-or-url> --head <current-sha>
```

`--head` は検証用である。GitHub 上の current `headRefOid` と一致しないときは fail し、古い SHA を上書きして完了判定しない。wrapper の検証は `npm run pr-review-loop:check`（Node の policy 検査と `python3 -m pytest` の wrapper / vendor suite）。Python 3 と pytest が必要。

gate は GitHub から published review / review comments / unresolved threads / Codex 完了シグナルを再取得する。認証済み `gh` ユーザー取得など必要な外部状態取得を先に終え、すべての GitHub 取得のあとに final HEAD recheck を行う。final HEAD recheck 後は純粋なローカル評価だけにする。`reviewThreads` は GraphQL cursor pagination で全ページ取る。API 先は PR URL の base repository を使う。pending は無視する。同一 reviewer・同一 commit の published review は最新 state だけを評価する。後続の `COMMENTED` では以前の `CHANGES_REQUESTED` を解除せず、以前の actionable な `COMMENTED` review も捨てない。`APPROVED` / `DISMISSED` / 新たな `CHANGES_REQUESTED` は、同じ reviewer・commit の保持済み COMMENTED も含めて解除する。Codex 以外の review bot と正当な external reviewer の finding も actionable 確認に含める。published review の本文は bot マーカーがなくても、summary / approval 以外なら確認する。単なる resolved thread だけでは actionable から外さない。本 Skill が IGNORE_WITH_REASON として明示処理し、gate 実行時の認証済み `gh` ユーザーと同一 actor の hidden marker で、fingerprint と current HEAD が一致し、かつ item と thread/comment ID が対応する指摘だけを除外する。fingerprint は path と正規化した指摘本文から取る。別 thread の同一 fingerprint は除外しない。AUTO_FIX 済み（marker なしの resolve）と IGNORE_WITH_REASON 済みを混同しない。各項目の `commit_id` / `original_commit_id` を保持する。published review と completion は `commit_id`、inline finding は `original_commit_id` を優先して current HEAD に紐づける。GitHub が後続 commit へ付け替えた `commit_id` だけでは、過去 review の指摘を新 HEAD の未処理にしない。未 resolve の live thread は残す。収集後に `headRefOid` を再取得し、開始時または `--head` と不一致なら fail する。GraphQL `author` が取れないコメントがある thread は不完全として IGNORE も resolve もしない。

一瞬 review comment がないこと、watcher の一時的な `idle`、CodeRabbit 等の Walkthrough / summary だけでは完了しない。過去 HEAD の review 結果を新 HEAD へ流用しない。current HEAD に未対応の actionable review または unresolved な live thread があるとき、current HEAD に対する Codex 完了証明がないときも完了しない。P0 / P1 finding badge と `changes requested` を actionable の主マーカーとする。P2 / P3 badge のみは `REVIEW.md` に従い review-clean を塞がない。

Codex Review を primary reviewer として扱う。完了証明は、Codex reviewer が current HEAD の review を出し終えたシグナルに限る。CodeRabbit・人間・external reviewer の review 自体は完了証明にしない。`DISMISSED` / `PENDING` は使わない。old HEAD や無関係な reaction は使わない。公式 identity は `chatgpt-codex-connector` / `chatgpt-codex-connector[bot]` / `codex[bot]` に限る。

次のいずれかを current HEAD に bind できたときだけ完了証明とする。

- Codex reviewer の published review
- current HEAD に bind した **未編集** の `@codex review` request への Codex 👍（`+1`）
- Codex reviewer 自身の issue comment で、`Reviewed commit` 形式により current HEAD を明示し、指摘なしの既知マーカー（`:+1:` / 👍、または同等の明示文）があるもの。本文への SHA 部分一致や、blocking badge の不在だけでは証明にしない。

`@codex review` の issue comment、Codex 👍、Codex の HEAD 結び完了コメントは完了証明だけに使い、finding 判定から除外する。

`@codex review` request は immutable とする。新しい HEAD では新しい `@codex review` comment を作る。過去 request を編集して別 HEAD へ再 bind しない。編集済み request comment は completion proof にしない。reaction の `created_at` と comment の `updated_at` の秒単位比較で前後関係を推定しない。

`@codex review` を書くときは current HEAD を本文に含める（`head: <sha>`）。gate は request の SHA と Codex 👍、および Codex 完了コメントの Reviewed commit を current HEAD に対応付ける。

current HEAD の Codex 完了証明が出る前に、同じ HEAD へ再度 `@codex review` を要求しない。完了証明のあと、finding を IGNORE_WITH_REASON として明示処理し、他に actionable finding が無ければ、同じ HEAD へ再度要求しない。そのまま final gate → CI → mergeability を確認する。完了証明のあとに AUTO_FIX して HEAD が変わった場合だけ、新 HEAD に対して新しい Codex review を 1 回要求する。Review budget の cycle 計数に従う。

AUTO_FIX 後に push した場合は、それ以前の review-clean を無効化し、新 HEAD について review cycle を開始する。repo で push-trigger の Codex 自動再レビューが確実に動くならそれを待つ（その自動 review も budget に含める）。保証されない場合は、許可された PR comment として新しい `@codex review`（`head: <sha>` 付き）を使い、人間を再レビュー開始の中継係にしない。既存 request comment の編集・再利用はしない。budget を使い切っているときは追加 request せず `ASK_HUMAN` する。

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
- 完了直前の `final_review_clean_gate.py` が published review / threads / Codex 完了シグナルを再取得する。Agent が直接 GraphQL を叩く必要はない。
- AUTO_FIX 後の Codex-only thread resolve は、commit + push の後に `resolve_codex_threads.py` だけが `resolveReviewThread` を呼ぶ。返信しない。各 mutation の直前に `headRefOid` を再取得し、対象 thread を再取得して comments_complete と参加者が引き続き Codex-only であることを確認する。thread 再取得の後と各 mutation の直前にも `headRefOid` を再確認する。不一致なら fail closed する。
- IGNORE_WITH_REASON の Codex-only 返信と resolve は `ignore_codex_threads.py` だけが `addPullRequestReviewThreadReply` / `updatePullRequestReviewComment` / `resolveReviewThread` を呼ぶ。同一 thread と同一 fingerprint の既存 helper 返信は更新して current HEAD に再bindし、新しい返信を増やさない。各 mutation の直前に `headRefOid` と対象 thread の参加者を再検証する。thread 再取得の後と各 mutation の直前にも `headRefOid` を再確認する。不一致なら fail closed する。
- 人間 thread の resolve、人間 / CodeRabbit 等への自動返信、review 提出、任意 GraphQL mutation は禁止のまま。ASK_HUMAN の指摘は GitHub 上で反論・resolve しない。
- launcher は `--retry-failed-now` を拒否する。`--retry-f` や `--retry-failed-n` など vendor argparse の短縮形も拒否する。vendor は `retry_failed_checks` を出しても flaky/unrelated 分類を検証せず failed runs を rerun するため。分類を機械的に確認できるまで retry mode は使わない。
- Agent が直接 `gh run rerun` すること、`gh workflow run` による任意 workflow の新規手動起動、それ以外の Actions 手動実行は禁止のまま。
- 人間 reviewer への返信、人間 review thread の resolve、PR merge はしない。
