---
name: suggest-claude-md
description: "Use when the user explicitly asks to analyze conversation history and suggest additions to CLAUDE.md; When NOT to use: when the user wants to directly edit CLAUDE.md without analysis; Trigger Keywords: [suggest-claude-md, CLAUDE.md, suggest rules, conversation analysis, pattern detection]."
---

# suggest-claude-md

Analyze conversation history and suggest new rules or patterns to add to CLAUDE.md.

## When to use

- 会話履歴から CLAUDE.md に追記すべきルールを抽出したいとき。
- 繰り返される修正指示やプロジェクト固有パターンを検出したいとき。
- コード変更と同じ PR に CLAUDE.md 更新を含めたいとき。

## When NOT to use

- CLAUDE.md を直接編集する指示が明確なとき。
- 一時的な判断や個別ケースの対応のとき。
- 既に CLAUDE.md に記載済みの内容のとき。

## Trigger Keywords

- suggest-claude-md
- CLAUDE.md
- suggest rules
- conversation analysis
- pattern detection

## Detection Triggers

### 1. Project-specific Rules

- "A ではなく B を使ってください" パターン
- "このプロジェクトでは X のようにしています" パターン
- 標準的コードを生成後にプロジェクト固有の方法に修正指示

### 2. Repeated Corrections

- 同じ種類の修正指示が 2 回以上出現
- 類似のコード修正が複数ファイルで発生
- 同じアドバイスが複数回

### 3. Cross-location Consistency

- "こことここは実装を合わせてください" パターン
- "Web 側と API 側で統一してください" パターン
- 関連する複数箇所での統一指示

## Procedure

1. 会話履歴を走査し、上記 3 つのトリガー条件に該当する内容を検出する。完了条件: 該当箇所をリストアップ。
2. 検出内容を CLAUDE.md に追記可能なルール形式に整形する。完了条件: 具体的な追記案が完成。
3. 既存の CLAUDE.md と照合し、重複がないことを確認する。完了条件: 重複排除済み。
4. 提案を所定フォーマットで出力する。完了条件: ユーザーが判断可能な形式。
5. ユーザーが承認した場合、CLAUDE.md に追記する。完了条件: 追記完了。

## Output Contract

### Trigger hit

```
会話履歴を分析しました。以下の内容をCLAUDE.mdに追記しませんか？

追記した方がよさそうであれば、「この内容をCLAUDE.mdに追記してください」のように指示してください。

[提案する具体的な内容]

理由: [プロジェクト独自のルール / 同じような修正指示の繰り返し(N回) / 関連箇所で揃えるべきパターン]
```

### No trigger

```
会話履歴を分析しました。CLAUDE.mdに追記すべき新しい内容は見つかりませんでした。
```

### NG例

- 会話の要約や完了報告形式で出力する（フォーマット違反）。
- 冒頭の「会話履歴を分析しました。」を省略する（一貫性欠如）。
- 不明確または曖昧な内容をルールとして提案する（品質不足）。

## Examples

### Example 1

Input: `/suggest-claude-md`
Output: 会話中に「Config モジュール経由でアクセスしてください」が 3 回出現 → ルール提案。

### Example 2

Input: `/suggest-claude-md`
Output: トリガー条件に該当なし → 「追記すべき内容は見つかりませんでした」。

### Example 3

Input: `/suggest-claude-md`
Output: Web/API エンドポイントの統一指示を検出 → パス命名規則を提案。
