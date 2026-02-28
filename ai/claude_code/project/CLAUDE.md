# Project Intelligence Guidelines

グローバル原則を継承し、プロジェクト固有の指示を優先する。

<project_context>

- 概要: README.md
- アーキテクチャ: directorystructure.md
- 技術スタック: technologystack.md

</project_context>

<development_commands>

## [開発・テスト・検証コマンドをここに追記]

<!-- 例: npm run dev / npm test / node test.js -->

</development_commands>

<development_rules>

## 自律動作プロトコル

**自律実行の境界**:

- **自律OK**: 単一ファイル編集、新規ファイル生成、非破壊的な Read/Search/Task。
- **要確認**: 複数ファイルの破壊的 Edit、ファイル/ディレクトリ削除。
  - 隔離環境（`git worktree` 等）での一括作業は計画提示→一括承認で個別確認不要。
- **`--dangerously-skip-permissions` 時**: 機密アクセスと破壊的操作（削除/force push）は禁止。

**検証の義務**:

- 既存テストがあれば実行し結果を報告に含めよ。
- テストがなければ CLI 実行か一時スクリプトで検証せよ（一時ファイルは検証後に削除）。

**完了の定義**:

- [ ] 意図した変更が反映されている
- [ ] テストがパスしている（または自律検証済み）
- [ ] 関連ドキュメントが更新されている
- [ ] ユーザーに報告し確認を求めている

## 固有規約

- コードレビュー: AGENTS.md `## コードレビュー` に準拠
- セキュリティ: パイプ・リダイレクトによる Deny 回避を厳禁
- Terminal: `cd`/`pushd`/`popd` 不使用。絶対パスで指定せよ。

</development_rules>
