---
name: prompt-evolution
description: "Use when the user explicitly asks to evolve, optimize, or refine a vague instruction into a high-quality prompt for Claude/Cursor; When NOT to use: when the user wants to execute a task directly without prompt optimization; Trigger Keywords: [prompt-evolution, プロンプト最適化, prompt optimize, 曖昧な指示を明確化, 指示を洗練, 指示をブラッシュアップ, 指示を最適化, 指示を昇華, プロンプトを昇華, /prompt-evolution]."
---

# prompt-evolution

曖昧なユーザー指示を Contract Style の高品質プロンプトへ変換する。

## 核心原則

- **Prompting Inversion**: 思考プロセス（CoT 等）を強制せず、Goal と成功基準のみを記述する。
- **Context Dosing**: ノイズを削ぎ、最小限の高信号トークンに絞る。

## Procedure

1. **Intent & Context Retrieval**: Goal と制約を解析する。情報不足ならユーザーに確認する。関連コードを Context として抽出する。
2. **Prompt Synthesis**: 核心原則に従いドラフトを生成する。
3. **Critic Evaluation**: 以下 4 指標で 10 点満点の自己評価。
   - Goal Alignment（意図一致）
   - Contract Style 遵守度
   - Token Efficiency
   - Prompting Inversion 回避度
4. **Iterate**: 初回は必ず 1 回改善ループ。2 回目以降は総合平均 9.0 以上で終了可（最大 3 回）。
5. **Emit**: 最終プロンプト（Markdown コードブロック）と評価サマリーを返す。

## Output Contract

| 項目          | 形式                                  |
| ------------- | ------------------------------------- |
| Final Prompt  | Markdown コードブロック（``` で囲む） |
| Evaluation    | 各指標スコアと総合平均                |
| Iteration Log | ループ回数と主な修正内容              |

## Examples

- 「このコードベースの課題を洗い出して」→ コード文脈を踏まえた分析タスクの Goal・成功基準・出力形式を含む Contract Style プロンプト。
- 「キャッシュ層や検索の導入を調べて意見が欲しい」→ 現状スタックを Context に、調査範囲・比較軸・推奨形式を明示したプロンプト。
