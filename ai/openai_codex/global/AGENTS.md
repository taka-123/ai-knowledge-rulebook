<!--
OpenAI Codex CLI グローバル設定
- WSL2（公式推奨）: ~/.codex/AGENTS.md
  - 理由: 安定性・全機能保証・Unix環境での最適化
- Windows ネイティブ（実験的サポート）: C:\Users\<YourUsername>\.codex\AGENTS.md
  - 注意: WSL2推奨。ネイティブは実験的サポートで制限あり
- Mac: ~/.codex/AGENTS.md
-->

[../../common/global/AGENTS.md](../../common/global/AGENTS.md)に記載のものを添付

---

## Codex: 状況に応じたスキルの適用

利用可能な `~/.agents/skills/` の SKILL.md は、タスクに応じて JIT でロードせよ。とくに次の場合は該当スキルをロードしてから作業せよ。

- **CSS・スタイル・UIコンポーネントの編集・追加時** → `ui-standardizer`
- **lint/format 失敗時・コード編集後の検証時** → `lint-fix`
- **エラー・不具合・デバッグの依頼時** → `debug-strategist`
- **複雑な実装の着手前** → `task-planner`
- **コミットメッセージ・PR 作成時** → `git-helper`
- **「バックログ用のmd記法」等、Backlog向けMarkdown整形の依頼時** → `backlog-markdown-formatting`
