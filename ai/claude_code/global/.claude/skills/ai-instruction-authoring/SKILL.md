---
name: ai-instruction-authoring
description: |
  Use proactively when editing any Skill (**/SKILL.md), Agent definition
  (.claude/agents/, .cursor/agents/, .codex/agents/), AGENTS.md, CLAUDE.md, or
  tool rules (.cursor/rules/, *.mdc). Also when the user explicitly asks to create
  or refine AI instructions.
  When NOT to use: general human docs as the main task (document-authoring);
  app code or tests only.
  Trigger Keywords: [ai-instruction-authoring, SKILL.md, Agent, AGENTS.md, CLAUDE.md, rules, mdc, スキル作成, エージェント作成, AI指示, 指示文書]
---

# ai-instruction-authoring

## 目的

AI 向け指示（Skill、Agent、ルール、`CLAUDE.md`、`AGENTS.md` など）の書き方。文章の短さ・一貫性・見直しタイミングは `document-authoring` に従い、本 Skill は **AI 指示固有の決めごと**だけを扱う。一般の共有ドキュメントと両方該当するなら、`document-authoring` も Read する。

## 書いてよいこと

- コードやリポジトリを読んでも分からない決めごと（パス規約、起動条件、出力形式、この環境だけの好み）
- 書かないと、有能なモデルでもついやりがちな失敗を止める文（実際に起きうる失敗が言えるもの）
- 調査や編集の範囲を絞る手がかり（どこを見るか。全体を闇雲に読ませないため）

## 書かないこと

- コードを読めばすぐ分かること
- 毎ターン意識しなくてよいこと（常時読込ファイルを太らせ、文脈を圧迫する）
- 言われなくても普通はやらないことの禁止、普通はやることの念押し
- 今回の会話で出ただけの例外を、恒久ルールにすること

## Skill / Agent の形式

- `Use when` / `When NOT to use` / `Trigger Keywords` など定型キーは英語。説明文は読みやすい日本語
- 上記 3 つは description に書き、本文で同じ説明を繰り返さない
- description の起動条件は次のどちらか（または併記）に寄せる:
  - 編集パスが明確 → `Use proactively when editing any file under <path> ...`
  - 明示依頼が主 → `Use when the user explicitly asks ...`
- 抽象条件（`when needed`、対象パスなし）は避ける
- 動きを直すときは、末尾に注意を足すのではなく、手順・判定・例をまとめて直す

## 例外

セキュリティや取り返しのつかない操作の注意は、当たり前でも残してよい。

## 運用憲法

- `AGENTS.md` と `CLAUDE.md` は平行憲法。同じ本質を各自に自己完結で書く。重複は健全。
- 重複を理由に片方を省略しない。レビューで「重複だからダメ」と指摘しない。
- 憲法・Skill・Agent に「憲法を読め / に従え」と書かない。毎ターン読む憲法本文に相手のファイル名も出さない。
- 共通の長文は第三ファイルへ切り出し、両方から参照する。一方→他方の委譲はしない。
