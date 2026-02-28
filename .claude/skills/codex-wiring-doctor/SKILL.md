---
name: codex-wiring-doctor
description: Use proactively when editing any file under .codex/agents/ or .codex/config*.toml to detect role mapping drift and orphan or dangling references; When NOT to use: when the task only touches .claude/skills content with no Codex agent wiring impact; Trigger Keywords: [codex wiring, config.toml, orphan agent, role mapping, preset].
---

# codex-wiring-doctor

## When to use

- `.codex/agents/*.toml` を新規追加または削除した直後に配線整合を確認したいとき。
- `.codex/config.toml` や `config.preset.*.toml` の role 割当を変更したとき。
- `orphan` / `dangling` を機械判定してレビュー前に潰したいとき。

## When NOT to use

- `.claude/skills/*/SKILL.md` の文言調整のみで `.codex/` が未変更のとき。
- Codex を利用しない単一プラットフォーム作業のとき。
- config 構成が未確定で判定結果を確定できないとき。

## Trigger Keywords

- codex wiring
- config.toml
- orphan agent
- role mapping
- preset

## Procedure

1. `find .codex/agents -maxdepth 1 -name '*.toml' -type f | sort` で agent 実体一覧を取得する。
2. `node .claude/skills/codex-wiring-doctor/scripts/check-codex-wiring.mjs` を実行して配線を検査する。
3. 必要なら `.claude/skills/codex-wiring-doctor/docs/wiring-rules.md` を Read で確認し、修正方針を確定する。
4. `./.codex/use-preset.sh review` または `./.codex/use-preset.sh audit` を適用後に再検査する。
5. 結果を PASS/FAIL で報告し、未解決が残る場合は BLOCKED として停止する。

## Output Contract

| 項目         | 形式                                                                     |
| ------------ | ------------------------------------------------------------------------ |
| Status       | `PASS / FAIL / BLOCKED`                                                  |
| Agent Files  | `- ./.codex/agents/<name>.toml`                                          |
| Orphan       | `None` または箇条書き                                                    |
| Dangling     | `None` または箇条書き                                                    |
| Verification | `node .claude/skills/codex-wiring-doctor/scripts/check-codex-wiring.mjs` |

### NG例

❌ 実体一覧を読まずに `config_file` を推測で書く（整合性が壊れる）。

❌ preset 側を無視して base config だけ確認する（未配線が残る）。

❌ orphan と dangling を同じ扱いで報告する（修正手順が誤る）。

## Examples

### Example 1

Input: `.codex/agents/security-reviewer.toml` を追加したので配線漏れを検査したい。
Output: orphan/dangling を含む JSON 結果表と修正対象一覧。

### Example 2

Input: `.codex/config.preset.review.toml` の role 割当を変更した。
Output: preset 適用後の再検査結果と最終 Status。

### Example 3

Input: `.codex/config.toml` が存在しない状態で agent を追加した。
Output: `Status: BLOCKED` と不足ファイルの復旧手順。
