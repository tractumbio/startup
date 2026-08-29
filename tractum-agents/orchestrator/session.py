"""Conversation state for interactive supervision.

A session is a named, persisted thread of turns with one or more agents. It survives
restarts: transcripts live in `workspace/<agent>/sessions/`, so the same cross-agent
visibility rules apply to conversations as to everything else — you can hand a thread
from `ophtha_science` to `valuation` and the second agent can see what the first said.
"""
from __future__ import annotations

import datetime as _dt
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

from . import store
from .agent import build_system_prompt
from .config import model_for
from .ollama import chat


def _now() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class Turn:
    role: str          # user | assistant
    content: str
    agent: str         # which agent produced/received it
    at: str = field(default_factory=_now)


@dataclass
class Session:
    name: str
    agent: str
    turns: list[Turn] = field(default_factory=list)
    created: str = field(default_factory=_now)

    # --- persistence -----------------------------------------------------

    @property
    def path(self) -> Path:
        return store.agent_dir(self.agent) / "sessions" / f"{self.name}.json"

    def save(self) -> Path:
        p = self.path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(asdict(self), indent=2))
        return p

    @classmethod
    def load(cls, name: str, agent: str) -> "Session | None":
        p = store.agent_dir(agent) / "sessions" / f"{name}.json"
        if not p.exists():
            return None
        raw = json.loads(p.read_text())
        return cls(
            name=raw["name"],
            agent=raw["agent"],
            created=raw.get("created", _now()),
            turns=[Turn(**t) for t in raw.get("turns", [])],
        )

    @staticmethod
    def list_all() -> list[tuple[str, str, int]]:
        """(agent, session name, turn count) for every saved session."""
        out = []
        root = store.workspace_root()
        if not root.is_dir():
            return out
        for agent_dir in sorted(root.iterdir()):
            sessions = agent_dir / "sessions"
            if not sessions.is_dir():
                continue
            for f in sorted(sessions.glob("*.json")):
                try:
                    raw = json.loads(f.read_text())
                    out.append((agent_dir.name, f.stem, len(raw.get("turns", []))))
                except (json.JSONDecodeError, OSError):
                    continue
        return out

    # --- conversation ----------------------------------------------------

    def messages(self) -> list[dict]:
        """Full payload for the model: system prompt + every prior turn.

        The system prompt is rebuilt each call rather than frozen at session start, so
        an edit to SOUL.md or the workspace manifest takes effect on the next message
        instead of requiring a new session.
        """
        msgs = [{"role": "system", "content": build_system_prompt(self.agent)}]
        for t in self.turns:
            # Mark turns that came from a different agent, so the current one knows
            # it is reading a colleague's work rather than its own.
            content = t.content
            if t.role == "assistant" and t.agent != self.agent:
                content = f"[from the {t.agent} agent]\n\n{content}"
            msgs.append({"role": t.role, "content": content})
        return msgs

    def ask(self, text: str, on_token=None) -> str:
        self.turns.append(Turn(role="user", content=text, agent=self.agent))
        host, model, options = model_for(self.agent)
        reply = chat(host, model, self.messages(), options=options, on_token=on_token)
        self.turns.append(Turn(role="assistant", content=reply, agent=self.agent))
        self.save()
        return reply

    def last_reply(self) -> str | None:
        for t in reversed(self.turns):
            if t.role == "assistant":
                return t.content
        return None

    def handoff(self, new_agent: str) -> None:
        """Move the thread to another agent, keeping the history visible.

        The point of supervision across agents: valuation picks up the conversation
        with ophtha_science's verdict already in front of it, in the words it was
        actually argued in, not a summary.
        """
        self.save()                    # keep the transcript with the outgoing agent too
        self.agent = new_agent
        self.save()

    def transcript(self) -> str:
        lines = [f"# Session `{self.name}` — started {self.created}", ""]
        for t in self.turns:
            who = "You" if t.role == "user" else f"{t.agent}"
            lines.append(f"**{who}** · {t.at}\n\n{t.content}\n")
        return "\n".join(lines)
