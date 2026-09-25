"""Extract every evidence-retrieval act and every URL observed in the corpus.

Produces analysis/data/retrieval.csv  (one row per retrieval attempt + result)
and analysis/data/url_mentions.csv   (domain/url -> sessions that saw it).

A "retrieval act" is any tool call whose purpose is to obtain external
information: web_search, web_fetch, or a bash command that invokes curl/wget/
news.sh/get.sh/pdftotext or similar. We also record whether the act produced an
error, because broken tooling is a first-class feature of this run.
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C  # noqa: E402

OUT = os.path.join(C.WORKSPACE, "analysis", "data")
os.makedirs(OUT, exist_ok=True)

URL_RE = re.compile(r"https?://[^\s\"'<>\)\],}\\]+")
RETRIEVAL_BASH = re.compile(
    r"\b(curl|wget|news\.sh|get\.sh|fetch\.sh|pdftotext|api\.openalex|arxiv|semanticscholar"
    r"|crossref|europepmc|\.sh\b)",
    re.I,
)
# domains that are search engines / proxies, not evidence sources themselves
SEARCH_HOSTS = {
    "www.google.com", "google.com", "news.google.com", "duckduckgo.com",
    "html.duckduckgo.com", "www.bing.com", "bing.com", "search.marcia",
    "www.mojeek.com", "mojeek.com", "search.brave.com", "lite.duckduckgo.com",
    "r.jina.ai", "webcache.googleusercontent.com",
}


def norm_url(u: str) -> str:
    u = u.rstrip(".,;:)]}\u201d\"'")
    return u


def host_of(u: str) -> str:
    try:
        h = urlparse(u).netloc.lower()
    except ValueError:
        return ""
    if h.startswith("www."):
        h = h[4:]
    return h


def bang_queries(cmd: str) -> list[str]:
    """Extract quoted search queries from a shell command."""
    qs = re.findall(r"""["']([^"']{8,200})["']""", cmd)
    return [q for q in qs if " " in q and not q.startswith("http")]


def main():
    sessions = C.load_all()
    retrieval = []
    urls: dict[str, dict] = {}

    for sid, s in sessions.items():
        calls = list(C.all_tool_calls(s))
        results = list(C.all_tool_results(s))
        rtext = {}
        for r in results:
            src = (r.get("message", {}) or {}).get("source", {}) or {}
            if src.get("callId"):
                rtext[src["callId"]] = C.text_of(
                    (r.get("message", {}) or {}).get("content")
                )
        # structured source metadata attached by the web_* tools
        meta_sources: dict[str, list] = {}
        for o in s.events:
            if o.get("type") != "tool/result":
                continue
            d = o.get("data") or {}
            src = (d.get("message", {}) or {}).get("source", {}) or {}
            meta = d.get("meta") or {}
            if src.get("callId") and meta.get("sources"):
                meta_sources[src["callId"]] = meta["sources"]

        for c in calls:
            name = c.get("name")
            try:
                a = json.loads(c.get("arguments") or "{}")
            except json.JSONDecodeError:
                a = {}
            txt = rtext.get(c.get("callId"), "") or ""
            kind = None
            target = ""
            if name == "web_search":
                kind = "web_search"
                target = a.get("query") or json.dumps(a)[:200]
            elif name == "web_fetch":
                kind = "web_fetch"
                target = a.get("url") or ""
            elif name == "read":
                fp = a.get("file_path") or ""
                if "/research/" in fp or "/sources/" in fp or "/findings/" in fp:
                    kind = "read_local_capture"
                    target = fp
            elif name == "bash":
                cmd = a.get("command") or ""
                if RETRIEVAL_BASH.search(cmd) and ("http" in cmd or "news.sh" in cmd
                                                    or "get.sh" in cmd):
                    kind = "bash_retrieval"
                    target = cmd[:400]
            if kind is None:
                continue

            is_err = bool(re.search(
                r"(?i)(unprocessable|error|failed|403|404|429|timed out|timeout|"
                r"connection refused|could not resolve|no such file|just a moment|"
                r"cloudflare|blocked|denied)", txt[:1500]))
            got_urls = sorted({norm_url(u) for u in URL_RE.findall(txt)})
            # structured sources returned by the web tools are authoritative
            structured = []
            for sc in meta_sources.get(c.get("callId"), []):
                if isinstance(sc, dict) and sc.get("url"):
                    structured.append(norm_url(sc["url"]))
            retrieval.append({
                "session": sid, "depth": s.depth, "label": s.label,
                "turn": c.get("turn"), "step": c.get("step"),
                "time": c.get("_time"), "tool": name, "kind": kind,
                "target": target.replace("\n", " ")[:400],
                "resultChars": len(txt),
                "suspectError": str(is_err),
                "nUrlsInResult": len(got_urls),
                "nStructuredSources": len(structured),
                "structuredSources": ";".join(structured[:40]),
                "query": (a.get("query") or "")[:200] if isinstance(a.get("query"), str) else "",
                "isLocalRead": str(kind == "read_local_capture"
                                   or (kind == "bash_retrieval" and "/deep-research/" in target
                                       and "sources/" in target)),
            })
            for u in set(got_urls) | set(structured):
                e = urls.setdefault(u, {"url": u, "host": host_of(u),
                                        "sessions": set(), "depth_min": 99,
                                        "structured": 0})
                e["sessions"].add(sid)
                e["depth_min"] = min(e["depth_min"], s.depth)
            for u in structured:
                if u in urls:
                    urls[u]["structured"] += 1

    fields = ["session", "depth", "label", "turn", "step", "time", "tool", "kind",
              "target", "resultChars", "suspectError", "nUrlsInResult",
              "nStructuredSources", "structuredSources", "query", "isLocalRead"]
    with open(os.path.join(OUT, "retrieval.csv"), "w", newline="", encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=fields)
        cw.writeheader()
        cw.writerows(retrieval)
    print(f"  retrieval.csv: {len(retrieval)} rows")

    urows = []
    for u, e in urls.items():
        urows.append({"url": u, "host": e["host"], "nSessions": len(e["sessions"]),
                      "sessions": ";".join(sorted(e["sessions"])),
                      "depthMin": e["depth_min"],
                      "fromStructuredMeta": e["structured"]})
    urows.sort(key=lambda r: (-r["nSessions"], r["host"]))
    with open(os.path.join(OUT, "url_mentions.csv"), "w", newline="", encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=list(urows[0].keys()))
        cw.writeheader()
        cw.writerows(urows)
    print(f"  url_mentions.csv: {len(urows)} unique URLs")

    # host-level rollup
    hosts: dict[str, dict] = {}
    for r in urows:
        h = hosts.setdefault(r["host"], {"host": r["host"], "nUrls": 0,
                                         "nSessions": set(), "urls": []})
        h["nUrls"] += 1
        h["nSessions"].update(r["sessions"].split(";"))
        h["urls"].append(r["url"])
    hrows = [{"host": h["host"], "nUrls": h["nUrls"],
              "nSessions": len(h["nSessions"]),
              "isSearchProxy": str(h["host"] in SEARCH_HOSTS)}
             for h in hosts.values()]
    hrows.sort(key=lambda r: -r["nUrls"])
    with open(os.path.join(OUT, "hosts.csv"), "w", newline="", encoding="utf-8") as f:
        cw = csv.DictWriter(f, fieldnames=list(hrows[0].keys()))
        cw.writeheader()
        cw.writerows(hrows)
    print(f"  hosts.csv: {len(hrows)} hosts")

    # quick console signal
    from collections import Counter
    kc = Counter(r["kind"] for r in retrieval)
    print("\n  retrieval kinds:", dict(kc))
    ec = Counter(r["suspectError"] for r in retrieval)
    print("  suspect-error:", dict(ec))
    shared = [r for r in urows if int(r["nSessions"]) > 1]
    print(f"  URLs seen by >1 session: {len(shared)} / {len(urows)}")
    print("  top shared URLs:")
    for r in shared[:15]:
        print(f"    x{r['nSessions']:<3} {r['url'][:110]}")


if __name__ == "__main__":
    main()
