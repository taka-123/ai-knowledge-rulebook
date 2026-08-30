# Upstream: OpenAI babysit-pr

このディレクトリの `vendor/openai-codex-babysit-pr/` は OpenAI 公式 `babysit-pr` の未改変コピーである。
監視・polling・review/CI 取得・push 後の watch 再開・CI 診断の正本はここ。
この rulebook 向けの改稿はしない。path 差は `scripts/run-gh-pr-watch.py` が吸収する。

| 項目       | 値                                                     |
| ---------- | ------------------------------------------------------ |
| repository | https://github.com/openai/codex                        |
| path       | `.codex/skills/babysit-pr/`                            |
| commit     | `a770e5b8470d3320eb53a56a286ea4a0a70a1f59`             |
| date       | 2026-06-09                                             |
| license    | Apache-2.0（`vendor/openai-codex-babysit-pr/LICENSE`） |

確認日: 2026-08-31

Patches: なし。公式ファイルは未改変。
