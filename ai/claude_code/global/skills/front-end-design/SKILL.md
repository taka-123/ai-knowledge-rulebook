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

- If you used Space Grotesk last time, try Bricolage Grotesque or Syne
- Alternate between light and dark themes
- Rotate through different aesthetic influences (brutalist → editorial → technical)
- Randomize accent color families (avoid always using blue)

**Variation Tracking Algorithm** (NEW):

```javascript
// Prevent repetition
const recentChoices = {
  fonts: [], // Last 3 fonts used
  colors: [], // Last 3 color schemes
  layouts: [], // Last 3 layout patterns
}

function selectUnique(category, options) {
  const unused = options.filter(o => !recentChoices[category].includes(o))
  return unused[Math.floor(Math.random() * unused.length)]
}
```

**Heuristic**: Ask yourself, "Does this look like something I've generated before?" If yes, change at least 2 major design decisions.

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

This skill encodes **design taste** into your outputs. Taste is about making opinionated choices that feel appropriate for context. When in doubt:

1. **Be bold**: Distinctive is better than safe
2. **Be consistent**: Commit to a cohesive aesthetic
3. **Be contextual**: Match the design to the use case
4. **Be varied**: Don't repeat yourself across generations
5. **Be performant**: Beauty without speed is failure

**Remember**: Your goal is not to follow a rigid template, but to internalize these principles and apply them creatively. Think like a designer who understands both aesthetics and implementation.
