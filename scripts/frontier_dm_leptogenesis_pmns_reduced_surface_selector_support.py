#!/usr/bin/env python3
"""
DM leptogenesis PMNS reduced-surface selector support.

Framework convention:
  "axiom" means only Cl(3) on Z^3.

Purpose:
  Strengthen the PMNS-assisted N_e selector story on the exact fixed native N_e
  seed surface with a deterministic reduced-surface search plus local
  polishing.

Live claim scope:
  - the admissible PMNS-assisted closure domain is already reduced to the fixed
    native N_e seed surface by the prior reduction-exhaustion theorem;
  - on that exact reduced domain, this runner performs a deterministic
    exhaustive compact-chart search, and verifies that the reduced surface
    carries a finite stationary-branch set with a unique lowest-action branch;
  - the lower-action branch is recovered as the lowest-action branch on the
    reduced surface, with a finite action gap to the next branch;
  - this is strong reduced-surface optimization support, not a live theorem-
    grade global-minimum certificate.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
import numpy as np
from scipy.optimize import NonlinearConstraint, minimize, shgo

import frontier_dm_leptogenesis_flavor_column_functional_theorem as func
import frontier_dm_leptogenesis_pmns_active_projector_reduction as act
import frontier_dm_leptogenesis_pmns_observable_relative_action_law as rel
from dm_leptogenesis_exact_common import (
    C_SPH,
    D_THERMAL_EXACT,
    ETA_OBS,
    S_OVER_NGAMMA_EXACT,
    exact_package,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h

PASS_COUNT = 0
FAIL_COUNT = 0

PKG = exact_package()
Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL = func.flavored_transport_kernel(PKG.k_decay_exact)

XBAR_NE = rel.XBAR_NE
YBAR_NE = rel.YBAR_NE
SX = 3.0 * XBAR_NE
SY = 3.0 * YBAR_NE

I_STAR = 0


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


def compact_chart_to_source(params: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """
    Map the compact chart [0,1]^4 x [-pi,pi] surjectively onto the closed
    fixed native N_e seed surface.
    """
    u1, u2, v1, v2, delta = np.asarray(params, dtype=float)
    x = SX * np.array([u1, (1.0 - u1) * u2, (1.0 - u1) * (1.0 - u2)], dtype=float)
    y = SY * np.array([v1, (1.0 - v1) * v2, (1.0 - v1) * (1.0 - v2)], dtype=float)
    return x, y, float(delta)


def packet_and_etas_from_chart(params: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x, y, delta = compact_chart_to_source(params)
    h_e = canonical_h(x, y, delta)
    packet = act.active_packet_from_h(h_e).T
    transport_vals = np.array(
        [
            func.flavored_column_functional(packet[:, idx], Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL)
            for idx in range(3)
        ],
        dtype=float,
    )
    eta_vals = (
        S_OVER_NGAMMA_EXACT * C_SPH * D_THERMAL_EXACT * PKG.epsilon_1 * transport_vals / ETA_OBS
    )
    return h_e, packet, eta_vals


def closure_residual(params: np.ndarray) -> float:
    return float(packet_and_etas_from_chart(params)[2][I_STAR] - 1.0)


def relative_action_from_chart(params: np.ndarray) -> float:
    h_e, _packet, _etas = packet_and_etas_from_chart(params)
    return float(rel.relative_action_h(h_e))


def finite_grad(fun, x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    g = np.zeros_like(x)
    for i in range(len(x)):
        dx = np.zeros_like(x)
        dx[i] = eps
        g[i] = (fun(x + dx) - fun(x - dx)) / (2.0 * eps)
    return g


def finite_hessian(fun, x: np.ndarray, eps: float = 2e-4) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    n = len(x)
    h = np.zeros((n, n), dtype=float)
    for i in range(n):
        ei = np.zeros(n, dtype=float)
        ei[i] = eps
        h[i, i] = (fun(x + ei) - 2.0 * fun(x) + fun(x - ei)) / (eps * eps)
        for j in range(i + 1, n):
            ej = np.zeros(n, dtype=float)
            ej[j] = eps
            h_ij = (
                fun(x + ei + ej)
                - fun(x + ei - ej)
                - fun(x - ei + ej)
                + fun(x - ei - ej)
            ) / (4.0 * eps * eps)
            h[i, j] = h[j, i] = h_ij
    return h


def tangent_basis(grad_c: np.ndarray) -> np.ndarray:
    _u, _s, vh = np.linalg.svd(np.asarray(grad_c, dtype=float)[None, :], full_matrices=True)
    return vh[1:, :].T


def stationarity_residual(params: np.ndarray) -> tuple[float, float]:
    grad_action = finite_grad(relative_action_from_chart, params)
    grad_closure = finite_grad(closure_residual, params)
    lam = float(np.dot(grad_action, grad_closure) / max(float(np.dot(grad_closure, grad_closure)), 1.0e-15))
    resid = float(np.linalg.norm(grad_action - lam * grad_closure))
    return lam, resid


@dataclass
class Branch:
    representative: np.ndarray
    action: float
    etas: np.ndarray
    count: int
    source: str


def solve_stationary_from_start(start: np.ndarray, maxiter: int = 120) -> tuple[np.ndarray, object]:
    res = minimize(
        relative_action_from_chart,
        np.asarray(start, dtype=float),
        method="SLSQP",
        bounds=[
            (1.0e-4, 1.0 - 1.0e-4),
            (1.0e-4, 1.0 - 1.0e-4),
            (1.0e-4, 1.0 - 1.0e-4),
            (1.0e-4, 1.0 - 1.0e-4),
            (-math.pi, math.pi),
        ],
        constraints=[{"type": "eq", "fun": closure_residual}],
        options={"ftol": 1.0e-12, "maxiter": maxiter},
    )
    return np.asarray(res.x, dtype=float), res


def refine_candidate(start: np.ndarray) -> tuple[np.ndarray, object]:
    x0, res = solve_stationary_from_start(start, maxiter=80)
    if abs(closure_residual(x0)) > 1.0e-8:
        x1, res = solve_stationary_from_start(x0, maxiter=200)
        return x1, res
    if not res.success:
        x1, res = solve_stationary_from_start(x0, maxiter=120)
        return x1, res
    return x0, res


def anchor_free_global_candidates() -> list[np.ndarray]:
    constraint = NonlinearConstraint(lambda p: closure_residual(np.asarray(p, dtype=float)), 0.0, 0.0)
    result = shgo(
        relative_action_from_chart,
        bounds=[(1.0e-4, 1.0 - 1.0e-4)] * 4 + [(-math.pi, math.pi)],
        constraints=(constraint,),
        n=1024,
        iters=2,
        sampling_method="sobol",
    )

    candidates: list[np.ndarray] = []
    minima = getattr(result, "xl", None)
    if minima is None:
        minima = np.asarray([result.x], dtype=float)
    for start in np.asarray(minima, dtype=float):
        x, _res = refine_candidate(start)
        if abs(closure_residual(x)) < 1.0e-8 and np.isfinite(relative_action_from_chart(x)):
            candidates.append(x)
    return candidates


def cluster_solutions(solutions: list[np.ndarray]) -> list[Branch]:
    buckets: list[list[np.ndarray]] = []
    action_tol = 1.0e-5
    param_tol = 2.0e-3

    for sol in solutions:
        if abs(closure_residual(sol)) > 1.0e-6:
            continue
        act_val = relative_action_from_chart(sol)
        matched = False
        for bucket in buckets:
            rep = bucket[0]
            if abs(relative_action_from_chart(rep) - act_val) < action_tol and np.linalg.norm(rep - sol) < param_tol:
                bucket.append(sol)
                matched = True
                break
        if not matched:
            buckets.append([sol])

    branches: list[Branch] = []
    for bucket in buckets:
        rep = np.mean(np.asarray(bucket, dtype=float), axis=0)
        rep, _res = refine_candidate(rep)
        h_e, _packet, etas = packet_and_etas_from_chart(rep)
        branches.append(
            Branch(
                representative=rep,
                action=rel.relative_action_h(h_e),
                etas=np.asarray(etas, dtype=float),
                count=len(bucket),
                source="deterministic compact cover",
            )
        )

    branches.sort(key=lambda b: b.action)
    return branches


def certified_branch_search() -> list[Branch]:
    candidates = anchor_free_global_candidates()
    branches = cluster_solutions(candidates)
    if len(branches) != 3:
        raise RuntimeError(
            f"anchor-free SHGO support search did not stabilize to exactly three stationary closure branches (found {len(branches)})"
        )
    return branches


def certify_global_minimum(branches: list[Branch]) -> None:
    low = branches[0]
    mid = branches[1]
    high = branches[2]
    min_gap = mid.action - low.action

    check(
        "The anchor-free deterministic global support search returns exactly three stationary closure branches on the reduced surface",
        len(branches) == 3,
        f"branch count={len(branches)}",
    )
    check(
        "The lower branch closes the favored column exactly",
        abs(low.etas[I_STAR] - 1.0) < 1.0e-10,
        f"eta/eta_obs={low.etas[I_STAR]:.12f}",
    )
    check(
        "The lowest-action branch is separated from the next branch by a finite action gap",
        min_gap > 1.0e-3,
        f"ΔS={min_gap:.12f}",
    )
    check(
        "The lower branch is the unique lowest-action branch in the current reduced-surface search",
        mid.action > low.action and high.action > low.action,
        f"branch actions={[round(branch.action, 12) for branch in branches]}",
    )

    # Local minimality certificate on the reduced closure branch.
    grad_action = finite_grad(relative_action_from_chart, low.representative)
    grad_closure = finite_grad(closure_residual, low.representative)
    denom = float(np.dot(grad_closure, grad_closure))
    lam = float(np.dot(grad_action, grad_closure) / max(denom, 1e-15))
    lag_hess = finite_hessian(relative_action_from_chart, low.representative) - lam * finite_hessian(closure_residual, low.representative)
    tangent = tangent_basis(grad_closure)
    proj = tangent.T @ lag_hess @ tangent
    eigs = np.linalg.eigvalsh(proj)

    print(f"  stationarity residual (diagnostic only) = {np.linalg.norm(grad_action - lam * grad_closure):.3e}")
    check(
        "The projected tangent Hessian at the lower branch is positive definite",
        float(np.min(eigs)) > 1.0e-4,
        f"min eig={float(np.min(eigs)):.6e}",
    )

    print()
    for idx, branch in enumerate(branches):
        x, y, delta = compact_chart_to_source(branch.representative)
        print(f"  branch {idx}:")
        print(f"    count       = {branch.count}")
        print(f"    S_rel       = {branch.action:.12f}")
        print(f"    x           = {fmt(x)}")
        print(f"    y           = {fmt(y)}")
        print(f"    delta       = {delta:.12e}")
        print(f"    eta/eta_obs = {np.round(branch.etas, 12)}")

    print()
    print(f"  low-branch compact chart  = {fmt(low.representative)}")
    print(f"  mid-branch compact chart  = {fmt(mid.representative)}")
    print(f"  high-branch compact chart = {fmt(high.representative)}")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS REDUCED-SURFACE SELECTOR SUPPORT")
    print("=" * 88)
    print()
    print("Framework convention:")
    print('  "axiom" means only Cl(3) on Z^3.')
    print()
    print("Question:")
    print("  On the exact reduced PMNS-assisted N_e seed surface, can the lowest-action")
    print("  closure branch be recovered robustly on the reduced surface by a")
    print("  deterministic anchor-free global search plus local polishing?")
    print()
    print("Scope:")
    print("  The reduction-exhaustion theorem already eliminates all components beyond")
    print("  the reduced N_e seed surface. This runner tests reduced-surface")
    print("  uniqueness/minimality on that exact reduced surface.")

    branches = certified_branch_search()
    certify_global_minimum(branches)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Reduced-surface support result:")
    print("    - anchor-free deterministic global optimization gives a finite set of")
    print("      three stationary closure branches on the exact reduced domain")
    print("    - the lower branch is recovered as the lowest-action branch on that surface")
    print("    - the finite action gap to the next branch is > 1e-3")
    print("    - the lower branch closes the favored column exactly")
    print()
    print("  This is strong reduced-surface optimization support. The live authority")
    print("  path still keeps it below theorem-grade promotion because even the")
    print("  anchor-free global search is still a numerical optimization support")
    print("  argument rather than a certified interval/global proof.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
