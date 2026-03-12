---
name: prompt-evolution
description: "Use when the user explicitly asks to evolve, optimize, or refine a vague instruction into a high-quality prompt for Claude/Cursor; When NOT to use: when the user wants to execute a task directly without prompt optimization; Trigger Keywords: [prompt-evolution, プロンプト最適化, prompt optimize, 曖昧な指示を明確化, 指示を洗練, 指示をブラッシュアップ, 指示を最適化, 指示を昇華, プロンプトを昇華, /prompt-evolution]."
---

# prompt-evolution

曖昧なユーザー指示を、Contract Style の高品質プロンプトへ変換する。

## When to use

- 曖昧・抽象的だったり、文脈不足の指示を明確なプロンプトへ変換したいとき。
- IDE/CLI（Claude Code, Cursor 等）で再利用可能なプロンプトを確定したいとき。

## When NOT to use

- 既に十分に具体的な指示をそのまま実行したいとき。
- プロンプト生成ではなくタスク実行が主目的のとき。
- 単純な typo 修正や文言の微調整だけで済むとき。

## Trigger Keywords

- prompt-evolution
- プロンプト最適化
- prompt optimize
- 曖昧な指示を明確化
- 指示を洗練
- 指示をブラッシュアップ
- 指示を最適化
- 指示を昇華
- プロンプトを昇華
- /prompt-evolution

## Procedure

核心原則:

- **Prompting Inversion**: 思考プロセス（CoT 等）を強制せず、Goal と成功基準のみを記述した Contract Style を採用する。
- **Context Dosing**: ノイズを削ぎ落とし、最小限の高信号トークンのみを使用する。

1. **Intent & Context Retrieval**: ユーザーの目的（Goal）と制約を解析する。情報が不足している場合はユーザーに質問して補完する。関連する既存コードやファイルがあれば読み込み、Context として抽出する。
2. **Prompt Synthesis (Act)**: 核心原則に従い、抽出したコード文脈を含めたプロンプトのドラフトを生成する。
3. **Critic Evaluation (Reflect)**: 以下の指標でドラフトを 10 点満点で自己評価する。
   - Goal Alignment（意図との一致度）
   - Contract Style 遵守度（要素の網羅性）
   - Token Efficiency（無駄なコンテキストがないか）
   - Prompting Inversion 回避度（過剰な制約がないか）
4. **Iterate**: 初回は必ず改善ループを 1 回実行する。2 回目以降は総合平均 9.0 以上で終了可（最大 3 回）。
5. **Final Emit**: 最終プロンプト（Markdown コードブロック形式）と評価サマリーを出力する。ユーザーが保存先を指定した場合はファイルに書き出す。

## Output Contract

| 項目          | 形式                                  |
| ------------- | ------------------------------------- |
| Final Prompt  | Markdown コードブロック（``` で囲む） |
| Evaluation    | 各指標スコアと総合平均                |
| Iteration Log | ループ回数と主な修正内容              |

### NG例

❌ CoT や段階的思考を強制する指示を含める（Prompting Inversion 違反）。

❌ 関連の薄いファイルを大量に Context に含める（Context Dosing 違反）。

❌ 評価なしで 1 回のドラフトで終了する（Critic ループ未実施）。

❌ ユーザーに確認せず生成プロンプトをそのまま実行する（スキルの責務逸脱）。

## Examples

### Example 1

Input: 「このコードベースの課題って何だろう、アーキテクチャ的にも技術的にも気になる点を洗い出してほしい」
Output: コード文脈を踏まえた分析タスクの Goal・成功基準・出力形式を含む Contract Style プロンプトと評価サマリー。

### Example 2

Input: 「今の技術スタックで、キャッシュ層や検索まわりをどう導入するのがいいか、調べて意見が欲しい」+ リポジトリの構成。
Output: 現状の技術スタックを Context に含め、調査範囲・比較軸・推奨の出力形式を明示したプロンプト。

### Example 3

Input: 「この機能があるなら、こういう新しい機能や画面を作ったら便利じゃないか、調べて提案してほしいな」
Output: 既存機能を前提に、提案の範囲・成功基準・出力形式を整理したプロンプト。
