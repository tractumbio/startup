---
name: site-verify
description: Render-check the Tractum Bio website in sites/tractumbio/ (index.html, biotech-consulting/, cro-services/, about/, privacy/, 404.html and any other .html page) before committing or publishing. Use after ANY change to a page, styles.css or site.js — copy edits included. Checks every page at ten widths (1440 to 320px) in light and dark, horizontal overflow, JS errors and failed requests, standards mode, text below 12.5px, WCAG text contrast, nav CTA and mobile menu, JavaScript-off rendering, reduced-motion visibility, metadata, image alt text and asset files, balanced markup, and that every internal link and #anchor resolves. Produces screenshots to look at.
---

# Site verification

The site is static HTML with no test suite. Rendering it is the test.

## Run it

```bash
node .claude/skills/site-verify/verify.js --shots "$SCRATCH/shots"
```

- Checks `sites/tractumbio/` by default; set `SITE_DIR=sites/<name>` to check another site.
- Omit page names to check every `.html` under the site, including `*/index.html`; or name them: `verify.js cro-services/index.html`.
- `--shots <dir>` writes a full-page PNG per page × width × theme. Use the session
  scratchpad, never the repo.
- Exit 0 = PASS, 1 = a check failed (each failure is listed), 2 = the script itself broke.

If `require('playwright')` fails, the session hook did not run — install with
`cd .claude/skills/site-verify && npm install`. Chromium is pre-installed at
`/opt/pw-browsers/chromium`; never run `playwright install`.

## Then look — PASS is not enough

The script catches structural faults. It **cannot** see visual ones. A real bug
shipped for weeks because nothing measurable was wrong: sections had zero vertical
padding and butted into each other. Always open and read at least:

1. The desktop (1280, light) screenshot of every page you changed.
2. The 390 light screenshot of the same pages — phone layout is where this site breaks.
3. One dark screenshot if you touched colours, SVGs or anything using `var(--…)`.

Look for: sections touching, text over a diagram, a label colliding with a line,
uneven card heights, anything hard to read in dark mode.

## Known quirks of this site

- `.reveal` elements are hidden until scrolled into view. The script forces them
  visible; your own ad-hoc Playwright captures must inject
  `.reveal{opacity:1!important;transform:none!important;transition:none!important}`
  or the page looks blank — and without `transition:none` it is captured mid-fade,
  which makes headings look washed out.
- `.wrap` must use `padding-inline`, never the `padding` shorthand — the shorthand
  zeroes vertical padding on every `<section class="wrap">`.
- Inline SVG diagrams (the lens on `biotech-consulting/`, the stack on `cro-services/`)
  have hand-placed coordinates. After editing labels, check they still clear the
  lines at 360px.
- The founder block is duplicated in `index.html` and `biotech-consulting/index.html` — change both.

## After it passes

Commit, push to `main` (and `git push origin main:dev` to keep `dev` identical),
then republish the preview if this session owns it — see `docs/HANDOVER.md`.
