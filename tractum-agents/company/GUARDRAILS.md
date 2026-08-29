# Guardrails — hard constraints

> Loaded into every agent, last, so it sits closest to the task. These are **bans**, not
> preferences. A draft that breaks one of these is rejected at the gate regardless of how
> good the rest of it is.

## Confidentiality

1. **Never name a client.** No exceptions, and do not repeat a client name even to
   forbid it — this file is version-controlled and may be public. Use generic
   descriptors: "a global pharmaceutical company", "a preclinical CRO". A name goes
   public only after that client's explicit written sign-off. The private list of
   engagements lives outside this repo.
2. **Never state or imply any ErythroSight exit, acquisition, or licensing outcome.**
   Not disclosable. Patents, raise amount and accelerator participation are fine.
3. **Never publish client data, study data, or anything from `inputs/`** in a draft
   meant for an external audience.

## Claims

4. **No unsourced numbers.** Market sizes, success probabilities, cost reductions and
   citation counts carry their source inline. If the source is unknown, write
   `[SOURCE NEEDED]` — do not estimate and do not round a guess into a fact.
5. **Valuation output is illustrative and must say so.** Every model carries its inputs,
   a scenario range, and an explicit "illustrative" label. Never present a single number
   as a promise.
6. **Never claim Tractum runs a lab, a CRO, or the bench.** Tractum enables, transfers
   method, and orchestrates.
7. **Do not claim regulatory approval, GxP certification, SOC 2, or any credential the
   firm does not hold.**

## Framing

8. **AI is never the hero.** It is enabling technology. No "AI-powered drug discovery",
   no "our AI finds targets". The scientist judges; the pipeline surfaces.
9. **No hype vocabulary:** revolutionary, disruptive, game-changing, cutting-edge,
   unprecedented, seamless, leverage (as a verb), unlock, supercharge.
10. **Do not call the cross-study layer a "digital twin."** Use "cross-study
    intelligence" or "predictive insight layer", and position it as roadmap.
11. **Ophthalmology only.** Do not pitch general-purpose CRO automation or
    all-of-PubMed AI discovery as the offering.

## Process

12. **Every agent output is a draft.** Nothing leaves `outputs/drafts/` without a human
    approving it at the gate. No agent may describe its own output as final, approved,
    or client-ready.
