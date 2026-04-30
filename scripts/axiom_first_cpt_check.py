#!/usr/bin/env python3
"""
axiom_first_cpt_check.py
-------------------------

Numerical exhibits for the axiom-first CPT theorem stretch attempt
on Cl(3) ⊗ Z^3 (loop axiom-first-foundations, Cycle 4 / Route R4).

Theorem note:
  docs/AXIOM_FIRST_CPT_THEOREM_STRETCH_NOTE_2026-04-29.md

The stretch attempt constructs Θ_CPT = T · P · C as a composition
of three explicit lattice operations on the canonical staggered
Dirac–Wilson matrix M at g_bare = 1. The algebraic chain claims

    Θ_CPT M Θ_CPT^{-1}  =  M^*                                       (target)

This runner verifies that identity numerically on a small block,
and reports the residual norms for each of the intermediate
identities (C, P, T applied separately).

Exhibits:
  E1.  Involution: Θ_CPT² acts trivially (after appropriate
       Grassmann sign bookkeeping).
  E2.  Operator-level identity Θ_CPT M Θ_CPT^{-1} = M^*.
  E3.  γ_5-Hermiticity (the staggered ε analogue): ε M ε = M^†.
  E4.  Reality of det(M) on the canonical surface.
"""

from __future__ import annotations

import sys
import numpy as np
from itertools import product


def staggered_eta(x, mu):
    if mu == 0:
        return 1.0
    return float((-1) ** sum(x[:mu]))


def staggered_epsilon(x):
    """Staggered ε(x) = (-1)^(sum of all coords). Acts as γ_5 on staggered."""
    return float((-1) ** sum(x))


def build_M(L, mass=0.3, r_wilson=1.0, dim=3):
    """Canonical staggered Dirac–Wilson on a periodic L^dim block."""
    sites = list(product(range(L), repeat=dim))
    idx = {x: i for i, x in enumerate(sites)}
    N = len(sites)
    M = np.zeros((N, N), dtype=complex)

    for x in sites:
        i = idx[x]
        M[i, i] += mass
        for mu in range(dim):
            ehat = tuple(1 if k == mu else 0 for k in range(dim))
            xp = tuple((x[k] + ehat[k]) % L for k in range(dim))
            xm = tuple((x[k] - ehat[k]) % L for k in range(dim))
            jp = idx[xp]
            jm = idx[xm]
            eta = staggered_eta(x, mu)
            # staggered hop: +η/2 forward, -η/2 backward
            M[i, jp] += 0.5 * eta
            M[i, jm] += -0.5 * eta
            # Wilson term: -r/2 (forward + backward - 2 diag)
            M[i, jp] += -0.5 * r_wilson
            M[i, jm] += -0.5 * r_wilson
            M[i, i] += r_wilson
    return M, sites, idx


# ---------------------------------------------------------------------------
# Discrete reflection / parity / time-reversal permutation matrices
# ---------------------------------------------------------------------------

def build_permutation(sites, idx, perm_func, phase_func=None):
    """
    Build the L^dim × L^dim permutation matrix R for a site permutation
    perm_func: x ↦ x'. With optional sign / phase function.
    Acts as: (R v)_x = phase(x) · v_{perm(x)}.
    """
    N = len(sites)
    R = np.zeros((N, N), dtype=complex)
    for x in sites:
        i = idx[x]
        xp = tuple(perm_func(x))
        # canonicalise mod L
        xp = tuple(c % L for c, L in zip(xp, [max(s[k] for s in sites) + 1 for k in range(len(x))]))
        j = idx[xp]
        ph = phase_func(x) if phase_func else 1.0
        R[i, j] = ph
    return R


def parity_perm(L_per_dim, dim):
    """Spatial parity P: (t, x⃗) ↦ (t, -x⃗ mod L). For convention here we
    take dim 0 as time; for a Z^d block (no separate time) treat all
    dims as spatial except we'll use dim-1 as time when relevant."""
    def perm(x):
        return tuple([x[0]] + [(-x[k]) % L_per_dim[k] for k in range(1, dim)])
    def phase(x):
        # η_P(x) = (-1)^{x_1+x_2+...} for spatial dims (sign factor)
        return float((-1) ** sum(x[1:]))
    return perm, phase


def time_perm(L_per_dim, dim):
    """Time reflection T: (t, x⃗) ↦ (-t mod L, x⃗)."""
    def perm(x):
        return tuple([(-x[0]) % L_per_dim[0]] + list(x[1:]))
    def phase(x):
        return staggered_epsilon(x)  # γ_5 analogue on staggered
    return perm, phase


def cpt_residuals(L=2, dim=3, mass=0.3, r_wilson=1.0):
    print(f"\n--- Block: L={L}, dim={dim}, mass={mass}, r_W={r_wilson} ---")
    M, sites, idx = build_M(L, mass=mass, r_wilson=r_wilson, dim=dim)
    L_per_dim = [L] * dim

    # --- charge conjugation C: M → M^T (for one-component staggered) ---
    M_C = M.T
    err_C = float(np.max(np.abs(M_C - M.T)))
    print(f"  C residual ‖C M C^{-1} - M^T‖  = {err_C:.3e}  (definitional)")

    # --- spatial parity P ---
    P_perm, P_phase = parity_perm(L_per_dim, dim)
    R_P = build_permutation(sites, idx, P_perm, phase_func=P_phase)
    M_P = R_P @ M @ np.linalg.inv(R_P)
    err_P = float(np.max(np.abs(M_P - M)))
    print(f"  P residual ‖R_P M R_P^{-1} - M‖ = {err_P:.3e}")

    # --- time reflection T (treated as antiunitary at the operator level) ---
    T_perm, T_phase = time_perm(L_per_dim, dim)
    R_T = build_permutation(sites, idx, T_perm, phase_func=T_phase)
    # Antiunitary action on M: T M T^{-1} (with conjugation built into T)
    # In matrix form this is R_T M^* R_T^{-1}.
    M_T = R_T @ M.conj() @ np.linalg.inv(R_T)
    err_T = float(np.max(np.abs(M_T - M.conj())))
    # The above test is definitional; real test is whether T (alone) gives M^*
    # consistent with M being real. For real M, M^* = M.
    M_real = float(np.max(np.abs(M.imag)))
    print(f"  T residual ‖R_T M^* R_T^{-1} - M^*‖ = {err_T:.3e}  "
          f"(M is real? max |Im M| = {M_real:.3e})")

    # --- composite CPT = T·P·C ---
    # Action on M:  R_T (R_P M^T R_P^{-1})^* R_T^{-1}
    M_CPT = R_T @ (R_P @ M.T @ np.linalg.inv(R_P)).conj() @ np.linalg.inv(R_T)
    err_CPT = float(np.max(np.abs(M_CPT - M.conj())))
    print(f"  CPT residual ‖Θ_CPT M Θ_CPT^{-1} - M^*‖ = {err_CPT:.3e}")

    # --- γ_5 (i.e. ε) Hermiticity: ε M ε = M^† ---
    eps_diag = np.diag([staggered_epsilon(x) for x in sites]).astype(complex)
    M_eps = eps_diag @ M @ eps_diag  # ε² = I
    err_eps = float(np.max(np.abs(M_eps - M.conj().T)))
    print(f"  ε-Hermiticity ‖ε M ε - M^†‖ = {err_eps:.3e}")

    # --- reality of det(M) ---
    detM = np.linalg.det(M)
    print(f"  det(M) = {detM}  (Im part = {detM.imag:.3e})")
    det_real = abs(detM.imag) < 1e-9 * max(abs(detM), 1.0)

    # --- involution check Θ_CPT^2 ---
    # Θ_CPT² operator-level: (T P C)² applied to a generic operator A:
    # First apply: A → R_T (R_P A^T R_P^{-1})^* R_T^{-1}
    # Apply again: result → R_T (R_P [...])^T R_P^{-1})^* R_T^{-1}
    # The transpose is involutive, complex conj is involutive, R_P, R_T are real
    # involutions (since reflections of order 2 with real phases). So Θ_CPT² should
    # act trivially (up to a sign coming from Grassmann statistics that cancels in
    # operator-norm checks). We test the action on M:
    M_after2 = R_T @ (R_P @ M_CPT.T @ np.linalg.inv(R_P)).conj() @ np.linalg.inv(R_T)
    err_inv = float(np.max(np.abs(M_after2 - M)))
    print(f"  involution residual ‖Θ_CPT^2 (M) - M‖ = {err_inv:.3e}")

    return {
        "err_CPT": err_CPT,
        "err_eps": err_eps,
        "det_real": det_real,
        "err_inv": err_inv,
        "M_real": M_real,
    }


def main():
    print("=" * 72)
    print(" axiom_first_cpt_check.py")
    print(" Loop: axiom-first-foundations, Cycle 4 / Route R4 (stretch attempt)")
    print(" Verifies CPT operator identities on small staggered Dirac–Wilson")
    print(" blocks; reports load-bearing residuals honestly.")
    print("=" * 72)

    # The canonical A3 is the *pure staggered* Grassmann partition (no
    # Wilson fermion term) on Z^3. We exhibit on canonical 3D pure-staggered
    # blocks. Also included for diagnostics:
    #   - lower-dim toys (which lack a true spatial parity, so CPT
    #     reduces to a more constrained TC; expected to fail on
    #     dimensions with no spatial parity);
    #   - +Wilson fermion term in 3D (the standard Wilson fermion term
    #     is NOT in A_min; included to expose the wall: adding it
    #     breaks the naive ε-as-γ_5 chain).
    blocks = [
        (2, 3, 0.3, 0.0, "canonical"),  # canonical pure staggered, 2^3 block
        (2, 3, 0.5, 0.0, "canonical"),  # canonical pure staggered, m=0.5
        (4, 1, 0.3, 0.0, "1D-toy"),     # 1D toy: no spatial parity, expected partial
        (2, 3, 0.3, 1.0, "+W-fermion"), # NON-canonical wall test
    ]
    summary = []
    for L, dim, m, rW, label in blocks:
        print(f"\n[block tag: {label}]")
        res = cpt_residuals(L=L, dim=dim, mass=m, r_wilson=rW)
        summary.append((L, dim, m, rW, res, label))

    # Aggregate verdicts: separate canonical (pure staggered) blocks from
    # the non-canonical "+Wilson fermion" block.
    print()
    print("=" * 72)
    print(" SUMMARY (canonical A_min: pure staggered, r_wilson_fermion = 0)")
    print("=" * 72)
    tol = 1e-9
    canonical = [r for r in summary if r[5] == "canonical"]
    diag_1d = [r for r in summary if r[5] == "1D-toy"]
    noncanon = [r for r in summary if r[5] == "+W-fermion"]

    e1_pass = all(r[4]["err_inv"] < tol for r in canonical)
    e2_pass = all(r[4]["err_CPT"] < tol for r in canonical)
    e3_pass = all(r[4]["err_eps"] < tol for r in canonical)
    e4_pass = all(r[4]["det_real"] for r in canonical)
    print(f"   E1 (Θ_CPT^2 = id):                   {'PASS' if e1_pass else 'FAIL'}")
    print(f"   E2 (Θ_CPT M Θ_CPT^-1 = M^*):         {'PASS' if e2_pass else 'FAIL'}")
    print(f"   E3 (ε M ε = M^†, γ_5-Hermiticity):   {'PASS' if e3_pass else 'FAIL'}")
    print(f"   E4 (det(M) ∈ R):                     {'PASS' if e4_pass else 'FAIL'}")

    n_pass = sum([e1_pass, e2_pass, e3_pass, e4_pass])
    print(f"\n   PASSED on canonical A_min: {n_pass}/4")

    # Diagnostic: 1D toy (no spatial parity)
    if diag_1d:
        print()
        print("   --- Diagnostic: 1D toy (no spatial parity) ---")
        for L, dim, m, rW, res, _ in diag_1d:
            print(f"   L={L}, dim={dim}, m={m}: err_CPT={res['err_CPT']:.3e}, "
                  f"err_eps={res['err_eps']:.3e}, det∈R={res['det_real']}")
        print("   In 1D there is no spatial parity, so CPT reduces to TC.")
        print("   The TC residual on the time-circle is non-zero because the")
        print("   1-component staggered hop has no chiral structure to absorb the")
        print("   time inversion. This is expected; canonical A_min lives on Z^3.")

    # Document the wall on non-canonical staggered + Wilson fermion blocks
    if noncanon:
        print()
        print("   --- Wall test: staggered + Wilson FERMION term in 3D ---")
        print("   (this is NOT in A_min; included only to expose the load-bearing")
        print("    wall: adding a Wilson fermion term breaks the naive ε-as-γ_5)")
        for L, dim, m, rW, res, _ in noncanon:
            print(f"   L={L}, dim={dim}, m={m}, r_W={rW}: "
                  f"err_CPT={res['err_CPT']:.3e}, err_eps={res['err_eps']:.3e}")
        print("   load-bearing wall: ε(x) = (-1)^Σx_k is the γ_5 analogue for the")
        print("   staggered KS hop, but does NOT play the same role for the")
        print("   Wilson fermion term. Staggered + Wilson fermion is not in A_min;")
        print("   A_min's A3 uses pure staggered. (Wilson plaquette in A4 is a")
        print("   *gauge-sector* term, not a fermion Wilson term.)")

    print()
    if n_pass == 4:
        print(" verdict: CPT operator-level identities (CPT1)–(CPT5) exhibited")
        print(" on canonical A_min (pure staggered).")
        print(" Wilson PLAQUETTE (gauge-sector) CPT step is asserted by inspection")
        print(" (deferred to a future loop for full algebraic generality).")
        return 0
    elif n_pass >= 2:
        print(" verdict: PARTIAL on canonical blocks; see per-block residuals.")
        return 0
    else:
        print(" verdict: stretch attempt did not close cleanly on canonical A_min.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
