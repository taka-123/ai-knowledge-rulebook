---
name: product-ui-ux
description: |
  Use when: 管理画面・業務画面・会員/外部利用者向け画面など、プロダクトUIの設計、画面刷新、新機能の画面設計、重要な画面改善を行うとき。画面の見た目・使いやすさに関わる依頼では標準で使用する。
  When NOT to use: UIに関わらないバックエンド実装、文言1箇所の修正等の自明な変更、UI以外のレビュー。
  Trigger Keywords: [UI, UX, 画面, デザイン, 刷新, リデザイン, 見た目, レイアウト, 使いやすく, フォーム, テーブル, アクセシビリティ, responsive, redesign, product-ui-ux]
---

# Product UI/UX

汎用的なAI生成UIではなく、使いやすく、保守しやすく、意図のある見た目のプロダクトUIを作るための Skill。

## 進め方

1. タスクを分類し（Surface / Task / Alignment）、工程の深さを決める
2. 画面の仕事を理解し、既存UIとコードを調査し、見た目より先にUX構造を設計する
3. 重要な `EXPLORE` では、Reference から原則を抽出し、2〜3案の方向を提案して人間の選択を待つ
4. Design Plan を確定し、既存の技術スタックで実装し、実際の描画結果で仕上げる
5. 完了前に `references/qa-checklist.md` を Read して QA する

## 1. 優先順位

指示が衝突したときは次の順で従う。

1. ユーザーの明示要件
2. 安全性、権限、法令、Accessibility 等の Hard constraints
3. プロジェクトで採用済みの UI Guidelines と正本 Components
4. 現在のタスクで人間が承認した Direction
5. 本 Skill
6. `frontend-design` の Visual 提案

本 Skill の一般的な推奨を、プロジェクトの Hard constraint に格上げしない。

## 2. タスクを分類する

設計前に次の3軸を確定する。

### Surface: 誰が使うか

- `INTERNAL_ADMIN`: 自社の担当者が使う管理画面 — 高密度、効率、Bulk操作、権限、状態把握、誤操作防止
- `FACILITY_ADMIN`: 顧客組織の担当者が使う業務画面 — 日常業務の速さ、学習しやすさ、検索・一覧・入力、状態の明確さ
- `USER_FACING`: 会員・顧客・一般公開・申込等の外部利用者向け画面 — 初見理解、安心感、Mobile、入力負荷、エラー回復、Accessibility、Visual quality

同じ見た目を全 Surface へ機械的に適用しない。共通の工程を使い、対象利用者に合わせて最適化する。

### Task: 何をするか

- `REDESIGN`: 既存画面を機能要件から再設計する
- `NEW_FEATURE`: 新しい画面・インタラクションを設計する
- `LOCAL_IMPROVEMENT`: 採用済みの方針内で既存画面を局所的に改善する

### Alignment: 既存の見た目へどこまで合わせるか

- `EXPLORE`: 現行の見た目を Hard constraint とせず、実質的により良い解を探索する
- `ALIGN`: 採用済みの基準画面・UI Guidelines・共通 Components に従う

既定の組み合わせ:

- `REDESIGN` / `NEW_FEATURE` → `EXPLORE`
- `LOCAL_IMPROVEMENT` → `ALIGN`。採用済み基準があればそれに、無ければ隣の現行画面に合わせる。新しい Art Direction は作らない
- 採用済み基準が無い刷新・新機能を、最初から `ALIGN` で始めない

3軸はタスクとリポジトリから確実に推定できる範囲で推定する。答えによって Direction や実装が実質的に変わる曖昧さだけ、ユーザーへ確認する。

## 3. 工程の深さを選ぶ

### LOCAL_IMPROVEMENT + ALIGN

コンパクトな工程を使う。

1. 問題と影響範囲を特定する
2. 採用済みのプロジェクトパターンを確認する
3. 最小の一貫した改善を行う
4. 影響する Viewport と状態を確認する
5. プロダクトの Art Direction を作り直さない

問題が実は構造的なら、`REDESIGN` への変更を提案する。

### REDESIGN / NEW_FEATURE + EXPLORE

以降のフル工程を使う。

## 4. 見た目より先に画面の仕事を理解する

次を確定する。

- 主な利用者 / 達成すべき仕事 / 主操作 / 副操作
- 利用頻度 / 習熟度 / 想定端末・Viewport
- 想定データ量 / エラーのコスト / 権限差
- 必要な状態 / Brand 制約 / Accessibility 要件 / 技術的 Hard constraints

色、カード、影、装飾から始めない。

## 5. 既存UIとコードを調査する

対象: Framework、Styling 方式、共通 Components、Tokens / CSS variables、Icon、Form 実装、Table / Grid、Modal / Drawer、Navigation、Breakpoints、Accessibility 慣習、テスト、既存 UI Guidelines、出来の良い既存画面。

次を区別する。

- 機能要件
- 技術制約
- 採用済みの基準
- 現行の見た目の偶然の特徴

`EXPLORE` では、プロジェクトが明示しない限り、現行の見た目の特徴は Hard constraint ではない。

## 6. UX構造を設計する

Visual の仕上げより先に次を定義する。

- 情報構造 / タスクフロー / 主操作と副操作 / Progressive disclosure
- Search / Filter / Sort / Bulk操作 / Validation
- 破壊的操作の保護 / 確認と Undo の方針
- Loading / Empty / Error / Success / 権限・読み取り専用の差

操作数、判断、読む量、入力、エラー、学習コストを実証的に減らせる場合を除き、慣れたインタラクションパターンを優先する。

## 7. Reference を使う

重要な `EXPLORE` では、利用可能なら 3〜5 件の Reference を使う。

Reference は見た目の仕様書ではない。各 Reference から次を抽出する。

- 情報の階層 / 密度の戦略 / インタラクションパターン
- 主操作・副操作の扱い / 状態の見せ方
- このプロダクトに使える原則 / 真似してはいけない表現

1つのプロダクトの模倣ではなく、原則を組み合わせる。

## 8. 方向を探索する

重要な `EXPLORE` では、本実装の前に、本質的に異なる 2〜3 案の方向を提案する。

各案に含める: コンセプト、階層、レイアウト、密度、Typography の方針、色の役割、中核インタラクション、象徴となる要素、残すもの、変えるもの、利点、リスク。

案の差が表面的（色違い等）ではいけない。情報構造、インタラクション、密度、レイアウトの論理など、実質的な性質で異なること。

### 案の見せ方

案は文章だけで提示せず、見て比べられる形で並べる。人間は描画結果を見て選ぶ方が正確に判断できる。判断に必要な最小の忠実度を選ぶ。

- 見た目の方向だけを比べる: 静止画または軽量モック各1枚で足りる。作り込まない
- UX・状態・構造まで比べる: 実プロジェクトの Components / Tokens / CSS を使った使い捨てプロトタイプ（dev 専用ルート、Storybook 等の隔離環境）で作り、主要 Viewport のスクリーンショットを並べて比較できるようにする
- ツールにアートボード生成や並列生成の機能があれば使ってよい

使い捨てプロトタイプの境界: API・DB・本番ルートに触れず、データは mock fixture だけにする。選ばれなかった案は削除する。採用案も本実装で改めて作る。

## 9. 人間の意思決定ゲート

重要な `EXPLORE` では、人間が方向を選ぶまで最終実装を始めない。

採用済みの基準を実質的に変える場合は、黙って基準を再定義せず、変更を提示して承認を得る。

小さな `LOCAL_IMPROVEMENT + ALIGN` では、依頼範囲を実質的に超えない限り、別途の承認ラウンドは不要。

## 10. `frontend-design` を併用する

次の場合は本 Skill に加えて `frontend-design` を使う。

- Visual / Art Direction の探索が重要なとき
- `REDESIGN + EXPLORE` で現行の見た目から離れる必要があるとき
- `NEW_FEATURE + EXPLORE` で独自性のある見た目が必要なとき
- `USER_FACING` で Visual quality が重要なとき
- Typography、レイアウト、構図、Brand 印象を大きく改善したいとき
- 提案が汎用的なAI風UIに収束しているとき

Task completion、UX、状態、Accessibility、プロジェクト制約の責任は本 Skill が持つ。`frontend-design` は Visual と Art Direction の品質に特化する。

## 11. Design Plan を確定する

方向の選択後、一貫して作るために必要な分だけ定義する: 色の役割、Typography、Spacing のリズム、レイアウト / Grid、必要なら Radius / Elevation、ボタンの階層、Form の挙動、一覧 / Table の挙動、Navigation の挙動、Motion、象徴となるインタラクション。

1画面のために大きな Design System を作らない。

## 12. 実装する

- 既存の技術スタックを基本にする
- 本当に合う Components は再利用する
- 選択した UX を阻害する既存 Component は改善してよい
- 見た目の新しさだけのために Library を追加しない
- 現実的なコンテンツとデータ量で作る
- 必要な機能と状態を維持する
- 無関係な基盤変更は今回のUIタスクと分ける

共有基盤の変更が複数画面を実質的に改善するなら、別途提案する。

## 13. 実際の描画結果で仕上げる

ソースコードだけで完成を判断しない。実際の描画結果を確認し、Spacing、整列、階層、密度、Typography、操作の目立ち方、状態の見えやすさ、一貫性を調整する。

Design Mode 等の視覚編集ツールは有用なら使ってよいが、QA の代替にしない。

## 14. 完了前の QA

完了前に `references/qa-checklist.md` を Read し、Task completion / 情報階層 / データ耐性 / 状態 / Responsive / Accessibility / Visual / 回帰を確認する。

追加の判定:

- `USER_FACING` は、プロジェクト要件が優先しない限り WCAG 2.2 Level AA を目標にする
- Task completion より先に Visual の新しさを最適化しない
- 意味のある修正の後は、描画結果を再確認する

## 15. 代表利用者での検証

重要またはリスクの高い画面では、代表的な利用者による短い検証を提案する。

観察する: 最初に何をすべきか分かるか、主要タスクを完了できるか、不要な後戻り、エラー、状態変化の誤解、読む量・判断の多さ、不要なステップ。

観察した難しさを、ドメイン知識によるもの、UI・情報設計によるもの、通常の不慣れ、に分けて評価する。UI自体が実質的な混乱を生んでいたら、タスクフローまたは情報構造へ戻る。

## 16. 基準への昇格

`EXPLORE` の成功は自動的に新基準にならない。昇格は次を満たした後だけ行う。

- 人間の明示的な採用
- Visual QA / 状態 QA / Accessibility QA
- 現実的なデータでの検証
- 必要なら代表利用者での検証
- 保守性のレビュー

昇格後は、再利用できる決定だけをプロジェクトの UI Guidelines、Tokens、Components へ抽出する。以降の画面は通常 `ALIGN` を使う。

## 17. 参照資料

- `references/qa-checklist.md`: 完了前の QA（手順 14 で Read する）
- `references/brief-template.md`: 重要な刷新・新機能の依頼テンプレ。局所改善では使わない
