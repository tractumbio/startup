# Tier 1 page: four capabilities, legible type, Apple-style flow, personal story

## Context

Seven changes to `index.html` (the Tractum Bio Tier 1 site), following a flow
and aesthetics review. The page currently reads well but has three concrete
weaknesses the user identified: several text sizes sit below comfortable
reading thresholds, section boundaries are abrupt (1px rules and hard
background switches), and the credibility story under-sells him — it omits
his strategy-consulting vantage and his standing in the patient/academic
community, and it has no personal narrative at all.

Two decisions were settled by the user this round:
- **Personal story**: draft from documented facts in `CLAUDE.md`; he edits.
- **Merck/EyeBio**: stays named. Closed — do not raise again.

No Explore/Plan subagents used: this is a single file authored across this
session, and the relevant CSS, JS, geometry and copy were read directly
(section order, full font-size inventory, reveal observer, lens SVG,
founder block, demand band).

---

## 1. Voice: decided — first person, "I"

Recorded as a decision, not an open question. `CLAUDE.md` "Firm shape" states
the firm sells a person and that corporate "we" is a liability; the page
already converted last round. Action here is only to **keep it consistent**
in all new copy (personal story, community lines, engagement text) and
re-grep for stragglers after editing.

## 2. Add strategy consulting as a fourth capability

The lens diagram (`#why`) currently has three rays: BIOLOGY / PATH / DEAL,
with Accenture folded into DEAL. Break it out:

| ray | label | sub |
|---|---|---|
| 1 | BIOLOGY | PhD · retinal degeneration |
| 2 | PATH | Pharma + biotech |
| 3 | DEAL | Founder-raised · IP secured |
| 4 | STRATEGY | Decision science · Accenture |

Geometry: extend viewBox from `0 0 620 250` to roughly `0 0 620 280`, ray
centres at about y=45/105/165/225, lens aperture widened to span them, and
all six ray endpoints recomputed against the new lens surface (the incoming
rays must terminate on the left face and the refracted rays start on the
right face — this was hand-tuned last round and must be redone, not scaled).

Copy consequence: the section h2 says "lived all three sides" and the founder
bio says "the three vantage points". Counting breaks with four. Replace with a
non-counting phrase — **"every side of the table"** — which stays memorable
and survives a future fifth capability.

**Follow-up flagged, not done here**: `CLAUDE.md` and
`tractum-agents/company/COMPANY.md` both document the spine as a *triple*
vantage (biology → deal → path). Adding a fourth diverges from the recorded
strategy, so those two files need mirroring or the `brand_voice` agent will
keep enforcing three. Raise with the user rather than silently editing
strategy docs.

## 3. Type scale — establish a legibility floor

Base font is 17px. Worst offenders and targets (floor: ~12.5px rendered for
uppercase micro-labels, ~14px for anything sentence-like):

| selector | now | → |
|---|---|---|
| `.ostat b small` | .6rem (10.2px) | .74rem |
| `.cap-sub` (SVG, ~0.9 scale) | 12u (~10.8px) | 15u |
| `.cap-lbl` (SVG) | 13u (~11.7px) | 15u |
| `.eng .ek`, `.wm-label` | .72rem | .78rem |
| `.phase .pnum`, `.gate .glabel` | .74rem | .78rem |
| `.foot .disc` | .77rem | .84rem |
| `.ostat span`, `.frole` | .82rem | .9rem / .88rem |
| `.creds li` | .9rem | .94rem |
| `.phase li` | .92rem | .95rem |
| `.eyebrow` | 12px | 12.5px |

The two SVG values also have `@media(max-width:760px)` overrides (17/19u)
that must be re-tuned once the base sizes and viewBox height change.

## 4. Apple-style section transitions

Current boundaries are hard: one `<hr class="divider">`, `.band` has
`border-top`/`border-bottom: 1px solid`, and `.founder` switches to
`--surface-2` abruptly.

- Delete the `<hr class="divider">` and the 1px rules on `.band`.
- Give tinted sections **soft gradient edges** instead of borders — a
  `::before`/`::after` on the tinted section fading `--ground` → `--surface-2`
  over ~80px, so the colour change is a transition rather than a line.
- Smooth the reveal: `.reveal` currently `translateY(16px)` /
  `transition: .6s ease`. Change to `translateY(24px)` and
  `cubic-bezier(.22,1,.36,1)` at ~.9s — long, decelerating, no bounce.
- **Stagger children.** In the `<script>` IntersectionObserver, when an element
  intersects, set `transitionDelay` from its index among `.reveal` siblings
  (cap ~60ms × 4) so grids cascade instead of snapping in together.
- Loosen the observer slightly: `threshold: 0.12`,
  `rootMargin: '0px 0px -12% 0px'` so reveals begin a touch earlier.
- `prefers-reduced-motion` branch already exists and must keep bypassing all
  of the above.

## 5. Pharma appetite moves into "Why the eye"

Delete the standalone `<section class="band" id="demand">` and add its figure
as a third `.ostat` in the why-the-eye column, matching the existing two:

```
$1.3B (2024) — Merck/EyeBio; pharma is buying ophthalmic assets, not building them
```

Keeps the citation attached. Removes a whole section, tightening flow. Note
`.band`, `.deal`, `.deal .big`, `.deal .cite` CSS becomes dead once the
section goes — check nothing else uses it before deleting (`.band .eyebrow`
is scoped to it).

## 6. Personal story + community standing

Both land in the `#founder` block, which currently has a role line, name, a
one-line vantage summary and a six-item `.creds` grid.

**Story** (~90 words, first person, drafted from `CLAUDE.md` facts only):
retinal degeneration research at ANU JCSMR → the gap between what the lab
produces and what reaches patients → founding **Vision ACTion** to put
researchers, clinicians and patients in one room → co-founding ErythroSight
to take a retinal therapeutic forward → now helping other companies make the
same call earlier and more cheaply. The emotional "why" is inferred and must
be flagged to the user for correction — it is the one part not in the notes.

**Community standing** — add to `.creds`, all documented:
- Founder, **Vision ACTion** — research translation forum uniting
  researchers, clinicians and patients
- **Genetics lecturer**, ANU JCSMR — 120+ medical students, 6 mentored
- **STEM outreach** — Canberra Science Week, 8,000+ attendees

Do not state or imply any ErythroSight exit/licensing outcome
(`CLAUDE.md` explicitly forbids it). Keep client names generic.

## 7. Make the repo self-sufficient for a fresh Claude account

Goal: clone the repo in a new account and continue with no loss of context.
Today the code is safe but the *reasoning* is not — it lives in this session
and in a plan file outside the repo.

Add a `docs/` directory:

- **`docs/HANDOVER.md`** — the entry point. What this repo is, which branch is
  live (`dev`), what is built vs. outstanding, how to run the agent stack
  (`cd tractum-agents && ./bootstrap.sh`, `make help`), how to preview and
  republish the site, and the open decisions list (photo, FAQ, hero balance,
  triple→four vantage mirroring, Track 1 fee/duration numbers).
- **`docs/DECISIONS.md`** — the decision record from this session, each with
  its rationale so a fresh session does not re-litigate: boutique expert
  practice / no scaling; two asymmetric arms; first person "I"; Merck stays
  named (**closed**); scarcity as positioning; bottom-up sizing, never the
  $37B drug market as TAM; latent demand is the binding risk; screen-not-
  assessment for the BD pipeline; human gate is structural with no global
  auto-approve.
- **`docs/plans/`** — copy the working plan file in, so the in-flight design
  reasoning travels with the repo.

**Artifact caveat, must be stated in `HANDOVER.md`:** the published artifact
(`https://claude.ai/artifact/BVNabh1kXuyG8GnC7eReVg`) is private to this
account. A new account **cannot** update that URL — it will publish its own
and get a new link. Nothing is lost because `index.html` is the source of
truth in the repo, but the existing link does not transfer. Record the URL
and the republish command anyway, for use from *this* account.

Also add a short "Continue here" pointer at the top of the root `CLAUDE.md`
aimed at `docs/HANDOVER.md`, since `CLAUDE.md` is what a fresh session reads
first.

---

## Files

- `/home/user/startup/index.html` — changes 1–6.
- `/home/user/startup/docs/HANDOVER.md`, `docs/DECISIONS.md`,
  `docs/plans/` — new (change 7).
- `/home/user/startup/CLAUDE.md` — add the "Continue here" pointer.
- Flagged for a later, separate decision: `/home/user/startup/CLAUDE.md` and
  `/home/user/startup/tractum-agents/company/COMPANY.md` (triple → four
  vantage).

## Verification

Reuse the Playwright harness pattern from this session (scratchpad script,
`/opt/pw-browsers/chromium`, `.reveal` forced visible via injected style):

1. Widths **1280 / 820 / 390 / 360**, light **and** dark: assert
   `scrollWidth - clientWidth === 0` and zero page errors.
2. Screenshot `#why` (four-ray lens), `#founder` (story + creds) and a
   section boundary at each width; read them back and confirm the lens
   labels are legible at 360px and the gradient edges read as a fade, not a
   band.
3. Confirm no text renders below ~12.5px: spot-check computed styles for
   `.ostat b small`, `.cap-sub`, `.eyebrow` via `getComputedStyle`.
4. With `prefers-reduced-motion: reduce` emulated, confirm all `.reveal`
   content is visible immediately and no transition/delay is applied.
5. Balanced-tag check (`<section>`, `<div>`, `<svg>`) and grep for dead
   `.band`/`.deal` references and any re-introduced "we/our".
6. Page height before/after — expect a net reduction despite added content,
   since the demand band is absorbed.
7. Portability check: from a clean temp directory, clone `dev` fresh and
   confirm `docs/HANDOVER.md` alone is enough to orient — the agent stack
   bootstraps (`./bootstrap.sh`, `make check`), and the site opens. This is
   the same fresh-clone test used earlier in the session, extended to the
   docs.

## Commit / push

One commit per logical group rather than a single large one: (a) type scale +
transitions, (b) four-ray lens + copy, (c) demand band merge, (d) personal
story + community, (e) `docs/` handover material. Push to `dev`, then
republish the artifact to the existing URL from this account so the live
preview stays current.
