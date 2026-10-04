#!/usr/bin/env node
// Render-check every top-level page of the Tractum Bio site.
// Usage: node verify.js [--shots <dir>] [page.html ...]
// Exits non-zero if any check fails.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..', '..', '..');
const args = process.argv.slice(2);
const shotIdx = args.indexOf('--shots');
const SHOTS = shotIdx >= 0 ? args.splice(shotIdx, 2)[1] : null;
const pages = (args.length ? args : fs.readdirSync(ROOT).filter(f => f.endsWith('.html'))).sort();
const WIDTHS = [1440, 1280, 900, 820, 768, 420, 390, 375, 360, 320];
const MIN_FONT = 12.5;
const CHROMIUM = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;

const failures = [];
const fail = (page, msg) => failures.push(`${page}: ${msg}`);

// Static checks: balanced tags and internal links/anchors.
const html = Object.fromEntries(pages.map(p => [p, fs.readFileSync(path.join(ROOT, p), 'utf8')]));
const ids = Object.fromEntries(pages.map(p => [p, new Set([...html[p].matchAll(/id="([^"]+)"/g)].map(m => m[1]))]));
for (const p of pages) {
  for (const tag of ['div', 'section', 'svg', 'article', 'ul']) {
    const open = (html[p].match(new RegExp(`<${tag}[\\s>]`, 'g')) || []).length;
    const close = (html[p].match(new RegExp(`</${tag}>`, 'g')) || []).length;
    if (open !== close) fail(p, `<${tag}> open ${open} / close ${close}`);
  }
  if (!/^<!doctype html>/i.test(html[p].trimStart())) fail(p, 'missing <!doctype html>');
  if (!/<link rel="icon"/.test(html[p])) fail(p, 'no favicon link');
  if (!/property="og:image"/.test(html[p])) fail(p, 'no og:image');
  if (!/<title>Tractum Bio \| /.test(html[p])) fail(p, 'title is not descriptive');
  // House style: no em dashes anywhere in a page (copy, attributes or comments).
  if (html[p].includes('\u2014') || /&mdash;|&#8212;/.test(html[p])) fail(p, `em dash found (${(html[p].match(/\u2014|&mdash;|&#8212;/g) || []).length})`);
  if (!/class="skip"/.test(html[p])) fail(p, 'no skip link');
  if (!/class="menu-btn"[^>]*aria-controls="primary-nav"/.test(html[p]) || !/id="primary-nav"/.test(html[p])) fail(p, 'menu button / primary-nav missing');
  for (const [tag] of html[p].matchAll(/<img\b[^>]*>/g)) {
    if (!/\balt="/.test(tag)) fail(p, `img without alt: ${tag.slice(0, 60)}`);
    const src = (tag.match(/src="([^"]+)"/) || [])[1];
    if (src && !/^https?:/.test(src) && !fs.existsSync(path.join(ROOT, src))) fail(p, `img src missing on disk: ${src}`);
  }
  for (const [, src] of html[p].matchAll(/(?:href|content)="(assets\/[^"]+)"/g)) {
    if (!fs.existsSync(path.join(ROOT, src))) fail(p, `asset missing on disk: ${src}`);
  }
  for (const [, href] of html[p].matchAll(/href="([^"]+)"/g)) {
    if (/^(mailto:|https?:|tel:)/.test(href) || /\.(css|js|png|svg|ico)$/.test(href)) continue;
    const [file, frag] = href.split('#');
    const target = file || p;
    if (!fs.existsSync(path.join(ROOT, target))) { fail(p, `link to missing page ${href}`); continue; }
    if (frag && ids[target] && !ids[target].has(frag)) fail(p, `link to missing anchor ${href}`);
  }
}

(async () => {
  const browser = await chromium.launch({ executablePath: CHROMIUM });
  if (SHOTS) fs.mkdirSync(SHOTS, { recursive: true });

  for (const p of pages) {
    const url = 'file://' + path.join(ROOT, p);
    const runs = WIDTHS.map(w => [w, 'light']).concat([[1280, 'dark'], [390, 'dark'], [320, 'dark']]);
    for (const [w, scheme] of runs) {
      const pg = await browser.newPage({ viewport: { width: w, height: 900 }, colorScheme: scheme });
      const errs = [];
      pg.on('pageerror', e => errs.push(String(e)));
      pg.on('requestfailed', r => errs.push('failed request ' + r.url()));
      await pg.goto(url);
      // Scroll-triggered reveals stay hidden in a headless capture; force them visible.
      await pg.addStyleTag({ content: '.reveal{opacity:1!important;transform:none!important;transition:none!important}' });
      await pg.waitForTimeout(250);
      const r = await pg.evaluate((minFont) => {
        const overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
        const small = new Set();
        document.querySelectorAll('body *').forEach(el => {
          if (el.closest('svg') || !el.childNodes.length) return;
          const ownText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
          if (!ownText) return;
          const fs = parseFloat(getComputedStyle(el).fontSize);
          if (fs < minFont) small.add(`${el.tagName.toLowerCase()}.${el.className || ''} ${fs.toFixed(1)}px`);
        });
        // WCAG 1.4.3 contrast for every visible text element outside SVGs: 4.5:1, or 3:1 for large text.
        // rgb()/rgba() report 0-255 channels; color(srgb ...) (what color-mix() computes to) reports 0-1.
        const rgba = c => { const m = c.replace(/^color\(srgb/, '').match(/[\d.]+/g).map(Number); const k = c.startsWith('color(') ? 255 : 1;
          return [m[0] * k, m[1] * k, m[2] * k, m.length > 3 ? m[3] : 1]; };
        const blend = (top, bot) => [0, 1, 2].map(i => top[i] * top[3] + bot[i] * (1 - top[3])).concat(1);
        const lum = c => { const v = c.slice(0, 3).map(x => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; }); return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
        const bgOf = el => { const layers = []; for (let e = el; e; e = e.parentElement) { const c = rgba(getComputedStyle(e).backgroundColor); if (c[3] > 0) { layers.push(c); if (c[3] >= 1) break; } }
          let out = [255, 255, 255, 1]; for (let i = layers.length - 1; i >= 0; i--) out = blend(layers[i], out); return out; };
        const lowContrast = new Set();
        document.querySelectorAll('body *').forEach(el => {
          if (el.closest('svg') || el.classList.contains('skip')) return;
          if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
          if (!el.getClientRects().length) return;
          const cs = getComputedStyle(el); if (cs.visibility === 'hidden') return;
          let op = 1; for (let e = el; e; e = e.parentElement) op *= parseFloat(getComputedStyle(e).opacity);
          const bg = bgOf(el); const fg = rgba(cs.color); fg[3] *= op;
          const f = blend(fg, bg); const a = lum(f), b = lum(bg);
          const ratio = (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
          const size = parseFloat(cs.fontSize), large = size >= 24 || (size >= 18.66 && parseInt(cs.fontWeight) >= 700);
          if (ratio < (large ? 3 : 4.5)) lowContrast.add(`${el.tagName.toLowerCase()}.${String(el.className).split(' ')[0]} "${el.textContent.trim().slice(0, 24)}" ${ratio.toFixed(2)}`);
        });
        const vis = el => !!el && getComputedStyle(el).display !== 'none' && el.getBoundingClientRect().width > 0;
        const cta = document.querySelector('.nav-cta');
        return { overflow, mode: document.compatMode, small: [...small].slice(0, 5),
          lowContrast: [...lowContrast],
          ctaText: cta ? cta.innerText.trim() : '', ctaVisible: vis(cta),
          menuVisible: vis(document.querySelector('.menu-btn')), linksVisible: vis(document.querySelector('nav.links')) };
      }, MIN_FONT);
      const tag = `${String(w).padStart(4)} ${scheme}`;
      if (r.overflow > 0) fail(p, `${tag}: horizontal overflow ${r.overflow}px`);
      if (r.mode !== 'CSS1Compat') fail(p, `${tag}: quirks mode`);
      if (errs.length) fail(p, `${tag}: ${errs[0]}`);
      if (w === 1280 && scheme === 'light' && r.small.length) fail(p, `text below ${MIN_FONT}px: ${r.small.join(', ')}`);
      if ((w === 1280 || w === 390) && r.lowContrast.length) fail(p, `${tag}: low contrast (${r.lowContrast.length}): ${r.lowContrast.slice(0, 6).join('; ')}`);
      // Navigation must be reachable at every width: inline links on desktop, a menu button on phones,
      // and the CTA pill must never render empty (a CSS-ordering bug once made it so).
      if (!r.ctaVisible || !r.ctaText) fail(p, `${tag}: nav CTA has no visible text`);
      if (w <= 900 && !r.menuVisible) fail(p, `${tag}: no menu button on narrow screen`);
      if (w > 900 && (!r.linksVisible || r.menuVisible)) fail(p, `${tag}: desktop nav state wrong (links ${r.linksVisible}, menu ${r.menuVisible})`);
      if (w <= 900) {
        await pg.click('.menu-btn');
        const m = await pg.evaluate(() => {
          const nl = document.querySelector('nav.links');
          return { open: !!nl && getComputedStyle(nl).display !== 'none', expanded: document.querySelector('.menu-btn').getAttribute('aria-expanded'),
            overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth };
        });
        if (!m.open || m.expanded !== 'true') fail(p, `${tag}: menu button does not open the nav`);
        if (m.overflow > 0) fail(p, `${tag}: horizontal overflow ${m.overflow}px with menu open`);
        if (SHOTS && w === 390 && scheme === 'light') await pg.screenshot({ path: path.join(SHOTS, `${p.replace('.html', '')}-${w}-menu.png`) });
        await pg.click('.menu-btn');
      }
      if (SHOTS) await pg.screenshot({ path: path.join(SHOTS, `${p.replace('.html', '')}-${w}-${scheme}.png`), fullPage: true });
      await pg.close();
    }
    // With JavaScript off, every block is visible and the nav links are reachable without the menu button.
    for (const w of [390, 1280]) {
      const nj = await browser.newPage({ viewport: { width: w, height: 900 }, javaScriptEnabled: false });
      await nj.goto(url);
      const q = await nj.evaluate(() => ({
        hidden: [...document.querySelectorAll('.reveal')].filter(e => getComputedStyle(e).opacity !== '1').length,
        links: [...document.querySelectorAll('nav.links a')].filter(a => a.getBoundingClientRect().width > 0).length,
        overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth }));
      if (q.hidden) fail(p, `${w} no-JS: ${q.hidden} .reveal elements hidden`);
      if (!q.links) fail(p, `${w} no-JS: nav links unreachable`);
      if (q.overflow > 0) fail(p, `${w} no-JS: horizontal overflow ${q.overflow}px`);
      await nj.close();
    }
    // Reduced motion must show everything with no transition.
    const pg = await browser.newPage({ reducedMotion: 'reduce' });
    await pg.goto(url); await pg.waitForTimeout(200);
    const hidden = await pg.evaluate(() => [...document.querySelectorAll('.reveal')].filter(e => getComputedStyle(e).opacity !== '1').length);
    if (hidden) fail(p, `reduced motion: ${hidden} .reveal elements not visible`);
    await pg.close();
  }
  await browser.close();

  console.log(`Checked ${pages.length} page(s) at ${WIDTHS.join('/')}px, light + dark, contrast, no-JS, reduced motion, nav/menu, links, assets, markup.`);
  if (SHOTS) console.log(`Screenshots: ${SHOTS}`);
  if (failures.length) { console.log(`\nFAIL (${failures.length}):`); failures.forEach(f => console.log('  - ' + f)); process.exit(1); }
  console.log('PASS');
})().catch(e => { console.error(e); process.exit(2); });
