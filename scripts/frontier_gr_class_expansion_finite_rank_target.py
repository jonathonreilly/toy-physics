#!/usr/bin/env python3
"""Class-expansion audit for the next gravity theorem.

This runner asks the narrow question:

    what is the smallest honest widening beyond the current
    star-supported/static-conformal restricted class?

It checks the finite-rank source route because that route already has exact
source/exterior closure and exact microscopic boundary-action stationarity.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent.parent


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


finite_rank = SourceFileLoader(
    "finite_rank_metric",
    str(ROOT / "scripts" / "frontier_finite_rank_source_to_metric_theorem.py"),
).load_module()


def main() -> int:
    print("GR CLASS EXPANSION AUDIT")
    print("=" * 78)
    print("  Question: smallest honest widening beyond the current restricted class")
    print("  Candidate: exact finite-rank source-to-metric theorem")
    print()

    phi_full, support, interior, q_eff = finite_rank.exact_finite_rank_field()
    boundary = finite_rank.boundary_stationarity_report(phi_full)
    coarse_report = finite_rank.coarse_metric_report(phi_full)
    best = coarse_report["best"]

    print(f"support size={len(support)}, q_eff_sum={np.sum(q_eff):.8f}")
    print(
        "best coarse row: "
        f"R_match={best[0]:.1f}, a={best[1]:.6f}, shell_rms={best[2]:.3f}, "
        f"direct={best[4]:.3e}, coarse={best[5]:.3e}"
    )
    print()

    record(
        "finite-rank source renormalization is exact",
        boundary["rebuild_err"] < 1e-12,
        f"boundary reconstruction error={boundary['rebuild_err']:.3e}",
    )
    record(
        "the microscopic boundary action is stationary on the finite-rank class",
        boundary["flux_err"] < 1e-12 and boundary["stationary_grad"] < 1e-12,
        (
            f"flux_err={boundary['flux_err']:.3e}, "
            f"stationary_grad={boundary['stationary_grad']:.3e}"
        ),
    )
    record(
        "the finite-rank class admits a vacuum-close coarse-grained scalar exterior metric",
        best[5] < 1e-5,
        (
            f"R_match={best[0]:.1f}, direct={best[4]:.3e}, "
            f"coarse={best[5]:.3e}"
        ),
        status="BOUNDED",
    )
    record(
        "the direct `3+1` metric residual remains nonzero",
        best[4] > 0,
        f"direct residual={best[4]:.3e}",
        status="BOUNDED",
    )

    print("\n" + "=" * 78)
    print("INTERPRETATION")
    print("=" * 78)
    print(
        "The finite-rank route widens the class cleanly: exact source-to-exterior "
        "closure and exact boundary-action stationarity survive. But the direct "
        "`3+1` tensor metric residual stays nonzero, so the exact Route-2 carrier/action "
        "does not naturally extend as a full tensor dynamics law beyond the current "
        "restricted class."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("Widening target supported: finite-rank source-to-metric.")
    else:
        print("One or more checks failed.")

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
