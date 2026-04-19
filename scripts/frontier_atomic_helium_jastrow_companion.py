#!/usr/bin/env python3
"""Helium Jastrow companion on the retained Cl(3)/Z³ lattice Hamiltonian surface.

==========================================================================
NUMERICAL JASTROW COMPANION ON THE LATTICE HAMILTONIAN SURFACE
==========================================================================

AXIOM 1: The physical local algebra is Cl(3).
AXIOM 2: The spatial substrate is the cubic lattice Z³.

Same kinetic operator and Coulomb kernel as
`frontier_atomic_helium_hartree_companion.py`.
The NEW step here is going beyond the separable (product-state) ansatz.

--------------------------------------------------------------------------
STEP 5-EXTENDED: JASTROW CORRELATION  [DERIVED from Z³ kernel]
--------------------------------------------------------------------------
The Hartree ansatz ψ(r₁,r₂) = φ(r₁)φ(r₂) is separable. The true
ground state is not separable: near r₁ ≈ r₂, V_ee = g_EM/|r₁-r₂| → ∞,
and the wavefunction must have a cusp to keep the local energy finite.

CUSP CONDITION (derived from the same Z³ Green's function kernel):
-----------------------------------------------------------------
Near contact r₁₂ = r₁ - r₂ → 0, write the eigenvalue equation:

    H₂ψ = Eψ
    (-Δ₁ - Δ₂ + V_nuc + g_EM/r₁₂) ψ = E ψ

Decompose into center-of-mass R = (r₁+r₂)/2 and relative r₁₂:
    -Δ₁ - Δ₂ = -(1/2)Δ_R - 2Δ_rel

The singular 1/r₁₂ term must be cancelled by the relative kinetic term.
In 3D spherical coordinates for r₁₂:

    -2(∂²/∂r₁₂² + (2/r₁₂)∂/∂r₁₂) + g_EM/r₁₂ = regular at r₁₂ → 0

At order 1/r₁₂:   -2 × (2/r₁₂) × ψ'(0) + g_EM/r₁₂ × ψ(0) = 0

Therefore:   ψ'(0) = (g_EM/4) × ψ(0)   [KATO CUSP CONDITION]

On the lattice Hamiltonian surface this follows from:
    1. The kinetic operator -Δ_Z³ (Cl(3)/Z³ axiom)
    2. The interaction kernel g_EM/|r₁₂| (Z³ Green's function)
    3. Self-adjointness of H₂ on l²(Z³×Z³)  (mathematical requirement)

JASTROW ANSATZ:
--------------
Enrich the product state by a correlation factor:

    ψ_J(r₁,r₂) = φ_H(r₁) × φ_H(r₂) × f_J(|r₁-r₂|)

where φ_H is the Hartree orbital (from the SCF) and f_J is a
correlation function satisfying the cusp condition.

Natural form (satisfies cusp + boundary conditions):

    f_J(r) = exp(u(r))
    u(r) = -(g_EM × r_J / 4) × exp(-r/r_J)

This gives:
    u'(0) = g_EM/4  ✓  [cusp condition, DERIVED above]
    u(∞) = 0        ✓  [no long-range correlation]
    f_J(∞) = 1      ✓  [uncorrelated at large separation]

The single variational parameter r_J (correlation length) is optimized
by minimizing the VMC energy ⟨E_L⟩.

VARIATIONAL MONTE CARLO (VMC):
------------------------------
The variational principle on l²(Z³×Z³) (Rayleigh-Ritz) guarantees:

    E_VMC = ⟨ψ_J | H₂ | ψ_J⟩ / ⟨ψ_J | ψ_J⟩ ≥ E_exact

We estimate E_VMC by sampling (r₁, r₂) from the distribution |ψ_J|²
using the Metropolis algorithm and averaging the local energy:

    E_L(r₁,r₂) = H₂ ψ_J(r₁,r₂) / ψ_J(r₁,r₂)

For the lattice Hamiltonian:
    E_L = T₁_L + T₂_L + V_nuc(r₁) + V_nuc(r₂) + g_EM/r₁₂

where:
    T_i_L(r_i) = 6 - Σ_{nn y of r_i} [φ_H(y)/φ_H(r_i)] × [f_J(|y-r_j|)/f_J(r₁₂)]

This is computable from φ_H and f_J alone: no matrices, no N⁶ problem.

COMPARISON (all dimensionless, coupling-independent):
-----------------------------------------------------
                 | E/E(He⁺) | Method
  ───────────────────────────────────────────────────
  Separable      |  ~1.424  | Hartree (product state)
  Jastrow        |  ~1.43+  | This script (+ cusp correlation)
  Full CI        |   1.452  | Exact (not tractable on lattice)
  Experiment     |   1.452  | Target (same as full CI for ground state)
  ───────────────────────────────────────────────────

The Jastrow correction captures a fraction of the correlation energy on
the same lattice surface. This is a bounded companion, not a closure of
the two-electron problem.

==========================================================================
"""

from __future__ import annotations

import os
import time

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh, spsolve


# ---------------------------------------------------------------------------
# Lattice operators (identical to frontier_atomic_helium_hartree_companion.py)
# ---------------------------------------------------------------------------

def build_graph_laplacian(N: int) -> sparse.csr_matrix:
    """Negative graph Laplacian -Δ_Z³ on N³ grid (Dirichlet BCs)."""
    diag = 2.0 * np.ones(N)
    off  = -1.0 * np.ones(N - 1)
    T1d  = sparse.diags([off, diag, off], [-1, 0, 1], shape=(N, N), format='csr')
    I    = sparse.eye(N, format='csr')
    T3 = (sparse.kron(sparse.kron(T1d, I), I) +
          sparse.kron(sparse.kron(I, T1d), I) +
          sparse.kron(sparse.kron(I, I), T1d))
    return T3.tocsr()


def build_coulomb_potential(N: int, g: float) -> np.ndarray:
    """V(r) = -g/|r| from Z³ Green's function; regularized at origin."""
    center = (N - 1) / 2.0
    ix, iy, iz = np.indices((N, N, N))
    r = np.sqrt((ix - center)**2 + (iy - center)**2 + (iz - center)**2).ravel()
    return -g / np.maximum(r, 0.5)


def solve_single_particle(T: sparse.csr_matrix,
                           V_nuc: np.ndarray,
                           V_extra: np.ndarray | None = None,
                           n_eig: int = 3) -> tuple[np.ndarray, np.ndarray]:
    V = V_nuc.copy()
    if V_extra is not None:
        V = V + V_extra
    H = T + sparse.diags(V, 0, format='csr')
    k = min(n_eig, T.shape[0] - 2)
    evals, evecs = eigsh(H, k=k, which='SA')
    idx = np.argsort(evals)
    return evals[idx], evecs[:, idx]


def solve_poisson(N: int, rho: np.ndarray, T: sparse.csr_matrix,
                  g_em: float) -> np.ndarray:
    """(-Δ_Z³) V_H = 4π g_EM ρ  (same Green's function kernel)."""
    rhs = 4.0 * np.pi * g_em * rho
    try:
        return spsolve(T.tocsc(), rhs)
    except Exception:
        from scipy.sparse.linalg import cg
        V, _ = cg(T, rhs, maxiter=2000, tol=1e-8)
        return V


def run_hartree_scf(N: int, g_nuc: float, g_em: float,
                    max_iter: int = 60, tol: float = 1e-6,
                    mix: float = 0.5) -> dict:
    """Hartree SCF — returns phi, E_var, and E(He⁺)."""
    T = build_graph_laplacian(N)
    V_nuc = build_coulomb_potential(N, g_nuc)

    _, evecs_init = solve_single_particle(T, V_nuc, n_eig=3)
    phi = evecs_init[:, 0].copy()
    phi /= np.sqrt(np.sum(phi**2))
    rho = phi**2
    V_H = np.zeros(N**3)

    for _ in range(max_iter):
        V_H_new = solve_poisson(N, rho, T, g_em)
        V_H = mix * V_H_new + (1.0 - mix) * V_H
        evals, evecs = solve_single_particle(T, V_nuc, V_H, n_eig=3)
        phi_new = evecs[:, 0].copy()
        phi_new /= np.sqrt(np.sum(phi_new**2))
        rho_new = phi_new**2
        if float(np.sqrt(np.sum((rho_new - rho)**2))) < tol:
            break
        phi, rho = phi_new, rho_new

    eps = float(evals[0])
    E_J = 0.5 * float(np.sum(rho * V_H))
    E_var = 2.0 * eps - E_J

    # He⁺ reference
    evals_hep, _ = solve_single_particle(T, V_nuc, n_eig=1)
    E_hep = float(evals_hep[0])

    return {"phi": phi, "rho": rho, "E_var": E_var, "E_hep": E_hep,
            "eps": eps, "E_J": E_J, "T": T, "V_nuc": V_nuc, "N": N}


# ---------------------------------------------------------------------------
# Jastrow factor (cusp condition derived from Z³ Green's function)
# ---------------------------------------------------------------------------

def make_jastrow(g_em: float, r_J: float):
    """Return f_J(r) = exp(-(g_EM × r_J / 4) × exp(-r/r_J)).

    Cusp condition (derived):  df_J/dr|_{r=0} = (g_EM/4) × f_J(0)
    Boundary condition:        f_J(r) → 1  as  r → ∞
    """
    a = g_em * r_J / 4.0

    def fJ(r: float) -> float:
        return float(np.exp(-a * np.exp(-r / r_J)))

    return fJ


# ---------------------------------------------------------------------------
# VMC local energy
# ---------------------------------------------------------------------------

def local_energy(r1: np.ndarray, r2: np.ndarray,
                 phi_3d: np.ndarray, V_nuc_3d: np.ndarray,
                 g_em: float, N: int, fJ) -> float:
    """E_L(r₁,r₂) = H₂ψ_J(r₁,r₂) / ψ_J(r₁,r₂).

    Kinetic part for electron i (i=1,2):
        T_i_L = 6 - Σ_{nn y of rᵢ} [φ_H(y)/φ_H(rᵢ)] × [f_J(|y-rⱼ|)/f_J(r₁₂)]
    """
    i1, j1, k1 = int(r1[0]), int(r1[1]), int(r1[2])
    i2, j2, k2 = int(r2[0]), int(r2[1]), int(r2[2])
    phi_r1 = phi_3d[i1, j1, k1]
    phi_r2 = phi_3d[i2, j2, k2]

    r12 = float(np.sqrt(np.sum((r1 - r2)**2)))
    f12 = fJ(max(r12, 1e-12))

    T1 = 6.0
    if phi_r1 != 0.0:
        for d in range(3):
            for delta in (-1, 1):
                y = r1.copy(); y[d] += delta
                if 0 <= y[d] < N:
                    iy = (int(y[0]), int(y[1]), int(y[2]))
                    ry12 = float(np.sqrt(np.sum((y - r2)**2)))
                    T1 -= (phi_3d[iy] / phi_r1) * (fJ(ry12) / f12)

    T2 = 6.0
    if phi_r2 != 0.0:
        for d in range(3):
            for delta in (-1, 1):
                y = r2.copy(); y[d] += delta
                if 0 <= y[d] < N:
                    iy = (int(y[0]), int(y[1]), int(y[2]))
                    ry12 = float(np.sqrt(np.sum((r1 - y)**2)))
                    T2 -= (phi_3d[iy] / phi_r2) * (fJ(ry12) / f12)

    V1 = V_nuc_3d[i1, j1, k1]
    V2 = V_nuc_3d[i2, j2, k2]
    V12 = g_em / max(r12, 0.5)

    return T1 + T2 + V1 + V2 + V12


# ---------------------------------------------------------------------------
# Metropolis VMC
# ---------------------------------------------------------------------------

def run_vmc(phi_3d: np.ndarray, V_nuc_3d: np.ndarray,
            g_em: float, g_nuc: float, N: int, r_J: float,
            n_warmup: int = 3000, n_meas: int = 40000,
            seed: int = 42) -> dict:
    """Metropolis VMC for ψ_J = φ_H(r₁)φ_H(r₂)f_J(r₁₂).

    Returns mean and standard error of E_L, and the acceptance rate.
    """
    rng = np.random.default_rng(seed)
    fJ = make_jastrow(g_em, r_J)

    # Initialize walkers well inside the box
    m = max(2, N // 4)
    hi = N - m - 1
    r1 = np.array([rng.integers(m, hi+1) for _ in range(3)], dtype=float)
    r2 = np.array([rng.integers(m, hi+1) for _ in range(3)], dtype=float)
    while np.allclose(r1, r2):
        r2 = np.array([rng.integers(m, hi+1) for _ in range(3)], dtype=float)

    def psi2(ra, rb):
        i, j, k = int(ra[0]), int(ra[1]), int(ra[2])
        p, q, s = int(rb[0]), int(rb[1]), int(rb[2])
        pa = phi_3d[i, j, k]
        pb = phi_3d[p, q, s]
        r12 = float(np.sqrt(np.sum((ra - rb)**2)))
        return (pa * pb * fJ(max(r12, 1e-12)))**2

    w_old = psi2(r1, r2)
    energies = []
    n_accept = 0

    for step in range(n_warmup + n_meas):
        e = int(rng.integers(2))
        d = int(rng.integers(3))
        delta = int(rng.choice([-1, 1]))

        if e == 0:
            r1_new = r1.copy(); r1_new[d] += delta
            r2_new = r2
        else:
            r1_new = r1
            r2_new = r2.copy(); r2_new[d] += delta

        if (np.any(r1_new < 0) or np.any(r1_new >= N) or
                np.any(r2_new < 0) or np.any(r2_new >= N)):
            if step >= n_warmup:
                energies.append(local_energy(r1, r2, phi_3d, V_nuc_3d, g_em, N, fJ))
            continue

        w_new = psi2(r1_new, r2_new)
        ratio = w_new / w_old if w_old > 0 else 1.0

        if rng.random() < ratio:
            r1, r2 = r1_new, r2_new
            w_old = w_new
            n_accept += 1

        if step >= n_warmup:
            energies.append(local_energy(r1, r2, phi_3d, V_nuc_3d, g_em, N, fJ))

    E_arr = np.array(energies)
    # Block averaging for error estimate (blocks of 200)
    block = 200
    n_blocks = len(E_arr) // block
    block_means = [np.mean(E_arr[i*block:(i+1)*block]) for i in range(n_blocks)]
    stderr = float(np.std(block_means) / np.sqrt(n_blocks)) if n_blocks > 1 else float('nan')

    return {
        "E_mean": float(np.mean(E_arr)),
        "E_stderr": stderr,
        "accept_rate": n_accept / (n_warmup + n_meas),
        "r_J": r_J,
        "n_meas": len(E_arr),
    }


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

LOG: list[str] = []


def log(msg: str = "") -> None:
    LOG.append(msg)
    print(msg)


def run_experiment() -> None:
    log("=" * 72)
    log("HELIUM JASTROW COMPANION ON THE Cl(3)/Z³ SURFACE")
    log("One-parameter correlation improvement on the retained two-electron kernel")
    log("=" * 72)
    log()

    # Coupling setup: same as frontier_atomic_helium_hartree_companion.py
    G_EM  = 0.5
    G_NUC = 2.0 * G_EM
    N = 20   # N=20 for tractable VMC; N=30 for reference Hartree

    log("Cusp condition derivation:")
    log("  Near r₁₂ → 0: -2Δ_rel ψ + (g_EM/r₁₂) ψ = finite")
    log("  -2 × (2/r₁₂) × ψ'(0) + (g_EM/r₁₂) × ψ(0) = 0")
    log(f"  → ψ'(0)/ψ(0) = g_EM/4 = {G_EM/4:.4f}  [DERIVED, same kernel as V_ee]")
    log()
    log(f"Jastrow form: f_J(r) = exp(-(g_EM r_J / 4) exp(-r/r_J))")
    log(f"  r_J: variational parameter (correlation length)")
    log(f"  Satisfies: f_J'(0)/f_J(0) = g_EM/4  and  f_J(∞) = 1")
    log()
    log(f"Computational parameters: N={N}, g_EM={G_EM}, g_nuc={G_NUC}")
    log()

    # ------------------------------------------------------------------
    # Step 1: Hartree SCF at N=20 as baseline
    # ------------------------------------------------------------------
    log("─" * 60)
    log("STEP 1: Hartree baseline at N=20")
    log("─" * 60)
    t0 = time.time()
    scf = run_hartree_scf(N, G_NUC, G_EM)
    dt = time.time() - t0

    phi_flat = scf["phi"]
    phi_3d = phi_flat.reshape(N, N, N)

    center = (N - 1) / 2.0
    ix, iy, iz = np.indices((N, N, N))
    r_grid = np.sqrt((ix - center)**2 + (iy - center)**2 + (iz - center)**2)
    V_nuc_3d = -G_NUC / np.maximum(r_grid, 0.5)

    E_hep = scf["E_hep"]
    E_hartree = scf["E_var"]
    ratio_hartree = abs(E_hartree) / abs(E_hep)

    log(f"  E(He⁺)   = {E_hep:.6f}")
    log(f"  E_Hartree = {E_hartree:.6f}")
    log(f"  |E(He)|/|E(He⁺)| = {ratio_hartree:.5f}  (Hartree target ~1.424)")
    log(f"  Time: {dt:.1f}s")
    log()

    # ------------------------------------------------------------------
    # Step 2: Derive Jastrow cusp parameter and scan r_J
    # ------------------------------------------------------------------
    log("─" * 60)
    log("STEP 2: Jastrow VMC scan over r_J (correlation length)")
    log("─" * 60)
    log()
    log(f"  Fixed: cusp coefficient a = g_EM × r_J / 4 → u'(0) = g_EM/4 = {G_EM/4:.4f}")
    log(f"  Scan r_J ∈ {{0.5, 1.0, 2.0, 3.0, 4.0, 6.0}} lattice units")
    log(f"  VMC: {3000} warmup + {40000} measurement steps per r_J")
    log()
    log(f"  {'r_J':>5}  {'E_VMC':>12}  {'±':>10}  {'|E|/|E(He⁺)|':>14}  "
        f"{'vs Hartree':>12}  {'accept':>7}")
    log("  " + "─" * 70)

    r_J_values = [0.5, 1.0, 2.0, 3.0, 4.0, 6.0]
    results = []
    t0_scan = time.time()

    for r_J in r_J_values:
        t_start = time.time()
        vmc = run_vmc(phi_3d, V_nuc_3d, G_EM, G_NUC, N, r_J,
                      n_warmup=3000, n_meas=40000, seed=42)
        dt_rJ = time.time() - t_start

        ratio_vmc = abs(vmc["E_mean"]) / abs(E_hep)
        delta_pct = 100.0 * (vmc["E_mean"] - E_hartree) / abs(E_hartree)
        results.append({**vmc, "ratio": ratio_vmc, "delta_pct": delta_pct})

        log(f"  {r_J:5.1f}  {vmc['E_mean']:12.6f}  ±{vmc['E_stderr']:9.6f}  "
            f"{ratio_vmc:14.5f}  {delta_pct:+11.2f}%  "
            f"{vmc['accept_rate']:6.2f}  ({dt_rJ:.1f}s)")

    dt_total = time.time() - t0_scan
    log(f"\n  Total scan time: {dt_total:.1f}s")
    log()

    # Find optimal r_J (lowest E_mean)
    best = min(results, key=lambda r: r["E_mean"])
    log(f"  Optimal r_J = {best['r_J']:.1f}  →  E_VMC = {best['E_mean']:.6f} ± {best['E_stderr']:.6f}")
    log()

    # ------------------------------------------------------------------
    # Step 3: Quantify correlation energy captured
    # ------------------------------------------------------------------
    log("─" * 60)
    log("STEP 3: Correlation energy captured by Jastrow")
    log("─" * 60)
    log()

    E_exact_scale = -G_NUC**2 / 4.0  # = E(He⁺) continuum
    E_exact_CI_ratio = 1.452          # full CI (historical reference)
    E_exact_CI = E_exact_CI_ratio * abs(E_exact_scale)  # for comparison

    E_hartree_gap = E_hartree - E_hep * 1.424  # Hartree−reference gap
    E_jastrow_best = best["E_mean"]

    ratio_jastrow = abs(E_jastrow_best) / abs(E_hep)
    ratio_CI = E_exact_CI_ratio

    # Correlation energy = exact - Hartree (in dimensionless units)
    corr_total = (ratio_CI - ratio_hartree) * abs(E_hep)
    corr_captured = abs(E_jastrow_best) - abs(E_hartree)
    frac_captured = corr_captured / corr_total if corr_total != 0 else float('nan')

    log(f"  E(He⁺) lattice:              {E_hep:.6f}")
    log(f"  E_Hartree:                   {E_hartree:.6f}  ratio = {ratio_hartree:.4f}")
    log(f"  E_Jastrow (opt r_J={best['r_J']:.0f}):    {E_jastrow_best:.6f}  ratio = {ratio_jastrow:.4f}")
    log(f"  Full CI reference ratio:     {ratio_CI:.4f}  (historical checkpoint)")
    log()
    log(f"  Correlation energy (CI - Hartree in ratio units): {ratio_CI - ratio_hartree:.4f}")
    log(f"  Correlation captured by Jastrow:   {ratio_jastrow - ratio_hartree:.4f}  "
        f"({100*frac_captured:.0f}% of total)")
    log()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    log("=" * 72)
    log("SUMMARY: HELIUM JASTROW COMPANION")
    log("=" * 72)
    log()

    rows = [
        ("Hartree (product)", ratio_hartree, 1.424, "separable ansatz; Hartree target"),
        (f"Jastrow (r_J={best['r_J']:.0f})", ratio_jastrow, None, "cusp corr. from Z³ kernel"),
        ("Full CI", 1.452, 1.452, "exact (historical checkpoint)"),
    ]
    log(f"  {'Method':>24}  {'|E(He)|/|E(He⁺)|':>18}  {'Target':>8}  Notes")
    log("  " + "─" * 70)
    for label, val, ref, note in rows:
        if ref is not None:
            err = 100.0 * (val - ref) / abs(ref)
            log(f"  {label:>24}  {val:18.5f}  {ref:8.4f}  ({err:+.1f}%)  {note}")
        else:
            log(f"  {label:>24}  {val:18.5f}  {'n/a':>8}  {note}")

    log()
    log("  DERIVATION STATUS:")
    log("  ✓ Cusp condition u'(0) = g_EM/4 derived from Z³ Green's function")
    log("  ✓ Jastrow form f_J(r) = exp(-a exp(-r/r_J)) satisfies both conditions")
    log("  ✓ VMC variational bound E_VMC ≥ E_exact (Rayleigh-Ritz on l²(Z³×Z³))")
    log("  ✓ Parameter r_J optimized variationally — no new physics inputs")
    log()
    log("  WHAT JASTROW CAPTURES:")
    log("  The electron-electron correlation hole: electrons avoid each other")
    log("  near contact. The cusp coefficient g_EM/4 is the SAME coupling that")
    log("  enters V_ee — the correlation is driven by the same Z³ kernel.")
    log()
    log("  WHAT REMAINS BEYOND JASTROW:")
    log("  Three-body and higher correlations (higher-order Jastrow terms)")
    log("  Backflow correlations (momentum-dependent Jastrow)")
    log("  These would be derived from higher-order terms in the 1/Z expansion")
    log("  of the two-body resolvent of H₂ on l²(Z³×Z³).")
    log()
    log("  BLOCKED:")
    log("  ✗ Absolute energy in eV still needs the electron-mass lane")
    log("  ✗ Exact two-body result remains open; Jastrow/VMC is only a bounded companion")
    log("=" * 72)

    os.makedirs("logs", exist_ok=True)
    log_path = f"logs/{time.strftime('%Y-%m-%d')}-atomic_helium_jastrow_companion.txt"
    try:
        with open(log_path, "w") as f:
            f.write("\n".join(LOG))
        print(f"\nLog saved to: {log_path}")
    except Exception as e:
        print(f"  (Could not write log: {e})")


if __name__ == "__main__":
    run_experiment()
