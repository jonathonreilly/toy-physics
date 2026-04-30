#!/usr/bin/env python3
"""Build the citation graph from all docs/*.md notes.

Walks every .md file under docs/ (excluding docs/audit/), extracts:
  - claim_id (stable, derived from path)
  - title (first H1)
  - raw status line and normalized current_status
  - cited authorities (markdown links to other .md files in docs/)
  - primary runner script path
  - note hash (sha256 of body)

Writes docs/audit/data/citation_graph.json.

This script is deterministic, offline, and read-only against the docs.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DOCS_DIR = REPO_ROOT / "docs"
AUDIT_DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
OUTPUT_PATH = AUDIT_DATA_DIR / "citation_graph.json"

# Skip the audit lane itself and any auto-generated subtrees.
SKIP_PREFIXES = ("audit/",)

# Status normalization: maps raw status text fragments to the audit lane's
# normalized vocabulary. Order matters; first match wins.
STATUS_PATTERNS = [
    (re.compile(r"\bproposed[_ -]retained\b", re.IGNORECASE), "proposed_retained"),
    (re.compile(r"\bproposed[_ -]promoted\b", re.IGNORECASE), "proposed_promoted"),
    # The audit lane treats every author-declared "retained" as
    # "proposed_retained" until audited. This is the load-bearing
    # interpretation rule from FRESH_LOOK_REQUIREMENTS.md.
    (re.compile(r"\bretained\b", re.IGNORECASE), "proposed_retained"),
    (re.compile(r"\bpromoted\b", re.IGNORECASE), "proposed_promoted"),
    (re.compile(r"\boutside\s+audit-ratified\s+tier\b", re.IGNORECASE), "support"),
    (re.compile(r"\bflagship\s+closed\b", re.IGNORECASE), "proposed_retained"),
    (re.compile(r"\bbounded\b", re.IGNORECASE), "bounded"),
    (re.compile(r"\bsupport\b", re.IGNORECASE), "support"),
    (re.compile(r"\b(open|scaffold|planning)\b", re.IGNORECASE), "open"),
    (re.compile(r"\baccepted\b", re.IGNORECASE), "support"),
    (re.compile(r"\bderived\b", re.IGNORECASE), "support"),
    (re.compile(r"\bno-?go\b", re.IGNORECASE), "support"),
]

STATUS_LINE_RE = re.compile(
    r"^\s*(?:\*\*Status:?\*\*|Status:)\s*(.+)$",
    re.IGNORECASE | re.MULTILINE,
)
TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
RUNNER_LABEL_RE = re.compile(
    r"^\s*(?:[-*]\s*)?"
    r"(?:\*\*(?:Primary runner|Primary artifact|Primary artifacts|Script|Runner):?\*\*|"
    r"Primary runner:|Primary artifact:|Primary artifacts:|Script:|Runner:)\s*",
    re.IGNORECASE,
)
RUNNER_PATH_RE = re.compile(
    r"(scripts/[A-Za-z0-9_./\-]+\.py)|(?<![A-Za-z0-9_./\-])([A-Za-z0-9_.\-]+\.py)"
)
RUNNER_SECTION_RE = re.compile(
    r"^##\s+(?:Primary\s+)?(?:Artifact(?:\s+chain)?|Artifacts|Script|Files)\b.*$",
    re.IGNORECASE | re.MULTILINE,
)
HEADING_RE = re.compile(r"^##\s+", re.MULTILINE)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s#]+\.md)(?:#[^)]*)?\)")


def claim_id_from_path(path: Path) -> str:
    """Stable claim_id from doc path: docs/X/Y.md -> X.Y (stem, lowercase)."""
    rel = path.relative_to(DOCS_DIR)
    parts = list(rel.with_suffix("").parts)
    return ".".join(parts).lower()


def normalize_status(raw: str | None) -> str:
    if not raw:
        return "unknown"
    text = raw.strip()
    for pattern, label in STATUS_PATTERNS:
        if pattern.search(text):
            return label
    return "unknown"


def extract_status(body: str) -> tuple[str | None, str]:
    m = STATUS_LINE_RE.search(body)
    if not m:
        return None, "unknown"
    raw = m.group(1).strip()
    return raw, normalize_status(raw)


def extract_title(body: str) -> str | None:
    m = TITLE_RE.search(body)
    return m.group(1).strip() if m else None


def normalize_runner_path(path: str) -> str | None:
    path = path.strip()
    if path.startswith("scripts/"):
        return path
    script_path = f"scripts/{path}"
    if (REPO_ROOT / script_path).exists():
        return script_path
    return None


def runner_paths(text: str) -> list[str]:
    paths: list[str] = []
    for m in RUNNER_PATH_RE.finditer(text):
        raw = m.group(1) or m.group(2)
        if raw:
            path = normalize_runner_path(raw)
            if path:
                paths.append(path)
    return paths


def first_runner_path(text: str) -> str | None:
    paths = runner_paths(text)
    return paths[0] if paths else None


def extract_section(body: str, start: int) -> str:
    m = HEADING_RE.search(body, start)
    end = m.start() if m else len(body)
    return body[start:end]


def extract_runner(body: str, rel_path: str | None = None) -> str | None:
    if rel_path and rel_path.startswith("ai_methodology/raw/"):
        return None

    lines = body.splitlines()
    for i, line in enumerate(lines):
        if not RUNNER_LABEL_RE.search(line):
            continue
        window = "\n".join(lines[i : i + 4])
        runner = first_runner_path(window)
        if runner:
            return runner

    for m in RUNNER_SECTION_RE.finditer(body):
        runner = first_runner_path(extract_section(body, m.end()))
        if runner:
            return runner

    top_paths = list(dict.fromkeys(runner_paths("\n".join(lines[:80]))))
    if len(top_paths) == 1:
        return top_paths[0]

    return None


def resolve_link_target(link_target: str, source_path: Path) -> Path | None:
    """Resolve a markdown link target relative to source_path. Returns
    the resolved path under DOCS_DIR if it lands inside DOCS_DIR, else None.
    """
    candidate = (source_path.parent / link_target).resolve()
    try:
        candidate.relative_to(DOCS_DIR)
    except ValueError:
        return None
    if not candidate.exists():
        return None
    return candidate


def extract_citations(body: str, source_path: Path) -> list[Path]:
    seen: dict[Path, None] = {}
    for raw_target in LINK_RE.findall(body):
        target_path = resolve_link_target(raw_target, source_path)
        if target_path is None or target_path == source_path:
            continue
        seen.setdefault(target_path, None)
    return list(seen.keys())


def is_skipped(rel_path: Path) -> bool:
    rel_str = rel_path.as_posix()
    return any(rel_str.startswith(prefix) for prefix in SKIP_PREFIXES)


def discover_notes() -> list[Path]:
    notes = []
    for path in sorted(DOCS_DIR.rglob("*.md")):
        rel = path.relative_to(DOCS_DIR)
        if is_skipped(rel):
            continue
        notes.append(path)
    return notes


def build_graph() -> dict:
    notes = discover_notes()
    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    path_to_id: dict[Path, str] = {}

    # First pass: register every note as a node.
    for note_path in notes:
        cid = claim_id_from_path(note_path)
        rel = note_path.relative_to(DOCS_DIR)
        body = note_path.read_text(encoding="utf-8", errors="replace")
        raw_status, current_status = extract_status(body)
        nodes[cid] = {
            "claim_id": cid,
            "path": note_path.relative_to(REPO_ROOT).as_posix(),
            "title": extract_title(body),
            "current_status_raw": raw_status,
            "current_status": current_status,
            "runner_path": extract_runner(body, rel.as_posix()),
            "note_hash": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "deps": [],
        }
        path_to_id[note_path] = cid

    # Second pass: resolve citations into deps.
    for note_path in notes:
        cid = path_to_id[note_path]
        body = note_path.read_text(encoding="utf-8", errors="replace")
        for cited_path in extract_citations(body, note_path):
            cited_cid = path_to_id.get(cited_path)
            if cited_cid is None or cited_cid == cid:
                continue
            if cited_cid in nodes[cid]["deps"]:
                continue
            nodes[cid]["deps"].append(cited_cid)
            edges.append({"from": cid, "to": cited_cid})

    # Stats.
    status_counts: dict[str, int] = {}
    for n in nodes.values():
        status_counts[n["current_status"]] = status_counts.get(n["current_status"], 0) + 1

    runners_with_path = sum(1 for n in nodes.values() if n["runner_path"])
    roots = [cid for cid, n in nodes.items() if not n["deps"]]
    leaves = [cid for cid in nodes if not any(e["to"] == cid for e in edges)]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": 1,
        "stats": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "status_counts": status_counts,
            "runners_with_path": runners_with_path,
            "root_count": len(roots),
            "leaf_count": len(leaves),
        },
        "nodes": nodes,
        "edges": edges,
        "roots": sorted(roots),
    }


def main() -> int:
    AUDIT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    graph = build_graph()
    OUTPUT_PATH.write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n")
    s = graph["stats"]
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"  nodes: {s['node_count']}  edges: {s['edge_count']}")
    print(f"  roots: {s['root_count']}  leaves: {s['leaf_count']}")
    print(f"  runners attached: {s['runners_with_path']}")
    print(f"  status_counts: {s['status_counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
