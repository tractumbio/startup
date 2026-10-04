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
const WIDTHS = [1280, 820, 390, 360];
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
    const runs = WIDTHS.map(w => [w, 'light']).concat([[1280, 'dark'], [390, 'dark']]);
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
        return { overflow, mode: document.compatMode, small: [...small].slice(0, 5) };
      }, MIN_FONT);
      const tag = `${String(w).padStart(4)} ${scheme}`;
      if (r.overflow > 0) fail(p, `${tag}: horizontal overflow ${r.overflow}px`);
      if (r.mode !== 'CSS1Compat') fail(p, `${tag}: quirks mode`);
      if (errs.length) fail(p, `${tag}: ${errs[0]}`);
      if (w === 1280 && scheme === 'light' && r.small.length) fail(p, `text below ${MIN_FONT}px: ${r.small.join(', ')}`);
      if (SHOTS) await pg.screenshot({ path: path.join(SHOTS, `${p.replace('.html', '')}-${w}-${scheme}.png`), fullPage: true });
      await pg.close();
    }
    // Reduced motion must show everything with no transition.
    const pg = await browser.newPage({ reducedMotion: 'reduce' });
    await pg.goto(url); await pg.waitForTimeout(200);
    const hidden = await pg.evaluate(() => [...document.querySelectorAll('.reveal')].filter(e => getComputedStyle(e).opacity !== '1').length);
    if (hidden) fail(p, `reduced motion: ${hidden} .reveal elements not visible`);
    await pg.close();
  }
  await browser.close();

  console.log(`Checked ${pages.length} page(s) at ${WIDTHS.join('/')}px, light + dark, reduced motion, links, markup.`);
  if (SHOTS) console.log(`Screenshots: ${SHOTS}`);
  if (failures.length) { console.log(`\nFAIL (${failures.length}):`); failures.forEach(f => console.log('  - ' + f)); process.exit(1); }
  console.log('PASS');
})().catch(e => { console.error(e); process.exit(2); });
