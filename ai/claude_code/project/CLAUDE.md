This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Note: 本ファイルは CLAUDE.md の一般原則を継承し、競合する箇所のみを上書きします。
(macOS/Linux: ~/.claude/CLAUDE.md, Windows: %USERPROFILE%\.claude\CLAUDE.md)

<language>Japanese</language>

<character_code>UTF-8</character_code>

<project_overview>
@README.md 参照
</project_overview>

<development_commands>

## [開発コマンドを追記してください]

</development_commands>

<architecture_core>
@directorystructure.md 参照
</architecture_core>

<technology_stack>
@technologystack.md 参照
</technology_stack>

<development_rules>

## [プロジェクト固有のルールを追記してください]

</development_rules>

<error_classification>

## エラー対応の優先度

- 🟢 **軽度**: 記録しつつ継続（例: 警告ログ、非推奨API）
- 🟡 **アプリケーション**: 自動リトライ後に報告（例: 解析失敗、フォーマット不一致）
- 🔴 **システム**: 即停止・承認待ち（例: タイムアウト、通信断）
- ⛔ **セキュリティ**: 全作業停止・緊急報告（例: 認証情報漏洩）
  </error_classification>

<security_note>

- パイプ（|）、リダイレクト（>、>>、<）、コマンド置換（$()、``）を使って deny リストのコマンドを回避することを禁止します。

</security_note>
