---
name: decide-tool
description: "Use when the user explicitly asks to delegate a task to an external CLI tool (Gemini/Cursor/Codex), or when Claude determines a task is better suited for an external tool; When NOT to use: when Claude can complete the task directly without external tool delegation; Trigger Keywords: [decide-tool, gemini, cursor, codex, external tool, tool selection, consensus]."
allowed-tools: Bash(gemini*), Bash(cursor-agent*), Bash(cursor*), Bash(codex*), Bash(bash -lc*)
---

# decide-tool

External CLI tool router. Analyzes the task and selects the optimal tool (Gemini / Cursor / Codex), then executes it.

## When to use

- 高速ドラフト・大量ファイル処理・最新情報検索など、外部CLIが得意な領域を委任するとき。
- ユーザーが `/gemini-*`, `/cursor-*`, `/codex-*` 等の外部ツール連携を明示的に要求したとき。
- 複数ツールの結果を比較してコンセンサスを取りたいとき（`consensus` モード）。

## When NOT to use

- Claude 単独で完結する設計・リファクタ・テスト・深い分析タスクのとき。
- 外部 CLI がインストールされていない環境のとき。
- 機密情報を含むタスクで外部 AI への送信が不適切なとき。

## Trigger Keywords

- decide-tool
- gemini
- cursor
- codex
- external tool
- tool selection
- consensus

## Tool Selection Matrix

| Category                    | Best Tool | CLI Command                            | Use Cases                            |
| --------------------------- | --------- | -------------------------------------- | ------------------------------------ |
| **Fast draft / Prototype**  | Gemini    | `gemini -p "$ARGUMENTS" -o text`       | 高速ドラフト、プロトタイプ作成       |
| **Breakdown / Planning**    | Gemini    | `gemini -p "$ARGUMENTS" -o text`       | 初動仕様分解、タスクブレイクダウン   |
| **Bulk processing**         | Gemini    | `gemini -p "$ARGUMENTS" -o text`       | 大量ファイル整理、反復作業           |
| **Research / Search**       | Gemini    | `gemini -p "$ARGUMENTS" -o text`       | 最新情報スキャン、市場調査、Web検索  |
| **UI / Visual**             | Cursor    | `cursor-agent -p --trust "$ARGUMENTS"` | UI調整、レスポンシブ最適化           |
| **Visual diff**             | Cursor    | `cursor-agent -p --trust "$ARGUMENTS"` | 目視diff確認、微調整                 |
| **Doc + Code polish**       | Cursor    | `cursor-agent -p --trust "$ARGUMENTS"` | コード＋ドキュメント同時洗練         |
| **Exploratory prototype**   | Cursor    | `cursor-agent -p --trust "$ARGUMENTS"` | 探索的プロトタイピング               |
| **Parallel implementation** | Codex     | `codex exec "$ARGUMENTS"`              | 複数機能同時並列実装                 |
| **Deep debug / Optimize**   | Codex     | `codex exec "$ARGUMENTS"`              | 低レベルdebug、アルゴリズム最適化    |
| **Long-running task**       | Codex     | `codex exec "$ARGUMENTS"`              | 夜間・長時間放置タスク（30分以上OK） |
| **Spec / PRD / Test plan**  | Codex     | `codex exec "$ARGUMENTS"`              | 厳密な構造文書・PRD・テスト計画      |

## Procedure

1. タスク内容を分析し、上記マトリクスから最適ツールを1つ選択する。選択根拠を明記する。
2. 対応する CLI コマンドを `$ARGUMENTS` を埋めて実行する。
3. 結果を要約し、Claude で品質チェック・次のアクション判断ができる形に整形する。

### Consensus モード

`/decide-tool consensus ...` または明示的にコンセンサスを求められた場合:

1. 3ツール全てを順番に実行する:
   - `gemini -p "$ARGUMENTS" -o text`
   - `cursor-agent -p --trust "$ARGUMENTS"`
   - `codex exec "$ARGUMENTS"`
2. 各結果を比較し、一致点・相違点をまとめる。
3. コンセンサスと最終推奨を提示する。

## Output Contract

| Item           | Format                    |
| -------------- | ------------------------- |
| Selected Tool  | `Gemini / Cursor / Codex` |
| Reason         | 選択根拠 1-2 文           |
| Command        | 実行した CLI コマンド     |
| Result Summary | 結果の要約                |
| Next Action    | Claude での後続作業提案   |

### NG例

- タスク分析なしにツールを決め打ちする（根拠不足）。
- 機密情報を外部 CLI に渡す（セキュリティ違反）。
- 結果をそのまま返して要約・品質チェックしない（付加価値なし）。

## Examples

### Example 1

Input: `/decide-tool React コンポーネントの初期設計をドラフトして`
Output: Gemini を選択（高速ドラフト向き）、`gemini -p "React コンポーネントの初期設計をドラフトして" -o text` を実行、結果を要約。

### Example 2

Input: `/decide-tool consensus このAPIのエラーハンドリング設計を評価して`
Output: 3ツール全実行、各視点を比較、コンセンサスを提示。

### Example 3

Input: `/decide-tool UIのレスポンシブ表示を調整して`
Output: Cursor を選択（UI/Visual 向き）、`cursor-agent -p --trust "..."` を実行。
