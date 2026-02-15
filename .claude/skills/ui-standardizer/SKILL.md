---
name: ui-standardizer
description: Use when CSS or UI component updates must follow explicit typography, color, spacing, and accessibility conventions for this repository; When NOT to use: backend-only tasks without UI changes; Trigger Keywords: UI, CSS, レイアウト, a11y, デザイン.
---

# ui-standardizer

## When to use

- CSS/Tailwind/コンポーネントの見た目を更新する。
- 可読性やアクセシビリティ改善を求められている。

## When NOT to use

- UI に触れないバックエンド作業。
- テキストのみのドキュメント編集。

## Trigger Keywords

- UI
- CSS
- レイアウト
- a11y
- デザイン

## Examples

### Example 1

Input: ダッシュボードのカード UI を整えてアクセシビリティも担保して。
Output: コントラスト、フォーカス可視化、キーボード操作を満たす CSS 修正を提案する。

### Example 2

Input: 既存トークンに合わせて配色を統一して。
Output: 直書きカラーを変数化し、共通トークンへ置き換える差分を作る。

### Example 3

Input: モバイルで崩れるレイアウトを最小変更で直したい。
Output: ブレークポイント単位で必要箇所だけ修正し、PC表示を維持する。

---

## 1. Workflow

1. **Intake**: UI 変更対象（コンポーネント、ページ、CSS ファイル）と要件（デザイン統一 / アクセシビリティ改善 / レスポンシブ対応）を確認する。
2. **Convention Load**: プロジェクトの UI 規約を確認する。
   - カラートークン（CSS 変数 / Tailwind テーマ）
   - タイポグラフィ（フォントサイズ、行間、ウェイト）
   - スペーシング（余白の基準単位）
   - ブレークポイント定義
3. **Audit**: 対象の現状を規約と照合し、違反箇所を検出する。アクセシビリティ（コントラスト比、フォーカス可視化、キーボード操作）を検証する。
4. **Fix Proposal**: 違反箇所ごとに最小差分の修正案を提示する。直書き値のトークン化、コントラスト比の改善、フォーカスリングの追加等。
5. **Apply & Verify**: Edit で修正を適用し、ブラウザでの表示確認手順を提示する。

## 2. Checklist

### Pre-flight

- [ ] 変更対象のファイルパスが特定済み
- [ ] プロジェクトの UI 規約（トークン、タイポグラフィ）を確認済み
- [ ] アクセシビリティ要件（WCAG レベル）を把握済み

### Post-flight

- [ ] 直書きカラー値がトークン化されている
- [ ] コントラスト比が WCAG AA 基準を満たしている
- [ ] フォーカス可視化が実装されている
- [ ] レスポンシブ対応がブレークポイント単位で検証されている
- [ ] 既存レイアウトが意図しない変更を受けていない

## 3. Output Format

```markdown
## ui-standardizer Report

**Action**: AUDIT | FIX
**Target**: <file path(s)>
**Requirements**: Design Consistency | Accessibility | Responsive

### Violations

| #   | File               | Line | Rule          | Current   | Expected               |
| --- | ------------------ | ---- | ------------- | --------- | ---------------------- |
| 1   | styles/card.css    | 12   | Color token   | `#3b82f6` | `var(--color-primary)` |
| 2   | components/nav.tsx | 45   | Focus visible | missing   | `outline: 2px solid`   |

### Fixes Applied

| #   | File            | Line | Change                              |
| --- | --------------- | ---- | ----------------------------------- |
| 1   | styles/card.css | 12   | Replaced hardcoded color with token |

### Accessibility Check

| Criteria       | Status | Detail                    |
| -------------- | ------ | ------------------------- |
| Contrast ratio | PASS   | 4.8:1 (AA requires 4.5:1) |
| Focus visible  | PASS   | Outline ring added        |
| Keyboard nav   | PASS   | Tab order verified        |
```

## 4. Memory Strategy

- **Persist**: プロジェクトのカラートークン、タイポグラフィ設定、ブレークポイント定義をキャッシュし、次回の監査を高速化する。
- **Invalidate**: CSS 変数定義、Tailwind 設定、デザインシステムの定義ファイルが変更された場合にキャッシュを無効化する。
- **Share**: 違反リストを `lint-fix` に提供し、自動修正可能な項目の処理に活用する。アクセシビリティ検証結果を `task-reviewer` Agent に提供し、品質監査の根拠とする。
