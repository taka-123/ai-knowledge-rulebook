# handoff-prompt-guide（実装依頼プロンプト ＋ ZIP 同梱 README）

深掘り完了後、新しい会話セッションで実装を始めるための **`implementation-handoff.md`** と、Backlog 添付 ZIP 用の **`README.md`** を出力する。
handoff は `prompt-evolution` の Contract Style をベースに **短版** に留める。詳細な整形が必要なら別途 `/prompt-evolution` を使う。

## 正本と優先順位（必読）

- **要件・受け入れ条件の正本は Backlog 本文 ＝ `requirements.md`**。
- `implementation-plan.md` / `implementation-handoff.md` / `README.md` は実装補助資料。
- 矛盾時の優先順位:
  1. Backlog 本文 / `requirements.md` の受け入れ条件
  2. `requirements.md` の対象範囲・対象外
  3. `implementation-plan.md`
  4. `implementation-handoff.md`
- PR レビューは Backlog 本文の受け入れ条件で判定する。`implementation-plan.md` との差分報告は求めない。

## 出力条件

- **出す**: 深掘り完了かつ実装着手可否が **可** または **条件付き可**（`implementation-handoff.md` と `README.md` をセットで生成）
- **出さない**: 軽量のみ / 実装着手可否 **不可** / `implementation-plan.md` 未生成

## 配置

- handoff: `.work/backlog/BUSSW-AI/implementation-handoff.md`（採番後は `BUSSW-XXXX` フォルダ）
- README: `.work/backlog/BUSSW-AI/README.md`（同上）
- ZIP 想定: `BUSSW-XXXX-implementation-support.zip` に `README.md` / `implementation-plan.md` / `implementation-handoff.md` を同梱（`requirements.md` は Backlog 本文が正本のため原則不要）
- チャット: handoff の「コピペ用プロンプト」節をコードブロックで再掲

## 書き方（handoff）

- 正本は **Backlog 本文 / `requirements.md`**。handoff は起動用の要約。矛盾時は正本を優先。
- パスは `# Context` に列挙する。**「ファイルを読んで」等の念押しは書かない**（@ 添付で足りる前提）。
- Goal / Constraints / Acceptance Criteria は **`requirements.md` と `implementation-plan.md` から抽出**する。推測で足さない。
- 実装着手可否が **条件付き可** のときは Constraints に「着手可能範囲」と「保留（実装しない）」を明示する。
- commit / PR / 本番デプロイは **明示依頼がない限り Constraints で禁止**。

## テンプレート（implementation-handoff.md）

```markdown
# 実装依頼（新セッション用）

> 正本: Backlog 本文 ＝ `.work/backlog/BUSSW-AI/requirements.md`
> 補助資料: `.work/backlog/BUSSW-AI/implementation-plan.md`（必要に応じて参照）
> 実装着手可否: [可 / 条件付き可] ／ ブランチ案: `[type]/BUSSW-XXXX-[slug]`

## 添付（@ 参照）

- `.work/backlog/BUSSW-AI/requirements.md`（正本）
- `.work/backlog/BUSSW-AI/implementation-plan.md`（補助）

## コピペ用プロンプト

（以下を新セッションに貼る）

---

# Goal

[1〜2文。チケットタイトル相当]

# Context

- 要件正本: `.work/backlog/BUSSW-AI/requirements.md`（Backlog 本文と同内容）
- 実装補助: `.work/backlog/BUSSW-AI/implementation-plan.md`（参考。必須ではない）
- 優先順位: 受け入れ条件 ＞ 対象範囲・対象外 ＞ implementation-plan ＞ 本プロンプト
- [影響リポジトリ・主要パス・関連原本パス]

# Constraints

- [編集してよい repo / パス]
- [触らないこと・スコープ外]
- [環境・権限・一時運用の制約]

# Acceptance Criteria

- [ ] [requirements.md の受け入れ条件から主要項目]

# Output Format

1. 変更ファイル一覧
2. 実装要点
3. ローカル確認手順（URL / コマンド）
4. 未検証・残リスク

# Verification Policy

- 受け入れ条件（requirements.md）を満たすか
- `implementation-plan.md` §5 / §6 は補助参照（差分報告は不要）

---

## 新セッション手順

1. 新規チャットを開く
2. 上記「添付」を @ 参照
3. 「コピペ用プロンプト」を貼って送信
```

## README.md テンプレート（ZIP 同梱用）

> 配置: `.work/backlog/BUSSW-AI/README.md`（採番後 `BUSSW-XXXX`）
> 目的: ZIP を受け取った実装者に、責任分界と進め方を1ページで伝える。

```markdown
# AI 実装補助資料

このZIPは、Backlog本文の要件をもとに実装を進めるための補助資料です。

## 正本

要件・受け入れ条件の正本は **Backlog本文** です。

`implementation-plan.md` と `implementation-handoff.md` は補助資料です。
PRレビューでは、これらの資料どおりに実装したかではなく、**Backlog本文の受け入れ条件を満たしているか**を確認します。

優先順位:

1. Backlog本文の受け入れ条件
2. Backlog本文の対象範囲・対象外
3. `implementation-plan.md`
4. `implementation-handoff.md`

## 含まれるファイル

* `implementation-plan.md`
  * 実装方針・実装順・検証観点の補助資料
* `implementation-handoff.md`
  * AI 実装開始用プロンプト

## 読む順番

1. Backlog 本文
2. `implementation-plan.md`
3. `implementation-handoff.md`

## 実装者の責任

実装者は、補助資料を必要に応じて参考にしつつ、最終的な成果物に責任を持ってください。

特に以下を確認してください。

* Backlog 本文の受け入れ条件を満たしていること
* 対象外の範囲を変更していないこと
* 危険領域を不用意に変更していないこと
* AI の出力をそのまま採用せず、既存実装・保守性・UI・影響範囲を確認していること
* 動作確認と検証結果を PR に記載していること
* 未確認事項を隠していないこと

## PR に記載すること

PR では以下を記載してください。

* 受け入れ条件ごとの確認結果
* 実行した検証
* 手動確認結果
* 未確認事項
* レビュアーに重点的に見てほしい箇所

`implementation-plan.md` との差分報告は不要です。
レビュー基準は Backlog 本文の受け入れ条件です。

## 不明点がある場合

要件・対象範囲・受け入れ条件に違和感や不足がある場合は、実装前に Backlog コメント等で確認してください。
```

## 品質チェック（出力前）

- [ ] 正本パスが実在するフォルダ名と一致している
- [ ] Acceptance Criteria が `requirements.md` と齟齬ない
- [ ] 「ファイルを読んでください」系の冗長文がない
- [ ] 実装着手可否 **不可** のときに `implementation-handoff.md` / `README.md` を生成していない
- [ ] handoff と README はセットで生成している（片方だけ出していない）
- [ ] README の正本表記が「Backlog 本文」になっている（`implementation-plan` を正本として書いていない）
