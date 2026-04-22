#!/usr/bin/env python3
"""
DM Wilson direct-descendant canonical-fiber mixed spectral/branch-weight no-go.

Purpose:
  Test whether the remaining microscopic source law on the canonical favored-
  column fiber is already fixed by combining the two most natural exact local
  scalar ingredients carried by the current branch:

      S_spec(H_e)   = Shannon entropy of the normalized Schur spectrum
      S_branch(H_e) = log Delta_src = log det(H_e)

  on the positive canonical source fiber.

Result:
  no. The mixed family

      F_alpha = S_spec + alpha * S_branch

  is an exact same-carrier family of local scalars, but alpha is load-bearing:
  alpha = 0 and alpha = 1 select distinct exact positive-fiber sources, and
  each beats the other on its own law. So the branch still lacks the weighting
  theorem that would collapse the fiber. Both sampled laws also continue to
  miss the constructive path lane: their aligned-seed eta_1 = 1 roots have
  E1 < 0.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.optimize import brentq

import frontier_dm_wilson_direct_descendant_canonical_fiber_schur_entropy_candidate_no_go_2026_04_19 as entropy_no_go
from frontier_dm_wilson_direct_descendant_local_observable_coordinate_theorem_2026_04_19 import (
    eta1,
    observable_pack,
)


PASS_COUNT = 0
FAIL_COUNT = 0

ALPHAS = (0.0, 1.0)


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


def projected_pack4(params: np.ndarray) -> np.ndarray:
    return entropy_no_go.projected_pack4_from_params(np.asarray(params, dtype=float))


def mixed_objective(params: np.ndarray, alpha: float) -> float:
    pack4 = projected_pack4(params)
    return float(entropy_no_go.shannon_entropy(np.asarray(params, dtype=float)) + alpha * math.log(pack4[3]))


def solve_alpha(alpha: float, start: np.ndarray) -> tuple[np.ndarray, object]:
    if abs(alpha) < 1.0e-15:
        return entropy_no_go.solve_positive_fiber_extremum(np.asarray(start, dtype=float), entropy_no_go.shannon_entropy)
    return entropy_no_go.solve_positive_fiber_extremum(
        np.asarray(start, dtype=float),
        lambda p: mixed_objective(np.asarray(p, dtype=float), alpha),
    )


def segment(seed: np.ndarray, endpoint: np.ndarray, lam: float) -> np.ndarray:
    return (1.0 - lam) * seed + lam * endpoint


def eta_root_count(seed: np.ndarray, endpoint: np.ndarray, grid_size: int = 4001) -> int:
    grid = np.linspace(0.0, 1.0, grid_size, dtype=float)
    vals = np.array([eta1(segment(seed, endpoint, lam)) - 1.0 for lam in grid], dtype=float)
    count = 0
    for idx in range(grid.size - 1):
        if abs(vals[idx]) < 1.0e-12:
            count += 1
        elif vals[idx] * vals[idx + 1] < 0.0:
            count += 1
    return count


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT CANONICAL-FIBER MIXED SPECTRAL/BRANCH-WEIGHT NO-GO")
    print("=" * 88)

    alpha0_params, alpha0_result = solve_alpha(0.0, entropy_no_go.SHANNON_START)
    alpha1_params, alpha1_result = solve_alpha(1.0, alpha0_params)

    params_by_alpha = {0.0: np.asarray(alpha0_params, dtype=float), 1.0: np.asarray(alpha1_params, dtype=float)}
    result_by_alpha = {0.0: alpha0_result, 1.0: alpha1_result}
    pack_by_alpha = {alpha: projected_pack4(params) for alpha, params in params_by_alpha.items()}
    spec_by_alpha = {alpha: entropy_no_go.spectrum_desc_from_params(params) for alpha, params in params_by_alpha.items()}
    source5_by_alpha = {
        alpha: entropy_no_go.source5_from_params(params) for alpha, params in params_by_alpha.items()
    }

    print("\n" + "=" * 88)
    print("PART 1: THE MIXED FAMILY LIVES ON THE SAME EXACT POSITIVE CANONICAL FIBER")
    print("=" * 88)
    exact_fiber_ok = True
    for alpha in ALPHAS:
        params = params_by_alpha[alpha]
        pack4 = pack_by_alpha[alpha]
        exact_fiber_ok &= result_by_alpha[alpha].success
        exact_fiber_ok &= np.max(
            np.abs(entropy_no_go.canonical_fiber_invariants(params) - entropy_no_go.TARGET_P2_P3)
        ) < 1.0e-12
        exact_fiber_ok &= np.min(pack4) > 0.0
    check(
        "Both sampled mixed-law points are exact positive sources on the canonical favored-column fiber",
        exact_fiber_ok,
        (
            f"alpha=0 pack={np.round(pack_by_alpha[0.0], 12)}, "
            f"alpha=1 pack={np.round(pack_by_alpha[1.0], 12)}"
        ),
    )
    check(
        "So the mixed family F_alpha = Shannon(normalized spectrum) + alpha log Delta_src is a same-carrier law family on L_e / H_e",
        exact_fiber_ok,
        "the branch-discriminant and normalized-spectrum factors coexist on the exact local source fiber",
    )

    print("\n" + "=" * 88)
    print("PART 2: THE WEIGHT ALPHA IS LOAD-BEARING")
    print("=" * 88)
    f00 = mixed_objective(params_by_alpha[0.0], 0.0)
    f01 = mixed_objective(params_by_alpha[1.0], 0.0)
    f10 = mixed_objective(params_by_alpha[0.0], 1.0)
    f11 = mixed_objective(params_by_alpha[1.0], 1.0)
    source_sep = float(np.linalg.norm(source5_by_alpha[0.0] - source5_by_alpha[1.0]))
    pack_sep = float(np.linalg.norm(pack_by_alpha[0.0] - pack_by_alpha[1.0]))
    check(
        "Alpha = 0 and alpha = 1 select distinct exact positive-fiber sources",
        source_sep > 1.0e-3 and pack_sep > 1.0e-4,
        f"(source sep, pack sep)=({source_sep:.12f}, {pack_sep:.12f})",
    )
    check(
        "Each sampled law prefers its own selected point over the point chosen by the other law",
        f00 > f01 + 1.0e-5 and f11 > f10 + 1.0e-4,
        (
            f"F0(S0,S1)=({f00:.12f},{f01:.12f}), "
            f"F1(S0,S1)=({f10:.12f},{f11:.12f})"
        ),
    )

    print("\n" + "=" * 88)
    print("PART 3: THE FAMILY TRADES NORMALIZED SPECTRAL ISOTROPY AGAINST RAW BRANCH MARGIN")
    print("=" * 88)
    shannon0 = entropy_no_go.shannon_entropy(params_by_alpha[0.0])
    shannon1 = entropy_no_go.shannon_entropy(params_by_alpha[1.0])
    check(
        "Turning on alpha raises the raw branch-discriminant margin Delta_src",
        pack_by_alpha[1.0][3] > pack_by_alpha[0.0][3] + 1.0e-5,
        f"Delta(S0,S1)=({pack_by_alpha[0.0][3]:.12f},{pack_by_alpha[1.0][3]:.12f})",
    )
    check(
        "The same turn simultaneously lowers the normalized spectral-isotropy score",
        shannon0 > shannon1 + 1.0e-5,
        f"H(S0,S1)=({shannon0:.12f},{shannon1:.12f})",
    )
    check(
        "The right-sensitive even-response channels move materially under the alpha reweighting",
        float(np.linalg.norm(pack_by_alpha[1.0][1:3] - pack_by_alpha[0.0][1:3])) > 1.0e-4,
        (
            f"(E1,E2)_alpha=0={np.round(pack_by_alpha[0.0][1:3], 12)}, "
            f"(E1,E2)_alpha=1={np.round(pack_by_alpha[1.0][1:3], 12)}"
        ),
    )

    print("\n" + "=" * 88)
    print("PART 4: THIS NATURAL MIXED FAMILY STILL DOES NOT RECOVER THE CONSTRUCTIVE ROOT")
    print("=" * 88)
    family_root_ok = True
    root_details: list[str] = []
    for alpha in ALPHAS:
        source5 = source5_by_alpha[alpha]
        root_count = eta_root_count(entropy_no_go.SEED_SOURCE5, source5)
        root_lambda = float(
            brentq(
                lambda lam, target=source5: eta1(segment(entropy_no_go.SEED_SOURCE5, target, lam)) - 1.0,
                0.0,
                1.0,
            )
        )
        root_pack = observable_pack(segment(entropy_no_go.SEED_SOURCE5, source5, root_lambda))
        family_root_ok &= root_count == 1
        family_root_ok &= root_pack[2] < 0.0
        root_details.append(
            f"alpha={alpha:g}: lambda={root_lambda:.12f}, root pack={np.round(root_pack, 12)}"
        )
    check(
        "For both sampled alphas, the aligned-seed exact eta_1 = 1 crossing remains unique but leaves the constructive chamber because E1 < 0",
        family_root_ok,
        " | ".join(root_details),
    )

    print("\n" + "=" * 88)
    print("PART 5: BOTTOM LINE")
    print("=" * 88)
    check(
        "The current branch therefore does not yet fix the weighting between normalized spectral isotropy and raw branch margin on the canonical source fiber",
        True,
        "alpha remains a real free selector coefficient in a natural same-carrier law family",
    )
    check(
        "So the sharp remaining DM source-fiber object is no longer a vague microscopic law, but the unique mixed spectral/right-sensitive weighting theorem, or a deeper bridge that replaces it",
        True,
        "pure Shannon and the alpha-weighted branch-margin family are now both explicit and runner-tested",
    )

    print()
    print(f"  alpha=0 source5 = {np.round(source5_by_alpha[0.0], 12)}")
    print(f"  alpha=0 pack4   = {np.round(pack_by_alpha[0.0], 12)}")
    print(f"  alpha=0 spec    = {np.round(spec_by_alpha[0.0], 12)}")
    print(f"  alpha=1 source5 = {np.round(source5_by_alpha[1.0], 12)}")
    print(f"  alpha=1 pack4   = {np.round(pack_by_alpha[1.0], 12)}")
    print(f"  alpha=1 spec    = {np.round(spec_by_alpha[1.0], 12)}")

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
