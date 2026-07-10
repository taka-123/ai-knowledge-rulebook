---
name: ai-instruction-authoring
description: |
  Use when: Skill / Agent / ルール / CLAUDE.md・AGENTS.md など、AI 向け指示を作成・編集するとき。何を書くか・常時読込に載せないか・形式を整えるとき。
  When NOT to use: 要件・計画・設計など一般ドキュメントが主目的のとき（document-authoring）。アプリコードの実装修正のみのとき。
  Trigger Keywords: [スキル作成, エージェント作成, 指示文書, CLAUDE.md, AGENTS.md, ルール作成, AI指示, ai-instruction-authoring]
---

# ai-instruction-authoring

AI 向け指示（Skill、Agent、ルール、`CLAUDE.md`、`AGENTS.md` など）の書き方。
文章の短さ・一貫性・見直しタイミングは `document-authoring` に従い、本 Skill は **AI 指示固有の決めごと**だけを扱う。

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
- 動きを直すときは、末尾に注意を足すのではなく、手順・判定・例をまとめて直す

## 例外

セキュリティや取り返しのつかない操作の注意は、当たり前でも残してよい。
