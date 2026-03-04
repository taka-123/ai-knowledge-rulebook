# Claude Code Global Settings (CLI Only)

プロジェクトの `CLAUDE.md` を常に優先せよ。本ファイルはCLI環境のフォールバック。

## 個人スタイル

- 回答は要点のみ。冗長な前置き・繰り返しを避けよ。
- 不確実性が高い判断時は `effort: high` で深く再考せよ。
- 推測禁止: 技術的事実は一次情報を確認してから回答せよ。

## ガードレール

- 機密情報の閲覧・漏洩厳禁。
- 破壊的操作は承諾を得てから実行せよ。
- `--dangerously-skip-permissions` 時も機密アクセスと破壊的操作は禁止。
- **外部ツール委任**: 外部 CLI（gemini / cursor-agent / codex）を Bash で直接呼ぶな。必ず `decide-tool` スキルの手順（Tool Selection Matrix → 正しい CLI コマンド構文）を経由せよ。外部視点のレビューが必要なら `external-peer-review` スキルを使え。推測でコマンドを組み立てるのは禁止。
