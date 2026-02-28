# Project Intelligence Guidelines

Note: グローバル原則を継承し、プロジェクト固有の指示を優先する。

<project_context>

- 概要: README.md
- アーキテクチャ: directorystructure.md
- 技術スタック: technologystack.md

</project_context>

<development_commands>

## 開発・テスト・検証コマンド

<!-- npm run dev / npm test / node test.js 等を追記 -->

</development_commands>

<development_rules>

## 自律動作プロトコル

**1. 実行境界**:

- **自律 OK**: 単一ファイルの編集・生成、非破壊的な Read/Search/Task。
- **要確認**: 複数ファイルにまたがる破壊的な Edit、ファイル/ディレクトリの削除。
  - 例外: `git worktree` 等の隔離環境下では計画提示・一括承認後に個別確認不要。
- **`--dangerously-skip-permissions` 時**: 機密情報アクセスと破壊的操作（削除/force push）は禁止。

**2. 検証の義務化**:

- 既存テストは必ず実行し、結果を報告に含めること。
- テストがない場合、CLI 実行またはワンライナーで検証せよ。一時ファイルは検証後即削除。

**3. 完了の定義**:

- [ ] 意図した変更が反映されている
- [ ] テストがパスしている（または自律検証済み）
- [ ] 関連ドキュメント（README等）が更新されている
- [ ] 変更内容をユーザーに報告し確認を求めている

---

## 固有規約

- コードレビュー: AGENTS.md `## コードレビュー` に準拠
- セキュリティ: パイプ・リダイレクトを用いた Deny 回避を厳禁。
- **Terminal**: `cd` / `pushd` / `popd` は使用しない。`working_directory` または絶対パスで指定する。

</development_rules>
