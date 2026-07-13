# Tractum Bio Consulting — Project Notes

Working notes for the Tractum Bio Consulting website. This file exists so context isn't
lost between sessions — read it before starting new work on this repo.

## Brand name

**Tractum Bio Consulting.** (An earlier prototype built in a separate claude.ai session
used the name "Tractus" — that name is superseded. If you find old files/exports
referencing "Tractus," rename to Tractum Bio Consulting before reusing them.)

## What the company does — two practices

### 1. CRO Automation Services (for any CRO)

Generic pipeline automation — not preclinical-specific, not tied to one CRO type.
Sold as: your scientists do the hands-on bench work, our tools handle analysis and
reporting.

**Workflow:** Analysis Plan → Process Assay Data (any assay/instrument) → Best-Practice
Analytics → High-Quality Reports.

**Core properties:** Deterministic · Fully auditable · Human-in-the-loop.

**Selling points:**
- Frees scientists for bench work instead of manual analysis/reporting
- Saves time, increases throughput without adding headcount
- Consolidates legacy platforms/instruments into a single pipeline (no rip-and-replace)
- Analytics stay current with best practice (updated centrally, not per-project)
- Enables new revenue-generating service lines from existing capability (e.g. RNA-seq,
  deeper insight from data already being generated)
- Analysis quality matches client expectations — important because sponsors have deep
  expertise in the assays they're buying
- Enterprise-grade: secure, auditable, integrates into existing GMP/GLP workflows rather
  than replacing them; ongoing support included

### 2. Ophthalmology Consulting (for any biotech entering ophthalmology)

Positioned as a **valuation-uplift argument**, not a services list. The pitch: "your
lead asset may already have a second market — it's in the eye."

**Centerpiece:** an illustrative small biotech valuation going **$85M → $150M (+76%)**
by adding an ophthalmic indication. Shown as:
- Before/after headline number with uplift badge
- Sum-of-the-parts waterfall (base asset + ophthalmic indication added)
- Scenario range: +30% / +76% / +140% (reads as modelling, not a cherry-picked number)
- Plain-language methodology note + "illustrative" disclaimer

**Supporting evidence (real, cited):**
- Ophthalmic drug market ~USD 37.49B (2025) → USD 60.29B (2031) — Mordor Intelligence
- Retinal indications carry pricing power (therapies often >$2,000/injection)
- 505(b)(2) repurposing pathway: 60–80% lower development cost, 50–70% success
  probability vs. 10–30% for new molecular entities
- "Pipeline-in-a-product" framing: sophisticated buyers value expansion optionality
- Precedent: bevacizumab (Avastin) — FDA approved 2004 for metastatic colorectal
  cancer; ophthalmic use discovered off-label, became the mechanism-is-real proof point

**Process (5 steps):** mechanism deep dive → indication screening (unmet need +
profitability) → safety/efficacy research plan → IP & path to Phase 1 → CRO matching
(Tractum connects/orchestrates, does not run the bench itself).

**Scope:** broad ophthalmology — retina (AMD, DR, RVO, GA/IRD) *and* anterior segment
(dry eye, glaucoma).

## Site structure (from the prototype build)

A prior claude.ai session built a working HTML prototype with this structure:
- `index.html` — gateway home, splits visitors into the two practices
- `tractus.html` → rename to reflect CRO Automation Services page
- `tractus-ophthalmology.html` → rename to reflect Ophthalmology Consulting page

Design system used: green = CRO practice, blue = biotech/ophthalmology practice,
consistent across both. Mobile breakpoints tuned at 600px and 380px (not just the
default 640px) — phone-width overflow was a recurring bug class, especially on the
valuation waterfall bar and disease-tabs nav; watch for this if rebuilding.

**Status:** prototype files are NOT in this repo. They exist only in the other
claude.ai session/project ("CRO Consulting") and have not been imported here yet.
If continuing from those files, get them uploaded into this repo first rather than
reconstructing from memory.

## Founder — Dr. Adrian Cioanca

- PhD in retinal degeneration research, Australian National University (ANU), John
  Curtin School of Medical Research
- **University Medal** — awarded to ANU's top-ranking Honours graduate (Bachelor of
  Advanced Science, 1st Class Honours, 2017)
- **Frank Fenner Medal** — outstanding PhD thesis, 2022 (thesis: understanding retinal
  degeneration via high-throughput gene expression)
- ~25 peer-reviewed publications over 4 years of research; **400+ citations, h-index 14**
- Published in *Communications Biology*, *Journal of Extracellular Vesicles*,
  *Molecular Neurobiology* / *Molecular Neurodegeneration*, among others
- Postdoctoral Fellow, Natoli Group / Clear Vision Research Lab, JCSMR — research
  focus: RNA-based therapeutics for retinal degeneration, targeting transcription
  factors; also extracellular vesicle biology (EVs as intercellular signaling in
  retinal health/disease)
- Co-founder, **ErythroSight** — accelerator-backed venture developing red blood
  cell-derived extracellular vesicle therapeutics for age-related macular degeneration.
  Raised $670K, holds 3 international patents; built partnerships with 4 biotech
  partners leading to a $3M capital raise. Participated in ON Prime / ON Accelerate
  (CSIRO deep-tech commercialization program, <5% acceptance rate).
- **J.G. Crawford Prize nominee** — 2 of ~7,000 ANU graduates
- Currently **Data & AI Consultant, Accenture** (Canberra, Australia)
- Led a 7-person team spanning gene therapeutics, preclinical models, and biomarker
  analytics; designed and delivered a **$200K Merck & Co. preclinical model
  project — 8× ROI**
- Technical skills: 5+ years R, Python, SQL; R Shiny apps; R Markdown automated
  reporting pipelines; statistical modelling (lm, glm, gam, XGBoost, ML frameworks);
  end-to-end data pipelines (wrangling → modelling → visualisation → report); DCF and
  rNPV financial modelling for investor materials
- Two bio source documents exist but are NOT yet in this repo:
  `CV_DAI_Adrian_Cioanca_2.pdf`, `Adrian_Cioanca_Resume_2025_data_analytics.pdf`
  (referenced in a separate claude.ai project; upload here if needed for further bio
  work).

## Related but SEPARATE venture: "Ophthalmic Precision" (investment memo)

**This is not Tractum Bio Consulting.** A separate investment memorandum exists for a
different, parallel play — do not blend its messaging into the Tractum Bio Consulting
site. Keep them distinct.

**What it is:** a pitch to acquire/build an operating, AI-powered **specialist
ophthalmic preclinical CRO** (i.e. actually running the lab and selling preclinical
services directly), not a consulting/advisory business. Framed as "A Commercial
Investment Case: Specialist Retinal Preclinical Services, Powered by AI-Automated Data
Pipelines," dated 2025.

**Headline numbers:** $450M addressable CRO market today, 12% annual growth, 25% AI
cost reduction in data analysis claimed, 4–5× 5-year return on incremental capital.
Illustrative model on a $50M baseline CRO: revenue $57M (Yr1) → $66.7M (Yr2) → $77.2M
(Yr3) → $94.1M (Yr5); Year 5 incremental EBITDA $11.5M; 12–14× specialist M&A multiple;
$138–161M enterprise value created.

**Thesis:** two converging trends — (1) ophthalmic drug pipeline growing ~2× the rate
of the broader preclinical CRO market on a $6.3B 2024 funding wave into retinal gene
therapy/cell therapy/biologics, and (2) AI lab automation cutting data-analysis costs
50–80%. No current competitor combines both. Plan: acquire a boutique ophthalmic CRO
(named candidates: EyeCRO, Powered Research, Ichor) for $5–15M all-in entry cost, layer
on AI pipelines, capture the specialist pricing premium (+15–30% over generalists) and
AI throughput gains.

**AI pipeline time-savings claimed per assay type:** OCT/fundus imaging 90–95%, ELISA
processing 80–85%, LC-MS/MS peak integration 70–85%, cell/morphology analysis 60–80%,
tox histopathology 40–50%, statistical reporting 65–70%, EDC/data capture 30–50%.
Annual labour cost avoidance $600K–$1.8M; AI implementation cost $400K–$1.0M; payback
12–18 months.

**Named market data points:** global preclinical CRO market $6.5B (2025, 7–8% CAGR);
ophthalmic preclinical CRO segment $450M (10–12% CAGR); ocular gene therapy market
$7.4B by 2032 (25% CAGR); $6.3B ophthalmology VC funding in 2024 (+$1.1B in Q1–Q2 2025);
73 active ocular gene therapy trials; 75 GA drugs in development (45 preclinical);
notable pharma validation deals — Merck $3B EyeBio, Lilly $475M MeiraGTx, BI $1B
Re-Vana. BIOSECURE Act (2024) cited as a tailwind, redirecting $2B+ from Chinese CROs
to Western providers.

**Named target companies (35+ identified, examples):** Gene therapy — Cirrus, RhyGaze,
PulseSight, Mirugen, HuidaGene. Cell therapy — GelMEDIX, InGel Therapeutics, Eyestem.
Small molecule/biologic — AsclepiX, ForwardVue, SeaBeLife, Re-Vana, Therini Bio. RNA
therapeutics — Isarna, City Therapeutics, Astherna. Large pharma divisions — Regeneron,
Roche, AbbVie, Merck (EyeBio), BI. Top 10 priority targets ranked with funding amounts
and outsourcing-propensity status are in the source deck if needed later.

**Competitive landscape named:** Charles River, Labcorp/Covance, EyeCRO, Experimentica,
Iris Pharma, Powered Research, Pharmaron — positioned as generalist-vs-specialist ×
no-AI-vs-full-AI, with this play claiming the specialist+AI whitespace.

**Source:** Google Slides deck, "Ophthalmic Precision — CRO + AI Analytics," read via
Drive on 2026-07-13 (file id `1JmYMkzff-3sk1EEbr7Fk4y85V2EFIfiXIEiy6jt3_Qo`). Full text
was extracted; go back to the source file for exact figures/formatting if rebuilding
this into its own materials.

## Team — other roles needed (not yet staffed with real people)

Ideal profiles drafted for: IP & scientific defensibility (PhD + patent law), molecular
biology & therapeutic development, biotech commercialization/investor, retina
specialist clinician (MD — currently the weakest-covered gap), strategy & business
development, CRO operations/quality specialist, engineering/data infrastructure lead,
preclinical safety/toxicology, regulatory affairs (ophthalmic). Recommendation: split
into a small core team + a named advisory board rather than stretching everyone across
too many hats.

## Design direction (from original brief)

Premium enterprise SaaS + biotech strategy + scientific publishing feel. No AI-as-hero
framing (AI is an enabling technology, never the headline). No generic biotech stock
photography, no hype language ("revolutionary," "disruptive"). Heavy use of white
space, typographic hierarchy, restrained color, workflow diagrams, decision trees,
cited evidence cards.

**Palette:** primary navy `#10233F`, deep scientific blue `#2463A7`, muted teal
`#2B8C86`, soft blue-grey `#EAF0F5`, warm off-white `#F8F9F7`, charcoal `#24313D`,
optional amber accent `#C58A2A` for decision points. (Note: the actual prototype used
green/blue as the two-practice color system — reconcile with this palette before
finalizing.)

## Open decisions / gaps to resolve

1. Import the real prototype HTML files + PDFs into this repo (currently absent).
2. Reconcile the green/blue practice-color system against the navy/teal palette above.
3. Fill in a named specific for Adrian's "AI/data systems" work (currently unbacked by
   a concrete example).
4. Decide on core team vs. advisory board split and recruit/confirm the clinician gap.
5. Tech stack / CMS / hosting not yet chosen for a production build.
