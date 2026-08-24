# UI/UX 依頼テンプレ

重要な刷新・新機能・大きな改善の依頼で使う。

局所改善（色・余白・ラベル等の小さな修正）はこのテンプレの対象外。直接依頼し、採用済みの基準（無ければ隣の現行画面）に合わせる。

## Classification

Surface:

- INTERNAL_ADMIN / FACILITY_ADMIN / USER_FACING

Task:

- REDESIGN / NEW_FEATURE / LOCAL_IMPROVEMENT

Alignment:

- EXPLORE / ALIGN

## Goal

この画面で利用者が達成すべき最重要目的:

## Users

主な利用者:

利用頻度:

習熟度:

主な端末 / Viewport:

## 現状の問題

遅延・混乱・エラー・無駄な手間の原因になっているもの:

## 残すもの

維持すべき機能、データ、権限、状態、色の役割、Components:

## 変えてよいもの

情報の優先順位、主操作、レイアウト、状態の見せ方、密度、その他変えてよいもの:

## データ

通常時と最悪時のデータ量:

## Hard constraints

技術:

Brand:

権限 / セキュリティ:

法令:

Accessibility:

## 採用済みの基準

基準画面:

UI Guidelines:

再利用する Components:

採用済みの基準が無ければ空欄にする。

## References

Reference 1:
使える原則:

Reference 2:
使える原則:

Reference 3:
使える原則:

## 受け入れ条件

Task completion:

必要な状態:

必要な Viewport:

Accessibility:

## Process（人間が止める点）

いきなり本実装を始めない。

- `EXPLORE`: 現行から十分離れた 2〜3 案の方向を提案し、人間が選ぶまで待つ
- `ALIGN`: 基準に沿った Design Plan を1案作り、人間が承認するまで待つ
- 実装後は実画面で、主要 Viewport、Loading / Empty / Error、実データに近い量、Keyboard / Focus を確認する

これは毎回すべて人間が記入するフォームではない。AIがコードや既存画面から推測できる項目は調査して埋める。人間へ確認するのは、答えによって Direction が実質的に変わる項目だけにする。
