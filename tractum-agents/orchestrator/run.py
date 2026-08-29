"""CLI entry point.

    python -m orchestrator.run doctor
    python -m orchestrator.run agent ophtha_science --input inputs/asset.md --set asset="ABC-123"
    python -m orchestrator.run pipeline tier1_assessment --input inputs/asset.md
    python -m orchestrator.run pipelines
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .agent import available_agents, run_agent
from .config import ROOT, load_env, load_yaml, model_for
from .gate import approve, ask, rel, write_draft
from .ollama import OllamaError, list_models


def _kv(pairs: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for pair in pairs or []:
        if "=" not in pair:
            raise SystemExit(f"--set expects key=value, got '{pair}'")
        key, _, val = pair.partition("=")
        out[key.strip()] = val
    return out


def _read_input(path: str | None) -> str:
    if not path:
        return ""
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    if not p.exists():
        raise SystemExit(f"input not found: {path}")
    return p.read_text()


def cmd_doctor(args) -> int:
    print("Tractum agent stack — preflight\n")
    ok = True

    for name in ("config/models.yaml", "config/orchestration.yaml"):
        exists = (ROOT / name).exists()
        print(f"  {'ok  ' if exists else 'MISS'} {name}")
        ok &= exists

    agents = available_agents()
    print(f"\n  agents found: {', '.join(agents) or '(none)'}")
    for a in agents:
        for f in (f"agents/{a}/SOUL.md", f"agents/{a}/prompts/system.md"):
            if not (ROOT / f).exists():
                print(f"  MISS {f}")
                ok = False

    print("\n  Ollama:")
    hosts: dict[str, list[tuple[str, str]]] = {}
    for a in agents:
        try:
            host, model, _ = model_for(a)
        except ValueError as exc:
            print(f"    FAIL {a}: {exc}")
            ok = False
            continue
        hosts.setdefault(host, []).append((a, model))

    for host, pairs in hosts.items():
        try:
            installed = list_models(host)
        except OllamaError as exc:
            print(f"    FAIL {exc}")
            print("         start it with: ollama serve")
            ok = False
            continue
        print(f"    ok   reachable at {host} ({len(installed)} models installed)")
        for a, model in pairs:
            hit = model in installed or any(m.split(":")[0] == model.split(":")[0] for m in installed)
            print(f"    {'ok  ' if hit else 'MISS'} {a} -> {model}"
                  + ("" if hit else f"   (run: ollama pull {model})"))
            ok &= hit

    print("\n" + ("All checks passed." if ok else "Some checks failed — see above."))
    return 0 if ok else 1


def cmd_agents(args) -> int:
    for a in available_agents():
        try:
            _, model, _ = model_for(a)
        except ValueError:
            model = "(unconfigured)"
        print(f"{a:18} {model}")
    return 0


def cmd_pipelines(args) -> int:
    pipelines = load_yaml("config/orchestration.yaml").get("pipelines", {})
    for name, spec in pipelines.items():
        print(f"\n{name}\n  {spec.get('description', '')}")
        for stage in spec.get("stages", []):
            feeds = stage.get("feeds_from") or []
            suffix = f"  <- {', '.join(feeds)}" if feeds else ""
            print(f"    {stage['id']:10} {stage['agent']:16} gate={stage.get('gate', 'required')}{suffix}")
    return 0


def _run_stage(agent: str, stage_id: str, values: dict, gate_mode: str, gate_prompt: str):
    print(f"\n--- stage '{stage_id}' :: agent '{agent}' ---", file=sys.stderr)
    result = run_agent(agent, values)
    draft = write_draft(
        agent,
        stage_id,
        result.output,
        {"agent": agent, "stage": stage_id, "model": result.model, "status": "draft"},
    )
    if gate_mode == "never":
        print(f"(gate skipped by config) draft: {rel(draft)}", file=sys.stderr)
        return result, draft, "approve", ""
    decision, note = ask(gate_prompt, draft)
    if decision == "approve":
        dest = approve(draft, note)
        print(f"approved -> {rel(dest)}", file=sys.stderr)
    return result, draft, decision, note


def cmd_agent(args) -> int:
    values = _kv(args.set)
    values.setdefault("input", _read_input(args.input))
    stage = args.stage or args.agent
    try:
        _, _, decision, _ = _run_stage(args.agent, stage, values, args.gate, "")
    except OllamaError as exc:
        print(f"\n{exc}", file=sys.stderr)
        return 2
    return 0 if decision == "approve" else 1


def cmd_pipeline(args) -> int:
    pipelines = load_yaml("config/orchestration.yaml").get("pipelines", {})
    spec = pipelines.get(args.pipeline)
    if not spec:
        raise SystemExit(
            f"unknown pipeline '{args.pipeline}'. Known: {', '.join(pipelines) or '(none)'}"
        )

    base = _kv(args.set)
    base.setdefault("input", _read_input(args.input))
    completed: dict[str, str] = {}

    for stage in spec.get("stages", []):
        values = dict(base)
        upstream = [
            f"### Output of stage '{sid}'\n\n{completed[sid]}"
            for sid in (stage.get("feeds_from") or [])
            if sid in completed
        ]
        if upstream:
            values["input"] = "\n\n".join(upstream + ([base["input"]] if base.get("input") else []))

        try:
            result, draft, decision, note = _run_stage(
                stage["agent"], stage["id"], values,
                stage.get("gate", "required"), stage.get("gate_prompt", ""),
            )
        except OllamaError as exc:
            print(f"\n{exc}", file=sys.stderr)
            return 2

        if decision == "approve":
            completed[stage["id"]] = result.output
            continue

        # Anything other than approval stops the pipeline. Deliberate: a rejected
        # stage feeding a downstream one is how bad analysis reaches a client.
        print(
            f"\nPipeline stopped at stage '{stage['id']}' ({decision})."
            + (f"\nNote: {note}" if note else "")
            + f"\nDraft kept at {rel(draft)}",
            file=sys.stderr,
        )
        return 1

    print("\nPipeline complete. Approved outputs are in outputs/approved/.", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    load_env()
    parser = argparse.ArgumentParser(prog="orchestrator.run", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("doctor", help="check config, agents and Ollama models").set_defaults(func=cmd_doctor)
    sub.add_parser("agents", help="list agents and their models").set_defaults(func=cmd_agents)
    sub.add_parser("pipelines", help="list pipelines and stages").set_defaults(func=cmd_pipelines)

    p_agent = sub.add_parser("agent", help="run a single agent")
    p_agent.add_argument("agent")
    p_agent.add_argument("--input", help="file whose contents fill {{input}}")
    p_agent.add_argument("--set", action="append", metavar="KEY=VALUE",
                         help="fill a {{placeholder}} in the task template")
    p_agent.add_argument("--stage", help="label for the draft filename")
    p_agent.add_argument("--gate", choices=["required", "never"], default="required")
    p_agent.set_defaults(func=cmd_agent)

    p_pipe = sub.add_parser("pipeline", help="run a multi-stage pipeline")
    p_pipe.add_argument("pipeline")
    p_pipe.add_argument("--input", help="file whose contents fill {{input}}")
    p_pipe.add_argument("--set", action="append", metavar="KEY=VALUE")
    p_pipe.set_defaults(func=cmd_pipeline)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
