---
name: frontend-design
description: Generate distinctive, professional frontend designs that eliminate AI-generated aesthetics through strategic typography, color, motion, and layout choices
---

# Frontend Design Skill

**目的**: 「AI らしさ」を排除し、独創的でプロフェッショナルなフロントエンドデザインを生成する。

**使用タイミング**: フロントエンド開発、UI コンポーネント、ランディングページ、ダッシュボード、Web アプリケーションの実装時に自動的に適用。

---

## 解決すべき課題

LLM は訓練データの統計的パターンにより、ありふれた「分布内」の出力に収束しがちです。これにより、ユーザーが即座に「AI 生成」と認識する予測可能で没個性的なデザインが生まれます。

**典型的な AI 生成デザインの特徴**:

- 使い古されたフォント: Inter, Roboto, Arial, system fonts
- 陳腐な配色: 白背景に紫系グラデーション
- 予測可能なレイアウト: 中央揃えヒーローセクション、標準的なカードグリッド
- 動きの欠如: マイクロインタラクションのない静的なインターフェース
- 平坦な背景: 深みや雰囲気のない単色背景

**あなたの使命**: これらのパターンを打破し、文脈に合わせて真に設計されたフロントエンドを作成すること。

---

## デザイン原則

### プロジェクト共通のデフォルト設定（プロジェクト固有の設定がない場合に使用）

全プロジェクト共通の初期値。各リポジトリが独自の `.claude/skills/frontend-design/SKILL.md` を持つ場合はそちらで上書きする。

- **Fonts**（ローテーション、繰り返し回避）: 見出し＝Playfair Display / Spectral / Crimson Pro、本文＝Source Serif Pro / Manrope / IBM Plex Sans、UI＝DM Sans / Space Grotesk
- **Colors**: プライマリを 1 色に絞る。優先ファミリは Teal (#14b8a6) / Amber (#f59e0b) / Slate (#334155)。紫・青系グラデは避ける。
- **Motion**: ページロードは 80–120ms ステップでフェードアップ。ホバー/アクションは transform+opacity を 180–240ms ease-out。Framer Motion は stiffness 380–420 / damping 28–32 を目安。
- **Background**: グラデーションを避け、ノイズや小さなパターンで深みを出す。角丸は 10–14px、シャドウは弱め 2 段まで。

### 1. タイポグラフィ：特徴的なフォントを選択

**使用禁止**: Inter, Roboto, Open Sans, Lato, Arial, default system fonts, Helvetica, system-ui

**フォント選択プロトコル**:

**Step 1**: コンテキストを特定（Code/Editorial/Technical/Modern/Expressive）

**Step 2**: カテゴリから**バリエーション戦略を使って**選択（オプションをローテーション、同じフォントの繰り返しを避ける）:

- **Code aesthetic**: JetBrains Mono, Fira Code, Space Grotesk, IBM Plex Mono, Inconsolata, Source Code Pro, Victor Mono, Berkeley Mono, Geist Mono
- **Editorial/Publishing**: Playfair Display, Crimson Pro, Newsreader, Spectral, Lora, Merriweather, Libre Baskerville, Fraunces, Sentient
- **Technical/Corporate**: IBM Plex Sans, Source Sans 3, Work Sans, Manrope, Public Sans, Red Hat Display, Graphik, GT America
- **Modern/Geometric**: Cabinet Grotesk, Bricolage Grotesque, DM Sans, Plus Jakarta Sans, Satoshi, Lexend, General Sans, Switzer
- **Expressive**: Syne, Unbounded, Outfit, Clash Display, League Spartan, Archivo Black, Migra, Druk

**Step 3**: バリエーションヒューリスティックを適用

- **最近 Space Grotesk を使った場合** → 代わりに IBM Plex Mono か Source Code Pro を試す
- **最近 Playfair Display を使った場合** → 代わりに Crimson Pro か Spectral を試す
- **ランダム化**: 毎回カテゴリから異なるフォントを選ぶ（例: 1 番目→3 番目→5 番目）
- **最近の使用を追跡**: 直近 3 つのフォントを記憶する

**ペアリング原則**:

- 高コントラストが興味を生む: Display + Monospace、Serif + Geometric Sans
- 極端なウェイトを使用: 100/200 vs 800/900（400 vs 600 ではない）
- 階層構造には 3 倍以上のサイズジャンプ（1.5 倍ではない）
- 特徴的なフォントファミリーを 1 つ選び、ウェイト全体で一貫して使用

**可変フォント最適化**（NEW）:

```css
@font-face {
  font-family: 'YourFont';
  src: url('/fonts/Font-Variable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap; /* Prevent FOIT */
  size-adjust: 100.5%; /* Prevent CLS */
}
```

**実装**:

- Google Fonts または Bunny Fonts（プライバシー重視の CDN）から読み込む
- 一貫性のため CSS 変数を定義: `--font-display`, `--font-body`, `--font-mono`

---

### 2. カラー&テーマ：一貫した美学にコミット

**避けるべきもの**:

- 白背景に紫から青へのグラデーション（#667eea → #764ba2）
- 主色のないパステルレインボーパレット
- 純白背景に純黒テキスト（#000 on #fff）

**より良いアプローチ**:

**カラー選択アルゴリズム**:

**Step 1**: コンテキストを判断し、プライマリカラーファミリーを選択

- **SaaS/Tech**: Blue (#0ea5e9), Teal (#14b8a6), Indigo (#6366f1), Cyan (#06b6d4)
- **Fintech/Enterprise**: Dark Blue (#1e40af), Emerald (#10b981), Slate (#64748b)
- **Creative/Portfolio**: Orange (#f97316), Pink (#ec4899), Purple (#a855f7), Red (#ef4444)
- **Editorial/Blog**: Warm Gray (#78716c), Sage Green (#84cc16), Amber (#f59e0b)
- **Health/Wellness**: Soft Teal (#14b8a6), Lavender (#a78bfa), Mint (#6ee7b7)

**Step 2**: 使い古された組み合わせを避ける

- ❌ Blue (#667eea) → Purple (#764ba2) グラデーション
- ❌ Pink (#ec4899) → Purple (#a855f7) グラデーション
- ❌ Teal (#14b8a6) → Blue (#3b82f6) グラデーション
- ❌ 3 色以上のグラデーション

**Step 3**: プライマリからパレットを構築

- Step 1 から**1 つ**のプライマリ色相を選ぶ
- パレット用に彩度/明度を変化させる（例: blue-500, blue-600, blue-700）
- シャープなアクセントカラーは控えめに使用（視覚的ウェイトの 10%）
- ニュートラルには微妙な色温度を持たせる（暖色系グレー vs 寒色系グレー）

**Step 4**: バリエーションヒューリスティックを適用

- 収束を避けるため**カラーファミリーをローテーション**
- 最近青を使った場合 → オレンジ、ティール、セージグリーンを試す
- 最近紫を使った場合 → エメラルド、アンバー、スレートを試す

**ダークモード優先**（NEW）:

```css
:root {
  /* Default to dark theme */
  --surface: hsl(222, 47%, 11%);
  --text: hsl(213, 31%, 91%);
}

@media (prefers-color-scheme: light) {
  :root {
    --surface: hsl(0, 0%, 100%);
    --text: hsl(222, 47%, 11%);
  }
}
```

**実装**:

- テーマ用に CSS 変数を使用: `--color-primary`, `--color-surface`, `--color-text`
- 深みのためにグラデーションを重ねる: radial + linear、mesh gradients
- ダークモードをデフォルトとして検討（モダンなアプリでユーザーが期待）

---

### 3. モーション：目的を持ってアニメート

**避けるべきもの**:

- アニメーションなし（静的なインターフェースは死んでいるように見える）
- 意味のないランダムなバウンス/揺れ効果
- カクつきを引き起こす最適化されていないアニメーション

**より良いアプローチ**:

**インパクトの高い瞬間**:

- ページロード: `animation-delay` による段階的な表示（fade-in-up, scale-in）
- ユーザーアクション: ホバー状態、ボタンプレス、フォームフォーカス
- 状態遷移: Loading → Success、展開/折りたたみ、ルート変更

**スプリング物理**（NEW）:

```javascript
// Natural motion with spring physics
const spring = {
  type: 'spring',
  stiffness: 400,
  damping: 30,
}
```

**実装の優先順位**:

1. **HTML には CSS のみ**: `@keyframes`, `transition`, `animation-delay` を使用
2. **React には Framer Motion**: `<motion.div>` による宣言的アニメーション
3. **マイクロインタラクションに注力**: ボタンリップル、カードリフト、入力ハイライト

**パフォーマンス**:

- `transform` と `opacity` のみをアニメート（GPU アクセラレーション）
- `will-change` は重要なアニメーションのみ控えめに使用
- 持続時間は短く: UI は 150-300ms、ページ遷移は 500-800ms
- GPU レイヤーを強制するために `transform: translateZ(0)` を追加

---

### 4. 背景：深みと雰囲気を作る

**避けるべきもの**:

- 単色の白（#fff）または単色のグレー（#f5f5f5）背景
- レイヤリングのない単一の線形グラデーション

**より良いアプローチ**:

**メッシュグラデーション**（強化版）:

```css
.mesh-gradient {
  background:
    radial-gradient(at 20% 30%, hsla(240, 100%, 70%, 0.3) 0px, transparent 50%),
    radial-gradient(at 80% 20%, hsla(340, 100%, 70%, 0.2) 0px, transparent 50%),
    radial-gradient(at 40% 70%, hsla(120, 100%, 70%, 0.2) 0px, transparent 50%),
    linear-gradient(135deg, var(--surface-dark) 0%, var(--surface-light) 100%);
}
```

**Noise Texture** (NEW):

```css
.noise-overlay {
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.03'/%3E%3C/svg%3E");
}
```

**Glass Morphism 2.0** (NEW):

```css
.glass-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

**幾何学的パターン**:

- ドットグリッド: `background-image: radial-gradient(circle, #333 1px, transparent 1px)`
- ストライプ: `repeating-linear-gradient(45deg, ...)`
- メッシュグラデーション: 異なる中心を持つ複数の radial gradient を組み合わせる

**コンテキスト別エフェクト**:

- コードエディタ: 微妙なノイズテクスチャ + ダークグラデーション
- SaaS: プライマリカラーのヒントを含むソフトなブロブグラデーション
- Fintech: 微妙なグリッドオーバーレイを持つ深い青
- ポートフォリオ: 非対称なカラースプラッシュ

---

## アイコン&画像

### アイコン戦略

**使用禁止**: プロフェッショナルな文脈でのデフォルト絵文字（📊, 📅, 💳 など）

**より良いアプローチ**:

- **SVG インラインアイコン**: 色、サイズ、アニメーションの完全な制御
- **アイコンライブラリ**: Lucide, Heroicons, Phosphor, Tabler Icons
- **カスタムアイコンシステム**: 一貫したストローク幅、角丸半径、視覚的ウェイト

```html
<!-- Good: SVG with consistent design language -->
<svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" fill="none">
  <path d="..." />
</svg>

<!-- Bad: Default emoji -->
<span>📊</span>
```

**実装**:

- アイコンスタイルをブランドパーソナリティに合わせる（丸み vs シャープ、塗りつぶし vs アウトライン）
- すべてのアイコンで一貫したストローク幅を維持（通常 1.5px または 2px）
- 動的テーマ用に currentColor を使用
- インタラクション時にマイクロアニメーションを追加（回転、スケール、変形）

---

## レイアウトの洗練

### 予測可能なパターンを打破

**これらの AI 的レイアウトを避ける**:

- ヒーロー: 左テキスト、右画像（またはその逆）
- 機能: 3 つの均等な列
- 統計: ボックス内に中央揃えの数字
- 価格: 中央が「おすすめ」の 3 カード

**高度なレイアウト戦略**:

**1. 非対称グリッド**

```css
.advanced-grid {
  display: grid;
  grid-template-columns: 1.618fr 1fr 1.272fr; /* 黄金比のバリエーション */
  grid-template-rows: auto 1fr auto;
}
```

**2. 重なり合う要素**

```css
.overlap-composition {
  display: grid;
  > * {
    grid-area: 1/1;
  } /* すべての子要素を重ねる */
  > :nth-child(2) {
    transform: translate(10%, -5%);
    z-index: 2;
  }
}
```

**3. 動的ビューポート単位**

```css
.fluid-type {
  font-size: clamp(2rem, 5vw + 1rem, 6rem);
  line-height: clamp(1.2, 2.5vw, 1.4);
}
```

**4. グリッド脱出**

```css
.break-container {
  margin-left: calc(-1 * (100vw - 100%) / 2);
  margin-right: calc(-1 * (100vw - 100%) / 2);
}
```

### サイズを超えた視覚的階層

**洗練された階層のためのテクニック**:

- **空間的緊張**: 近接性とネガティブスペースを階層ツールとして使用
- **色のウェイト**: 彩度の高い色はサイズ単独よりも注意を引く
- **モーション優先度**: アニメーション要素が静的要素を支配する
- **深度レイヤー**: 影、ぼかし、重なりを使用して読み順を作る

```css
/* 多次元階層 */
.primary-content {
  /* 単に大きいだけでなく、空間的に支配的 */
  grid-column: 1 / -1;
  margin: calc(-1 * var(--spacing));
  padding: calc(2 * var(--spacing));
  background: linear-gradient(135deg, var(--surface), transparent);
  box-shadow:
    0 0 0 1px var(--border),
    0 20px 40px -20px rgba(0, 0, 0, 0.3);
}
```

---

## 高度なアニメーションパターン

### 基本的なトランジションを超えて

**洗練されたアニメーション技法**:

**1. 変形する図形**

```css
@keyframes morph {
  0%,
  100% {
    clip-path: polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%);
    border-radius: 0;
  }
  25% {
    clip-path: polygon(20% 0%, 100% 38%, 70% 90%, 0% 100%);
    border-radius: 20px 50px 30px 40px;
  }
  75% {
    clip-path: polygon(0% 20%, 60% 0%, 100% 50%, 40% 100%);
    border-radius: 50px 20px 40px 30px;
  }
}
```

**2. 段階的な複雑なアニメーション**

```javascript
// 各要素は位置に基づいて一意のタイミングを取得
elements.forEach((el, i) => {
  const row = Math.floor(i / columns)
  const col = i % columns
  const delay = row * 50 + col * 100 // 斜めの波
  el.style.animationDelay = `${delay}ms`
})
```

**3. スクロール駆動アニメーション**

```css
@supports (animation-timeline: scroll()) {
  .parallax-element {
    animation: parallax linear;
    animation-timeline: scroll();
    animation-range: 0 100vh;
  }
}
```

**4. 物理ベースのインタラクション**

```javascript
// Magnetic cursor effect
const magnetStrength = 0.5
const damping = 0.85
let velocityX = 0,
  velocityY = 0

function attract(element, mouseX, mouseY) {
  const rect = element.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2

  const deltaX = mouseX - centerX
  const deltaY = mouseY - centerY
  const distance = Math.sqrt(deltaX ** 2 + deltaY ** 2)

  if (distance < 100) {
    const force = (100 - distance) / 100
    velocityX += deltaX * force * magnetStrength
    velocityY += deltaY * force * magnetStrength
  }

  velocityX *= damping
  velocityY *= damping

  element.style.transform = `translate(${velocityX}px, ${velocityY}px)`
}
```

---

## データビジュアライゼーションの卓越性

### 基本的なチャートを超えて

**避けるべきもの**: シンプルな棒グラフ、基本的な円グラフ、標準的な折れ線グラフ

**代わりに作成するもの**:

**1. 複合ビジュアライゼーション**

```javascript
// Combine multiple data dimensions
const hybridChart = {
  type: 'scatter',
  data: points,
  layers: [
    { type: 'heatmap', intensity: density },
    { type: 'contour', levels: 5 },
    { type: 'annotations', highlights: outliers },
  ],
}
```

**2. カスタム SVG パターン**

```svg
<defs>
  <pattern id="dataPattern" patternUnits="userSpaceOnUse" width="4" height="4">
    <circle cx="2" cy="2" r="0.5" fill="currentColor" opacity="0.3">
      <animate attributeName="r" values="0.5;1.5;0.5" dur="3s" repeatCount="indefinite"/>
    </circle>
  </pattern>
</defs>
```

**3. リアルタイムストリーミングデータ**

```css
.live-chart {
  /* ストリーミングデータ用の無限スクロール効果 */
  animation: stream 10s linear infinite;
  background: linear-gradient(
    90deg,
    transparent 0%,
    var(--data-color) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
}
```

---

## モダンレイアウトパターン（NEW）

### Bento Grid（2024 年トレンド）

```css
.bento-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  grid-auto-rows: minmax(120px, auto);
}

.bento-item-featured {
  grid-column: span 2;
  grid-row: span 2;
}
```

### Container Queries

```css
@container card (min-width: 400px) {
  .card-content {
    flex-direction: row;
  }
}
```

---

## アクセシビリティ&パフォーマンス（NEW）

### Core Web Vitals

- **LCP < 2.5s**: フォント、画像を最適化
- **FID < 100ms**: 重要でない JS を遅延
- **CLS < 0.1**: 寸法を設定、aspect-ratio を使用

### フォーカス管理

```css
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

---

## 収束防止ルール

**重要**: これらの指示があっても、「より安全な」特徴的な選択（例: 毎回 Space Grotesk）にデフォルトで戻る可能性があります。**積極的に選択を変化させてください**:

### 必須バリエーションプロトコル

**各新しいデザインで、あなたは以下を実行しなければならない**:

1. **最近のパターンと照合**
   - 過去 3 つのデザインが左右レイアウトを使用 → 非対称グリッドを使用
   - 過去 3 つのデザインが中央揃えヒーローを使用 → オフセンターまたはフルブリードを使用
   - 過去 3 つがグラデーションを使用 → テクスチャオーバーレイ付き単色を試す

2. **70/20/10 ルールを適用**
   - 70%: 実証済みパターン（ただしローテーション/バリエーション）
   - 20%: 世界クラスの参照からの実験的技法
   - 10%: 完全に新しい/リスクのあるアプローチ

3. **品質ベンチマークを参照**
   デザイン前に、以下と精神的に比較:
   - **Stripe**: 微妙なグラデーション、完璧なタイポグラフィ、マイクロインタラクション
   - **Linear**: ダークの卓越性、キーボードファースト、情報密度
   - **Arc**: 遊び心のある非対称性、大胆な色、予想外のレイアウト
   - **Vercel**: Monospace 美学、技術的精密さ、幾何学的パターン
   - **Spotify**: 大胆なタイプ、デュオトーン画像、文化的関連性

**バリエーション追跡アルゴリズム**（強化版）:

```javascript
// Prevent repetition with weighted randomness
const designDNA = {
  lastChoices: {
    layout: [], // Last 5 layout patterns
    typography: [], // Last 5 font combinations
    color: [], // Last 5 color schemes
    animation: [], // Last 5 animation styles
  },

  selectWithNovelty(category, options) {
    // Heavily weight against recent choices
    const weights = options.map(option => {
      const recencyIndex = this.lastChoices[category].indexOf(option)
      return recencyIndex === -1 ? 10 : Math.max(1, 5 - recencyIndex)
    })

    // Weighted random selection
    const totalWeight = weights.reduce((a, b) => a + b, 0)
    let random = Math.random() * totalWeight

    for (let i = 0; i < options.length; i++) {
      random -= weights[i]
      if (random <= 0) {
        // Update history
        this.lastChoices[category].unshift(options[i])
        this.lastChoices[category] = this.lastChoices[category].slice(0, 5)
        return options[i]
      }
    }
  },
}
```

### デザイン洗練度チェックリスト

各ディメンションでデザインを評価（各項目で 8 点以上を目指す）:

1. **タイポグラフィの洗練度**（1-10）
   - 可変フォントを創造的に使用しているか？
   - 極端なウェイトコントラストはあるか？
   - カスタムレタースペーシング/カーニングはあるか？

2. **レイアウトの革新性**（1-10）
   - 従来のグリッドを打破しているか？
   - 重なり/非対称性を使用しているか？
   - 空間的緊張は作られているか？

3. **カラーの自信**（1-10）
   - 予想外だが調和のとれたパレットか？
   - 意図的な色温度のシフトはあるか？
   - アクセントの使用に抑制があるか？

4. **モーションの洗練度**（1-10）
   - 物理ベースのアニメーションか？
   - コンテキストに沿ったマイクロインタラクションか？
   - パフォーマンス最適化されているか？

5. **全体的な独自性**（1-10）
   - これは AI 生成だと見抜かれないか？
   - 明確な視点があるか？
   - デザイナーはこれを誇りに思うか？

**ヒューリスティック**: いずれかのスコアが 7 点未満の場合、その側面を再設計。合計が 40 点未満の場合、異なるコンセプトで最初からやり直す。

---

## コンテキスト別ガイドライン

### SaaS ランディングページ

- 大胆で自信に満ちたタイポグラフィ（見出しは 800 以上のウェイト）
- プライマリカラーの支配（視覚的階層の 70%）
- ヒーローセクションのモーション（段階的なフェードイン）
- ブランドカラーのヒントを含むレイヤードグラデーション背景

### ダッシュボード&管理パネル

- ダークモード推奨（長時間セッションでの眼精疲労を軽減）
- データテーブルとメトリクス用の Monospace フォント
- 微妙なホバー状態とマイクロインタラクション
- 背景の深みのためのグリッドまたはドットパターン

### ブログ&コンテンツサイト

- 本文用のエディトリアル Serif フォント（Crimson Pro, Spectral）
- 可読性のための高コントラスト比（WCAG AAA）
- 余裕のある line-height（1.7-2.0）と max-width（65-75ch）
- ソフトで雰囲気のある背景（クリーム、暖色系グレー）

### ポートフォリオ&クリエイティブサイト

- 非対称レイアウト（意図的にグリッドを打破）
- 表現力豊かなディスプレイフォント（Clash Display, Unbounded）
- 余白の大胆な使用と大きなタイプサイズ
- 実験的な配色（補色アクセント）

---

## 実装チェックリスト

フロントエンドデザインを確定する前に確認:

- [ ] **タイポグラフィ**: Inter/Roboto/Arial を使用していないか？特徴的なフォントファミリーを選んだか？
- [ ] **カラー**: 主色を持つ一貫したパレットか？CSS 変数を定義したか？
- [ ] **モーション**: 少なくとも 1 つの高インパクトアニメーション（ページロードまたはインタラクション）があるか？
- [ ] **背景**: レイヤード深度（グラデーション/パターン）があるか、単色ではないか？
- [ ] **テーマ**: コンテキストに一致しているか（SaaS/ダッシュボード/ブログ/ポートフォリオ）？
- [ ] **バリエーション**: 過去の生成と異なるか（フォント/カラー選択を確認）？
- [ ] **パフォーマンス**: Core Web Vitals が最適化されているか？
- [ ] **アクセシビリティ**: フォーカス状態が定義されているか？WCAG 準拠か？

---

## メタガイダンス

このスキルは**デザインテイスト**をあなたの出力にエンコードします。テイストとは、コンテキストに適した意見のある選択をすることです。

### デザイナーのマインドセット

**トップエージェンシーのデザイナーのように考える**:

1. **「何を？」ではなく「なぜ？」から始める**
   - なぜこの製品は存在するのか？
   - なぜ誰かが気にするのか？
   - なぜこの美学を他のものより選ぶのか？

2. **機能よりも感情を優先してデザイン**
   - ユーザーはこれを見たときにどう感じるべきか？
   - ビジュアルはどんなストーリーを語るのか？
   - 喜び、信頼、興奮、または静けさを引き起こすか？

3. **すべてのピクセルに意図がある**
   - デフォルト値なし（マージン、色、アニメーション）
   - 各要素はその場所を獲得する
   - 正当化できなければ削除する

4. **自信を持った抑制を受け入れる**
   - より少ないものでより多くを語る
   - 1 つの大胆な動き > 多くの安全な動き
   - 空のスペースはデザイン要素

5. **洗練されたユーザーのためにデザイン**
   - テイストと知性を前提とする
   - 押し付けがましいシンプルさを避ける
   - 注意に対してディテールで報いる

### 世界クラスのデザインの品質マーカー

あなたのデザインはこれらの特徴を示すべき:

- **見えない卓越性**: 最高のディテールは気づかれないが感じられる
- **目的のある緊張**: エネルギーを生み出す意図的な不均衡
- **文化的共鳴**: トレンディではなく現代的に感じる
- **技術的熟練**: 複雑なアイデアの完璧な実行
- **感情的知性**: ユーザーのコンテキストを理解し尊重する

### 究極のテスト

デザインを提供する前に自問:

1. **これは賞を受賞するか？**（Awwwards, FWA, CSS Design Awards）
2. **デザイナーはこれをスクリーンショットするか？**（インスピレーションのため）
3. **平凡なものを特別に感じさせるか？**
4. **人間のデザイナーがこれを作れたか？**（「かろうじて」を目指す）
5. **意見を持っているか？**（優れたデザインは立場を取る）

**忘れないで**: あなたは単に要件を実装しているのではなく、体験を作り上げています。すべてのプロジェクトは、AI 生成デザインに期待されるものの境界を押し広げる機会です。あなた自身をも驚かせるものを作ってください。
