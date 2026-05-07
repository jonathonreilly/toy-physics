"""
Cl(3) -> KS, 2x2 spatial torus, spin-network exact diagonalization
WITH OVERLAPPING-PLAQUETTE CORRELATIONS via NUMERICAL CASIMIR ACTION.

Strategy:
  - Build a rich gauge-invariant basis of Wilson-loop products on the 8-link
    2x2 torus, including overlapping plaquette products that the
    Casimir-diagonal v3 basis could not handle.
  - Compute the Casimir matrix elements NUMERICALLY by applying the
    link Lie-derivative via finite-difference perturbations of the
    Haar samples. This avoids needing analytic SU(3) Clebsch-Gordan
    or 6j symbols.
  - Compute the magnetic matrix elements numerically (already standard).
  - Solve the generalized eigenvalue problem H psi = E G psi.

Hamiltonian:
  H = (g^2/2) Sum_e Chat_e  -  (1/(g^2 N_c)) Sum_p Re Tr U_p

Casimir operator on link e via Lie-derivative (left-invariant):
  (Chat_e Psi)(U) = -Sum_a d^2/ds^2 Psi(... U_e exp(i s T_a) ...) at s=0

Implemented via finite difference:
  Chat_e Psi(U) ~ -Sum_a [Psi(U_e e^{i eps T_a}) + Psi(U_e e^{-i eps T_a})
                          - 2 Psi(U_e)] / eps^2
where T_a are the 8 Gell-Mann/2 generators.

Sanity check: Chat_e applied to chi_(1,0)(W_e) for a single Wilson loop
W_e through e should give (4/3) chi_(1,0)(W_e) since W_e is in the
fundamental rep and C_2(fund) = 4/3.

Output: <P>_KS at canonical g^2 = 1 for the 2x2 torus, with irrep cutoff
convergence study.
"""

from __future__ import annotations

import time
import numpy as np
from numpy.linalg import eigh
from scipy.linalg import expm

from cl3_ks_single_plaquette_2026_05_07 import casimir
from cl3_ks_two_plaquette_2026_05_07 import sample_su3, chi_pq


# -------------------------------------------------------------------
# SU(3) generators (Gell-Mann/2)
# -------------------------------------------------------------------

def gell_mann_generators():
    """Return list of 8 SU(3) Hermitian generators T_a = lambda_a / 2."""
    L = []
    # lambda_1
    L.append(np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex))
    # lambda_2
    L.append(np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex))
    # lambda_3
    L.append(np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex))
    # lambda_4
    L.append(np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex))
    # lambda_5
    L.append(np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex))
    # lambda_6
    L.append(np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex))
    # lambda_7
    L.append(np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex))
    # lambda_8
    L.append(np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex)
              / np.sqrt(3))
    return [0.5 * Lam for Lam in L]


def verify_gell_mann():
    """Verify Tr(T_a T_b) = (1/2) delta_ab and Sum_a T_a^2 = (4/3) I."""
    Ts = gell_mann_generators()
    # Trace orthonormality
    for a in range(8):
        for b in range(8):
            tr = np.trace(Ts[a] @ Ts[b])
            expected = 0.5 if a == b else 0.0
            assert np.isclose(tr.real, expected) and np.isclose(tr.imag, 0), \
                f"Tr(T{a} T{b}) = {tr}, expected {expected}"
    # Casimir: Sum T_a^2 = (4/3) I in fundamental
    cas = sum(T @ T for T in Ts)
    diag = np.diag(cas)
    assert np.allclose(diag, 4.0 / 3.0), f"Casimir diag = {diag}"
    assert np.allclose(cas - np.diag(np.diag(cas)), 0), "Casimir not diagonal"
    print(f"  Tr(T_a T_b) = (1/2) delta_ab verified")
    print(f"  Sum_a T_a^2 = (4/3) I verified (C_2(fund) = 4/3)")


# -------------------------------------------------------------------
# Wilson-loop holonomies on 2x2 torus
# -------------------------------------------------------------------

LINK_KEYS = ['x_00', 'x_10', 'x_01', 'x_11', 'y_00', 'y_10', 'y_01', 'y_11']


def matprod(*Us):
    out = Us[0]
    for U in Us[1:]:
        out = np.einsum('nij,njk->nik', out, U)
    return out


def matinv(U):
    return np.conj(U.transpose(0, 2, 1))


def re_trace_over_Nc(M, N_c=3):
    return np.trace(M, axis1=1, axis2=2).real / N_c


def haar_sample_8links(N: int, seed: int = 42):
    samples = {}
    for k, key in enumerate(LINK_KEYS):
        samples[key] = sample_su3(N, seed=seed + k)
    return samples


def perturbed_links(samples, link_key, T_a, eps, sign=+1):
    """Return new samples dict with link_key replaced by U_link @ exp(i eps sign T_a).

    Other links are unchanged (shared object refs).
    """
    new = dict(samples)
    U = samples[link_key]
    # exp(i eps sign T_a): same matrix for all samples, broadcast
    delta = expm(1j * eps * sign * T_a)
    new[link_key] = np.einsum('nij,jk->nik', U, delta)
    return new


# -------------------------------------------------------------------
# Wilson-loop holonomies on 2x2 torus (returns dict)
# -------------------------------------------------------------------

def loop_holonomies(samples):
    """Compute all relevant Wilson-loop holonomies."""
    holos = {}
    lengths = {}
    edge_sets = {}  # which links each loop traverses

    # 4 plaquettes (length 4 each)
    # P_ij = U_x(i,j) U_y(i+1,j) U_x(i,j+1)^-1 U_y(i,j)^-1
    for i in [0, 1]:
        for j in [0, 1]:
            ip = (i + 1) % 2
            jp = (j + 1) % 2
            U1 = samples[f'x_{i}{j}']
            U2 = samples[f'y_{ip}{j}']
            U3_inv = matinv(samples[f'x_{i}{jp}'])
            U4_inv = matinv(samples[f'y_{i}{j}'])
            holos[f'P{i}{j}'] = matprod(U1, U2, U3_inv, U4_inv)
            lengths[f'P{i}{j}'] = 4
            edge_sets[f'P{i}{j}'] = {f'x_{i}{j}', f'y_{ip}{j}',
                                     f'x_{i}{jp}', f'y_{i}{j}'}

    # 4 non-contractible loops
    for j in [0, 1]:
        holos[f'X{j}'] = matprod(samples[f'x_0{j}'], samples[f'x_1{j}'])
        lengths[f'X{j}'] = 2
        edge_sets[f'X{j}'] = {f'x_0{j}', f'x_1{j}'}
    for i in [0, 1]:
        holos[f'Y{i}'] = matprod(samples[f'y_{i}0'], samples[f'y_{i}1'])
        lengths[f'Y{i}'] = 2
        edge_sets[f'Y{i}'] = {f'y_{i}0', f'y_{i}1'}

    # 1x2 rectangular Wilson loops (length 6 each)
    # Two adjacent plaquettes joined: traverse perimeter of 1x2 rectangle.
    # On 2x2 PBC torus, the 1x2 rectangle is equivalent to traversing
    # the FULL torus boundary in one direction (then comes back through).
    # Most natural: combine plaquettes by symmetric difference of edges.
    # Skip for now to keep basis manageable.

    # Also 4 "sliding" length-4 loops: plaquette traversed in various ways.
    # Skip — already covered by P_ij and combinations.

    return holos, lengths, edge_sets


# -------------------------------------------------------------------
# Basis construction: gauge-invariant Wilson-loop products
# (including overlapping plaquette products)
# -------------------------------------------------------------------

def build_basis_products(holos, lengths, edge_sets, irrep_set,
                          include_pairs=False,
                          include_triples=False):
    """
    Build a basis of products of Wilson-loop characters.

    Each basis element is:
        Trivial: 1
        Single: chi_lambda(W) for each (W, lambda)
        Double: chi_lambda(W1) chi_mu(W2) for each pair (W1, W2) of distinct loops

    Includes overlapping pairs (this is the key advance over v3 basis).

    Returns:
        F: (n_basis, N) array of basis function values
        labels: list of dicts describing each basis element
    """
    N = next(iter(holos.values())).shape[0]
    F_list = [np.ones(N, dtype=complex)]
    labels = [{'loops': [], 'edges_in_loops': []}]

    plaq_ids = ['P00', 'P10', 'P01', 'P11']
    nc_ids = ['X0', 'X1', 'Y0', 'Y1']

    all_loop_ids = plaq_ids + nc_ids

    # Singles
    nontriv_irreps = [lam for lam in irrep_set if lam != (0, 0)]
    for W in all_loop_ids:
        for lam in nontriv_irreps:
            F_list.append(chi_pq(holos[W], *lam))
            labels.append({
                'loops': [(W, lam)],
                'edges_in_loops': [edge_sets[W]],
            })

    # Pairs (always include — this is the new content)
    if include_pairs:
        # Lower-rank irreps for pair products to control basis size
        low_irreps = [lam for lam in irrep_set
                       if lam in [(1, 0), (0, 1), (1, 1)]]
        for ia, W1 in enumerate(all_loop_ids):
            for ib, W2 in enumerate(all_loop_ids):
                if ib <= ia:
                    continue
                for lam1 in low_irreps:
                    for lam2 in low_irreps:
                        F_list.append(
                            chi_pq(holos[W1], *lam1) * chi_pq(holos[W2], *lam2)
                        )
                        labels.append({
                            'loops': [(W1, lam1), (W2, lam2)],
                            'edges_in_loops': [edge_sets[W1], edge_sets[W2]],
                        })

    # Triples (controlled growth)
    if include_triples:
        low_irreps = [lam for lam in irrep_set if lam in [(1, 0), (0, 1)]]
        for ia, W1 in enumerate(all_loop_ids):
            for ib, W2 in enumerate(all_loop_ids):
                if ib <= ia:
                    continue
                for ic, W3 in enumerate(all_loop_ids):
                    if ic <= ib:
                        continue
                    for lam1 in low_irreps:
                        for lam2 in low_irreps:
                            for lam3 in low_irreps:
                                F_list.append(
                                    chi_pq(holos[W1], *lam1)
                                    * chi_pq(holos[W2], *lam2)
                                    * chi_pq(holos[W3], *lam3)
                                )
                                labels.append({
                                    'loops': [(W1, lam1), (W2, lam2),
                                               (W3, lam3)],
                                    'edges_in_loops': [edge_sets[W1],
                                                        edge_sets[W2],
                                                        edge_sets[W3]],
                                })

    F = np.array(F_list)
    return F, labels


# -------------------------------------------------------------------
# Numerical Casimir action via finite difference Lie-derivatives
# -------------------------------------------------------------------

def evaluate_basis_at_samples(samples, irrep_set, include_pairs, include_triples):
    """Compute basis values F at given Haar samples."""
    holos, lengths, edge_sets = loop_holonomies(samples)
    F, labels = build_basis_products(
        holos, lengths, edge_sets, irrep_set,
        include_pairs=include_pairs,
        include_triples=include_triples,
    )
    return F, labels, holos, lengths, edge_sets


def _evaluate_F_only(samples, irrep_set, include_pairs, include_triples):
    """Compute F values without holos return — for perturbed links."""
    holos, _, edge_sets = loop_holonomies(samples)
    F, _ = build_basis_products(
        holos, [], edge_sets, irrep_set,
        include_pairs=include_pairs,
        include_triples=include_triples,
    )
    return F


def casimir_action_link(F_at_U, samples, link_key, irrep_set,
                         include_pairs, include_triples,
                         eps, T_list):
    """
    Compute Chat_e F at the given samples for link e = link_key.

    Uses central difference along each generator T_a:
       (Chat_e F)(U) ~ -Sum_a [F(U^{+a}) + F(U^{-a}) - 2 F(U)] / eps^2
    where U^{+-a} has link_key replaced by U_link exp(+- i eps T_a).

    Returns: array of shape (n_basis, N) — the function values of Chat_e F.
    """
    n_basis, N = F_at_U.shape
    Chat_F = np.zeros((n_basis, N), dtype=complex)

    for T_a in T_list:
        # Forward perturbation
        samples_plus = perturbed_links(samples, link_key, T_a, eps, sign=+1)
        F_plus = _evaluate_F_only(samples_plus, irrep_set,
                                    include_pairs, include_triples)
        # Backward
        samples_minus = perturbed_links(samples, link_key, T_a, eps, sign=-1)
        F_minus = _evaluate_F_only(samples_minus, irrep_set,
                                    include_pairs, include_triples)
        # Central difference of second derivative; minus sign from Casimir convention
        Chat_F -= (F_plus + F_minus - 2.0 * F_at_U) / (eps ** 2)

    return Chat_F


def build_hamiltonian_matrices(g_squared, samples, irrep_set,
                                include_pairs, include_triples,
                                eps=1e-2, verbose=True, N_c=3):
    """
    Build full H and Gram matrices for the spin-network basis.

    Casimir matrix element <F_a | Chat_e | F_b> = mean_n F_a(U^n)* (Chat_e F_b)(U^n)

    Magnetic matrix element <F_a | M | F_b> with
       M(U) = -(1/(g^2 N_c)) Sum_p Re Tr U_p
    """
    F, labels, holos, lengths, edge_sets = evaluate_basis_at_samples(
        samples, irrep_set, include_pairs, include_triples
    )
    n_basis, N = F.shape
    if verbose:
        print(f"  Basis size: {n_basis}, samples: {N}")

    # Gram matrix
    Gram = (np.conj(F) @ F.T) / N

    # Magnetic operator on samples
    plaqs = [holos[f'P{i}{j}'] for i in [0, 1] for j in [0, 1]]
    M_values = -(1.0 / g_squared) * sum(re_trace_over_Nc(p, N_c) for p in plaqs)
    H_mag = (np.conj(F) * M_values[np.newaxis, :]) @ F.T / N

    # Casimir on each link
    T_list = gell_mann_generators()
    H_C = np.zeros((n_basis, n_basis), dtype=complex)
    for k, link_key in enumerate(LINK_KEYS):
        if verbose:
            t0 = time.time()
        Chat_F = casimir_action_link(F, samples, link_key, irrep_set,
                                       include_pairs, include_triples,
                                       eps, T_list)
        # <F_a | Chat_e | F_b> = sum_n F_a(U^n)* (Chat_e F_b)(U^n) / N
        contrib = (np.conj(F) @ Chat_F.T) / N
        H_C += contrib
        if verbose:
            dt = time.time() - t0
            print(f"    link {link_key}: Casimir contribution computed "
                  f"({dt:.1f}s)")
    H_C *= (g_squared / 2.0)

    H = H_C + H_mag
    H = 0.5 * (H + np.conj(H.T))
    Gram = 0.5 * (Gram + np.conj(Gram.T))

    return H, Gram, F, labels, holos


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
    plaqs = [holos[f'P{i}{j}'] for i in [0, 1] for j in [0, 1]]
    P_vals = sum(re_trace_over_Nc(p) for p in plaqs) / 4.0
    psi_at = np.conj(psi) @ F
    norm = np.mean(np.abs(psi_at) ** 2)
    return float(np.mean(np.abs(psi_at) ** 2 * P_vals) / norm)


def expectation_P_indiv(psi, F, holos):
    plaqs = [holos[f'P{i}{j}'] for i in [0, 1] for j in [0, 1]]
    psi_at = np.conj(psi) @ F
    norm = np.mean(np.abs(psi_at) ** 2)
    return [float(np.mean(np.abs(psi_at) ** 2 * re_trace_over_Nc(p)) / norm)
             for p in plaqs]


def run_one(g_squared, irrep_set, N_samples=20000, seed=11,
             include_pairs=True, include_triples=False, eps=1e-2,
             verbose=True):
    if verbose:
        print(f"\n--- 2x2 torus spin-network, g^2 = {g_squared}, "
              f"N = {N_samples}, eps = {eps} ---")
        print(f"  irreps: {irrep_set}, pairs: {include_pairs}, "
              f"triples: {include_triples}")
    t0 = time.time()
    samples = haar_sample_8links(N_samples, seed=seed)
    H, Gram, F, labels, holos = build_hamiltonian_matrices(
        g_squared, samples, irrep_set,
        include_pairs=include_pairs,
        include_triples=include_triples,
        eps=eps, verbose=verbose,
    )
    evals, evecs, n_keep = diagonalize_with_gram(H, Gram)

    psi0 = evecs[:, 0]
    P_avg = expectation_P(psi0, F, holos)
    P_indiv = expectation_P_indiv(psi0, F, holos)

    if verbose:
        print(f"  E_0 = {evals[0].real:.6f}  (kept {n_keep}/{F.shape[0]})")
        print(f"  <P>_avg = {P_avg:.6f}")
        print(f"  Plaq: P00={P_indiv[0]:.4f}, P10={P_indiv[1]:.4f}, "
              f"P01={P_indiv[2]:.4f}, P11={P_indiv[3]:.4f}")
        print(f"  Total time: {time.time()-t0:.1f}s")

    return {
        'g_squared': g_squared,
        'P_avg': P_avg,
        'P_indiv': P_indiv,
        'E_0': evals[0].real,
        'n_basis': F.shape[0],
        'n_kept': n_keep,
        'eigenvalues': evals[:5].real.tolist(),
    }


# -------------------------------------------------------------------
# Sanity checks for numerical Casimir
# -------------------------------------------------------------------

def sanity_check_casimir():
    """
    Verify numerical Casimir on chi_(1,0)(P_00).
    chi_(1,0)(P_00) is a fundamental-rep character of the plaquette holonomy.
    The plaquette traverses 4 links: x_00, y_10, x_01 (inv), y_00 (inv).
    Each link has Casimir eigenvalue C_2(fund) = 4/3 acting on this character.
    Total Casimir sum: Sum_e Chat_e chi_(1,0)(P00) = 4 * (4/3) chi_(1,0)(P00)
                     = (16/3) chi_(1,0)(P00).
    """
    print("\n=== Sanity check: numerical Casimir on chi_(1,0)(P_00) ===")
    samples = haar_sample_8links(N=200, seed=999)
    holos, lengths, edge_sets = loop_holonomies(samples)
    F_test = chi_pq(holos['P00'], 1, 0)  # shape (N,)

    T_list = gell_mann_generators()
    eps = 1e-2

    total = np.zeros_like(F_test)
    P00_edges = edge_sets['P00']
    for link_key in LINK_KEYS:
        Chat_F = np.zeros_like(F_test)
        for T_a in T_list:
            samples_plus = perturbed_links(samples, link_key, T_a, eps, +1)
            holos_plus, _, _ = loop_holonomies(samples_plus)
            F_plus = chi_pq(holos_plus['P00'], 1, 0)
            samples_minus = perturbed_links(samples, link_key, T_a, eps, -1)
            holos_minus, _, _ = loop_holonomies(samples_minus)
            F_minus = chi_pq(holos_minus['P00'], 1, 0)
            Chat_F -= (F_plus + F_minus - 2.0 * F_test) / (eps ** 2)
        # Compute ratio Chat_F / F_test as an indicator
        if link_key in P00_edges:
            ratio = np.mean(Chat_F.real * F_test.real
                             + Chat_F.imag * F_test.imag) \
                    / np.mean(np.abs(F_test) ** 2)
            print(f"  link {link_key} (in P00): Chat_e contribution / |F|^2 ~ "
                  f"{ratio:.4f}  (expected 4/3 = 1.333)")
        else:
            ratio = np.mean(np.abs(Chat_F) ** 2) ** 0.5 / np.mean(np.abs(F_test) ** 2) ** 0.5
            print(f"  link {link_key} (NOT in P00): |Chat_e F| / |F| ~ "
                  f"{ratio:.4e}  (expected ~0)")
        total += Chat_F

    total_ratio = np.mean(total.real * F_test.real + total.imag * F_test.imag) \
                   / np.mean(np.abs(F_test) ** 2)
    print(f"\n  TOTAL: Sum_e Chat_e chi_(1,0)(P00) / chi_(1,0)(P00) ~ "
          f"{total_ratio:.4f}  (expected 16/3 = 5.333)")


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 70)
    print("Cl(3) -> KS, 2x2 spatial torus, spin-network ED")
    print("(numerical Casimir via finite-difference Lie derivatives)")
    print("=" * 70)

    print("\n[1] Verify Gell-Mann generators")
    verify_gell_mann()

    print("\n[2] Sanity check numerical Casimir")
    sanity_check_casimir()

    print("\n[3] Test small basis at g^2 = 1")
    irrep_3 = [(0, 0), (1, 0), (0, 1)]
    r1 = run_one(1.0, irrep_3, N_samples=4000, seed=11,
                  include_pairs=False, eps=1e-2, verbose=True)

    print("\n[4] Add overlapping pairs at g^2 = 1")
    r2 = run_one(1.0, irrep_3, N_samples=4000, seed=11,
                  include_pairs=True, eps=1e-2, verbose=True)

    print("\n[5] 4 irreps with pairs at g^2 = 1")
    irrep_4 = [(0, 0), (1, 0), (0, 1), (1, 1)]
    r3 = run_one(1.0, irrep_4, N_samples=4000, seed=11,
                  include_pairs=True, eps=1e-2, verbose=True)

    print("\n[6] 6 irreps with pairs at g^2 = 1")
    irrep_6 = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]
    r4 = run_one(1.0, irrep_6, N_samples=4000, seed=11,
                  include_pairs=True, eps=1e-2, verbose=True)

    print("\n[7] 8 irreps with pairs at g^2 = 1")
    irrep_8 = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2), (2, 1), (1, 2)]
    r5 = run_one(1.0, irrep_8, N_samples=4000, seed=11,
                  include_pairs=True, eps=1e-2, verbose=True)

    print("\n=== Summary at g^2 = 1.0 ===")
    print(f"3 irreps, no pairs:                <P> = {r1['P_avg']:.4f}, n_basis = {r1['n_basis']}")
    print(f"3 irreps, with pairs:              <P> = {r2['P_avg']:.4f}, n_basis = {r2['n_basis']}")
    print(f"4 irreps, with pairs:              <P> = {r3['P_avg']:.4f}, n_basis = {r3['n_basis']}")
    print(f"6 irreps, with pairs:              <P> = {r4['P_avg']:.4f}, n_basis = {r4['n_basis']}")
    print(f"8 irreps, with pairs:              <P> = {r5['P_avg']:.4f}, n_basis = {r5['n_basis']}")
    print(f"\nReference targets:")
    print(f"  Wilson 4D MC beta=6, 2x2x2x16:    0.6243 (spatial only)")
    print(f"  Wilson 4D MC beta=6, 4x4x4x4:     0.5974 (spatial only)")
    print(f"  KS literature (3D thermo limit):  ~0.55-0.60")
    print(f"  Strong-coupling LO at g^2=1:      0.0417")
    print(f"  v3 Casimir-diagonal basis:        0.0434")
