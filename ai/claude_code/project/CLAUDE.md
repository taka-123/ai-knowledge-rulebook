# Project Intelligence Guidelines

グローバル原則を継承し、プロジェクト固有の指示を優先する。

<project_context>

<!-- ファイルがないなら、ここはタグ毎削除で良い -->

- 概要: README.md
- アーキテクチャ: directorystructure.md
- 技術スタック: technologystack.md

</project_context>

<development_commands>

## 開発コマンド

<!-- プロジェクトに合わせて記入 -->
<!-- 例:
```bash
npm run dev          # 開発サーバー起動
npm test             # テスト実行
npm run lint         # Lint チェック
npm run build        # ビルド
```
-->

</development_commands>

<delegation_policy>

## 委任原則

`.claude/agents/` と `.claude/skills/` の description にマッチするタスクは自発的に委任せよ。

- **品質ゲート**: 完了報告前に品質監査を実行せよ。
- **計画先行**: 複数ファイルにまたがる変更は計画→承認→着手の順序を守れ。
- 重い探索・試行錯誤は Subagents に閉じ込め、メイン窓のトークン消費を抑えよ。
- 技術的回答は一次情報に接地させ、出典URLを伴う根拠を示せ。

</delegation_policy>

<development_rules>

## 自律動作プロトコル

**自律実行の境界**:

- **自律OK**: 単一ファイル編集、新規ファイル生成、非破壊的な Read/Search/Task。
- **要確認**: 複数ファイルの破壊的 Edit、ファイル/ディレクトリ削除。
  - 隔離環境（`git worktree` 等）での一括作業は計画提示→一括承認で個別確認不要。
- **`--dangerously-skip-permissions` 時**: 機密アクセスと破壊的操作（削除/force push）は禁止。

## 検証の義務

- 既存テストがあれば実行し結果を報告に含めよ。
- テストがなければ CLI 実行か一時スクリプトで検証せよ（一時ファイルは検証後に削除）。

## 完了の定義

- [ ] 意図した変更が反映されている
- [ ] テストがパスしている（または自律検証済み）
- [ ] 関連ドキュメントが更新されている
- [ ] ユーザーに報告し確認を求めている

## 固有規約

- コードレビュー: AGENTS.md `## コードレビュー` に準拠
- セキュリティ: パイプ・リダイレクトによる Deny 回避を厳禁
- Terminal: 絶対パスで指定せよ（`cd`/`pushd`/`popd` 不使用）

</development_rules>
