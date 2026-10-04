#!/bin/bash
# Session start for Tractum Bio cloud sessions.
# Installs the site-verify tooling and the agent stack's Python deps, and warns
# (without switching anything) if this checkout is behind main.
# Anything printed to stdout is shown to Claude at session start, so installers
# write to /dev/null and only the notices below are printed.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
cd "$ROOT"
problems=()

# 1. Site verification (Playwright; Chromium is pre-installed in /opt/pw-browsers)
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
if [ -d .claude/skills/site-verify ]; then
  if ! (cd .claude/skills/site-verify && npm install --no-audit --no-fund >/dev/null 2>&1); then
    problems+=("site-verify: npm install failed — run it manually in .claude/skills/site-verify")
  fi
fi

# 2. Agent stack (stdlib + requests + PyYAML in a local venv)
if [ -f tractum-agents/requirements.txt ]; then
  if ! ( cd tractum-agents \
         && { [ -d .venv ] || python3 -m venv .venv; } \
         && .venv/bin/python -m pip install -q -r requirements.txt ) >/dev/null 2>&1; then
    problems+=("tractum-agents: dependency install failed — run ./bootstrap.sh")
  fi
fi

# 3. Stale checkout warning. Never switch branches here: the session owns that.
branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"
if git fetch -q origin main >/dev/null 2>&1; then
  behind="$(git rev-list --count HEAD..origin/main 2>/dev/null || echo 0)"
  if [ "${behind:-0}" -gt 0 ]; then
    echo "NOTE: this checkout ($branch) is ${behind} commit(s) behind origin/main, which is the live branch."
    echo "Current work is on main. Check with the user before building on this branch."
  fi
fi

for p in "${problems[@]+"${problems[@]}"}"; do echo "SETUP PROBLEM: $p"; done
exit 0
