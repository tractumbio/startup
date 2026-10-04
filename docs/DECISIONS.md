# Decision record

Settled decisions and the reasoning behind them, so a fresh session doesn't
re-litigate them. If you disagree with one, say so explicitly — don't quietly
reverse it.

Dates are when the decision was taken, not when it was written up.

---

## Firm shape — Sept 2026

**Tractum is a boutique expert practice. There is no plan to scale it.**

Adrian chose this explicitly over building something sellable. Do not propose
growth-shaped strategy — productisation, headcount, enterprise software,
venture funding — unless he reopens it.

Consequences that follow, and that shape everything else:

- **Two arms, deliberately asymmetric.** Ophthalmic advisory is the front
  door: brand, website, content, outbound. CRO data-flow automation is the
  cash engine — genuinely domain-agnostic, served by referral, never
  brand-led, no separate practice branding.
- **The spine is the vantage claim, not the domain.** Bench → computer →
  client for the CRO arm, biology → deal → path for advisory. That is what
  makes one firm coherent across two unrelated buyers.
- **Scarcity is positioning, not a shortfall.** Capacity is roughly 8–12 Tier 1
  engagements a year. Never write defensively about size.
- **The firm sells a person.** Adrian's record is the product.

## Voice: first person — Sept 2026

**Use "I". Never corporate "we".**

A one-person practice saying "we" in its own credibility section undercuts the
exact claim it is making. This was applied across the whole page, not just the
bio. If you add copy, match it.

## Market sizing: bottom-up only — Sept 2026

TAM is `reachable companies × conversion × fee`, capped by delivery capacity.

**Never cite the ~$37B ophthalmic drug market as Tractum's market.** That is
the *clients'* market. Quoting it as our own is the fastest way to look like
we don't understand the business.

## The binding risk is reach, not competition — Sept 2026

Ophthalmic advisory sells into **latent** demand: "your asset may already
matter in the eye" is not a thought the CSO is already having, and nobody
searches for it. There is no incumbent and no price comparison — but nobody
knows to call.

Effort belongs in demand generation, not differentiation. This is also why a
passive "put both sites up and see what converts" test is misleading: the
automation arm sells into known demand and will always win that comparison,
which would talk you out of the better long-term position.

## Merck/EyeBio stays named — Sept 2026. CLOSED.

The EyeBio acquisition is public information and citing it is normal market
commentary. Merck also appears in Adrian's CV as a client, and this repo and
site are public, so a reader could connect the two. Raised three times,
decided: **keep it named.** Do not raise again.

Separately and still binding: **no other client names on the public site**
without written sign-off, and **never state or imply any ErythroSight exit or
licensing outcome** — not disclosable.

## Agent stack: the human gate is structural — Aug 2026

Every pipeline stage writes a draft *before* asking anything; an unapproved
stage halts the pipeline rather than feeding downstream; with no TTY the gate
stops rather than assuming approval. There is deliberately **no global
auto-approve flag**. If unattended runs are ever requested, raise the
trade-off rather than adding one.

## Agent storage: read wide, write narrow — Aug 2026

Every agent can read every other agent's store; an agent writes only its own
or `shared/`. The asymmetry is the point — `valuation` is useless without
`ophtha_science`'s verdict, but an agent that could overwrite another's store
could corrupt the record a human is about to approve.

Chat sessions live in `workspace/<agent>/sessions/` but are excluded from the
workspace manifest: conversation state is not a citable document. `make clean`
must never delete them.

## BD screen is a screen, not an assessment — Sept 2026

`bd_screen/` scores companies for plausible ocular relevance. Scores are
computed **in code from visible weights, never by a model**, and every point
traces to the phrase that earned it. A high score means a scientist should
spend an hour on it — nothing more. `ophtha_science` is expected to reject
most of the list; that is the design, not a failure.

Companies that already name the eye are flagged and excluded from the prospect
list: they are competitors, partners or comparables, never pitch targets.

## Site: four capabilities, not three — Sept 2026

The lens diagram shows biology, path, deal **and strategy** (decision science
/ Accenture). Copy avoids counting ("every side of the table") so a fifth
would not break it.

`CLAUDE.md` and `tractum-agents/company/COMPANY.md` were mirrored to four
vantages in Oct 2026, along with the "brand-led on the CRO page" amendment
below.

## Site routes by buyer, and the lab page brand-leads omics + automation — Oct 2026

The site is now three pages: a landing page (`index.html`) with two doors, a
biotech page (`asset.html`) and a labs page (`capability.html`).

This is **not** the two-door gateway that was rejected earlier. That one split
the firm into two businesses (generic CRO automation vs. ophthalmology). This
one splits **one firm by buyer**, and the landing page carries shared substance
(why the eye, the founder, contact) rather than being a splash screen.

**Change to the "Firm shape" decision, made by Adrian:** the labs page now
presents three equal capabilities — ophthalmic services, cutting-edge omics
(bulk, single-cell, spatial) and full pipeline automation — with omics and
automation explicitly scoped to *any therapeutic area*. Previously the
domain-agnostic work was referral-only and never brand-led. It is now brand-led
on the labs page. Ophthalmology remains the specialism and the landing page's
framing.

Reason: lab buyers have **active** demand (a lost sponsor request is a known
gap), unlike the latent demand on the biotech side.

## External website review applied — Oct 2026

Adrian supplied an external review (`docs/reviews/2026-10-04-website-review.md`) and
asked for its noteworthy suggestions to be implemented. What changed, and why it is now
the rule rather than a preference:

- **Numbers corrected to their sources.** 11.9% vs 7.9% (not 7.9% alone); one market
  estimate (US$37.5B, Mordor, 2025) instead of a blended US$20–40B; EyeBio split into
  US$1.3B upfront plus up to US$1.7B milestones. Sources are linked in each footer.
- **Valuation uplift removed from the site.** The +76% / $85M→$150M figures were
  illustrative with no model behind them. The biotech outcome column now shows the
  decision gate (proceed / pause / stop) — the "no-go is the hero" idea made concrete.
- **First paid step defined** on the biotech page (who it is for, inputs, work,
  deliverables, decision, fee basis, exclusions). Duration and price are deliberately
  absent until Adrian supplies them.
- **Homepage headline replaced.** "The eye, judged by someone who has worked every side
  of it" → "Ophthalmic development decisions. Practical capability for the labs behind
  them." The review's reason: the old line did not name the service. Door headings ("I
  have an asset" / "I run a CRO") were kept because Adrian chose them directly.
- **"IND-ready" kept in the hero** (Adrian's explicit wording) but the route card now
  says "IND-ready plan" and names who files.
- **CRO claims narrowed** and a handover-package list added; see `CLAUDE.md` → Claims
  discipline for the exact wording.
- **Contrast fixed site-wide.** Light-theme teal, amber, bright blue and muted text were
  darkened to reach 4.5:1; filled buttons got their own `--btn*` tokens. `verify.js` now
  checks contrast on every text element, JavaScript-off rendering, and ten widths.

Not adopted: the review's door headings ("Assess an ophthalmic opportunity" / "Build
ophthalmic and analytical capabilities") — Adrian's own wording stands. Conversion
measurement is deferred until an analytics tool is chosen.

## No em dashes, plain copy — Oct 2026

Adrian asked for no em dashes and no "AI slop" feel. All em dashes were removed from the
three pages, and `verify.js` now fails on any. Slogan constructions ("X, not Y"),
aphorisms, stock phrases and most section kicker labels were rewritten or removed;
headings now name the section plainly. The landing headline became "I help biotechs decide
whether a drug belongs in the eye, and help CROs build the services to test it." The rule
is recorded in `CLAUDE.md` → Claims discipline and mirrored in the agents' `BRAND.md`.
