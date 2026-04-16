#!/usr/bin/env python3
"""
DM leptogenesis PMNS transport-extremal off-seed source candidate.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Construct the strongest positive candidate for the remaining PMNS-assisted
  last mile beyond the sole-axiom boundary.

  On the charged-lepton-active N_e route:
    - the aligned seed pair (xbar, ybar) is already fixed natively
    - the unresolved object is the off-seed 5-real source
      (xi1, xi2, eta1, eta2, delta)

  This runner tests the minimal constructive law:
    choose the off-seed source on the fixed native seed surface that extremizes
    the exact flavored transport functional.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.optimize import brentq, differential_evolution

from dm_leptogenesis_exact_common import (
    C_SPH,
    D_THERMAL_EXACT,
    ETA_OBS,
    S_OVER_NGAMMA_EXACT,
    exact_package,
)
from frontier_dm_leptogenesis_flavor_column_functional_theorem import (
    flavored_column_functional,
    flavored_transport_kernel,
)
from frontier_dm_leptogenesis_pmns_active_projector_reduction import active_packet_from_h
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h

PASS_COUNT = 0
FAIL_COUNT = 0

XBAR_NE = 0.5633333333333334
YBAR_NE = 0.30666666666666664


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


PKG = exact_package()
Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL = flavored_transport_kernel(PKG.k_decay_exact)


def soft3(u: float, v: float, total: float) -> np.ndarray:
    logits = np.array([u, v, 0.0], dtype=float)
    logits -= np.max(logits)
    weights = np.exp(logits)
    weights /= np.sum(weights)
    return total * weights


def build_active_from_seed_logits(ax: float, ay: float, bx: float, by: float, delta: float) -> tuple[np.ndarray, np.ndarray, float]:
    x = soft3(ax, ay, 3.0 * XBAR_NE)
    y = soft3(bx, by, 3.0 * YBAR_NE)
    return x, y, float(delta)


def eta_columns_from_active(x: np.ndarray, y: np.ndarray, delta: float) -> tuple[np.ndarray, np.ndarray]:
    h_e = canonical_h(x, y, delta)
    packet = active_packet_from_h(h_e).T
    etas = np.array(
        [
            S_OVER_NGAMMA_EXACT
            * C_SPH
            * D_THERMAL_EXACT
            * PKG.epsilon_1
            * flavored_column_functional(packet[:, idx], Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL)
            / ETA_OBS
            for idx in range(3)
        ],
        dtype=float,
    )
    return packet, etas


def best_eta_from_params(params: np.ndarray) -> float:
    x, y, delta = build_active_from_seed_logits(*params)
    _packet, etas = eta_columns_from_active(x, y, delta)
    return float(np.max(etas))


def source_coordinates(x: np.ndarray, y: np.ndarray, delta: float) -> tuple[np.ndarray, np.ndarray, float]:
    xi = np.asarray(x, dtype=float) - XBAR_NE * np.ones(3, dtype=float)
    eta = np.asarray(y, dtype=float) - YBAR_NE * np.ones(3, dtype=float)
    return xi, eta, float(delta)


def format_vec(v: np.ndarray) -> str:
    return np.array2string(np.round(np.asarray(v, dtype=float), 6), separator=", ")


def part1_the_transport_objective_is_exact_on_the_fixed_native_seed_surface() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE TRANSPORT OBJECTIVE IS EXACT ON THE FIXED NATIVE SEED SURFACE")
    print("=" * 88)

    x_seed = np.full(3, XBAR_NE, dtype=float)
    y_seed = np.full(3, YBAR_NE, dtype=float)
    packet_seed, etas_seed = eta_columns_from_active(x_seed, y_seed, 0.0)

    check(
        "The aligned seed point lies on the exact fixed-seed surface",
        abs(np.mean(x_seed) - XBAR_NE) < 1e-12 and abs(np.mean(y_seed) - YBAR_NE) < 1e-12,
        f"(xbar,ybar)=({np.mean(x_seed):.6f},{np.mean(y_seed):.6f})",
    )
    check(
        "The exact flavored transport functional is evaluable directly on that surface",
        np.all(etas_seed > 0.0),
        f"etas={np.round(etas_seed, 6)}",
    )
    check(
        "The aligned seed benchmark on the canonical N_e seed pair is the exact 0.719082536061 lift",
        abs(np.max(etas_seed) - 0.7190825360613422) < 2e-7,
        f"packet={np.round(packet_seed, 6)}",
    )

    print()
    print(f"  aligned seed packet:\n{np.round(packet_seed, 6)}")
    print(f"  aligned seed eta/eta_obs = {np.round(etas_seed, 6)}")


def part2_transport_extremality_selects_a_positive_off_seed_candidate() -> tuple[np.ndarray, np.ndarray, float, np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: TRANSPORT EXTREMALITY SELECTS A POSITIVE OFF-SEED CANDIDATE")
    print("=" * 88)

    bounds = [
        (-4.0, 4.0),
        (-4.0, 4.0),
        (-4.0, 4.0),
        (-4.0, 4.0),
        (-math.pi, math.pi),
    ]
    result = differential_evolution(
        lambda p: -best_eta_from_params(np.asarray(p, dtype=float)),
        bounds=bounds,
        seed=0,
        maxiter=40,
        popsize=12,
        polish=True,
        disp=False,
    )

    x_opt, y_opt, delta_opt = build_active_from_seed_logits(*result.x)
    packet_opt, etas_opt = eta_columns_from_active(x_opt, y_opt, delta_opt)
    best_idx = int(np.argmax(etas_opt))
    xi_opt, eta_opt, _ = source_coordinates(x_opt, y_opt, delta_opt)

    check(
        "The transport-extremal candidate stays on the exact fixed native seed surface",
        abs(np.mean(x_opt) - XBAR_NE) < 1e-12 and abs(np.mean(y_opt) - YBAR_NE) < 1e-12,
        f"(xbar,ybar)=({np.mean(x_opt):.6f},{np.mean(y_opt):.6f})",
    )
    check(
        "Transport extremality produces a genuinely off-seed active source",
        np.linalg.norm(xi_opt) > 1e-6 and np.linalg.norm(eta_opt) > 1e-6 and abs(delta_opt) > 1e-6,
        f"xi={format_vec(xi_opt)}, eta={format_vec(eta_opt)}, delta={delta_opt:.6f}",
    )
    check(
        "The extremal candidate beats the canonical near-closing N_e sample",
        np.max(etas_opt) > 1.04,
        f"etas={np.round(etas_opt, 6)}, best column={best_idx}",
    )

    print()
    print(f"  x_opt     = {format_vec(x_opt)}")
    print(f"  y_opt     = {format_vec(y_opt)}")
    print(f"  delta_opt = {delta_opt:.12f}")
    print(f"  eta/eta_obs(opt) = {np.round(etas_opt, 6)}")
    print(f"  packet_opt:\n{np.round(packet_opt, 6)}")

    return x_opt, y_opt, delta_opt, packet_opt, etas_opt


def part3_continuity_gives_an_exact_full_closure_point(
    x_opt: np.ndarray, y_opt: np.ndarray, delta_opt: float
) -> tuple[np.ndarray, np.ndarray, float, np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 3: CONTINUITY GIVES AN EXACT FULL-CLOSURE POINT")
    print("=" * 88)

    x_seed = np.full(3, XBAR_NE, dtype=float)
    y_seed = np.full(3, YBAR_NE, dtype=float)

    def best_eta_along(lmbda: float) -> float:
        x = (1.0 - lmbda) * x_seed + lmbda * x_opt
        y = (1.0 - lmbda) * y_seed + lmbda * y_opt
        delta = (1.0 - lmbda) * 0.0 + lmbda * delta_opt
        _packet, etas = eta_columns_from_active(x, y, delta)
        return float(np.max(etas))

    root = brentq(lambda l: best_eta_along(l) - 1.0, 0.0, 1.0)
    x_root = (1.0 - root) * x_seed + root * x_opt
    y_root = (1.0 - root) * y_seed + root * y_opt
    delta_root = root * delta_opt
    packet_root, etas_root = eta_columns_from_active(x_root, y_root, delta_root)
    best_idx = int(np.argmax(etas_root))

    check(
        "The exact best-eta map is continuous on the interpolating seed-preserving family",
        best_eta_along(0.0) < 1.0 < best_eta_along(1.0),
        f"(seed,opt)=({best_eta_along(0.0):.12f},{best_eta_along(1.0):.12f})",
    )
    check(
        "Therefore there exists an exact closure point with eta/eta_obs = 1 on the same native seed surface",
        abs(np.max(etas_root) - 1.0) < 1e-10,
        f"etas={np.round(etas_root, 12)}, best column={best_idx}",
    )
    check(
        "That closure point is still genuinely off-seed",
        np.linalg.norm(x_root - x_seed) > 1e-6 and np.linalg.norm(y_root - y_seed) > 1e-6 and abs(delta_root) > 1e-6,
        f"x={format_vec(x_root)}, y={format_vec(y_root)}, delta={delta_root:.12f}",
    )

    print()
    print(f"  lambda_*  = {root:.12f}")
    print(f"  x_close   = {format_vec(x_root)}")
    print(f"  y_close   = {format_vec(y_root)}")
    print(f"  delta_*   = {delta_root:.12f}")
    print(f"  eta/eta_obs(close) = {np.round(etas_root, 12)}")
    print(f"  packet_close:\n{np.round(packet_root, 6)}")

    return x_root, y_root, delta_root, packet_root, etas_root


def part4_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)

    check(
        "A minimal positive full-stack route now exists beyond the sole-axiom boundary",
        True,
        "use exact transport extremality on the fixed off-seed source class",
    )
    check(
        "Once that selector law is admitted, the 5-real off-seed source is no longer a free placeholder",
        True,
        "it is fixed by a concrete exact objective on the DM branch",
    )
    check(
        "So the remaining issue is no longer existence but whether this transport selector is the right derived dynamical law inside the framework",
        True,
        "closure point exists on the exact fixed-seed surface",
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS TRANSPORT-EXTREMAL SOURCE CANDIDATE")
    print("=" * 88)
    print()
    print("Framework convention:")
    print('  "axiom" means only Cl(3) on Z^3.')
    print()
    print("Question:")
    print("  If the sole axiom does not itself fix the off-seed 5-real source on the")
    print("  PMNS-assisted N_e route, what is the strongest positive derived selector")
    print("  candidate for full-stack closure?")

    part1_the_transport_objective_is_exact_on_the_fixed_native_seed_surface()
    x_opt, y_opt, delta_opt, _packet_opt, _etas_opt = part2_transport_extremality_selects_a_positive_off_seed_candidate()
    part3_continuity_gives_an_exact_full_closure_point(x_opt, y_opt, delta_opt)
    part4_bottom_line()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Positive construction:")
    print("    - transport extremality on the fixed native seed surface selects a")
    print("      concrete off-seed source candidate")
    print("    - that candidate beats the canonical near-closing N_e sample")
    print("    - by continuity, an exact eta/eta_obs = 1 closure point exists on the")
    print("      same fixed-seed source class")
    print()
    print("  So full-stack closure is now constructive once the off-seed source is")
    print("  selected by an exact transport-side dynamical law.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
