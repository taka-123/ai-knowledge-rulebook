---
name: commit-message-suggester
description: |
  Use when: コミットすべきタイミングと判断したとき、またはユーザーが明示的にコミットメッセージを求めたとき。`<prefix>: <日本語1行>` 形式で提示する。
  When NOT to use: コミット対象の差分が無いとき。既存コミットの書き換え（git commit --amend）が目的のとき。
  Trigger Keywords: [コミットメッセージ, commit message, コミット案, commit-message-suggester]
---

# commit-message-suggester

固定フォーマット `<prefix>: <日本語1行>` でコミットメッセージを提示する。

## フォーマット

| prefix  | 用途                                                   |
| ------- | ------------------------------------------------------ |
| `feat`  | 新機能・新規ファイル/スキル/エージェント追加           |
| `fix`   | バグ修正・不具合対応                                   |
| `chore` | 設定整理・依存更新・リファクタリング・ドキュメント更新 |

ルール:

- `<prefix>` の直後は **半角コロン + 半角スペース 1 個**。
- 日本語 1 行、改行・句点（`。`）禁止。

## 振る舞い

- 複数意図が混在する差分は、分割案と各メッセージを別個に提示する。
- prefix 選定で迷う場合は候補 2 つを根拠 1 文付きで併記する。
- Backlog 起票時のブランチ名は対象外（→ `backlog-issue-planner`）。

## Examples

- `feat: commit-message-suggester スキルを追加`
- `fix: 認証ハンドラで null セッションを参照しないよう修正`
- `chore: グローバル Claude Code のスキル構成を精選`

複数意図混在時:

```text
複数意図が混ざっています。以下に分割を推奨します。
1. fix: 既存ハンドラの null 参照を修正
2. feat: 通知メール送信機能を追加
```
