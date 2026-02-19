<!--
Windsurf グローバル設定
- Mac: ~/.codeium/windsurf/memories/global_rules.md
- Windows: %APPDATA%\Codeium\windsurf\memories\global_rules.md
-->

[../../common/global/AGENTS.md](../../common/global/AGENTS.md)に記載のものを添付

---

## Windsurf: Skills 運用

### 探索対象

- Skills: `~/.codeium/windsurf/skills/<skill>/SKILL.md` / `.windsurf/skills/<skill>/SKILL.md`

### 運用ルール

- タスクに関連するスキルを発見した場合は、該当 `SKILL.md` を JIT でロードする。
- スキル名に言及がある場合は、該当スキルを優先して適用する。

### 優先ロードトリガー

- **CSS・スタイル・UIコンポーネントの編集・追加時** → `ui-standardizer`
- **lint/format 失敗時・コード編集後の検証時** → `lint-fix`
- **エラー・不具合・デバッグの依頼時** → `debug-strategist`
- **複雑な実装の着手前** → `task-planner`
- **コミットメッセージ・PR 作成時** → `git-helper`
- **「バックログ用のmd記法」等、Backlog向けMarkdown整形の依頼時** → `backlog-markdown-formatting`
