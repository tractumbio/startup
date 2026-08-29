# Tractum Agents

Four local agents on Ollama, orchestrated with a human gate at every stage. Nothing this
system produces is ever final: agents write to `outputs/drafts/`, a person approves, and
only then does it reach `outputs/approved/`.

**Status: scaffold.** The structure, orchestration and guardrails are real and working.
The models, prompts and reference material are placeholders — see
[What you need to supply](#what-you-need-to-supply).

---

## The four agents

| Agent | Role | Tier |
|---|---|---|
| `lit_intel` | Monitors ophthalmic literature; surfaces and ranks targets, mechanisms, repurposing candidates | engine |
| `ophtha_science` | Mechanism deep dive, indication screening, safety/efficacy plan → GO/NO-GO | Tier 1 |
| `valuation` | rNPV/DCF sum-of-the-parts, scenario ranges, sensitivity | Tier 1 |
| `brand_voice` | Writes client-facing prose; audits any draft against brand + guardrails | both |

Each has a `SOUL.md` — who the agent is, how it thinks, what it must never do — loaded
into its context on every run.

## Layout

```
tractum-agents/
├── company/              baseline context, loaded into EVERY agent
│   ├── COMPANY.md          what the firm is, the two tiers
│   ├── BRAND.md            voice and visual system
│   └── GUARDRAILS.md       hard bans (confidentiality, claims, framing)
├── agents/<name>/
│   ├── SOUL.md             the agent's character and refusals
│   └── prompts/
│       ├── system.md       its operating instructions + output contract
│       └── task.md         task template with {{fields}}
├── config/
│   ├── models.yaml         which Ollama model runs which agent
│   └── orchestration.yaml  pipelines, stages, gates, context order
├── orchestrator/           the runtime (~500 lines, stdlib + requests + yaml)
├── inputs/                 your source material — gitignored
└── outputs/
    ├── drafts/             every agent run lands here
    └── approved/           only what a human approved
```

**Context assembly order** (set in `config/orchestration.yaml`):
`COMPANY.md → BRAND.md → <agent>/SOUL.md → GUARDRAILS.md → <agent>/prompts/system.md`.
Guardrails sit last, closest to the task, on purpose.

## Setup

```bash
cd tractum-agents
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # .env is gitignored

ollama serve                  # in another terminal
ollama pull llama3.1:8b       # or whatever you set in config/models.yaml

python -m orchestrator.run doctor
```

`doctor` checks config, finds the agents, reaches Ollama, and tells you exactly which
models are missing and the `ollama pull` command to fix each one.

## Use

```bash
# what's configured
python -m orchestrator.run agents
python -m orchestrator.run pipelines

# one agent
python -m orchestrator.run agent ophtha_science \
    --input inputs/asset-brief.md \
    --set asset="TBC-101" \
    --set primary_indication="idiopathic pulmonary fibrosis" \
    --set client_question="Is there a retinal opportunity here?"

# full Tier 1 chain: scan -> assess -> model -> write, gated at each step
python -m orchestrator.run pipeline tier1_assessment --input inputs/asset-brief.md

# audit an existing draft against brand + guardrails
python -m orchestrator.run agent brand_voice \
    --set mode=AUDIT --set ask="Audit this against GUARDRAILS.md" \
    --input outputs/drafts/some-draft.md
```

Output streams to your terminal as it generates. At each gate you get
`[a]pprove [r]evise [x]reject [e]dit [q]uit` — `e` opens the draft in `$EDITOR`.

## The human gate

- Every stage writes a draft **before** asking anything.
- A stage that is not approved **stops the pipeline**. Rejected analysis never feeds a
  downstream stage — that is the main way bad reasoning reaches a client.
- With no TTY (cron, CI, a piped run) the gate **stops rather than assumes approval**.
  There is no global auto-approve flag, deliberately.
- `gate: never` exists per-stage in `orchestration.yaml` for cheap, low-risk steps. Use
  it sparingly; nothing currently ships with it.

## What you need to supply

The scaffold runs; these are the placeholders that make it *yours*. In priority order:

**1. Models — `config/models.yaml`.** Every agent currently points at `llama3.1:8b`.
Per-agent temperature is already tuned for the job (valuation `0.1`, lit_intel `0.2`,
brand_voice `0.6`) — keep that shape when you swap models. Your strongest reasoning model
belongs on `ophtha_science`; your best writer on `brand_voice`.

**2. Baseline context — `company/*.md`.** These load into every single run, so an error
here is an error in every draft. `COMPANY.md` and `BRAND.md` are drawn from the project
notes and are accurate but thin. The highest-value thing you can add: two or three
paragraphs of **your own writing** you'd be happy to send a client, dropped into
`BRAND.md`. That teaches voice better than any list of adjectives.

**3. Reference files — `inputs/` and `workspace/`.** Both gitignored, so client material
is safe in either. Use `inputs/` for raw source you pass with `--input`; use
`workspace/<agent>/` for material a given agent should hold onto across runs, and
`workspace/shared/` for anything all four should be able to cite.

**4. Prompts — `agents/*/prompts/`.** The output contracts are opinionated already. Tune
`system.md` when an agent's output is the wrong *shape*; tune `SOUL.md` when its
*judgment* is wrong.

**5. Guardrails — `company/GUARDRAILS.md`.** Twelve hard bans covering client
confidentiality, unsourced numbers, the ErythroSight non-disclosure, AI-as-hero framing,
and the "digital twin" ban. Add to this whenever a draft gets something wrong in a way
that must never recur.

## Secrets

`.gitignore` excludes `.env` and every `*.env*` variant, `outputs/`, `inputs/` (except
its README), `workspace/` contents (the folder structure is kept, the working data is
not), `*.key`, `*.pem`, `*credentials*.json`, model blobs (`*.gguf`, `*.bin`,
`*.safetensors`), and `.DS_Store`. The default local-Ollama setup needs **no API key at
all**. If you add a hosted provider later, its key goes in `.env` and nowhere else.

Client names never appear in this repo — that is guardrail #1, and it applies to source
files as much as to output.
