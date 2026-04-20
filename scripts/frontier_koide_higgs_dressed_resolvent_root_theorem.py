#!/usr/bin/env python3
"""
Frontier runner — Koide Higgs-dressed resolvent root theorem.

Companion to
`docs/KOIDE_HIGGS_DRESSED_RESOLVENT_ROOT_THEOREM_NOTE_2026-04-20.md`.

Claim.
  On the retained missing-axis 4x4 lift

      W_4(h_0) = diag(h_0, H_*(m, delta, q_+))

  used in the existing Higgs-dressed intermediate-propagator avenue, the
  resolvent family

      R_lambda(h_0) = (lambda I_4 - W_4(h_0))^{-1}

  induces a species block

      Sigma_lambda(h_0) = P_T1 Gamma_1 R_lambda(h_0) Gamma_1 P_T1

  whose eigenvalue magnitudes hit the Koide surface `Q = 2/3` at isolated
  scalar roots. For the most natural baseline `h_0 = 0`, there is a unique
  small positive root `lambda_*` near the old chamber-slack scalar. This
  yields a near-PDG charged-lepton direction while remaining an honest
  one-scalar open law.
"""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np
from scipy.optimize import brentq

from frontier_higgs_dressed_propagator_v1 import (
    DELTA_STAR,
    E1,
    H_lift_missing_axis,
    M_STAR,
    Q_PLUS_STAR,
    direction_cos,
    embed_4x4_to_16,
    koide_Q,
    sigma_with_weight_operator,
)


PASS = 0
FAIL = 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] {label}" + (f"  ({detail})" if detail else ""))


def symmetrized_eigs(mat: np.ndarray) -> np.ndarray:
    herm = 0.5 * (mat + mat.conj().T)
    return np.linalg.eigvalsh(herm)


def sigma_data(lambda_value: float, h0: float) -> tuple[float, float, np.ndarray, np.ndarray, np.ndarray]:
    w4 = H_lift_missing_axis(h0)
    w4_eigs, w4_vecs = np.linalg.eigh(w4)
    diffs = lambda_value - w4_eigs
    if np.min(np.abs(diffs)) < 1.0e-9:
        raise ValueError("lambda too close to a pole")
    w4_res = w4_vecs @ np.diag(1.0 / diffs) @ w4_vecs.conj().T
    sigma = sigma_with_weight_operator(embed_4x4_to_16(w4_res))
    sigma_eigs = symmetrized_eigs(sigma)
    masses = np.abs(sigma_eigs)
    return (
        koide_Q(masses),
        direction_cos(masses),
        sigma_eigs,
        np.real(np.diag(sigma)),
        w4_eigs,
    )


def q_residual(lambda_value: float, h0: float) -> float:
    return sigma_data(lambda_value, h0)[0] - 2.0 / 3.0


def root_scan(
    f,
    grid: Iterable[float],
    skip_if,
    dedup_tol: float = 1.0e-8,
) -> list[float]:
    roots: list[float] = []
    prev_x = None
    prev_v = None
    for x in grid:
        if skip_if(x):
            prev_x = None
            prev_v = None
            continue
        v = f(x)
        if not np.isfinite(v):
            prev_x = None
            prev_v = None
            continue
        if prev_v is not None and prev_v * v < 0.0:
            root = brentq(f, prev_x, x)
            if not roots or min(abs(root - old) for old in roots) > dedup_tol:
                roots.append(root)
        prev_x = x
        prev_v = v
    return roots


print("=" * 88)
print("Koide Higgs-dressed resolvent root theorem")
print("=" * 88)

w4_zero = H_lift_missing_axis(0.0)
w4_zero_eigs, _ = np.linalg.eigh(w4_zero)
lambda_slack = Q_PLUS_STAR + DELTA_STAR - E1

check(
    "The missing-axis lift W_4(0) is Hermitian with poles given by one O_0 zero plus the three lifted H_* eigenvalues",
    np.allclose(w4_zero, w4_zero.conj().T),
    detail=f"poles={np.round(w4_zero_eigs, 6).tolist()}",
)
check(
    "The small positive chamber-slack scalar lies strictly between the O_0 pole and the positive lifted H_* pole",
    0.0 < lambda_slack < float(w4_zero_eigs[-1]),
    detail=f"lambda_slack={lambda_slack:.15f}",
)

# Global root scan on h0 = 0.
lambda_grid = np.linspace(-5.0, 5.0, 30001)
roots_h0_zero = root_scan(
    lambda x: q_residual(x, 0.0),
    lambda_grid,
    skip_if=lambda x: np.min(np.abs(x - w4_zero_eigs)) < 2.0e-4,
)

check(
    "At h_0 = 0 the missing-axis resolvent family has exactly eight Q=2/3 roots on [-5,5]",
    len(roots_h0_zero) == 8,
    detail=f"roots={[round(r, 12) for r in roots_h0_zero]}",
)

positive_roots = [r for r in roots_h0_zero if r > 0.0]
small_positive_root = min(positive_roots)
q_star, cs_star, sigma_eigs_star, sigma_diag_star, _ = sigma_data(small_positive_root, 0.0)

check(
    "There is a unique small positive Q=2/3 root below 0.1",
    sum(1 for r in roots_h0_zero if 0.0 < r < 0.1) == 1,
    detail=f"lambda_*={small_positive_root:.15f}",
)
check(
    "At the small positive root the induced species spectrum lies on Koide Q=2/3",
    abs(q_star - 2.0 / 3.0) < 1.0e-12,
    detail=f"Q={q_star:.15f}",
)
check(
    "That root also gives a strong charged-lepton direction match",
    cs_star > 0.996,
    detail=f"cos={cs_star:.12f}",
)

gap = small_positive_root - lambda_slack
check(
    "The exact Koide root is close to chamber slack but not equal to it",
    abs(gap) < 1.0e-4 and abs(gap) > 1.0e-5,
    detail=f"lambda_* - lambda_slack = {gap:+.12e}",
)

q_slack, cs_slack, sigma_eigs_slack, sigma_diag_slack, _ = sigma_data(lambda_slack, 0.0)
check(
    "At h_0 = 0, chamber slack is only a near-hit rather than an exact Koide root",
    abs(q_slack - 2.0 / 3.0) > 1.0e-5 and abs(q_slack - 2.0 / 3.0) < 5.0e-4,
    detail=f"Q_slack={q_slack:.12f}, cos_slack={cs_slack:.12f}",
)

# For fixed chamber slack, scan h0 roots.
h0_grid = np.linspace(-0.01, 0.08, 30001)
h0_roots = root_scan(
    lambda h0: q_residual(lambda_slack, h0),
    h0_grid,
    skip_if=lambda _h0: False,
)

check(
    "At fixed chamber slack there are exactly two h_0 corrections restoring Q=2/3 on the tested window",
    len(h0_roots) == 2,
    detail=f"h0_roots={[round(r, 12) for r in h0_roots]}",
)

small_h0_root = min(r for r in h0_roots if r > -1.0e-6)
q_h0, cs_h0, sigma_eigs_h0, sigma_diag_h0, _ = sigma_data(lambda_slack, small_h0_root)
check(
    "One of those h_0 corrections is microscopic and positive",
    0.0 < small_h0_root < 1.0e-4,
    detail=f"h0_small={small_h0_root:.12e}",
)
check(
    "With that microscopic h_0 correction, chamber slack hits exact Koide Q=2/3",
    abs(q_h0 - 2.0 / 3.0) < 1.0e-12,
    detail=f"Q={q_h0:.15f}, cos={cs_h0:.12f}",
)

print()
print("Interpretation:")
print("  The missing-axis Higgs-dressed resolvent avenue is not a generic transport")
print("  search anymore. Once the natural O_0 baseline h_0=0 is fixed, Koide lives")
print("  on isolated scalar lambda-roots of the resolvent family.")
print("  The best-supported root is the unique small positive one near chamber slack.")
print("  So this avenue now reduces to one scalar lambda-law (or the equivalent")
print("  two-parameter near-surface law on (lambda, h_0)), not a broad functional-class")
print("  ambiguity.")
print()
print(f"  small positive lambda_* = {small_positive_root:.15f}")
print(f"  chamber slack           = {lambda_slack:.15f}")
print(f"  sigma eigs(lambda_*)    = {np.round(sigma_eigs_star, 12).tolist()}")
print(f"  sigma diag(lambda_*)    = {np.round(sigma_diag_star, 12).tolist()}")
print(f"  tiny h_0 at slack       = {small_h0_root:.12e}")
print()
print(f"PASS={PASS} FAIL={FAIL}")
if FAIL > 0:
    raise SystemExit(1)
