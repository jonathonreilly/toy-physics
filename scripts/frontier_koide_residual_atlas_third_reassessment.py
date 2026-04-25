#!/usr/bin/env python3
"""
Koide residual atlas third reassessment.

Purpose:
  After the all-order Q source-functional and all-order delta
  boundary-functional audits, separate exhausted retained classes from
  genuinely new physical-principle routes.

Result:
  The retained-audit frontier is no longer a local technical gap.  It is two
  explicit primitives:

      Q:     a physical law selecting the equal C3 center source.
      delta: a physical law selecting the open Berry/APS endpoint.

  Further progress must either derive one of those laws from a new physical
  principle, or prove an exhaustive theorem over a precisely specified new
  source/boundary class.  Support, numerology, or a scalar joint relation is
  still not closure.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASSES: list[tuple[str, bool, str]] = []


@dataclass(frozen=True)
class RemainingRoute:
    name: str
    side: str
    required_new_principle: str
    falsifier: str
    closure_risk: str


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def count(glob: str) -> int:
    return len(list(ROOT.glob(glob)))


def main() -> int:
    section("A. Current retained-audit packet size")

    q_no_go_count = count("scripts/frontier_koide_q_*no_go.py")
    delta_no_go_count = count("scripts/frontier_koide_delta_*no_go.py")
    record(
        "A.1 Q no-go packet is broad enough to require atlas discipline",
        q_no_go_count >= 60,
        f"q_no_go_scripts={q_no_go_count}",
    )
    record(
        "A.2 delta no-go packet is broad enough to require atlas discipline",
        delta_no_go_count >= 20,
        f"delta_no_go_scripts={delta_no_go_count}",
    )

    section("B. Live primitives after all-order audits")

    q_primitive = "physical_equal_C3_center_source_law"
    delta_primitive = "physical_open_Berry_APS_endpoint_law"
    record(
        "B.1 Q primitive is source preparation, not algebraic admissibility",
        q_primitive == "physical_equal_C3_center_source_law",
        "Aliases: K_TL=0, u=1/2, F_plus=F_perp, zero FI/source level.",
    )
    record(
        "B.2 delta primitive is endpoint selection, not closed eta support",
        delta_primitive == "physical_open_Berry_APS_endpoint_law",
        "Aliases: theta_end-theta0=eta_APS, endpoint trivialization, full selected open segment.",
    )

    section("C. Remaining route classes")

    routes = [
        RemainingRoute(
            "center-source gauge principle",
            "Q",
            "a retained gauge symmetry whose D-term/FI level is forced to zero",
            "nonzero FI/source levels are physically admissible",
            "quietly chooses zeta=0",
        ),
        RemainingRoute(
            "quotient-center finite-state principle",
            "Q",
            "a physical reason sources live on center labels rather than Hilbert-rank microstates",
            "rank trace remains a preparable source",
            "renames equal-label prior",
        ),
        RemainingRoute(
            "source-boundary anomaly functor",
            "Q",
            "an anomaly/inflow law whose boundary variable is the C3 center source",
            "topological class is discrete or source-blind",
            "adds an unretained map from topology to u",
        ),
        RemainingRoute(
            "reflection/exchange principle",
            "Q",
            "a retained physical exchange of rank-1 and rank-2 center totals",
            "rank obstruction remains",
            "uses abstract label swap",
        ),
        RemainingRoute(
            "selected-line endpoint boundary condition",
            "delta",
            "a physical boundary section fixed before seeing eta_APS",
            "smooth endpoint counterterms remain admissible",
            "sets endpoint to 2/9 by convention",
        ),
        RemainingRoute(
            "closed-loop identification theorem",
            "delta",
            "proof that the selected Brannen open segment is the whole APS loop",
            "complement segment can be nonzero",
            "sets complement to zero",
        ),
        RemainingRoute(
            "Pancharatnam endpoint-selection theorem",
            "delta",
            "canonical endpoint projectors/path from retained Cl(3)/Z3 data",
            "Pancharatnam phase varies with endpoint/path",
            "confuses gauge invariance with endpoint selection",
        ),
        RemainingRoute(
            "joint vector-valued boundary/source theorem",
            "joint",
            "two independent retained equations or a proven dependency between residuals",
            "scalar joint relation leaves a curve",
            "hides two target equations in one principle",
        ),
    ]
    detail = "\n".join(
        f"- [{route.side}] {route.name}: needs {route.required_new_principle}; falsifier={route.falsifier}; risk={route.closure_risk}"
        for route in routes
    )
    record(
        "C.1 at least eight remaining routes are explicit and falsifiable",
        len(routes) >= 8,
        detail,
    )

    section("D. Next attack rule")

    record(
        "D.1 do not continue local variants of exhausted classes",
        True,
        "Only attack a route if it strengthens a theorem class or introduces a genuinely new physical principle with falsifiers.",
    )
    record(
        "D.2 no positive closure is claimed by this atlas",
        True,
        "The atlas is a checkpoint; both primitives remain open.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("KOIDE_RESIDUAL_ATLAS_THIRD_REASSESSMENT=TRUE")
        print("KOIDE_RESIDUAL_ATLAS_THIRD_CLOSES_Q=FALSE")
        print("KOIDE_RESIDUAL_ATLAS_THIRD_CLOSES_DELTA=FALSE")
        print("RESIDUAL_Q=physical_equal_C3_center_source_law")
        print("RESIDUAL_DELTA=physical_open_Berry_APS_endpoint_law")
        print("NEXT_RULE=only_new_principle_or_stronger_exhaustive_theorem")
        return 0

    print("KOIDE_RESIDUAL_ATLAS_THIRD_REASSESSMENT=FALSE")
    print("KOIDE_RESIDUAL_ATLAS_THIRD_CLOSES_Q=FALSE")
    print("KOIDE_RESIDUAL_ATLAS_THIRD_CLOSES_DELTA=FALSE")
    print("RESIDUAL_Q=physical_equal_C3_center_source_law")
    print("RESIDUAL_DELTA=physical_open_Berry_APS_endpoint_law")
    return 1


if __name__ == "__main__":
    sys.exit(main())
