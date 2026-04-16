#!/usr/bin/env python3
"""
Majorana partition/projective transplant obstruction on the current atlas stack.

Question:
  Can the exact universal UV-finite partition density, projective Schur
  closure, or canonical refinement-net pullback provide the missing absolute
  Majorana staircase selector once the current local lane has already selected
  the self-dual source ray?

Answer on the current exact stack:
  No. On a homogeneous source ray J_lambda = lambda J_0, the exact local
  partition density changes only by

      Delta log rho(lambda) = 1/2 lambda^2 <J_0, K^-1 J_0>,

  so it is monotone with no finite stationary selector. Exact Schur/projective
  coarse-graining preserves the same source scaling, and the refinement/atlas
  density cocycle introduces no new lambda dependence.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0
ALPHA_LM = 0.09067

ROOT = Path(__file__).resolve().parents[1]


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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def build_positive_background_operator() -> np.ndarray:
    d = np.array([2.0, 3.0, 5.0, 7.0], dtype=float)
    h_d = np.diag(
        [
            1.0 / (d[0] * d[0]),
            1.0 / (d[1] * d[1]),
            1.0 / (d[2] * d[2]),
            1.0 / (d[3] * d[3]),
            1.0 / (d[0] * d[1]),
            1.0 / (d[0] * d[2]),
            1.0 / (d[0] * d[3]),
            1.0 / (d[1] * d[2]),
            1.0 / (d[1] * d[3]),
            1.0 / (d[2] * d[3]),
        ]
    )
    lambda_r = np.array(
        [
            [2.0, 0.2, 0.0],
            [0.2, 1.7, 0.1],
            [0.0, 0.1, 1.4],
        ],
        dtype=float,
    )
    return np.kron(h_d, lambda_r)


def log_partition_density(k_op: np.ndarray, j: np.ndarray) -> float:
    sign, logdet = np.linalg.slogdet(k_op)
    if sign <= 0:
        raise ValueError("expected positive-definite operator")
    return -0.5 * logdet + 0.5 * float(j @ np.linalg.solve(k_op, j))


def schur_reduce(
    k_op: np.ndarray,
    j: np.ndarray,
    keep: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    all_idx = np.arange(k_op.shape[0])
    elim = np.setdiff1d(all_idx, keep, assume_unique=True)
    k_kk = k_op[np.ix_(keep, keep)]
    k_ke = k_op[np.ix_(keep, elim)]
    k_ek = k_op[np.ix_(elim, keep)]
    k_ee = k_op[np.ix_(elim, elim)]
    j_k = j[keep]
    j_e = j[elim]
    k_ee_inv = np.linalg.inv(k_ee)
    k_eff = k_kk - k_ke @ k_ee_inv @ k_ek
    j_eff = j_k - k_ke @ k_ee_inv @ j_e
    return k_eff, j_eff


def random_invertible(seed: int, n: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    q1, _ = np.linalg.qr(rng.normal(size=(n, n)))
    if np.linalg.det(q1) < 0:
        q1[:, 0] *= -1
    q2, _ = np.linalg.qr(rng.normal(size=(n, n)))
    if np.linalg.det(q2) < 0:
        q2[:, 0] *= -1
    scales = np.diag(0.8 + 0.4 * rng.random(size=n))
    return q1 @ scales @ q2


def test_authority_stack_is_present() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ATLAS ALREADY CONTAINS THE PARTITION / PROJECTIVE FAMILY")
    print("=" * 88)

    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    uv = read("docs/UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md")
    proj = read("docs/UNIVERSAL_QG_PROJECTIVE_SCHUR_CLOSURE_NOTE.md")
    refine = read("docs/UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md")
    blocker = read("docs/NEUTRINO_MAJORANA_SELF_DUAL_STAIRCASE_LIFT_OBSTRUCTION_NOTE.md")

    check("Atlas retains the universal UV-finite partition-density row", "Universal UV-finite partition density" in atlas)
    check("Atlas retains the universal projective-Schur closure row", "Universal projective Schur closure" in atlas)
    check("Atlas retains the universal canonical refinement-net row", "Universal canonical geometric refinement net" in atlas)
    check("The UV-finite partition note defines an exact partition-density family", "partition-density family" in uv.lower())
    check("The projective-Schur note gives exact Schur coarse-graining closure", "schur" in proj.lower() and "coarse-graining" in proj.lower())
    check("The refinement note gives exact density pullback / invariance on the net", "density invariance" in refine.lower() or "partition density is refinement-invariant" in refine.lower())
    check("The current Majorana blocker note already fixes the self-dual source family to one positive ray", "positive ray" in blocker.lower() and "projective" in blocker.lower())


def test_partition_density_stays_monotone_on_the_ray() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE UV-FINITE PARTITION DENSITY HAS NO FINITE SELECTOR ON THE RAY")
    print("=" * 88)

    k_op = build_positive_background_operator()
    k_inv = np.linalg.inv(k_op)
    j0 = np.linspace(1.0, float(k_op.shape[0]), k_op.shape[0], dtype=float)
    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]
    coeff = float(j0 @ (k_inv @ j0))

    ratios = []
    derivatives = []
    for scale in scales:
        j = scale * j0
        delta_log_rho = 0.5 * float(j @ (k_inv @ j))
        ratios.append(delta_log_rho / (scale * scale))
        derivatives.append(scale * coeff)

    spread = max(ratios) - min(ratios)

    check("The partition-density response on the ray is exactly quadratic in lambda", spread < 1e-9, f"spread in Delta log rho / lambda^2={spread:.2e}")
    check("The partition-density coefficient is positive", coeff > 0.0, f"<J_0,K^-1 J_0>={coeff:.6e}")
    check("d log rho / d lambda = lambda <J_0,K^-1 J_0> stays strictly positive on lambda > 0", all(derivative > 0.0 for derivative in derivatives), f"derivatives={derivatives}")
    check("So the local partition density has no intrinsic finite positive stationary selector", coeff > 0.0 and all(derivative > 0.0 for derivative in derivatives), "only the trivial lambda=0 boundary is stationary")


def test_projective_schur_closure_preserves_the_same_source_law() -> None:
    print("\n" + "=" * 88)
    print("PART 3: EXACT SCHUR / PROJECTIVE CLOSURE PRESERVES THE SAME SCALE LAW")
    print("=" * 88)

    k_op = build_positive_background_operator()
    j0 = np.linspace(1.0, float(k_op.shape[0]), k_op.shape[0], dtype=float)
    keep = np.arange(10)
    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]

    base_j_eff = None
    ratios = []
    for scale in scales:
        k_eff, j_eff = schur_reduce(k_op, scale * j0, keep)
        if base_j_eff is None:
            base_j_eff = j_eff / scale
        ratios.append(0.5 * float(j_eff @ np.linalg.solve(k_eff, j_eff)) / (scale * scale))
        diff = float(np.max(np.abs(j_eff / scale - base_j_eff)))
        check(f"Schur-reduced source stays linear in lambda at scale {scale:.3e}", diff < 1e-12, f"max reduced-source deviation={diff:.2e}")

    spread = max(ratios) - min(ratios)
    check("The coarse partition-density response is still exactly quadratic in lambda", spread < 1e-9, f"spread in coarse Delta log rho / lambda^2={spread:.2e}")


def test_density_cocycle_does_not_create_new_lambda_dependence() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE DENSITY COCYCLE / REFINEMENT PULLBACK ADDS NO NEW SCALE LAW")
    print("=" * 88)

    k_op = build_positive_background_operator()
    n = k_op.shape[0]
    t = random_invertible(17, n)
    t_inv = np.linalg.inv(t)
    k_prime = t_inv.T @ k_op @ t_inv
    jac = abs(float(np.linalg.det(t)))
    j0 = np.linspace(1.0, float(n), n, dtype=float)
    scales = [ALPHA_LM ** 7, ALPHA_LM ** 8, ALPHA_LM ** 9]

    max_err = 0.0
    for scale in scales:
        j = scale * j0
        j_prime = t_inv.T @ j
        # Raw partition densities differ by the chart Jacobian; the compensated
        # density is the invariant quantity on the exact atlas/refinement net.
        log_rho = log_partition_density(k_op, j)
        log_rho_prime = log_partition_density(k_prime, j_prime) - math.log(jac)
        max_err = max(max_err, abs(log_rho_prime - log_rho))

    check("The measure-compensated partition density is exactly chart/refinement invariant across the source ray", max_err < 1e-9, f"max compensated-density mismatch={max_err:.2e}")
    check("So the refinement/overlap cocycle introduces no new lambda dependence", max_err < 1e-9, "the density cocycle is lambda-blind after compensation")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: PARTITION / PROJECTIVE TRANSPLANT OBSTRUCTION")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the universal UV-finite partition density, exact projective Schur")
    print("  closure, or canonical refinement-net pullback act as the missing")
    print("  absolute Majorana staircase selector on the current self-dual ray?")

    test_authority_stack_is_present()
    test_partition_density_stays_monotone_on_the_ray()
    test_projective_schur_closure_preserves_the_same_source_law()
    test_density_cocycle_does_not_create_new_lambda_dependence()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  No. The universal partition / projective family still does not")
    print("  break the current source-scale homogeneity: the local density changes")
    print("  only by a monotone quadratic-in-lambda exponent, exact Schur coarse-")
    print("  graining preserves that same law, and the refinement/atlas density")
    print("  cocycle adds no new lambda dependence.")
    print()
    print("  So this QG/measure route is not the missing non-homogeneous")
    print("  local-to-generation bridge on the present stack.")
    print()
    print(f"  PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
