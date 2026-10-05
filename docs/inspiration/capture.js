#!/usr/bin/env node
// Screenshot a reference site at desktop and phone width into shots/<slug>-desktop.png and -mobile.png.
// Usage: node capture.js <url> <slug>
// Needs the site-verify dependencies: (cd ../../.claude/skills/site-verify && npm install)
const fs = require('fs');
const path = require('path');
const { chromium } = require('../../.claude/skills/site-verify/node_modules/playwright');

const [url, slug] = process.argv.slice(2);
if (!url || !slug || !/^[a-z0-9-]+$/.test(slug)) {
  console.error('Usage: node capture.js <url> <slug>   (slug: lowercase letters, digits, hyphens)');
  process.exit(2);
}
const CHROMIUM = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
const out = path.join(__dirname, 'shots');

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ executablePath: CHROMIUM });
  for (const [name, width, height] of [['desktop', 1440, 900], ['mobile', 390, 844]]) {
    const page = await browser.newPage({ viewport: { width, height } });
    await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
    await page.screenshot({ path: path.join(out, `${slug}-${name}.png`), fullPage: true });
    await page.close();
    console.log(`wrote shots/${slug}-${name}.png`);
  }
  await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
