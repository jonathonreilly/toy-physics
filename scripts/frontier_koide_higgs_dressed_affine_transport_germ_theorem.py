#!/usr/bin/env python3
"""
Frontier runner — Koide Higgs-dressed affine transport germ theorem.

Companion to
`docs/KOIDE_HIGGS_DRESSED_AFFINE_TRANSPORT_GERM_THEOREM_NOTE_2026-04-20.md`.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

from frontier_koide_higgs_dressed_chamber_link_renormalization_theorem import (
    q_residual,
)


PASS = 0
FAIL = 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    print(f"  [{status}] {label}" + (f"  ({detail})" if detail else ""))


LAMBDA_STAR = 0.01580870328539511
LAMBDA_SLACK = 0.01585551149054787
H0_SLACK = 4.489898313255e-05


def local_branch_root(lambda_value: float, lo: float = -2.0e-4, hi: float = 2.0e-4) -> float:
    grid = np.linspace(lo, hi, 2001)
    prev_x = None
    prev_v = None
    roots: list[float] = []
    for x in grid:
        v = q_residual(lambda_value, x)
        if not np.isfinite(v):
            prev_x = None
            prev_v = None
            continue
        if prev_v is not None and prev_v * v < 0.0:
            roots.append(brentq(lambda h0: q_residual(lambda_value, h0), prev_x, x))
        prev_x = x
        prev_v = v
    if len(roots) != 1:
        raise ValueError(f"expected exactly one local branch root, got {roots}")
    return roots[0]


print("=" * 88)
print("Koide Higgs-dressed affine transport germ theorem")
print("=" * 88)

window = 1.2e-4
sample_lambdas = np.linspace(LAMBDA_STAR - window, LAMBDA_STAR + window, 13)
branch_roots = np.array([local_branch_root(lam) for lam in sample_lambdas])
dl = sample_lambdas - LAMBDA_STAR

check(
    "Across the physical micro-window there is a unique small Koide branch root at every sampled lambda",
    np.all(np.abs(branch_roots) < 1.2e-4),
    detail=f"h0(lambda)={[round(x, 12) for x in branch_roots.tolist()]}",
)
check(
    "The local branch crosses the physical root exactly at h_0(lambda_*) = 0",
    abs(branch_roots[len(branch_roots) // 2]) < 1.0e-15,
)
check(
    "The local branch is monotone increasing across the full tested micro-window",
    np.all(np.diff(branch_roots) > 0.0),
)

linear = np.polyfit(dl, branch_roots, 1)
quadratic = np.polyfit(dl, branch_roots, 2)
cubic = np.polyfit(dl, branch_roots, 3)

linear_err = float(np.max(np.abs(np.polyval(linear, dl) - branch_roots)))
quadratic_err = float(np.max(np.abs(np.polyval(quadratic, dl) - branch_roots)))
cubic_err = float(np.max(np.abs(np.polyval(cubic, dl) - branch_roots)))

check(
    "The local transport branch is affine to about 7e-11 across the visible chamber window",
    linear_err < 1.0e-10,
    detail=f"linear_err={linear_err:.3e}",
)
check(
    "A quadratic germ resolves the same branch to numerical machine precision",
    quadratic_err < 1.0e-12,
    detail=f"quadratic_err={quadratic_err:.3e}",
)
check(
    "A cubic fit gives no meaningful improvement over the quadratic germ on this window",
    cubic_err <= quadratic_err + 1.0e-13,
    detail=f"cubic_err={cubic_err:.3e}",
)

alpha = float(linear[0])
beta = float(quadratic[0])
check(
    "The affine germ coefficient is stable on the physical branch",
    0.95 < alpha < 0.97,
    detail=f"alpha={alpha:.12f}",
)
check(
    "The quadratic curvature coefficient is tiny and negative on the same window",
    -0.02 < beta < 0.0,
    detail=f"beta={beta:.12f}",
)

dl_slack = LAMBDA_SLACK - LAMBDA_STAR
pred_linear = float(np.polyval(linear, dl_slack))
pred_quadratic = float(np.polyval(quadratic, dl_slack))
pred_cubic = float(np.polyval(cubic, dl_slack))

check(
    "The visible chamber-link correction is already predicted to 3e-11 by the affine germ alone",
    abs(pred_linear - H0_SLACK) < 5.0e-11,
    detail=f"linear_pred={pred_linear:.12e}",
)
check(
    "The quadratic germ reproduces the exact chamber-link correction to machine precision",
    abs(pred_quadratic - H0_SLACK) < 1.0e-12,
    detail=f"quadratic_pred={pred_quadratic:.12e}",
)
check(
    "The cubic germ gives the same chamber-link correction to the displayed digits",
    abs(pred_cubic - H0_SLACK) < 1.0e-12,
    detail=f"cubic_pred={pred_cubic:.12e}",
)

print()
print("Interpretation:")
print("  On the physical micro-window around lambda_*, the exact Koide branch is")
print("  already an affine transport germ to 7e-11, with only tiny quadratic")
print("  curvature. The visible chamber-link correction at lambda_slack is not a")
print("  new mechanism; it lies on that same local branch.")
print("  So the remaining microscopic object can be read as:")
print("      derive the affine O_0 transport renormalization coefficient alpha")
print("  (and, if desired, its tiny higher-order curvature corrections).")
print()
print(f"  alpha = {alpha:.12f}")
print(f"  beta  = {beta:.12f}")
print(f"  linear prediction at lambda_slack    = {pred_linear:.12e}")
print(f"  quadratic prediction at lambda_slack = {pred_quadratic:.12e}")
print(f"  exact h0(lambda_slack)               = {H0_SLACK:.12e}")
print()
print(f"PASS={PASS} FAIL={FAIL}")
if FAIL:
    raise SystemExit(1)
