"""Step 3: tag included companies with their ClinicalTrials.gov trials.

Enrichment only — a company with zero matching trials stays in the final list
(that is the expected shape of a preclinical biotech). Output feeds the
development_stage column built in Step 4.
"""

from __future__ import annotations

import argparse
import time

import pandas as pd

from common import (
    CLASSIFIED_CSV,
    COMPANY_TRIALS_PARQUET,
    TRIALS_PARQUET,
    ensure_dirs,
    get_with_retry,
    make_session,
    name_similarity,
    normalize_company_name,
    require_input,
)

API_URL = "https://clinicaltrials.gov/api/v2/studies"
MATCH_THRESHOLD = 0.6
PAGE_SIZE = 50


def fetch_sponsor_studies(session, company_name: str) -> list[dict]:
    """All studies the registry associates with this sponsor name, paginated."""
    studies: list[dict] = []
    params = {
        "query.spons": normalize_company_name(company_name) or company_name,
        "pageSize": PAGE_SIZE,
    }
    while True:
        response = get_with_retry(session, API_URL, params=params)
        if response is None:
            break
        payload = response.json()
        studies.extend(payload.get("studies", []))
        token = payload.get("nextPageToken")
        if not token:
            break
        params["pageToken"] = token
    return studies


def parse_study(study: dict) -> dict:
    protocol = study.get("protocolSection", {})
    identification = protocol.get("identificationModule", {})
    status = protocol.get("statusModule", {})
    design = protocol.get("designModule", {})
    conditions = protocol.get("conditionsModule", {})
    arms = protocol.get("armsInterventionsModule", {})
    sponsor = protocol.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {})

    interventions = [
        i.get("name", "") for i in arms.get("interventions", []) if i.get("name")
    ]
    return {
        "nct_id": identification.get("nctId", ""),
        "brief_title": identification.get("briefTitle", ""),
        "phase": ", ".join(design.get("phases", []) or []),
        "status": status.get("overallStatus", ""),
        "start_date": status.get("startDateStruct", {}).get("date", ""),
        "condition": ", ".join(conditions.get("conditions", []) or []),
        "intervention": ", ".join(interventions),
        "sponsor_name_raw": sponsor.get("name", ""),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, help="Only process the first N companies.")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between API calls.")
    args = parser.parse_args()

    ensure_dirs()
    require_input(CLASSIFIED_CSV, "classify_biotech.py (step 2)")
    companies = pd.read_csv(CLASSIFIED_CSV)
    companies = companies[companies["included"]].reset_index(drop=True)
    if args.limit:
        companies = companies.head(args.limit)

    session = make_session()
    trials: dict[str, dict] = {}
    links: list[dict] = []

    for position, row in enumerate(companies.itertuples(index=False), start=1):
        print(f"[{position}/{len(companies)}] {row.asx_code} — {row.company_name}")
        for study in fetch_sponsor_studies(session, row.company_name):
            parsed = parse_study(study)
            if not parsed["nct_id"]:
                continue
            confidence = name_similarity(row.company_name, parsed["sponsor_name_raw"])
            if confidence < MATCH_THRESHOLD:
                continue
            trials[parsed["nct_id"]] = parsed
            links.append(
                {
                    "asx_code": row.asx_code,
                    "nct_id": parsed["nct_id"],
                    "match_confidence": round(confidence, 3),
                }
            )
        time.sleep(args.delay)

    trials_frame = pd.DataFrame(list(trials.values()))
    links_frame = pd.DataFrame(links)
    trials_frame.to_parquet(TRIALS_PARQUET, index=False)
    links_frame.to_parquet(COMPANY_TRIALS_PARQUET, index=False)

    matched = links_frame["asx_code"].nunique() if not links_frame.empty else 0
    print(f"\n{len(trials_frame)} trials matched across {matched} of {len(companies)} companies")
    print(f"Wrote {TRIALS_PARQUET} and {COMPANY_TRIALS_PARQUET}")


if __name__ == "__main__":
    main()
