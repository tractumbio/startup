# Tractum Bio Consulting

| Path | What it is |
|---|---|
| [`sites/`](sites/) | One folder per website. `sites/tractumbio/` is the company site (static HTML, no build step). |
| [`tractum-agents/`](tractum-agents/) | Human-gated Ollama agent stack for the practice. |
| [`docs/`](docs/) | Handover, decisions, plans and reviews. Start with `docs/HANDOVER.md`. New documents go here. |
| [`CLAUDE.md`](CLAUDE.md) | Strategy and working notes, read at the start of every session. |

## Adding a site

Create `sites/<name>/` with its own `index.html`, `404.html`, assets and `robots.txt`. Each site must be
deployable by pointing a static host at its folder. Check it with
`SITE_DIR=sites/<name> node .claude/skills/site-verify/verify.js`.
