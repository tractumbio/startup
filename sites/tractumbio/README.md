# tractumbio.com

Static HTML, no build step. One folder per section; each folder holds an `index.html`, so URLs are clean
(`/cro-services/`, not `/capability.html`).

```
index.html                landing page: shared claim, the two doors, founder strip, contact
cro-services/             CRO services (ophthalmic services, omics, pipeline automation)
biotech-consulting/       ophthalmology consulting for biotech firms
about/                    bio, accolades, prior success stories
privacy/                  privacy note
404.html                  must stay at the root (hosts look for it there)
styles.css  site.js       shared by every page
assets/                   shared images, favicon, social card
tools/make_og.py          regenerates assets/og.jpg
robots.txt  sitemap.xml
```

## Where new content goes

- **Prior work / success stories:** `about/`. If it outgrows one page, add `about/<topic>/index.html`
  (for example `about/track-record/`) rather than a new top-level folder.
- **Dual contact and booking:** today the contact block is `#contact` on the landing page. When the
  design is settled, each practice page ends with its own contact block (biotech and CRO), and a
  shared booking link sits in the footer. If it needs its own page, make it `contact/index.html`.
- **A new page:** `<section>/index.html`, with `styles.css`, `site.js` and `assets/` referenced by relative
  path (`../styles.css`), then add it to `sitemap.xml` and to the nav on every page.

## Paths

Pages in a folder link up with `../`. Internal links to sections use the folder form (`../cro-services/`).
`file://` previews do not open folder links, so preview with a static server (`python3 -m http.server`
from this folder). `site-verify` resolves folder links to their `index.html` itself.
