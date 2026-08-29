# inputs/

Source material for agent runs. **Everything here except this file is gitignored** —
client briefs, study data, papers and internal documents are safe to drop in.

Point an agent at a file with `--input`:

```bash
python -m orchestrator.run agent ophtha_science --input inputs/asset-brief.md
```

The file's contents fill the `{{input}}` field of that agent's task template; other
fields are filled with `--set key=value`. Anything you don't provide shows up in the
prompt as `[NOT PROVIDED: field]` rather than silently vanishing — a blank field is how a
model invents one.

Suggested files:

- `asset-brief.md` — the molecule, its current indication, mechanism, stage
- `literature/` — papers or abstracts for `lit_intel` to work through
- `valuation-inputs.md` — comparables, pricing, population figures with their sources
- `voice-samples/` — your own writing, for `brand_voice` to match

Nothing here is read automatically. Agents only see what you pass on the command line.
