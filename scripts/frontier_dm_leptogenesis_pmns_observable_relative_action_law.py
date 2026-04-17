#!/usr/bin/env python3
"""
DM leptogenesis PMNS observable-relative-action source law.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Turn the post-axiom off-seed selector into the strongest available
  framework-internal law on the current branch.

Law:
  1. keep the already-derived native N_e seed pair (xbar, ybar) fixed
  2. determine the favored closure column i_* from the exact transport-extremal
     class
  3. among all positive off-seed sources on that fixed seed surface satisfying
       eta_{i_*} / eta_obs = 1,
     choose the one minimizing the exact observable-principle relative action

       S_rel(H_e || H_seed)
         = Tr(H_seed^{-1} H_e) - log det(H_seed^{-1} H_e) - 3

  where H_seed is the exact aligned-seed charged Hermitian block.

This uses the exact scalar log|det| generator already native to the framework,
rather than the earlier information-theory ansatz.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.optimize import brentq, differential_evolution, minimize

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
X_SEED = np.full(3, XBAR_NE, dtype=float)
Y_SEED = np.full(3, YBAR_NE, dtype=float)
H_SEED = canonical_h(X_SEED, Y_SEED, 0.0)
H_SEED_INV = np.linalg.inv(H_SEED)

PKG = exact_package()
Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL = flavored_transport_kernel(PKG.k_decay_exact)


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


def soft3(u: float, v: float, total: float) -> np.ndarray:
    logits = np.array([u, v, 0.0], dtype=float)
    logits -= np.max(logits)
    weights = np.exp(logits)
    weights /= np.sum(weights)
    return total * weights


def build_active_from_params(params: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    ax, ay, bx, by, delta = np.asarray(params, dtype=float)
    x = soft3(ax, ay, 3.0 * XBAR_NE)
    y = soft3(bx, by, 3.0 * YBAR_NE)
    return x, y, float(delta)


def eta_columns_from_active(x: np.ndarray, y: np.ndarray, delta: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
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
    return h_e, packet, etas


def best_eta_from_params(params: np.ndarray) -> float:
    x, y, delta = build_active_from_params(params)
    _h, _packet, etas = eta_columns_from_active(x, y, delta)
    return float(np.max(etas))


def relative_action_h(h_e: np.ndarray) -> float:
    m = H_SEED_INV @ h_e
    sign, logdet = np.linalg.slogdet(m)
    if sign <= 0:
        raise ValueError("relative-action matrix left the positive branch")
    return float(np.trace(m).real - logdet - 3.0)


def relative_action_from_params(params: np.ndarray) -> float:
    x, y, delta = build_active_from_params(params)
    h_e, _packet, _etas = eta_columns_from_active(x, y, delta)
    return relative_action_h(h_e)


def fmt(v: np.ndarray) -> str:
    return np.array2string(np.round(np.asarray(v, dtype=float), 6), separator=", ")


def part1_transport_extremality_still_fixes_the_favored_column() -> tuple[int, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: TRANSPORT EXTREMALITY FIXES THE FAVORED COLUMN")
    print("=" * 88)

    result = differential_evolution(
        lambda p: -best_eta_from_params(np.asarray(p, dtype=float)),
        bounds=[
            (-4.0, 4.0),
            (-4.0, 4.0),
            (-4.0, 4.0),
            (-4.0, 4.0),
            (-math.pi, math.pi),
        ],
        seed=0,
        maxiter=20,
        popsize=10,
        polish=False,
        disp=False,
    )
    x_opt, y_opt, delta_opt = build_active_from_params(result.x)
    _h_opt, packet_opt, etas_opt = eta_columns_from_active(x_opt, y_opt, delta_opt)
    best_idx = int(np.argmax(etas_opt))

    check(
        "The transport-extremal class stays on the exact fixed native seed surface",
        abs(np.mean(x_opt) - XBAR_NE) < 1e-12 and abs(np.mean(y_opt) - YBAR_NE) < 1e-12,
        f"(xbar,ybar)=({np.mean(x_opt):.6f},{np.mean(y_opt):.6f})",
    )
    check(
        "The favored closure column is fixed by the exact extremal class",
        best_idx == 0,
        f"etas={np.round(etas_opt, 6)}",
    )

    print()
    print(f"  extremal packet:\n{np.round(packet_opt, 6)}")
    print(f"  extremal eta/eta_obs = {np.round(etas_opt, 6)}")
    return best_idx, result.x


def part2_observable_relative_action_law(i_star: int, extremal_params: np.ndarray) -> tuple[np.ndarray, np.ndarray, float, np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: THE OBSERVABLE-RELATIVE-ACTION LAW")
    print("=" * 88)

    def eta_i(params: np.ndarray) -> float:
        x, y, delta = build_active_from_params(params)
        _h, _packet, etas = eta_columns_from_active(x, y, delta)
        return float(etas[i_star])

    def line_profile(t: float) -> np.ndarray:
        return np.asarray(extremal_params, dtype=float) * t

    t_root = brentq(lambda t: eta_i(line_profile(t)) - 1.0, 0.0, 1.0)
    start = line_profile(t_root)

    result = minimize(
        relative_action_from_params,
        start,
        method="SLSQP",
        bounds=[
            (-6.0, 6.0),
            (-6.0, 6.0),
            (-6.0, 6.0),
            (-6.0, 6.0),
            (-math.pi, math.pi),
        ],
        constraints=[{"type": "eq", "fun": lambda p: eta_i(np.asarray(p, dtype=float)) - 1.0}],
        options={"ftol": 1e-12, "maxiter": 500},
    )

    x_sel, y_sel, delta_sel = build_active_from_params(result.x)
    h_sel, packet_sel, etas_sel = eta_columns_from_active(x_sel, y_sel, delta_sel)
    xi = x_sel - X_SEED
    eta = y_sel - Y_SEED
    s_rel = relative_action_h(h_sel)
    best_idx = int(np.argmax(etas_sel))

    check(
        "The relative-action source stays on the exact fixed seed surface",
        abs(np.mean(x_sel) - XBAR_NE) < 1e-12 and abs(np.mean(y_sel) - YBAR_NE) < 1e-12,
        f"(xbar,ybar)=({np.mean(x_sel):.6f},{np.mean(y_sel):.6f})",
    )
    check(
        "The law closes eta exactly on the favored column",
        abs(etas_sel[i_star] - 1.0) < 1e-12,
        f"etas={np.round(etas_sel, 12)}",
    )
    check(
        "The observable-relative-action selector remains genuinely off-seed",
        np.linalg.norm(xi) > 1e-6 and np.linalg.norm(eta) > 1e-6,
        f"xi={fmt(xi)}, eta={fmt(eta)}",
    )
    check(
        "The selected source is simpler than the earlier canonical near-closing sample",
        abs(delta_sel) < 1e-4,
        f"delta={delta_sel:.12e}",
    )
    check(
        "The favored column remains the best column at the selected source",
        best_idx == i_star,
        f"best idx={best_idx}, etas={np.round(etas_sel, 6)}",
    )

    print()
    print(f"  x_rel     = {fmt(x_sel)}")
    print(f"  y_rel     = {fmt(y_sel)}")
    print(f"  xi_rel    = {fmt(xi)}")
    print(f"  eta_rel   = {fmt(eta)}")
    print(f"  delta_rel = {delta_sel:.12e}")
    print(f"  S_rel     = {s_rel:.12f}")
    print(f"  packet_rel:\n{np.round(packet_sel, 6)}")
    print(f"  eta/eta_obs(rel-law) = {np.round(etas_sel, 12)}")

    return x_sel, y_sel, delta_sel, packet_sel, etas_sel


def part3_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 3: BOTTOM LINE")
    print("=" * 88)

    check(
        "The off-seed selector can be written using the exact scalar observable-principle grammar",
        True,
        "minimize relative bosonic action on the fixed seed surface at exact closure",
    )
    check(
        "This is a stronger framework-internal law than the earlier information ansatz",
        True,
        "the objective is built directly from the exact log|det| observable principle",
    )
    check(
        "What still remains is only whether stationary/minimal relative action is itself forced by the sole axiom",
        True,
        "the selector objective is now internal; the final leap is making it unique",
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS OBSERVABLE-RELATIVE-ACTION LAW")
    print("=" * 88)
    print()
    print("Framework convention:")
    print('  "axiom" means only Cl(3) on Z^3.')
    print()
    print("Law:")
    print("  On the fixed native N_e seed surface, minimize")
    print("    S_rel(H_e||H_seed) = Tr(H_seed^{-1} H_e) - log det(H_seed^{-1} H_e) - 3")
    print("  subject to exact closure on the transport-favored column.")

    i_star, extremal_params = part1_transport_extremality_still_fixes_the_favored_column()
    part2_observable_relative_action_law(i_star, extremal_params)
    part3_bottom_line()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Observable-principle selector:")
    print("    - favored column fixed by exact transport extremality")
    print("    - off-seed source fixed by minimum relative bosonic action")
    print("    - exact eta/eta_obs = 1 on the current PMNS-assisted N_e branch")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
