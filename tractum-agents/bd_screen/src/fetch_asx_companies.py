"""Step 1: pull the ASX company directory and keep the healthcare candidates.

Writes an untouched copy of the feed to data/raw/asx_directory/<date>.csv as an
audit trail, then a filtered candidate list to data/processed/.
"""

from __future__ import annotations

import argparse
import io
import sys
from datetime import date

import pandas as pd

from common import (
    ASX_DIRECTORY_DIR,
    CANDIDATES_CSV,
    ensure_dirs,
    get_with_retry,
    make_session,
)

# Undocumented feed backing the ASX's own company-directory page. The token is a
# fixed value embedded in that page, not a personal credential.
DIRECTORY_URL = (
    "https://asx.api.markitdigital.com/asx-research/1.0/companies/directory/file"
    "?access_token=83ff96335c2d45a094df02a206a39ff4"
)

TARGET_INDUSTRY_GROUP = "pharmaceuticals, biotechnology & life sciences"

COLUMN_ALIASES = {
    "asx code": "asx_code",
    "company name": "company_name",
    "gics industry group": "gics_industry_group",
    "gic industry group": "gics_industry_group",
    "gics industry group name": "gics_industry_group",
    "listing date": "listing_date",
    "market cap": "market_cap",
}


def download_directory(local_copy: bool | str = False) -> pd.DataFrame:
    if local_copy:
        print(f"Reading directory from local file {local_copy}")
        return pd.read_csv(local_copy)

    session = make_session()
    print("Downloading ASX company directory...")
    response = get_with_retry(session, DIRECTORY_URL)
    if response is None:
        sys.exit(
            "Could not download the ASX directory feed. It is an undocumented "
            "endpoint and may have changed. Fall back to the manual CSV export "
            "from asx.com.au and re-run with --from-file."
        )

    raw_path = ASX_DIRECTORY_DIR / f"{date.today().isoformat()}.csv"
    raw_path.write_bytes(response.content)
    print(f"Saved raw feed to {raw_path}")
    return pd.read_csv(io.BytesIO(response.content))


def normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    renamed = {}
    for column in frame.columns:
        key = column.strip().lower()
        renamed[column] = COLUMN_ALIASES.get(key, key.replace(" ", "_"))
    frame = frame.rename(columns=renamed)

    missing = {"asx_code", "company_name", "gics_industry_group"} - set(frame.columns)
    if missing:
        sys.exit(
            f"Directory feed is missing expected columns {sorted(missing)}. "
            f"Columns present: {sorted(frame.columns)}. The feed's schema likely "
            "changed — update COLUMN_ALIASES."
        )
    return frame


def filter_candidates(frame: pd.DataFrame) -> pd.DataFrame:
    keep = [
        c
        for c in ("asx_code", "company_name", "gics_industry_group", "listing_date", "market_cap")
        if c in frame.columns
    ]
    frame = frame[keep].copy()
    frame["asx_code"] = frame["asx_code"].astype(str).str.strip().str.upper()

    group = frame["gics_industry_group"].astype(str).str.strip().str.lower()
    candidates = frame[group == TARGET_INDUSTRY_GROUP]
    return candidates.sort_values("asx_code").reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from-file",
        help="Parse this local CSV instead of downloading (manual ASX export fallback).",
    )
    args = parser.parse_args()

    ensure_dirs()
    directory = normalize_columns(download_directory(args.from_file))
    candidates = filter_candidates(directory)

    if candidates.empty:
        groups = sorted(directory["gics_industry_group"].dropna().unique())
        sys.exit(
            "No companies matched the target GICS industry group. Groups seen in "
            f"the feed: {groups}"
        )

    candidates.to_csv(CANDIDATES_CSV, index=False)
    print(f"{len(directory)} listed companies -> {len(candidates)} healthcare candidates")
    print(f"Wrote {CANDIDATES_CSV}")


if __name__ == "__main__":
    main()
