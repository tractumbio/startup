# Handover — start here

Everything needed to pick this project up in a fresh session or a new Claude
account. Read this, then the root `CLAUDE.md` (strategy) and
`docs/DECISIONS.md` (what's already settled and why).

## What this repo is

Tractum Bio Consulting — a boutique ophthalmic advisory practice run by
Dr. Adrian Cioanca. Two things live here. Site files are under `sites/tractumbio/` (paths below are relative to it). Pages now live in folders: `asset.html` is
`biotech-consulting/index.html`, `capability.html` is `cro-services/index.html`, `about.html` is `about/index.html`,
`privacy.html` is `privacy/index.html`. See `sites/tractumbio/README.md`:

| Path | What it is |
|---|---|
| `index.html` | Landing page — shared claim, two doors, why the eye, founder, contact |
| `asset.html` | For biotech — tracks, outcome, engagement (was the old `index.html`) |
| `capability.html` | For labs — ophthalmic services, omics, pipeline automation, build rail |
| `about.html` | Full founder profile: story, background, how I work |
| `privacy.html`, `404.html` | Privacy note and page-not-found (the 404 is `noindex`) |
| `styles.css`, `site.js` | Shared by all three pages — edit once, applies everywhere |
| `assets/` | Logo, email-signature reference, founder portrait (`adrian.png`), favicon, OG card (`og.jpg`) |
| `tools/make_og.py` | Regenerates `assets/og.jpg` — run it after changing the landing headline |
| `robots.txt`, `sitemap.xml` | For the production domain `tractumbio.com` |
| `tractum-agents/` | Four local Ollama agents with a human gate, plus a BD screen |
| `CLAUDE.md` | Strategy, positioning, founder facts. Read before writing copy |
| `docs/` | This handover, the decision record, working plans, and `reviews/` (external site reviews) |

## Branch

**`main` is the live branch.** `dev` is kept identical to it.

```bash
git clone https://github.com/tractumbio/startup.git
cd startup && git checkout main
```

Note the repo has **no `main`** — the default branch is
`claude/branch-repo-startup-622dv6`, a historical artefact. Renaming it to
`main` in GitHub settings is a one-click cleanup that preserves open PRs.

## The website

Three static HTML pages sharing `styles.css` and `site.js` — no framework, no
build step. Open any of them in a browser.

- `index.html`: hero → two doors (each ends with its first paid step) → credential strip → why the eye → founder → contact
- `asset.html`: split hero (route card) → track rail → why this / why me →
  engagement → compact founder card → contact
- `capability.html`: split hero (route card) → three capabilities → pipeline →
  build rail → what you own → engagement → contact

The full founder profile lives only on `about.html`; the landing page keeps a
short bio that links to it. `asset.html` carries a compact card that links to it, so
there is one place to edit. Navigation collapses to a menu button below 900px
(`.menu-btn` + `#primary-nav`, toggled in `site.js`). Every page has a skip
link, favicon, and Open Graph tags pointing at `assets/og.jpg` on
`https://tractumbio.com/` — if the site is hosted at another origin, change
those absolute URLs.

Footer links: LinkedIn (`adrian-c-58743b25a`) and Google Scholar
(`m-zNPssAAAAJ`), both taken from the `tractumbio/resume` repo.

Design constraints that matter (see `CLAUDE.md` for the full brief):
- Premium, restrained. No stock photography, no hype vocabulary.
- Amber is reserved for decision points only.
- First person "I", never corporate "we" — this is a one-person practice.
- Every number carries a citation, or is labelled illustrative.
- Known bug class: phone-width horizontal overflow. Always verify at 360px.

### Previewing and publishing

The page has been published as a private Claude Artifact at:

```
https://claude.ai/artifact/BVNabh1kXuyG8GnC7eReVg
```

**That URL belongs to the account that created it.** A different Claude
account cannot update it — it will publish its own copy and get a new link.
Nothing is lost: `index.html` in this repo is the source of truth. From the
original account, republish with the Artifact tool passing that URL so the
link stays stable.

## The agent stack

```bash
cd tractum-agents
./bootstrap.sh      # venv, deps, .env, preflight — safe to re-run
make help           # every task
make doctor         # which Ollama models are missing
make check          # sanity check before committing
```

Needs Ollama running locally (`ollama serve`) with the models named in
`config/models.yaml`. `tractum-agents/CLAUDE.md` documents the design
decisions — read it before changing anything in that directory.

The BD screen (`tractum-agents/bd_screen/`) builds a list of biotechs whose
lead asset may already be relevant in the eye. Heavier dependencies, installed
separately: `pip install -r bd_screen/requirements.txt`, then `make bd-screen`.

## Open — needs Adrian, not Claude

1. **A calendar-booking link.** Every CTA is still `mailto:`. A Calendly-style
   link converts far better for a "free intro call"; drop the URL in and the
   `.mailbtn` / `.nav-cta` hrefs can switch to it.
2. **Track 1 fee and duration.** The biotech page now defines the first paid
   step in full (inputs, work, deliverables, decision, exclusions) but says only
   "fixed scope and fee". Supply a duration range and a fee basis you can keep.
3. **The personal story** in the About block was drafted from documented facts.
   The emotional core is inferred — read it and make it true.
4. **Two case studies.** One ophthalmic capability, one analytics/automation.
   Use the six-part template in `docs/reviews/2026-10-04-website-review.md` §7
   (context, starting point, your role, work delivered, evidence, limitations).
   Qualitative is fine; client approval or anonymisation is required.
5. **Founder numbers conflict.** `CLAUDE.md` says ~25 publications, 400+
   citations, h-index 14, 3 patents; the resume repo says h-index 9, 196
   citations, 2 patents. The site no longer prints citation metrics (it links
   Google Scholar), but CVs and decks still need one answer.
7. **Confirm three statements written on your behalf** (Oct 2026 review pass):
   - CRO page: "any overlap with my biotech advisory clients is declared before
     we start" — a conflict-of-interest commitment.
   - CRO page: "Retina is my hands-on research field; anterior segment and ocular
     safety are delivered with specialist partners."
   - Landing page: CRO scoping returns "a fixed quote for the build".
8. **Analytics.** The review proposes measuring route visits, contact clicks,
   enquiries, qualified enquiries and engagements. Pick a privacy-respecting tool
   (e.g. Plausible) and it can be wired in; never put asset details in event data.
7b. **Confirm the privacy note** (`privacy.html`). It is accurate for the site as
   built (no cookies, analytics or third-party loads) and promises email is used
   only to reply and to do agreed work. If analytics are added, it must change.
8b. **Hosting.** The site is static and ready to deploy (any static host works:
   GitHub Pages, Netlify, Cloudflare Pages). Point the host's 404 at `404.html`
   and DNS for tractumbio.com at it. This needs your account, so it is not done.
6. **GitHub default branch** is still the old `claude/...` branch. Flip it to
   `main` in Settings → Branches.

## Open — Claude can do next

- **FAQ block** — "What if the answer is no?", "Do you run the lab work?",
  "How do you handle confidentiality?", "What does it cost?"
- **Case-study section** — the layout can be built as soon as the content in
  item 4 exists; do not publish placeholders.
- **Hypothetical valuation model** — only if Adrian wants the uplift story back:
  a worked, clearly-labelled model with every input visible (see `CLAUDE.md` →
  Claims discipline).

## How work gets verified here

There is no test suite; the site is verified by rendering it. That procedure is
now a project skill:

```bash
node .claude/skills/site-verify/verify.js --shots <scratch-dir>
```

It checks every page at ten widths (1440 down to 320) in light and dark, overflow,
errors, links and anchors, markup balance, minimum text size, WCAG text contrast,
nav/menu behaviour, JavaScript-off rendering and reduced motion — then
**look at the screenshots**, because purely visual faults pass every check. See
`.claude/skills/site-verify/SKILL.md`.

`.claude/hooks/session-start.sh` runs automatically at the start of every cloud
session: it installs the verify tooling and the agent stack's Python deps (~8s
cold, near-instant after), and prints a warning if the checkout is behind `main`.
