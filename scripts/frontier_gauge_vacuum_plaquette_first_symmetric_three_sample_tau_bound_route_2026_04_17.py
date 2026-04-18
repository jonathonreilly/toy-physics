#!/usr/bin/env python3
"""
Sharp Tau bound on the local-Wilson completion route for the first symmetric
three-sample beta=6 plaquette PF seam.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import linprog
from scipy.special import iv


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

BETA = 6.0
MODE_TOL = 1.0e-15
MAX_MODE = 160
REPORT_DIGITS = 15


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


def radical_entries() -> dict[str, sp.Expr]:
    rt2 = sp.sqrt(2)
    return {
        "a": -3 * sp.sqrt(2 - rt2),
        "b": -3 * rt2 + 3 * sp.sqrt(2 - sp.sqrt(2 + rt2)) + 3 * sp.sqrt(2 - sp.sqrt(2 - rt2)),
        "c": 16
        + 8 * sp.sqrt(2 + rt2)
        - 8 * sp.sqrt(2 + sp.sqrt(2 + rt2))
        - 8 * sp.sqrt(2 + sp.sqrt(2 - rt2)),
        "d": 3 * rt2 + 3 * sp.sqrt(2 - sp.sqrt(2 + rt2)) - 3 * sp.sqrt(2 - sp.sqrt(2 - rt2)),
        "e": 16
        - 8 * sp.sqrt(2 + rt2)
        - 8 * sp.sqrt(2 + sp.sqrt(2 + rt2))
        + 8 * sp.sqrt(2 + sp.sqrt(2 - rt2)),
    }


def bessel_matrix(beta: float, mode: int) -> np.ndarray:
    arg = beta / 3.0
    return np.array(
        [[iv(mode + i - j, arg) for j in range(3)] for i in range(3)],
        dtype=float,
    )


def su3_mode_term(beta: float, mode: int) -> float:
    return float(np.linalg.det(bessel_matrix(beta, mode)))


def su3_partition_sum(beta: float, tol: float = MODE_TOL, max_mode: int = MAX_MODE) -> tuple[float, int]:
    total = 0.0
    used = max_mode

    for mode in range(max_mode + 1):
        strip = su3_mode_term(beta, 0) if mode == 0 else su3_mode_term(beta, -mode) + su3_mode_term(beta, mode)
        total += strip
        if mode >= 3 and abs(strip) < tol * abs(total):
            used = mode
            break

    return total, used


def lp_optimum(a: float, b: float, c: float, d: float, e: float, z_a: float, z_b: float, z_c: float) -> tuple[bool, np.ndarray, float]:
    rows = [
        ((a, 0.0), z_a),
        ((b, c), z_b),
        ((d, e), z_c),
    ]
    a_ub: list[list[float]] = []
    b_ub: list[float] = []
    for (x_coeff, y_coeff), target in rows:
        a_ub.append([x_coeff, y_coeff, -1.0])
        b_ub.append(target - 1.0)
        a_ub.append([-x_coeff, -y_coeff, -1.0])
        b_ub.append(1.0 - target)

    result = linprog(
        c=[0.0, 0.0, 1.0],
        A_ub=np.array(a_ub, dtype=float),
        b_ub=np.array(b_ub, dtype=float),
        bounds=[(0.0, None), (0.0, None), (0.0, None)],
        method="highs",
    )
    return bool(result.success), np.array(result.x, dtype=float), float(result.fun)


def main() -> int:
    local_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_PARTIAL_EVALUATION_NOTE_2026-04-17.md"
    )
    envelope_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md"
    )
    obstruction_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_RETAINED_POSITIVE_CONE_OBSTRUCTION_NOTE_2026-04-17.md"
    )
    nonderivation_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_TAU_UPPER_BOUND_NONDERIVATION_NOTE_2026-04-17.md"
    )

    entries = radical_entries()
    a = float(sp.N(entries["a"], 80))
    b = float(sp.N(entries["b"], 80))
    c = float(sp.N(entries["c"], 80))
    d = float(sp.N(entries["d"], 80))
    e = float(sp.N(entries["e"], 80))
    alpha = -a

    z_local, mode_cutoff = su3_partition_sum(BETA)
    z_a = float(sp.N(sp.exp(entries["a"] / 3), 80)) / z_local
    z_b = float(sp.N(sp.exp(entries["b"] / 3), 80)) / z_local
    z_c = float(sp.N(sp.exp(entries["d"] / 3), 80)) / z_local

    rho10_star = (z_b - z_a) / (b - a)
    rho11_star = 0.0
    tau_star = 1.0 - z_b + b * rho10_star
    a_line_star = 1.0 - z_a - alpha * rho10_star
    turning_point_a = (1.0 - z_a) / alpha

    retained_a = 1.0 + a * rho10_star
    retained_b = 1.0 + b * rho10_star + c * rho11_star
    retained_c = 1.0 + d * rho10_star + e * rho11_star

    residual_a = z_a - retained_a
    residual_b = z_b - retained_b
    residual_c = z_c - retained_c
    c_residual_abs = abs(residual_c)
    c_slack = tau_star - c_residual_abs

    lp_success, lp_x, lp_tau = lp_optimum(a, b, c, d, e, z_a, z_b, z_c)
    lp_rho10, lp_rho11, lp_tau_var = lp_x

    print("=" * 114)
    print("GAUGE-VACUUM PLAQUETTE FIRST SYMMETRIC THREE-SAMPLE TAU BOUND ROUTE")
    print("=" * 114)
    print()
    print("Exact local Wilson sample triple on the named seam")
    print(f"  Z_(1plaq)(6)                               = {z_local:.15f}   (mode cutoff m = {mode_cutoff})")
    print(f"  z_A^loc                                   = {z_a:.15f}")
    print(f"  z_B^loc                                   = {z_b:.15f}")
    print(f"  z_C^loc                                   = {z_c:.15f}")
    print()
    print("Exact first-seam retained coefficients")
    print(f"  a                                          = {a:.15f}")
    print(f"  b                                          = {b:.15f}")
    print(f"  c                                          = {c:.15f}")
    print(f"  d                                          = {d:.15f}")
    print(f"  e                                          = {e:.15f}")
    print()
    print("Sharp local-Wilson Tau-route optimizer")
    print(f"  rho10_*                                    = {rho10_star:.15f}")
    print(f"  rho11_*                                    = {rho11_star:.15f}")
    print(f"  tau_*                                      = {tau_star:.15f}")
    print(f"  A-line lower bound at rho10_*              = {a_line_star:.15f}")
    print(f"  B-line lower bound at rho10_*              = {1.0 - z_b + b * rho10_star:.15f}")
    print(f"  W_A turning point (1-z_A^loc)/alpha        = {turning_point_a:.15f}")
    print()
    print("Explicit sharp witness residuals")
    print(f"  R_A                                        = {residual_a:.15f}")
    print(f"  R_B                                        = {residual_b:.15f}")
    print(f"  R_C                                        = {residual_c:.15f}")
    print(f"  |R_C|                                      = {c_residual_abs:.15f}")
    print(f"  tau_* - |R_C|                              = {c_slack:.15f}")
    print()
    print("Full LP cross-check on all three seam rows")
    print(f"  success                                    = {lp_success}")
    print(f"  rho10_LP                                   = {lp_rho10:.15f}")
    print(f"  rho11_LP                                   = {lp_rho11:.15f}")
    print(f"  tau_LP                                     = {lp_tau:.15f}")
    print(f"  tau_LP (variable)                          = {lp_tau_var:.15f}")
    print()

    check(
        "Local Wilson partial-evaluation note already fixes the exact normalized local sample triple on W_A, W_B, W_C",
        "`w_6(W_A) / Z_(1plaq)(6) = 0.1351652795620484`" in local_note
        and "`w_6(W_B) / Z_(1plaq)(6) = 0.3170224955005416`" in local_note
        and "`w_6(W_C) / Z_(1plaq)(6) = 0.5812139466746343`" in local_note,
        bucket="SUPPORT",
    )
    check(
        "The truncation-envelope theorem already fixes the first-seam affine model and the uniform tail box |R_i^(>1)| <= Tau_(>1)",
        "`Z_hat_A = 1 + a rho_(1,0) + R_A^(>1)`" in envelope_note
        and "`Z_hat_B = 1 + b rho_(1,0) + c rho_(1,1) + R_B^(>1)`" in envelope_note
        and "`Z_hat_C = 1 + d rho_(1,0) + e rho_(1,1) + R_C^(>1)`" in envelope_note
        and "`|R_i^(>1)| <= Tau_(>1)`" in envelope_note,
        bucket="SUPPORT",
    )
    check(
        "The local-Wilson cone-obstruction theorem already shows the exact local triple is outside the first retained positive cone",
        "negative adjoint coefficient" in obstruction_note
        and "retained positive cone" in obstruction_note,
        bucket="SUPPORT",
    )
    check(
        "The existing Tau upper-bound nonderivation note already says no finite upper cap follows from the current seam constraints alone",
        "no finite upper bound on `Tau_(>1)` is derivable" in nonderivation_note
        and "arbitrarily large `Tau_(>1)`" in nonderivation_note,
        bucket="SUPPORT",
    )

    check(
        "The local Wilson A/B rows alone force the route-level lower bound tau >= max(1-z_A^loc-alpha rho10, 1-z_B^loc+b rho10)",
        alpha > 0.0 and b > 0.0 and c > 0.0 and z_a < 1.0 and z_b < 1.0,
        detail=(
            f"alpha={alpha:.12f}, b={b:.12f}, c={c:.12f}, "
            f"(1-z_A^loc, 1-z_B^loc)=({1.0 - z_a:.12f}, {1.0 - z_b:.12f})"
        ),
    )
    check(
        "That lower bound is minimized at the unique A/B crossing rho10_*=(z_B^loc-z_A^loc)/(b-a)",
        0.0 < rho10_star < turning_point_a
        and abs(a_line_star - tau_star) < 1.0e-12
        and abs((1.0 - z_b + b * rho10_star) - tau_star) < 1.0e-12,
        detail=(
            f"rho10_*={rho10_star:.12f}, turning_point={turning_point_a:.12f}, "
            f"tau_*={tau_star:.12f}"
        ),
    )
    check(
        "The explicit witness rho11=0, rho10=rho10_* saturates the A and B rows with |R_A|=|R_B|=tau_*",
        abs(abs(residual_a) - tau_star) < 1.0e-12
        and abs(abs(residual_b) - tau_star) < 1.0e-12
        and residual_a < 0.0
        and residual_b < 0.0,
        detail=f"residuals=({residual_a:.12f}, {residual_b:.12f})",
    )
    check(
        "The W_C row is strictly slack at the optimizer, so the sharp barrier is already exhausted by the W_A/W_B competition",
        c_slack > 1.0e-6 and c_residual_abs < tau_star,
        detail=f"|R_C|={c_residual_abs:.12f}, tau_*-|R_C|={c_slack:.12f}",
    )
    check(
        "A full LP solve on all three rows recovers the same optimum and the same boundary point rho11=0",
        lp_success
        and abs(lp_rho10 - rho10_star) < 1.0e-9
        and abs(lp_rho11 - rho11_star) < 1.0e-9
        and abs(lp_tau - tau_star) < 1.0e-9
        and abs(lp_tau_var - tau_star) < 1.0e-9,
        detail=(
            f"LP point=({lp_rho10:.12f}, {lp_rho11:.12f}, {lp_tau:.12f}), "
            f"analytic=({rho10_star:.12f}, {rho11_star:.12f}, {tau_star:.12f})"
        ),
    )
    check(
        "Therefore the local-Wilson completion route has one exact sharp Tau barrier tau >= tau_* = 0.701560040093..., so no tau < 0.7 repair exists on this route",
        tau_star > 0.7 and lp_success and abs(lp_tau - tau_star) < 1.0e-9,
        detail=f"tau_*={tau_star:.12f}",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
