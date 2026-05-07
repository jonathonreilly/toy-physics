"""
Cl(3) -> KS, 2x2 spatial torus, spin-network ED v4.

KEY INSIGHT: characters-of-Wilson-loops basis converges SLOWLY for
weak-coupling vacuum. The weak-coupling Gaussian Ψ_WC(U) ~ exp(-α S(U))
has an infinite tower of irrep contributions.

INSTEAD: use 'magnetic coherent states' = exp(-alpha S_mag(U)) for various
alpha values, including character products to capture deeper Hilbert space.

Basis:
  - g_alpha(U) = exp(alpha * sum_p Re Tr(U_p)/N_c) for alpha in [0, alpha_max]
    These are magnetic coherent states peaking at U_p = I.
    They form a complete basis as alpha sweeps continuously.
  - Plus character products from v3 (orthogonal complement).

The Hamiltonian acts on g_alpha straightforwardly:
  - Magnetic: M g_alpha = -(1/(g^2 N_c)) Sum_p Re Tr U_p * g_alpha [diagonal in g_alpha]
  - Casimir: numerical via finite-difference (already validated)

Variational subspace: span{g_alpha for alpha in {0, 0.5, 1, 2, 5, 10, 20}}.
Diagonalize H in this 7-dim subspace + low-irrep characters.
"""

from __future__ import annotations

import time
import numpy as np
from numpy.linalg import eigh

from cl3_ks_single_plaquette_2026_05_07 import casimir, dim_irrep
from cl3_ks_two_plaquette_2026_05_07 import sample_su3, chi_pq
from cl3_ks_spinnetwork_2x2_2026_05_07 import (
    LINK_KEYS, gell_mann_generators, perturbed_links,
    diagonalize_with_gram, haar_sample_8links,
)
from cl3_ks_spinnetwork_2x2_v2_2026_05_07 import loop_matrices


def matprod(*Us):
    out = Us[0]
    for U in Us[1:]:
        out = np.einsum('nij,njk->nik', out, U)
    return out


def matinv(U):
    return np.conj(U.transpose(0, 2, 1))


def re_trace_over_Nc(M, N_c=3):
    return np.trace(M, axis1=1, axis2=2).real / N_c


# -------------------------------------------------------------------
# Magnetic coherent states + characters basis
# -------------------------------------------------------------------

def total_re_tr_plaq(holos, N_c=3):
    """sum over 4 plaquettes of Re Tr U_p / N_c."""
    plaqs = [holos[f'P{i}{j}'] for i in [0, 1] for j in [0, 1]]
    return sum(re_trace_over_Nc(p, N_c) for p in plaqs)


def build_basis_v4(samples, alphas, irrep_set,
                    include_chi_products=True,
                    include_pair_chars=False,
                    N_c=3):
    """
    Build basis: magnetic coherent states + low-irrep characters.

    g_alpha(U) = exp(alpha * S_mag(U))  where S_mag = sum_p Re Tr U_p / N_c.

    Plus product characters chi_lam(P_p) for each plaquette and irrep.
    """
    holos = loop_matrices(samples)
    N = next(iter(holos.values())).shape[0]
    F_list = []
    labels = []

    # Magnetic coherent states
    S_mag = total_re_tr_plaq(holos, N_c)  # (N,)
    for alpha in alphas:
        g_a = np.exp(alpha * S_mag).astype(complex)
        F_list.append(g_a)
        labels.append({'kind': 'coh', 'alpha': alpha})

    # Plus characters per plaquette (not products, just singles)
    if include_chi_products:
        plaq_ids = ['P00', 'P10', 'P01', 'P11']
        for W in plaq_ids:
            for lam in irrep_set:
                if lam == (0, 0):
                    continue
                F_list.append(chi_pq(holos[W], *lam))
                labels.append({'kind': 'chi', 'loop': W, 'irrep': lam})

        # Non-contractible singles
        nc_ids = ['X0', 'X1', 'Y0', 'Y1']
        for W in nc_ids:
            for lam in irrep_set:
                if lam == (0, 0):
                    continue
                F_list.append(chi_pq(holos[W], *lam))
                labels.append({'kind': 'chi_nc', 'loop': W, 'irrep': lam})

        # Coherent state * single character (mixing)
        for alpha in alphas:
            if alpha == 0:
                continue
            g_a = np.exp(alpha * S_mag)
            for W in plaq_ids:
                for lam in irrep_set:
                    if lam == (0, 0):
                        continue
                    F_list.append(g_a * chi_pq(holos[W], *lam))
                    labels.append({'kind': 'coh_chi', 'alpha': alpha,
                                     'loop': W, 'irrep': lam})

        # Pair characters (cross-plaquette)
        if include_pair_chars:
            low_irreps = [lam for lam in irrep_set
                           if lam in [(1, 0), (0, 1), (1, 1)]]
            plaq_ids_full = plaq_ids
            for ia, W1 in enumerate(plaq_ids_full):
                for ib, W2 in enumerate(plaq_ids_full):
                    if ib <= ia:
                        continue
                    for lam1 in low_irreps:
                        for lam2 in low_irreps:
                            F_list.append(
                                chi_pq(holos[W1], *lam1)
                                * chi_pq(holos[W2], *lam2)
                            )
                            labels.append({'kind': 'pair_chi',
                                             'l1': (W1, lam1),
                                             'l2': (W2, lam2)})

    F = np.array(F_list)
    return F, labels, holos


def build_H_v4(g_squared, samples, alphas, irrep_set,
                include_chi_products, include_pair_chars,
                eps=1e-2, verbose=True, N_c=3):
    F, labels, holos = build_basis_v4(
        samples, alphas, irrep_set,
        include_chi_products=include_chi_products,
        include_pair_chars=include_pair_chars,
    )
    n_basis, N = F.shape
    if verbose:
        print(f"  Basis size: {n_basis}, samples: {N}")

    Gram = (np.conj(F) @ F.T) / N

    plaqs = [holos[f'P{i}{j}'] for i in [0, 1] for j in [0, 1]]
    M_values = -(1.0 / g_squared) * sum(re_trace_over_Nc(p, N_c) for p in plaqs)
    H_mag = (np.conj(F) * M_values[np.newaxis, :]) @ F.T / N

    T_list = gell_mann_generators()
    H_C = np.zeros((n_basis, n_basis), dtype=complex)
    for k, link_key in enumerate(LINK_KEYS):
        if verbose:
            t0 = time.time()
        Chat_F = np.zeros((n_basis, N), dtype=complex)
        for T_a in T_list:
            samples_p = perturbed_links(samples, link_key, T_a, eps, +1)
            samples_m = perturbed_links(samples, link_key, T_a, eps, -1)
            F_p, _, _ = build_basis_v4(
                samples_p, alphas, irrep_set,
                include_chi_products=include_chi_products,
                include_pair_chars=include_pair_chars,
            )
            F_m, _, _ = build_basis_v4(
                samples_m, alphas, irrep_set,
                include_chi_products=include_chi_products,
                include_pair_chars=include_pair_chars,
            )
            Chat_F -= (F_p + F_m - 2.0 * F) / (eps ** 2)
        contrib = (np.conj(F) @ Chat_F.T) / N
        H_C += contrib
        if verbose:
            dt = time.time() - t0
            print(f"    link {link_key}: {dt:.1f}s")
    H_C *= (g_squared / 2.0)

    H = H_C + H_mag
    H = 0.5 * (H + np.conj(H.T))
    Gram = 0.5 * (Gram + np.conj(Gram.T))

    return H, Gram, F, labels, holos


def expectation_P(psi, F, holos, N_c=3):
    plaqs = [holos[f'P{i}{j}'] for i in [0, 1] for j in [0, 1]]
    P_vals = sum(re_trace_over_Nc(p) for p in plaqs) / 4.0
    psi_at = np.conj(psi) @ F
    norm = np.mean(np.abs(psi_at) ** 2)
    return float(np.mean(np.abs(psi_at) ** 2 * P_vals) / norm)


def run_one(g_squared, alphas, irrep_set,
             N_samples=10000, seed=11,
             include_chi_products=True,
             include_pair_chars=False,
             eps=1e-2, verbose=True):
    if verbose:
        print(f"\n--- 2x2 torus v4 (coherent + chars), g^2 = {g_squared} ---")
        print(f"  alphas: {alphas}")
        print(f"  irreps: {irrep_set}")
        print(f"  chi_products: {include_chi_products}, pair_chars: {include_pair_chars}")
    t0 = time.time()
    samples = haar_sample_8links(N_samples, seed=seed)
    H, Gram, F, labels, holos = build_H_v4(
        g_squared, samples, alphas, irrep_set,
        include_chi_products=include_chi_products,
        include_pair_chars=include_pair_chars,
        eps=eps, verbose=verbose,
    )
    evals, evecs, n_keep = diagonalize_with_gram(H, Gram)

    psi0 = evecs[:, 0]
    P_avg = expectation_P(psi0, F, holos)

    if verbose:
        print(f"  E_0 = {evals[0].real:.6f}  (kept {n_keep}/{F.shape[0]})")
        print(f"  <P>_avg = {P_avg:.6f}")
        # Top components
        abs_psi = np.abs(psi0)
        top = np.argsort(-abs_psi)[:5]
        for idx in top:
            lbl = labels[idx]
            print(f"  amp={psi0[idx].real:+.4f}: {lbl}")
        print(f"  Total time: {time.time()-t0:.1f}s")

    return {
        'g_squared': g_squared,
        'P_avg': P_avg,
        'E_0': evals[0].real,
        'n_basis': F.shape[0],
        'n_kept': n_keep,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("Cl(3) -> KS, 2x2 spatial torus, spin-network ED v4")
    print("(MAGNETIC COHERENT STATES + character products)")
    print("=" * 70)

    irrep_3 = [(0, 0), (1, 0), (0, 1)]

    # alpha_max convergence study
    print("\n[1] alpha_max convergence at g^2=1, 3 irreps + chi pairs")
    alpha_sets = [
        [0, 0.5, 1.0, 2.0],
        [0, 0.5, 1.0, 2.0, 5.0],
        [0, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0],
        [0, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 12.0],
        [0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 12.0, 16.0],
        [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0, 15.0, 20.0],
    ]
    rows_alpha = []
    for alphas in alpha_sets:
        r = run_one(1.0, alphas, irrep_3,
                     N_samples=20000, seed=11,
                     include_chi_products=True,
                     include_pair_chars=True, eps=1e-2,
                     verbose=False)
        rows_alpha.append((alphas, r))
        print(f"  alphas={alphas[-1]:.0f}_max ({len(alphas)} alphas): "
              f"<P>={r['P_avg']:.4f}, n_basis={r['n_basis']}, "
              f"n_kept={r['n_kept']}, E_0={r['E_0']:.4f}")

    # Multi-seed verification at best alphas
    print("\n[2] Multi-seed verification at best alpha set")
    best_alphas = alpha_sets[-2]  # 11 alphas up to 16
    print(f"  alphas: {best_alphas}")
    for seed in [11, 22, 33, 44, 55]:
        r = run_one(1.0, best_alphas, irrep_3,
                     N_samples=20000, seed=seed,
                     include_chi_products=True,
                     include_pair_chars=True, eps=1e-2,
                     verbose=False)
        print(f"  seed={seed}: <P> = {r['P_avg']:.4f}, n_kept = {r['n_kept']}")

    # Coupling sweep
    print("\n[3] Coupling sweep at best alpha set")
    for g2 in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0]:
        r = run_one(g2, best_alphas, irrep_3,
                     N_samples=20000, seed=11,
                     include_chi_products=True,
                     include_pair_chars=True, eps=1e-2,
                     verbose=False)
        print(f"  g^2={g2}: <P> = {r['P_avg']:.4f}, n_kept = {r['n_kept']}, "
              f"E_0 = {r['E_0']:.4f}")

    print("\n=== Reference targets ===")
    print(f"  Wilson 4D MC at beta=6, 2x2x2x16:    0.6243 (spatial)")
    print(f"  Wilson 4D MC at beta=6, 4x4x4x4:     0.5974 (spatial)")
    print(f"  KS literature (3D thermo limit):     ~0.55-0.60")
