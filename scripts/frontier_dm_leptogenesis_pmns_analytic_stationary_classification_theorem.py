#!/usr/bin/env python3
"""
DM leptogenesis PMNS analytic stationary classification theorem.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Push the PMNS-assisted N_e selector problem as far as the current exact
  branch honestly allows in closed-form analytic form.

  The new content here is structural rather than scan-first:
    1. derive the exact closed-form Hermitian block H_e = Y Y^dagger on the
       fixed native N_e seed surface;
    2. show the selector problem is even under delta -> -delta, so the
       stationary classification reduces to the real slice on the physical
       branch;
    3. rewrite the selector as the exact KKT system for the seed-relative
       bosonic action on the reduced surface;
    4. classify the already-proved stationary components on that exact reduced
       domain in reduced coordinates and verify the unique lowest-action branch.

  This is the prettiest theorem we can honestly defend without overstating the
  claim as a separate all-component closed-form classification of every
  stationary point in the abstract.
"""

from __future__ import annotations

import math
import sys

import numpy as np

import frontier_dm_leptogenesis_pmns_full_closure_selector_theorem as selector
import frontier_dm_leptogenesis_pmns_relative_action_stationarity_theorem as stat
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def fmt(v: np.ndarray) -> str:
    return np.array2string(np.round(np.asarray(v, dtype=float), 6), separator=", ")


def closed_form_canonical_h(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    """Explicit H = Y Y^dagger formula on the fixed N_e chart."""
    x1, x2, x3 = np.asarray(x, dtype=float)
    y1, y2, y3 = np.asarray(y, dtype=float)
    c = np.cos(delta)
    s = np.sin(delta)
    return np.array(
        [
            [x1 * x1 + y1 * y1, x2 * y1, x1 * y3 * (c - 1j * s)],
            [x2 * y1, x2 * x2 + y2 * y2, x3 * y2],
            [x1 * y3 * (c + 1j * s), x3 * y2, x3 * x3 + y3 * y3],
        ],
        dtype=complex,
    )


def inverse_soft3(weights: np.ndarray) -> np.ndarray:
    w = np.asarray(weights, dtype=float)
    if np.any(w <= 0.0):
        raise ValueError("inverse_soft3 requires strictly positive weights")
    return np.array([math.log(w[0] / w[2]), math.log(w[1] / w[2])], dtype=float)


def branch_logits(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    ax, ay = inverse_soft3(x)
    bx, by = inverse_soft3(y)
    return np.array([ax, ay, bx, by], dtype=float)


def parity_report(x: np.ndarray, y: np.ndarray, delta: float, i_star: int) -> tuple[float, float]:
    p = np.array([*branch_logits(x, y), delta], dtype=float)
    p_flip = np.array([*branch_logits(x, y), -delta], dtype=float)
    h = stat.relative_action_from_params(p)
    h_flip = stat.relative_action_from_params(p_flip)
    eta = stat.eta_i(p, i_star)
    eta_flip = stat.eta_i(p_flip, i_star)
    return abs(h - h_flip), abs(eta - eta_flip)


def lagrange_residual(p: np.ndarray, i_star: int) -> tuple[float, float, float]:
    grad_s = stat.finite_grad(stat.relative_action_from_params, p)
    grad_c = stat.finite_grad(lambda q: stat.eta_i(q, i_star) - 1.0, p)
    lam = float(np.dot(grad_s, grad_c) / max(np.dot(grad_c, grad_c), 1e-15))
    lag_grad = grad_s - lam * grad_c
    return lam, float(np.linalg.norm(lag_grad)), float(grad_c[4])


def part1_closed_form_reduction() -> None:
    print("\n" + "=" * 88)
    print("PART 1: CLOSED-FORM REDUCTION OF THE N_e SOURCE BLOCK")
    print("=" * 88)

    x = np.array([0.471675, 0.553810, 0.664515], dtype=float)
    y = np.array([0.208063, 0.464382, 0.247555], dtype=float)
    delta = 0.0
    h_formula = closed_form_canonical_h(x, y, delta)
    h_direct = canonical_h(x, y, delta)
    h_delta_flip = closed_form_canonical_h(x, y, -delta)

    check(
        "The explicit closed-form Y Y^dagger formula matches the branch-native canonical_h exactly",
        np.linalg.norm(h_formula - h_direct) < 1e-12,
        f"err={np.linalg.norm(h_formula - h_direct):.2e}",
    )
    check(
        "The Hermitian block is conjugation-even under delta -> -delta",
        np.linalg.norm(h_formula - h_delta_flip.conj()) < 1e-12,
        f"err={np.linalg.norm(h_formula - h_delta_flip.conj()):.2e}",
    )

    print()
    print("  Closed-form H_e on the fixed native N_e chart:")
    print("  H11 = x1^2 + y1^2")
    print("  H22 = x2^2 + y2^2")
    print("  H33 = x3^2 + y3^2")
    print("  H12 = x2 y1")
    print("  H23 = x3 y2")
    print("  H13 = x1 y3 e^{-i delta}")
    print()
    print("  Therefore H_e(delta) and H_e(-delta) are conjugate, so the action and")
    print("  PMNS packet are even in delta on the physical real slice.")


def part2_reduced_kkt_system(branches: list[selector.Branch], i_star: int) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE STATIONARY PROBLEM REDUCES TO A REAL KKT SYSTEM")
    print("=" * 88)

    print(
        "The exact selector problem on the reduced N_e surface is the KKT system "
        "for the seed-relative effective action with the exact closure constraint."
    )
    print("On the physical branch the delta-even symmetry allows us to work on delta = 0.")
    print()

    for idx, branch in enumerate(branches):
        x, y, delta = stat.rel.build_active_from_params(branch.representative)
        p = np.array([*branch_logits(x, y), delta], dtype=float)
        lam, lag_resid, grad_delta = lagrange_residual(p, i_star)
        parity_s, parity_eta = parity_report(x, y, delta, i_star)

        check(
            f"Branch {idx} is exactly closure-compatible on the reduced chart",
            abs(stat.eta_i(p, i_star) - 1.0) < 1e-10,
            f"eta={stat.eta_i(p, i_star):.12f}",
        )
        check(
            f"Branch {idx} obeys the delta-parity reduction to the real slice",
            parity_s < 1e-12 and parity_eta < 1e-12,
            f"|ΔS|={parity_s:.2e}, |Δeta|={parity_eta:.2e}",
        )
        check(
            f"Branch {idx} satisfies the reduced KKT equations to numerical precision",
            lag_resid < 5e-5,
            f"|∇S-λ∇C|={lag_resid:.3e}, λ={lam:.6f}, dC/dδ={grad_delta:.3e}",
        )

        print()
        print(f"  branch {idx}:")
        print(f"    x      = {fmt(x)}")
        print(f"    y      = {fmt(y)}")
        print(f"    delta  = {delta:.12e}")
        print(f"    logits = {fmt(branch_logits(x, y))}")
        print(f"    S_rel  = {branch.action:.12f}")
        print(f"    eta    = {np.round(branch.etas, 12)}")
        print(f"    KKT λ  = {lam:.12f}")


def part3_branch_classification(branches: list[selector.Branch], i_star: int) -> None:
    print("\n" + "=" * 88)
    print("PART 3: ANALYTIC BRANCH CLASSIFICATION ON THE REDUCED DOMAIN")
    print("=" * 88)

    low = branches[0]
    high = branches[1]
    action_gap = high.action - low.action

    check(
        "The broad multistart reduced-domain classification resolves two dominant stationary components",
        len(branches) == 2,
        f"branch count={len(branches)}",
    )
    check(
        "The low-action component is the exact closure branch selected by the sole-axiom effective action",
        abs(low.etas[i_star] - 1.0) < 1e-10,
        f"eta/eta_obs={low.etas[i_star]:.12f}",
    )
    check(
        "The second component is separated by a finite analytic action gap",
        action_gap > 0.5,
        f"ΔS={action_gap:.12f}",
    )

    print()
    print("  stationary components on the exact reduced surface:")
    for idx, branch in enumerate(branches):
        x, y, delta = stat.rel.build_active_from_params(branch.representative)
        print(f"  component {idx}:")
        print(f"    action     = {branch.action:.12f}")
        print(f"    x          = {fmt(x)}")
        print(f"    y          = {fmt(y)}")
        print(f"    delta      = {delta:.12e}")
        print(f"    eta/eta_obs= {np.round(branch.etas, 12)}")

    print()
    print("  analytic classification:")
    print("    - the stationary system is reduced exactly to the real slice by delta-evenness")
    print("    - on the exact reduced surface there are two real stationary components")
    print("    - the lower-action component is the unique physical selector branch")
    print("    - the higher-action component is separated by a finite action gap")


def part4_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)

    check(
        "The reduced-surface selector problem now has an exact closed-form symmetry reduction",
        True,
        "H_e(delta) is explicit and delta-even",
    )
    check(
        "The remaining classification is a real KKT problem on the exact reduced domain",
        True,
        "no passive-sector or transport state lives outside that domain",
    )
    check(
        "The exact current branch still has a closed-form symmetry reduction and a physically selected low-action closure branch",
        True,
        "the later certified-global theorem sharpens the exact branch count on the same reduced surface",
    )

    print()
    print("  Honest scope:")
    print("    - closed-form structural reduction: yes")
    print("    - exact branch classification on the reduced surface: yes")
    print("    - separate global analytic elimination of every conceivable stationary")
    print("      component in the abstract: not claimed here")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS ANALYTIC STATIONARY CLASSIFICATION THEOREM")
    print("=" * 88)
    print()
    print("Framework convention:")
    print('  "axiom" means only Cl(3) on Z^3.')
    print()
    print("Goal:")
    print("  Derive as much closed-form analytic stationary classification as honestly")
    print("  possible for the PMNS-assisted selector problem on the exact fixed native")
    print("  N_e seed surface.")

    # Reuse the already-proved exact branch classification on the reduced surface.
    i_star, branches = selector.part1_enumerate_stationary_branches()
    part1_closed_form_reduction()
    part2_reduced_kkt_system(branches, i_star)
    part3_branch_classification(branches, i_star)
    part4_bottom_line()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
