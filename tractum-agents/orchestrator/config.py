"""Config loading, with ${VAR:-default} expansion for env-driven values."""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent

_ENV_RE = re.compile(r"\$\{([A-Z_][A-Z0-9_]*)(?::-([^}]*))?\}")


def _expand(value: Any) -> Any:
    if isinstance(value, str):
        return _ENV_RE.sub(lambda m: os.environ.get(m.group(1), m.group(2) or ""), value)
    if isinstance(value, dict):
        return {k: _expand(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand(v) for v in value]
    return value


def load_yaml(relpath: str) -> dict:
    path = ROOT / relpath
    if not path.exists():
        raise FileNotFoundError(f"missing config: {relpath}")
    return _expand(yaml.safe_load(path.read_text()) or {})


def load_env() -> None:
    """Read .env into os.environ without clobbering what's already set."""
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def model_for(agent: str) -> tuple[str, str, dict]:
    """Return (host, model, options) for an agent, merging defaults."""
    cfg = load_yaml("config/models.yaml")
    defaults = cfg.get("defaults", {}) or {}
    entry = (cfg.get("agents", {}) or {}).get(agent, {}) or {}

    host = entry.get("host") or defaults.get("host") or "http://localhost:11434"
    model = entry.get("model") or defaults.get("model")
    if not model:
        raise ValueError(f"no model configured for agent '{agent}' in config/models.yaml")

    options = dict(defaults.get("options") or {})
    options.update(entry.get("options") or {})
    return host, model, options
