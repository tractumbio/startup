# Handover — start here

Everything needed to pick this project up in a fresh session or a new Claude
account. Read this, then the root `CLAUDE.md` (strategy) and
`docs/DECISIONS.md` (what's already settled and why).

## What this repo is

Tractum Bio Consulting — a boutique ophthalmic advisory practice run by
Dr. Adrian Cioanca. Two things live here:

| Path | What it is |
|---|---|
| `index.html` | The Tier 1 website — single page, self-contained, no build step |
| `assets/` | Logo and email-signature reference images |
| `tractum-agents/` | Four local Ollama agents with a human gate, plus a BD screen |
| `CLAUDE.md` | Strategy, positioning, founder facts. Read before writing copy |
| `docs/` | This handover, the decision record, and working plans |

## Branch

**`dev` is the live branch.** All current work is there.

```bash
git clone https://github.com/tractumbio/startup.git
cd startup && git checkout dev
```

Note the repo has **no `main`** — the default branch is
`claude/branch-repo-startup-622dv6`, a historical artefact. Renaming it to
`main` in GitHub settings is a one-click cleanup that preserves open PRs.

## The website

`index.html` is a single self-contained file — no framework, no build, no
external CSS or JS. Open it directly in a browser.

Section order: hero → approach (the track rail) → why this / why me →
engagement → about → execution strip → contact.

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

There is no test suite; the page is verified by rendering it. The pattern used
throughout, with the pre-installed Chromium at `/opt/pw-browsers/chromium`:

1. Load the page, inject `.reveal{opacity:1!important;transform:none!important}`
   (content is scroll-triggered and won't appear otherwise).
2. Assert `scrollWidth - clientWidth === 0` at **1280 / 820 / 390 / 360**.
3. Screenshot the changed sections and actually look at them.
4. Check both `colorScheme: 'light'` and `'dark'`.
5. For motion changes, emulate `reducedMotion: 'reduce'` and confirm content
   is visible with no transition.
