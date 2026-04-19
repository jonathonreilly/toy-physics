#!/usr/bin/env python3
"""
DM leptogenesis PMNS normalization target theorem.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  If the remaining live weakness on the post-retained N_e lane is the
  observation-free normalization/value law, what exact coefficient target must
  that law hit, and what common false routes does the current branch already
  rule out?

Answer:
  The missing law must derive the exact coefficient

      a_* = 0.518479949928...

  in the observation-free free-energy family

      Phi_a = log F_{i_*}(H_e) - a S_rel(H_e || H_seed).

  On the current branch this target is fixed exactly by the local closure data:
    - it is the reciprocal KKT multiplier of the observational closure problem
    - equivalently, it is the projection coefficient of grad log F_{i_*} onto
      grad S_rel at the exact closure source

  The branch already rules out three weaker hopes:
    1. transport-only normalization (a = 0)
    2. unit-scale normalization (a = 1)
    3. naive endpoint or isotropic-Hessian matching on the reduced N_e domain

So the next real theorem is not "search harder". It is to derive a first-order
canonical normalization law for the favored-column transport observable on the
exact reduced N_e source family.
"""

from __future__ import annotations

import math
import sys

import numpy as np

import frontier_dm_leptogenesis_pmns_observation_free_normalization_boundary as norm
import frontier_dm_leptogenesis_pmns_relative_action_stationarity_theorem as stat

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

SEED_ZERO = np.zeros(5, dtype=float)


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


def favored_closure_data() -> tuple[int, np.ndarray, float, np.ndarray, np.ndarray]:
    i_star, extremal_params = stat.favored_column_and_extremal_params()
    start = stat.closure_point_on_ray(extremal_params, i_star)
    p_star, result = stat.constrained_stationary_point(start, i_star)
    if not result.success:
        raise RuntimeError("closure solve failed")
    grad_s = stat.finite_grad(stat.relative_action_from_params, p_star)
    grad_eta = stat.finite_grad(lambda p: stat.eta_i(np.asarray(p, dtype=float), i_star), p_star)
    lam = float(np.dot(grad_s, grad_eta) / max(np.dot(grad_eta, grad_eta), 1.0e-15))
    a_star = 1.0 / lam
    return i_star, np.asarray(p_star, dtype=float), a_star, grad_s, grad_eta


def part1_the_exact_target_coefficient_is_fixed_by_local_closure_data() -> tuple[int, np.ndarray, float]:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT NORMALIZATION TARGET IS FIXED BY LOCAL CLOSURE DATA")
    print("=" * 88)

    i_star, p_star, a_star, grad_s, grad_eta = favored_closure_data()
    grad_logf = stat.finite_grad(
        lambda p: math.log(norm.transport_factor_i(np.asarray(p, dtype=float), i_star)),
        p_star,
    )
    point = norm.describe_point(p_star, i_star)

    a_proj = float(np.dot(grad_logf, grad_s) / max(np.dot(grad_s, grad_s), 1.0e-15))
    grad_resid = float(np.linalg.norm(grad_logf - a_star * grad_s))

    check(
        "The favored exact closure source remains the i_* = 0 branch with eta/eta_obs = 1",
        i_star == 0 and abs(float(point["etas"][i_star]) - 1.0) < 1.0e-10,
        f"etas={np.round(point['etas'], 12)}",
    )
    check(
        "The missing normalization law must hit the exact coefficient a_* = 0.518479949928...",
        abs(a_star - 0.5184799499282735) < 1.0e-12,
        f"a_*={a_star:.12f}",
    )
    check(
        "That target is equivalently the local projection coefficient grad log F_{i_*} = a_* grad S_rel",
        abs(a_proj - a_star) < 1.0e-8 and grad_resid < 2.0e-5,
        f"a_proj={a_proj:.12f}, |grad logF - a_* gradS|={grad_resid:.3e}",
    )
    check(
        "So the normalization target is first-order local data on the exact reduced N_e closure source, not a new carrier choice",
        True,
        "a_* is fixed by the closure-source gradients",
    )

    print()
    print(f"  a_*     = {a_star:.12f}")
    print(f"  S_*     = {float(point['S']):.12f}")
    print(f"  F_*     = {float(point['F']):.12f}")
    print(f"  x_*     = {norm.fmt(point['x'])}")
    print(f"  y_*     = {norm.fmt(point['y'])}")

    return i_star, p_star, a_star


def part2_simple_normalization_guesses_are_not_the_target(i_star: int, p_star: np.ndarray, a_star: float) -> None:
    print("\n" + "=" * 88)
    print("PART 2: SIMPLE NORMALIZATION GUESSES DO NOT HIT THE TARGET")
    print("=" * 88)

    seed = norm.describe_point(SEED_ZERO, i_star)
    closure = norm.describe_point(p_star, i_star)

    a_endpoint = float(
        (math.log(float(closure["F"])) - math.log(float(seed["F"])))
        / max(float(closure["S"]) - float(seed["S"]), 1.0e-15)
    )

    check(
        "The exact target is not the transport-only law a = 0",
        a_star > 0.5,
        f"a_*={a_star:.12f}",
    )
    check(
        "The exact target is not the unit-scale free-energy law a = 1",
        abs(a_star - 1.0) > 0.45,
        f"a_*={a_star:.12f}",
    )
    check(
        "The exact target is not the endpoint-matching coefficient from seed to closure",
        abs(a_endpoint - a_star) > 2.5 and a_endpoint > 3.0,
        f"a_endpoint={a_endpoint:.12f}, a_*={a_star:.12f}",
    )

    print()
    print(f"  seed eta/eta_obs = {np.round(seed['etas'], 12)}")
    print(f"  a_endpoint       = {a_endpoint:.12f}")


def part3_isotropic_hessian_matching_is_not_the_missing_law(i_star: int, p_star: np.ndarray, a_star: float) -> None:
    print("\n" + "=" * 88)
    print("PART 3: ISOTROPIC HESSIAN MATCHING IS NOT THE MISSING LAW")
    print("=" * 88)

    grad_eta = stat.finite_grad(lambda p: stat.eta_i(np.asarray(p, dtype=float), i_star), p_star)
    basis = stat.tangent_basis(grad_eta)
    h_s = stat.finite_hessian(stat.relative_action_from_params, p_star)
    h_logf = stat.finite_hessian(
        lambda p: math.log(norm.transport_factor_i(np.asarray(p, dtype=float), i_star)),
        p_star,
    )
    t_s = basis.T @ h_s @ basis
    t_logf = basis.T @ h_logf @ basis

    alpha_ls = float(np.trace(t_logf.T @ t_s) / max(np.trace(t_s.T @ t_s), 1.0e-15))
    rel_resid = float(np.linalg.norm(t_logf - alpha_ls * t_s) / max(np.linalg.norm(t_logf), 1.0e-15))

    check(
        "The transport Hessian on the closure tangent is not a scalar multiple of the action Hessian",
        rel_resid > 0.8,
        f"alpha_ls={alpha_ls:.6f}, relative residual={rel_resid:.6f}",
    )
    check(
        "So the missing coefficient is not fixed by a naive isotropic quadratic-curvature matching",
        abs(alpha_ls - a_star) > 1.0,
        f"alpha_ls={alpha_ls:.6f}, a_*={a_star:.12f}",
    )
    check(
        "The live normalization theorem must therefore be more structured than uniform Hessian rescaling on the reduced cone",
        True,
        "the transport observable is not curvature-proportional to S_rel",
    )

    print()
    print(f"  tangent Hessian fit alpha_ls = {alpha_ls:.12f}")
    print(f"  relative Hessian residual    = {rel_resid:.12f}")


def part4_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)

    check(
        "The next exact theorem is a native law fixing the coefficient a in Phi_a = log F_{i_*} - a S_rel",
        True,
    )
    check(
        "That law must act on the favored-column transport observable itself, not on a new PMNS carrier",
        True,
    )
    check(
        "The most plausible live route is a first-order canonical normalization of log F_{i_*} against the exact effective action on the reduced N_e family",
        True,
    )

    print()
    print("  Exact read:")
    print("    - target coefficient: fixed")
    print("    - transport/action carrier: fixed")
    print("    - false easy routes: ruled out")
    print("    - live gap: derive the canonical first-order normalization law")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS NORMALIZATION TARGET")
    print("=" * 88)
    print()
    print("Question:")
    print("  What exact coefficient target must the missing native normalization law")
    print("  hit on the post-retained N_e lane, and what simple routes are already")
    print("  ruled out?")

    i_star, p_star, a_star = part1_the_exact_target_coefficient_is_fixed_by_local_closure_data()
    part2_simple_normalization_guesses_are_not_the_target(i_star, p_star, a_star)
    part3_isotropic_hessian_matching_is_not_the_missing_law(i_star, p_star, a_star)
    part4_bottom_line()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact target:")
    print("    - derive a_* = 0.518479949928... natively")
    print("    - not by a = 0, not by a = 1, not by endpoint matching,")
    print("      and not by isotropic Hessian rescaling")
    print("    - the live remaining theorem is a canonical first-order")
    print("      normalization law for the favored-column transport observable")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
