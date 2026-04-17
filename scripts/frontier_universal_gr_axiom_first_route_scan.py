#!/usr/bin/env python3
"""Rank direct-to-universal-GR route candidates from the axiom-first survey.

This is a lightweight formalized check, not a proof. It scores the route
survey by how much each route looks like a universal action/self-consistency
architecture versus a restricted-class tensor completion ladder.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path("/Users/jonreilly/Projects/Physics")
SURVEY = ROOT / "docs" / "FULL_GR_AXIOM_FIRST_PATHS_NOTE.md"
OUTPUT = ROOT / "docs" / "UNIVERSAL_GR_AXIOM_FIRST_ROUTE_MEMO.md"


POSITIVE_TERMS = {
    "observable principle": 6,
    "self-consistency": 6,
    "effective action": 5,
    "variational": 5,
    "covariance": 4,
    "local action": 4,
    "unique": 3,
    "universal": 2,
    "axiom": 2,
    "field theory": 2,
}

NEGATIVE_TERMS = {
    "restricted class": 8,
    "star-supported": 6,
    "finite-rank": 5,
    "shell": 4,
    "support block": 4,
    "tensor boundary": 4,
    "tensor completion": 3,
    "boundary": 2,
    "source family": 3,
}


@dataclass
class RouteScore:
    number: int
    title: str
    score: int
    positive_hits: list[str]
    negative_hits: list[str]


def load_survey() -> str:
    return SURVEY.read_text(encoding="utf-8")


def split_routes(text: str) -> list[tuple[int, str, str]]:
    pattern = re.compile(r"^## (\d+)\. (.+)$", re.M)
    matches = list(pattern.finditer(text))
    routes: list[tuple[int, str, str]] = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        number = int(m.group(1))
        title = m.group(2).strip()
        body = text[start:end]
        routes.append((number, title, body))
    return routes


def score_route(number: int, title: str, body: str) -> RouteScore:
    lower = body.lower()
    score = 0
    positive_hits: list[str] = []
    negative_hits: list[str] = []

    for term, weight in POSITIVE_TERMS.items():
        count = lower.count(term)
        if count:
            score += weight * count
            positive_hits.append(f"{term} x{count}")

    for term, weight in NEGATIVE_TERMS.items():
        count = lower.count(term)
        if count:
            score -= weight * count
            negative_hits.append(f"{term} x{count}")

    return RouteScore(number, title, score, positive_hits, negative_hits)


def main() -> int:
    text = load_survey()
    routes = [score_route(n, t, b) for n, t, b in split_routes(text)]
    routes.sort(key=lambda r: r.score, reverse=True)

    print("UNIVERSAL GR AXIOM-FIRST ROUTE SCAN")
    print("=" * 78)
    for r in routes[:5]:
        print(f"Route {r.number}: {r.title}")
        print(f"  score: {r.score}")
        if r.positive_hits:
            print(f"  positive: {', '.join(r.positive_hits[:4])}")
        if r.negative_hits:
            print(f"  negative: {', '.join(r.negative_hits[:4])}")
        print()

    top = routes[0]
    print("Top direct-universal candidate:")
    print(f"  Route {top.number}: {top.title}")
    print(
        "  Interpretation: the top route is the least tethered to the restricted "
        "class language and most aligned with axiom/self-consistency/action "
        "language."
    )
    print()
    print(
        "Caveat: this is a route-ranking sanity check, not a proof. The memo "
        "must still be judged against the actual tensor-action blocker."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
