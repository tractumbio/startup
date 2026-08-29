# Tractum Bio Consulting — Project Notes

Working notes for the Tractum Bio Consulting website. This file exists so context isn't
lost between sessions — read it before starting new work on this repo.

## Brand name

**Tractum Bio Consulting.** (An earlier prototype built in a separate claude.ai session
used the name "Tractus" — that name is superseded. If you find old files/exports
referencing "Tractus," rename to Tractum Bio Consulting before reusing them.)

Domain **tractumbio.com** is live; founder email is `adrian@tractumbio.com`. Real logo
asset recovered from Drive and saved to `assets/logo.png` (blue arrow-through-"T" mark,
wordmark "tractumbio," tagline "WORKFLOW AUTOMATION" — that tagline only reflects the
CRO practice, so don't use the tagline version in contexts covering both practices).
Reference email signature saved to `assets/emailsig.png` — confirms Adrian's title as
**Managing Director and Founder**.

## Strategic direction (CURRENT — an ophthalmic-focused firm)

**Supersedes the earlier "two independent practices (generic CRO automation + biotech
ophthalmology)" framing.** Tractum is narrowing to ONE domain — **ophthalmology** — to
play entirely to Adrian's real moat. Generic "any preclinical CRO automation" is NOT the
centerpiece; the data/analytics/pipeline skill is retained but applied IN SERVICE OF
ophthalmology (it becomes the "advanced analytics" component of the pharma capability
build), not sold as a standalone generic CRO product.

**One firm, one domain, two buyer tiers (differentiated by what the client already
has / needs):**

**Tier 1 — Small biotech → advisory & guidance.** They lack ophthalmic expertise,
infra, and capability. Tractum guides them through the whole preclinical-to-IP journey:
is the eye a real, valuable opportunity for your asset (go/no-go + valuation) → then
guidance through the preclinical path to IP (mechanism → indication → safety/efficacy
plan → IP & path to Phase 1 → valuation modelling → CRO matching). Deliverable =
decisions + roadmap + defensible valuation story. *(This is the existing 5-act
ophthalmology journey — see "Ophthalmology Consulting" section below.)*

**Tier 2 — Pharma (and preclinical CROs wanting ophthalmic capability) → full end-to-end
capability build.** They already HAVE data infra (AWS/GCP) + research infra + resources;
they want ophthalmic testing capability in-house. **VALIDATED — Adrian has built
ophthalmic animal models for large pharma bringing testing in-house.** Tractum builds it
end-to-end, layered ON TOP of their existing infrastructure (we provide ophthalmic
domain capability + analytics, NOT infrastructure): bespoke disease modelling +
molecular/histology work + imaging + RNA (transcriptomics) + advanced analytics.
Deliverable = a working ophthalmic capability with method/know-how transferred and
analytics built. Bigger, deeper, higher-value engagement than Tier 1. *(The analytics
layer reuses the multimodal pipeline story in the "CRO Automation" section below.)*

**Why this focus is right:** eliminates the depth-vs-breadth problem (everything is
ophthalmic = everything plays to the moat); legible in one sentence ("we guide biotechs
into the eye, and we build ophthalmic capability for pharma"); both tiers validated by
real experience; the pharma "on top of existing infra" scope is realistic for a small
firm (specialist capability layer, not enterprise vendor — sidesteps the SOC 2 / GxP /
2am-support credibility problem because the client owns the infra). Trade-off
consciously accepted: smaller TAM (ophthalmology only) for credibility + focus — can
broaden later from strength.

**Boundary (unchanged):** capability build = enablement / method-and-know-how transfer,
NOT Tractum operating an ongoing lab/CRO (consistent with killing the "Ophthalmic
Precision" operate-a-CRO model).

**Additional capability layers folded into Tier 2 (engine, not standalone offerings —
do not spin these out as separate doors/pillars; they power the two tiers above):**

- **Agentic literature-intelligence workflows.** NLP/agentic pipelines continuously
  monitor published ophthalmic research to surface emerging retinal/ocular targets,
  mechanisms, and repurposing candidates — an expert (Adrian) then judges what's real.
  AI mines/ranks/surfaces; the scientist decides. Same human-in-the-loop philosophy as
  everywhere else. Powers Tier 1's mechanism/indication screening (faster, evidence-
  current) and is a sellable standing capability within Tier 2. Do NOT pitch as
  general "AI drug discovery across all of PubMed" — that's a red ocean (BenevolentAI,
  Recursion, Insilico) and reads as AI-as-hero, which the brand brief explicitly bans.
  Scope strictly to ophthalmology.
- **Cross-study predictive insight layer (long-term ROADMAP item, not sellable today).**
  As pharma clients run more studies through the same standardized Tier-2 pipeline, the
  accumulated structured data (multimodal: imaging, molecular, RNA, assay) becomes a
  growing evidence base that can be mined for cross-study patterns a single report never
  surfaces, and can reduce redundant animal studies (real regulatory tailwind to cite:
  FDA Modernization Act 2.0 / the 3Rs). **Do NOT call this a "digital twin" publicly —
  that implies a validated mechanistic simulation this firm hasn't built and can't yet
  prove ("show me the twin" is the obvious rebuttal).** Use grounded language: "cross-
  study intelligence" / "predictive insight layer." Position as where Tier 2 is
  HEADING with a long-running client, not a current deliverable — this is the
  compounding-value pitch made inside a Tier-2 engagement, not a fourth pillar to build
  and sell in parallel now.

**Pharma proof point:** cite generically ("built ophthalmic disease models for a global
pharmaceutical company") — keep client names private pending sign-off.

---

## Reference detail — the two service stories (now re-slotted under the tiers above)

The two worked stories below predate the ophthalmic-focus pivot. They are still the
content, re-slotted: the **CRO Automation / multimodal pipeline story = the analytics
component of Tier 2 (pharma build)**; the **Ophthalmology Consulting journey = Tier 1
(biotech advisory)**. Kept for their detailed narrative/value-prop work.

### 1. CRO Automation Services (analytics engine — now the Tier-2 analytics layer)

Generic pipeline automation — not preclinical-specific, not tied to one CRO type.
Sold as: your scientists do the hands-on bench work, our tools handle analysis and
reporting.

**Key point — two distinct value props, both must be present:**
1. **Improve what they already do** — make existing workflows better and raise product
   (deliverable) quality on services they already offer.
2. **Expand what they can offer** — help them launch entirely new service lines /
   enter new markets they don't currently serve (e.g. add RNA-seq, advanced imaging,
   or other capabilities without building every specialist in-house).

Don't let the page collapse into just "we make you faster" — the market-expansion
angle is equally central, not a minor add-on.

**Workflow:** Analysis Plan → Process Assay Data (any assay/instrument) → Best-Practice
Analytics → High-Quality Reports.

**Worked example — the concrete proof artifact for this page.** Tell it as a STORY (a
single study's journey from bench to client-ready report), not a feature list. Keep it
generic to any CRO — do NOT name a real CRO (no Iris Pharma etc.). Use genuinely
multimodal inputs: image data, numerical assay data, the experimental protocol, and
metadata.

**The sharp value prop (the spine):** Most analytics vendors have only ever sat at the
computer. Tractum has stood at the bench that generates the data, at the computer that
turns it into evidence, AND at the client's desk that receives the report — so the
pipeline is built to serve all three. That triple vantage (bench → computer → client)
is the moat; a software vendor only knows the middle one.

**The journey — one study, five acts:**
- **Act 1 — the bench:** a study wraps, producing multimodal raw data — high-content
  images, numerical assay readouts, the protocol that defines what it means, the
  metadata tying every file to subject/group/timepoint. Rich but heterogeneous, inert,
  scattered.
- **Act 2 — the old path (pain):** days of manual wrangling; images graded by hand,
  assay numbers pasted between tools, ad-hoc stats, thin methods. Sponsor gets 20+
  loose files and a report that never shows HOW each number was derived. Scientists
  stuck at the keyboard instead of the bench.
- **Act 3 — the pipeline (where the 3 vantage points show):** one pipeline that
  (a) reads protocol + metadata FIRST so it analyses in context, knowing design/arms/
  endpoints/acceptance criteria [= knows what happens at the bench];
  (b) processes each modality correctly, automation carrying the grind [= knows what
  must happen at the computer];
  (c) applies the RIGHT statistics for the design, consistently, every time;
  (d) keeps the human at the quality gate — scientists own exclusions/QC/sign-off;
  automation removes labour, never judgment.
- **Act 4 — the deliverable (payoff):** not 20 files — ONE report: accurate results,
  clear analytics, publication-grade figures, fully transparent traceable methods
  (every value maps to how it was computed). The sponsor — who knows the assay cold —
  can audit it, trust it, hand it to their board [= knows what the client wants to see].
- **Act 5 — the compounding edge (dynamic + adaptable):** modular, so a better method
  drops in centrally and every future study inherits it, and NEW services (RNA-seq /
  omics) plug into the same frame. Because Tractum understands the biology, those
  analytics are customised to the client's disease question, not a generic off-the-shelf
  readout. Deliverable keeps sharpening; service menu keeps widening.

**Why this carries both value props as ONE continuous story (not a bolted-on list):**
improve what you deliver today (Acts 3–4) and expand what you can offer tomorrow
(Act 5) are the same pipeline seen at two moments in time.

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

### 2. Ophthalmology Consulting (= TIER 1: small-biotech advisory & guidance)

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

**Worked story — tell the ophthalmology page as a JOURNEY (parallel in structure to the
CRO story), not a service list.**

**The sharp value prop (the spine):** a banker can model the upside but can't judge
whether the biology is real; a bench scientist can judge the biology but can't model the
deal or chart the path to the clinic. Tractum has been all three — the retinal
scientist, the biotech founder who raised on these very models, and the translational
developer — so the number handed over is one the client can defend to their board and
partners. The triple vantage is **biology → deal → path**, mapping to Adrian's real,
unfakeable credentials (retinal PhD/fluency; ErythroSight raise + rNPV/DCF modelling;
translational development). This is the direct answer to "why should I trust your
valuation?"

**The journey — one asset, five acts:**
- **Act 1 — the asset (setup):** a biotech has a lead molecule in its first indication;
  the board sees a single-asset company with a single-asset valuation. But mechanism
  doesn't care what the molecule was designed for — it may already be relevant in the
  eye, where no one is looking.
- **Act 2 — why the eye (reframe):** the eye is a uniquely favourable development site —
  small, contained, immune-privileged, directly accessible, microgram doses, deep
  regulatory/clinical precedent; retinal therapies carry pricing power; 505(b)(2)
  repurposing is cheaper/faster/higher-PoS (~50–70% vs 10–30% for a new molecule). A
  second eye indication is disproportionately de-risked upside on an asset already owned.
- **Act 3 — the rigorous assessment (where the 3 vantages show):** a decision funnel,
  not a service menu — mechanism deep dive (is the rationale REAL; the scientist
  vantage) → indication screening (unmet need AND profitability) → safety/efficacy plan
  (what evidence proves it) → IP & path to Phase 1 (defensible? route?) → valuation
  modelling (rNPV/DCF; the founder/investor vantage) → CRO matching (orchestrate the
  real development; the developer vantage — Tractum connects, doesn't run the bench).
- **Act 4 — the decision (payoff; NO-GO is the hero):** output is never a promise of
  success — it is a high-quality decision made before serious capital is committed.
  GO → focused roadmap to the next value-inflection point + defensible uplift story.
  NO-GO → clear scientific/commercial rationale for NOT pursuing; preserve capital.
  "We will tell you no" is what makes a yes worth trusting — the line that converts a
  skeptical CSO.
- **Act 5 — the prize, quantified (transparent, not hyped):** illustratively $85M →
  $150M (+76%) via a credible ophthalmic indication, shown as a transparent, TUNABLE
  sum-of-the-parts model with scenario range (+30% / +76% / +140%), every input visible,
  labelled illustrative. Point isn't the number — it's that a de-risked second
  indication is one of the highest-leverage moves a single-asset biotech can make.
  Precedent: bevacizumab (designed for colorectal cancer; ophthalmic value discovered
  later — the mechanism was always there).

**Deliberate symmetry with the CRO story (this is what makes the two practices read as
ONE firm, resolving the two-practice coherence risk):** both rest on a triple-vantage
claim (bench/computer/client ↔ biology/deal/path); both make the honest/human element
the trust anchor (human QC gate ↔ the no-go); both end on the compounding prize
(better+wider deliverable ↔ valuation uplift).

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

## Agent stack (`tractum-agents/`)

Four local agents on Ollama with a human gate at every stage — `lit_intel`,
`ophtha_science`, `valuation`, `brand_voice`. Lives in `tractum-agents/`, which has its
own `CLAUDE.md` covering design decisions, storage model and setup. Read that before
changing anything in there.

Setup is `cd tractum-agents && ./bootstrap.sh`, then `make help`.

The agents load `tractum-agents/company/COMPANY.md` and `BRAND.md` into every run, and
both were derived from **this** file — so a correction here should be mirrored there, or
the agents keep working from the stale version.

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
- **Title: Managing Director and Founder, Tractum Bio Consulting** (confirmed via email
  signature asset)
- Tractum itself (founded 2025) already has real, active client contracts — described
  in Adrian's CV as AI-powered ophthalmic drug development models and automated CRO
  data pipelines. **Client names are to stay private on the public site** (use generic
  language like "a global pharmaceutical company" — do not publish specific client
  names without their explicit sign-off first).
- ANU JCSMR: Postdoctoral Fellow & Genetics Lecturer, 2022–2026. Partnered with biotech
  and large pharma (named in CV) to build bespoke analytics pipelines; led a 7-person
  team; mentored 6 students (all top of cohort); delivered genetics lectures to 120+
  medical students (4.8/5 teaching score, pass rate improved 82% → 97%)
- ErythroSight (co-founder & CTO, 2023–2026): secured 3 patents, raised $670K; DCF/rNPV
  modelling; pitched at 3 national accelerators including CSIRO ON Accelerate (<5%
  acceptance). **Do not state or imply any exit/licensing outcome publicly or in any
  materials — not disclosable.**
- Founded **Vision ACTion** — a research translation forum uniting researchers,
  clinicians, and patients to accelerate therapeutic development
- Featured in national media: Startup Daily, Ophthalmology Times, CSIRO, Sky News
  Australia
- STEM outreach speaker, Canberra Science Week (8,000+ attendees) and national high
  school programs
- Multiple CV drafts exist in Drive with slightly varying numbers (publication counts
  ranging ~20–25, patent counts 2–3 depending on context) — treat the figures already
  in this file as the ones to use; if precision matters for a specific claim, go back
  to the source CVs in Drive rather than re-deriving.
- One CV draft's summary mentions a personal long-term interest in transitioning
  toward quantitative trading. Confirmed as **outdated / not reflective of current
  plans** — Tractum is the real, current focus. Do not let this influence the site,
  bio, or any framing of commitment to the company.

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

1. Prototype HTML files (`index.html`, `tractus.html`, `tractus-ophthalmology.html`)
   were searched for in Google Drive and NOT found — only brand assets (logo,
   email signature) turned up in the Drive "website" folder. They may only exist in
   the other claude.ai project's sandbox output and may need to be rebuilt from
   scratch here rather than imported, unless Adrian can export them from that project.
2. Site structure now follows the ophthalmic-focus pivot: ONE ophthalmic firm, two
   buyer tiers (Tier 1 small-biotech advisory / Tier 2 pharma capability build) — NOT
   the old "CRO automation vs ophthalmology" two-practice split. The green/blue
   two-practice color system from the prototype no longer maps cleanly; likely move to
   a single ophthalmic-led palette (logo blue ~#2E7BE0, sample the file). Reconcile
   before building.
3. Fill in a named specific for Adrian's "AI/data systems" work beyond the retinal
   bioinformatics pipelines already documented (text embeddings/NLP/vector-similarity
   work at Accenture is documented now — may be sufficient).
4. Decide on core team vs. advisory board split and recruit/confirm the clinician gap.
5. Tech stack / CMS / hosting not yet chosen for a production build.
6. Real client names (Merck, GenN Tech per CV) must stay off the public site pending
   their explicit sign-off — use generic descriptors instead.
