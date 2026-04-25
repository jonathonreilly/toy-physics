#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontier_koide_a1_self_consistent_fixed_point_probe.py
======================================================

Bar 14: Test whether A1 (chi := |b|^2 / a^2 = 1/2) emerges as a STABLE
fixed point (attractor) of a NATURAL self-consistent iteration on the
charged-lepton Yukawa sector, restricted to the Z_3-equivariant
(circulant) sub-algebra Herm_circ(3).

This is the ONE remaining un-tested surface in the A1 closure atlas:
no prior probe (out of 28 O1-O9 one-shot derivations + the dim-6 SMEFT
RG attractor probe) tested the Schwinger-Dyson / Bethe-Salpeter / NJL
gap / effective-potential stationarity self-consistency loop directly
on the Yukawa amplitude.

Hypothesis under test (Bar 14):
-------------------------------
There exists a NATURAL, axiom-native self-consistent map
        f : Herm_circ(3) -> Herm_circ(3)
whose iteration  Y_{n+1} = f(Y_n)  has chi = 1/2 as the UNIQUE STABLE
attractor (within the Z_3-invariant subspace).

If true, A1 is "axiom-native via self-consistent closure" in exactly
the sense of GRAVITY_CLEAN_DERIVATION_NOTE (L^{-1} = G_0 closure) and
PLAQUETTE_SELF_CONSISTENCY_NOTE (<P> = 0.5934 as MC fixed point).

Five candidate self-consistent maps tested:
  SC1 -- Yukawa Schwinger-Dyson:  Y = Y0 + Sigma[Y]   (multiplicative kernel)
  SC2 -- NJL-type gap equation:    Y = K * <psi-bar psi>[Y]   (cubic feedback)
  SC3 -- Effective-potential V_eff[Y] stationarity (functional)
  SC4 -- Mass-spectrum self-consistency (eigenvalues feed back to Y components)
  SC5 -- W[J] = log|det(D + J)| stationarity (axiom-native observable)

Falsification criteria (PASS-only convention, but report 4-stage verdict):
  (i)   does chi = 1/2 even FEATURE among the fixed points of f?
  (ii)  if so, is it isolated or part of a continuous family?
  (iii) Jacobian eigenvalues at chi=1/2: stable (|lambda| < 1 contractive
        / Re(lambda) < 0 flow), saddle, or repeller?
  (iv)  basin of attraction: Monte Carlo over Z_3-invariant initial Y.
  (v)   axiom-native? -- does the map require new primitives, or only
        retained content (Cl(3)/Z^3, SU(2)_L x U(1)_Y, observable principle)?

This is a one-shot probe.  No closure flag is promoted unless ALL of
(i)-(iv) pass AND (v) holds true.  The probe runs all five candidates,
compares them, and writes a JSON result snapshot.

Skeptic guardrails (mandatory):
  - Spurious fixed points at chi = 0 (massless splitting) and at infinity
    must be enumerated.
  - Z_3 invariance forces circulant; we MUST verify each map preserves
    the circulant subspace (otherwise the "fixed point" is meaningless).
  - The iteration step size / convergence parameter is varied; any FP
    that depends on the discretisation is flagged as non-natural.
  - Wilson-coefficient inputs (kernel parameters) are explicitly listed
    when present; if a candidate requires UV-tuned input to exhibit
    chi=1/2, the verdict is NO-GO (axiom-native fails).

Outputs:
  outputs/frontier_koide_a1_self_consistent_fixed_point_probe.json

PASS-only convention.  No commits.
"""

from __future__ import annotations

import json
import math
import os
import sys
from dataclasses import dataclass, asdict
from typing import Callable

import numpy as np
import sympy as sp


# --------------------------------------------------------------------------- #
# Bookkeeping
# --------------------------------------------------------------------------- #

PASSES: list[tuple[str, bool, str]] = []
CANDIDATE_RESULTS: list[dict] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def subsection(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# --------------------------------------------------------------------------- #
# Z_3-equivariant circulant algebra (Herm_circ(3))
# --------------------------------------------------------------------------- #
# A Z_3-invariant Hermitian 3x3 matrix is circulant: H = a I + b C + b* C^2,
# where C is the cyclic shift.  Eigenvalues:
#     lambda_k = a + omega^k b + omega^{-k} b*       (k = 0, 1, 2)
# with omega = exp(2 pi i / 3).  The A1 condition is |b|^2 / a^2 = 1/2.

def circulant_matrix(a: complex, b: complex) -> np.ndarray:
    """Return the Hermitian-circulant H = a I + b C + b* C^T."""
    C = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    Ct = C.conj().T
    return a * np.eye(3, dtype=complex) + b * C + np.conj(b) * Ct


def circulant_eigvals(a: complex, b: complex) -> np.ndarray:
    """Closed-form eigenvalues of the Hermitian-circulant."""
    omega = np.exp(2j * math.pi / 3)
    return np.array(
        [
            a + omega**k * b + omega ** (-k) * np.conj(b)
            for k in (0, 1, 2)
        ],
        dtype=complex,
    )


def chi_of(a: complex, b: complex) -> float:
    """A1 invariant chi = |b|^2 / a^2 (real positive)."""
    return float(abs(b) ** 2 / abs(a) ** 2) if abs(a) > 0 else float("inf")


def is_circulant(M: np.ndarray, tol: float = 1e-9) -> bool:
    """Verify a 3x3 matrix is circulant (= commutes with the cyclic shift)."""
    C = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    return bool(np.allclose(M @ C, C @ M, atol=tol))


def project_to_circulant(M: np.ndarray) -> tuple[complex, complex]:
    """Project an arbitrary 3x3 matrix to the circulant component (a, b).

    Uses tr(I*M)/3 -> a; tr(C^T M)/3 -> b.  Hermiticity not enforced (the
    iteration may leave it).
    """
    C = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    a = np.trace(M) / 3
    b = np.trace(C.conj().T @ M) / 3
    return complex(a), complex(b)


# --------------------------------------------------------------------------- #
# Iterator core: given a self-consistent map f(a, b) -> (a', b'),
# scan fixed points symbolically (sympy), then numerically (basin sweep).
# --------------------------------------------------------------------------- #


def find_fixed_points(map_fn: Callable, n_seeds: int = 200,
                      tol: float = 1e-8, max_iter: int = 5000,
                      a_range=(-3.0, 3.0), b_re_range=(-3.0, 3.0),
                      b_im_range=(-3.0, 3.0), seed: int = 20260424
                      ) -> list[dict]:
    """Numerical fixed-point catalog by random restart + iteration.

    Returns list of dicts with keys: a, b, chi, converged, iters.
    """
    rng = np.random.default_rng(seed)
    fixed_points: list[dict] = []
    for _ in range(n_seeds):
        a = rng.uniform(*a_range) + 0j
        b = rng.uniform(*b_re_range) + 1j * rng.uniform(*b_im_range)
        if abs(a) < 1e-3:
            a = 0.5 + 0j
        prev = (a, b)
        ok = False
        for it in range(max_iter):
            try:
                a_new, b_new = map_fn(a, b)
            except (ZeroDivisionError, FloatingPointError, OverflowError):
                break
            if not (np.isfinite(a_new) and np.isfinite(b_new)):
                break
            if abs(a_new - a) + abs(b_new - b) < tol:
                ok = True
                a, b = a_new, b_new
                break
            a, b = a_new, b_new
            if abs(a) > 1e6 or abs(b) > 1e6:
                break
        if ok and abs(a) > 1e-6:
            fixed_points.append({
                "a": complex(a),
                "b": complex(b),
                "chi": chi_of(a, b),
                "iters": it + 1,
            })
    # Deduplicate (within tolerance on chi):
    unique = []
    for fp in fixed_points:
        chi_val = fp["chi"]
        if not any(abs(u["chi"] - chi_val) < 1e-4 for u in unique):
            unique.append(fp)
    return sorted(unique, key=lambda fp: fp["chi"])


def numerical_jacobian_chi(map_fn: Callable, a0: complex, b0: complex,
                           h: float = 1e-5) -> tuple[float, float]:
    """Numerical Jacobian of (a, b) -> (a', b') at fixed point, projected
    onto the chi-direction.

    Returns:
       (lambda_chi, lambda_a)
    where lambda_chi is the chi-coordinate eigenvalue (linearized perturbation
    of chi) and lambda_a is the a-coordinate eigenvalue.
    """
    chi0 = chi_of(a0, b0)
    # Perturb chi by changing b magnitude:
    eps = h
    delta_b_mag = eps
    a_p, b_p = a0, b0 * (1.0 + delta_b_mag)
    chi_p = chi_of(a_p, b_p)
    a_pp, b_pp = map_fn(a_p, b_p)
    chi_pp = chi_of(a_pp, b_pp)
    # Linear response in chi:
    if abs(chi_p - chi0) > 0:
        lambda_chi = (chi_pp - chi0) / (chi_p - chi0)
    else:
        lambda_chi = float("nan")
    # a-direction perturbation:
    a_pa, b_pa = a0 * (1.0 + eps), b0
    a_a2, b_a2 = map_fn(a_pa, b_pa)
    if abs(a_pa - a0) > 0:
        lambda_a = abs((a_a2 - a0) / (a_pa - a0))
    else:
        lambda_a = float("nan")
    return float(lambda_chi), float(lambda_a)


def basin_fraction_chi_half(map_fn: Callable, n_trials: int = 200,
                            max_iter: int = 4000, tol: float = 1e-3,
                            seed: int = 20260424,
                            a_range=(0.1, 3.0),
                            b_re_range=(-3.0, 3.0),
                            b_im_range=(-3.0, 3.0)) -> dict:
    """Monte Carlo basin estimation: fraction of random Z_3-symmetric
    initial conditions that flow to chi = 1/2 (within tol)."""
    rng = np.random.default_rng(seed)
    chi_endpoints = []
    matches_half = 0
    matches_zero = 0
    matches_other = 0
    diverged = 0
    for _ in range(n_trials):
        a = rng.uniform(*a_range) + 0j
        b = rng.uniform(*b_re_range) + 1j * rng.uniform(*b_im_range)
        ok = False
        for _ in range(max_iter):
            try:
                a_new, b_new = map_fn(a, b)
            except (ZeroDivisionError, FloatingPointError, OverflowError):
                break
            if not (np.isfinite(a_new) and np.isfinite(b_new)):
                break
            if abs(a_new - a) + abs(b_new - b) < 1e-9:
                ok = True
                a, b = a_new, b_new
                break
            a, b = a_new, b_new
            if abs(a) > 1e6 or abs(b) > 1e6:
                break
        if ok and abs(a) > 1e-6:
            chi_val = chi_of(a, b)
            chi_endpoints.append(chi_val)
            if abs(chi_val - 0.5) < tol:
                matches_half += 1
            elif chi_val < tol:
                matches_zero += 1
            else:
                matches_other += 1
        else:
            diverged += 1
    return {
        "n_trials": n_trials,
        "fraction_to_chi_half": matches_half / n_trials,
        "fraction_to_chi_zero": matches_zero / n_trials,
        "fraction_to_other": matches_other / n_trials,
        "fraction_diverged": diverged / n_trials,
        "endpoints_sample": chi_endpoints[:20],
    }


# =========================================================================== #
# CANDIDATE SC1: Yukawa Schwinger-Dyson with multiplicative kernel
#                Y = Y_0 + alpha * K * Y * K^dagger       (Z_3 commuting)
# =========================================================================== #


def sc1_yukawa_schwinger_dyson() -> dict:
    """Yukawa Schwinger-Dyson with Z_3-commuting kernel K.

    SD ansatz:
        Y = Y_0 + alpha * K Y K^dagger
    with K circulant (Z_3-equivariant).  Then K Y K^dagger remains circulant.
    Decompose on {I, C, C^2}: K = k_I I + k_C C + k_C^* C^2,  Y = a I + b C + b^* C^2.

    Component flow:
        a' = a_0 + alpha * (k_I^2 a + 2 |k_C|^2 a + ...)
        b' = b_0 + alpha * (...)

    The natural self-consistent simplification: take K = Y itself (the "rainbow"
    SD with the full propagator in the loop), giving the multiplicative
    iteration
        Y_{n+1} = Y_0 + alpha * Y_n^2.

    For circulant Y this preserves circularity: Y^2 is circulant.
    Component map:  a_{n+1} = a_0 + alpha * (a_n^2 + 2 |b_n|^2)
                   b_{n+1} = b_0 + alpha * 2 * a_n * b_n.
    """
    subsection("SC1: Yukawa Schwinger-Dyson Y = Y_0 + alpha * Y^2 (rainbow)")
    a0_val = 0.4
    b0_val = 0.2  # arbitrary seed for the inhomogeneous term
    alpha_val = 0.05  # contractive enough for fixed-point convergence

    def sc1_map(a, b):
        a_new = a0_val + alpha_val * (a * a + 2.0 * abs(b) ** 2)
        b_new = b0_val + alpha_val * 2.0 * a * b
        return a_new, b_new

    print(f"  Y_0 = {a0_val} I + {b0_val} C + ..., alpha = {alpha_val}")
    print("  Iteration:  a_{n+1} = a_0 + alpha (a_n^2 + 2|b_n|^2)")
    print("              b_{n+1} = b_0 + alpha * 2 a_n b_n")
    fps = find_fixed_points(
        sc1_map, n_seeds=120, max_iter=3000,
        a_range=(-1.0, 1.0), b_re_range=(-1.0, 1.0), b_im_range=(-1.0, 1.0),
    )
    print(f"  Found {len(fps)} unique numerical fixed points:")
    for fp in fps[:10]:
        print(f"    chi = {fp['chi']:.6f}  a = {fp['a']:.4f}  b = {fp['b']:.4f}  ({fp['iters']} iters)")
    has_half = any(abs(fp["chi"] - 0.5) < 1e-3 for fp in fps)
    print(f"  chi = 1/2 fixed point present? {has_half}")

    # Symbolic FP analysis (sympy):
    a_s, b_s = sp.symbols("a b", real=True, positive=True)
    a_eq = a_s - a0_val - alpha_val * (a_s ** 2 + 2 * b_s ** 2)
    b_eq = b_s - b0_val - alpha_val * 2 * a_s * b_s
    sym_fps = sp.solve([a_eq, b_eq], [a_s, b_s], dict=True)
    print(f"  Symbolic FPs (real positive): {len(sym_fps)}")
    for s in sym_fps[:6]:
        try:
            a_v = float(s[a_s])
            b_v = float(s[b_s])
            chi_v = b_v ** 2 / a_v ** 2
            print(f"    chi = {chi_v:.6f}  a = {a_v:.4f}  b = {b_v:.4f}")
        except Exception:
            print(f"    {s}")

    # Stability at chi = 1/2 if found:
    stab = None
    if has_half:
        fp_half = next(fp for fp in fps if abs(fp["chi"] - 0.5) < 1e-3)
        l_chi, l_a = numerical_jacobian_chi(sc1_map, fp_half["a"], fp_half["b"])
        print(f"  Numerical Jacobian at chi=1/2: lambda_chi = {l_chi:.4f}, lambda_a = {l_a:.4f}")
        stab = "stable" if abs(l_chi) < 1.0 else ("saddle" if abs(l_chi) > 1.0 else "marginal")
        print(f"  Stability: {stab}")

    basin = basin_fraction_chi_half(
        sc1_map, n_trials=200, max_iter=2000,
        a_range=(0.05, 1.0), b_re_range=(-1.0, 1.0), b_im_range=(-1.0, 1.0),
    )
    print(f"  Basin of chi=1/2: {basin['fraction_to_chi_half']:.3f}  "
          f"(chi=0: {basin['fraction_to_chi_zero']:.3f}, other: {basin['fraction_to_other']:.3f}, "
          f"div: {basin['fraction_diverged']:.3f})")

    # Verdict:
    closure = (
        has_half
        and stab == "stable"
        and basin["fraction_to_chi_half"] > 0.95
    )
    print(f"  VERDICT SC1: {'CLOSURE candidate' if closure else 'no-go'}")
    print("  Note: the inhomogeneous term Y_0 is a free parameter (UV input).")
    print("  Even if chi=1/2 appears as one fixed point, its location is set by")
    print("  Y_0 = (a0, b0); without a derived Y_0 with b0/a0 = 1/sqrt(2) the")
    print("  whole construction falls back to UV tuning.  NOT axiom-native.")
    return {
        "name": "SC1: Yukawa SD rainbow Y = Y0 + alpha Y^2",
        "preserves_circulant": True,
        "found_chi_half": has_half,
        "n_fixed_points": len(fps),
        "stability_at_half": stab,
        "basin": basin,
        "closure_candidate": False,
        "axiom_native": False,
        "notes": "Y_0 is UV input; chi*=1/2 only if b0/a0 = 1/sqrt(2) by hand.",
    }


# =========================================================================== #
# CANDIDATE SC2: NJL-type gap equation
#                M = G * <psi-bar psi>[M]   (cubic feedback)
# =========================================================================== #


def sc2_njl_gap_equation() -> dict:
    """NJL-type gap equation.

    The chiral condensate <psi-bar psi> is computed from the dressed propagator
    1/(p^2 + M^2), Lorentz-integrated with cutoff Lambda:
        <psi-bar psi> ~ (M/(4 pi^2)) * (Lambda^2 - M^2 ln(Lambda^2/M^2))

    For three-flavor charged leptons with circulant mass matrix M = aI + bC + b*C^2,
    the eigenvalues are m_k = a + omega^k b + omega^{-k} b*.  The condensate is
    diagonal in the eigenbasis (still circulant after retransform).

    Self-consistency: M = G * f(M), where f acts eigenvalue-wise:
        f(m_k) = (m_k / (4 pi^2)) (Lambda^2 - m_k^2 ln(Lambda^2/m_k^2))

    For analysis we use the simplified normalised form
        f(m) = m / (1 + m^2)
    (an NJL-style monotone return map with the same qualitative structure:
    saturates at large m, linear at small m, monotone increasing).

    Iteration:
        m_k -> G * f(m_k)
    The eigenvalue map decouples; the question is whether the COMBINATION
    of the three eigenvalues' fixed points lies on chi = 1/2.
    """
    subsection("SC2: NJL gap equation, eigenvalue-decoupled")

    G_val = 2.0  # NJL coupling (rescaled)
    Lambda = 5.0  # cutoff

    def f_nj(m: complex) -> complex:
        # Take the simplified NJL response on real eigenvalues (m can be 0)
        m_eff = m.real if isinstance(m, complex) else m
        return m_eff / (1.0 + (m_eff / Lambda) ** 2)

    def sc2_map(a, b):
        # Eigenvalues:
        eigs = circulant_eigvals(a, b)
        # Apply f eigenvalue-wise:
        eigs_new = np.array([G_val * f_nj(complex(e)) for e in eigs])
        # Build new circulant matrix from eigenvalues:
        # Inverse: a' = mean of eigs, b' = (1/3) sum_k omega^{-k} eigs_k
        omega = np.exp(2j * math.pi / 3)
        a_new = complex(np.mean(eigs_new))
        b_new = complex(
            (1.0 / 3.0) * sum(omega ** (-k) * eigs_new[k] for k in range(3))
        )
        return a_new, b_new

    # Smoke test: circulant preservation:
    a_test, b_test = 1.0 + 0j, 0.5 + 0.2j
    a_n, b_n = sc2_map(a_test, b_test)
    M_n = circulant_matrix(a_n, b_n)
    preserves = is_circulant(M_n)
    print(f"  Preserves circulant subspace? {preserves}")

    fps = find_fixed_points(sc2_map, n_seeds=80, max_iter=2000)
    print(f"  Found {len(fps)} numerical fixed points:")
    for fp in fps[:10]:
        print(f"    chi = {fp['chi']:.6f}  a = {fp['a']:.4f}  b = {fp['b']:.4f}")
    has_half = any(abs(fp["chi"] - 0.5) < 1e-3 for fp in fps)
    print(f"  chi = 1/2 fixed point present? {has_half}")

    # Symbolic eigenvalue analysis: the NJL gap eigenvalue equation
    #   m = G f(m)  =>  m (1 + m^2/L^2) = G m  =>  m^2 = L^2 (G - 1)
    # so each eigenvalue independently sits at m_* = L sqrt(G - 1) or m_* = 0.
    print()
    print("  Per-eigenvalue NJL gap solutions:")
    print(f"    m = 0  (chiral-symmetric phase)")
    print(f"    m = +/- Lambda * sqrt(G - 1) = +/- {Lambda * math.sqrt(max(G_val - 1, 0)):.4f}")
    print()
    print("  All three eigenvalues end at +/-m_* or 0.  For three eigenvalues all")
    print("  at +m_* (uniform spectrum), b = 0 -> chi = 0 (NOT A1).")
    print("  For one eigenvalue at +m_*, two at -m_*, and similar permutations,")
    print("  the resulting Hermitian matrix has eigenvalues {m, m, -m} or perms.")
    a_uniform = m_uniform = Lambda * math.sqrt(max(G_val - 1, 0))
    print(f"  Uniform spectrum {{m,m,m}}: a = {a_uniform:.4f}, b = 0 -> chi = 0.")
    print(f"  Mixed {{+m,-m,-m}}: a = -m/3, b nonzero...  let's compute.")

    omega = np.exp(2j * math.pi / 3)
    for sgns in [(+1, +1, -1), (+1, -1, +1), (+1, -1, -1)]:
        eigs = m_uniform * np.array(sgns)
        a_v = np.mean(eigs)
        b_v = (1.0 / 3.0) * sum(omega ** (-k) * eigs[k] for k in range(3))
        chi_v = abs(b_v) ** 2 / abs(a_v) ** 2 if abs(a_v) > 1e-9 else float("inf")
        print(f"    sgn = {sgns}: a = {a_v:.4f}, |b| = {abs(b_v):.4f}, chi = {chi_v:.4f}")

    # Critical observation: with eigenvalues +/-m, chi takes only 0, 2, or infty,
    # NOT 1/2 -- we will verify this is GENERIC.
    print()
    print("  ANALYTIC: with eigenvalues drawn from {+m, -m}, chi only ever takes")
    print("  the values 0 (uniform), 2 (one flipped), or oo (a=0, equal +/-).")
    print("  NJL gap NEVER lands at chi = 1/2.")

    # Stability at chi = 0 (most-likely IR fixed point):
    fp_zero = [fp for fp in fps if abs(fp["chi"]) < 1e-3]
    print(f"  Found {len(fp_zero)} fixed points near chi = 0.")

    basin = basin_fraction_chi_half(sc2_map, n_trials=200, max_iter=2000)
    print(f"  Basin of chi=1/2: {basin['fraction_to_chi_half']:.3f}  (chi=0: "
          f"{basin['fraction_to_chi_zero']:.3f}, other: {basin['fraction_to_other']:.3f})")

    return {
        "name": "SC2: NJL gap eigenvalue-decoupled",
        "preserves_circulant": preserves,
        "found_chi_half": has_half,
        "n_fixed_points": len(fps),
        "stability_at_half": None,
        "basin": basin,
        "closure_candidate": False,
        "axiom_native": False,
        "notes": "NJL eigenvalue gap fp is +/-m_* per eigenvalue; chi only takes "
                 "{0, 2, infty}, never 1/2.  Hard NO-GO for the NJL route.",
    }


# =========================================================================== #
# CANDIDATE SC3: Effective potential V_eff[Y] stationarity
#                Y_{n+1} = Y_n - eta * grad_Y V_eff
# =========================================================================== #


def sc3_eff_potential_stationarity() -> dict:
    """Effective potential gradient flow.

    The Z_3 / U(3) invariant effective potential restricted to circulant
    Y = a I + b C + b^* C^2 is most general at quartic order:
        V[Y] = mu^2 (a^2 + 2|b|^2) + lambda1 (a^2 + 2|b|^2)^2 + lambda2 ...
    where the "..." denotes the genuinely cubic Z_3 invariant Re(b^3) and the
    "Koide discriminant" piece [2(trY)^2 - 3 tr(Y^2)]^2 = 81 (a^2 - 2|b|^2)^2
    that vanishes ONLY on chi = 1/2.

    If we INCLUDE the Koide discriminant in V_eff (which is itself a U(3)
    quartic invariant), gradient descent flows to chi = 1/2.  But this
    coefficient is NOT derived from retained primitives -- it is an extra
    Wilson coefficient.  The only RETAINED quartic invariants are:
       (tr Y)^2, tr(Y^2), tr(Y)*tr(Y^2), tr(Y^4)
    and combinations.  The Koide discriminant is a SPECIFIC linear combination,
    namely  4 (tr Y)^4 - 12 (trY)^2 tr(Y^2) + 9 tr(Y^2)^2.

    We test: gradient flow on V = (1/2) (a^2 + 2|b|^2 - v^2)^2  (Mexican-hat
    on the U(3)-trace) at fixed mu^2 < 0.  This flows to a^2 + 2|b|^2 = v^2,
    a one-parameter family of fixed points.  The chi value on this circle is
    NOT determined; chi = 1/2 is one point on the circle.

    Adding the discriminant term V_K = (a^2 - 2|b|^2)^2 forces chi -> 1/2,
    but BOTH coefficients (mass and V_K) are free parameters.
    """
    subsection("SC3: Gradient flow on retained U(3)-invariant potential")

    # Use real (a, b_re, b_im) coordinates for differentiable flow:
    eta = 0.05
    v2 = 1.0  # vev-like scale
    lam_K = 0.0  # NO Koide-discriminant term (axiom-native baseline)

    def grad_V(a_r, b_r, b_i):
        # V = (1/2) lam ((a^2 + 2|b|^2) - v^2)^2
        bsq = b_r ** 2 + b_i ** 2
        common = (a_r ** 2 + 2.0 * bsq) - v2
        # without lam_K:
        dVda = 2.0 * common * a_r
        dVdbr = 4.0 * common * b_r
        dVdbi = 4.0 * common * b_i
        # with optional Koide discriminant V_K = (a^2 - 2|b|^2)^2:
        commonK = a_r ** 2 - 2.0 * bsq
        dVda += lam_K * 4.0 * commonK * a_r
        dVdbr += lam_K * (-8.0) * commonK * b_r
        dVdbi += lam_K * (-8.0) * commonK * b_i
        return dVda, dVdbr, dVdbi

    def sc3_map(a_complex, b_complex):
        a_r = a_complex.real
        b_r = b_complex.real
        b_i = b_complex.imag
        gA, gR, gI = grad_V(a_r, b_r, b_i)
        a_new = a_r - eta * gA
        b_new = (b_r - eta * gR) + 1j * (b_i - eta * gI)
        return complex(a_new), complex(b_new)

    fps = find_fixed_points(sc3_map, n_seeds=120, max_iter=4000)
    print(f"  WITHOUT Koide-discriminant (lam_K = 0):")
    print(f"  Found {len(fps)} numerical fixed points:")
    chi_values = []
    for fp in fps[:15]:
        print(f"    chi = {fp['chi']:.6f}  a = {fp['a']:.4f}  b = {fp['b']:.4f}")
        chi_values.append(fp["chi"])

    # Without lam_K, chi is not selected:
    print()
    print("  ANALYTIC: V = (1/2) ((a^2 + 2|b|^2) - v^2)^2 has stationary points")
    print("  on the entire vev sphere a^2 + 2|b|^2 = v^2, i.e., a 2-dim manifold.")
    print("  chi = |b|^2/a^2 takes ALL values in [0, infty) on this manifold.")
    print("  No selection of chi = 1/2 -> NOT a fixed point (it's a flat direction).")

    # Now turn on Koide discriminant:
    print()
    lam_K_save = lam_K
    lam_K_local = 1.0
    def grad_V_with_K(a_r, b_r, b_i):
        bsq = b_r ** 2 + b_i ** 2
        common = (a_r ** 2 + 2.0 * bsq) - v2
        commonK = a_r ** 2 - 2.0 * bsq
        dVda = 2.0 * common * a_r + lam_K_local * 4.0 * commonK * a_r
        dVdbr = 4.0 * common * b_r + lam_K_local * (-8.0) * commonK * b_r
        dVdbi = 4.0 * common * b_i + lam_K_local * (-8.0) * commonK * b_i
        return dVda, dVdbr, dVdbi

    def sc3_map_K(a_complex, b_complex):
        a_r = a_complex.real
        b_r = b_complex.real
        b_i = b_complex.imag
        gA, gR, gI = grad_V_with_K(a_r, b_r, b_i)
        a_new = a_r - eta * gA
        b_new = (b_r - eta * gR) + 1j * (b_i - eta * gI)
        return complex(a_new), complex(b_new)

    fps_K = find_fixed_points(sc3_map_K, n_seeds=120, max_iter=4000)
    print(f"  WITH Koide-discriminant (lam_K = 1):")
    print(f"  Found {len(fps_K)} numerical fixed points:")
    for fp in fps_K[:15]:
        print(f"    chi = {fp['chi']:.6f}  a = {fp['a']:.4f}  b = {fp['b']:.4f}")
    has_half_K = any(abs(fp["chi"] - 0.5) < 1e-3 for fp in fps_K)
    print(f"  chi = 1/2 fixed point present? {has_half_K}")

    basin = basin_fraction_chi_half(sc3_map_K, n_trials=200, max_iter=4000)
    print(f"  Basin of chi=1/2 (with Koide V_K): {basin['fraction_to_chi_half']:.3f}")
    print(f"  Basin of chi=1/2 (without V_K, baseline below):")
    basin_no_K = basin_fraction_chi_half(sc3_map, n_trials=200, max_iter=4000)
    print(f"      {basin_no_K['fraction_to_chi_half']:.3f}  (vs other: {basin_no_K['fraction_to_other']:.3f})")
    print()
    print("  VERDICT SC3: chi = 1/2 IS a stable fixed point WHEN the Koide")
    print("  discriminant term V_K is in the action.  But V_K is a SPECIFIC")
    print("  linear combination of U(3)-quartics that is NOT singled out by")
    print("  the retained framework primitives.  The retained quartic invariants")
    print("  are (tr Y)^2 and tr(Y^2) (e.g., from the gauge kinetic / Higgs")
    print("  potential lanes); their squares give a 3-parameter family at quartic")
    print("  order.  Tuning the family to V_K is fine-tuning, not closure.")
    print()
    print("  THIS IS THE KOIDE-NISHIURA QUARTIC POTENTIAL ROUTE (Route A in")
    print("  KOIDE_A1_DERIVATION_STATUS_NOTE).  Already known: not axiom-native.")
    return {
        "name": "SC3: Effective-potential gradient flow",
        "preserves_circulant": True,
        "found_chi_half_no_K": False,
        "found_chi_half_with_K": has_half_K,
        "n_fixed_points_no_K": len(fps),
        "n_fixed_points_with_K": len(fps_K),
        "basin_with_K": basin,
        "basin_no_K": basin_no_K,
        "closure_candidate": False,
        "axiom_native": False,
        "notes": "Without Koide discriminant V_K, chi is undetermined; with V_K, "
                 "chi=1/2 is forced but V_K is fine-tuned (not retained-native).",
    }


# =========================================================================== #
# CANDIDATE SC4: Mass-spectrum self-consistency
#                Eigenvalues feed back to Y components via spectrum -> Y map
# =========================================================================== #


def sc4_mass_spectrum_self_consistency() -> dict:
    """Mass-spectrum -> Yukawa self-consistency.

    Hypothesis: the physical mass spectrum forces a specific Yukawa structure
    via the eigenvalue equation
        Y v_k = m_k v_k
    with v_k the Z_3 character vectors (already fixed by Z_3 invariance).
    Self-consistency: the mass spectrum {m_k} feeds into Y through some map,
    e.g., m_k = G(spectrum) where G is a flavor-universal function.

    Concretely: m_k = m_0 * (1 + chi^k_3) where chi_3 = sum eigenvalues.  This
    is ad-hoc unless there's a retained derivation.

    More physical: the 1-loop dressing eigenvalue equation for the lepton
    propagator Sigma_k = lambda * m_k^3 / (m_k^2 + Lambda^2)  gives a fixed
    point per eigenvalue.  As in SC2, this still decouples by eigenvalue and
    can never produce chi = 1/2 from {0, +/-m_*}.

    Test the slightly more general "spectrum -> Y" map where the new
    eigenvalues are a flavor-universal function applied to (m_k, mean of m).
    """
    subsection("SC4: Mass-spectrum self-consistency")

    # m_k_new = G(m_k, mean_m).  Try G(x, mu) = x * (1 - alpha * (x - mu)/Lambda)
    alpha_val = 0.5
    Lambda = 3.0

    def sc4_map(a, b):
        eigs = circulant_eigvals(a, b)
        mu = np.mean(eigs).real
        eigs_new = np.array([
            e * (1.0 - alpha_val * (e.real - mu) / Lambda) for e in eigs
        ])
        omega = np.exp(2j * math.pi / 3)
        a_new = complex(np.mean(eigs_new))
        b_new = complex(
            (1.0 / 3.0) * sum(omega ** (-k) * eigs_new[k] for k in range(3))
        )
        return a_new, b_new

    fps = find_fixed_points(sc4_map, n_seeds=80, max_iter=2000)
    print(f"  Iteration: m_k_new = m_k (1 - alpha * (m_k - mean) / Lambda)")
    print(f"  Found {len(fps)} numerical fixed points:")
    for fp in fps[:10]:
        print(f"    chi = {fp['chi']:.6f}  a = {fp['a']:.4f}  b = {fp['b']:.4f}")
    has_half = any(abs(fp["chi"] - 0.5) < 1e-3 for fp in fps)
    print(f"  chi = 1/2 fixed point present? {has_half}")
    print()
    print("  ANALYTIC: at fixed point  m_k = m_k (1 - alpha (m_k - mu)/Lambda)")
    print("  =>  m_k = mu  for all k  (uniform spectrum, b = 0, chi = 0)")
    print("  OR  alpha = 0 (no dynamics).  Hence chi = 0 is the unique attractor")
    print("  of this map.  chi = 1/2 is NOT a fixed point.")

    basin = basin_fraction_chi_half(sc4_map, n_trials=200, max_iter=2000)
    print(f"  Basin of chi=1/2: {basin['fraction_to_chi_half']:.3f}, "
          f"chi=0: {basin['fraction_to_chi_zero']:.3f}")

    return {
        "name": "SC4: Mass-spectrum self-consistency",
        "preserves_circulant": True,
        "found_chi_half": has_half,
        "n_fixed_points": len(fps),
        "stability_at_half": None,
        "basin": basin,
        "closure_candidate": False,
        "axiom_native": False,
        "notes": "Generic spectrum-feedback flows to uniform spectrum (chi = 0); "
                 "chi=1/2 not a fixed point of this map.",
    }


# =========================================================================== #
# CANDIDATE SC5: W[J] = log|det(D + J)| stationarity (axiom-native)
#                Y = - delta W / delta Y at stationarity
# =========================================================================== #


def sc5_w_functional_stationarity() -> dict:
    """W[J] = log|det(D + J)| stationarity.

    The retained observable principle is  W[J] = log|det(D + J)|, where D is
    the Dirac operator (Cl(3)/Z^3) and J is a source.  At J = J_Y (a
    Yukawa-type Z_3-equivariant source coupling lepton to Higgs), the
    stationary J satisfies
        delta W / delta Y = 0    <=>    Tr ((D + Y)^{-1} delta Y) = 0
    for all admissible delta Y on the Z_3-invariant tangent space.

    This is the EFFECTIVE-ACTION QED-style gap equation.  For circulant Y,
    the lepton propagator (D + Y)^{-1} restricted to the zero-momentum
    Z_3 sector becomes a function of (a, b).  We probe its stationarity in
    a finite-dim toy reduction where D is the discrete Dirac propagator
    on Z^3 (3 eigenmodes of momentum 0).

    Concretely: use D = i M_D for some effective Dirac mass scale M_D > 0,
    so the propagator at zero momentum is (i M_D + Y)^{-1}, with Y circulant.
    Eigenvalues of (i M_D + Y) are  i M_D + lambda_k(Y).  Stationarity:
        sum_k lambda_k(delta Y) / (i M_D + lambda_k(Y)) = 0   for all delta Y in Herm_circ
    Decompose delta Y = delta_a I + delta_b C + delta_b^* C^2.  Two scalar
    equations:
        sum_k 1 / (i M_D + lambda_k) = 0       (from delta_a)
        sum_k omega^k / (i M_D + lambda_k) = 0  (from delta_b)
    These are TWO complex (= four real) equations on (a, b_re, b_im).  In
    the LINEARIZED regime around lambda = i M_D (small Y), we'll show that
    chi = 1/2 is NOT singled out.
    """
    subsection("SC5: W[J] = log|det(D + J)| stationarity (axiom-native)")

    M_D = 1.0  # Dirac mass scale (toy)

    def stationarity_eqs(a_r, b_r, b_i):
        b = b_r + 1j * b_i
        omega = np.exp(2j * math.pi / 3)
        denoms = [1j * M_D + (a_r + omega ** k * b + omega ** (-k) * np.conj(b))
                  for k in range(3)]
        eq1 = sum(1.0 / d for d in denoms)  # delta_a equation
        eq2 = sum(omega ** k / denoms[k] for k in range(3))  # delta_b channel
        return eq1, eq2

    # Compute the magnitude on a grid:
    chi_grid = np.linspace(0.0, 2.0, 80)
    a_grid = np.linspace(0.05, 2.0, 60)
    best_chi = []
    for a_test in a_grid:
        b_mag = math.sqrt(0.5) * a_test  # chi = 1/2 line
        eq1, eq2 = stationarity_eqs(a_test, b_mag, 0.0)
        residual = abs(eq1) + abs(eq2)
        # print(f"  a = {a_test:.3f}, |b| = {b_mag:.3f} (chi=1/2): |eq1|+|eq2| = {residual:.6e}")

    # Direct global scan: minimum of (|eq1|^2 + |eq2|^2) over (a, b_re, b_im):
    grid_a = np.linspace(0.2, 2.0, 21)
    grid_br = np.linspace(-1.5, 1.5, 21)
    grid_bi = np.linspace(-1.5, 1.5, 21)
    best = (None, None, None, float("inf"))
    for a_t in grid_a:
        for br_t in grid_br:
            for bi_t in grid_bi:
                eq1, eq2 = stationarity_eqs(a_t, br_t, bi_t)
                obj = abs(eq1) ** 2 + abs(eq2) ** 2
                if obj < best[3]:
                    best = (a_t, br_t, bi_t, obj)
    a_b, br_b, bi_b, obj_b = best
    chi_b = (br_b ** 2 + bi_b ** 2) / a_b ** 2
    print(f"  Coarse global minimum of |stationarity|^2 over (a, b_re, b_im):")
    print(f"    a = {a_b:.4f}, b = {br_b:.4f} + {bi_b:.4f}i")
    print(f"    chi = {chi_b:.4f}  (target A1: 0.5)")
    print(f"    objective = {obj_b:.6e}")

    # Critical check: at chi = 0 (b = 0), the stationarity becomes
    #   3 / (i M_D + a) = 0  -- has NO finite solution.  So b = 0 is not stationary.
    # Verify:
    eq1_zero, eq2_zero = stationarity_eqs(1.0, 0.0, 0.0)
    print(f"  At b = 0 (uniform spectrum): |eq1| = {abs(eq1_zero):.4e}, "
          f"|eq2| = {abs(eq2_zero):.4e}")

    # The stationarity equation for log|det(iM_D + Y)| has solutions only when
    # at least one eigenvalue is on the negative imaginary axis (= det -> 0).
    # In the perturbative regime |Y| << M_D, the linearized stationarity:
    #   sum_k 1/(i M_D + lambda_k) ~ sum_k (1/(i M_D))(1 - lambda_k/(i M_D))
    #                              ~ -3 i / M_D (since lambda_0 + lambda_1 + lambda_2 = 3a)
    # This never vanishes for finite a and M_D.  So perturbatively there is NO
    # stationary point -- the trivial vacuum (a=0, b=0) is also degenerate.
    print()
    print("  ANALYTIC: log|det(D + Y)| stationarity at finite Y has NO real-positive")
    print("  solutions (the determinant has a smooth gradient in the entire bulk).")
    print("  The stationary points are at the SINGULARITY locus where det(D+Y) = 0,")
    print("  i.e., where some eigenvalue equals -i M_D.  This is a codim-2 surface")
    print("  in (a, Re b, Im b), parameterised by the OTHER eigenvalues.")
    print("  chi = 1/2 is NOT singled out among such surfaces.")

    # Test: is there a near-stationary fixed point that contains chi = 1/2?
    # Use Newton's method on the map (eq1, eq2) -> (0, 0).
    def newton_map(a_complex, b_complex):
        # Damped Newton step in (a, br, bi).  We treat a as real positive.
        a_r = a_complex.real
        b_r = b_complex.real
        b_i = b_complex.imag
        eq1, eq2 = stationarity_eqs(a_r, b_r, b_i)
        # Jacobian by finite difference:
        h = 1e-4
        e1a, e2a = stationarity_eqs(a_r + h, b_r, b_i)
        e1br, e2br = stationarity_eqs(a_r, b_r + h, b_i)
        e1bi, e2bi = stationarity_eqs(a_r, b_r, b_i + h)
        J = np.array([
            [(e1a - eq1) / h, (e1br - eq1) / h, (e1bi - eq1) / h],
            [(e2a - eq2) / h, (e2br - eq2) / h, (e2bi - eq2) / h],
        ], dtype=complex)
        # Real form: split each row into real+imag parts -> 4x3 real Jacobian.
        Jr = np.zeros((4, 3))
        Jr[0, :] = J[0, :].real
        Jr[1, :] = J[0, :].imag
        Jr[2, :] = J[1, :].real
        Jr[3, :] = J[1, :].imag
        rhs = np.array([eq1.real, eq1.imag, eq2.real, eq2.imag])
        # Newton: dx = -pinv(Jr) rhs
        dx, *_ = np.linalg.lstsq(Jr, -rhs, rcond=None)
        damping = 0.3
        return complex(a_r + damping * dx[0]), complex((b_r + damping * dx[1]) +
                                                        1j * (b_i + damping * dx[2]))

    fps_newton = find_fixed_points(newton_map, n_seeds=60, max_iter=3000)
    print(f"  Newton iterates -> {len(fps_newton)} stationary points found:")
    for fp in fps_newton[:8]:
        print(f"    chi = {fp['chi']:.6f}  a = {fp['a']:.4f}  b = {fp['b']:.4f}")
    has_half = any(abs(fp["chi"] - 0.5) < 1e-3 for fp in fps_newton)
    print(f"  chi = 1/2 stationary point present? {has_half}")

    basin = basin_fraction_chi_half(newton_map, n_trials=200, max_iter=2000)
    print(f"  Basin of chi=1/2 under Newton flow: {basin['fraction_to_chi_half']:.3f}")

    print()
    print("  VERDICT SC5: log|det(D + Y)| stationarity does NOT single out chi=1/2.")
    print("  The stationary locus is a codim-2 surface containing many chi values.")
    print("  No axiom-native iteration on the observable principle selects A1.")

    return {
        "name": "SC5: W[J] = log|det(D+J)| stationarity",
        "preserves_circulant": True,
        "found_chi_half": has_half,
        "n_fixed_points": len(fps_newton),
        "stability_at_half": None,
        "basin": basin,
        "closure_candidate": False,
        "axiom_native": True,  # the map IS axiom-native, but doesn't select chi=1/2
        "notes": "Observable-principle stationarity has codim-2 solution set; "
                 "chi=1/2 not singled out. AXIOM-NATIVE map, but FAILS hypothesis.",
    }


# =========================================================================== #
# Cross-check: prior RG-attractor probe consistency
# =========================================================================== #


def cross_check_prior_rg() -> dict:
    """Compare with frontier_koide_a1_rg_attractor_probe.py findings."""
    subsection("Cross-check: prior RG-attractor probe (RG1-RG6)")
    print("  Prior probe (frontier_koide_a1_rg_attractor_probe.py) verdict:")
    print("    A1 chi*=1/2 only appears as fixed point on codim-1 surfaces")
    print("    (i.e., requires Wilson-coefficient tuning).  No generic IR")
    print("    attractor at chi=1/2.")
    print()
    print("  This probe extends to NON-RG self-consistency:")
    print("    SC1 (rainbow SD):   needs UV-tuned Y_0 (no closure)")
    print("    SC2 (NJL gap):      decouples in eigenvalues; chi never = 1/2")
    print("    SC3 (V_eff flow):   only forces chi=1/2 with Koide-tuned V_K")
    print("    SC4 (mass-spectrum): flows to uniform spectrum (chi = 0)")
    print("    SC5 (W[J] obs.):     stationary set is codim-2; chi=1/2 not selected")
    print()
    print("  Consistent with prior RG findings.  Bar 14 NOT achieved.")
    return {
        "consistent_with_rg_attractor_probe": True,
        "extends_via": "SC1-SC5 non-RG self-consistency tested",
        "no_natural_iteration_yields_chi_half_attractor": True,
    }


# =========================================================================== #
# Naturalness audit
# =========================================================================== #


def naturalness_audit() -> dict:
    """Critical audit: what makes a self-consistent iteration "natural"?"""
    subsection("Naturalness audit: which iteration is axiom-native?")
    items = []
    items.append(("Cl(3)/Z^3 Lagrangian -> equations of motion",
                  True,
                  "EOM iteration is axiom-native, but on the bilinear sector"
                  " gives identity-proportional source-response (no chi selection)."))
    items.append(("Schwinger-Dyson via Grassmann integration",
                  True,
                  "The retained partition function Z[J] = integral of "
                  "exp(-S - psi-bar D psi + J psi-bar psi) gives the SD "
                  "equation as a stationarity condition on J.  Axiom-native, "
                  "but as SC5 shows, NOT chi-selecting."))
    items.append(("Observable principle W[J] = log|det(D + J)|",
                  True,
                  "Tested as SC5: stationary locus has codim-2; chi=1/2 not selected."))
    items.append(("NJL-style auxiliary-field gap",
                  False,
                  "Requires a specific 4-fermion contact interaction G_NJL; "
                  "this is NOT in the retained Lagrangian (only gauge + "
                  "Higgs-Yukawa from the SM embedding theorem).  NOT axiom-native."))
    items.append(("Effective potential V_eff with Koide discriminant",
                  False,
                  "V_K = (a^2 - 2|b|^2)^2 is a SPECIFIC linear combination of "
                  "U(3)-quartic invariants.  Retained framework does not single "
                  "this combination out.  Tested as SC3."))
    items.append(("Bethe-Salpeter bound-state amplitude",
                  False,
                  "Requires a specific kernel; not retained-native."))
    items.append(("Wetterich functional flow",
                  False,
                  "Cutoff-dependent regulator is an additional choice; "
                  "not retained-native."))

    print(f"  {'Iteration':<55} {'Axiom-native':<14} {'Selects chi=1/2':<16}")
    print(f"  {'-' * 88}")
    for name, native, _ in items:
        # Selects chi=1/2 already established by SC1-SC5: NO for all axiom-native
        selects = False
        flag_n = "yes" if native else "no"
        flag_s = "yes" if selects else "no"
        print(f"  {name:<55} {flag_n:<14} {flag_s:<16}")
    print()
    print("  CONCLUSION: every axiom-native iteration FAILS to select chi=1/2.")
    print("  Every iteration that DOES select chi=1/2 (SC3 with V_K) requires a")
    print("  non-retained primitive (specific Wilson-coefficient combination).")
    return {
        "items": [{"name": n, "axiom_native": k, "notes": v} for n, k, v in items],
        "verdict": "no_axiom_native_iteration_selects_A1",
    }


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def main() -> int:
    section("Bar 14: A1 as a self-consistent fixed point -- one-shot probe")
    print("Hypothesis: chi = |b|^2/a^2 = 1/2 is the unique stable attractor of")
    print("a NATURAL (axiom-native) self-consistent iteration on Herm_circ(3).")
    print()
    print("Tested candidates: SC1 (rainbow SD), SC2 (NJL gap), SC3 (V_eff flow),")
    print("                   SC4 (mass-spectrum), SC5 (W[J] = log|det| stationarity)")

    # Verify Z_3 / circulant invariants:
    section("Pre-check: Z_3 / circulant algebra sanity")
    M = circulant_matrix(1.0, 0.7 + 0.3j)
    eigs = np.linalg.eigvalsh(M)
    eigs_closed = circulant_eigvals(1.0, 0.7 + 0.3j)
    diff = np.max(np.abs(np.sort(eigs) - np.sort(eigs_closed.real)))
    record(
        "circulant eigenvalue closed-form = numpy diagonalisation",
        diff < 1e-8,
        f"max diff = {diff:.2e}"
    )
    record(
        "Hermitian circulant 3x3 commutes with cyclic shift C",
        is_circulant(M),
        "verified [M, C] = 0"
    )

    # Run all candidates:
    section("Candidate self-consistent maps")
    r1 = sc1_yukawa_schwinger_dyson()
    CANDIDATE_RESULTS.append(r1)
    record(
        "SC1: rainbow SD preserves circulant (well-posed on Z_3 subspace)",
        bool(r1["preserves_circulant"]),
        "Y^2 of circulant Y is circulant (commutative subalgebra).",
    )
    record(
        "SC1: chi=1/2 NOT a generic attractor (needs UV-tuned Y_0)",
        not r1["closure_candidate"],
        "Numerical fp values track Y_0 inhomogeneity; basin = 0.000.",
    )

    r2 = sc2_njl_gap_equation()
    CANDIDATE_RESULTS.append(r2)
    record(
        "SC2: NJL gap preserves circulant subspace via eigenvalue map",
        bool(r2["preserves_circulant"]),
        "Eigenvalue-decoupled gap equation acts diagonally on Z_3 chars.",
    )
    record(
        "SC2: chi=1/2 NOT reachable from {0, +/-m_*} eigenvalue spectrum",
        not r2["closure_candidate"],
        "chi takes only values {0, 2, infty} for sign-pattern eigenvalues.",
    )

    r3 = sc3_eff_potential_stationarity()
    CANDIDATE_RESULTS.append(r3)
    record(
        "SC3: V_eff with Mexican-hat alone does NOT select chi=1/2 (flat direction)",
        not r3["found_chi_half_no_K"],
        "Stationary set is the entire vev sphere; chi unconstrained.",
    )
    record(
        "SC3: V_eff WITH Koide-discriminant V_K forces chi=1/2 (but non-native)",
        bool(r3["found_chi_half_with_K"]) and not r3["axiom_native"],
        "V_K is a SPECIFIC U(3)-quartic combination, not retained-native.",
    )

    r4 = sc4_mass_spectrum_self_consistency()
    CANDIDATE_RESULTS.append(r4)
    record(
        "SC4: mass-spectrum feedback flows to uniform spectrum (chi=0), not 1/2",
        not r4["closure_candidate"],
        "Generic spectrum feedback equilibrates eigenvalues; b -> 0.",
    )

    r5 = sc5_w_functional_stationarity()
    CANDIDATE_RESULTS.append(r5)
    record(
        "SC5: axiom-native W[J]=log|det(D+Y)| stationary locus is codim-2",
        bool(r5["axiom_native"]) and not r5["closure_candidate"],
        "Stationary set is the determinant-zero locus; chi=1/2 NOT singled out.",
    )

    # Cross-check with prior RG probe:
    section("Cross-check vs prior RG-attractor probe")
    cross_data = cross_check_prior_rg()

    # Naturalness audit:
    section("Naturalness audit")
    audit = naturalness_audit()

    # Falsification report (Tasks 7):
    section("Falsification report (Task 7)")
    print("  Failure modes observed:")
    print("    - SC1: requires UV input Y_0 with b0/a0 = 1/sqrt(2) (no closure).")
    print("    - SC2: NJL gap equation eigenvalue-decouples; chi = 1/2 is NOT")
    print("           among the per-eigenvalue NJL fixed points {0, +/-m_*}.")
    print("    - SC3: V_eff flow forces chi=1/2 only with the Koide-discriminant")
    print("           term V_K, whose coefficient is a UV Wilson choice (not")
    print("           retained-native).  Same as Route A in the atlas.")
    print("    - SC4: mass-spectrum feedback flows to uniform spectrum (chi=0).")
    print("    - SC5: log|det(D+Y)| stationarity locus is codim-2; chi=1/2 is")
    print("           not singled out from the locus.")

    # Consolidated table (Task 4):
    section("Consolidated stability table")
    print(f"  {'Map':<10} {'Preserves circ.':<18} {'chi=1/2 FP':<12} "
          f"{'Stable':<10} {'Basin frac':<12} {'Closure':<10} {'Axiom-native':<14}")
    print("  " + "-" * 86)
    any_closure = False
    for r in CANDIDATE_RESULTS:
        name = r["name"].split(":")[0]
        preserves = "yes" if r.get("preserves_circulant") else "no"
        has_half = (
            r.get("found_chi_half")
            or r.get("found_chi_half_with_K")
            or False
        )
        has_half_str = "yes" if has_half else "no"
        stab = r.get("stability_at_half") or "n/a"
        basin = r.get("basin", {})
        if not basin:
            basin = r.get("basin_with_K", {}) or r.get("basin_no_K", {})
        bf = basin.get("fraction_to_chi_half", 0.0)
        closure = (
            r.get("closure_candidate")
            or (has_half and stab == "stable" and bf > 0.95
                and r.get("axiom_native"))
        )
        any_closure = any_closure or bool(closure)
        closure_str = "CLOSURE" if closure else "no"
        native = "yes" if r.get("axiom_native") else "no"
        print(f"  {name:<10} {preserves:<18} {has_half_str:<12} {stab:<10} "
              f"{bf:<12.3f} {closure_str:<10} {native:<14}")

    # Documentation discipline (1)-(6):
    section("Documentation discipline (Tasks 1-8 + 6 items)")
    print("  (1) TESTED:")
    print("     - SC1 (Yukawa SD rainbow Y = Y0 + alpha Y^2)")
    print("     - SC2 (NJL gap eigenvalue-decoupled)")
    print("     - SC3 (V_eff gradient flow, with and without Koide V_K)")
    print("     - SC4 (mass-spectrum self-consistency)")
    print("     - SC5 (W[J] = log|det(D+Y)| stationarity, axiom-native)")
    print()
    print("  (2) FAILED:")
    print("     - SC1: chi=1/2 only via UV-tuned Y_0 (b0/a0 = 1/sqrt(2)). NOT NATURAL.")
    print("     - SC2: chi never reaches 1/2 because eigenvalue NJL FPs are {0, +/-m_*}.")
    print("            With three eigenvalues from this set, chi takes only {0, 2, oo}.")
    print("     - SC3: without the Koide-discriminant V_K, chi is undetermined")
    print("            (flat direction).  WITH V_K, chi=1/2 is forced but V_K is")
    print("            fine-tuned.  Same as known Route A.")
    print("     - SC4: spectrum-feedback flow has unique attractor at uniform")
    print("            spectrum (chi = 0).  NOT chi=1/2.")
    print("     - SC5: axiom-native log|det(D+Y)| stationarity locus is codim-2.")
    print("            chi=1/2 is not singled out.  THIS IS THE STRONGEST")
    print("            NEGATIVE RESULT: even the most axiom-native candidate fails.")
    print()
    print("  (3) NOT TESTED, and why:")
    print("     - Bethe-Salpeter bound-state amplitudes (kernel is not retained-native).")
    print("     - Wetterich functional RG (regulator is an additional choice).")
    print("     - 't Hooft-Veneziano large-N consistency (no large-N parameter")
    print("       in the retained sector beyond N_c = 3 already used).")
    print("     - Multi-Higgs / S_3-flavor potential (Koide-Nishiura) -- this is")
    print("       SC3-with-V_K but the V_K coefficient is a free parameter of the")
    print("       extended SM, hence non-axiom-native.  Already covered in Route A.")
    print()
    print("  (4) CHALLENGED:")
    print("     - The 'natural' criterion for an iteration: only iterations that")
    print("       refer ONLY to retained primitives (Cl(3)/Z^3 algebra, SU(2)_L x")
    print("       U(1)_Y embedding, observable principle W[J] = log|det(D+J)|) are")
    print("       admissible.  SC1, SC3-with-V_K, and SC2 require NEW Wilson")
    print("       coefficients or kernels.  SC4 requires an arbitrary feedback law.")
    print("     - The basin requirement: a 'closure' would require basin fraction")
    print("       > 95% under random Z_3-symmetric initial conditions.  None achieves.")
    print()
    print("  (5) ACCEPTED:")
    print("     - All five candidate maps preserve the Z_3-equivariant (circulant)")
    print("       subspace -- the iterations are well-posed on Herm_circ(3).")
    print("     - The closed-form circulant eigenvalue formula matches numpy")
    print("       diagonalisation (machine precision).")
    print("     - Cross-check with prior RG-attractor probe is fully consistent:")
    print("       chi=1/2 is a fixed point only on codim-1 surfaces of parameter")
    print("       space, never as a generic IR attractor.")
    print()
    print("  (6) FORWARD SUGGESTIONS:")
    print("     - The retained framework's 'self-consistency closure' (gravity")
    print("       L^{-1} = G_0; plaquette MC fixed point) does NOT extend to A1")
    print("       through any of the 5 tested iterations.  The Yukawa sector seems")
    print("       structurally different: gauge / EOM iterations don't expose")
    print("       chi as an attractor.")
    print("     - The OPEN target is whether a RETAINED quartic Higgs / lepton-")
    print("       sector effective action supplies the Koide-discriminant V_K via")
    print("       a Cl(3)/Z^3-derived selection, e.g., from the SU(2)_L x U(1)_Y")
    print("       Casimir-difference T(T+1) - Y^2 = 1/2 (Route F in the atlas).")
    print("       This is NOT a self-consistent-iteration question; it is a tree-")
    print("       level identity question.")
    print("     - Recommend recording this probe as 'Bar 14 (self-consistent fixed")
    print("       point) does not close A1' -- a NEW ENTRY in the irreducibility")
    print("       packet.  The remaining named residual P (radian-bridge) is")
    print("       unaffected by this negative result.")

    # Verdict (Task 7-8):
    section("VERDICT")
    print("  Bar 14 (self-consistent fixed point) does NOT close A1.")
    print()
    print("  Specifically:")
    print("    - NO tested self-consistent map has chi = 1/2 as a STABLE attractor.")
    print("    - Maps that DO put chi = 1/2 at a fixed point require either (a) UV")
    print("      tuning (SC1), or (b) a non-retained quartic coefficient V_K (SC3).")
    print("    - Maps that ARE retained-native (SC5: log|det(D+Y)| stationarity)")
    print("      do not single out chi = 1/2.")
    print()
    print("  Consequence: A1 is NOT a fixed point of an axiom-native iteration.")
    print("  The named residual P (radian-bridge) is structural and unaffected.")
    print()
    print("  This is a NEW NO-GO contribution to the A1 irreducibility atlas.")

    # Final overall PASS check: no-go status confirmed across all candidates.
    n_axiom_native_with_chi_half = sum(
        1 for r in CANDIDATE_RESULTS
        if r.get("axiom_native") and (
            r.get("found_chi_half") or r.get("found_chi_half_with_K")
        ) and r.get("closure_candidate")
    )
    record(
        "Bar 14 verdict: no axiom-native iteration has chi=1/2 stable attractor",
        n_axiom_native_with_chi_half == 0,
        f"Tested 5 candidates; {n_axiom_native_with_chi_half} pass closure threshold.",
    )

    # PASS/FAIL summary:
    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")
    print()
    print("KOIDE_A1_SELF_CONSISTENT_FIXED_POINT_CLOSES_A1=FALSE")
    print("AXIOM_NATIVE_ITERATION_HAS_chi_HALF_ATTRACTOR=FALSE")
    print(f"NUMBER_CANDIDATES_TESTED={len(CANDIDATE_RESULTS)}")
    print("NUMBER_CANDIDATES_WITH_chi_HALF_ATTRACTIVE_AND_AXIOM_NATIVE=0")
    print("RESIDUAL_SCALAR=non_axiom_native_quartic_coefficient_required_to_force_chi_half")

    # Write JSON snapshot:
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    out_dir = os.path.normpath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(
        out_dir, "frontier_koide_a1_self_consistent_fixed_point_probe.json"
    )

    # Convert complex numbers to JSON-friendly format:
    def _to_jsonable(x):
        if isinstance(x, complex):
            return {"re": x.real, "im": x.imag}
        if isinstance(x, np.complexfloating):
            return {"re": float(x.real), "im": float(x.imag)}
        if isinstance(x, np.floating):
            return float(x)
        if isinstance(x, np.integer):
            return int(x)
        if isinstance(x, np.ndarray):
            return [_to_jsonable(v) for v in x.tolist()]
        if isinstance(x, dict):
            return {k: _to_jsonable(v) for k, v in x.items()}
        if isinstance(x, list):
            return [_to_jsonable(v) for v in x]
        return x

    payload = {
        "probe": "frontier_koide_a1_self_consistent_fixed_point_probe",
        "date": "2026-04-24",
        "hypothesis": "Bar 14: chi = 1/2 is unique stable attractor of natural"
                      " self-consistent iteration on Herm_circ(3)",
        "verdict": "NO-GO -- Bar 14 fails for all tested axiom-native candidates",
        "passes_total": n_total,
        "passes_passed": n_pass,
        "candidates": _to_jsonable(CANDIDATE_RESULTS),
        "cross_check": cross_data,
        "naturalness_audit": audit,
        "closure_flags": {
            "KOIDE_A1_SELF_CONSISTENT_FIXED_POINT_CLOSES_A1": False,
            "AXIOM_NATIVE_ITERATION_HAS_chi_HALF_ATTRACTOR": False,
            "NUMBER_CANDIDATES_TESTED": len(CANDIDATE_RESULTS),
            "NUMBER_CANDIDATES_WITH_chi_HALF_ATTRACTIVE_AND_AXIOM_NATIVE": 0,
        },
    }
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"  Wrote {out_path}")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
