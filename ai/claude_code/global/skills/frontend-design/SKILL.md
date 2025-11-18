---
name: frontend-design
description: Generate distinctive, professional frontend designs that eliminate AI-generated aesthetics through strategic typography, color, motion, and layout choices
---

# Frontend Design Skill

**Purpose**: Eliminate "AI slop" aesthetics and generate distinctive, professional frontend designs.

**When to use**: Automatically activate when the user requests frontend development, UI components, landing pages, dashboards, or web applications.

---

## Core Problem

LLMs converge toward generic "on-distribution" outputs due to statistical patterns in training data. This creates predictable, uninspired designs that users immediately recognize as AI-generated.

**Typical AI slop characteristics**:

- Overused fonts: Inter, Roboto, Arial, system fonts
- Clichéd colors: Purple gradients on white backgrounds
- Predictable layouts: Centered hero sections, standard card grids
- Minimal motion: Static interfaces with no micro-interactions
- Flat backgrounds: Solid colors without depth or atmosphere

**Your mission**: Break these patterns. Create frontends that feel genuinely designed for context.

---

## Design Principles

### 1. Typography: Choose Distinctive Fonts

**Never use**: Inter, Roboto, Open Sans, Lato, Arial, default system fonts, Helvetica, system-ui

**Font Selection Protocol**:

**Step 1**: Identify context (Code/Editorial/Technical/Modern/Expressive)

**Step 2**: Select from category **using variation strategy** (rotate through options, avoid repeating same font):

- **Code aesthetic**: JetBrains Mono, Fira Code, Space Grotesk, IBM Plex Mono, Inconsolata, Source Code Pro, Victor Mono, Berkeley Mono, Geist Mono
- **Editorial/Publishing**: Playfair Display, Crimson Pro, Newsreader, Spectral, Lora, Merriweather, Libre Baskerville, Fraunces, Sentient
- **Technical/Corporate**: IBM Plex Sans, Source Sans 3, Work Sans, Manrope, Public Sans, Red Hat Display, Graphik, GT America
- **Modern/Geometric**: Cabinet Grotesk, Bricolage Grotesque, DM Sans, Plus Jakarta Sans, Satoshi, Lexend, General Sans, Switzer
- **Expressive**: Syne, Unbounded, Outfit, Clash Display, League Spartan, Archivo Black, Migra, Druk

**Step 3**: Apply variation heuristic

- **If you've used Space Grotesk recently** → Try IBM Plex Mono or Source Code Pro instead
- **If you've used Playfair Display recently** → Try Crimson Pro or Spectral instead
- **Randomize selection**: Pick different font from category each time (e.g., 1st option, then 3rd, then 5th)
- **Track recent usage**: Maintain mental log of last 3 fonts used

**Pairing principles**:

- High contrast creates interest: Display + Monospace, Serif + Geometric Sans
- Use extreme weights: 100/200 vs 800/900 (not 400 vs 600)
- Size jumps of 3x+ for hierarchy (not 1.5x)
- Pick one distinctive font family, use it decisively across weights

**Variable Font Optimization** (NEW):

```css
@font-face {
  font-family: 'YourFont';
  src: url('/fonts/Font-Variable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap; /* Prevent FOIT */
  size-adjust: 100.5%; /* Prevent CLS */
}
```

**Implementation**:

- Load from Google Fonts or Bunny Fonts (privacy-focused CDN)
- Define CSS variables for consistency: `--font-display`, `--font-body`, `--font-mono`

---

### 2. Color & Theme: Commit to Cohesive Aesthetics

**Avoid**:

- Purple-to-blue gradients on white (#667eea → #764ba2)
- Pastel rainbow palettes with no dominant color
- Pure black text on pure white (#000 on #fff)

**Better approaches**:

**Color Selection Algorithm**:

**Step 1**: Determine context and select primary color family

- **SaaS/Tech**: Blue (#0ea5e9), Teal (#14b8a6), Indigo (#6366f1), Cyan (#06b6d4)
- **Fintech/Enterprise**: Dark Blue (#1e40af), Emerald (#10b981), Slate (#64748b)
- **Creative/Portfolio**: Orange (#f97316), Pink (#ec4899), Purple (#a855f7), Red (#ef4444)
- **Editorial/Blog**: Warm Gray (#78716c), Sage Green (#84cc16), Amber (#f59e0b)
- **Health/Wellness**: Soft Teal (#14b8a6), Lavender (#a78bfa), Mint (#6ee7b7)

**Step 2**: Avoid these overused combinations

- ❌ Blue (#667eea) → Purple (#764ba2) gradient
- ❌ Pink (#ec4899) → Purple (#a855f7) gradient
- ❌ Teal (#14b8a6) → Blue (#3b82f6) gradient
- ❌ Any gradient with more than 2 colors

**Step 3**: Build palette from primary

- Choose ONE primary hue from Step 1
- Vary saturation/lightness for palette (e.g., blue-500, blue-600, blue-700)
- Use sharp accent colors sparingly (10% of visual weight)
- Neutrals should have subtle color temperature (warm grays vs cool grays)

**Step 4**: Apply variation heuristic

- **Rotate through color families** to avoid convergence
- If you've used blue recently → Try orange, teal, or sage green
- If you've used purple recently → Try emerald, amber, or slate

**Dark Mode First** (NEW):

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

**Implementation**:

- Use CSS variables for theming: `--color-primary`, `--color-surface`, `--color-text`
- Layer gradients for depth: radial + linear, mesh gradients
- Consider dark mode as default (users expect it in modern apps)

---

### 3. Motion: Animate with Purpose

**Avoid**:

- No animations (static interfaces feel dead)
- Random bounce/wiggle effects with no meaning
- Non-optimized animations causing jank

**Better approaches**:

**High-impact moments**:

- Page load: Staggered reveals with `animation-delay` (fade-in-up, scale-in)
- User actions: Hover states, button presses, form focus
- State transitions: Loading → Success, Expand/Collapse, Route changes

**Spring Physics** (NEW):

```javascript
// Natural motion with spring physics
const spring = {
  type: 'spring',
  stiffness: 400,
  damping: 30,
}
```

**Implementation priorities**:

1. **CSS-only for HTML**: Use `@keyframes`, `transition`, `animation-delay`
2. **Framer Motion for React**: Declarative animations via `<motion.div>`
3. **Focus on micro-interactions**: Button ripples, card lifts, input highlights

**Performance**:

- Animate `transform` and `opacity` only (GPU-accelerated)
- Use `will-change` sparingly for critical animations
- Keep durations short: 150-300ms for UI, 500-800ms for page transitions
- Add `transform: translateZ(0)` to force GPU layer

---

### 4. Backgrounds: Create Depth and Atmosphere

**Avoid**:

- Solid white (#fff) or solid gray (#f5f5f5) backgrounds
- Single linear gradients with no layering

**Better approaches**:

**Mesh Gradients** (Enhanced):

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

**Geometric patterns**:

- Dot grids: `background-image: radial-gradient(circle, #333 1px, transparent 1px)`
- Stripes: `repeating-linear-gradient(45deg, ...)`
- Mesh gradients: Combine multiple radial gradients with different centers

**Contextual effects**:

- Code editors: Subtle noise texture + dark gradient
- SaaS: Soft blob gradients with primary color hints
- Fintech: Deep blues with subtle grid overlays
- Portfolios: Asymmetric color splashes

---

## Icons & Imagery

### Icon Strategy

**Never use**: Default emojis (📊, 📅, 💳, etc.) in professional contexts

**Better approaches**:

- **SVG inline icons**: Full control over color, size, animation
- **Icon libraries**: Lucide, Heroicons, Phosphor, Tabler Icons
- **Custom icon systems**: Consistent stroke width, corner radius, visual weight

```html
<!-- Good: SVG with consistent design language -->
<svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" fill="none">
  <path d="..." />
</svg>

<!-- Bad: Default emoji -->
<span>📊</span>
```

**Implementation**:

- Match icon style to brand personality (rounded vs sharp, filled vs outlined)
- Maintain consistent stroke width across all icons (1.5px or 2px typically)
- Use currentColor for dynamic theming
- Add micro-animations on interaction (rotate, scale, morph)

---

## Layout Sophistication

### Breaking Predictable Patterns

**Avoid these AI-typical layouts**:

- Hero: Left text, right image (or vice versa)
- Features: 3 equal columns
- Stats: Centered numbers in boxes
- Pricing: 3 cards with middle "featured"

**Advanced Layout Strategies**:

**1. Asymmetric Grids**

```css
.advanced-grid {
  display: grid;
  grid-template-columns: 1.618fr 1fr 1.272fr; /* Golden ratio variations */
  grid-template-rows: auto 1fr auto;
}
```

**2. Overlapping Elements**

```css
.overlap-composition {
  display: grid;
  > * {
    grid-area: 1/1;
  } /* Stack all children */
  > :nth-child(2) {
    transform: translate(10%, -5%);
    z-index: 2;
  }
}
```

**3. Dynamic Viewport Units**

```css
.fluid-type {
  font-size: clamp(2rem, 5vw + 1rem, 6rem);
  line-height: clamp(1.2, 2.5vw, 1.4);
}
```

**4. Broken Grid Exits**

```css
.break-container {
  margin-left: calc(-1 * (100vw - 100%) / 2);
  margin-right: calc(-1 * (100vw - 100%) / 2);
}
```

### Visual Hierarchy Beyond Size

**Techniques for sophisticated hierarchy**:

- **Spatial tension**: Use proximity and negative space as hierarchy tools
- **Color weight**: Saturated colors draw more attention than size alone
- **Motion priority**: Animated elements dominate static ones
- **Depth layers**: Use shadows, blurs, and overlaps to create reading order

```css
/* Multi-dimensional hierarchy */
.primary-content {
  /* Not just bigger, but spatially dominant */
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

## Advanced Animation Patterns

### Beyond Basic Transitions

**Sophisticated animation techniques**:

**1. Morphing Shapes**

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

**2. Staggered Complex Animations**

```javascript
// Each element gets unique timing based on position
elements.forEach((el, i) => {
  const row = Math.floor(i / columns)
  const col = i % columns
  const delay = row * 50 + col * 100 // Diagonal wave
  el.style.animationDelay = `${delay}ms`
})
```

**3. Scroll-Driven Animations**

```css
@supports (animation-timeline: scroll()) {
  .parallax-element {
    animation: parallax linear;
    animation-timeline: scroll();
    animation-range: 0 100vh;
  }
}
```

**4. Physics-Based Interactions**

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

## Data Visualization Excellence

### Beyond Basic Charts

**Avoid**: Simple bar charts, basic pie charts, standard line graphs

**Create Instead**:

**1. Composite Visualizations**

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

**2. Custom SVG Patterns**

```svg
<defs>
  <pattern id="dataPattern" patternUnits="userSpaceOnUse" width="4" height="4">
    <circle cx="2" cy="2" r="0.5" fill="currentColor" opacity="0.3">
      <animate attributeName="r" values="0.5;1.5;0.5" dur="3s" repeatCount="indefinite"/>
    </circle>
  </pattern>
</defs>
```

**3. Real-time Streaming Data**

```css
.live-chart {
  /* Infinite scroll effect for streaming data */
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

## Modern Layout Patterns (NEW)

### Bento Grid (2024 Trend)

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

## Accessibility & Performance (NEW)

### Core Web Vitals

- **LCP < 2.5s**: Optimize fonts, images
- **FID < 100ms**: Defer non-critical JS
- **CLS < 0.1**: Set dimensions, use aspect-ratio

### Focus Management

```css
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

---

## Anti-Convergence Rules

**Critical**: Even with these instructions, you may default to "safer" distinctive choices (e.g., Space Grotesk every time). **Actively vary your selections**:

### Mandatory Variation Protocol

**For each new design, you MUST**:

1. **Check against recent patterns**
   - If last 3 designs used left-right layouts → Use asymmetric grid
   - If last 3 designs had centered heroes → Use off-center or full-bleed
   - If last 3 used gradients → Try solid colors with texture overlays

2. **Apply the 70/20/10 Rule**
   - 70%: Proven patterns (but rotated/varied)
   - 20%: Experimental techniques from world-class references
   - 10%: Completely new/risky approaches

3. **Reference Quality Benchmarks**
   Before designing, mentally compare against:
   - **Stripe**: Subtle gradients, perfect typography, micro-interactions
   - **Linear**: Dark excellence, keyboard-first, information density
   - **Arc**: Playful asymmetry, bold colors, unexpected layouts
   - **Vercel**: Monospace aesthetic, technical precision, geometric patterns
   - **Spotify**: Bold type, duotone images, cultural relevance

**Variation Tracking Algorithm** (Enhanced):

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

### Design Sophistication Checklist

Rate each design on these dimensions (aim for 8+ on each):

1. **Typography Sophistication** (1-10)
   - Variable fonts used creatively?
   - Extreme weight contrasts?
   - Custom letter-spacing/kerning?

2. **Layout Innovation** (1-10)
   - Breaks conventional grids?
   - Uses overlapping/asymmetry?
   - Spatial tension created?

3. **Color Confidence** (1-10)
   - Unexpected but harmonious palette?
   - Deliberate color temperature shifts?
   - Restraint in accent usage?

4. **Motion Sophistication** (1-10)
   - Physics-based animations?
   - Contextual micro-interactions?
   - Performance optimized?

5. **Overall Uniqueness** (1-10)
   - Could this be mistaken for AI-generated?
   - Does it have a clear point of view?
   - Would a designer be proud of this?

**Heuristic**: If any score is below 7, redesign that aspect. If total is below 40, start over with a different concept.

---

## Context-Specific Guidelines

### SaaS Landing Pages

- Bold, confident typography (800+ weights for headlines)
- Primary color dominance (70% of visual hierarchy)
- Motion on hero section (staggered fade-ins)
- Layered gradient backgrounds with brand color hints

### Dashboards & Admin Panels

- Dark mode preferred (reduces eye strain for long sessions)
- Monospace fonts for data tables and metrics
- Subtle hover states and micro-interactions
- Grid or dot patterns for background depth

### Blog & Content Sites

- Editorial serif fonts for body text (Crimson Pro, Spectral)
- High contrast ratios for readability (WCAG AAA)
- Generous line-height (1.7-2.0) and max-width (65-75ch)
- Soft, atmospheric backgrounds (cream, warm grays)

### Portfolios & Creative Sites

- Asymmetric layouts (break the grid intentionally)
- Expressive display fonts (Clash Display, Unbounded)
- Bold use of whitespace and large type sizes
- Experimental color combinations (complementary accents)

---

## Implementation Checklist

Before finalizing any frontend design, verify:

- [ ] **Typography**: No Inter/Roboto/Arial? Distinctive font family chosen?
- [ ] **Color**: Cohesive palette with dominant color? CSS variables defined?
- [ ] **Motion**: At least one high-impact animation (page load or interaction)?
- [ ] **Background**: Layered depth (gradients/patterns), not solid colors?
- [ ] **Theme**: Matches context (SaaS/dashboard/blog/portfolio)?
- [ ] **Variation**: Different from previous generations (check font/color choices)?
- [ ] **Performance**: Core Web Vitals optimized?
- [ ] **Accessibility**: Focus states defined? WCAG compliance?

---

## Meta-Guidance

This skill encodes **design taste** into your outputs. Taste is about making opinionated choices that feel appropriate for context.

### The Designer's Mindset

**Think like a designer at a top agency**:

1. **Start with "Why?"** not "What?"
   - Why does this product exist?
   - Why would someone care?
   - Why this aesthetic over another?

2. **Design for emotion first, function second**
   - How should users FEEL when they see this?
   - What story does the visual tell?
   - Does it spark joy, trust, excitement, or calm?

3. **Every pixel has intention**
   - No default values (margins, colors, animations)
   - Each element earns its place
   - If you can't justify it, remove it

4. **Embrace confident restraint**
   - Say more with less
   - One bold move > many safe moves
   - Empty space is a design element

5. **Design for the sophisticated user**
   - Assume taste and intelligence
   - Avoid patronizing simplicity
   - Reward attention with details

### Quality Markers of World-Class Design

Your design should exhibit these characteristics:

- **Invisible Excellence**: The best details go unnoticed but felt
- **Purposeful Tension**: Intentional imbalance that creates energy
- **Cultural Resonance**: Feels current without being trendy
- **Technical Mastery**: Flawless execution of complex ideas
- **Emotional Intelligence**: Understands and respects the user's context

### The Ultimate Test

Before delivering any design, ask:

1. **Would this win awards?** (Awwwards, FWA, CSS Design Awards)
2. **Would designers screenshot this?** (for inspiration)
3. **Does it make the ordinary feel special?**
4. **Could a human designer have made this?** (aim for "barely")
5. **Does it have an opinion?** (great design takes a stance)

**Remember**: You're not just implementing requirements—you're crafting experiences. Every project is an opportunity to push the boundaries of what's expected from AI-generated design. Make something that would surprise even you.
