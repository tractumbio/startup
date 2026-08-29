"""Thin Ollama HTTP client. No SDK, no key — just the local server."""
from __future__ import annotations

import json
import os
import sys
from typing import Iterator

import requests


class OllamaError(RuntimeError):
    pass


def list_models(host: str) -> list[str]:
    try:
        r = requests.get(f"{host.rstrip('/')}/api/tags", timeout=10)
        r.raise_for_status()
    except requests.RequestException as exc:
        raise OllamaError(f"cannot reach Ollama at {host}: {exc}") from exc
    return [m["name"] for m in r.json().get("models", [])]


def generate(
    host: str,
    model: str,
    system: str,
    prompt: str,
    options: dict | None = None,
    stream: bool = True,
) -> str:
    """Run one completion. Streams to stderr so the operator sees progress."""
    payload = {
        "model": model,
        "system": system,
        "prompt": prompt,
        "stream": stream,
        "options": options or {},
    }
    timeout = float(os.environ.get("TRACTUM_TIMEOUT", "600"))
    url = f"{host.rstrip('/')}/api/generate"

    try:
        resp = requests.post(url, json=payload, stream=stream, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise OllamaError(
            f"Ollama call failed ({model} @ {host}): {exc}\n"
            f"Is `ollama serve` running, and have you pulled '{model}'?"
        ) from exc

    if not stream:
        return resp.json().get("response", "")

    chunks: list[str] = []
    for line in resp.iter_lines():
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        piece = data.get("response", "")
        chunks.append(piece)
        sys.stderr.write(piece)
        sys.stderr.flush()
        if data.get("done"):
            break
    sys.stderr.write("\n")
    return "".join(chunks)
