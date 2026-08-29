"""Agent construction: SOUL + baseline context + prompts."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from . import store
from .config import ROOT, load_yaml, model_for
from .ollama import generate

_PLACEHOLDER = re.compile(r"\{\{(\w+)\}\}")


def available_agents() -> list[str]:
    agents_dir = ROOT / "agents"
    return sorted(p.name for p in agents_dir.iterdir() if (p / "SOUL.md").exists())


def _read(relpath: str) -> str:
    path = ROOT / relpath
    return path.read_text() if path.exists() else ""


def build_system_prompt(agent: str) -> str:
    """Assemble baseline context in the order set by orchestration.yaml.

    Guardrails land last, closest to the task, on purpose.
    """
    order = load_yaml("config/orchestration.yaml").get("context_order") or []
    parts: list[str] = []
    for entry in order:
        rel = entry.replace("{agent}", agent)
        body = _read(rel)
        if body.strip():
            parts.append(f"<!-- === {rel} === -->\n{body.strip()}")

    system = _read(f"agents/{agent}/prompts/system.md")
    if system.strip():
        parts.append(f"<!-- === agents/{agent}/prompts/system.md === -->\n{system.strip()}")

    manifest = store.manifest(agent)
    if manifest:
        parts.append(f"<!-- === workspace manifest === -->\n{manifest}")
    return "\n\n---\n\n".join(parts)


def render_task(agent: str, values: dict[str, str]) -> str:
    """Fill {{placeholders}} in the agent's task template.

    Unfilled placeholders become an explicit NOT PROVIDED marker rather than
    vanishing — a silently empty field is how a model invents one.
    """
    template = _read(f"agents/{agent}/prompts/task.md")
    if not template.strip():
        return values.get("input", "")

    def sub(match: re.Match) -> str:
        key = match.group(1)
        val = values.get(key)
        return val if val not in (None, "") else f"[NOT PROVIDED: {key}]"

    return _PLACEHOLDER.sub(sub, template)


@dataclass
class Result:
    agent: str
    model: str
    system: str
    task: str
    output: str


def load_refs(agent: str, refs: list[str] | None) -> str:
    """Inline the bodies of explicitly requested workspace files."""
    blocks = []
    for ref in refs or []:
        body = store.read(ref, agent)
        blocks.append(f"### Workspace file `{ref}`\n\n{body}")
    return "\n\n".join(blocks)


def run_agent(
    agent: str,
    values: dict[str, str],
    stream: bool = True,
    load: list[str] | None = None,
) -> Result:
    if agent not in available_agents():
        raise ValueError(f"unknown agent '{agent}'. Known: {', '.join(available_agents())}")
    host, model, options = model_for(agent)
    system = build_system_prompt(agent)

    loaded = load_refs(agent, load)
    if loaded:
        values = dict(values)
        values["input"] = "\n\n".join(filter(None, [loaded, values.get("input", "")]))

    task = render_task(agent, values)
    output = generate(host, model, system, task, options=options, stream=stream)
    return Result(agent=agent, model=model, system=system, task=task, output=output)
