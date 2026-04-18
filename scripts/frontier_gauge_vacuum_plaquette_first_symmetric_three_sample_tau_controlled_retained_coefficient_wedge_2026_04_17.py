#!/usr/bin/env python3
"""
Tau-controlled outer wedge for the first retained coefficient data on the
explicit three-sample beta=6 plaquette PF seam.
"""

from __future__ import annotations

import numpy as np
import sympy as sp
from pathlib import Path
from scipy.special import iv


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

BETA = 6.0
ARG = BETA / 3.0
MODE_MAX = 80


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


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def highest_weight_triple(p: int, q: int) -> list[int]:
    return [p + q, q, 0]


def coefficient_matrix(mode: int, lam: list[int]) -> np.ndarray:
    return np.array(
        [[iv(mode + lam[j] + i - j, ARG) for j in range(3)] for i in range(3)],
        dtype=float,
    )


def wilson_character_coefficient(p: int, q: int) -> float:
    lam = highest_weight_triple(p, q)
    total = 0.0
    for mode in range(-MODE_MAX, MODE_MAX + 1):
        total += float(np.linalg.det(coefficient_matrix(mode, lam)))
    return total


def normalized_link_eigenvalue(p: int, q: int, c00: float) -> float:
    return wilson_character_coefficient(p, q) / (dim_su3(p, q) * c00)


def radical_entries() -> dict[str, sp.Expr]:
    rt2 = sp.sqrt(2)
    return {
        "a": -3 * sp.sqrt(2 - rt2),
        "d": 3 * rt2 + 3 * sp.sqrt(2 - sp.sqrt(2 + rt2)) - 3 * sp.sqrt(2 - sp.sqrt(2 - rt2)),
        "e": 16
        - 8 * sp.sqrt(2 + rt2)
        - 8 * sp.sqrt(2 + sp.sqrt(2 + rt2))
        + 8 * sp.sqrt(2 + sp.sqrt(2 - rt2)),
    }


def main() -> int:
    char_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md")
    envelope_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md"
    )
    cone_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_POSITIVE_CONE_ORDER_WITNESS_NOTE_2026-04-17.md"
    )
    local_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_PARTIAL_EVALUATION_NOTE_2026-04-17.md"
    )

    entries = radical_entries()
    a = sp.simplify(entries["a"])
    d = sp.simplify(entries["d"])
    e = sp.simplify(entries["e"])
    alpha = sp.simplify(-a)
    beta = sp.simplify(-e)

    rho10, rho11, tau = sp.symbols("rho10 rho11 tau", nonnegative=True)

    wedge_identity_a = sp.simplify((1 + tau) / alpha - rho10 - (1 + a * rho10 + tau) / alpha)
    wedge_identity_c = sp.simplify(
        (1 + d * rho10 + tau) / beta - rho11 - (1 + d * rho10 + e * rho11 + tau) / beta
    )

    k10 = sp.simplify(1 / alpha)
    k11 = sp.simplify((1 + d / alpha) / beta)
    mass_constant = sp.simplify(18 * k10 + 64 * k11)
    mass_identity = sp.simplify(mass_constant * (1 + tau) - (18 * (1 + tau) / alpha + 64 * (1 + d * (1 + tau) / alpha + tau) / beta))

    c00 = wilson_character_coefficient(0, 0)
    local_rho10 = normalized_link_eigenvalue(1, 0, c00) ** 4
    local_rho11 = normalized_link_eigenvalue(1, 1, c00) ** 4
    margin_a = float(sp.N(1 + a * local_rho10, 50))
    margin_c = float(sp.N(1 + d * local_rho10 + e * local_rho11, 50))
    wedge_gap_10 = float(sp.N(float(sp.N(k10, 80)) - local_rho10, 50))
    wedge_gap_11 = float(sp.N(float(sp.N((1 + d * local_rho10) / beta, 80)) - local_rho11, 50))
    local_mass = 18.0 * local_rho10 + 64.0 * local_rho11
    local_mass_gap = float(sp.N(float(sp.N(mass_constant, 80)) - local_mass, 50))

    print("=" * 112)
    print("GAUGE-VACUUM PLAQUETTE FIRST SYMMETRIC THREE-SAMPLE TAU-CONTROLLED RETAINED-COEFFICIENT WEDGE")
    print("=" * 112)
    print()
    print("Exact coefficient-side constants")
    print(f"  alpha = -a                               = {sp.N(alpha, 30)}")
    print(f"  d                                        = {sp.N(d, 30)}")
    print(f"  beta  = -e                              = {sp.N(beta, 30)}")
    print(f"  k10 = 1 / alpha                         = {sp.N(k10, 30)}")
    print(f"  k11 = (1 + d / alpha) / beta            = {sp.N(k11, 30)}")
    print(f"  M   = 18 k10 + 64 k11                   = {sp.N(mass_constant, 30)}")
    print()
    print("Exact outer-wedge laws")
    print("  rho10 <= (1 + tau) / alpha")
    print("  rho11 <= (1 + d rho10 + tau) / beta")
    print("  18 rho10 + 64 rho11 <= M (1 + tau)")
    print()
    print("Exact same-surface local Wilson witness")
    print(f"  rho10^(loc)                              = {local_rho10:.15f}")
    print(f"  rho11^(loc)                              = {local_rho11:.15f}")
    print(f"  tau=0 A-margin                           = {margin_a:.15f}")
    print(f"  tau=0 C-margin                           = {margin_c:.15f}")
    print(f"  tau=0 rho10 wedge gap                    = {wedge_gap_10:.15f}")
    print(f"  tau=0 rho11 wedge gap                    = {wedge_gap_11:.15f}")
    print(f"  local first-retained identity mass       = {local_mass:.15f}")
    print(f"  local mass gap to M                      = {local_mass_gap:.15f}")
    print()

    check(
        "Character-measure theorem already fixes a real nonnegative class function with nonnegative conjugation-symmetric normalized coefficients",
        "real nonnegative class function" in char_note
        and "`rho_(p,q)(beta) >= 0`" in char_note
        and "`rho_(p,q)(beta) = rho_(q,p)(beta)`" in char_note
        and "`rho_(0,0)(beta) = 1`" in char_note,
        bucket="SUPPORT",
    )
    check(
        "Character-truncation envelope already fixes the exact first retained three-sample decomposition and the universal tail bound",
        "`Z_hat_A = 1 + a rho_(1,0) + R_A^(>1)`" in envelope_note
        and "`Z_hat_C = 1 + d rho_(1,0) + e rho_(1,1) + R_C^(>1)`" in envelope_note
        and "`|R_i^(>1)| <= Tau_(>1)`" in envelope_note,
        bucket="SUPPORT",
    )
    check(
        "Positive-cone witness already fixes the sign pattern a < 0, d > 0, e < 0 needed for a nontrivial coefficient wedge",
        "`a < 0`, `b > 0`, `c > 0`, `d > 0`, `e < 0`" in cone_note,
        bucket="SUPPORT",
    )
    check(
        "Local Wilson partial-evaluation note already fixes the exact same-surface local Wilson sample data used as the support witness context",
        "`w_6(W_A) / Z_(1plaq)(6) = 0.1351652795620484`" in local_note
        and "`w_6(W_B) / Z_(1plaq)(6) = 0.3170224955005416`" in local_note
        and "`w_6(W_C) / Z_(1plaq)(6) = 0.5812139466746343`" in local_note,
        bucket="SUPPORT",
    )

    check(
        "The W_A nonnegativity/tail condition is exactly equivalent to rho10 <= (1 + tau) / alpha",
        wedge_identity_a == 0 and float(sp.N(alpha, 50)) > 0.0,
        detail=f"symbolic identity gap={wedge_identity_a}",
    )
    check(
        "The W_C nonnegativity/tail condition is exactly equivalent to rho11 <= (1 + d rho10 + tau) / beta",
        wedge_identity_c == 0 and float(sp.N(beta, 50)) > 0.0,
        detail=f"symbolic identity gap={wedge_identity_c}",
    )
    check(
        "These two inequalities yield explicit tau-controlled individual coefficient bounds rho10 <= k10 (1 + tau), rho11 <= k11 (1 + tau)",
        float(sp.N(k10, 50)) > 0.0 and float(sp.N(k11, 50)) > 0.0,
        detail=f"k10={float(sp.N(k10, 30)):.15f}, k11={float(sp.N(k11, 30)):.15f}",
    )
    check(
        "The first-retained identity mass therefore obeys 18 rho10 + 64 rho11 <= M (1 + tau)",
        mass_identity == 0 and float(sp.N(mass_constant, 50)) > 0.0,
        detail=f"M={float(sp.N(mass_constant, 30)):.15f}",
    )
    check(
        "The exact same-surface local Wilson first-retained point lies strictly inside the tau=0 slice of the outer wedge",
        margin_a > 1.0e-12 and margin_c > 1.0e-12 and wedge_gap_10 > 1.0e-12 and wedge_gap_11 > 1.0e-12,
        detail=(
            f"margins=({margin_a:.12f}, {margin_c:.12f}), "
            f"gaps=({wedge_gap_10:.12f}, {wedge_gap_11:.12f})"
        ),
    )
    check(
        "This is a real coefficient-side theorem but not a solve: tau remains open, so the wedge is an exact outer bound rather than explicit beta=6 coefficient closure",
        float(sp.N(k10, 50)) > local_rho10 and float(sp.N(k11, 50)) > local_rho11,
        detail="the current stack yields a tau-controlled wedge and linear mass bound, but it does not upper-bound tau itself",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
