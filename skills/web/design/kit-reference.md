# Falconshire kit v1 — component reference

All classes are prefixed `k-`. Tokens are CSS variables `--k-*`; use them in page CSS instead of raw hex.

## Tokens
- Color: `--k-page --k-surface --k-surface-2 --k-ink --k-ink-2 --k-muted --k-line --k-line-strong --k-accent --k-accent-soft --k-good(-soft) --k-warn(-soft) --k-bad(-soft)`
- Chart: `--k-s1…--k-s8` (fixed order), `--k-seq-1…--k-seq-5`, `--k-grid --k-axis`
- Type: `--k-font --k-serif --k-mono`, sizes `--k-fs-xs sm md lg xl 2xl 3xl 4xl`
- Space `--k-sp-1…8` (4 8 12 16 24 32 48 72), radius `--k-r-sm md lg`, `--k-max` 1180px, `--k-measure` 40em
- Dark mode is automatic (OS) plus a toggle: any button with `data-k-theme-toggle`.
- Style skins: `<link rel="stylesheet" href="kit/styles/economist.css">` after `v1.css` restyles the same components (see `charts.md`); `apply_kit.py` inlines it too. The economist skin adds `--k-brand` (red rule) and `--k-chart-font`, and is light-only.

## Skeleton
```html
<body class="k">
<header class="k-header"><div class="k-page k-header__in">
  <a class="k-brand" href="#top"><span class="k-brand__mark">杯</span><span class="k-brand__name">站名</span></a>
  <nav class="k-nav"><a href="#s1">章节</a></nav>
  <button class="k-btn k-btn--icon" data-k-theme-toggle type="button">☾</button>
</div></header>
<main id="top">
  <section class="k-hero [k-hero--image]" [style="background-image:url(hero.webp)"]><div class="k-page">
    <div class="k-hero__eyebrow">分类 · 日期</div><h1>标题</h1>
    <p class="k-hero__lede">一句话导语</p><div class="k-hero__meta"><span>…</span></div>
  </div></section>
  <div class="k-page k-with-toc">
    <nav class="k-toc"><a href="#s1">01 …</a></nav>
    <div>
      <section class="k-section" id="s1">
        <div class="k-section__head"><span class="k-section__num">01</span><h2>…</h2></div>
        <div class="k-prose"><p>…<span class="k-cite">[1]</span></p></div>
      </section>
    </div>
  </div>
</main>
<footer class="k-footer"><div class="k-page">…</div></footer>
```
Without a TOC, drop `k-with-toc`/`k-toc` and put sections directly in `.k-page`.

## Report blocks
- Verdict: `<div class="k-verdict"><div class="k-verdict__label">结论</div><p class="k-verdict__text">…</p><p class="k-verdict__note">…</p></div>`
- KPIs: `<div class="k-kpis"><div class="k-kpi"><div class="k-kpi__value">86<span class="k-kpi__unit">%</span></div><div class="k-kpi__label">…</div><div class="k-kpi__delta k-kpi__delta--up">▲ …</div></div></div>` (`--down` for red)
- Callout: `<div class="k-callout [k-callout--good|--warn|--bad]"><div class="k-callout__title">假设</div><div>…</div></div>`
- Figure: `<figure class="k-figure"><div class="k-figure__title">…</div><div class="k-figure__sub">单位…</div><div class="k-chart">SVG + <div class="k-tooltip"></div></div><figcaption>来源…</figcaption></figure>`
  SVG helper classes: `k-grid-line k-axis-line k-tick k-dlabel`; legend `<div class="k-legend"><span><i style="background:var(--k-s1)"></i>系列</span></div>`; tooltip shows with `data-show="true"`.
- Table: `<div class="k-table-wrap"><table class="k-table">…</table></div>`; numeric cells `class="k-num"`; highlight row `class="k-row--hi"`.
- Sources: `<ol class="k-sources"><li>作者/机构，标题，年份，<a>链接</a></li></ol>`

## Catalog blocks
- Search (sticky under header): `<div class="k-search"><input type="search" placeholder="…"></div>`
- Chips: `<div class="k-chips" [data-k-single]><button class="k-chip" aria-pressed="true">全部</button>…</div>`; each click fires a bubbling `k:chip` event.
- Cards: `<div class="k-grid k-grid--rows">` (use `k-grid--2` for two wide columns) containing `<button class="k-card" data-k-open="drawerId"><div class="k-card__media" style="background-image:url(…)"></div><div class="k-card__body"><div class="k-card__title">…</div><div class="k-card__meta">…</div><p class="k-card__text">…</p><div class="k-tags">…</div></div></button>` (`<a class="k-card">` for links).
- Tags: `k-tag` + `--accent --good --warn --bad`.
- Drawer (one scrim per page):
```html
<div class="k-scrim"></div>
<aside class="k-drawer" id="d1" aria-hidden="true">
  <button class="k-btn k-btn--icon k-drawer__close" data-k-close>✕</button>
  <div class="k-drawer__media" style="background-image:url(…)"></div>
  <div class="k-drawer__body"><h3 class="k-drawer__title">…</h3>
    <dl class="k-facts"><div class="k-fact"><dt>产区</dt><dd>…</dd></div></dl>
    <div class="k-prose">…</div><ol class="k-sources">…</ol></div>
</aside>
```
  JS: `kit.openDrawer(id)` / `kit.closeDrawers()` to fill one drawer dynamically; Esc and scrim close it.
- Tabs: `<div class="k-tabs"><button class="k-tab" aria-selected="true" aria-controls="p1">…</button></div><div class="k-tabpanel" id="p1">…</div>` (others `hidden`).
- Buttons: `k-btn`, `k-btn--primary`, `k-btn--icon`.

## Map chrome
`<div class="k-map">` + `.k-map__hint` (one-line pan/zoom hint), `.k-map__controls` (+ / − / ⟲ buttons and `.k-map__zoom` level text), `.k-map__legend`. Works around Leaflet/MapLibre containers or an SVG.

## Utilities
`k-muted k-ink2 k-small k-center k-num k-sr-only k-reveal k-stack k-grid`
