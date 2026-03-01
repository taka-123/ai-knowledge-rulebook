---
name: ui-standardizer
description: Use when UI or CSS updates must follow repository visual conventions and accessibility checks across app surfaces; When NOT to use: when tasks are backend-only and have no presentation layer impact; Trigger Keywords: [UI, CSS, レイアウト, accessibility, a11y].
---

# ui-standardizer

## When to use

- UI 実装の見た目とアクセシビリティを同時に整えたい場合。
- デザイントークンや共有定数とコンポーネントの整合性を確認したい場合。

## When NOT to use

- バックエンド処理のみで UI 変更が発生しない場合。
- デザイン方針が未確定で規約適用ができない場合。

## Trigger Keywords

- UI
- CSS
- レイアウト
- accessibility
- a11y

## デザイン指針（プロジェクトにトークンがない／新規作成時）

- **避ける**: 紫〜青系の線形グラデーション背景、Inter / Roboto / Arial など汎用サンセリフのみの構成、中央寄せヒーロー＋均等カードグリッドのテンプレ配置、影・モーションなしのフラットだけの UI
- **推奨**: タイポグラフィの階層差（サイズ・ウェイト）をはっきりつける、単一のプライマリ色＋濃淡で統一、角丸・シャドウ・控えめなモーションで質感を出す

## Procedure

1. `Grep` で `tailwind.config.*` や `variables.css`（または同等）を特定し、プロジェクトのデザイントークンを把握する。トークンがなければ上記デザイン指針を適用する。
2. 新規・修正コードにマジックナンバーやトークンに反する値がないか監査する。色・余白・タイポグラフィは CSS 変数や共有定数を使い、直書きを避ける。
3. アクセシビリティを確認する（ARIA の使い方、コントラスト比、キーボード操作）。WCAG を意識した水準を満たすよう修正する。
4. 画面差分を最小に保ちながら修正し、影響箇所のみ再確認する。

## Output Contract

- 必ず「変更したデザイン規約項目 / a11y確認項目 / 残課題」を分けて報告する。
- 見た目の主観説明だけで終わらせず、規約根拠を添える。
- UI以外の変更（ロジック大改修）は別タスクとして分離する。

### NG例

❌ マジックナンバーやトークンに反する値を直書きする（規約逸脱）。

❌ インタラクティブ要素に ARIA やキーボード操作を欠いたまま完了とする（a11y 不足）。

❌ UI 以外のロジック大改修を同時に行う（責務混在）。

## 完了前チェックリスト

- [ ] 新規・変更したスタイルはプロジェクトのトークン／変数を使っており、マジックナンバーになっていない（トークンがなければ上記デザイン指針に沿っている）
- [ ] インタラクティブ要素に適切な ARIA とキーボード操作が備わっている
- [ ] 色・コントラストが可読性の要件を満たしている

## Examples

### Example 1

Input: ダッシュボード画面の余白ルールを統一したい。
Output: 既存変数に寄せた spacing 指針と修正順を提示する。

### Example 2

Input: テーマ定義の色を画面全体へ反映したい。
Output: 利用箇所を列挙し、段階的な置換計画を提示する。

### Example 3

Input: ビルド後の UI 回帰確認を短時間で実施したい。
Output: 主要画面チェックリストと a11y 観点を提示する。
