"""Step 2: narrow the healthcare candidates to therapeutic developers.

Enriches each candidate with Yahoo Finance industry/business-summary data, then
applies two keyword checks: is the company doing therapeutic development, and
does it name a lead program at any stage (preclinical counts).
"""

from __future__ import annotations

import argparse
import re
import time

import pandas as pd
import yfinance as yf

from common import CANDIDATES_CSV, CLASSIFIED_CSV, ensure_dirs, require_input

KEEP_INDUSTRY_KEYWORDS = ("biotechnology", "drug manufacturers", "pharmaceutical")

THERAPEUTIC_TERMS = (
    "therapeutic", "therapy", "therapies", "treatment of", "treatment for",
    "drug candidate", "drug development", "product candidate", "medicine",
    "biologic", "vaccine", "gene therapy", "cell therapy", "antibody",
    "small molecule", "peptide", "oncology", "immunotherapy", "rna therapeutic",
)

LEAD_PROGRAM_TERMS = (
    "lead candidate", "lead product", "lead compound", "lead molecule",
    "lead asset", "lead program", "lead drug", "pipeline", "preclinical",
    "pre-clinical", "clinical-stage", "clinical stage", "phase i", "phase ii",
    "phase iii", "phase 1", "phase 2", "phase 3", "investigational",
    "candidate for the treatment", "in development for",
)

# Terms that mean the company is not primarily a drug developer, even if Yahoo
# files it under biotechnology.
EXCLUSION_TERMS = (
    "contract research organization", "diagnostic tests", "diagnostic imaging services",
    "medical devices", "veterinary", "agricultural", "crop", "laboratory services",
    "distributor of", "consumer health", "nutraceutical", "cosmetic",
)


def matched_terms(text: str, terms: tuple[str, ...]) -> list[str]:
    return [term for term in terms if term in text]


def extract_snippet(text: str, terms: list[str], width: int = 160) -> str:
    """Return the window around the first matched term, snapped to word boundaries."""
    if not terms:
        return ""
    position = text.find(terms[0])
    start = text.rfind(" ", 0, max(0, position - width // 2)) + 1
    end = text.find(" ", position + width)
    return re.sub(r"\s+", " ", text[start : end if end != -1 else len(text)]).strip()


def fetch_profile(asx_code: str) -> dict:
    ticker = yf.Ticker(f"{asx_code}.AX")
    try:
        info = ticker.info or {}
    except Exception as exc:  # yfinance raises assorted network/parse errors
        print(f"  ! {asx_code}: {type(exc).__name__}: {exc}")
        return {}
    return {
        "yahoo_industry": info.get("industry") or "",
        "yahoo_sector": info.get("sector") or "",
        "business_summary": info.get("longBusinessSummary") or "",
        "market_cap_yahoo": info.get("marketCap"),
    }


def classify(row: pd.Series) -> dict:
    summary = (row.get("business_summary") or "").lower()
    industry = (row.get("yahoo_industry") or "").lower()

    industry_ok = any(k in industry for k in KEEP_INDUSTRY_KEYWORDS)
    therapeutic_hits = matched_terms(summary, THERAPEUTIC_TERMS)
    lead_hits = matched_terms(summary, LEAD_PROGRAM_TERMS)
    exclusion_hits = matched_terms(summary, EXCLUSION_TERMS)

    reasons = []
    if not industry_ok:
        reasons.append(f"industry '{row.get('yahoo_industry') or 'unknown'}' not a drug developer")
    if not therapeutic_hits:
        reasons.append("no therapeutic-development language in summary")
    if not lead_hits:
        reasons.append("no lead-program language in summary")
    if exclusion_hits:
        reasons.append(f"excluded by {exclusion_hits}")

    return {
        "industry_ok": industry_ok,
        "therapeutic_focus": bool(therapeutic_hits),
        "has_lead_program": bool(lead_hits),
        "excluded": bool(exclusion_hits),
        "included": industry_ok and bool(therapeutic_hits) and bool(lead_hits) and not exclusion_hits,
        "therapeutic_terms": ", ".join(therapeutic_hits),
        "lead_program_terms": ", ".join(lead_hits),
        "lead_program_snippet": extract_snippet(summary, lead_hits),
        "exclusion_reason": "; ".join(reasons),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, help="Only process the first N candidates.")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between Yahoo calls.")
    args = parser.parse_args()

    ensure_dirs()
    require_input(CANDIDATES_CSV, "fetch_asx_companies.py (step 1)")
    candidates = pd.read_csv(CANDIDATES_CSV)
    if args.limit:
        candidates = candidates.head(args.limit)

    records = []
    for position, row in enumerate(candidates.itertuples(index=False), start=1):
        code = row.asx_code
        print(f"[{position}/{len(candidates)}] {code}")
        record = {**row._asdict(), **fetch_profile(code)}
        records.append({**record, **classify(pd.Series(record))})
        time.sleep(args.delay)

    frame = pd.DataFrame(records)
    frame.to_csv(CLASSIFIED_CSV, index=False)

    included = int(frame["included"].sum())
    print(f"\n{included} of {len(frame)} candidates classified as therapeutic developers")
    print(f"Wrote {CLASSIFIED_CSV}")


if __name__ == "__main__":
    main()
