目的：
このノートで「今チェックされているソース」だけを根拠に、後工程（Gemini Canvas / Googleスライド）で
社内共有向けの“編集可能スライド”を作るための SlideSpec（設計図）を Data Table として作る。

絶対ルール：

- 根拠は「チェックされているソースのみ」。推測禁止。不明は不明と明記。
- 1スライド=1メッセージ（結論/主張）。slide_title は名詞句NG、言い切り。
- 1スライドの要点は最大3つ（bullets_1〜3）。短く。
- “機能しないUI（Prev/Next等のボタン風装飾）”は禁止（diagram_specにも書かない）。
- 図はSVG前提にしない。Googleスライドの「図形・線・矢印・テキストボックス」で再現できる粒度で diagram_spec を書く。
- スライド枚数は上限を決めない（情報量を落とさない）。ただし詰め込み禁止。
  - bulletsが3つに収まらない → スライドを分割
  - diagram_specのblocksが8個を超える → 図を単純化より“分割”を優先
  - 1枚で2つ以上の主張を扱わない

枚数ガード（必須）：

- 最低スライド枚数（=Data Table行数）は 12。
- もし初回出力が 12 行未満になったら、次を守って「増やして再出力」すること：
  - 情報量を落とさず、主張の単位でスライドを分割して行数を増やす
  - bulletsが3つに収まらない箇所、diagram_specのblocksが8を超える箇所を優先的に分割する
  - 再出力でも推測は禁止。不明は不明のまま

出力（Data Table列）：

1. slide_no（1,2,3...）
2. slide_title（結論/主張を1行。言い切り）
3. one_liner（30文字以内）
4. bullets_1（40文字以内）
5. bullets_2（40文字以内）
6. bullets_3（40文字以内）
7. example（現場適用例。60文字以内）
8. layout（次から1つ：2_split_contrast / 3_column_air / 4_grid_matrix / timeline_flow / mechanism_diagram / text_only）
9. diagram_spec（図形で再現できるレベルの指示。必ず以下の形式で書く）
   - blocks: [ {id, label, shape(rect|rounded|pill), emphasis(true|false)} ... ]
   - arrows: [ {from, to, label(optional), type(arrow|line)} ... ]
   - notes: [ {target, text} ... ]
10. speaker_notes（発表者向け補足。任意）
11. sources（必須。根拠：ソース名 + 節番号。複数可）

品質ゲート（出力前セルフチェック）：

- 先頭に「想定スライド枚数（=行数）」を1行で宣言してから、Data Tableを出力したか
  例：想定スライド枚数：18
- 全行に sources が入っているか（空欄禁止）
- slide_title が結論の言い切りになっているか（名詞句になっていないか）
- bullets が各行3つ以内か（超える論点は分割できているか）
- diagram_spec が「図形で作れる粒度」か（UI装飾になってないか）
- diagram_spec の blocks が 8 を超えていないか（超えるなら分割したか）
