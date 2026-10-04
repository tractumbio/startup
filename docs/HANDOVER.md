# Handover — start here

Everything needed to pick this project up in a fresh session or a new Claude
account. Read this, then the root `CLAUDE.md` (strategy) and
`docs/DECISIONS.md` (what's already settled and why).

## What this repo is

Tractum Bio Consulting — a boutique ophthalmic advisory practice run by
Dr. Adrian Cioanca. Two things live here:

| Path | What it is |
|---|---|
| `index.html` | Landing page — shared claim, two doors, why the eye, founder, contact |
| `asset.html` | For biotech — tracks, outcome, engagement (was the old `index.html`) |
| `capability.html` | For labs — ophthalmic services, omics, pipeline automation, build rail |
| `styles.css`, `site.js` | Shared by all three pages — edit once, applies everywhere |
| `assets/` | Logo and email-signature reference images |
| `tractum-agents/` | Four local Ollama agents with a human gate, plus a BD screen |
| `CLAUDE.md` | Strategy, positioning, founder facts. Read before writing copy |
| `docs/` | This handover, the decision record, and working plans |

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

- `index.html`: hero → two doors → why the eye → founder → contact
- `asset.html`: hero → track rail → why this / why me → engagement → founder → contact
- `capability.html`: hero → three capabilities → pipeline → build rail →
  what you own → engagement → contact

The founder block exists in both `index.html` and `asset.html` (outbound links
to biotechs land directly on `asset.html`, so it must stand alone). Edit both.

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

1. **A photograph.** The About block still shows the logo mark where a portrait
   should be. For a practice that sells a person this is the single biggest
   trust gap on the page.
2. **Track 1 fee and duration.** The engagement section states shape only
   ("fixed fee", "weeks, not quarters"). Real numbers convert better; vagueness
   reads as expensive.
3. **The personal story** in the About block was drafted from documented facts.
   The emotional core is inferred — read it and make it true.
4. **Triple → four vantage.** The site now shows four capabilities (biology,
   path, deal, strategy). `CLAUDE.md` and `tractum-agents/company/COMPANY.md`
   still document a *triple* vantage. Mirror them, or `brand_voice` will keep
   enforcing three.

## Open — Claude can do next

- **FAQ block** — "What if the answer is no?", "Do you run the lab work?",
  "How do you handle confidentiality?", "What does it cost?"
- **Hero balance** — roughly 45% of the hero is empty on the right at desktop.
- **Tier 2 page** — the pharma/CRO capability-build buyer currently has
  nothing to land on. This is a whole page that does not exist yet.
- **A second site** for the CRO automation arm — decided as a one-pager served
  by referral, deliberately not brand-led.

## How work gets verified here

There is no test suite; the site is verified by rendering it. That procedure is
now a project skill:

```bash
node .claude/skills/site-verify/verify.js --shots <scratch-dir>
```

It checks every page at 1280/820/390/360 in light and dark, overflow, errors,
links and anchors, markup balance, minimum text size and reduced motion — then
**look at the screenshots**, because purely visual faults pass every check. See
`.claude/skills/site-verify/SKILL.md`.

`.claude/hooks/session-start.sh` runs automatically at the start of every cloud
session: it installs the verify tooling and the agent stack's Python deps (~8s
cold, near-instant after), and prints a warning if the checkout is behind `main`.
