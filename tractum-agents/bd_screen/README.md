# BD screen

Builds a list of biotechs whose **lead asset may already be relevant in the eye** —
the top of the Tier 1 funnel, so outreach starts from a thesis about a specific
molecule rather than a cold email.

Adapted from `tractumbio/biotech-trading-strategy`, which built the same universe
for an investment thesis. Steps 1–4 are that pipeline, largely unchanged. Step 5
is new and is the part that makes it Tractum's.

## What it produces

`workspace/shared/bd-shortlist.md` — readable by **every** agent, since it lands in
the shared store. Two lists: prospects worth an hour of your reading, and companies
that already name the eye (competitors, partners or comparables — never pitch targets).

## Running it

```bash
pip install -r bd_screen/requirements.txt     # separate from the agent runtime
cd bd_screen

python src/fetch_asx_companies.py       # 1. ASX directory -> healthcare candidates
python src/classify_biotech.py          # 2. Yahoo enrichment -> therapeutic developers
python src/fetch_clinical_trials.py     # 3. ClinicalTrials.gov -> development stage
python src/build_dataset.py             # 4. final company list
python src/score_ocular_relevance.py    # 5. ocular relevance -> shortlist
```

Or `make bd-screen` from `tractum-agents/`.

Then hand it to a scientist:

```bash
python -m orchestrator.run chat ophtha_science --session bd
# /load shared:bd-shortlist.md
```

## How the scoring works

Computed in code from weights visible in `src/score_ocular_relevance.py`. Every
point is traceable to the phrase that earned it — the `why` column shows the
arithmetic. No model decides the score.

| Signal | Weight | Meaning |
|---|---|---|
| already-ocular | +6 | names the eye itself — flagged, never pitched |
| mechanism-ocular-precedent | +4 | VEGF, complement, inflammasome, neuroprotection… |
| modality-travels-to-eye | +3 | AAV, siRNA, antibody fragment, peptide, EV |
| degenerative-or-inflammatory | +2 | the disease biology the eye shares |
| systemic-only-delivery | −3 | oral, IV, inhaled, transdermal |
| indication-far-from-eye | −2 | dermatology, GI, urology… |
| stage | +3 / +2 / 0 | preclinical & Ph1 / Ph2 / Ph3 — Ph3 is too late to matter |

Tune the weights in that file. The shortlist shows what changed.

## What this is not

**A screen, not an assessment.** A high score means a scientist should spend an hour
on it. Nothing here has been judged. `ophtha_science` takes the shortlist and is
expected to throw most of it out — that is the design, not a failure of it.

## Scope limits, stated plainly

- **ASX only.** Australian listed companies. The global universe needs another
  source; SEC EDGAR was investigated and dropped upstream when scope narrowed.
- **Keyword matching, not semantics.** A company describing its mechanism in
  unusual language will be missed. False negatives are the expected failure mode.
- **Two unofficial endpoints.** The ASX directory and announcements feeds are
  undocumented and can rotate without notice. ClinicalTrials.gov is official.
- **ANZCTR has no API**, so AU-only small-caps in local trials can show as
  `Preclinical` when they are not.
- Read ASX's terms of use before running step 5 (announcements) at any scale.

## Data

`data/reference/` is committed — hand-written input. Everything under `data/raw/`
and `data/processed/` is generated and gitignored; each clone builds its own.
