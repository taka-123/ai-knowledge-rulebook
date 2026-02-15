---
name: research-protocol
description: Use when external specifications require source-grounded verification with dated citations and explicit fact-versus-inference boundaries; When NOT to use: purely local repository edits with stable requirements; Trigger Keywords: 仕様確認, 出典, 最新, citation, 検証.
---

# research-protocol

## When to use

- 仕様の最新性確認が必要。
- 外部ドキュメントを根拠付きで引用する。

## When NOT to use

- ローカル編集だけで完結する作業。
- 最新情報が不要な固定仕様。

## Trigger Keywords

- 仕様確認
- 出典
- 最新
- citation
- 検証

## Examples

### Example 1

Input: Agent Skills の最新制約を確認して。
Output: 公式一次情報の URL と日付を添えて制約を列挙する。

### Example 2

Input: ルール配置パスの記述が正しいか検証したい。
Output: ツール公式ドキュメントを参照し、差異を明示した修正案を提示する。

### Example 3

Input: 推測が混ざる箇所を区別して報告して。
Output: 事実と推論を分離し、推論箇所には条件付き表現を付与する。

---

## 1. Workflow

1. **Intake**: 調査対象（API 仕様、ツールバージョン、外部制約）と求められる精度（確定事実のみ / 推測許容）を確認する。
2. **Source Collection**: 一次情報（公式ドキュメント、リリースノート、RFC）を `tech-researcher` Agent 経由で取得する。URL と取得日を記録する。
3. **Fact/Inference Separation**: 取得情報を「確定事実」「推測」「未確認」に分類する。推測には根拠と信頼度を付記する。
4. **Freshness Check**: 情報の取得時点を記録し、90 日以上前の情報には STALE 注記を付与する。
5. **Report**: Output Format に従い、出典付きの調査結果を出力する。

## 2. Checklist

### Pre-flight

- [ ] 調査対象が明示されている
- [ ] 求められる精度レベルが確認済み
- [ ] 一次情報ソースの特定方法を把握済み

### Post-flight

- [ ] 全記述に「確定」「推測」「未確認」のラベルが付与されている
- [ ] 確定事実には出典 URL と取得日が付記されている
- [ ] 推測には根拠と信頼度が明示されている
- [ ] STALE 情報（90 日以上前）が注記されている

## 3. Output Format

```markdown
## research-protocol Report

**Topic**: <調査対象>
**Sources**: <N> primary sources consulted
**Freshness**: ALL_CURRENT | HAS_STALE

### Verified Facts

| #   | Claim                | Source URL         | Verified Date | Status    |
| --- | -------------------- | ------------------ | ------------- | --------- |
| 1   | Node.js 18+ required | https://nodejs.org | 2026-02-15    | CONFIRMED |

### Inferences

| #   | Statement            | Basis            | Confidence | Annotation |
| --- | -------------------- | ---------------- | ---------- | ---------- |
| 1   | v20 で非推奨の可能性 | changelog の傾向 | MEDIUM     | （推測）   |

### Unverified

| #   | Claim | Reason           | Recommendation |
| --- | ----- | ---------------- | -------------- |
| 1   | ...   | 公式ソース未発見 | 追加調査が必要 |
```

## 4. Memory Strategy

- **Persist**: 調査済みの一次情報 URL と確認日をキャッシュし、短期間での重複調査を回避する。
- **Invalidate**: 対象技術のメジャーバージョン更新、または前回調査から 90 日経過した場合にキャッシュを無効化する。
- **Share**: 確定事実を `content-writer` Agent に提供し、リポジトリへの書き込み内容の根拠とする。未確認事項を `external-fact-guardian` Agent に提供し、追加検証の入力とする。
