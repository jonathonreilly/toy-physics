"""
Cl(3) -> KS symmetric 2x2 torus computation, version 2.

Approach: NO gauge fixing. Use 8 SU(3) link variables on the torus.
Basis: products of GAUGE-INVARIANT Wilson loop characters chi_lambda(W)
where W is a closed path on the 2x2 torus lattice.

Geometry: 2x2 spatial torus (Z^2 with PBC). 4 sites, 8 links, 4 plaquettes.
Each link is shared by EXACTLY 2 plaquettes.

The Wilson loop basis consists of:
  (1) trivial constant 1
  (2) chi_lambda(P_p) for each of 4 plaquettes p, each lambda
  (3) chi_lambda(W_x) and chi_lambda(W_y) for non-contractible loops
  (4) products of plaquette characters (multi-loop states)

The Casimir is k * C_2(lambda) for each Wilson loop with k links.
This treats all plaquettes SYMMETRICALLY (each has k=4).

The magnetic operator H_M = -(1/(g^2 N_c)) sum_p Re Tr U_p is computed
numerically at Monte Carlo samples; matrix elements via Haar^8 average.
"""

from __future__ import annotations

import sys
import time
import re
import numpy as np
from numpy.linalg import eigh

from cl3_ks_single_plaquette_2026_05_07 import casimir, dim_irrep
from cl3_ks_two_plaquette_2026_05_07 import sample_su3, chi_pq


def haar_sample_8links(N: int, seed: int = 42):
    """Generate N samples of 8 independent SU(3) matrices.

    Convention: links are
      U_x_ij = link from (i,j) to (i+1 mod 2, j)
      U_y_ij = link from (i,j) to (i, j+1 mod 2)
    for i, j in {0, 1}.

    Returns dict: keys 'x_00', 'x_10', 'x_01', 'x_11', 'y_00', 'y_10', 'y_01', 'y_11'
    """
    keys = ['x_00', 'x_10', 'x_01', 'x_11', 'y_00', 'y_10', 'y_01', 'y_11']
    samples = {}
    for k, key in enumerate(keys):
        samples[key] = sample_su3(N, seed=seed + k)
    return samples


def matprod(*Us):
    """Sequential matrix product (along sample axis)."""
    out = Us[0]
    for U in Us[1:]:
        out = np.einsum('nij,njk->nik', out, U)
    return out


def matinv(U):
    """Inverse via Hermitian conjugate (for unitary)."""
    return np.conj(U.transpose(0, 2, 1))


def plaquette_holonomy(samples, i, j):
    """U_p(i,j) = U_x(i,j) U_y(i+1,j) U_x(i,j+1)^-1 U_y(i,j)^-1."""
    ip = (i + 1) % 2
    jp = (j + 1) % 2
    U1 = samples[f'x_{i}{j}']
    U2 = samples[f'y_{ip}{j}']
    U3_inv = matinv(samples[f'x_{i}{jp}'])
    U4_inv = matinv(samples[f'y_{i}{j}'])
    return matprod(U1, U2, U3_inv, U4_inv)


def all_4_plaquettes(samples):
    return [plaquette_holonomy(samples, i, j) for i in range(2) for j in range(2)]


def non_contractible_x(samples):
    """Non-contractible loop in x direction at row j: U_x(0,j) U_x(1,j).
    Returns list [j=0, j=1]."""
    out = []
    for j in [0, 1]:
        out.append(matprod(samples[f'x_0{j}'], samples[f'x_1{j}']))
    return out


def non_contractible_y(samples):
    """Non-contractible loop in y direction at col i: U_y(i,0) U_y(i,1)."""
    out = []
    for i in [0, 1]:
        out.append(matprod(samples[f'y_{i}0'], samples[f'y_{i}1']))
    return out


def re_trace_over_Nc(M, N_c=3):
    return np.trace(M, axis1=1, axis2=2).real / N_c


# -------------------------------------------------------------------
# Build basis (Wilson-loop characters)
# -------------------------------------------------------------------

# Each basis element is labeled by a tuple of (loop_id, irrep) -> represents
# product of chi_lambda(W). Single-element tuples = single Wilson loop;
# multi-element tuples = product (chi_a(W1) chi_b(W2)...).
#
# Loop IDs:
#   'P00', 'P10', 'P01', 'P11' = 4 plaquettes (k=4 links each)
#   'X0', 'X1' = non-contractible x-loops at row j=0,1 (k=2)
#   'Y0', 'Y1' = non-contractible y-loops at col i=0,1 (k=2)

LOOP_LINKS = {
    'P00': 4, 'P10': 4, 'P01': 4, 'P11': 4,
    'X0': 2, 'X1': 2, 'Y0': 2, 'Y1': 2,
}

LOOP_LINK_SETS = {
    'P00': frozenset(['x_00', 'y_10', 'x_01', 'y_00']),
    'P10': frozenset(['x_10', 'y_00', 'x_11', 'y_10']),
    'P01': frozenset(['x_01', 'y_11', 'x_00', 'y_01']),
    'P11': frozenset(['x_11', 'y_01', 'x_10', 'y_11']),
    'X0': frozenset(['x_00', 'x_10']),
    'X1': frozenset(['x_01', 'x_11']),
    'Y0': frozenset(['y_00', 'y_01']),
    'Y1': frozenset(['y_10', 'y_11']),
}


def build_loop_holonomies(samples):
    """Build all loop holonomies in a dict."""
    out = {}
    out['P00'] = plaquette_holonomy(samples, 0, 0)
    out['P10'] = plaquette_holonomy(samples, 1, 0)
    out['P01'] = plaquette_holonomy(samples, 0, 1)
    out['P11'] = plaquette_holonomy(samples, 1, 1)
    out['X0'] = matprod(samples['x_00'], samples['x_10'])
    out['X1'] = matprod(samples['x_01'], samples['x_11'])
    out['Y0'] = matprod(samples['y_00'], samples['y_01'])
    out['Y1'] = matprod(samples['y_10'], samples['y_11'])
    return out


def build_basis(samples, irrep_set,
                include_plaquettes=True,
                include_noncontractible=False,
                include_double_plaquettes=True,
                include_triple_plaquettes=False):
    """
    Build basis of Wilson-loop characters and products.

    Returns: F (n_basis x N_samples), labels list.
    Each label is a tuple of ((loop_id, irrep), ...) factors.
    """
    holos = build_loop_holonomies(samples)
    N = next(iter(holos.values())).shape[0]

    F_list = [np.ones(N, dtype=complex)]
    labels = [()]  # empty product = trivial

    # Single Wilson loops
    if include_plaquettes:
        for loop_id in ['P00', 'P10', 'P01', 'P11']:
            for lam in irrep_set:
                if lam == (0, 0):
                    continue
                F_list.append(chi_pq(holos[loop_id], *lam))
                labels.append(((loop_id, lam),))

    if include_noncontractible:
        for loop_id in ['X0', 'X1', 'Y0', 'Y1']:
            for lam in irrep_set:
                if lam == (0, 0):
                    continue
                F_list.append(chi_pq(holos[loop_id], *lam))
                labels.append(((loop_id, lam),))

    # Double plaquette products
    if include_double_plaquettes:
        plaq_ids = ['P00', 'P10', 'P01', 'P11']
        # Limit irreps for double products to keep basis size manageable
        low_irreps = [lam for lam in irrep_set if lam in [(1, 0), (0, 1)]]
        for i in range(4):
            for j in range(i, 4):  # i <= j (avoid duplicates if irreps same)
                p_i = plaq_ids[i]
                p_j = plaq_ids[j]
                for lam_i in low_irreps:
                    for lam_j in low_irreps:
                        if i == j and (p_j, lam_j) < (p_i, lam_i):
                            continue
                        if i == j and (lam_i == lam_j):
                            # chi^2 — keep as separate basis element
                            pass
                        F_list.append(
                            chi_pq(holos[p_i], *lam_i) * chi_pq(holos[p_j], *lam_j)
                        )
                        labels.append(((p_i, lam_i), (p_j, lam_j)))

    # Triple plaquette products (optional, basis grows fast)
    if include_triple_plaquettes:
        plaq_ids = ['P00', 'P10', 'P01', 'P11']
        low_irreps = [(1, 0), (0, 1)]
        for i in range(4):
            for j in range(i + 1, 4):
                for k in range(j + 1, 4):
                    for lam_i in low_irreps:
                        for lam_j in low_irreps:
                            for lam_k in low_irreps:
                                F_list.append(
                                    chi_pq(holos[plaq_ids[i]], *lam_i) *
                                    chi_pq(holos[plaq_ids[j]], *lam_j) *
                                    chi_pq(holos[plaq_ids[k]], *lam_k)
                                )
                                labels.append((
                                    (plaq_ids[i], lam_i),
                                    (plaq_ids[j], lam_j),
                                    (plaq_ids[k], lam_k),
                                ))

    return np.array(F_list), labels, holos


def casimir_diag_value(label):
    """
    Casimir matrix-element diagonal value for basis element labeled by
    a tuple of ((loop_id, irrep), ...).

    For SUM of single-link Casimir over all 8 links acting on
    chi_lambda(W) where W has k links: the operator gives k * C_2(lambda).

    For PRODUCT chi_a(W_1) chi_b(W_2): Casimir on each link e gives:
      sum_{e in W_1 only} C_2(a) * F_factor
      + sum_{e in W_2 only} C_2(b) * F_factor
      + sum_{e in W_1 and W_2} ??? -- depends on tensor product

    For the simple case where W_1 and W_2 are disjoint:
      Casimir = |W_1| C_2(a) + |W_2| C_2(b)

    For shared edges, Casimir on shared link sees irrep a (x) b. The
    tensor product decomposes into irreps c with multiplicities. For
    each c, C_2(c) is the Casimir eigenvalue. For an UPPER BOUND we use:
      Casimir on shared link <= max C_2(c in a x b) -- usually a + b.
    For SU(3): C_2((1,0) x (1,0)) decomposes as (2,0) + (0,1), with
      C_2(2,0) = 10/3, C_2(0,1) = 4/3
      and C_2(a) + C_2(b) = 4/3 + 4/3 = 8/3
      So adding C_2(a) + C_2(b) is between max and min of components.

    For a CONSERVATIVE variational treatment (giving an upper bound on
    the energy gap and hence a LOWER bound on <P>_GS in the magnetic
    sector), use C_2(a) + C_2(b) on shared edges. But this changes the
    answer slightly. The cleanest approach: use C_2(a) + C_2(b) on
    shared edges as an APPROXIMATION; report the tensor-product analysis
    separately.

    Implementation: for each link e (8 total), figure out which
    representations are passing through it from the loops in this
    label. Sum C_2(rep) for each rep per link.
    """
    # Build mapping: link -> list of (irreps passing through it)
    # For a chi_lambda(W) factor: each link in W carries irrep lambda
    if len(label) == 0:
        return 0.0

    link_irreps = {}  # link_id -> list of (p,q)
    for (loop_id, lam) in label:
        for link_id in LOOP_LINK_SETS[loop_id]:
            link_irreps.setdefault(link_id, []).append(lam)

    # Total Casimir = sum_link sum_irrep C_2(irrep)
    total = 0.0
    for link_id, irreps_list in link_irreps.items():
        # When multiple irreps pass through, the simple-additive
        # approximation gives sum of individual Casimirs
        for (p, q) in irreps_list:
            total += casimir(p, q)
    return total


def build_hamiltonian_2x2_torus_v2(g_squared, samples, F, labels, holos, N_c=3):
    """Build H, Gram in the basis."""
    n = F.shape[0]
    N_samples = F.shape[1]

    # Magnetic operator at samples
    plaqs = [holos['P00'], holos['P10'], holos['P01'], holos['P11']]
    re_tr_p = sum(re_trace_over_Nc(p) for p in plaqs)
    M_values = -(1.0 / g_squared) * re_tr_p
    # See docstring: H_mag/N_c factor handled via re_trace_over_Nc which
    # divides by N_c. So M_values = -(1/g^2) * sum_p (1/N_c) Re Tr U_p
    # = -(1/(g^2 N_c)) sum_p Re Tr U_p  ✓

    # Gram matrix
    Gram = (np.conj(F) @ F.T) / N_samples

    # Magnetic matrix
    H_mag = (np.conj(F) * M_values[np.newaxis, :]) @ F.T / N_samples

    # Casimir matrix (diagonal in label basis if labels are linearly
    # independent and basis elements are eigenstates of sum_e Chat)
    H_cas = np.zeros((n, n), dtype=complex)
    for i, label in enumerate(labels):
        cas_val = casimir_diag_value(label)
        H_cas[i, i] = (g_squared / 2.0) * cas_val

    H = H_cas + H_mag
    H = 0.5 * (H + np.conj(H.T))
    Gram = 0.5 * (Gram + np.conj(Gram.T))
    return H, Gram


def diagonalize_with_gram(H, Gram, tol=1e-7):
    Gram = 0.5 * (Gram + np.conj(Gram.T))
    g_evals, g_evecs = eigh(Gram)
    keep_mask = g_evals > tol * max(g_evals[-1], 1e-12)
    n_keep = int(np.sum(keep_mask))
    g_inv_sqrt = np.zeros_like(g_evals)
    g_inv_sqrt[keep_mask] = 1.0 / np.sqrt(g_evals[keep_mask])
    P_proj = g_evecs[:, keep_mask] * g_inv_sqrt[keep_mask][np.newaxis, :]
    H_orth = np.conj(P_proj.T) @ H @ P_proj
    H_orth = 0.5 * (H_orth + np.conj(H_orth.T))
    evals, evecs_orth = eigh(H_orth)
    evecs = P_proj @ evecs_orth
    return evals, evecs, n_keep


def expectation_P(psi, F, holos, N_c=3):
    """<P>_avg over the 4 plaquettes."""
    plaqs = [holos['P00'], holos['P10'], holos['P01'], holos['P11']]
    P_vals = sum(re_trace_over_Nc(p) for p in plaqs) / 4.0
    psi_at = np.conj(psi) @ F
    norm = np.mean(np.abs(psi_at) ** 2)
    return float(np.mean(np.abs(psi_at) ** 2 * P_vals) / norm)


def expectation_P_indiv(psi, F, holos):
    plaqs = [holos['P00'], holos['P10'], holos['P01'], holos['P11']]
    psi_at = np.conj(psi) @ F
    norm = np.mean(np.abs(psi_at) ** 2)
    return [float(np.mean(np.abs(psi_at) ** 2 * re_trace_over_Nc(p)) / norm)
             for p in plaqs]


def run_one_g(g_squared, irrep_set, N_samples, seed=11,
               include_double_plaquettes=True,
               include_noncontractible=False,
               include_triple_plaquettes=False,
               verbose=True):
    if verbose:
        print(f"\n--- 2x2 torus (8-link, no gauge fix), g^2 = {g_squared} "
              f"N_samples = {N_samples} ---")
    t0 = time.time()
    samples = haar_sample_8links(N_samples, seed=seed)
    F, labels, holos = build_basis(
        samples, irrep_set,
        include_plaquettes=True,
        include_noncontractible=include_noncontractible,
        include_double_plaquettes=include_double_plaquettes,
        include_triple_plaquettes=include_triple_plaquettes,
    )
    if verbose:
        print(f"  Basis size: {F.shape[0]}")
        print(f"  Sample+basis: {time.time()-t0:.1f}s")

    t1 = time.time()
    H, Gram = build_hamiltonian_2x2_torus_v2(g_squared, samples, F, labels, holos)
    if verbose:
        print(f"  H+Gram: {time.time()-t1:.1f}s")

    t2 = time.time()
    evals, evecs, n_keep = diagonalize_with_gram(H, Gram)
    if verbose:
        print(f"  Diag: {time.time()-t2:.1f}s")

    psi0 = evecs[:, 0]
    P_avg = expectation_P(psi0, F, holos)
    P_indiv = expectation_P_indiv(psi0, F, holos)

    if verbose:
        print(f"  E_0 = {evals[0].real:.6f}  (kept {n_keep}/{F.shape[0]})")
        print(f"  <P>_avg = {P_avg:.6f}")
        print(f"  Plaq: P00={P_indiv[0]:.4f}, P10={P_indiv[1]:.4f}, "
              f"P01={P_indiv[2]:.4f}, P11={P_indiv[3]:.4f}")
        # Top components
        abs_psi = np.abs(psi0)
        top = np.argsort(-abs_psi)[:6]
        print(f"  Top 6 components:")
        for idx in top:
            if idx < len(labels):
                lbl = str(labels[idx]) if labels[idx] else '1'
                print(f"    {lbl[:55]:<55} {psi0[idx].real:>+.4f}")

    return {
        'g_squared': g_squared,
        'P_avg': P_avg,
        'P_indiv': P_indiv,
        'E_0': evals[0].real,
        'n_basis': F.shape[0],
        'n_kept': n_keep,
    }


def coupling_sweep(irrep_set, N_samples=20000, seed=11,
                    **basis_kwargs):
    print("\n=== Coupling sweep, 2x2 torus 8-link (no gauge fix) ===")
    print(f"  Irrep set: {irrep_set}, N_samples: {N_samples}")
    print()
    rows = []
    for g2 in [0.5, 0.75, 1.0, 1.5, 2.0]:
        r = run_one_g(g2, irrep_set, N_samples, seed,
                       verbose=True, **basis_kwargs)
        rows.append(r)

    print()
    print("=" * 70)
    print(f"Summary (N_samples={N_samples}, basis options: {basis_kwargs}):")
    print("=" * 70)
    print(f"{'g^2':>6}  {'<P>_avg':>10}  {'plaq dispersion':>22}")
    for r in rows:
        std = float(np.std(r['P_indiv']))
        mean = float(np.mean(r['P_indiv']))
        print(f"{r['g_squared']:>6.2f}  {r['P_avg']:>10.6f}  "
              f"{mean:.4f} +- {std:.4f}")
    return rows


def basis_convergence(g_squared=1.0, N_samples=20000, seed=11):
    print("\n=== Basis convergence at g^2 = 1.0 ===")
    print()
    rows = []
    test_cases = [
        # (irrep_set, options dict, label)
        ([(0, 0), (1, 0), (0, 1)], dict(), '3 irreps, plaq-only'),
        ([(0, 0), (1, 0), (0, 1)], dict(include_double_plaquettes=True),
         '3 irreps + double-plaq'),
        ([(0, 0), (1, 0), (0, 1), (1, 1)], dict(include_double_plaquettes=True),
         '4 irreps + double-plaq'),
        ([(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)],
         dict(include_double_plaquettes=True), '6 irreps + double-plaq'),
        ([(0, 0), (1, 0), (0, 1), (1, 1)],
         dict(include_double_plaquettes=True, include_triple_plaquettes=True),
         '4 irreps + double + triple'),
    ]
    for irreps, opts, lbl in test_cases:
        print(f"\n--- {lbl} ---")
        r = run_one_g(g_squared, irreps, N_samples, seed,
                       verbose=True, **opts)
        rows.append({**r, 'label': lbl})

    print()
    print("=" * 70)
    print("Basis convergence summary:")
    print("=" * 70)
    print(f"{'config':<35} {'#basis':>7} {'E_0':>10} {'<P>_avg':>10}")
    for r in rows:
        print(f"{r['label']:<35} {r['n_basis']:>7}  "
              f"{r['E_0']:>10.6f}  {r['P_avg']:>10.6f}")


def sample_convergence(irrep_set, **basis_kwargs):
    print("\n=== Sample convergence at g^2 = 1.0 ===")
    rows = []
    for N in [5000, 10000, 20000, 50000, 100000]:
        for seed in [11, 22, 33]:
            r = run_one_g(1.0, irrep_set, N, seed=seed, verbose=False,
                           **basis_kwargs)
            rows.append({'N': N, 'seed': seed, **r})

    print(f"\n{'N':>8}  {'seed':>5}  {'<P>_avg':>10}  {'E_0':>12}")
    for r in rows:
        print(f"{r['N']:>8}  {r['seed']:>5}  {r['P_avg']:>10.6f}  "
              f"{r['E_0']:>12.6f}")

    print()
    print(f"{'N':>8}  {'mean<P>':>10}  {'stdev':>10}")
    Ns = sorted(set(r['N'] for r in rows))
    for N in Ns:
        Ps = [r['P_avg'] for r in rows if r['N'] == N]
        mean = float(np.mean(Ps))
        std = float(np.std(Ps, ddof=1)) if len(Ps) > 1 else 0.0
        print(f"{N:>8}  {mean:>10.6f}  {std:>10.6f}")


if __name__ == "__main__":
    print("=" * 70)
    print("Cl(3) -> KS, 2x2 spatial torus, no gauge fix, 8 SU(3) link vars")
    print("=" * 70)

    # [1] Basis convergence
    print("\n[1] Basis convergence")
    basis_convergence(g_squared=1.0, N_samples=20000, seed=11)

    # [2] Sample convergence
    print("\n[2] Sample convergence")
    sample_convergence(irrep_set=[(0, 0), (1, 0), (0, 1), (1, 1)],
                        include_double_plaquettes=True)

    # [3] Coupling sweep at converged setup
    print("\n[3] Coupling sweep")
    coupling_sweep(irrep_set=[(0, 0), (1, 0), (0, 1), (1, 1)],
                    N_samples=50000, seed=11,
                    include_double_plaquettes=True)

    print()
    print("=" * 70)
    print("Reference values for comparison:")
    print("  KS Hamilton limit (literature) at g^2~1:    ~0.55-0.60")
    print("  Wilson 4D MC at beta=6:                       0.5934")
    print("  Single-plaquette toy at g^2=1:                0.218")
    print("  Dumbbell (asymmetric, basis-limited):         0.152")
    print("  Strong-coupling LO at g^2=1:                  0.0417")
    print("  Mean-field K=4 (3D cubic):                    0.589")
    print("=" * 70)
