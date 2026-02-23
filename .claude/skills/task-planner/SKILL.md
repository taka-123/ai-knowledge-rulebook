---
name: task-planner
description: Use when implementation requires step-by-step planning with explicit file targets and verification gates; When NOT to use: when a one-line edit can be completed safely without decomposition; Trigger Keywords: [計画, 分解, roadmap, milestone, 実装手順].
---

# task-planner

## When to use

- 複数ファイルにまたがる変更を着手前に分解したい場合。
- 変更の影響範囲・順序・検証コマンドを事前に確定してから実装したい場合。

## When NOT to use

- 単一ファイルの軽微な文言修正のみで完了する場合。
- 既存手順が確定しており追加計画が不要な場合。
- ユーザーが「計画不要で実装して」と明示している場合。

## Trigger Keywords

- 計画
- 分解
- roadmap
- milestone
- 実装手順

## Procedure

1. タスクを 🟢（安全）/ 🟡（要注意）/ 🔴（破壊的）で分類し、先に宣言する。
2. 対象ファイルを明示する（新規 / 更新 / 削除に分けてリストアップ）。
3. 実装ステップを 3〜6 手順で書く（各手順に「完了条件」を付ける）。
4. 検証コマンドを先に固定する：最低 `npm run format:check`、JSON 変更時は `npm run schema:check`、スキル変更時は `npm run agent:check`。
5. 前提不足や依存関係が不明な場合だけ質問し、それ以外は実装に進む。

## Output Contract

必ず以下の順で提示する：

**🎯 目的**: 1行で何を解決するか
**⚠️ 制約**: 守るべきルール（最大差分・破壊的操作禁止等）
**🔍 影響範囲**: 対象ファイル一覧（新規/更新/削除）
**📝 実装手順**: チェックリスト形式（各手順に完了条件）
**✅ 検証**: 実行するコマンドと期待する結果

### NG例

```
❌ 「調査してから判断します」で終わらせて実装アクションを示さない
❌ 影響ファイルを列挙せずに「関連ファイルを更新する」と曖昧に書く
❌ 検証コマンドを省略する
❌ チェックリスト形式にせず「〜する予定」と書く（完了判断が曖昧）
```

## Examples

### Example 1

Input: 複数のスキルファイルを同時に改良したい。改修順を決めてほしい。
Output: 🟢 安全な変更と宣言し、スキルごとの改修ステップ（各ファイルを更新 → `npm run agent:check` でパス確認）をチェックリスト形式で提示する。

### Example 2

Input: JSON スキーマを追加して既存の JSON も対応させたい。
Output: 🟡 スキーマ追加（`schemas/`） → 既存 JSON 更新（`ai/`） → `npm run schema:check` の順で計画を提示する。

### Example 3

Input: 新しいスクリプトを追加して `agent:check` パイプラインに組み込みたい。
Output: スクリプト新規作成 → `package.json` 更新 → `npm run agent:check` で全件パス確認の3ステップ計画を提示する。
