このノートで「今チェックされているソース」だけを根拠に、推測せずに回答してください。不明はTBDにしてください。

目的：
横長16:9の“社内共有向けインフォグラフィック”を、後工程（Gemini Canvas / Claude Artifacts）で編集可能なHTMLとして生成するための設計図（InfographicSpec）を作る。

絶対ルール：

- 根拠はチェックされているソースのみ。本文にない断定は禁止。
- 1枚=1メッセージ（top_messageは結論の言い切り1文）
- 各ブロックの箇条書きは最大3点（checklistのみ最大5点）
- 各項目に必ず根拠（ファイル名 + 節番号）を付ける
- 図形は「四角/角丸/線/矢印/小ラベル」で表現できる粒度にする（装飾やアイコン前提は禁止）
- diagram_spec の label は10文字以内。長い文は blocks に出し、図形内に詰め込まない
- 図形内ラベルは短語に限定（必要ならA/B/Cなどで簡略化し、意味は本文側に書く）

出力形式（YAML、キー順固定、コードブロックで）：

```yaml
title:
top_message:
blocks:
  context:
    items:
      - text:
        evidence:
  flow:
    steps:
      - label:
        text:
        evidence:
  solution_insight:
    items:
      - text:
        evidence:
  implications:
    items:
      - text:
        evidence:
  checklist:
    items:
      - text:
        evidence:
  anti_patterns:
    items:
      - text:
        evidence:
layout_spec:
  grid:
    - area: top
      description:
    - area: left
      description:
    - area: center
      description:
    - area: right
      description:
    - area: bottom
      description:
  diagram_spec:
    blocks:
      - id:
        label:
        shape: rounded|rect|pill
        emphasis: true|false
    arrows:
      - from:
        to:
        label:
        type: arrow|line
footer:
  fig_label: 'FIG. 01 / Claude Code'
  footnote_evidence_policy: '各項目のevidenceを脚注に集約（重複はまとめる）'
quality_gate:
  - 'top_messageが結論の言い切りになっている'
  - '各items/stepsにevidenceが入っている'
  - '推測がない（TBDで止めている）'
  - 'diagram_specが過剰装飾前提になっていない'
```
