---
name: source-date-compliance
description: Source citation compliance for 出典URL, 取得日, clips, 引用整合 tasks. Use when documentation or notes must include source links and retrieval dates.
---

# Source Date Compliance

## 手順

1. `clips/` と `notes/` の対象 Markdown を確認する。
2. 出典 URL と取得日の有無をチェックする。
3. 欠落項目をテンプレート形式で補完提案する。
4. 技術仕様の記述は事実と推測を分離して整理する。
5. 反映後に Markdown の構文とリンク形式を再確認する。

## Safety

- 認証情報や機密を含む URL は取り扱わない。
- `auth` `login` `password` `secret` `token` `admin` を含む危険 URL はアクセスしない。
- `push` `deploy` `migrate` `infra` `db` 系操作は提案止まりにし、承認後に実行する。

## 継承

- `tech-researcher` の出典厳格性と `task-reviewer` の完遂確認を継承する。
