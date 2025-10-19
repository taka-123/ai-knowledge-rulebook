# プロジェクトルールの置き場所

- WSL2（推奨）: ~/.claude/
  - 理由: 安定性・パフォーマンス・Linuxツールへのアクセス
- Windows ネイティブ（公式サポート）: %USERPROFILE%\.claude\
  - 前提: Git for Windows 推奨
- Mac: ~/.claude/

の下に、`CLAUDE.md`や、`hooks/`, `commands/`, `agents/` ディレクトリ等を配置してください。
