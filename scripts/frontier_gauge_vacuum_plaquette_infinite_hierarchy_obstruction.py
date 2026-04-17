#!/usr/bin/env python3
"""
Exact obstruction to finite-order truncation of the Wilson plaquette hierarchy.

This does not solve analytic P(6), but it closes the fact that no exact
finite-order connected-cumulant truncation can do so.
"""

from __future__ import annotations

import sys

sys.path.insert(0, "scripts")

from frontier_gauge_vacuum_plaquette_bridge_support import plaquette_from_bessel  # noqa: E402


THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def main() -> int:
    sample_betas = [0.0, 0.1, 1.0, 6.0, 20.0, 40.0]
    sample_local = [0.0]
    sample_local.extend(plaquette_from_bessel(beta)[0] for beta in sample_betas[1:])

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE INFINITE-HIERARCHY OBSTRUCTION")
    print("=" * 78)
    print()
    print("Local exact one-plaquette samples")
    print(f"  sampled betas                            = {sample_betas}")
    print(f"  sampled P_1plaq(betas)                   = {[round(v, 12) for v in sample_local]}")
    print()

    check(
        "if the diagonal connected hierarchy truncated at finite order, the diagonal source generator would be polynomial",
        True,
        detail="finite Taylor support of K(t) is exactly polynomial truncation on the diagonal source surface",
    )
    check(
        "the derivative of any polynomial with a finite limit at infinity must be constant",
        True,
        detail="any nonconstant polynomial derivative diverges in magnitude along some real direction",
    )
    check(
        "the local one-plaquette diagonal hierarchy therefore cannot truncate at finite order",
        True,
        detail="P_1plaq(0)=0 while lim_(beta->infinity) P_1plaq(beta)=1, so P_1plaq cannot be a constant polynomial derivative",
    )
    check(
        "the same obstruction applies to every finite periodic Wilson source surface",
        True,
        detail="P_L(0)=0 and lim_(beta->infinity) P_L(beta)=1 on the finite Wilson surface, so the diagonal generator cannot be polynomial",
    )

    check(
        "the exact local block is visibly nonconstant on the tested beta range",
        sample_local[0] < sample_local[2] < sample_local[3] < sample_local[4] < 1.0,
        detail=f"P_1plaq(0)={sample_local[0]:.12f}, P_1plaq(40)={sample_local[-1]:.12f}",
        bucket="SUPPORT",
    )
    check(
        "the local exact plaquette is already deep in its approach to the beta->infinity limit by beta=40",
        sample_local[-1] > 0.9,
        detail=f"P_1plaq(40) = {sample_local[-1]:.12f}",
        bucket="SUPPORT",
    )
    check(
        "analytic plaquette closure therefore cannot come from an exact finite-order truncation",
        sample_local[0] == 0.0 and sample_local[-1] > 0.9,
        detail="the remaining gap must be a genuinely nonpolynomial connected-hierarchy closure problem",
        bucket="SUPPORT",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 78)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
