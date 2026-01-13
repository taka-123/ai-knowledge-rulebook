**【ホストの役割（視点設定）】**

- **ホストA（学習者視点）**: 教科書的な理論や定義を提示する役。
- **ホストB（PM視点）**: 「実務でのコスト判断」や「トレードオフ」の観点からコメントする役。

**【指示内容】**
アップロードされた資料に基づき、基本情報技術者試験の対策として、かつ**将来的なプロジェクトマネジメント（PM）視点**でも役立つ要約動画を作成してください。

**1. 情報源の本質**
この章が扱う技術が、システム全体のパフォーマンスや意思決定にどう影響するかという「上位レイヤーの視点」を盛り込んでください。

**2. 目的**
試験合格に必要な基礎知識の習得に加え、ステークホルダーへ技術的なトレードオフを説明する際の「論理的根拠」を学べる内容にすること。

**3. トーン**
効率化を重視するプロフェッショナル向けに、無駄を削ぎ落とした**方法的で、批判的思考（Critical Thinking）を含んだトーン**で解説してください。

**4. 視認性の確保**
画面上の元図版は小さく表示されるため、**右側のスライド（要約テキスト）だけで内容が完結するよう**、図表内の重要な数値や名称を省略せずテキスト化してください。

**5. Style & Typography Instructions (Critical)**

- **Font:** Japanese Gothic / Sans-Serif, bold, high legibility. (Do NOT render font names.)
- **Language Context:** Render strictly in **Standard Japanese Orthography** (Japan-standard Kanji strokes).
- **Negative Constraint:** Absolutely NO "Simplified Chinese" variants (Avoid Han Unification errors). NO garbled text, NO pseudo-text, NO decorative/handwritten fonts.
- **Quality:** Text must be "highly legible," "crisp," and "high-resolution vector style."

**6. Text Rendering Guardrails（文字化け回避）**

- **短く・大きく**: 1行12〜16文字程度、最大2行。長文は箇条書きで分割。
- **配置を明示**: 右側の要約テキスト領域に集約。
- **図形内に文字を埋め込まない**: 文字はテロップ/テキストボックスのみ。
- **図形内ラベルは英数字のみ**: A/B/C/1/2など1〜2文字に限定し、日本語は外側テキストへ。
- **指示文やフォント名を描画しない**: 内容テキストのみを出力。
- **引用符は描画しない**: 文字列は内部的に"..."で扱い、表示は引用符なし。
- **不確実な文字は置換**: 画数が多い漢字は、意味が変わらない範囲でひらがな/平易語に置換。
- **吹き出し/アイコン内の文字は禁止**: ラベルは外側のテキストボックス＋リーダー線で。
- **小さなスクリーンショット禁止**: 書籍ページ・UI・コード等の画像を貼らず、必要なら大きな簡略図に置き換える。
