"""Shared paths, HTTP session and name-matching helpers for the pipeline."""

from __future__ import annotations

import difflib
import re
import time
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REFERENCE_DIR = DATA_DIR / "reference"

ASX_DIRECTORY_DIR = RAW_DIR / "asx_directory"
ANNOUNCEMENTS_DIR = RAW_DIR / "announcements"

REFERENCE_LIST = REFERENCE_DIR / "asx_biotech_reference_list.csv"
CANDIDATES_CSV = PROCESSED_DIR / "asx_biotech_candidates.csv"
CLASSIFIED_CSV = PROCESSED_DIR / "classified_companies.csv"
COMPANIES_PARQUET = PROCESSED_DIR / "companies.parquet"
TRIALS_PARQUET = PROCESSED_DIR / "trials.parquet"
COMPANY_TRIALS_PARQUET = PROCESSED_DIR / "company_trials.parquet"
ANNOUNCEMENTS_PARQUET = PROCESSED_DIR / "announcements.parquet"
DOCUMENT_INDEX_PARQUET = PROCESSED_DIR / "document_index.parquet"
FINAL_CSV = PROCESSED_DIR / "biotech_lead_drug_companies.csv"
OCULAR_SCORED_CSV = PROCESSED_DIR / "ocular_relevance_scored.csv"

# Where the shortlist is handed to the agents. Writing into the shared store means
# every agent can read it, not just the one that produced it.
WORKSPACE_SHARED = REPO_ROOT.parent / "workspace" / "shared"
SHORTLIST_MD = WORKSPACE_SHARED / "bd-shortlist.md"

USER_AGENT = (
    "Tractum Bio Consulting BD screen "
    "(+https://github.com/tractumbio/startup)"
)

# Corporate suffixes stripped before fuzzy-matching a company name against an
# external registry's sponsor name.
_SUFFIXES = (
    "limited", "ltd", "pty", "plc", "inc", "incorporated", "corp",
    "corporation", "holdings", "group", "company", "co", "nl",
)


def ensure_dirs() -> None:
    for path in (RAW_DIR, PROCESSED_DIR, REFERENCE_DIR, ASX_DIRECTORY_DIR, ANNOUNCEMENTS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def require_input(path: Path, produced_by: str) -> None:
    """Exit with a pointer to the step that produces a missing pipeline input."""
    if not path.exists():
        raise SystemExit(f"{path} not found — run {produced_by} first.")


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json, */*"})
    return session


def get_with_retry(
    session: requests.Session,
    url: str,
    *,
    params: dict | None = None,
    attempts: int = 4,
    timeout: int = 30,
    stream: bool = False,
) -> requests.Response | None:
    """GET with exponential backoff. Returns None once retries are exhausted."""
    delay = 2.0
    for attempt in range(1, attempts + 1):
        try:
            response = session.get(url, params=params, timeout=timeout, stream=stream)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response
        except requests.RequestException as exc:
            if attempt == attempts:
                print(f"  ! giving up on {url}: {exc}")
                return None
            time.sleep(delay)
            delay *= 2
    return None


def normalize_company_name(name: str) -> str:
    """Lowercase, strip punctuation and corporate suffixes for fuzzy matching."""
    cleaned = re.sub(r"[^a-z0-9 ]+", " ", (name or "").lower())
    words = [w for w in cleaned.split() if w not in _SUFFIXES]
    return " ".join(words)


def name_similarity(left: str, right: str) -> float:
    a, b = normalize_company_name(left), normalize_company_name(right)
    if not a or not b:
        return 0.0
    # A registry sponsor name often embeds the company name verbatim
    # ("Immutep Australia Pty Ltd" vs "Immutep"), which ratio() scores poorly.
    if a in b or b in a:
        return 1.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def slugify(text: str, max_length: int = 80) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return slug[:max_length] or "untitled"
