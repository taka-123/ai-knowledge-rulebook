# Claude Code グローバル設定テンプレート

本ディレクトリはテンプレートライブラリです。実環境 `~/.claude/` へはユーザーが手動でコピーまたはシンボリックリンクして反映してください。

> **重要**: Claude が `~/.claude/` を直接変更することは禁止です（セキュリティ上の理由 + Git 管理外のため差分追跡不可）。変更はこのリポジトリのテンプレートに対して行い、ユーザーが実環境へ反映します。

## 配置先

| 環境                 | パス                      |
| -------------------- | ------------------------- |
| Mac                  | `~/.claude/`              |
| WSL2（推奨）         | `~/.claude/`              |
| Windows ネイティブ   | `%USERPROFILE%\.claude\`  |

## ディレクトリ構成

```
~/.claude/
  CLAUDE.md          # グローバル設定
  settings.json      # パーミッション等
  skills/            # スキル定義（推奨形式）
    decide-tool/
      SKILL.md
    external-peer-review/
      SKILL.md
    ...
  agents/            # エージェント定義
  hooks/             # フック定義
```

> **Note**: `.claude/commands/` (旧 slash commands) は `.claude/skills/` に統合済みです。新規作成は skills 形式で行ってください。
