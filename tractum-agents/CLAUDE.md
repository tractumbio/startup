# tractum-agents — working notes

Read this before touching the agent stack. The parent repo's `../CLAUDE.md` covers the
firm's strategy and the founder's background; this file covers only this subdirectory.

## What this is

Four local agents on Ollama, orchestrated with a human gate at every stage. Scaffold
status: structure, orchestration, storage and guardrails are real and tested. Models,
prompts and reference material are placeholders.

## Setup

`./bootstrap.sh` then `make help`. Re-running bootstrap is safe — it never clobbers
`.env` or an existing venv.

## Design decisions already made — do not silently reverse these

1. **The human gate is structural, not a setting.** Every stage writes to
   `outputs/drafts/` before asking anything; an unapproved stage halts the pipeline
   rather than feeding downstream; with no TTY the gate stops rather than assuming
   approval. There is deliberately **no global auto-approve flag**. If a future task
   asks for unattended runs, raise the trade-off rather than adding one.

2. **Storage: read wide, write narrow.** Every agent reads every other agent's store;
   an agent writes only its own store or `shared/`. The asymmetry is the point — an
   agent that could overwrite another's store could corrupt the record a human is about
   to approve.

3. **Manifest, not contents.** Runs get a listing of workspace files; bodies are inlined
   only when named via `--load` or a stage's `load:`. Keeps contexts small and stops
   agents assuming what a file contains.

4. **Chat sessions are conversation state, not workspace documents.** They live in
   `workspace/<agent>/sessions/` but are excluded from `store.list_all()` and therefore
   from the manifest — otherwise every agent sees JSON transcripts listed as citable
   material. `make clean` must never delete them; that bug was introduced and fixed once
   already.

5. **Guardrails load last**, closest to the task, per `context_order` in
   `config/orchestration.yaml`. Keep that ordering.

6. **Refs cannot escape the workspace.** `store.resolve()` rejects `../` traversal.
   Tested; keep the test in mind if you refactor it.

## The repo is PUBLIC

`tractumbio/startup` is a public repository. Consequences that have already bitten once:

- **Never write a client name here, even to forbid it.** `GUARDRAILS.md` originally read
  "never name Merck, never name GenN Tech" — which publishes the association just as
  effectively as using it would. The private engagement list lives outside this repo.
- No `.env`, no client data, no study data in tracked files. `inputs/`, `outputs/` and
  `workspace/` contents are all gitignored for this reason.

## Where things live

- `company/` — baseline context loaded into **every** agent on **every** run. An error
  here is an error in every draft. `COMPANY.md` and `BRAND.md` were derived from the
  parent `CLAUDE.md`, so they inherit anything stale there.
- `agents/<name>/SOUL.md` — the agent's character and refusals. Edit this when its
  *judgment* is wrong.
- `agents/<name>/prompts/system.md` — output contract. Edit this when its output is the
  wrong *shape*.
- `config/models.yaml` — per-agent model and temperature. Temperatures are tuned by job
  (valuation 0.1, lit_intel 0.2, ophtha_science 0.3, brand_voice 0.6). Keep that shape
  when swapping models.
- `orchestrator/` — runtime. ~1,100 lines, stdlib plus `requests` and `PyYAML`.
  `run.py` CLI · `agent.py` one-shot runs · `session.py` + `repl.py` interactive chat ·
  `store.py` workspace · `gate.py` approval · `ollama.py` HTTP client (`generate` for
  one-shot, `chat` for multi-turn).

## Branch topology (as of this commit)

The repo has **no `main`**. The default branch is `claude/branch-repo-startup-622dv6`.
`dev` is the integration branch and carries the agent stack. PR #2 targets the default
branch from `claude/tractum-agent-github-setup-raopjg`.

Recommended cleanup, one manual step in GitHub settings: rename the default branch to
`main` (a rename preserves open PRs; creating a new branch does not).

## Verifying a change

`make check` — compiles the package, parses both configs, assembles every agent's prompt,
and confirms `.env` is ignored. Run it before committing.
