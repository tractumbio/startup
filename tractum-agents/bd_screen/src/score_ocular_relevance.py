"""Step 5: score each therapeutic developer for plausible ophthalmic relevance.

This is the step that makes the pipeline Tractum's rather than an investor's. The
upstream steps answer "who is developing a drug?"; this one answers "whose lead
asset might already be relevant in the eye, without anyone having looked?"

It is a SCREEN, not an assessment. A high score means a scientist should spend an
hour on it — nothing more. The score is computed in code from visible weights, and
every point is traceable to the phrase that earned it; the real judgement happens
in `ophtha_science`, which takes the shortlist and can throw any of it out.

Signals, in descending weight:
  direct      the company already says "ophthalmic", "retina", "macular" — not a
              prospect, a competitor or a partner. Scored, but flagged separately.
  mechanism   the target/pathway has published ocular relevance (VEGF, complement,
              inflammasome, oxidative stress, neuroprotection, gene therapy ...)
  modality    the format travels to the eye well (intravitreal-compatible: AAV,
              antibody fragment, siRNA, peptide) or badly (oral systemic, IV infusion)
  stage       preclinical and Phase 1 are the window where a second indication is
              still cheap to add; Phase 3 is too late to matter
"""

from __future__ import annotations

import argparse
import datetime as dt
import re

import pandas as pd

from common import (
    FINAL_CSV,
    OCULAR_SCORED_CSV,
    SHORTLIST_MD,
    WORKSPACE_SHARED,
    ensure_dirs,
    require_input,
)

# (weight, label, terms). Weights are visible on purpose — tune them here, and the
# scorecard in the output will show what changed.
SIGNALS: list[tuple[int, str, tuple[str, ...]]] = [
    (6, "already-ocular", (
        "ophthalmic", "ophthalmology", "retina", "retinal", "macular", "uveitis",
        "glaucoma", "dry eye", "intravitreal", "corneal", "ocular",
    )),
    (4, "mechanism-ocular-precedent", (
        "vegf", "complement", "c3 ", "c5 ", "inflammasome", "nlrp3",
        "oxidative stress", "neuroprotect", "neuroinflammation", "microglia",
        "angiogenesis", "anti-angiogenic", "photoreceptor", "rpe",
        "blood-retinal", "tnf", "il-6", "integrin", "tie2", "angiopoietin",
    )),
    (3, "modality-travels-to-eye", (
        "gene therapy", "aav", "sirna", "rnai", "antisense", "oligonucleotide",
        "antibody fragment", "fab", "scfv", "peptide", "cell therapy",
        "extracellular vesicle", "exosome", "small molecule",
    )),
    (2, "degenerative-or-inflammatory", (
        "degeneration", "degenerative", "fibrosis", "fibrotic", "inflammation",
        "inflammatory", "autoimmune", "ischemia", "ischaemia", "hypoxia",
    )),
]

# Formats and settings that argue against an ocular second indication.
NEGATIVE_SIGNALS: list[tuple[int, str, tuple[str, ...]]] = [
    (-3, "systemic-only-delivery", (
        "intravenous infusion", "oral tablet", "oral capsule", "inhaled",
        "subcutaneous injection", "transdermal",
    )),
    (-2, "indication-far-from-eye", (
        "dermatolog", "psoriasis", "gastrointestinal", "irritable bowel",
        "urolog", "prostate", "fertility", "contracept", "dental", "wound healing",
    )),
]

STAGE_WEIGHTS = {
    "preclinical": 3,      # the window: a second indication is still cheap
    "phase 1": 3,
    "phase i": 3,
    "phase 2": 2,
    "phase ii": 2,
    "phase 3": 0,          # too late for this conversation to change anything
    "phase iii": 0,
}


def _hits(text: str, terms: tuple[str, ...]) -> list[str]:
    return sorted({t.strip() for t in terms if t in text})


def score_row(row: pd.Series) -> dict:
    text = " ".join(
        str(row.get(col, "") or "")
        for col in ("name", "business_summary", "lead_program_note",
                    "conditions", "interventions", "yahoo_industry")
    ).lower()
    text = re.sub(r"\s+", " ", text)

    score = 0
    reasons: list[str] = []
    labels: list[str] = []

    for weight, label, terms in SIGNALS + NEGATIVE_SIGNALS:
        hits = _hits(text, terms)
        if hits:
            score += weight
            labels.append(label)
            reasons.append(f"{label} ({weight:+d}): {', '.join(hits[:4])}")

    stage = str(row.get("development_stage", "") or "").lower()
    for key, weight in STAGE_WEIGHTS.items():
        if key in stage:
            score += weight
            reasons.append(f"stage {stage} ({weight:+d})")
            break

    return {
        "ocular_score": score,
        "signals": "; ".join(labels),
        "why": " | ".join(reasons),
        # An already-ocular company is not a Tier 1 prospect — it is a competitor,
        # a partner, or a comparable. Keep it, but never pitch it.
        "already_ocular": "already-ocular" in labels,
    }


def build_shortlist(df: pd.DataFrame, top: int) -> str:
    prospects = df[~df["already_ocular"]].head(top)
    incumbents = df[df["already_ocular"]].head(10)
    today = dt.date.today().isoformat()

    lines = [
        "# BD screen — ophthalmic prospects",
        "",
        f"Generated {today} by `bd_screen/src/score_ocular_relevance.py`.",
        "",
        "**This is a screen, not an assessment.** Scores are computed in code from the",
        "weights in that file; every point is traceable to the phrase that earned it.",
        "A high score means *a scientist should spend an hour here* — nothing more.",
        "Nothing on this list has been judged by anyone yet.",
        "",
        "## Prospects — lead asset may have unexamined ocular relevance",
        "",
        "| # | Code | Company | Score | Stage | Why it surfaced |",
        "|---|---|---|---|---|---|",
    ]
    for i, (_, r) in enumerate(prospects.iterrows(), 1):
        why = str(r["why"])[:160].replace("|", "/")
        lines.append(
            f"| {i} | {r.get('asx_code','')} | {str(r.get('name',''))[:40]} | "
            f"{r['ocular_score']} | {r.get('development_stage','?')} | {why} |"
        )

    lines += [
        "",
        "## Already ophthalmic — not prospects",
        "",
        "These name the eye themselves. They are competitors, potential partners or",
        "valuation comparables — never Tier 1 pitch targets.",
        "",
    ]
    for _, r in incumbents.iterrows():
        lines.append(f"- **{r.get('asx_code','')}** {str(r.get('name',''))[:50]} — score {r['ocular_score']}")

    lines += [
        "",
        "## Next step",
        "",
        "Hand the top prospects to `ophtha_science` for a real mechanism read:",
        "",
        "```bash",
        "python -m orchestrator.run chat ophtha_science --session bd",
        "# then:  /load shared:bd-shortlist.md",
        "```",
        "",
        "Expect most of this list to be wrong. The screen is cheap; the judgement is not.",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top", type=int, default=25, help="prospects in the shortlist")
    parser.add_argument("--min-score", type=int, default=4,
                        help="drop anything below this before writing the shortlist")
    args = parser.parse_args()

    ensure_dirs()
    require_input(FINAL_CSV, "build_dataset.py")

    df = pd.read_csv(FINAL_CSV)
    scored = pd.concat([df, df.apply(score_row, axis=1, result_type="expand")], axis=1)
    scored = scored.sort_values("ocular_score", ascending=False)
    scored.to_csv(OCULAR_SCORED_CSV, index=False)
    print(f"scored {len(scored)} companies -> {OCULAR_SCORED_CSV}")

    kept = scored[scored["ocular_score"] >= args.min_score]
    WORKSPACE_SHARED.mkdir(parents=True, exist_ok=True)
    SHORTLIST_MD.write_text(build_shortlist(kept, args.top))
    print(f"shortlist ({len(kept)} above threshold) -> {SHORTLIST_MD}")
    print("\nEvery agent can now read it as `shared:bd-shortlist.md`.")


if __name__ == "__main__":
    main()
