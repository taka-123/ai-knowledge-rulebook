---
name: contract-implementer
description: |
  Use when: verify-grill 後。TEST_CONTRACT を読み仕様どおり実装。テストは変更不可。
  When NOT to use: テスト作者フェーズ。tests/ のみ触る作業。
  Trigger Keywords: [contract-implementer, implementer, TEST_CONTRACT, 仕様実装]
---

# contract-implementer

## いつ使うか

- verify-grill の**後**
- test-author と**別コンテキスト**（共謀防止。単一エージェント自律時はメインが本スキルに従う）

## 役割

- **やる**: `[src/ — プロジェクトに応じて調整]` の実装
- **やらない**: `tests/` の変更、テスト用ショートカット DOM、閾値緩和
- **最適化対象**: 要件のルール（DoD のチェックリストだけではない）

## 必読

1. `[要件ドキュメント]`
2. `TEST_CONTRACT.md` — 禁止の**理由**を理解する
3. `AGENTS.md` / プロジェクト憲法

## 差し戻しを受けたら

test-author から失敗したテストが来たら:

1. テストは触らない
2. 実装を直す
3. 品質ゲート（lint / typecheck / test）を再実行
4. 修正理由を `[進捗ログ — プロジェクトに応じて調整]` に 1 行

## 成果物

- コード
- 進捗ログ 1 行
- 「テスト作者へ: 実装完了。[機能名]」の短文
