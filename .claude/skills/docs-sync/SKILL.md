---
name: docs-sync
description: リポジトリの変更後に README.md・directorystructure.md・technologystack.md が実態と一致しているか確認し、不整合があれば同期するスキル。キーワード「README」「directory」「structure」「tech stack」「ドキュメント同期」「構成変更」で自動検出。
user-invocable: true
allowed-tools: Read, Glob, Bash
disable-model-invocation: true
---

# Docs Sync

リポジトリの構成やスタックに変更があった際に、以下3つのドキュメントが実態と一致しているか確認し、不整合があれば最小限に同期する。

対象ドキュメント:

- `README.md`
- `directorystructure.md`
- `technologystack.md`

## 実行手順

1. 変更セット（追加・削除・変更されたディレクトリ・ファイル・スタック）を特定する。
2. 上記3ファイルを読み込み、変更セットと照合する。
3. 不整合があれば、確認済みの事実のみを最小限で反映する。推測による変更は行わない。
4. 編集後は `./format.sh check` を実行し結果を報告する。

## 判定ルール

- 確認済みの変更のみを反映する。推測は一切行わない。
- 既存のスタイルと一貫性を維持する。
- 変更は最小限に収める。

## 出力形式

```markdown
## Docs Sync 結果

- **対象ドキュメント**: [更新したファイル]
- **更新内容**: [何を・なぜ変更したか]
- **検証**: ./format.sh check の結果
```

## 制約

- 3つの対象ドキュメント以外を変更してはならない。
- 編集後の検証は必須。
