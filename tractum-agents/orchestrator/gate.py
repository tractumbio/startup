"""The human gate. Nothing leaves drafts without a person saying so."""
from __future__ import annotations

import datetime as _dt
import os
import subprocess
import sys
from pathlib import Path

from .config import ROOT


def outputs_dir() -> Path:
    return ROOT / os.environ.get("TRACTUM_OUTPUT_DIR", "outputs")


def rel(path: Path) -> str:
    """Display path relative to the repo root, tolerating paths outside it."""
    try:
        return str(Path(path).resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def _stamp() -> str:
    return _dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def write_draft(agent: str, stage: str, content: str, meta: dict) -> Path:
    d = outputs_dir() / "drafts"
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{_stamp()}_{stage}_{agent}.md"
    header = "\n".join(f"{k}: {v}" for k, v in meta.items())
    path.write_text(f"---\n{header}\n---\n\n{content}\n")
    return path


def approve(draft: Path, note: str = "") -> Path:
    d = outputs_dir() / "approved"
    d.mkdir(parents=True, exist_ok=True)
    dest = d / draft.name
    body = draft.read_text()
    if note:
        body += f"\n\n---\n**Approver note:** {note}\n"
    dest.write_text(body)
    return dest


def ask(prompt: str, draft: Path) -> tuple[str, str]:
    """Block for a human decision on a draft.

    Returns (decision, note) where decision is approve | revise | reject | stop.
    Refuses to auto-approve when there is no TTY — an unattended run stops instead.
    """
    print(f"\n{'=' * 70}", file=sys.stderr)
    print(f"HUMAN GATE — draft written to {rel(draft)}", file=sys.stderr)
    if prompt:
        print(f"\n{prompt.strip()}", file=sys.stderr)
    print(f"{'=' * 70}", file=sys.stderr)

    if not sys.stdin.isatty():
        print(
            "No TTY: cannot ask for approval, so stopping. The draft is on disk; "
            "review it and re-run the stage interactively.",
            file=sys.stderr,
        )
        return "stop", "no tty"

    while True:
        choice = input("[a]pprove  [r]evise  [x] reject  [e]dit  [q]uit > ").strip().lower()
        if choice in ("a", "approve"):
            return "approve", input("note (optional) > ").strip()
        if choice in ("r", "revise"):
            return "revise", input("what should change? > ").strip()
        if choice in ("x", "reject"):
            return "reject", input("why? > ").strip()
        if choice in ("e", "edit"):
            editor = os.environ.get("EDITOR", "nano")
            subprocess.call([editor, str(draft)])
            continue
        if choice in ("q", "quit"):
            return "stop", ""
        print("  pick one of a / r / x / e / q", file=sys.stderr)
