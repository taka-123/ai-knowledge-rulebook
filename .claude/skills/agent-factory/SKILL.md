---
name: agent-factory
description: Use when new agents or skills must be designed with non-overlapping responsibilities, clear triggers, and validation gates; When NOT to use: single-file bug fixes without routing impact; Trigger Keywords: agent, skill, router, workflow, trigger.
---

# agent-factory

## When to use

- 新規エージェントやスキルを設計する。
- 役割重複を避けたルーティング体系を作る。

## When NOT to use

- 単発の軽微修正。
- 既存配線を変えない依頼。

## Trigger Keywords

- agent
- skill
- router
- workflow
- trigger

## Examples

### Example 1

Input: ドキュメント監査専用エージェントを追加したい。
Output: 目的、入力、禁止事項、完了条件を定義したエージェント仕様を作る。

### Example 2

Input: 既存 skill の重複を解消して。
Output: 重複領域を表で可視化し、統合先と削除候補を最小差分で提案する。

### Example 3

Input: ルーターの発火精度を上げる trigger 設計をして。
Output: キーワード群を衝突回避しつつ、優先順位付きで再定義する。
