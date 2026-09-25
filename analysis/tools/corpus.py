"""Shared corpus loader for the DSH research-process analysis.

Reads the immutable export under dsh-session-session-<id>/ (main session.v3.jsonl
plus subagents/<uuid>/session.v3.jsonl) and yields normalised Python objects.

The corpus is NEVER written to. All derived data goes to analysis/data/.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from typing import Any, Iterator

WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CORPUS_ROOT = os.path.join(
    WORKSPACE, "dsh-session-session-92c9e38d-5c41-403b-8bd0-52dc0ac5c357"
)
MAIN = os.path.join(CORPUS_ROOT, "session.v3.jsonl")
SUBAGENTS = os.path.join(CORPUS_ROOT, "subagents")

# Main session id (from the `session` header record).
MAIN_SESSION_ID = "session-92c9e38d-5c41-403b-8bd0-52dc0ac5c357"


def sha256_file(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def session_paths() -> list[tuple[str, str]]:
    """Return [(session_id, path)] for main + all subagents, ordered by id."""
    out = [(MAIN_SESSION_ID, MAIN)]
    if os.path.isdir(SUBAGENTS):
        for d in sorted(os.listdir(SUBAGENTS)):
            p = os.path.join(SUBAGENTS, d, "session.v3.jsonl")
            if os.path.isfile(p):
                out.append((d, p))
    return out


@dataclass
class Session:
    sid: str
    path: str
    header: dict[str, Any]
    descriptor: dict[str, Any] | None = None
    events: list[dict[str, Any]] = field(default_factory=list)
    malformed: int = 0

    # derived
    @property
    def parent(self) -> str | None:
        return self.header.get("parentSession")

    @property
    def depth(self) -> int:
        return int(self.header.get("delegationDepth") or 0)

    @property
    def created_at(self) -> int:
        return int(self.header.get("createdAt") or 0)

    @property
    def label(self) -> str:
        if self.descriptor:
            return self.descriptor.get("label") or ""
        return ""

    def __iter__(self) -> Iterator[dict[str, Any]]:
        return iter(self.events)


def load_session(sid: str, path: str) -> Session:
    header: dict[str, Any] = {}
    descriptor = None
    events: list[dict[str, Any]] = []
    malformed = 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            t = o.get("type")
            if t == "session":
                header = o
                continue
            if t == "subagent/descriptor":
                descriptor = o.get("data")
                continue
            events.append(o)
    return Session(sid=sid, path=path, header=header, descriptor=descriptor,
                   events=events, malformed=malformed)


def load_all() -> dict[str, Session]:
    return {sid: load_session(sid, p) for sid, p in session_paths()}


# --------------------------------------------------------------------------
# Event accessors
# --------------------------------------------------------------------------

def ev_time(o: dict) -> int:
    return int(o.get("time") or 0)


def text_of(content: Any) -> str:
    """Flatten a DSH content array into plain text."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    parts: list[str] = []
    if isinstance(content, list):
        for c in content:
            if not isinstance(c, dict):
                parts.append(str(c))
                continue
            ct = c.get("type")
            if ct == "text":
                parts.append(c.get("text") or "")
            elif ct == "reasoning":
                parts.append(c.get("text") or "")
            elif ct == "tool-result":
                parts.append(text_of(c.get("content")))
            elif ct == "tool-call":
                parts.append(c.get("arguments") or "")
    return "\n".join(p for p in parts if p)


def iter_steps(s: Session):
    """Yield (turn, step, assistant_event, [tool_calls], [tool_results])."""
    calls: dict[int, list[dict]] = {}
    results: dict[int, list[dict]] = {}
    for o in s.events:
        t = o.get("type")
        d = o.get("data") or {}
        if t == "tool/call":
            calls.setdefault((d.get("turn"), d.get("step")), []).append(d)
        elif t == "tool/result":
            results.setdefault((d.get("turn"), d.get("step")), []).append(d)
    for o in s.events:
        if o.get("type") != "assistant/message":
            continue
        d = o.get("data") or {}
        key = (d.get("turn"), d.get("step"))
        yield d.get("turn"), d.get("step"), d, calls.get(key, []), results.get(key, [])


def all_tool_calls(s: Session):
    for o in s.events:
        if o.get("type") == "tool/call":
            d = dict(o.get("data") or {})
            d["_time"] = o.get("time")
            d["_seq"] = o.get("seq")
            yield d


def all_tool_results(s: Session):
    for o in s.events:
        if o.get("type") == "tool/result":
            yield o.get("data") or {}
