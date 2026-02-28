---
name: backlog-issue-planner
description: |
  Use when: Backlogチケット起票に向けて、要件定義・実装計画・ブランチ名を一括で生成したい場合。情報が不足している場合は壁打ちで補完する。
  When NOT to use: 既にチケットが起票済みでドキュメント更新のみの場合。Backlog以外の課題管理ツールを使う場合。
  Trigger Keywords: [backlog起票, チケット作成, 要件定義, 実装計画, BUSSW, issue作成, backlog-issue-planner]
---

# backlog-issue-planner

Backlogチケット起票に必要な3ファイル（`backlog.md` / `requirements.md` / `implementation-plan.md`）と
ブランチ名を、ユーザーの要求から生成する。

## When to use

- Backlogチケットを起票する前に、要件・実装計画を整理したい場合。
- 要求から `backlog.md`・`requirements.md`・`implementation-plan.md` を一括生成したい場合。

## When NOT to use

- 既にチケットが起票済みで、ドキュメント更新のみ必要な場合。
- Backlog以外のツール（GitHub Issues、Jiraなど）向けのチケットを作る場合。
- Markdown整形だけが目的の場合（`backlog-markdown-formatting` を使うこと）。

## Trigger Keywords

- backlog起票
- チケット作成
- 要件定義
- 実装計画
- BUSSW
- issue作成
- backlog-issue-planner

## Procedure

> このスキルは **2段階** で動作する。
> 起票に必要な情報が揃ったら `backlog.md` を先に生成し、その後に詳細を詰めて `requirements.md` + `design.md` を生成する。

---

### フェーズ 1: 起票情報の収集（backlog.md のしきい値）

1. ユーザーの要求から以下を抽出する:

   | 項目                         | 起票しきい値 | requirements/design しきい値 |
   | ---------------------------- | ------------ | ----------------------------- |
   | 目的・背景（なぜ必要か）     | ◎ 必須       | ◎ 必須                        |
   | 実装したい機能・修正内容     | ◎ 必須       | ◎ 必須                        |
   | 対象コンポーネント・スコープ | ○ ざっくりでよい | ○ 明確に                  |
   | スコープ外（やらないこと）   | ○ ざっくりでよい | ○ 明確に                  |
   | 受け入れ条件                 | ○ ざっくりでよい | ○ テスト可能な粒度で        |
   | DB変更の有無                 | ○ 有無だけでよい | ○ 詳細スキーマまで         |
   | 技術アプローチ・制約         | 不要         | ○ 必要                        |
   | 優先度・期限                 | △ あれば     | △ あれば                      |

2. ◎ 項目が不足している場合は、**最大3つ**の質問をまとめて確認し、回答を待つ。
3. **起票しきい値**（◎ + スコープ・完了条件がざっくりでも揃っている）を満たしたら → フェーズ 2 へ進む。

---

### フェーズ 2: backlog.md の生成・Backlog 起票案内

4. `docs/template-guide.md` を Read で参照し、ブランチ種別・命名規則を確認する。
5. ブランチ種別を判定し、提案する:

   | 種別                             | 使いどころ                       |
   | -------------------------------- | -------------------------------- |
   | `feat/BUSSW-XXXX-<description>`  | 新機能・新規開発                 |
   | `fix/BUSSW-XXXX-<description>`   | バグ修正・不具合対応             |
   | `chore/BUSSW-XXXX-<description>` | 設定変更・整備・リファクタリング |

   `<description>` は英語のkebab-caseで10語以内に要約する。

6. 出力先ディレクトリ `.work/backlog/BUSSW-AI/` が存在しない場合は `mkdir -p` で作成する。
7. `../backlog-markdown-formatting/docs/transform-rules.md` を Read で参照し、変換規則を取得する。
   その規則に従って `backlog.md` を生成する:
   - テンプレートは `docs/template-guide.md` の「backlog.md テンプレート」を使用する。
   - 非エンジニアも読む想定で平易な表現にする。コードレベルの詳細は書かない。
   - DB変更がある場合のみ「DB変更」セクションを追加する（詳細が未確定でも変更有無が分かる粒度でよい）。
8. `backlog.md` を生成したら以下を提示する:
   - 生成した `backlog.md` のパス
   - 提案ブランチ名
   - 「**この内容で Backlog に起票できます。** `requirements.md` と `design.md` の作成を続けますか？」

---

### フェーズ 3: 詳細情報の収集（requirements/design のしきい値）

9. ユーザーが続行を希望した場合、不足している詳細情報を追加確認する:
   - 受け入れ条件の詳細（テスト可能な粒度）
   - DB 詳細スキーマ（カラム名・型・NULL 制約・説明）
   - 技術アプローチ・影響リポジトリ
   - API 設計・外部サービス連携
   - ビジネスロジック・制御ルール・エッジケース
10. 詳細情報が充分に揃ったら → フェーズ 4 へ進む。

---

### フェーズ 4: requirements.md + design.md の生成

11. `requirements.md` を生成する:
    - 標準GFM（`-` 箇条書き・ATX見出し）で記述する。
    - テンプレートは `docs/template-guide.md` の「requirements.md テンプレート」を使用する。
12. `design.md` を生成する:
    - 標準GFM（`-` 箇条書き・ATX見出し）で記述する。
    - テンプレートは `docs/template-guide.md` の「design.md テンプレート」を使用する。
    - **書くこと**: アーキテクチャ方針・影響リポジトリ・DB スキーマ詳細・API 設計・制御ルール・実装推奨順。
    - **書かないこと**: 具体的なファイルパスやコード変更（AI がコードを探索して決める）。

### フェーズ 5: 完了案内

13. 生成した全ファイルの一覧を提示する。
14. 以下の案内を必ず添える:

    > **Backlog起票後の手順**
    >
    > 1. Backlogでチケットを起票し、採番（例: `BUSSW-1234`）を確認する。
    > 2. フォルダ名を `.work/backlog/BUSSW-AI/` から `.work/backlog/BUSSW-1234/` に変更する。
    > 3. ブランチ名の `XXXX` を採番した番号に書き換える（例: `feat/BUSSW-1234-add-user-auth`）。

## Output Contract

| 成果物                   | 配置先                                          | 記法                                              |
| ------------------------ | ----------------------------------------------- | ------------------------------------------------- |
| `backlog.md`             | `.work/backlog/BUSSW-AI/backlog.md`             | `backlog-markdown-formatting` 準拠                |
| `requirements.md`        | `.work/backlog/BUSSW-AI/requirements.md`        | 標準GFM                                           |
| `design.md`              | `.work/backlog/BUSSW-AI/design.md`              | 標準GFM                                           |
| ブランチ名提案           | 出力テキスト                                    | ``feat`or`fix`or`chore`/BUSSW-XXXX-<description>` |

### NG例

❌ 情報が不足しているのに壁打ちせず、推測だけでファイルを生成する。

❌ `../backlog-markdown-formatting/docs/transform-rules.md` を Read せずに `backlog.md` を生成する（規則の重複管理になる）。

❌ ブランチ名の `XXXX` をリアルな番号で埋める（採番はBacklog起票後のため）。

❌ 起票後のフォルダ名変更・ブランチ名変更の案内を省略する。

❌ `.work/backlog/BUSSW-AI/` 以外の場所にファイルを生成する。

## Examples

### Example 1

Input: 「ユーザー認証機能を追加したい。メール・パスワードでログインできるようにする」
Output:
壁打ち（受け入れ条件とスコープ外を確認）→ backlog.md / requirements.md / design.md を生成 →
ブランチ名: `feat/BUSSW-XXXX-add-email-password-authentication` を提案。

### Example 2

Input: 「決済処理でNullPointerExceptionが発生する不具合を修正したい」
Output:
壁打ちなし（情報が充分）→ backlog.md / requirements.md / design.md を生成 →
ブランチ名: `fix/BUSSW-XXXX-fix-payment-null-pointer-exception` を提案。

### Example 3

Input: 「CIのLintチェックを追加して、マージ前に自動確認できるようにしたい」
Output:
壁打ち（対象ブランチ・ツール確認）→ backlog.md / requirements.md / design.md を生成 →
ブランチ名: `chore/BUSSW-XXXX-add-ci-lint-check` を提案。
