"""Interactive chat with the agents, with supervision built in.

Talk normally; slash commands do the work around the conversation. The point is that
reviewing and steering happen in the same place as the talking — you push back, and when
an answer is good you send it to the gate without leaving the thread.
"""
from __future__ import annotations

import sys
from pathlib import Path

from . import store
from .agent import available_agents
from .config import ROOT, model_for
from .gate import approve, rel, write_draft
from .ollama import OllamaError
from .session import Session, Turn

BOLD, DIM, RESET = "\033[1m", "\033[2m", "\033[0m"

HELP = """
Talk to the agent by just typing. Commands:

  /who                  list agents and their models
  /agent <name>         hand this conversation to another agent, history intact
  /new [name]           start a fresh session
  /open <agent> <name>  reopen a saved session
  /sessions             list saved sessions

  /ls                   list workspace files (every agent's)
  /load <owner:name>    put a workspace file into the conversation
  /save <name>          save the last reply into this agent's store
  /share <name>         save the last reply into shared/ (all agents can read it)

  /draft                send the last reply to the approval gate
  /transcript           save the whole conversation as a draft
  /history              replay this conversation
  /clear                forget this conversation (the saved file stays)

  /help                 this
  /quit                 leave (the session is saved automatically)
"""


def _banner(sess: Session) -> None:
    try:
        _, model, _ = model_for(sess.agent)
    except ValueError:
        model = "(unconfigured)"
    print(f"\n{BOLD}{sess.agent}{RESET} {DIM}· {model} · session '{sess.name}'{RESET}")
    print(f"{DIM}/help for commands, /quit to leave{RESET}\n")


def _cmd(sess: Session, line: str) -> tuple[Session, bool]:
    """Handle a slash command. Returns (session, keep_going)."""
    parts = line.strip().split()
    cmd, args = parts[0], parts[1:]

    if cmd in ("/quit", "/q", "/exit"):
        sess.save()
        print(f"{DIM}saved: {rel(sess.path)}{RESET}")
        return sess, False

    if cmd == "/help":
        print(HELP)

    elif cmd == "/who":
        for a in available_agents():
            try:
                _, model, opts = model_for(a)
            except ValueError:
                model, opts = "(unconfigured)", {}
            here = "  <- you are here" if a == sess.agent else ""
            temp = opts.get("temperature", "?")
            print(f"  {a:16} {model:20} temp={temp}{here}")

    elif cmd == "/agent":
        if not args:
            print("  usage: /agent <name>")
        elif args[0] not in available_agents():
            print(f"  unknown agent. Known: {', '.join(available_agents())}")
        elif args[0] == sess.agent:
            print(f"  already talking to {sess.agent}")
        else:
            old = sess.agent
            sess.handoff(args[0])
            print(f"  {old} -> {BOLD}{sess.agent}{RESET}; it can see the conversation so far")

    elif cmd == "/new":
        name = args[0] if args else f"chat-{len(Session.list_all()) + 1}"
        sess.save()
        sess = Session(name=name, agent=sess.agent)
        print(f"  new session '{name}' with {sess.agent}")

    elif cmd == "/open":
        if len(args) < 2:
            print("  usage: /open <agent> <session-name>")
        else:
            loaded = Session.load(args[1], args[0])
            if not loaded:
                print(f"  no session '{args[1]}' for {args[0]}")
            else:
                sess.save()
                sess = loaded
                print(f"  opened '{sess.name}' ({len(sess.turns)} turns)")

    elif cmd == "/sessions":
        rows = Session.list_all()
        if not rows:
            print("  no saved sessions")
        for agent, name, count in rows:
            print(f"  {agent:16} {name:24} {count} turns")

    elif cmd == "/ls":
        entries = store.list_all()
        if not entries:
            print("  workspace is empty")
        for e in entries:
            print(f"  {e.ref:46} {e.size:>8,} b  {e.modified}")

    elif cmd == "/load":
        if not args:
            print("  usage: /load <owner:name>")
        else:
            try:
                body = store.read(args[0], sess.agent)
            except (ValueError, FileNotFoundError, PermissionError) as exc:
                print(f"  {exc}")
            else:
                sess.turns.append(Turn(
                    role="user",
                    content=f"Here is the workspace file `{args[0]}`:\n\n{body}",
                    agent=sess.agent,
                ))
                sess.save()
                print(f"  loaded {args[0]} ({len(body):,} chars) into the conversation")

    elif cmd in ("/save", "/share"):
        reply = sess.last_reply()
        if not reply:
            print("  nothing to save yet")
        elif not args:
            print(f"  usage: {cmd} <name>")
        else:
            name = args[0] if args[0].endswith(".md") else f"{args[0]}.md"
            target = f"shared:{name}" if cmd == "/share" else name
            try:
                path = store.write(sess.agent, target, reply)
            except (ValueError, PermissionError) as exc:
                print(f"  {exc}")
            else:
                print(f"  wrote {rel(path)}")

    elif cmd == "/draft":
        reply = sess.last_reply()
        if not reply:
            print("  nothing to send to the gate yet")
        else:
            try:
                _, model, _ = model_for(sess.agent)
            except ValueError:
                model = "unknown"
            d = write_draft(sess.agent, "chat", reply,
                            {"agent": sess.agent, "stage": "chat", "model": model,
                             "session": sess.name, "status": "draft"})
            print(f"  draft: {rel(d)}")
            if input("  approve it now? [y/N] ").strip().lower() in ("y", "yes"):
                note = input("  note (optional) > ").strip()
                dest = approve(d, note, agent=sess.agent)
                print(f"  approved -> {rel(dest)}")
            else:
                print("  left in drafts for review")

    elif cmd == "/transcript":
        d = write_draft(sess.agent, "transcript", sess.transcript(),
                        {"agent": sess.agent, "stage": "transcript",
                         "session": sess.name, "status": "draft"})
        print(f"  transcript: {rel(d)}")

    elif cmd == "/history":
        if not sess.turns:
            print("  nothing yet")
        for t in sess.turns:
            who = "you" if t.role == "user" else t.agent
            body = t.content if len(t.content) < 400 else t.content[:400] + " […]"
            print(f"\n{BOLD}{who}{RESET} {DIM}{t.at}{RESET}\n{body}")

    elif cmd == "/clear":
        sess.turns = []
        sess.save()
        print("  conversation cleared")

    else:
        print(f"  unknown command {cmd} — /help for the list")

    return sess, True


def run(agent: str, session_name: str = "default") -> int:
    if agent not in available_agents():
        print(f"unknown agent '{agent}'. Known: {', '.join(available_agents())}", file=sys.stderr)
        return 1
    if not sys.stdin.isatty():
        print("chat needs an interactive terminal", file=sys.stderr)
        return 1

    sess = Session.load(session_name, agent) or Session(name=session_name, agent=agent)
    _banner(sess)
    if sess.turns:
        print(f"{DIM}resuming — {len(sess.turns)} turns so far (/history to review){RESET}\n")

    while True:
        try:
            line = input(f"{BOLD}you ›{RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            sess.save()
            print(f"\n{DIM}saved: {rel(sess.path)}{RESET}")
            return 0

        if not line:
            continue
        if line.startswith("/"):
            sess, keep = _cmd(sess, line)
            if not keep:
                return 0
            continue

        print(f"\n{BOLD}{sess.agent} ›{RESET} ", end="", flush=True)
        try:
            sess.ask(line)
        except OllamaError as exc:
            print(f"\n{exc}", file=sys.stderr)
        except KeyboardInterrupt:
            print(f"\n{DIM}(interrupted){RESET}")
        print()
