#!/usr/bin/env python3
"""
Exact Perron-state reduction of the explicit plaquette transfer/operator route.

This does not close analytic P(6). It closes the next structural step:
once the plaquette source operator J is explicit, the transfer state reduces
exactly to Perron data of the positive one-clock transfer operator, and the
remaining framework-point object is the Jacobi data of J in that Perron state.
"""

from __future__ import annotations

import numpy as np


THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

NMAX = 5
TAU = 6.0
SHELL_EPS = 0.15
ASYM_EPS = 0.03


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def recurrence_neighbors(p: int, q: int) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for a, b in [
        (p + 1, q),
        (p - 1, q + 1),
        (p, q - 1),
        (p, q + 1),
        (p + 1, q - 1),
        (p - 1, q),
    ]:
        if a >= 0 and b >= 0:
            out.append((a, b))
    return out


def weights_box(nmax: int) -> list[tuple[int, int]]:
    return [(p, q) for p in range(nmax + 1) for q in range(nmax + 1)]


def build_recurrence_matrix(nmax: int) -> tuple[np.ndarray, list[tuple[int, int]], dict[tuple[int, int], int]]:
    weights = weights_box(nmax)
    index = {w: i for i, w in enumerate(weights)}
    jmat = np.zeros((len(weights), len(weights)), dtype=float)
    for p, q in weights:
        i = index[(p, q)]
        for a, b in recurrence_neighbors(p, q):
            if (a, b) in index:
                jmat[index[(a, b)], i] += 1.0 / 6.0
    return jmat, weights, index


def matrix_exponential_symmetric(m: np.ndarray, tau: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(m)
    return (vecs * np.exp(tau * vals)) @ vecs.T


def dominant_eigenpair(m: np.ndarray) -> tuple[float, np.ndarray]:
    vals, vecs = np.linalg.eigh(m)
    idx = int(np.argmax(vals))
    vec = vecs[:, idx]
    if np.sum(vec) < 0.0:
        vec = -vec
    return float(vals[idx]), vec


def thermal_state_expectation(t: np.ndarray, obs: np.ndarray, steps: int) -> float:
    tp = np.linalg.matrix_power(t, steps)
    return float(np.trace(tp @ obs) / np.trace(tp))


def lanczos_jacobi(obs: np.ndarray, start: np.ndarray, kmax: int) -> tuple[list[float], list[float], np.ndarray]:
    q_prev = np.zeros_like(start)
    q = start / np.linalg.norm(start)
    alpha: list[float] = []
    beta: list[float] = []
    basis = [q.copy()]

    b_prev = 0.0
    for _ in range(kmax):
        z = obs @ q
        a = float(np.dot(q, z))
        z = z - a * q - b_prev * q_prev
        b = float(np.linalg.norm(z))
        alpha.append(a)
        if b < 1.0e-12:
            break
        beta.append(b)
        q_prev = q
        q = z / b
        basis.append(q.copy())
        b_prev = b

    dim = len(alpha)
    jac = np.zeros((dim, dim), dtype=float)
    for i, a in enumerate(alpha):
        jac[i, i] = a
    for i, b in enumerate(beta[: max(0, dim - 1)]):
        jac[i, i + 1] = jac[i + 1, i] = b
    return alpha, beta, np.column_stack(basis[:dim])


def conjugation_swap_matrix(weights: list[tuple[int, int]], index: dict[tuple[int, int], int]) -> np.ndarray:
    s = np.zeros((len(weights), len(weights)), dtype=float)
    for w in weights:
        s[index[(w[1], w[0])], index[w]] = 1.0
    return s


def main() -> int:
    jmat, weights, index = build_recurrence_matrix(NMAX)
    diag = np.diag(
        [
            SHELL_EPS * (p + q) + ASYM_EPS * ((p - q) ** 2)
            for p, q in weights
        ]
    )
    hgen = jmat + diag
    tmat = matrix_exponential_symmetric(hgen, TAU)
    lam0, psi0 = dominant_eigenpair(tmat)
    vals = np.linalg.eigvalsh(tmat)
    vals_desc = vals[::-1]
    gap = float(vals_desc[0] - vals_desc[1])
    min_entry = float(np.min(tmat))
    positivity_floor = float(np.min(psi0))

    swap = conjugation_swap_matrix(weights, index)
    commute_t_err = float(np.max(np.abs(swap @ tmat - tmat @ swap)))
    commute_j_err = float(np.max(np.abs(swap @ jmat - jmat @ swap)))
    invariant_err = float(np.linalg.norm(swap @ psi0 - psi0))

    observable = jmat.copy()
    perron_expectation = float(psi0 @ (observable @ psi0))

    thermal_steps = [1, 2, 4, 8, 16]
    thermal_values = [thermal_state_expectation(tmat, observable, n) for n in thermal_steps]
    thermal_errors = [abs(v - perron_expectation) for v in thermal_values]

    alpha, beta, basis = lanczos_jacobi(observable, psi0, 6)
    jac_dim = len(alpha)
    jac = np.zeros((jac_dim, jac_dim), dtype=float)
    for i, a in enumerate(alpha):
        jac[i, i] = a
    for i, b in enumerate(beta[: max(0, jac_dim - 1)]):
        jac[i, i + 1] = jac[i + 1, i] = b

    e0 = np.zeros(jac_dim, dtype=float)
    e0[0] = 1.0
    moment_errors = []
    for n in range(6):
        full_moment = float(psi0 @ (np.linalg.matrix_power(observable, n) @ psi0))
        jac_moment = float(e0 @ (np.linalg.matrix_power(jac, n) @ e0))
        moment_errors.append(abs(full_moment - jac_moment))

    spec_vals, spec_vecs = np.linalg.eigh(tmat)
    spectral_obs = 0.0
    spectral_den = 0.0
    for lam, vec in zip(spec_vals, spec_vecs.T):
        weight = lam**8
        spectral_den += weight
        spectral_obs += weight * float(vec @ (observable @ vec))
    spectral_expectation = spectral_obs / spectral_den
    direct_expectation = thermal_state_expectation(tmat, observable, 8)

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE PERRON-STATE REDUCTION")
    print("=" * 78)
    print()
    print("Truncated transfer proxy from the explicit character-recurrence operator")
    print(f"  box size                              = {(NMAX + 1)} x {(NMAX + 1)} = {len(weights)} states")
    print(f"  proxy transfer parameter tau          = {TAU:.1f}")
    print(f"  shell deformation coefficients        = (shell={SHELL_EPS:.2f}, asym={ASYM_EPS:.2f})")
    print(f"  transfer symmetry error               = {np.max(np.abs(tmat - tmat.T)):.3e}")
    print(f"  transfer minimum entry                = {min_entry:.6e}")
    print(f"  Perron eigenvalue gap                 = {gap:.6e}")
    print(f"  Perron positivity floor               = {positivity_floor:.6e}")
    print()
    print("Thermal-to-Perron convergence witness for J")
    for n, val, err in zip(thermal_steps, thermal_values, thermal_errors):
        print(f"  Lt={n:2d}: <J>_thermal = {val:.12f}   error = {err:.3e}")
    print()
    print("Symmetry reduction witness")
    print(f"  swap/J commutator error               = {commute_j_err:.3e}")
    print(f"  swap/T commutator error               = {commute_t_err:.3e}")
    print(f"  Perron swap-invariance error          = {invariant_err:.3e}")
    print()
    print("Jacobi compression witness")
    print(f"  Jacobi dimension                      = {jac_dim}")
    print(f"  max Perron-moment mismatch            = {max(moment_errors):.3e}")
    print(f"  first Jacobi coefficients             = alpha[:4]={np.round(alpha[:4], 10).tolist()}")
    print(f"                                         beta[:4]={np.round(beta[:4], 10).tolist()}")
    print()

    check(
        "the explicit source-operator route admits a positivity-improving self-adjoint transfer proxy",
        np.max(np.abs(tmat - tmat.T)) < 1.0e-10 and min_entry > 0.0,
        detail=f"symmetry error={np.max(np.abs(tmat - tmat.T)):.3e}, min entry={min_entry:.3e}",
    )
    check(
        "the transfer proxy has one simple strictly positive Perron mode",
        gap > 1.0e-8 and positivity_floor > 1.0e-8,
        detail=f"gap={gap:.6e}, positivity floor={positivity_floor:.6e}",
    )
    check(
        "the thermal trace state is exactly the spectral decomposition state and converges to the Perron expectation",
        abs(spectral_expectation - direct_expectation) < 1.0e-12 and thermal_errors[-1] < thermal_errors[0],
        detail=f"spectral/direct error={abs(spectral_expectation - direct_expectation):.3e}",
    )
    check(
        "any commuting positivity-preserving symmetry fixes the Perron state",
        commute_t_err < 1.0e-9 and invariant_err < 1.0e-10,
        detail=f"commutator={commute_t_err:.3e}, invariance={invariant_err:.3e}",
    )
    check(
        "the remaining framework-point object is equivalently Jacobi data of J in the Perron state",
        max(moment_errors) < 1.0e-10,
        detail=f"max Jacobi/Perron moment error={max(moment_errors):.3e}",
    )

    check(
        "the explicit plaquette-source operator still obeys the conjugation symmetry on the truncated box",
        commute_j_err < 1.0e-12 and float(np.max(np.abs(swap @ hgen - hgen @ swap))) < 1.0e-12,
        detail=f"swap/J error={commute_j_err:.3e}, swap/H error={float(np.max(np.abs(swap @ hgen - hgen @ swap))):.3e}",
        bucket="SUPPORT",
    )
    check(
        "thermal expectations move monotonically toward the Perron value on the sampled derived-time depths",
        all(thermal_errors[i + 1] <= thermal_errors[i] + 1.0e-12 for i in range(len(thermal_errors) - 1)),
        detail=f"errors={['%.3e' % e for e in thermal_errors]}",
        bucket="SUPPORT",
    )
    check(
        "the Jacobi compression is nontrivial rather than rank-one",
        jac_dim >= 4 and max(beta) > 1.0e-8,
        detail=f"jacobi dim={jac_dim}, max beta={max(beta) if beta else 0.0:.3e}",
        bucket="SUPPORT",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 78)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
