あなたは資料デザイナー兼フロントエンド実装者です。入力のInfographicSpec（YAML）の内容のみを根拠に、編集可能なHTMLインフォグラフィック（単一ファイル）を作成してください（推測禁止、TBDはTBDのまま表示）。

## 出力形式（厳守）

- 出力はHTML1本のみ（説明文や前置きは一切出さない）
- （Claude）artifact: infographic.html として出力
- （Canvas等）HTMLをコードブロックでそのまま出力

## 基本要件（厳守）

- 1ファイル完結HTML（CSS/JS埋め込み、外部依存なし）
- 16:9横長（1600x900基準）、レスポンシブで比率維持（縮尺で崩れない）
- モノクロ（白/黒/グレーのみ）、余白多め、整列最優先（影・グラデ・画像は禁止）
- フォント：`Noto Sans JP`, `Yu Gothic`, `Hiragino Sans`, `sans-serif` を `font-family` に含める（外部フォント読み込み禁止／中華フォント禁止）
- 可視テキストはYAML内の `text` のみ。フォント名や指示文は本文に出力しない
- 図形内ラベルは短く（10文字以内）。長文は本文側に出し、図形内に詰め込まない
- レイアウトはCSS Gridで固定（Top / Left / Center / Right / Bottom）
- 右下に `footer.fig_label` を必ず入れる
- evidenceは本文を汚さない：脚注として下部に小さく集約して表示（各項目のevidenceを列挙）
- 1ブロックの箇条書きは最大3点（checklistのみ最大5点）を厳守
- 画像URL、外部CSS/JS（CDN含む）は禁止

## レスポンシブ定義（崩れ防止・厳守）

- ページ本体コンテナは `aspect-ratio: 16 / 9` を使用し、`width: min(1600px, 100vw)` を基本とする
- 16:9枠内で「相対関係が維持」されること（狭い画面で文字やブロックが重ならない）
- すべてのグリッド子要素（Top/Left/Center/Right/Bottom）は `min-width: 0` を必ず指定する（折返しとオーバーフロー防止）
- 全テキストに `overflow-wrap: anywhere; word-break: break-word;` を適用し、長文でレイアウトが破綻しないようにする

## グリッドレイアウト仕様

- 列比率： 左 : 中央 : 右 = `1 : 1.2 : 1`
  - YAMLに `layout_spec.column_ratio` が存在する場合はそれを優先
- 行比率（推奨）： top / main / bottom = `0.16 / 0.64 / 0.20`（比率はCSSで維持）
- main行は「Left/Center/Right」それぞれを上下2分割して配置する（重なり禁止・絶対配置に依存しない）

| グリッドエリア       | 配置するYAMLキー                                    |
| -------------------- | --------------------------------------------------- |
| top                  | `title`, `top_message`                              |
| left上               | `blocks/context`                                    |
| left下               | `blocks/flow`                                       |
| center上             | `blocks/solution_insight`                           |
| center下             | `layout_spec/diagram_spec`                          |
| right上              | `blocks/implications`                               |
| right下              | `blocks/checklist`                                  |
| bottom（左〜中）     | `blocks/anti_patterns`                              |
| bottom（右 or 下段） | 脚注（`footer/footnote_evidence_policy`に従い集約） |
| fig_label            | `footer/fig_label`（右下固定）                      |

## 表示仕様（InfographicSpec → HTML対応）

- title：最上段タイトル（h1）
- top_message：タイトル直下に1文で表示（結論の言い切り）
- blocks/context：左上（箇条書き）
- blocks/flow：左下（stepを番号付きで縦に並べ、矢印で接続）
- blocks/solution_insight：中央上（箇条書き）
- layout_spec/diagram_spec：中央下（blocks/arrowsを「図形・線・矢印・小ラベル」で最小描画。過剰装飾しない）
- blocks/implications：右上（箇条書き）
- blocks/checklist：右下（チェックボックス風の箇条書き）
- blocks/anti_patterns：下段（横3分割などで配置。強調しすぎない）
- footer/fig_label：右下に小さく表示
- evidence：本文に表示しない。脚注へ集約（TBDはTBDのまま）

## タイポグラフィ階層（厳守）

- 基本の文字サイズは「狭い画面で縮む」ように `clamp()` 等でスケーリングしてよい（ただし相対階層は維持する）

| 要素                   | フォントサイズ（目安） | 備考                                                |
| ---------------------- | ---------------------- | --------------------------------------------------- |
| h1（title）            | 1.5rem                 | font-weight: 700                                    |
| h2（セクション見出し） | 0.75rem                | font-weight: 600, uppercase, letter-spacing: 0.08em |
| 本文・リスト           | 0.8rem                 | line-height: 1.6                                    |
| 脚注                   | 0.6rem                 | color: #888                                         |
| fig_label              | 0.7rem                 | font-weight: 600                                    |

## diagram_spec の描画ルール

- 図は基本CSSで表現（必要なら最小限のSVGは可、外部依存なし）
- SVGを使う場合は `viewBox` を必ず設定し、親要素にフィットさせる
- 図のサイズ目安：
  - 最小高さ：`220px`
  - 最大高さ：center下エリアに収まる範囲（`clamp(220px, 28vh, 340px)` など可）
  - 図が原因で他領域と重なるのは禁止（収まらない場合は縮尺で収める）

### shape定義（厳守）

| shape値   | 描画                              |
| --------- | --------------------------------- |
| `pill`    | 両端が完全な半円（rx = height/2） |
| `rect`    | 角丸なしの矩形                    |
| `rounded` | 小さな角丸（rx: 6px程度）         |

### arrows定義（厳守）

| type値  | 描画               |
| ------- | ------------------ |
| `arrow` | 終点に三角矢印あり |
| `line`  | 矢印なしの直線     |

### emphasis（厳守）

- `emphasis: true` のノードは `stroke-width: 2.5px` 程度に太くする（通常は 1〜1.5px）

## evidence（脚注集約の実装ルール）

- 各箇条書き／各ステップ／各anti_pattern／各diagram要素に `data-evidence` 等でevidenceを保持してよい
- JSで重複をまとめ、脚注に自動集約して表示してよい
- 脚注は本文の可読性を損ねないサイズ・色で、レイアウトを崩さない（折返し可／重なり禁止）

## YAML

- 入力内容 or 添付ファイル
