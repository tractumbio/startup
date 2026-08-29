#!/usr/bin/env bash
# One-shot local setup. Safe to re-run — it skips whatever is already done.
set -euo pipefail

cd "$(dirname "$0")"
say() { printf '\n\033[1m%s\033[0m\n' "$*"; }
ok()  { printf '  ok   %s\n' "$*"; }
warn(){ printf '  --   %s\n' "$*"; }

say "Tractum agents — local setup"

# --- python ---
PY=""
for c in python3.12 python3.11 python3; do
  if command -v "$c" >/dev/null 2>&1; then
    if "$c" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)'; then
      PY="$c"; break
    fi
  fi
done
if [ -z "$PY" ]; then
  echo "  !!   need Python 3.10+; none found on PATH" >&2
  exit 1
fi
ok "python: $($PY --version)"

# --- venv ---
if [ -d .venv ]; then
  ok "venv already exists (.venv)"
else
  "$PY" -m venv .venv
  ok "created .venv"
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt
ok "dependencies installed"

# --- env ---
if [ -f .env ]; then
  ok ".env already present (left untouched)"
else
  cp .env.example .env
  ok "created .env from .env.example"
fi

# --- ollama ---
say "Ollama"
if command -v ollama >/dev/null 2>&1; then
  ok "ollama installed: $(ollama --version 2>&1 | head -1)"
  if curl -sf "${OLLAMA_HOST:-http://localhost:11434}/api/tags" >/dev/null 2>&1; then
    ok "server reachable"
  else
    warn "server not reachable — start it with:  ollama serve"
  fi
else
  warn "ollama not installed — https://ollama.com/download"
  warn "then:  ollama pull llama3.1:8b   (or whatever you set in config/models.yaml)"
fi

# --- preflight ---
say "Preflight"
python -m orchestrator.run doctor || true

say "Next"
cat <<'TXT'
  source .venv/bin/activate
  make help                  # what you can run
  make doctor                # re-check models once Ollama is up

  Then edit, in priority order:
    config/models.yaml       which model runs which agent
    company/COMPANY.md       the firm (loads into EVERY run)
    company/BRAND.md         voice — add your own writing here
TXT
