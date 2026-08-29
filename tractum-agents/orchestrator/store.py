"""Per-agent storage with cross-agent read visibility.

Layout:

    workspace/
      shared/            written by anyone, read by everyone
      <agent>/           written by that agent only, read by everyone

The asymmetry is the point. An agent needs to see what the others have found —
`valuation` is useless without `ophtha_science`'s verdict — but an agent that can
overwrite another's store can quietly corrupt the record that a human is about to
approve. So: read wide, write narrow.

Nothing here is read into a prompt automatically. Every run gets a *manifest* of what
exists; file bodies are pulled in only when asked for, by name.
"""
from __future__ import annotations

import datetime as _dt
import shutil
from dataclasses import dataclass
from pathlib import Path

from .config import ROOT

SHARED = "shared"
_TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".tsv", ".py", ".r", ".sql"}


def workspace_root() -> Path:
    return ROOT / "workspace"


def agent_dir(agent: str) -> Path:
    d = workspace_root() / agent
    d.mkdir(parents=True, exist_ok=True)
    return d


@dataclass(frozen=True)
class Entry:
    owner: str          # agent name, or "shared"
    name: str           # path relative to that owner's dir
    size: int
    modified: str

    @property
    def ref(self) -> str:
        """The address an agent uses to ask for this file: owner:name."""
        return f"{self.owner}:{self.name}"


def _entries_for(owner: str) -> list[Entry]:
    base = workspace_root() / owner
    if not base.is_dir():
        return []
    out = []
    for p in sorted(base.rglob("*")):
        if not p.is_file() or p.name == ".gitkeep":
            continue
        # Conversation state is not a workspace document. Listing sessions/ here would
        # put JSON transcripts in every agent's manifest as if they were citable
        # material; use `chat --session` / `/sessions` to reach them instead.
        if "sessions" in p.relative_to(base).parts:
            continue
        st = p.stat()
        out.append(Entry(
            owner=owner,
            name=str(p.relative_to(base)),
            size=st.st_size,
            modified=_dt.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
        ))
    return out


def owners() -> list[str]:
    root = workspace_root()
    if not root.is_dir():
        return []
    names = sorted(p.name for p in root.iterdir() if p.is_dir())
    # shared first — it is the common ground
    return ([SHARED] if SHARED in names else []) + [n for n in names if n != SHARED]


def list_all() -> list[Entry]:
    return [e for owner in owners() for e in _entries_for(owner)]


def resolve(ref: str, requesting_agent: str) -> Path:
    """Turn 'owner:name' (or a bare 'name', meaning the caller's own store) into a path.

    Refuses to escape the workspace — a crafted ref like '../../.env' is how a store
    turns into a file-read primitive.
    """
    owner, _, name = ref.partition(":")
    if not name:
        owner, name = requesting_agent, owner
    if not name:
        raise ValueError(f"empty file reference: '{ref}'")

    base = (workspace_root() / owner).resolve()
    target = (base / name).resolve()
    if not str(target).startswith(str(base) + "/") and target != base:
        raise ValueError(f"reference escapes the workspace: '{ref}'")
    if not target.is_file():
        raise FileNotFoundError(f"no such file in the workspace: '{ref}'")
    return target


def read(ref: str, requesting_agent: str) -> str:
    """Read any agent's file. Cross-visibility is unrestricted for reads."""
    path = resolve(ref, requesting_agent)
    if path.suffix.lower() not in _TEXT_SUFFIXES:
        raise ValueError(f"'{ref}' is not a text file this system will inline")
    return path.read_text()


def write(agent: str, name: str, content: str) -> Path:
    """Write into an agent's OWN store. An agent cannot write another's."""
    if ":" in name:
        owner, _, bare = name.partition(":")
        if owner not in (agent, SHARED):
            raise PermissionError(
                f"'{agent}' may not write to '{owner}'. Write to your own store, or to "
                f"'{SHARED}:' if the other agents need it."
            )
        agent, name = owner, bare

    base = agent_dir(agent).resolve()
    target = (base / name).resolve()
    if not str(target).startswith(str(base) + "/"):
        raise ValueError(f"write escapes the store: '{name}'")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    return target


def promote(ref: str, requesting_agent: str, new_name: str | None = None) -> Path:
    """Copy a file into shared/, making it common ground for every agent."""
    src = resolve(ref, requesting_agent)
    dest = agent_dir(SHARED) / (new_name or src.name)
    shutil.copy2(src, dest)
    return dest


def manifest(for_agent: str) -> str:
    """A rendering of what every agent currently holds, for prompt context.

    Names and sizes only — never bodies. The agent asks for what it wants by ref.
    """
    entries = list_all()
    if not entries:
        return ""

    lines = [
        "## Workspace",
        "",
        "Files currently held by you and the other agents. You can READ any of them; you "
        "can WRITE only to your own store and to `shared`.",
        "",
    ]
    for owner in owners():
        owned = [e for e in entries if e.owner == owner]
        if not owned:
            continue
        label = "your store" if owner == for_agent else (
            "common ground, readable and writable by all" if owner == SHARED else "read-only to you"
        )
        lines.append(f"**{owner}** ({label})")
        for e in owned:
            lines.append(f"- `{e.ref}` — {e.size:,} bytes, modified {e.modified}")
        lines.append("")

    lines.append(
        "To use a file's contents, name its ref in your output and ask the operator to "
        "supply it with `--load <ref>`. Do not guess at the contents of a file you have "
        "not been given."
    )
    return "\n".join(lines)
