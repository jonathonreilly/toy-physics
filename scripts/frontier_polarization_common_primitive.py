#!/usr/bin/env python3
"""Cross-lane synthesis for the missing polarization primitive family.

This is not a closure proof. It checks whether the finite-rank widening lane
and the direct universal GR lane are asking for the same axiom-native object
in two stages:

1. support-side `Pi_3+1` before scalar renormalization collapse;
2. curvature-side `Pi_curv` after the exact `3+1` Hessian candidate.

The intended conclusion is:

- same primitive family: yes
- same exact object: no
- smallest common primitive: a covariant `3+1` polarization bundle /
  projector bundle with both support-side and curvature-side specializations
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

FINITE_RANK = DOCS / "FINITE_RANK_3PLUS1_PROMOTION_BLOCKER_NOTE.md"
FINITE_FRAME = DOCS / "FINITE_RANK_SUPPORT_POLARIZATION_FRAME_NOTE.md"
UNIVERSAL_FRAME = DOCS / "UNIVERSAL_GR_POLARIZATION_FRAME_BUNDLE_BLOCKER_NOTE.md"
UNIVERSAL_CURV = DOCS / "UNIVERSAL_GR_CURVATURE_LOCALIZATION_BLOCKER_NOTE.md"
ROUTE2 = DOCS / "S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md"
SYNTHESIS = DOCS / "POLARIZATION_COMMON_PRIMITIVE_SYNTHESIS_NOTE.md"


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


CHECKS: list[Check] = []


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def matches(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) is not None


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def main() -> int:
    finite_rank = read(FINITE_RANK)
    finite_frame = read(FINITE_FRAME)
    universal_frame = read(UNIVERSAL_FRAME)
    universal_curv = read(UNIVERSAL_CURV)
    route2 = read(ROUTE2)
    synthesis = read(SYNTHESIS)

    record(
        "finite-rank blocker asks for a support-side polarization lift before scalar collapse",
        has(finite_rank, "Pi_3+1") and has(finite_rank, "tensor-valued support-side polarization frame"),
        "finite-rank lane is explicitly pre-collapse and support-side",
    )
    record(
        "finite-rank support-frame note shows the current support side is rank one after renormalization",
        has(finite_frame, "rank one") and has(finite_frame, "polarization frame"),
        "rank-one support collapse prevents a canonical support-side frame",
    )
    record(
        "universal blocker asks for a covariant polarization-frame bundle before curvature localization",
        has(universal_frame, "covariant `3+1` polarization-frame / projector bundle") and has(universal_frame, "Pi_curv"),
        "universal lane is explicitly post-candidate and localization-side",
    )
    record(
        "universal curvature blocker says localization is frame-dependent across valid `3+1` frames",
        (matches(universal_curv, r"different localized channel\s+coefficients")
         or has(universal_curv, "canonical `Pi_curv`"))
        and has(universal_curv, "Pi_curv"),
        "the universal lane is blocked by missing covariance, not by missing scalar data",
    )
    record(
        "Route 2 provides the shared interface object between support and curvature sides",
        has(route2, "K_R(q)") and has(route2, "I_TB") and has(route2, "Xi_TB"),
        "Route 2 carries the aligned bright channels plus the `PL S^3 x R` semigroup factor",
    )
    record(
        "the synthesis note states the same-family / not-same-object conclusion",
        matches(synthesis, r"same missing\s+primitive family") and has(synthesis, "not the same exact object"),
        "the note isolates a shared polarization-bundle family with two specializations",
    )

    print("\n" + "=" * 78)
    print("SYNTHESIS")
    print("=" * 78)
    print("Shared primitive family: YES")
    print("Same exact object: NO")
    print(
        "Smallest common primitive: a covariant `3+1` polarization-frame / projector "
        "bundle with support-side and curvature-side specializations."
    )
    print("Support specialization: `Pi_3+1` before scalar collapse.")
    print("Curvature specialization: `Pi_curv` before Einstein/Regge localization.")

    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print("\n" + "=" * 78)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
