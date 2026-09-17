"""Step 4: assemble the final company table and report reference coverage.

Joins the Step 2 classification with the Step 3 trial matches, derives a
development_stage per company, and writes companies.parquet plus a CSV copy.
"""

from __future__ import annotations

import pandas as pd

from common import (
    CLASSIFIED_CSV,
    COMPANIES_PARQUET,
    COMPANY_TRIALS_PARQUET,
    FINAL_CSV,
    REFERENCE_LIST,
    TRIALS_PARQUET,
    ensure_dirs,
    require_input,
)

# Highest phase wins when a company has several trials.
PHASE_RANK = {
    "EARLY_PHASE1": 1,
    "PHASE1": 2,
    "PHASE2": 3,
    "PHASE3": 4,
    "PHASE4": 5,
}
PHASE_LABELS = {
    1: "Phase 1 (early)",
    2: "Phase 1",
    3: "Phase 2",
    4: "Phase 3",
    5: "Phase 4 / marketed",
}

OUTPUT_COLUMNS = [
    "asx_code", "company_name", "gics_industry_group", "yahoo_industry",
    "yahoo_sector", "market_cap", "development_stage", "trial_count",
    "therapeutic_focus", "has_lead_program", "lead_program_terms",
    "lead_program_snippet", "business_summary",
]


def highest_phase(phases: pd.Series) -> str:
    ranks = [
        PHASE_RANK[phase]
        for entry in phases.dropna()
        for phase in str(entry).split(", ")
        if phase in PHASE_RANK
    ]
    if not ranks:
        return "Clinical (phase unspecified)"
    return PHASE_LABELS[max(ranks)]


def stage_per_company(trials: pd.DataFrame, links: pd.DataFrame) -> pd.DataFrame:
    if links.empty or trials.empty:
        return pd.DataFrame(columns=["asx_code", "development_stage", "trial_count"])

    joined = links.merge(trials, on="nct_id", how="left")
    return (
        joined.groupby("asx_code")
        .agg(development_stage=("phase", highest_phase), trial_count=("nct_id", "nunique"))
        .reset_index()
    )


def report_reference_coverage(companies: pd.DataFrame) -> None:
    if not REFERENCE_LIST.exists():
        return

    reference = pd.read_csv(REFERENCE_LIST)
    found = set(companies["asx_code"])
    reference["recovered"] = reference["asx_code"].isin(found)

    print("\nReference-list coverage")
    for tier in ("large", "mid", "early"):
        tier_rows = reference[reference["stage_tier"] == tier]
        if tier_rows.empty:
            continue
        hits = int(tier_rows["recovered"].sum())
        print(f"  {tier:<6} {hits}/{len(tier_rows)}")

    missing = reference[~reference["recovered"]]
    if not missing.empty:
        print("\n  Missing from the pipeline output:")
        for row in missing.itertuples(index=False):
            print(f"    {row.asx_code:<5} {row.name}")
        print(
            "\n  Check each against data/processed/classified_companies.csv — the "
            "exclusion_reason column says whether it failed the industry filter, "
            "the keyword checks, or never appeared in the ASX directory at all."
        )


def main() -> None:
    ensure_dirs()
    require_input(CLASSIFIED_CSV, "classify_biotech.py (step 2)")

    classified = pd.read_csv(CLASSIFIED_CSV)
    companies = classified[classified["included"]].copy()

    trials = pd.read_parquet(TRIALS_PARQUET) if TRIALS_PARQUET.exists() else pd.DataFrame()
    links = (
        pd.read_parquet(COMPANY_TRIALS_PARQUET)
        if COMPANY_TRIALS_PARQUET.exists()
        else pd.DataFrame()
    )

    stages = stage_per_company(trials, links)
    companies = companies.merge(stages, on="asx_code", how="left")
    companies["development_stage"] = companies["development_stage"].fillna("Preclinical")
    companies["trial_count"] = companies["trial_count"].fillna(0).astype(int)

    columns = [c for c in OUTPUT_COLUMNS if c in companies.columns]
    companies = companies[columns].sort_values("asx_code").reset_index(drop=True)

    companies.to_parquet(COMPANIES_PARQUET, index=False)
    companies.to_csv(FINAL_CSV, index=False)

    print(f"{len(companies)} companies in the final list")
    print(companies["development_stage"].value_counts().to_string())
    report_reference_coverage(companies)
    print(f"\nWrote {COMPANIES_PARQUET} and {FINAL_CSV}")


if __name__ == "__main__":
    main()
