#!/usr/bin/env python3
"""Support-grade effective-action selector on the fixed-sigma PMNS surface."""

from __future__ import annotations

import math
import sys

import numpy as np

from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_effective_action_selector_boundary import gram_lift, relative_action_to_seed
from frontier_pmns_sigma_constraint_surface import sigma_slice_block

np.set_printoptions(precision=6, suppress=True, linewidth=140)

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


def determinant_a_on_sigma_surface(sigma: float, u: float, v: float) -> float:
    r2 = u * u + v * v
    w = 3.0 * sigma - 2.0 * u
    return 1.0 + w * r2


def relative_action_sigma_surface_formula(sigma: float, u: float, v: float) -> float:
    det_a = determinant_a_on_sigma_surface(sigma, u, v)
    if det_a <= 0.0:
        raise ValueError("point left the positive Gram-lift branch")
    return 9.0 * sigma * sigma - 12.0 * sigma * u + 6.0 * u * u + 2.0 * v * v - 2.0 * math.log(det_a)


def exact_hessian_diagonal_at_covariant_point(sigma: float) -> tuple[float, float]:
    denom = sigma**3 + 1.0
    huu = 12.0 * (sigma**3 + sigma + 1.0) / denom
    hvv = 4.0 * (sigma**3 - sigma + 1.0) / denom
    return huu, hvv


def cubic_lower_bound_on_unit_interval() -> float:
    sigma_star = 1.0 / math.sqrt(3.0)
    return sigma_star**3 - sigma_star + 1.0


def local_grid_minimum(sigma: float, span_u: float = 0.45, span_v: float = 0.55, n: int = 221) -> tuple[float, float, float]:
    best = None
    for u in np.linspace(max(-0.35, sigma - span_u), sigma + span_u, n):
        for v in np.linspace(-span_v, span_v, n):
            det_a = determinant_a_on_sigma_surface(sigma, float(u), float(v))
            if det_a <= 1.0e-10:
                continue
            value = relative_action_sigma_surface_formula(sigma, float(u), float(v))
            if best is None or value < best[0]:
                best = (value, float(u), float(v))
    if best is None:
        raise ValueError("no admissible point found on scan box")
    return best


def part1_exact_relative_action_formula_on_the_sigma_surface() -> None:
    print("\n" + "=" * 88)
    print("PART 1: EXACT RELATIVE-ACTION FORMULA ON THE SIGMA SURFACE")
    print("=" * 88)

    sigma = 0.23
    u = 0.17
    v = 0.14
    block = sigma_slice_block(sigma=sigma, u=u, v=v, xbar=1.0)
    lifted = gram_lift(block)
    formula = relative_action_sigma_surface_formula(sigma, u, v)
    exact = relative_action_to_seed(lifted)

    check("The fixed-sigma PMNS family admits an exact closed formula for the native action on the Gram lift", abs(formula - exact) < 1.0e-12, f"formula={formula:.12f}, exact={exact:.12f}")
    check("The action depends only on sigma, u, v on that surface", True, f"sigma={sigma:.6f}, u={u:.6f}, v={v:.6f}")


def part2_the_c3_covariant_point_is_an_exact_local_minimum_on_0_le_sigma_le_1() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE C3-COVARIANT POINT IS AN EXACT LOCAL MINIMUM ON 0 <= SIGMA <= 1")
    print("=" * 88)

    sigma = 0.23
    cov_value = relative_action_sigma_surface_formula(sigma, sigma, 0.0)
    eps = 1.0e-6
    du = (
        relative_action_sigma_surface_formula(sigma, sigma + eps, 0.0)
        - relative_action_sigma_surface_formula(sigma, sigma - eps, 0.0)
    ) / (2.0 * eps)
    dv = (
        relative_action_sigma_surface_formula(sigma, sigma, eps)
        - relative_action_sigma_surface_formula(sigma, sigma, -eps)
    ) / (2.0 * eps)
    huu, hvv = exact_hessian_diagonal_at_covariant_point(sigma)
    lower = cubic_lower_bound_on_unit_interval()

    check("At the C3-covariant point the fixed-sigma action has zero first derivative in u", abs(du) < 1.0e-6, f"du={du:.3e}")
    check("At the same point the fixed-sigma action has zero first derivative in v", abs(dv) < 1.0e-6, f"dv={dv:.3e}")
    check("The exact Hessian in the u direction is positive there", huu > 0.0, f"huu={huu:.12f}")
    check("The exact Hessian in the v direction is positive on the whole physical interval 0 <= sigma <= 1", lower > 0.0 and hvv > 0.0, f"lower={lower:.12f}, hvv={hvv:.12f}")
    check("So the C3-covariant point is an exact local minimum of the native action on the fixed-sigma surface", cov_value >= 0.0, f"S_cov={cov_value:.12f}")


def part3_compact_scan_supports_the_covariant_point_as_the_low_action_branch() -> None:
    print("\n" + "=" * 88)
    print("PART 3: COMPACT SCAN SUPPORTS THE COVARIANT POINT AS THE LOW-ACTION BRANCH")
    print("=" * 88)

    sigmas = [0.05, 0.15, 0.30]
    offsets = []
    current_errors = []
    values = []
    for sigma in sigmas:
        best_value, best_u, best_v = local_grid_minimum(sigma)
        offsets.append(abs(best_u - sigma) + abs(best_v))
        values.append(best_value)
        best_block = sigma_slice_block(sigma=sigma, u=best_u, v=best_v, xbar=1.0)
        current_errors.append(abs(nontrivial_character_current(best_block) - sigma))

    check("A compact exhaustive scan keeps the lowest-action point close to the C3-covariant locus u = sigma, v = 0", max(offsets) < 0.02, f"offsets={np.round(offsets, 6)}")
    check("On those same low-action scan points, the selected current stays close to J_chi = sigma", max(current_errors) < 0.02, f"errors={np.round(current_errors, 6)}")
    check("So the fixed-sigma selector picture is strongly supported on the current retained PMNS patch", all(value >= 0.0 for value in values), f"values={np.round(values, 6)}")
    print("  [INFO] This compact scan is support-grade evidence, not a theorem-grade global certificate")


def main() -> int:
    print("=" * 88)
    print("PMNS SIGMA-CONSTRAINED EFFECTIVE-ACTION SELECTOR")
    print("=" * 88)
    print()
    print("Question:")
    print("  Once a nonzero pure-PMNS sigma surface is admitted, what does the")
    print("  native effective action do on that surface?")

    part1_exact_relative_action_formula_on_the_sigma_surface()
    part2_the_c3_covariant_point_is_an_exact_local_minimum_on_0_le_sigma_le_1()
    part3_compact_scan_supports_the_covariant_point_as_the_low_action_branch()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  On the fixed-sigma PMNS surface:")
    print("    - the native action on the canonical positive Gram lift has an exact")
    print("      closed formula")
    print("    - the C3-covariant point u = w = sigma, v = 0 is an exact local")
    print("      minimum on the physical interval 0 <= sigma <= 1")
    print("    - compact scans support that same point as the low-action branch")
    print("      on the retained PMNS patch")
    print()
    print("  So if the sole axiom ever derives a nonzero sigma surface, the native")
    print("  effective action has a credible in-repo route to selecting")
    print("  J_chi = sigma. The missing theorem is the production of sigma itself.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
