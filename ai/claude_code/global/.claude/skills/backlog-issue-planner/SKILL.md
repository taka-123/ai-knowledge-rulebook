---
name: backlog-issue-planner
description: |
  Use when: Backlogチケット起票に向けて、要件定義・実装計画・ブランチ名を一括で生成したい場合。情報が不足している場合は壁打ちで補完する。
  When NOT to use: 既にチケットが起票済みでドキュメント更新のみの場合。Backlog以外の課題管理ツールを使う場合。
  Trigger Keywords: [backlog起票, チケット作成, 要件定義, 実装計画, BUSSW, issue作成, backlog-issue-planner]
---

# backlog-issue-planner

Backlog 起票に必要な 3 ファイル（`backlog.md` / `requirements.md` / `design.md`）と
ブランチ名を、ユーザーの要求から段階的に生成する。

## 必要情報

| 項目                         | backlog.md (起票) | requirements / design |
| ---------------------------- | ----------------- | --------------------- |
| 目的・背景                   | ◎ 必須            | ◎ 必須                |
| 実装したい機能・修正内容     | ◎ 必須            | ◎ 必須                |
| 対象コンポーネント・スコープ | ○ ざっくり        | ○ 明確に              |
| スコープ外                   | ○ ざっくり        | ○ 明確に              |
| 受け入れ条件                 | ○ ざっくり        | ○ テスト可能な粒度    |
| DB 変更                      | ○ 有無のみ        | ○ スキーマ詳細        |
| 技術アプローチ・制約         | 不要              | ○ 必要                |

◎ が不足している場合は最大 3 つの質問でまとめて確認する。

## 出力先 & ブランチ命名

- ファイル配置: `.work/backlog/BUSSW-AI/{backlog,requirements,design}.md`
- ブランチ名: `<種別>/BUSSW-XXXX-<英語kebab-case>`（10 語以内）

| 種別    | 用途                             |
| ------- | -------------------------------- |
| `feat`  | 新機能・新規開発                 |
| `fix`   | バグ修正・不具合対応             |
| `chore` | 設定変更・整備・リファクタリング |

## Procedure

1. **起票情報を収集**: ◎ 項目が揃うまで壁打ち。

2. **`backlog.md` 生成 + ブランチ名提案**:
   - `mkdir -p .work/backlog/BUSSW-AI/`
   - `docs/template-guide.md` の「backlog.md テンプレート」を Read。
   - `backlog-markdown-formatting` スキルの変換規則で `backlog.md` を生成。非エンジニアも読む想定で平易に。
   - 「この内容で Backlog に起票できます。`requirements.md` と `design.md` を続けますか？」と問う。

3. **詳細情報を追加収集**（続行希望時）: 受け入れ条件詳細・DB スキーマ・技術アプローチ・API 設計・エッジケース。

4. **`requirements.md` + `design.md` 生成**:
   - 両ファイルは標準 GFM（`-` 箇条書き・ATX 見出し）。
   - `docs/template-guide.md` の対応テンプレートを Read。
   - `design.md` は **アーキテクチャ方針 / 影響リポジトリ / DB / API / 制御ルール / 実装推奨順** を含む。具体的なファイルパスは書かない（実装時に決める）。

5. **起票後の手順を案内**:

   > 1. Backlog でチケットを起票し採番（例: `BUSSW-1234`）を確認する。
   > 2. フォルダ名を `.work/backlog/BUSSW-AI/` → `.work/backlog/BUSSW-1234/` に変更する。
   > 3. ブランチ名の `XXXX` を採番に書き換える（例: `feat/BUSSW-1234-add-user-auth`）。

## ルール（必守）

- `.work/backlog/BUSSW-AI/` 以外の場所には生成しない。
- ブランチ名の `XXXX` を実番号で埋めない（採番は起票後）。
- `backlog-markdown-formatting` を経由せず独自記法で `backlog.md` を生成しない。
- 情報不足時に推測でファイルを生成しない（壁打ちで補完する）。

## Examples

- 「ユーザー認証機能を追加したい（メール・パスワードログイン）」→ 壁打ち後、3 ファイル生成、ブランチ案 `feat/BUSSW-XXXX-add-email-password-authentication`。
- 「決済処理で NullPointerException が出る不具合を修正」→ 情報十分なので壁打ちなし、3 ファイル生成、ブランチ案 `fix/BUSSW-XXXX-fix-payment-null-pointer-exception`。
