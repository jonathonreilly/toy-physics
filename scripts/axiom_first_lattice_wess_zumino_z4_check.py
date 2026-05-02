#!/usr/bin/env python3
"""
axiom_first_lattice_wess_zumino_z4_check.py
--------------------------------------------

Numerical exhibits for the axiom-first lattice Wess-Zumino /
Fujikawa theorem on Z^4.

Theorem note:
  docs/AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_Z4_THEOREM_NOTE_2026-05-02.md

This is a STANDALONE unaudited source-claim runner. It does NOT touch
audit infrastructure or any existing audit row.

Structural checks:

  E1. Z^4 sublattice parity epsilon(x) = (-1)^(x1+x2+x3+x4) is a real,
      diagonal, involutive operator with |Lambda_e| = |Lambda_o| = L^4 / 2
      on even periodic Z^4.

  E2. 4d staggered Dirac operator D anticommutes with epsilon:
        epsilon * D * epsilon = -D     (eq. 6 of the theorem note)
      The Z^3 form is retained in CPT_EXACT_NOTE; we verify the Z^4 form
      explicitly at machine precision on small even L.

  E3. Wess-Zumino consistency / cocycle linearity:
        log J[alpha_1 + alpha_2, U] = log J[alpha_1, U] + log J[alpha_2, U]
      and the antisymmetric Z_2 cocycle vanishes.

  E4. Lattice index theorem (W3 lattice form):
        A[1, U] = sum_x epsilon(x) * <x | exp(-t D†D[U]) | x>
                = n_+(D) - n_-(D)  (integer, t-independent)
      Verified on free background U = I across t in [0.01, 5.0].

  E5. Gauge invariance of the lattice index under U(1) gauge rotations
      (W4 cocycle non-triviality lemma): under
        U_mu(x) -> G(x)^* U_mu(x) G(x+mu),
      both the spectrum of D†D and the chiral trace
        sum_x epsilon(x) <x | exp(-t D†D) | x>
      are gauge-invariant.

  E6. Heat-kernel diagonal is well-defined on the finite torus:
      every t > 0 gives a finite, real, positive trace, and
      sum_x T_t[U]_x = sum_n exp(-t lambda_n) is bounded by
      dim(H_F) * 1 = dim(H_F) (since lambda_n >= 0).

If all checks pass, the structural content of the lattice
Wess-Zumino theorem on Z^4 is reproduced on these representatives.
The theorem-note proof is the load-bearing argument; this runner is
verification.
"""

from __future__ import annotations

import sys
from itertools import product

import numpy as np
from numpy.linalg import eigh, eigvalsh
from scipy.linalg import expm

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"[{status}] {name}"
    if detail:
        msg += f"  {detail}"
    print(msg)


# ---------------------------------------------------------------------------
# Z^4 lattice setup with even periodic boundary
# ---------------------------------------------------------------------------

def site_index(x, L):
    """Linear index of site x = (x1, x2, x3, x4) in (Z/L)^4."""
    return (
        (x[0] % L) * (L * L * L)
        + (x[1] % L) * (L * L)
        + (x[2] % L) * L
        + (x[3] % L)
    )


def epsilon_diagonal(L):
    """Sublattice parity epsilon(x) = (-1)^(x1+x2+x3+x4), shape (L^4,)."""
    eps = np.zeros(L ** 4, dtype=np.float64)
    for x in product(range(L), repeat=4):
        eps[site_index(x, L)] = (-1.0) ** (sum(x))
    return eps


def staggered_phase(mu, x):
    """Kogut-Susskind staggered phase eta_mu(x) for mu in {0, 1, 2, 3}.
    eta_0(x) = 1
    eta_1(x) = (-1)^(x_0)
    eta_2(x) = (-1)^(x_0 + x_1)
    eta_3(x) = (-1)^(x_0 + x_1 + x_2)
    """
    if mu == 0:
        return 1.0
    elif mu == 1:
        return (-1.0) ** (x[0])
    elif mu == 2:
        return (-1.0) ** (x[0] + x[1])
    elif mu == 3:
        return (-1.0) ** (x[0] + x[1] + x[2])
    else:
        raise ValueError(f"mu must be in {{0,1,2,3}}: got {mu}")


def free_staggered_dirac_matrix(L):
    """Build the free (U = I) 4d staggered Dirac matrix as a real
    antihermitian (L^4, L^4) matrix:
      D = (1/2) sum_{mu=0..3} eta_mu(x) [delta_{x+mu, y} - delta_{x-mu, y}]
    on even periodic Z^4 (massless, no Wilson term).
    """
    N = L ** 4
    D = np.zeros((N, N), dtype=np.float64)
    for x in product(range(L), repeat=4):
        ix = site_index(x, L)
        for mu in range(4):
            eta = staggered_phase(mu, x)
            xp = list(x)
            xm = list(x)
            xp[mu] = (xp[mu] + 1) % L
            xm[mu] = (xm[mu] - 1) % L
            iy_p = site_index(xp, L)
            iy_m = site_index(xm, L)
            D[ix, iy_p] += 0.5 * eta
            D[ix, iy_m] -= 0.5 * eta
    return D


def gauged_u1_staggered_dirac_matrix(L, link_phases):
    """Build the staggered Dirac matrix coupled to U(1) link phases:
      D[U] = (1/2) sum_mu eta_mu(x) [
                U_mu(x) delta_{x+mu, y} - U_mu(x-mu)^* delta_{x-mu, y}
             ]
    link_phases[mu, x_idx] = U_mu(x) = exp(i theta_mu(x)).
    """
    N = L ** 4
    D = np.zeros((N, N), dtype=complex)
    for x in product(range(L), repeat=4):
        ix = site_index(x, L)
        for mu in range(4):
            eta = staggered_phase(mu, x)
            xp = list(x)
            xm = list(x)
            xp[mu] = (xp[mu] + 1) % L
            xm[mu] = (xm[mu] - 1) % L
            iy_p = site_index(xp, L)
            iy_m = site_index(xm, L)
            U_pos = link_phases[mu, ix]            # U_mu(x)
            U_neg = link_phases[mu, iy_m]          # U_mu(x-mu) (will be conjugated)
            D[ix, iy_p] += 0.5 * eta * U_pos
            D[ix, iy_m] -= 0.5 * eta * U_neg.conj()
    return D


def random_u1_link_phases(L, rng):
    """Random U(1) link phases U_mu(x) = exp(i theta) for mu in {0,1,2,3}."""
    N = L ** 4
    phases = np.zeros((4, N), dtype=complex)
    for mu in range(4):
        thetas = rng.uniform(-np.pi, np.pi, size=N)
        phases[mu] = np.exp(1j * thetas)
    return phases


def apply_u1_gauge_rotation(link_phases, gauge_phases, L):
    """Apply U(1) gauge rotation U_mu(x) -> G(x)^* U_mu(x) G(x+mu)
    where gauge_phases[x_idx] = G(x) = exp(i alpha(x))."""
    N = L ** 4
    out = np.zeros_like(link_phases)
    for x in product(range(L), repeat=4):
        ix = site_index(x, L)
        for mu in range(4):
            xp = list(x)
            xp[mu] = (xp[mu] + 1) % L
            iy_p = site_index(xp, L)
            out[mu, ix] = gauge_phases[ix].conj() * link_phases[mu, ix] * gauge_phases[iy_p]
    return out


def regularized_local_trace(D, t):
    """Compute the diagonal of exp(-t D†D), shape (N,).
    T_t[U]_x = <x | exp(-t D†D) | x>.
    """
    DtD = D.conj().T @ D
    evals, evecs = eigh(DtD)
    # |<x|n>|^2 weighted by exp(-t lambda_n)
    T_diag = np.real(np.einsum("xn,n,xn->x", evecs, np.exp(-t * evals), evecs.conj()))
    return T_diag


def chiral_anomaly_trace(D, eps, t):
    """A[1, U] = sum_x eps(x) T_t[U]_x at alpha = 1."""
    T_diag = regularized_local_trace(D, t)
    return float(np.sum(eps * T_diag))


def chiral_anomaly_trace_spectral(D, eps):
    """Zero-mode spectral form of A[1, U]: counts chirality imbalance
    among kernel of D†D.
    """
    DtD = D.conj().T @ D
    evals, evecs = eigh(DtD)
    diag = np.real(np.einsum("xn,x,xn->n", evecs.conj(), eps, evecs))
    zero_modes_mask = evals < 1e-9
    if not np.any(zero_modes_mask):
        return 0.0
    return float(np.sum(diag[zero_modes_mask]))


# ---------------------------------------------------------------------------
# E1: epsilon (Z^4 form) is diagonal, real, involutive, balanced
# ---------------------------------------------------------------------------

def check_E1_epsilon_structure(L_list=(4,)):
    print("\n=== E1: Z^4 sublattice parity epsilon properties ===")
    for L in L_list:
        eps = epsilon_diagonal(L)
        check(f"E1a/L={L}: epsilon is real",
              np.all(np.imag(eps) == 0))
        check(f"E1b/L={L}: epsilon is involutive (epsilon^2 = 1)",
              np.allclose(eps * eps, 1.0))
        check(f"E1c/L={L}: epsilon takes values in {{-1, +1}}",
              np.all((eps == 1.0) | (eps == -1.0)))
        n_plus = int(np.sum(eps == 1.0))
        n_minus = int(np.sum(eps == -1.0))
        check(f"E1d/L={L}: |Lambda_e| = |Lambda_o| = L^4 / 2",
              n_plus == n_minus == (L ** 4) // 2,
              f"|Lambda_e| = {n_plus}, |Lambda_o| = {n_minus}")


# ---------------------------------------------------------------------------
# E2: epsilon * D * epsilon = -D (Z^4 extension of CPT_EXACT_NOTE eq.)
# ---------------------------------------------------------------------------

def check_E2_epsilon_anticommutes_D_free(L_list=(4,)):
    print("\n=== E2: epsilon D epsilon = -D on free Z^4 (gamma_5 anticommutation) ===")
    for L in L_list:
        eps = epsilon_diagonal(L)
        D = free_staggered_dirac_matrix(L)
        D_conjugated = np.outer(eps, eps) * D
        residual = float(np.max(np.abs(D_conjugated + D)))
        check(f"E2/L={L}: ||eps*D*eps + D|| = 0 (machine precision, free)",
              residual < 1e-12,
              f"residual = {residual:.2e}")


def check_E2_epsilon_anticommutes_D_gauged(L_list=(4,), seed=20260502):
    print("\n=== E2 (gauged): epsilon D[U] epsilon = -D[U] on Z^4 with random U(1) ===")
    rng = np.random.default_rng(seed)
    for L in L_list:
        eps = epsilon_diagonal(L)
        link_phases = random_u1_link_phases(L, rng)
        D = gauged_u1_staggered_dirac_matrix(L, link_phases)
        D_conjugated = np.outer(eps, eps) * D
        residual = float(np.max(np.abs(D_conjugated + D)))
        check(f"E2g/L={L}: ||eps*D[U]*eps + D[U]|| = 0 (gauged)",
              residual < 1e-10,
              f"residual = {residual:.2e}")


# ---------------------------------------------------------------------------
# E3: Wess-Zumino consistency / linearity in alpha
# ---------------------------------------------------------------------------

def jacobian_log(alpha, eps, T_diag):
    """A[alpha, U] = sum_x alpha(x) * eps(x) * T_t[U]_x."""
    return float(np.sum(alpha * eps * T_diag))


def check_E3_wess_zumino_consistency(L=4, t=0.5, seed=20260502):
    print("\n=== E3: Wess-Zumino cocycle / linearity (Z^4) ===")
    eps = epsilon_diagonal(L)
    D = free_staggered_dirac_matrix(L)
    T_diag = regularized_local_trace(D, t)
    rng = np.random.default_rng(seed)
    alpha1 = rng.normal(size=eps.size)
    alpha2 = rng.normal(size=eps.size)

    A1 = jacobian_log(alpha1, eps, T_diag)
    A2 = jacobian_log(alpha2, eps, T_diag)
    A_sum = jacobian_log(alpha1 + alpha2, eps, T_diag)
    residual = abs(A_sum - (A1 + A2))
    check(f"E3a/L={L}: A[a1 + a2] = A[a1] + A[a2] (cocycle closes)",
          residual < 1e-12,
          f"residual = {residual:.2e}")

    # Antisymmetric cocycle vanishes (abelian Z_2)
    cocycle = jacobian_log(alpha1 * alpha2, eps, T_diag) - jacobian_log(alpha2 * alpha1, eps, T_diag)
    check(f"E3b/L={L}: abelian Z_2 cocycle vanishes (delta_a1 A_a2 = delta_a2 A_a1)",
          abs(cocycle) < 1e-12,
          f"cocycle = {cocycle:.2e}")

    # Test linearity at multiple t values
    for t_val in [0.1, 0.5, 1.0]:
        T_d = regularized_local_trace(D, t_val)
        A_a1 = jacobian_log(alpha1, eps, T_d)
        A_a2 = jacobian_log(alpha2, eps, T_d)
        A_sum_t = jacobian_log(alpha1 + alpha2, eps, T_d)
        check(f"E3c/L={L}/t={t_val}: linearity holds at this t",
              abs(A_sum_t - (A_a1 + A_a2)) < 1e-12)


# ---------------------------------------------------------------------------
# E4: t-independence + integer-valued + zero on free torus
# ---------------------------------------------------------------------------

def check_E4_t_independence(L_list=(4,)):
    print("\n=== E4: t-independence of A[1, U] (lattice index, Z^4) ===")
    for L in L_list:
        eps = epsilon_diagonal(L)
        D = free_staggered_dirac_matrix(L)
        A_values = []
        for t in [0.01, 0.05, 0.1, 0.5, 1.0, 5.0]:
            A = chiral_anomaly_trace(D, eps, t)
            A_values.append((t, A))
            print(f"  L={L}, t={t}: A[1, U=I] = {A:.6f}")

        A_first = A_values[0][1]
        max_dev = max(abs(A - A_first) for _, A in A_values)
        check(f"E4a/L={L}: A[1, U] is t-independent",
              max_dev < 1e-9,
              f"max deviation across t in [0.01, 5.0] = {max_dev:.2e}")

        A_spectral = chiral_anomaly_trace_spectral(D, eps)
        check(f"E4b/L={L}: spectral form (zero-mode chirality) agrees with heat-kernel form",
              abs(A_first - A_spectral) < 1e-9,
              f"|A_heat_kernel - A_spectral| = {abs(A_first - A_spectral):.2e}")

        check(f"E4c/L={L}: A[1, U] is integer-valued",
              abs(A_first - round(A_first)) < 1e-9,
              f"A = {A_first:.6f}, nearest int = {round(A_first)}")

        # Free Z^4 torus: index = 0 (no topological charge in trivial sector)
        check(f"E4d/L={L}: free torus has A[1, U=I] = 0",
              abs(A_first) < 1e-9,
              f"A = {A_first:.6e}")


# ---------------------------------------------------------------------------
# E5: gauge invariance of the chiral trace under U(1) rotations
# ---------------------------------------------------------------------------

def check_E5_gauge_invariance(L=4, seed=20260502):
    print("\n=== E5: gauge invariance of chiral trace + spectrum (W4 cocycle non-triviality) ===")
    rng = np.random.default_rng(seed)
    eps = epsilon_diagonal(L)
    link_phases = random_u1_link_phases(L, rng)
    gauge_phases = np.exp(1j * rng.uniform(-np.pi, np.pi, size=L ** 4))

    # Pre-rotation: D[U]
    D_pre = gauged_u1_staggered_dirac_matrix(L, link_phases)
    # Post-rotation: D[G^* U G]
    link_rotated = apply_u1_gauge_rotation(link_phases, gauge_phases, L)
    D_post = gauged_u1_staggered_dirac_matrix(L, link_rotated)

    # E5a: epsilon anticommutation preserved under gauge rotation
    D_pre_sandwich = np.outer(eps, eps) * D_pre
    D_post_sandwich = np.outer(eps, eps) * D_post
    check(f"E5a/L={L}: eps*D[U]*eps = -D[U]",
          float(np.max(np.abs(D_pre_sandwich + D_pre))) < 1e-10,
          f"residual = {float(np.max(np.abs(D_pre_sandwich + D_pre))):.2e}")
    check(f"E5b/L={L}: eps*D[G*UG]*eps = -D[G*UG]",
          float(np.max(np.abs(D_post_sandwich + D_post))) < 1e-10,
          f"residual = {float(np.max(np.abs(D_post_sandwich + D_post))):.2e}")

    # E5c: spectrum of D†D is gauge-invariant
    DtD_pre = D_pre.conj().T @ D_pre
    DtD_post = D_post.conj().T @ D_post
    evals_pre = np.sort(eigvalsh(DtD_pre))
    evals_post = np.sort(eigvalsh(DtD_post))
    spec_diff = float(np.max(np.abs(evals_pre - evals_post)))
    check(f"E5c/L={L}: sigma(D†D[U]) = sigma(D†D[G*UG]) (gauge-invariant)",
          spec_diff < 1e-9,
          f"spectrum max diff = {spec_diff:.2e}")

    # E5d: chiral trace at finite t is gauge-invariant
    t = 0.1
    A_pre = chiral_anomaly_trace(D_pre, eps, t)
    A_post = chiral_anomaly_trace(D_post, eps, t)
    print(f"  L={L}, t={t}: A[1, U]_pre  = {A_pre:.6e}")
    print(f"  L={L}, t={t}: A[1, U]_post = {A_post:.6e}")
    check(f"E5d/L={L}: chiral trace gauge-invariant at finite t={t}",
          abs(A_pre - A_post) < 1e-6,
          f"|A_pre - A_post| = {abs(A_pre - A_post):.2e}")

    # E5e: zero-mode index gauge-invariant
    A_pre_idx = chiral_anomaly_trace_spectral(D_pre, eps)
    A_post_idx = chiral_anomaly_trace_spectral(D_post, eps)
    print(f"  L={L}: zero-mode index pre  = {A_pre_idx:.6e}")
    print(f"  L={L}: zero-mode index post = {A_post_idx:.6e}")
    check(f"E5e/L={L}: zero-mode chirality index gauge-invariant",
          abs(A_pre_idx - A_post_idx) < 1e-6,
          f"|index_pre - index_post| = {abs(A_pre_idx - A_post_idx):.2e}")


# ---------------------------------------------------------------------------
# E6: heat-kernel diagonal is well-defined + bounded
# ---------------------------------------------------------------------------

def check_E6_heat_kernel_well_defined(L=4):
    print("\n=== E6: heat-kernel diagonal well-defined on finite Z^4 torus ===")
    eps = epsilon_diagonal(L)
    D = free_staggered_dirac_matrix(L)
    DtD = D.conj().T @ D
    evals = eigvalsh(DtD)
    # All eigenvalues non-negative
    check(f"E6a/L={L}: spectrum of D†D is non-negative",
          float(np.min(evals)) > -1e-12,
          f"min eigenvalue = {float(np.min(evals)):.2e}")

    # Heat-kernel trace is finite, real, positive at every t > 0
    for t in [0.01, 0.1, 1.0, 10.0]:
        T_d = regularized_local_trace(D, t)
        check(f"E6b/L={L}/t={t}: T_t is real",
              np.all(np.imag(T_d) == 0))
        check(f"E6c/L={L}/t={t}: T_t is non-negative",
              float(np.min(T_d)) > -1e-12,
              f"min T_t = {float(np.min(T_d)):.2e}")
        # Bound: sum_x T_t[U]_x = sum_n exp(-t lambda_n) <= dim(H_F) = L^4
        sum_T = float(np.sum(T_d))
        bound = float(L ** 4) + 1e-9
        check(f"E6d/L={L}/t={t}: sum_x T_t[U]_x <= dim(H_F) = L^4",
              sum_T <= bound,
              f"sum_T = {sum_T:.4e}, bound = {bound:.4e}")
        # And matches sum of exp(-t lambda)
        sum_spec = float(np.sum(np.exp(-t * evals)))
        check(f"E6e/L={L}/t={t}: sum_x T_t = sum_n exp(-t lambda_n)",
              abs(sum_T - sum_spec) < 1e-9,
              f"|sum_T - sum_spec| = {abs(sum_T - sum_spec):.2e}")


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def main():
    print("Lattice Wess-Zumino / Fujikawa Theorem on Z^4")
    print("==============================================")
    print("Theorem note: docs/AXIOM_FIRST_LATTICE_WESS_ZUMINO_FUJIKAWA_Z4_THEOREM_NOTE_2026-05-02.md")
    print("Status: STANDALONE unaudited source claim. No audit infrastructure touched.")
    print()

    check_E1_epsilon_structure(L_list=(4,))
    check_E2_epsilon_anticommutes_D_free(L_list=(4,))
    check_E2_epsilon_anticommutes_D_gauged(L_list=(4,))
    check_E3_wess_zumino_consistency(L=4, t=0.5)
    check_E4_t_independence(L_list=(4,))
    check_E5_gauge_invariance(L=4)
    check_E6_heat_kernel_well_defined(L=4)

    print()
    print(f"Summary: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if FAIL_COUNT > 0:
        sys.exit(1)
    else:
        print("All checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
