---
name: backlog-intake-planner
description: "Use when 薄い・曖昧な要求を requirements.md / implementation-plan.md / implementation-handoff.md に起こしたいとき。AskUserQuestion で壁打ちしながら起票。When NOT to use: 起票済みで体裁のみ、実装そのもの、横断 Change order のみ。Trigger Keywords: [要求整理, 起票, 要件定義, 実装計画, チケット作成, backlog-intake-planner]."
---

# backlog-intake-planner

薄い・曖昧な要求を、Backlog 本文として貼る `requirements.md`（要件・受け入れ条件の正本）と、実装補助資料に起こす。
要求の明確化から要件整理・実装計画までを、軽くも深くも、段階的に進める。

正本は **Backlog 本文 ＝ `requirements.md`** のみ。`implementation-plan.md` / `implementation-handoff.md` / `README.md` は実装補助資料であり、PR レビューの判定基準にはしない。

手順・生成物・雛形・実装着手可否チェックの正本は本ファイルと Skill 内 `docs/`。二重定義しない。

## 起動

- Skill 添付、または `/backlog-intake-planner`（新規チャット推奨）
- 起票と実装は**別チャット**に分ける

## 生成物

| ファイル                    | 位置づけ                                 | いつ                                                          |
| --------------------------- | ---------------------------------------- | ------------------------------------------------------------- |
| `requirements.md`           | **正本**。Backlog 本文にそのまま貼る     | 常に（軽量は前半中心。深掘りで後半を埋める）                  |
| `implementation-plan.md`    | 実装補助資料（実装方針・順序・検証観点） | 深掘り時のみ（実装着手可否が**不可**なら生成しない）          |
| `implementation-handoff.md` | 実装補助資料（AI 実装開始用プロンプト）  | 深掘り完了かつ実装着手可否が**可 / 条件付き可**のときのみ     |
| `README.md`                 | Backlog 添付 ZIP の説明書                | `implementation-plan.md` / `implementation-handoff.md` 生成時 |

- 配置: `.work/backlog/BUSSW-AI/{requirements,implementation-plan,implementation-handoff,README}.md`（採番後 `BUSSW-XXXX`。plan / handoff / README は深掘り完了時のみ）
- ZIP 想定: `BUSSW-XXXX-implementation-support.zip` に `README.md` / `implementation-plan.md` / `implementation-handoff.md` を同梱（`requirements.md` は Backlog 本文が正本のため原則不要）
- 雛形・Backlog 記法: `docs/template-guide.md` / handoff・README: `docs/handoff-prompt-guide.md` / 実装着手可否: `docs/definition-of-ready.md`

## モード

- **軽量（既定）**: `requirements.md` の前半（概要・完成イメージ・やらないこと・前提・確認したいこと）を最大5問・平易な質問で埋め、Draft 起票する。
- **深掘り**: `requirements.md` の後半（要件・受け入れ条件・DB変更・レビュー観点）と `implementation-plan.md` を、技術質問も使って埋める。要件は「要件1 / 要件2」と番号を振り、受け入れ条件から対応付ける。書き方は下記の品質基準と `docs/template-guide.md` に従う。実装着手可否が**可 / 条件付き可**なら `implementation-handoff.md` も生成する。
- **モードの選び方**: 既定は軽量。ユーザーが起動時に「設計まで」「実装計画も」「深掘りして」等と言えば最初から深掘り。指定がなければ軽量で進め、**軽量の起票が終わった最後に深掘り要否を必ず尋ねる**（進め方 10）。**不可**なら深掘りを提案しない。勝手に深掘りを始めない／勝手に省略しない。
- SE・営業サポート: 深掘り **n** で requirements Draft のみでも可
- 実装者: 深掘り **y** → plan + handoff → 別チャットで実装

## 受け入れ条件の品質基準

深掘りの受け入れ条件は、**課題の形に応じた完成度**を目指す。横断チケットの参考例は `.work/backlog/BUSSW-4099/requirements.md`（雛形・例は `docs/template-guide.md`）。

| 課題の形                       | 書き方                                                                                                  |
| ------------------------------ | ------------------------------------------------------------------------------------------------------- |
| 単一 repo・単一画面            | 小見出し省略可。`#n [repo] [要件x]` のフラット列で足りる                                                |
| 単一 repo・複数導線            | 期待結果が同じなら 1 項目に `導線A` / `導線B`。期待結果が違えば項目を分ける。`または` で1文にまとめない |
| 設定 repo → 利用 repo          | 設定・利用を分け、横断効果は `[結合確認]` で別項目化                                                    |
| フロント + API（scr + scp 等） | フロント/API 単体ではなく **結合確認** セクションを正とする                                             |
| 例外・バイパス                 | `完成イメージ` の **例外** と、通常/例外で受け入れ条件を分ける                                          |

壁打ちでは、類似既存機能（年齢制限、権限、管理者バイパス等）を手がかりに導線の範囲と例外を先に固める。

各項目は **期待結果 1 文 → 導線 or 確認方法 → 必要なら補足/確認**。`#通番 [repo] [要件x]` は単一 repo でも省略しない。PR 前に動作確認できる項目だけを書き、再現不可は「検証環境で確認できない事項」へ。推測した導線は確定事項にせず「前提」または「確認したいこと」へ。導線の記法（`TOP` / `設定（歯車）` の明示、実 UI 文言・System_Names 既定表示名、取得元の確認）は `sc-ui-navigation-notation` skill に従う。

横断で読みづらくなったら `### [repo] — [機能エリア]` で小見出し（モード差・API 経路は直前に引用 1 行）。並び順方針を先頭に 1 行置き、同じ導線で新規項目と `[後方互換]` を連続配置する。設定追加系は未設定・既存データの `[後方互換]` を最低 1 項目入れる。

## implementation-plan.md の品質基準

深掘りで生成する補助資料。ステップ列だけの薄い計画にしない。

- §2 データモデル・§3 契約・§4 制御ルールで、実装中に迷う判断を先に確定する（横断・DB 変更・API 境界がある場合は必須。単純 fix は「なし」で可）
- §1.5 参考実装はファイルパス＋クラス/メソッドまで（「既存を参考」で止めない）
- §5 各ステップに対象・やること・完了確認の 3 点を付け、完了確認は `requirements.md` の受け入れ条件 #n に紐付ける

## 必須情報

起票には最低限「目的・背景」と「やりたいこと（機能・修正の内容）」が要る。揃うまで壁打ちで補い、それでも埋まらない分は推測で補って「前提」欄に明記する。

## 進め方

1. 要求文（読めるならリポジトリも）から、推測で埋められる前提を埋め、`requirements.md` の「前提（こちらで補った・要確認）」欄に**推測として明記**する。要求者の確定回答とは分ける。
2. 残る不明点のうち、仕様の核に効くものを選ぶ（この機能で合っているか／この機能は不要では／画面・UI はどうあるべきか）。
3. 軽量モードは、その中から**最大5問**を選択式で1回にまとめて聞く（質問のしかた参照）。平易な言葉で、コード・DB・技術には触れない。
4. 5問で埋まらなくても、またスキップされた質問があっても **Draft 起票して終える**。残り・スキップ分は「確認したいこと / 未確定」へ**宛先付き**で置く。
5. `docs/definition-of-ready.md` を参照して実装着手可否を判定し、結果を**チャットにのみ**提示する。**`implementation-plan.md` を書く前に必ず実施**する（起動時から深掘り指定でも同じ）。`requirements.md` には書かない。
6. ブランチ名を提案する（下記）。
7. 起票後の手順を案内する: ① Backlog で起票し採番（例 `BUSSW-1234`）を確認 ② フォルダ名を `BUSSW-AI` → `BUSSW-1234` にリネーム ③ ブランチの `XXXX` を採番に置換。`requirements.md` を Backlog に貼る。
8. スキップ・宛先付きの確認事項がある場合は、**宛先ごとの確認依頼文**を提示する（下記）。
9. 実装着手可否が**不可**のとき: 不足・確認事項を提示したうえで起票セッションを終了する。深掘り y/n は尋ねず、`implementation-plan.md` と `implementation-handoff.md` は生成しない。
10. 軽量のみで**可 / 条件付き可**のとき:「**さらに要件の詳細・実装計画（implementation-plan.md）まで深掘りしますか？**」と **y / n**。最初から深掘り指定があれば step 11 へ。
11. **深掘り**（明示 or y）: `requirements.md` 後半と `implementation-plan.md` を埋める（plan は §2〜4 確定後 §5）。品質基準 2 節と `docs/template-guide.md` に従う。類似既存機能の導線をコードベースまたは利用者に確認し、導線は実 UI 表記で書く。完了後 step 5 を**再判定**し、チャットに提示する。
12. 深掘り完了 + **可 / 条件付き可**: `implementation-handoff.md` と Backlog 添付 ZIP 用の `README.md` を生成し、チャットに handoff のコピペ用プロンプトを提示する（`docs/handoff-prompt-guide.md`）。
13. handoff の詳細整形が必要なら `/prompt-evolution` を案内する（任意）。

## 質問のしかた

- **AskUserQuestion が使える環境**: 選択式 UI で提示し、回答を待つ。
- **使えない環境**（Codex / Windsurf 等）: 下記フォーマットで**改行付き**に出す。1行に詰めない。
- 軽量は1回**最大5問**。各問 **3〜5 選択肢**（A/B/C…、最後は「その他」）。**スキップ選択肢**を必ず入れる。スキップ分は「確認したいこと」へ（確定にしない）。

改行ルール（壁打ち・確認依頼文の共通）: 前置き・締めは1文1行／`Qn.` 前後に空行／選択肢は1行1つ／質問間に空行／`Q1. A) xxx B) yyy` のインライン列挙は禁止。

例（壁打ち・本文）:

```markdown
## 確認事項（1回目・最大5問）

**Q1.** [平易な言葉の質問]

A) [選択肢]
B) [選択肢]
C) わからない／営業・サポート・顧客に確認が必要
D) その他（自由記述）
```

## 確認依頼文の提示

起票の最後に、スキップ・宛先付きの確認事項を**営業・サポート・顧客へ送るコピペ文**として提示する（壁打ち用ではない）。

- 宛先ごと1つのフェンス付きコードブロック。改行ルールは上記「質問のしかた」に同じ。
- 非エンジニア向けの平易な言葉。技術用語・コード・ファイル名は入れない。
- 各質問は A/B/C 選択式（最大5、最後は「その他」）。構成: 前置き → 質問 → 回答のお願い。

```
[機能名]の件で、確認させてください。
記号（A / B / C…）でお答えいただけると幸いです。

Q1. [平易な言葉の質問]
　　A) [選択肢]
　　B) [選択肢]
　　C) その他（ご記入ください）

Q2. [平易な言葉の質問]
　　A) [選択肢]
　　B) その他（ご記入ください）

お手数おかけしますが、よろしくお願いいたします。
```

## ブランチ名

- `<feat|fix|chore|refactor>/BUSSW-XXXX-<英語 kebab-case・10語以内>`
  - `feat`=新機能 / `fix`=修正 / `chore`=整備 / `refactor`=リファクタリング。
  - `XXXX` は採番後に置き換える（ユーザーからの明示がない場合、生成時は埋めない）。

## ルール（必守）

- `requirements.md` は **Backlog にそのまま貼れる内容だけ**を書く。実装着手可否の判定詳細・AI 向けメタ情報・HTML 作業用コメントは載せない。記法は `docs/template-guide.md` の「Backlog 記法」節。
- `requirements.md` に **ローカルパス・作業ディレクトリ・他ファイルへの相対リンクを書かない**（例: `.work/backlog/...`、`docs/foo.md`、`[text](../bar.md)`）。Backlog 上では開けず「何の話か」が分からなくなる。根拠資料は「別添PDF」「別添の調査資料」など添付物の呼び方にするか、公開URL / Backlog チケット URL だけにする。ローカルの詳細メモは `implementation-plan.md` や作業用 `docs/` 側へ置く。
- 受け入れ条件・`implementation-plan.md` の書き方の詳細は、上記**品質基準 2 節**と `docs/template-guide.md` に従う（本節で再掲しない）。
- 推測は必ず「前提」欄に置き、確定事項として書かない。必須情報が欠けたまま黙って確定要件として生成しない。
- 軽量モードでコード・DB・技術選定の質問をしない／5問を超えない。
- `implementation-plan.md` は**実装補助資料**であり正本ではない。PR レビューの判定基準は Backlog 本文 / `requirements.md` の受け入れ条件。
- `.work/backlog/BUSSW-AI/` 以外に生成しない。
- 実装着手可否が**不可**のときは `implementation-plan.md` / `implementation-handoff.md` / `README.md` を生成しない（不足整理・確認依頼文の提示までは行う）。
- 横断 Change order・implementer 委任は `planner` / implementer 系の範囲（本 Skill は起票のみ）

## Examples

- 「請求の画面で、金額をもっと見やすくしてほしい」（軽量）→ 誰の画面か／変更か追加か／何に困っているか等を最大5問で確認し、`requirements.md` 前半を埋めて Draft 起票。推測は「前提」、未確定は「確認したいこと」へ。ブランチ案 `feat/BUSSW-XXXX-highlight-invoice-total`。
- 上記の起票後「要件と計画まで詰めて着手したい」（深掘り）→ 品質基準と `docs/template-guide.md` に沿って `requirements.md` 後半と `implementation-plan.md` を埋める。
- 「予約枠に性別制限を追加し振替・予約・体験へ横展開」（深掘り・横断）→ 参考 `.work/backlog/BUSSW-4099/requirements.md`。
- 「決済処理で NullPointerException が出る不具合を修正」（情報十分）→ 壁打ちは1〜2問に絞ってすぐ Draft 起票。ブランチ案 `fix/BUSSW-XXXX-fix-payment-null-pointer`。
- 「決済失敗時に施設側から失敗者へ案内メールを自動送付」（深掘り・横断）→ 影響リポジトリ `sc` / `sc_ddl` / `ScSbPaymentTransfer` を `影響範囲・レビュー観点` に列挙。受け入れ条件は `#1 [sc] [要件1] ...` のように `通番 + 対象リポジトリ + 要件番号` で記載し、横断レビュー時にどの repo の条件かを即特定できるようにする。サンドボックスで再現できない type_code 別経路・通信エラー・確定要求 API エラー等は「検証環境で確認できない事項」セクションに分離し、チェック項目化はしない（コードレビューと本番カナリアで担保）。
