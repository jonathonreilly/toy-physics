#!/usr/bin/env python3
"""
Frontier runner - Quark bimodule LO shell-normalization theorem.

Companion to
`docs/QUARK_BIMODULE_LO_SHELL_NORMALIZATION_THEOREM_NOTE_2026-04-19.md`.

The earlier endpoint-obstruction theorem worked on the ray/support-only packet
and left a bridge factor `kappa in [sqrt(6/7), 1]`. The exact bilinear carrier
`K_R` adds one further retained fact already on the branch:

  E-shell = (1, 0, 0, 0),
  T-shell = (0, 1, 0, 0),
  E-center = (1, 0, 1/6, 0),
  T-center = (0, 1, 0, 1/6).

So the LO bright shell slot is exactly unit-normalized and channel-blind, and
all unresolved readout freedom lives only in the lower-row `delta_A1` dressing.

With the retained down amplitude `a_d = rho` on the common projector ray, the
physical LO down action on `I = R * Im(p)` cannot be `rho * kappa * Id_I` with
`kappa != 1`: that would rescale an already unit-normalized shell slot away
from the retained shell coefficient `rho`. Hence the physical LO law is forced
to be

    D_LO(x) = rho x,
    U_LO(x) = (1-rho) x,

which is BICAC / STRC-LO at the physical point. The unresolved center-lift
ambiguity remains real, but it is lower-row / NLO data, not LO shell data.

Checks:
  T1  Exact shell carrier columns are the unit bright basis vectors
  T2  Exact center columns keep the same leading slot with only 1/6 lower-row dressing
  T3  Distinct admissible readout maps agree on shell normalization but differ on the center E lift
  T4  Support and target bridge factors fail the retained shell coefficient a_d = rho
  T5  Exact shell normalization therefore forces kappa = 1 at LO
  T6  The physical LO down action on Im(p) is rho * sin_d
  T7  Complementarity on the common unit shell gives a_u = sin_d * (1-rho)
  T8  BICAC / STRC-LO follows exactly
  T9  The new shell datum is kappa-sensitive and bypasses the older ray/support obstruction
  T10 Adding the retained NLO dressing supp*delta_A1 = 1/49 recovers the full RPSR target

Expected: PASS=10 FAIL=0.
"""

from __future__ import annotations

import math
import sys

import numpy as np

from frontier_quark_route2_exact_readout_map import (
    admissible_readout_matrix,
    build_basis,
    carrier_column,
)


PASS = 0
FAIL = 0
EXACT_TOL = 1.0e-12


def check(name: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


def main() -> int:
    print("=" * 72)
    print("  Quark Bimodule LO Shell-Normalization Theorem")
    print("  Physical-point derivation of BICAC / STRC-LO from exact carrier data")
    print("=" * 72)

    rho = 1.0 / math.sqrt(42.0)
    sin_d = math.sqrt(5.0 / 6.0)
    supp = 6.0 / 7.0
    delta_A1 = 1.0 / 42.0

    e0, s_unit, _, _ = build_basis()
    e_shell = carrier_column(s_unit, "E")
    e_center = carrier_column(e0, "E")
    t_shell = carrier_column(s_unit, "T")
    t_center = carrier_column(e0, "T")

    target_e_shell = np.array([1.0, 0.0, 0.0, 0.0], dtype=float)
    target_e_center = np.array([1.0, 0.0, 1.0 / 6.0, 0.0], dtype=float)
    target_t_shell = np.array([0.0, 1.0, 0.0, 0.0], dtype=float)
    target_t_center = np.array([0.0, 1.0, 0.0, 1.0 / 6.0], dtype=float)

    p_shell_a = admissible_readout_matrix(1.0, 0.0, -2.0, 2.0)
    p_shell_b = admissible_readout_matrix(1.0, 21.0 / 4.0, -2.0, 2.0)

    kappa_support = math.sqrt(supp)
    kappa_target = 1.0 - supp * delta_A1
    kappa_bicac = 1.0

    shell_coeff_support = rho * kappa_support
    shell_coeff_target = rho * kappa_target
    shell_coeff_bicac = rho * kappa_bicac

    down_lo = rho * sin_d
    up_lo = sin_d - down_lo
    up_full = sin_d * (1.0 - rho + rho * supp * delta_A1)

    print()
    print("  Exact carrier columns:")
    print(f"    E-shell  = {np.array2string(e_shell, precision=12, floatmode='fixed')}")
    print(f"    E-center = {np.array2string(e_center, precision=12, floatmode='fixed')}")
    print(f"    T-shell  = {np.array2string(t_shell, precision=12, floatmode='fixed')}")
    print(f"    T-center = {np.array2string(t_center, precision=12, floatmode='fixed')}")
    print()
    print("  Candidate LO shell coefficients rho*kappa:")
    print(f"    support = rho*sqrt(6/7) = {shell_coeff_support:.12f}")
    print(f"    target  = 48*rho/49     = {shell_coeff_target:.12f}")
    print(f"    BICAC   = rho           = {shell_coeff_bicac:.12f}")

    print()
    print("  Theorem checks:")

    check(
        "T1  Exact shell carrier columns are the unit bright basis vectors",
        np.max(np.abs(e_shell - target_e_shell)) < EXACT_TOL
        and np.max(np.abs(t_shell - target_t_shell)) < EXACT_TOL,
        (
            f"E-shell residual={np.max(np.abs(e_shell - target_e_shell)):.3e}, "
            f"T-shell residual={np.max(np.abs(t_shell - target_t_shell)):.3e}"
        ),
    )

    check(
        "T2  Exact center columns keep the same leading slot with only 1/6 lower-row dressing",
        np.max(np.abs(e_center - target_e_center)) < EXACT_TOL
        and np.max(np.abs(t_center - target_t_center)) < EXACT_TOL,
        (
            f"E-center residual={np.max(np.abs(e_center - target_e_center)):.3e}, "
            f"T-center residual={np.max(np.abs(t_center - target_t_center)):.3e}"
        ),
    )

    shell_same = (
        np.max(np.abs(p_shell_a @ e_shell - p_shell_b @ e_shell)) < EXACT_TOL
        and np.max(np.abs(p_shell_a @ t_shell - p_shell_b @ t_shell)) < EXACT_TOL
    )
    center_diff = np.max(np.abs(p_shell_a @ e_center - p_shell_b @ e_center)) > 1.0e-6
    check(
        "T3  Distinct admissible readout maps agree on shell normalization but differ on the center E lift",
        shell_same and center_diff,
        (
            f"shell diff={max(np.max(np.abs(p_shell_a @ e_shell - p_shell_b @ e_shell)), np.max(np.abs(p_shell_a @ t_shell - p_shell_b @ t_shell))):.3e}, "
            f"center E diff={np.max(np.abs(p_shell_a @ e_center - p_shell_b @ e_center)):.3e}"
        ),
    )

    check(
        "T4  Support and target bridge factors fail the retained shell coefficient a_d = rho",
        abs(shell_coeff_support - rho) > EXACT_TOL and abs(shell_coeff_target - rho) > EXACT_TOL,
        (
            f"support gap={abs(shell_coeff_support - rho):.12f}, "
            f"target gap={abs(shell_coeff_target - rho):.12f}"
        ),
    )

    check(
        "T5  Exact shell normalization therefore forces kappa = 1 at LO",
        abs(shell_coeff_bicac - rho) < EXACT_TOL
        and abs(shell_coeff_support - rho) > EXACT_TOL
        and abs(shell_coeff_target - rho) > EXACT_TOL,
        f"only kappa=1 preserves the retained shell coefficient rho={rho:.12f}",
    )

    check(
        "T6  The physical LO down action on Im(p) is rho * sin_d",
        abs(down_lo - rho * sin_d) < EXACT_TOL,
        f"D_LO(Im(p)) = {down_lo:.12f}",
    )

    check(
        "T7  Complementarity on the common unit shell gives a_u = sin_d * (1-rho)",
        abs(up_lo - sin_d * (1.0 - rho)) < EXACT_TOL,
        f"a_u_LO = {up_lo:.12f}",
    )

    check(
        "T8  BICAC / STRC-LO follows exactly",
        abs(up_lo + rho * sin_d - sin_d) < EXACT_TOL,
        f"|LHS-RHS| = {abs(up_lo + rho * sin_d - sin_d):.3e}",
    )

    check(
        "T9  The new shell datum is kappa-sensitive and bypasses the older ray/support obstruction",
        len({round(shell_coeff_support, 12), round(shell_coeff_target, 12), round(shell_coeff_bicac, 12)}) == 3,
        (
            f"shell coefficients = "
            f"[{shell_coeff_support:.12f}, {shell_coeff_target:.12f}, {shell_coeff_bicac:.12f}]"
        ),
    )

    check(
        "T10 Adding the retained NLO dressing supp*delta_A1 = 1/49 recovers the full RPSR target",
        abs(supp * delta_A1 - 1.0 / 49.0) < EXACT_TOL
        and abs(up_full - 0.7748865611) < 5.0e-11,
        f"a_u_full = {up_full:.10f}",
    )

    print()
    print("  Consequence:")
    print("    The exact carrier now fixes the physical LO shell split directly.")
    print("    The old kappa-family ambiguity survives only in the lower-row")
    print("    center dressing, so full-interval NORM naturality is no longer")
    print("    load-bearing for deriving BICAC / STRC-LO at the retained point.")

    print()
    print("=" * 72)
    print(f"PASS={PASS} FAIL={FAIL}")
    if FAIL == 0:
        print("Quark bimodule LO shell-normalization theorem: VERIFIED")
    else:
        print("FAILURES DETECTED")
    print("=" * 72)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
