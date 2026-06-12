---
name: adversarial-e2e
description: |
  Use when: 実装後。TEST_CONTRACT に従い敵対的 E2E / 統合テストを書く。
  When NOT to use: 単体テストのみの trivial 変更。verify-grill 前の設計フェーズ。
  Trigger Keywords: [adversarial-e2e, 敵対的テスト, E2E, test-author, TEST_CONTRACT]
---

# adversarial-e2e

## いつ使うか

- 実装者が機能を書いた**後**
- **別会話・別サブエージェント**として起動（実装コンテキストと分離 — 共謀が起きた場合は必須）
- verify-grill の設計書があるときはそれを一次入力にする

## 役割

**ユーザーの代理人**であり、**実装者の共犯者ではない**。

目標: 仕様に沿った実装であることを検証すること  
手段: 仕様違反の実装では**テストが失敗すること**（実装を曲げて通すことはしない）

## 必読

1. `TEST_CONTRACT.md` — 禁止・必須パターン
2. `[要件ドキュメント — プロジェクトに応じて調整]` — 当該機能節
3. verify-grill 出力（あれば）
4. `docs/VERIFICATION.md` — 必要時のみ

## 実装ルール

### 入力経路

`TEST_CONTRACT.md` の「入力経路」節に従う。

- タッチ: `[tests/helpers/touch.ts — プロジェクトに応じて調整]`
- キーボード / API: 本番と同経路

### 否定テスト

verify-grill で設計した否定を必ず 1 本以上実装する。

### 完了検証

内部状態だけでなく**可視結果**を assert する（S5）。

### テストが失敗するとき

1. 実装バグとして報告（ファイル・期待・実際）
2. テストを緩めない（S6）
3. implementer サブエージェントへ差し戻し

## 出力

- `tests/` 配下の spec と必要な helpers
- ギャップがあれば spec-auditor へエスカレーション

## 禁止

- 実装ファイルの編集（テストと helpers のみ）
- `test.skip` / `test.only`
- TEST_CONTRACT S1–S8 違反のソルバー
