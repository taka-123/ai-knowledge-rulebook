# Project Intelligence Guidelines

グローバル原則を継承し、プロジェクト固有の指示を優先する。

<project_context>

<!-- テンプレート注記: `README.md` / `directorystructure.md` / `technologystack.md` の3項目のみ使用。不存在の行を削除し、3項目すべて不存在ならブロックごと削除 -->

- 概要: `README.md`
- アーキテクチャ: `directorystructure.md`
- 技術スタック: `technologystack.md`

</project_context>

<development_commands>

## 開発コマンド

<!-- テンプレート注記: 無理に記載しない。毎ターン有益な開発コマンドのみ記載 -->

</development_commands>

<development_rules>

## 実行プロトコル（Claude Code）

- 計画先行: 複数ファイル変更は `Plan → 実装 → Verify` の順で進める。
- 自律OK: 単一ファイル編集、新規ファイル生成、非破壊の Read/Search/Task。
- 要確認: 複数ファイルの破壊的 Edit、復元困難な削除、タスク範囲外の変更。
- 委任: 重い探索や試行錯誤は Subagents へ委任する。
- 検証: 既存テストを優先実行。なければ CLI 等で代替検証し、未検証範囲を明示する。
- 完了報告: 変更概要、検証結果、未実施事項（ある場合）を含める。
- レビュー: AGENTS.md の `レビュー基準` に準拠する。
- セキュリティ: パイプ/リダイレクトで権限制約を回避しない。
- Terminal: 絶対パスで指定する（`cd`/`pushd`/`popd` 不使用）。

</development_rules>
