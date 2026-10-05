# Design inspiration

Reference websites for the Tractum Bio design. Point Claude at a URL and it adds an entry here;
when the final design is decided, the index below is the shortlist to draw from.

## How to add a site

Tell Claude: "add https://example.com to inspiration, I like the hero and the pricing layout".
Claude will:

1. Capture desktop and phone screenshots into `shots/` (`node capture.js <url> <slug>`; set `SETTLE_MS=12000` for sites behind a bot check).
2. Add a row to the index below.
3. Write `entries/<slug>.md` from `entries/_template.md`: what is worth borrowing, what is not, and
   how it maps to a Tractum page.

If the session's network policy blocks the site, the capture fails with `ERR_TUNNEL_CONNECTION_FAILED`. Either
add the host under Allowed domains in the environment settings, or send Claude your own screenshots
(drop them in `shots/`) and describe what you like. The entry is then written from those.

Screenshots are for private design reference only. Do not publish them or copy a site's text,
imagery or code.

## Index

Ranked by how much of each site is worth carrying into the Tractum design. Entries in `entries/`,
screenshots in `shots/`.

| Site | Why it is here | Maps to | Added |
|---|---|---|---|
| [ClearView](entries/clearview.md) | the benchmark for quiet and credible; vertical practice selector | landing, biotech-consulting | 2026-10-05 |
| [Prescient](entries/prescient.md) | hero + proof strip + four practice cards; dual CTA | landing | 2026-10-05 |
| [Vintura](entries/vintura.md) | serif headline, one accent, named-person CTAs | landing, contact | 2026-10-05 |
| [Alacrita](entries/alacrita.md) | kicker + two-clause headline + three proofs; sticky sub-nav | about, biotech-consulting | 2026-10-05 |
| [Catenion](entries/catenion.md) | numbered three reasons with one coloured phrase each | about, biotech-consulting | 2026-10-05 |
| [Beghou](entries/beghou.md) | verb-led capability cards; single CTA | cro-services | 2026-10-05 |
| [Blue Matter](entries/blue-matter.md) | two-column service lists; publication as proof | cro-services, biotech-consulting | 2026-10-05 |
| [Trinity](entries/trinity.md) | three-door landing, and its enterprise failure mode | landing | 2026-10-05 |
| [BioBoston](entries/bioboston.md) | proof tiles with specific credentials; name needs confirming | about, cro-services | 2026-10-05 |
| [G&Co.](entries/g-co.md) | grotesk + serif type pairing; otherwise a counter-example | landing | 2026-10-05 |
| [IQVIA](entries/iqvia.md) | CRO-side vocabulary; on-page sub-nav; density counter-example | cro-services | 2026-10-05 |
| [Putnam / Inizio](entries/putnam.md) | merged brand, nothing to borrow; kept for the record | none | 2026-10-05 |

Not captured: **McKinsey Life Sciences** (https://www.mckinsey.com/industries/life-sciences/how-we-help-clients).
The egress proxy returns "upstream request failed" for mckinsey.com even with the host allowed. Send
screenshots and it gets an entry.

## Patterns that recur across the good ones

1. One sentence that says what the firm is and for whom, before any slogan (Blue Matter, Catenion, Prescient).
2. Proof placed next to the claim, as numbers with a credential attached, not adjectives (Prescient, Alacrita, BioBoston).
3. Three reasons or three doors, never five (Catenion, Alacrita, Trinity, Beghou).
4. One primary CTA per screen, phrased as a next step; the best version names the person (Vintura).
5. A quiet palette with a single accent colour; serif display type reads as advisory, grotesk as agency (Vintura, ClearView vs G&Co.).
6. Lazy-loaded media is the commonest visible defect: three of twelve home pages had blank blocks in a plain capture.

## What we are looking for

Tractum Bio is a boutique ophthalmic advisory practice with two audiences (biotech firms and CRO or
lab teams). Good references are credible, quiet and specific: clear first-screen claim, restrained
palette, proof placed near claims, an obvious next step. Note anything that fails this too, since
a "do not do this" entry is useful.

## Source lists

- `firms-compared.jpg`: the "Firms Compared" table from g-co.agency's article on pharma strategy consultancies, which supplied ten of the sites above.
