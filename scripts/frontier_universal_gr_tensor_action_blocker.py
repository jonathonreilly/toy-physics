#!/usr/bin/env python3
"""Verifier for the direct-universal-GR tensor-action blocker.

This is not a closure proof. It checks that the current atlas really gives:

1. an exact scalar observable generator from the axiom-side observable
   principle;
2. an exact `3+1` kinematic lift on `PL S^3 x R`;
3. an exact tensor-valued variational candidate whose Einstein/Regge
   identification is still missing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

OBSERVABLE = DOCS / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md"
ROUTE2 = DOCS / "S3_TIME_SPACETIME_OBSERVABLE_ROUTE_NOTE.md"
HESSIAN = DOCS / "S3_TIME_OBSERVABLE_HESSIAN_ROUTE_NOTE.md"
BLOCKER = DOCS / "UNIVERSAL_GR_TENSOR_ACTION_BLOCKER_NOTE.md"
CANDIDATE = DOCS / "UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md"


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def main() -> int:
    obs = read(OBSERVABLE)
    r2 = read(ROUTE2)
    hess = read(HESSIAN)
    blk = read(BLOCKER)
    cand = read(CANDIDATE)

    checks = [
        Check(
            "scalar generator is exact",
            has(obs, "observable principle")
            and has(obs, "det(d+j)")
            and has(obs, "det d"),
            "observable principle gives the exact scalar generator",
        ),
        Check(
            "route-2 kinematic lift is exact",
            has(r2, "O_lift = 1"),
            "route-2 gives the exact PL S^3 x R selector",
        ),
        Check(
            "observable principle remains scalar-only on route-2",
            has(hess, "scalar-only on this route"),
            "the route-2 Hessian remains scalar-valued",
        ),
        Check(
            "tensor-valued candidate is exact but not yet identified",
            has(cand, "metric-source hessian")
            and has(cand, "unique symmetric")
            and has(cand, "quotient kernel")
            and has(blk, "curvature-localization map")
            and has(blk, "einstein/regge"),
            "candidate is exact as a construction, but the curvature-localization primitive is still open",
        ),
        Check(
            "missing identification is now sharp",
            has(blk, "curvature-localization map")
            and has(blk, "unique symmetric")
            and has(blk, "hessian kernel")
            and has(blk, "einstein/regge tensor law"),
            "blocker note names the exact remaining identification problem",
        ),
    ]

    print("UNIVERSAL GR TENSOR ACTION BLOCKER AUDIT")
    print("=" * 78)
    for c in checks:
        tag = "PASS" if c.ok else "FAIL"
        print(f"[{tag}] {c.name}")
        print(f"    {c.detail}")

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in checks)
    n_fail = len(checks) - n_pass
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(checks)}")
    if n_fail == 0:
        print(
            "Blocker confirmed: exact scalar observable principle and exact 3+1 "
            "kinematic lift are in hand, but no exact tensor-valued action or "
            "uniqueness theorem has been built."
        )
        return 0

    print("One or more blocker checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
