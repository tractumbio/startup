"""Step 5: download every ASX announcement PDF for the final company list.

Prospectuses, financials, annual reports and all other disclosures come through
the same per-company announcements feed. Downloads are incremental — a file
already on disk is never re-fetched.

This is the heaviest step in the pipeline: hundreds of companies with up to
hundreds of PDFs each. Start with --limit or --tickers on a small pilot, keep
the default delay, and read ASX's terms of use before running it in full.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import pandas as pd

from classify_announcement import classify_announcement
from common import (
    ANNOUNCEMENTS_DIR,
    ANNOUNCEMENTS_PARQUET,
    COMPANIES_PARQUET,
    DOCUMENT_INDEX_PARQUET,
    REPO_ROOT,
    ensure_dirs,
    get_with_retry,
    make_session,
    require_input,
    slugify,
)

ANNOUNCEMENTS_URL = "https://www.asx.com.au/asx/1/company/{ticker}/announcements"


def fetch_announcements(session, ticker: str, count: int, market_sensitive: bool) -> list[dict]:
    params = {"count": count, "market_sensitive": str(market_sensitive).lower()}
    response = get_with_retry(session, ANNOUNCEMENTS_URL.format(ticker=ticker), params=params)
    if response is None:
        return []
    try:
        return response.json().get("data", []) or []
    except ValueError:
        print(f"  ! {ticker}: announcements response was not JSON")
        return []


def parse_announcement(ticker: str, item: dict) -> dict:
    document_date = (item.get("document_date") or item.get("release_date") or "")[:10]
    title = item.get("header") or item.get("title") or "Untitled"
    return {
        "asx_code": ticker,
        "title": title,
        "doc_type": classify_announcement(title),
        "url": item.get("url", ""),
        "release_date": item.get("release_date", ""),
        "document_date": document_date,
        "num_pages": item.get("number_of_pages") or item.get("num_pages"),
        # Passed through verbatim — the feed's unit/format is unconfirmed.
        "size": item.get("size"),
    }


def download_pdf(session, record: dict, delay: float) -> Path | None:
    if not record["url"]:
        return None

    target_dir = ANNOUNCEMENTS_DIR / record["asx_code"]
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{record['document_date'] or 'undated'}_{slugify(record['title'])}.pdf"
    target = target_dir / filename

    if target.exists():
        return target

    response = get_with_retry(session, record["url"], stream=True)
    if response is None:
        return None
    target.write_bytes(response.content)
    time.sleep(delay)
    return target


def write_index(records: list[dict]) -> None:
    frame = pd.DataFrame(records)
    frame.to_parquet(ANNOUNCEMENTS_PARQUET, index=False)

    index = frame.assign(source="asx_announcements", doc_format="pdf").rename(
        columns={"document_date": "published_date", "title": "doc_title"}
    )[
        [
            "asx_code", "source", "doc_type", "doc_title", "doc_format",
            "published_date", "url", "local_path",
        ]
    ]
    index.to_parquet(DOCUMENT_INDEX_PARQUET, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tickers", nargs="+", help="Only these ASX codes (pilot run).")
    parser.add_argument("--limit", type=int, help="Only the first N companies.")
    parser.add_argument("--count", type=int, default=500, help="Announcements requested per company.")
    parser.add_argument(
        "--market-sensitive-only",
        action="store_true",
        help="Request only price-sensitive announcements instead of the full history.",
    )
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between downloads.")
    args = parser.parse_args()

    ensure_dirs()
    require_input(COMPANIES_PARQUET, "build_dataset.py (step 4)")
    companies = pd.read_parquet(COMPANIES_PARQUET)
    if args.tickers:
        wanted = {t.upper() for t in args.tickers}
        companies = companies[companies["asx_code"].isin(wanted)]
    if args.limit:
        companies = companies.head(args.limit)

    session = make_session()
    records: list[dict] = []

    for position, row in enumerate(companies.itertuples(index=False), start=1):
        ticker = row.asx_code
        items = fetch_announcements(
            session, ticker, args.count, not args.market_sensitive_only
        )
        print(f"[{position}/{len(companies)}] {ticker}: {len(items)} announcements")

        for item in items:
            record = parse_announcement(ticker, item)
            path = download_pdf(session, record, args.delay)
            record["local_path"] = str(path.relative_to(REPO_ROOT)) if path else ""
            records.append(record)
        time.sleep(args.delay)

    if not records:
        print("No announcements retrieved — check the feed URL and parameters.")
        return

    write_index(records)
    downloaded = sum(1 for r in records if r["local_path"])
    print(f"\n{len(records)} announcements indexed, {downloaded} PDFs on disk")
    print(pd.DataFrame(records)["doc_type"].value_counts().to_string())
    print(f"\nWrote {ANNOUNCEMENTS_PARQUET} and {DOCUMENT_INDEX_PARQUET}")


if __name__ == "__main__":
    main()
