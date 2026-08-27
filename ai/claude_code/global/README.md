# Claude Code グローバル設定テンプレート

`~/.claude/` へコピーまたはシンボリックリンクして使う。変更は本ディレクトリに対して行い、実環境への反映はユーザーが行う。`~/.claude/` は Git 管理外で差分追跡できず、セキュリティ上も直接変更しない。

## 配置先

| 環境               | パス                     |
| ------------------ | ------------------------ |
| Mac                | `~/.claude/`             |
| WSL2（推奨）       | `~/.claude/`             |
| Windows ネイティブ | `%USERPROFILE%\.claude\` |

## ディレクトリ構成

```
~/.claude/
  CLAUDE.md          # グローバル設定
  settings.json      # パーミッション等
  skills/            # document-authoring 等
  agents/            # codebase-explorer / tech-researcher
  hooks/             # フック
```

`.claude/commands/`（旧 slash commands）は `skills/` に統合済み。新規は skills 形式で作る。
