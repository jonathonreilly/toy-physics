"""
Cl(3) -> KS, 2x2 spatial torus, spin-network ED v3.

UPGRADE: products of HIGH-IRREP plaquette characters.

The previous basis was limited because:
  - Pair products only used LOW irreps (1,0), (0,1), (1,1)
  - High-irrep characters were only single, never multiplied

The weak-coupling vacuum needs <Pi_p delta(U_p - I)> structure, which in
character form is Pi_p [Sum_lambda d_lambda chi_lambda(U_p)]. To represent
this, we need PRODUCTS of HIGH-IRREP characters across ALL plaquettes.

Specifically, this v3 includes:
  - Products chi_lambda_1(P_00) chi_lambda_2(P_10) chi_lambda_3(P_01) chi_lambda_4(P_11)
    for ALL irreps up to a Casimir cutoff
  - This gives a Tensor product of plaquette character sub-spaces.
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
# Build basis: products of plaquette characters in arbitrary irreps
# -------------------------------------------------------------------

def build_basis_v3(samples, irrep_set, max_total_casimir=None,
                    include_nc_loops=True, include_pairs_nc=False):
    """
    Build basis of products of plaquette characters in any irreps,
    with constraint that total Casimir is bounded.

    For 4 plaquettes, basis element is:
        F_{l1, l2, l3, l4}(U) = chi_l1(P_00) chi_l2(P_10) chi_l3(P_01) chi_l4(P_11)
    where each l_i is an irrep in irrep_set.

    Total Casimir per state (estimate): sum over edges of C_2(rep on each link).
    Each plaquette uses 4 edges, but plaquettes overlap. In the worst case
    where no overlap: total C_2 = 4 * C_2(rep) per plaquette.

    To control basis size, only include states where sum of Casimirs of the
    plaquette irreps is bounded.

    Returns: F (n_basis, N), labels.
    """
    holos = loop_matrices(samples)
    N = next(iter(holos.values())).shape[0]

    plaq_ids = ['P00', 'P10', 'P01', 'P11']
    nc_ids = ['X0', 'X1', 'Y0', 'Y1']

    # Pre-compute character values for each plaquette and each irrep
    # plaq_chars[plaq_id][lam] = (N,) array
    plaq_chars = {}
    for W in plaq_ids:
        plaq_chars[W] = {}
        for lam in irrep_set:
            plaq_chars[W][lam] = chi_pq(holos[W], *lam)

    F_list = []
    labels = []

    # Tensor product: chi_l1(P_00) chi_l2(P_10) chi_l3(P_01) chi_l4(P_11)
    # For each combination of irreps (l1, l2, l3, l4)
    for l1 in irrep_set:
        for l2 in irrep_set:
            for l3 in irrep_set:
                for l4 in irrep_set:
                    if max_total_casimir is not None:
                        total_c = (casimir(*l1) + casimir(*l2)
                                    + casimir(*l3) + casimir(*l4))
                        if total_c > max_total_casimir:
                            continue
                    f = (plaq_chars['P00'][l1]
                         * plaq_chars['P10'][l2]
                         * plaq_chars['P01'][l3]
                         * plaq_chars['P11'][l4])
                    F_list.append(f)
                    labels.append({'kind': 'plaq_quad',
                                     'l1': l1, 'l2': l2, 'l3': l3, 'l4': l4})

    # Add non-contractible loop characters and their products
    if include_nc_loops:
        nc_chars = {}
        for W in nc_ids:
            nc_chars[W] = {}
            for lam in irrep_set:
                if lam == (0, 0):
                    continue
                nc_chars[W][lam] = chi_pq(holos[W], *lam)
                F_list.append(nc_chars[W][lam])
                labels.append({'kind': 'nc_single', 'loop': W, 'irrep': lam})

        # Also chi_lam(plaquette) * chi_mu(nc loop) products
        if include_pairs_nc:
            low_irreps = [lam for lam in irrep_set if lam in [(1, 0), (0, 1)]]
            for plaq_id in plaq_ids:
                for nc_id in nc_ids:
                    for lam_p in low_irreps:
                        for lam_nc in low_irreps:
                            F_list.append(plaq_chars[plaq_id][lam_p]
                                            * nc_chars[nc_id][lam_nc])
                            labels.append({'kind': 'plaq_nc_pair',
                                             'plaq': (plaq_id, lam_p),
                                             'nc': (nc_id, lam_nc)})

    F = np.array(F_list)
    return F, labels, holos


def build_H_v3(g_squared, samples, irrep_set, max_total_casimir,
                include_nc_loops, include_pairs_nc, eps=1e-2,
                verbose=True, N_c=3):
    F, labels, holos = build_basis_v3(
        samples, irrep_set,
        max_total_casimir=max_total_casimir,
        include_nc_loops=include_nc_loops,
        include_pairs_nc=include_pairs_nc,
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
            F_p, _, _ = build_basis_v3(
                samples_p, irrep_set,
                max_total_casimir=max_total_casimir,
                include_nc_loops=include_nc_loops,
                include_pairs_nc=include_pairs_nc,
            )
            F_m, _, _ = build_basis_v3(
                samples_m, irrep_set,
                max_total_casimir=max_total_casimir,
                include_nc_loops=include_nc_loops,
                include_pairs_nc=include_pairs_nc,
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


def run_one(g_squared, irrep_set, max_total_casimir,
             N_samples=10000, seed=11,
             include_nc_loops=True, include_pairs_nc=False,
             eps=1e-2, verbose=True):
    if verbose:
        print(f"\n--- 2x2 torus v3 spin-network, g^2 = {g_squared} ---")
        print(f"  irreps: {irrep_set}")
        print(f"  max_total_casimir: {max_total_casimir}")
        print(f"  include_nc_loops: {include_nc_loops}, "
              f"include_pairs_nc: {include_pairs_nc}")
    t0 = time.time()
    samples = haar_sample_8links(N_samples, seed=seed)
    H, Gram, F, labels, holos = build_H_v3(
        g_squared, samples, irrep_set,
        max_total_casimir=max_total_casimir,
        include_nc_loops=include_nc_loops,
        include_pairs_nc=include_pairs_nc,
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
    print("Cl(3) -> KS, 2x2 spatial torus, spin-network ED v3")
    print("(plaquette-quad character products with HIGH irreps)")
    print("=" * 70)

    # Step 1: Test trivial case (only (0,0)+(1,0)+(0,1) on each plaq)
    print("\n[1] 3 irreps per plaq, max_total_casimir = 4 (low cutoff)")
    irrep_3 = [(0, 0), (1, 0), (0, 1)]
    r1 = run_one(1.0, irrep_3, max_total_casimir=4.0,
                  N_samples=10000, seed=11, include_nc_loops=True,
                  include_pairs_nc=False, eps=1e-2, verbose=True)

    print("\n[2] 3 irreps, max_total_casimir = 8 (higher mixing)")
    r2 = run_one(1.0, irrep_3, max_total_casimir=8.0,
                  N_samples=10000, seed=11, include_nc_loops=True,
                  include_pairs_nc=False, eps=1e-2, verbose=True)

    # Add (1,1)
    print("\n[3] 4 irreps + max_total_casimir = 8")
    irrep_4 = [(0, 0), (1, 0), (0, 1), (1, 1)]
    r3 = run_one(1.0, irrep_4, max_total_casimir=8.0,
                  N_samples=10000, seed=11, include_nc_loops=True,
                  include_pairs_nc=False, eps=1e-2, verbose=True)

    # Add (2,0), (0,2)
    print("\n[4] 6 irreps, max_total_casimir = 8")
    irrep_6 = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]
    r4 = run_one(1.0, irrep_6, max_total_casimir=8.0,
                  N_samples=10000, seed=11, include_nc_loops=True,
                  include_pairs_nc=False, eps=1e-2, verbose=True)

    print("\n=== Summary at g^2 = 1.0 ===")
    print(f"3 irreps,     C_tot<=4:    <P> = {r1['P_avg']:.4f}, n_basis = {r1['n_basis']}")
    print(f"3 irreps,     C_tot<=8:    <P> = {r2['P_avg']:.4f}, n_basis = {r2['n_basis']}")
    print(f"4 irreps (+ad), C_tot<=8:  <P> = {r3['P_avg']:.4f}, n_basis = {r3['n_basis']}")
    print(f"6 irreps (+sym), C_tot<=8: <P> = {r4['P_avg']:.4f}, n_basis = {r4['n_basis']}")
    print(f"\nReference targets:")
    print(f"  Wilson 4D MC at beta=6, 2x2x2x16:    0.6243 (spatial, finite-N_t)")
    print(f"  Wilson 4D MC at beta=6, 4x4x4x4:     0.5974 (spatial)")
    print(f"  KS literature (3D thermo limit):     ~0.55-0.60")
