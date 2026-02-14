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
