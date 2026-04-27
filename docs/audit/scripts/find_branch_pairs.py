#!/usr/bin/env python3
"""For every branch with novel paths, detect whether a paired Codex
review/land branch exists. Output a re-classification distinguishing:

  - reviewed_unlanded:  novel-path branch HAS a paired codex/{review,land}-*
                        branch but neither was merged to main. The work
                        was reviewed but not landed.
  - unreviewed_unlanded: novel-path branch has NO paired codex review/land
                         branch. This is the bucket the user explicitly
                         wants consolidated.
  - is_codex_review:    the branch is itself a codex/{review,land}-* branch.

Pairing heuristic: a Codex branch named codex/(review|land)-FOO-YYYY-MM-DD
is paired with a non-codex branch whose name shares a long substring with
FOO. We compute shared-substring overlap and accept matches above a
threshold. Manual review is logged for borderline cases.

Writes docs/audit/data/branch_pairs.json.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
INV_PATH = DATA_DIR / "branch_inventory.json"
OUTPUT_PATH = DATA_DIR / "branch_pairs.json"

CODEX_PREFIX_RE = re.compile(r"^codex/(?:review-|land-)?(.+?)(?:-\d{4}-\d{2}-\d{2})?$")
SIMILARITY_THRESHOLD = 0.55


def codex_topic(branch: str) -> str | None:
    if not branch.startswith("codex/"):
        return None
    m = CODEX_PREFIX_RE.match(branch)
    if not m:
        return None
    return m.group(1)


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(a=a, b=b).ratio()


def main() -> int:
    inv = json.loads(INV_PATH.read_text(encoding="utf-8"))
    branches = inv["branches"]

    by_name = {b["branch"]: b for b in branches}
    novel = [b for b in branches if b["category"] == "has_novel_paths"]

    codex_topics = []
    for b in branches:
        topic = codex_topic(b["branch"])
        if topic is not None:
            codex_topics.append((b["branch"], topic))

    out: list[dict] = []
    for b in novel:
        name = b["branch"]
        # Is this branch itself a codex review/land branch?
        if name.startswith("codex/"):
            out.append({
                "branch": name,
                "classification": "is_codex_review_or_land",
                "partners": [],
                "best_partner_score": None,
                "novel_path_count": b["novel_path_count"],
            })
            continue
        # Look for a codex partner whose topic-fragment matches this branch name.
        partners = []
        for codex_name, topic in codex_topics:
            score = similarity(name.lower(), topic.lower())
            if score >= SIMILARITY_THRESHOLD:
                partners.append({"codex_branch": codex_name, "score": round(score, 3)})
        partners.sort(key=lambda p: -p["score"])
        cls = "reviewed_unlanded" if partners else "unreviewed_unlanded"
        out.append({
            "branch": name,
            "classification": cls,
            "partners": partners[:3],  # top 3 candidate partners
            "best_partner_score": partners[0]["score"] if partners else None,
            "novel_path_count": b["novel_path_count"],
        })

    # Stats.
    counts = {}
    for o in out:
        counts[o["classification"]] = counts.get(o["classification"], 0) + 1

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "similarity_threshold": SIMILARITY_THRESHOLD,
        "novel_branch_count": len(out),
        "classification_counts": counts,
        "branches": sorted(out, key=lambda x: (x["classification"], x["branch"])),
    }
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"  classified: {len(out)}")
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {k:30s}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
