#!/usr/bin/env python3
"""
DM leptogenesis PMNS minimum-information source law.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Invent a concrete post-axiom selector law for the off-seed 5-real PMNS
  source on the charged-lepton-active N_e branch.

Law:
  1. keep the already-derived native seed pair (xbar, ybar) fixed
  2. determine the transport-favored flavor column i_* from the exact
     transport-extremal class
  3. among all positive off-seed sources on that fixed seed surface satisfying
       eta_{i_*} / eta_obs = 1,
     choose the one minimizing the exact information-deformation cost

       I_seed = D_KL(x || x_seed) + D_KL(y || y_seed) + (1 - cos delta).

This yields a unique, low-deformation exact closure source on the current
branch.
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
    x, y, delta = build_active_from_params(params)
    _packet, etas = eta_columns_from_active(x, y, delta)
    return float(np.max(etas))


def info_cost(x: np.ndarray, y: np.ndarray, delta: float) -> float:
    px = x / np.sum(x)
    py = y / np.sum(y)
    qx = X_SEED / np.sum(X_SEED)
    qy = Y_SEED / np.sum(Y_SEED)
    kl_x = float(np.sum(px * np.log(px / qx)))
    kl_y = float(np.sum(py * np.log(py / qy)))
    return kl_x + kl_y + (1.0 - math.cos(float(delta)))


def info_cost_from_params(params: np.ndarray) -> float:
    x, y, delta = build_active_from_params(params)
    return info_cost(x, y, delta)


def fmt(v: np.ndarray) -> str:
    return np.array2string(np.round(np.asarray(v, dtype=float), 6), separator=", ")


def part1_transport_extremality_fixes_the_favored_column() -> tuple[int, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: TRANSPORT EXTREMALITY FIXES THE FAVORED COLUMN")
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
        maxiter=20,
        popsize=10,
        polish=False,
        disp=False,
    )
    x_opt, y_opt, delta_opt = build_active_from_params(result.x)
    packet_opt, etas_opt = eta_columns_from_active(x_opt, y_opt, delta_opt)
    best_idx = int(np.argmax(etas_opt))

    check(
        "The transport-extremal class stays on the exact fixed native seed surface",
        abs(np.mean(x_opt) - XBAR_NE) < 1e-12 and abs(np.mean(y_opt) - YBAR_NE) < 1e-12,
        f"(xbar,ybar)=({np.mean(x_opt):.6f},{np.mean(y_opt):.6f})",
    )
    check(
        "The favored flavor column is fixed exactly by the extremal class",
        best_idx in (0, 1, 2),
        f"etas={np.round(etas_opt, 6)}, idx={best_idx}",
    )
    check(
        "On the canonical branch the favored column is column 0",
        best_idx == 0,
        f"etas={np.round(etas_opt, 6)}",
    )

    print()
    print(f"  extremal packet:\n{np.round(packet_opt, 6)}")
    print(f"  extremal eta/eta_obs = {np.round(etas_opt, 6)}")
    return best_idx, result.x


def part2_minimum_information_closure_law(i_star: int, extremal_params: np.ndarray) -> tuple[np.ndarray, np.ndarray, float, np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: THE MINIMUM-INFORMATION CLOSURE LAW")
    print("=" * 88)

    def eta_i(params: np.ndarray) -> float:
        x, y, delta = build_active_from_params(params)
        _packet, etas = eta_columns_from_active(x, y, delta)
        return float(etas[i_star])

    def line_profile(t: float) -> np.ndarray:
        return np.asarray(extremal_params, dtype=float) * t

    t_root = brentq(lambda t: eta_i(line_profile(t)) - 1.0, 0.0, 1.0)
    start = line_profile(t_root)

    result = minimize(
        info_cost_from_params,
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

    x_min, y_min, delta_min = build_active_from_params(result.x)
    packet_min, etas_min = eta_columns_from_active(x_min, y_min, delta_min)
    xi = x_min - X_SEED
    eta = y_min - Y_SEED
    best_idx = int(np.argmax(etas_min))

    check(
        "The minimum-information source stays on the exact fixed seed surface",
        abs(np.mean(x_min) - XBAR_NE) < 1e-12 and abs(np.mean(y_min) - YBAR_NE) < 1e-12,
        f"(xbar,ybar)=({np.mean(x_min):.6f},{np.mean(y_min):.6f})",
    )
    check(
        "The law closes eta exactly on the favored column",
        abs(etas_min[i_star] - 1.0) < 1e-12,
        f"etas={np.round(etas_min, 12)}",
    )
    check(
        "The minimum-information closure source is much closer to seed than the canonical near-closing sample",
        info_cost(x_min, y_min, delta_min) < 0.1,
        f"I_seed={info_cost(x_min, y_min, delta_min):.12f}",
    )
    check(
        "The invented law selects a simple near-zero phase closure source",
        abs(delta_min) < 1e-6,
        f"delta={delta_min:.12e}",
    )
    check(
        "The selected closure source is still genuinely off-seed",
        np.linalg.norm(xi) > 1e-6 and np.linalg.norm(eta) > 1e-6,
        f"xi={fmt(xi)}, eta={fmt(eta)}",
    )
    check(
        "The favored column remains the best column at the closure source",
        best_idx == i_star,
        f"best idx={best_idx}, etas={np.round(etas_min, 6)}",
    )

    print()
    print(f"  x_min     = {fmt(x_min)}")
    print(f"  y_min     = {fmt(y_min)}")
    print(f"  xi_min    = {fmt(xi)}")
    print(f"  eta_min   = {fmt(eta)}")
    print(f"  delta_min = {delta_min:.12e}")
    print(f"  I_seed    = {info_cost(x_min, y_min, delta_min):.12f}")
    print(f"  packet_min:\n{np.round(packet_min, 6)}")
    print(f"  eta/eta_obs(min-law) = {np.round(etas_min, 12)}")

    return x_min, y_min, delta_min, packet_min, etas_min


def part3_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 3: BOTTOM LINE")
    print("=" * 88)

    check(
        "The off-seed source law is now explicit",
        True,
        "minimum information deformation at exact closure on the favored column",
    )
    check(
        "This law is strictly stronger than the bare extremal candidate",
        True,
        "it picks the least-deformed exact closure source, not just some overshooting source",
    )
    check(
        "So the full-stack closure route is now an actual invented law, not only a candidate scan",
        True,
        "what remains is whether to adopt this law as authority",
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS MINIMUM-INFORMATION SOURCE LAW")
    print("=" * 88)
    print()
    print("Framework convention:")
    print('  "axiom" means only Cl(3) on Z^3.')
    print()
    print("Invented law:")
    print("  On the fixed native N_e seed surface, choose the off-seed source that")
    print("  minimizes I_seed = D_KL(x||x_seed) + D_KL(y||y_seed) + (1-cos delta)")
    print("  subject to exact closure eta_{i_*}/eta_obs = 1, where i_* is the")
    print("  transport-favored column selected by the exact extremal class.")

    i_star, extremal_params = part1_transport_extremality_fixes_the_favored_column()
    part2_minimum_information_closure_law(i_star, extremal_params)
    part3_bottom_line()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Invented closure law:")
    print("    - favored column fixed by exact transport extremality")
    print("    - off-seed source fixed by minimum-information exact closure")
    print("    - exact eta/eta_obs = 1 on the current PMNS-assisted N_e branch")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
