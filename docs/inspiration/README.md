# Design inspiration

Reference websites for the Tractum Bio design. Point Claude at a URL and it adds an entry here;
when the final design is decided, the index below is the shortlist to draw from.

## How to add a site

Tell Claude: "add https://example.com to inspiration, I like the hero and the pricing layout".
Claude will:

1. Capture desktop and phone screenshots into `shots/` (`node capture.js <url> <slug>`).
2. Add a row to the index below.
3. Write `entries/<slug>.md` from `entries/_template.md`: what is worth borrowing, what is not, and
   how it maps to a Tractum page.

If the session's network policy blocks the site, the capture fails with `ERR_TUNNEL_CONNECTION_FAILED`. Either
add the host under Allowed domains in the environment settings, or send Claude your own screenshots
(drop them in `shots/`) and describe what you like. The entry is then written from those.

Screenshots are for private design reference only. Do not publish them or copy a site's text,
imagery or code.

## Index

| Site | Why it is here | Maps to | Added |
|---|---|---|---|
| _none yet_ | | | |

## Queue (named, not yet captured)

Sites asked for but not yet looked at, because the session's network policy blocked them. Each needs
a capture and an entry once the host is allowed, or screenshots are supplied.

| Site | URL | Note |
|---|---|---|
| Boston Biomedical Consulting | https://www.bostonbio.com/ | boutique life-sciences consultancy, closest in size to Tractum |
| McKinsey Life Sciences | https://www.mckinsey.com/industries/life-sciences/how-we-help-clients | how a top-tier firm presents a sector practice |
| IQVIA | https://www.iqvia.com/ | large CRO/data company; CRO-side language and proof |
| g-co.agency list | https://www.g-co.agency/insights/top-pharma-strategy-consulting-firms-to-work-with | article listing pharma strategy consultancies; each firm it names is a candidate for this index |

Firms from that article's "Firms Compared" table (`firms-compared.jpg`). URLs are best guesses and
unverified until captured.

| Firm | URL (unverified) | Best for (per the article) |
|---|---|---|
| G&Co. | https://www.g-co.agency/ | commercial strategy and digital transformation |
| Blue Matter | https://www.bluematterconsulting.com/ | launch and commercialization strategy |
| ClearView | https://www.clearviewhc.com/ | portfolio and asset evaluation |
| Putnam Associates | https://www.putassoc.com/ | commercial and pricing strategy |
| Prescient | https://www.prescienthg.com/ | competitive intelligence and positioning |
| Trinity Life Sciences | https://trinitylifesciences.com/ | launch strategy and market access |
| Alacrita | https://www.alacrita.com/ | clinical development and licensing |
| Vintura | https://www.vintura.com/ | European access and value strategy |
| Catenion | https://www.catenion.com/ | R&D productivity and pipeline strategy |
| Beghou Consulting | https://www.beghouconsulting.com/ | commercial analytics and field strategy |

## What we are looking for

Tractum Bio is a boutique ophthalmic advisory practice with two audiences (biotech firms and CRO or
lab teams). Good references are credible, quiet and specific: clear first-screen claim, restrained
palette, proof placed near claims, an obvious next step. Note anything that fails this too, since
a "do not do this" entry is useful.

## Source lists

- `firms-compared.jpg`: the "Firms Compared" table from g-co.agency's article on pharma strategy consultancies, which supplied ten of the sites above.
