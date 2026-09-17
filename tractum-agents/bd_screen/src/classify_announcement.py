"""Infer an announcement's document type from its title.

The ASX feed carries no document-type field, so this is a keyword guess. The raw
title is always kept alongside the guess so a misclassification is recoverable.
"""

from __future__ import annotations

# Ordered: the first matching rule wins, so put the specific ones first.
RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Prospectus", ("prospectus", "offer document", "product disclosure statement",
                    "replacement prospectus", "offer information statement")),
    ("Capital Raising", ("placement", "entitlement offer", "share purchase plan",
                         "capital raising", "rights issue", "appendix 3b",
                         "appendix 2a", "cleansing notice")),
    ("Annual Report", ("annual report", "annual financial report", "appendix 4g",
                       "corporate governance statement")),
    ("Financials", ("appendix 4c", "appendix 4d", "appendix 4e", "quarterly cash flow",
                    "quarterly activities", "half year", "half-year", "full year",
                    "financial report", "financial statements", "preliminary final")),
    ("AGM", ("notice of meeting", "annual general meeting", "agm", "chairman's address",
             "results of meeting", "proxy")),
    ("Clinical Update", ("clinical", "phase 1", "phase 2", "phase 3", "phase i",
                         "phase ii", "phase iii", "trial", "patient", "dosing",
                         "topline", "efficacy", "fda", "tga", "ema", "orphan drug",
                         "ind ", "regulatory approval", "patent")),
    ("Presentation", ("investor presentation", "presentation", "webinar", "roadshow")),
    ("Governance", ("appendix 3y", "appendix 3x", "appendix 3z", "change of director",
                    "director's interest", "substantial holder", "becoming a substantial",
                    "ceasing to be a substantial", "change in substantial")),
)


def classify_announcement(title: str) -> str:
    lowered = (title or "").lower()
    for doc_type, keywords in RULES:
        if any(keyword in lowered for keyword in keywords):
            return doc_type
    return "Other"
