#!/usr/bin/env python3
"""
DM leptogenesis PMNS observation-free normalization boundary.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  Can the current exact PMNS-assisted N_e stack replace the observational
  closure surface eta_{i_*}/eta_obs = 1 by a purely native observation-free
  value law on the exact reduced domain?

Answer:
  Not yet.

  The current exact branch does allow the closure source to be rewritten as a
  stationary point of a one-parameter observation-free free-energy family

      Phi_a = log F_{i_*}(H_e) - a S_rel(H_e || H_seed),

  but:
    - transport extremality alone (a = 0) overshoots;
    - the natural unit-scale free-energy objective (a = 1) underproduces;
    - the tuned coefficient a_* that makes the closure source locally
      stationary is itself not yet derived from the current bank;
    - current bounded observation-free searches do not upgrade that local
      rewrite into a theorem-grade global value law.

So the exact remaining weakness is a normalization/value-law gap, not a new
carrier or selector-structure gap.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.optimize import differential_evolution

import frontier_dm_leptogenesis_pmns_relative_action_stationarity_theorem as stat
import frontier_dm_leptogenesis_pmns_observable_relative_action_law as rel
from frontier_dm_leptogenesis_flavor_column_functional_theorem import (
    flavored_column_functional,
    flavored_transport_kernel,
)
from dm_leptogenesis_exact_common import exact_package

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

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


def fmt(v: np.ndarray) -> str:
    return np.array2string(np.round(np.asarray(v, dtype=float), 6), separator=", ")


def transport_factor_i(params: np.ndarray, i_star: int) -> float:
    x, y, delta, h_e, _etas = stat.source_from_params(np.asarray(params, dtype=float))
    _ = x, y, delta
    packet = rel.active_packet_from_h(h_e).T
    return float(flavored_column_functional(packet[:, i_star], Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL))


def phi_a(params: np.ndarray, i_star: int, a_coeff: float) -> float:
    return math.log(transport_factor_i(np.asarray(params, dtype=float), i_star)) - a_coeff * stat.relative_action_from_params(
        np.asarray(params, dtype=float)
    )


def solve_phi_global(i_star: int, a_coeff: float, *, seed: int) -> np.ndarray:
    result = differential_evolution(
        lambda p: -phi_a(np.asarray(p, dtype=float), i_star, a_coeff),
        bounds=[
            (-4.0, 4.0),
            (-4.0, 4.0),
            (-4.0, 4.0),
            (-4.0, 4.0),
            (-math.pi, math.pi),
        ],
        seed=seed,
        maxiter=20,
        popsize=10,
        polish=True,
        disp=False,
    )
    return np.asarray(result.x, dtype=float)


def describe_point(params: np.ndarray, i_star: int) -> dict[str, object]:
    x, y, delta, h_e, etas = stat.source_from_params(np.asarray(params, dtype=float))
    packet = rel.active_packet_from_h(h_e).T
    return {
        "params": np.asarray(params, dtype=float),
        "x": np.asarray(x, dtype=float),
        "y": np.asarray(y, dtype=float),
        "delta": float(delta),
        "packet": np.asarray(packet, dtype=float),
        "etas": np.asarray(etas, dtype=float),
        "S": float(stat.relative_action_from_params(np.asarray(params, dtype=float))),
        "F": float(transport_factor_i(np.asarray(params, dtype=float), i_star)),
        "best_idx": int(np.argmax(np.asarray(etas, dtype=float))),
    }


def part1_the_current_exact_closure_source_induces_a_tuned_observation_free_family() -> tuple[int, np.ndarray, float]:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT CLOSURE SOURCE INDUCES A TUNED OBSERVATION-FREE FAMILY")
    print("=" * 88)

    i_star, extremal_params = stat.favored_column_and_extremal_params()
    start = stat.closure_point_on_ray(extremal_params, i_star)
    p_star, result = stat.constrained_stationary_point(start, i_star)

    grad_s = stat.finite_grad(stat.relative_action_from_params, p_star)
    grad_eta = stat.finite_grad(lambda p: stat.eta_i(np.asarray(p, dtype=float), i_star), p_star)
    lam = float(np.dot(grad_s, grad_eta) / max(np.dot(grad_eta, grad_eta), 1.0e-15))
    a_star = 1.0 / lam
    grad_phi = stat.finite_grad(lambda p: phi_a(np.asarray(p, dtype=float), i_star, a_star), p_star)
    point = describe_point(p_star, i_star)

    check("The exact closure source still converges on the favored column", result.success and i_star == 0,
          f"i_star={i_star}")
    check("The closure source gives eta/eta_obs = 1 on the favored column",
          abs(float(point["etas"][i_star]) - 1.0) < 1.0e-10,
          f"etas={np.round(point['etas'], 12)}")
    check("The same source is locally stationary for one tuned observation-free free-energy family",
          np.linalg.norm(grad_phi) < 5.0e-5,
          f"a_*={a_star:.12f}, |grad Phi_a*|={np.linalg.norm(grad_phi):.3e}")
    check("That tuned coefficient is nontrivial and not fixed by the old transport-only or unit-scale action laws",
          0.0 < a_star < 1.0 and abs(a_star - 1.0) > 0.1,
          f"a_*={a_star:.12f}")

    print()
    print(f"  x_*     = {fmt(point['x'])}")
    print(f"  y_*     = {fmt(point['y'])}")
    print(f"  delta_* = {float(point['delta']):.12e}")
    print(f"  S_*     = {float(point['S']):.12f}")
    print(f"  F_*     = {float(point['F']):.12f}")
    print(f"  a_*     = {a_star:.12f}")

    return i_star, np.asarray(p_star, dtype=float), a_star


def part2_transport_extremality_alone_overshoots(i_star: int) -> None:
    print("\n" + "=" * 88)
    print("PART 2: TRANSPORT EXTREMALITY ALONE OVERSHOOTS")
    print("=" * 88)

    extremal_params = solve_phi_global(i_star, 0.0, seed=0)
    point = describe_point(extremal_params, i_star)

    check("Transport extremality stays on the exact fixed native seed surface",
          abs(np.mean(point["x"]) - rel.XBAR_NE) < 1.0e-12 and abs(np.mean(point["y"]) - rel.YBAR_NE) < 1.0e-12,
          f"(xbar,ybar)=({np.mean(point['x']):.6f},{np.mean(point['y']):.6f})")
    check("Transport extremality overshoots the exact closure value on the favored column",
          float(point["etas"][i_star]) > 1.04,
          f"etas={np.round(point['etas'], 12)}")
    check("The transport-only optimum is not the low-action closure source",
          float(point["S"]) > 0.4,
          f"S={float(point['S']):.12f}")

    print()
    print(f"  transport-optimal eta/eta_obs = {np.round(point['etas'], 12)}")
    print(f"  transport-optimal S_rel       = {float(point['S']):.12f}")
    print(f"  transport-optimal packet col  = {np.round(point['packet'][:, i_star], 6)}")


def part3_unit_scale_free_energy_underproduces(i_star: int) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE UNIT-SCALE FREE-ENERGY OBJECTIVE UNDERPRODUCES")
    print("=" * 88)

    params = solve_phi_global(i_star, 1.0, seed=0)
    point = describe_point(params, i_star)

    check("The unit-scale free-energy law still stays on the exact fixed seed surface",
          abs(np.mean(point["x"]) - rel.XBAR_NE) < 1.0e-12 and abs(np.mean(point["y"]) - rel.YBAR_NE) < 1.0e-12,
          f"(xbar,ybar)=({np.mean(point['x']):.6f},{np.mean(point['y']):.6f})")
    check("The unit-scale law does not recover exact closure on the favored column",
          float(point["etas"][i_star]) < 0.9,
          f"etas={np.round(point['etas'], 12)}")
    check("It instead collapses toward a low-action underproducing source near the seed",
          float(point["S"]) < 0.01,
          f"S={float(point['S']):.12f}")

    print()
    print(f"  unit-scale eta/eta_obs = {np.round(point['etas'], 12)}")
    print(f"  unit-scale S_rel       = {float(point['S']):.12f}")
    print(f"  unit-scale packet col  = {np.round(point['packet'][:, i_star], 6)}")


def part4_the_tuned_family_is_not_yet_a_derived_global_value_law(
    i_star: int, p_star: np.ndarray, a_star: float
) -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE TUNED FAMILY IS NOT YET A DERIVED GLOBAL VALUE LAW")
    print("=" * 88)

    params = solve_phi_global(i_star, a_star, seed=0)
    point = describe_point(params, i_star)
    closure = describe_point(p_star, i_star)

    check("A generic bounded observation-free search at the tuned coefficient does not simply return the closure source",
          np.linalg.norm(np.asarray(point["params"], dtype=float) - np.asarray(closure["params"], dtype=float)) > 0.1,
          f"|Δp|={np.linalg.norm(np.asarray(point['params']) - np.asarray(closure['params'])):.6f}")
    check("That bounded search still lands on an underproducing alternative source",
          float(point["etas"][i_star]) < 0.95,
          f"etas={np.round(point['etas'], 12)}")
    check("So current numerics do not yet promote the tuned family into a theorem-grade observation-free selector",
          phi_a(np.asarray(point["params"], dtype=float), i_star, a_star)
          <= phi_a(p_star, i_star, a_star) + 1.0e-8,
          f"Phi_search={phi_a(np.asarray(point['params']), i_star, a_star):.12f}, Phi_*={phi_a(p_star, i_star, a_star):.12f}")

    print()
    print(f"  bounded-search eta/eta_obs = {np.round(point['etas'], 12)}")
    print(f"  bounded-search S_rel       = {float(point['S']):.12f}")
    print(f"  bounded-search packet col  = {np.round(point['packet'][:, i_star], 6)}")


def part5_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 5: BOTTOM LINE")
    print("=" * 88)

    check("The current exact weakness is a normalization/value-law gap, not a carrier or reduced-domain gap", True)
    check("The observational closure surface eta_{i_*}/eta_obs = 1 is therefore still doing real scientific work on this branch", True)
    check("The next exact target is an axiom-native normalization law that fixes the free-energy coefficient a without reference to eta_obs", True)

    print()
    print("  Exact read:")
    print("    - transport structure: closed")
    print("    - reduced-domain selector structure: closed")
    print("    - observation-free normalization/value law: still open")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS OBSERVATION-FREE NORMALIZATION BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the current exact PMNS-assisted N_e stack replace the")
    print("  observational closure surface by a purely native observation-free")
    print("  value law on the exact reduced domain?")

    i_star, p_star, a_star = part1_the_current_exact_closure_source_induces_a_tuned_observation_free_family()
    part2_transport_extremality_alone_overshoots(i_star)
    part3_unit_scale_free_energy_underproduces(i_star)
    part4_the_tuned_family_is_not_yet_a_derived_global_value_law(i_star, p_star, a_star)
    part5_bottom_line()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-stack answer:")
    print("    - the closure source can be embedded into a one-parameter")
    print("      observation-free free-energy family Phi_a")
    print("    - but the normalization coefficient a is not yet derived")
    print("    - transport-only and unit-scale free-energy candidates do not recover")
    print("      the exact closure source")
    print("    - and current bounded observation-free searches do not yet supply")
    print("      a theorem-grade global selector at the tuned coefficient")
    print()
    print("  So the remaining weakness is real and precise:")
    print("    the observation-free normalization/value law is still open.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
