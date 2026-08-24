# UI/UX QA チェックリスト

## Task completion

- 主要タスクがすぐ理解できる
- 主操作が視覚的・意味的に明確
- 副操作が不必要に競合しない
- 不要な判断とステップが取り除かれている

## 情報の階層

- 重要な情報が二次情報より先に見える
- 見出しとグループが利用者のタスクを反映している
- 密度の高い情報も一覧しやすい
- 有効な箇所で Progressive disclosure を使っている

## データ耐性

- 現実的なデータで確認した
- 長いテキストで成立する
- 長いラベルで成立する
- 多い行で成立する
- 多い Filter で成立する
- 空データで成立する
- Overflow と折り返しが意図どおり

## 状態

- Loading
- Empty
- Error
- Validation error
- Success
- Disabled
- Read only
- 権限なし
- Hover
- Active
- Focus

機能に関係するすべての状態を確認する。

## Responsive

- Desktop
- 狭い Desktop / Tablet
- 対象なら Mobile
- Zoom・狭い Viewport で必須機能が失われない

## Accessibility

- Keyboard だけで主要フローが完了する
- Focus が見える
- Focus が隠れない
- Label がある
- エラーが入力と関連付いている
- Status が伝わる
- Contrast が十分
- 色だけに意味を持たせていない
- 十分なターゲットサイズ
- Reduced motion に対応

## Visual quality

- Spacing のリズムが一貫している
- 整列が意図的
- Typography の階層が明確
- 密度が Surface に合っている
- Components に統一感がある
- 装飾に理由がある
- 無思考な汎用AIテンプレ風に見えない

## Regression

- 既存の必要機能が残っている
- 関連画面・Components を壊していない
- 既存テストが通る
- 基盤があれば Visual regression を確認する

## 最終批評

次の順で見直す。

1. Task completion
2. 情報の階層
3. 一貫性と密度
4. 状態と Accessibility
5. Visual の独自性
