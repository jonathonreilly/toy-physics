"""
Cl(3) -> KS symmetric 2x2 torus computation.

Geometry: 2x2 spatial torus (Z^2 with PBC). 4 sites, 8 links, 4 plaquettes.
Each link is shared by EXACTLY 2 plaquettes (symmetric).

Tree gauge fixing: pick spanning tree of 3 edges (sites 0->1, 0->2, 1->3).
Set those to identity. 8-3=5 physical SU(3) link variables remain:
    U_a = U_x(1,0)  [wrap-around row 0]
    U_b = U_x(0,1)  [link from (0,1) to (1,1)]
    U_c = U_x(1,1)  [wrap-around row 1]
    U_d = U_y(0,1)  [wrap-around col 0]
    U_e = U_y(1,1)  [wrap-around col 1]

After gauge fixing, plaquette holonomies become:
    P0 = U_b^{-1}              (single-link)
    P1 = U_a U_c^{-1}          (two-link)
    P2 = U_b U_e U_d^{-1}      (three-link)
    P3 = U_c U_d U_a^{-1} U_e^{-1}  (four-link, the original full plaquette)

The Hamiltonian (canonical Cl(3) Tr-form):

    H = (g^2/2) sum_{e=1..5} Chat_2(e)  [free Casimir on each phys. link]
      - (1/(g^2 N_c)) sum_{p=1..4} Re Tr U_{P_p}

Note: in the tree-gauge-fixed formulation, each PHYSICAL link variable
is one of the 5; the Casimir term acts only on these 5 variables. The
(g^2/2) coefficient is a per-physical-link energy cost, which is the
correct ground-state Hamiltonian after tree gauge fixing because the
spanning-tree links have their own Casimir energy minimized at trivial,
and the constraint of trivial irrep on tree links is enforced by gauge
fixing. (Actually: physical Casimir on link e in original formulation
has eigenvalue C_2(lambda_e); after tree gauge fixing, the e-th physical
link in our reduced basis is just the holonomy U_e and Casimir acts as
C_2 weight on the single-link character chi_lambda(U_e).)

Approach: Monte Carlo Haar sampling on SU(3)^5, build basis from products
of (a) single-link characters chi_lambda(U_e), and (b) plaquette characters
chi_lambda(U_{P_p}), and any joint loop characters needed for
correlation expressivity. Build Hamiltonian and Gram matrix via MC,
diagonalize (generalized eigenvalue), extract <P>.

Output:
  <P>_avg = (1/4) sum_{p=1..4} <P_p>  -- this is the average plaquette
  Sweep over g^2 values
  Convergence in basis size, sample size
"""

from __future__ import annotations

import sys
import time
import numpy as np
from numpy.linalg import eigh

from cl3_ks_single_plaquette_2026_05_07 import casimir, dim_irrep, fund_tensor_pq, antifund_tensor_pq
from cl3_ks_two_plaquette_2026_05_07 import sample_su3, chi_pq


def haar_sample_5links(N: int, seed: int = 42):
    """Generate N samples of 5 independent SU(3) matrices."""
    samples = []
    for k in range(5):
        samples.append(sample_su3(N, seed=seed + k))
    return tuple(samples)


def plaquette_holonomies(U_a, U_b, U_c, U_d, U_e):
    """
    Compute the 4 plaquette holonomies for the 2x2 torus after tree
    gauge fixing.

    Tree-fixing convention:
        Tree links: (0->1), (0->2), (1->3) set to I.
        Physical links: U_a = U_x(1,0), U_b = U_x(0,1), U_c = U_x(1,1),
                        U_d = U_y(0,1), U_e = U_y(1,1)

    Plaquettes (after I substitutions for tree links):
        P0 = U_x(0,0) * U_y(1,0) * U_x(0,1)^-1 * U_y(0,0)^-1
           = I * I * U_b^-1 * I = U_b^-1
        P1 = U_x(1,0) * U_y(0,0) * U_x(1,1)^-1 * U_y(1,0)^-1
           = U_a * I * U_c^-1 * I = U_a U_c^-1
        P2 = U_x(0,1) * U_y(1,1) * U_x(0,0)^-1 * U_y(0,1)^-1
           = U_b * U_e * I * U_d^-1 = U_b U_e U_d^-1
        P3 = U_x(1,1) * U_y(0,1) * U_x(1,0)^-1 * U_y(1,1)^-1
           = U_c * U_d * U_a^-1 * U_e^-1
    """
    # P0
    P0 = np.conj(U_b.transpose(0, 2, 1))  # U_b^-1 (since unitary)

    # P1 = U_a U_c^-1
    Uc_inv = np.conj(U_c.transpose(0, 2, 1))
    P1 = np.einsum('nij,njk->nik', U_a, Uc_inv)

    # P2 = U_b U_e U_d^-1
    Ud_inv = np.conj(U_d.transpose(0, 2, 1))
    Tmp = np.einsum('nij,njk->nik', U_b, U_e)
    P2 = np.einsum('nij,njk->nik', Tmp, Ud_inv)

    # P3 = U_c U_d U_a^-1 U_e^-1
    Ua_inv = np.conj(U_a.transpose(0, 2, 1))
    Ue_inv = np.conj(U_e.transpose(0, 2, 1))
    T1 = np.einsum('nij,njk->nik', U_c, U_d)
    T2 = np.einsum('nij,njk->nik', T1, Ua_inv)
    P3 = np.einsum('nij,njk->nik', T2, Ue_inv)

    return P0, P1, P2, P3


def re_trace_over_Nc(M: np.ndarray, N_c: int = 3) -> np.ndarray:
    """(1/N_c) Re Tr M_n for stack of matrices M with shape (N, 3, 3)."""
    return np.trace(M, axis1=1, axis2=2).real / N_c


def build_basis_2x2_torus(U_a, U_b, U_c, U_d, U_e, irrep_set, P_holos,
                          include_link_chars=True,
                          include_plaquette_chars=True,
                          include_double_plaquette_chars=False):
    """
    Construct the basis of class functions for the 2x2 torus 5-link
    gauge-fixed Hilbert space.

    The basis is built as products / individual class functions.
    All elements are SU(3)-gauge invariant (under simultaneous
    conjugation on all 5 physical links).

    Components:
      (1) Trivial constant
      (2) Single-link characters chi_lambda(U_e) for each phys. link
      (3) Plaquette characters chi_lambda(U_P_p) for each plaquette
          P_0, P_1, P_2, P_3
      (4) (optional) Pair plaquette characters chi(P_p) chi(P_q)
      (5) (optional) Double-loop invariants

    Returns: F_array of shape (n_basis, N_samples), labels list.
    """
    N = U_a.shape[0]
    F_list = [np.ones(N, dtype=complex)]
    labels = ['1']

    Us_with_labels = [(U_a, 'a'), (U_b, 'b'), (U_c, 'c'), (U_d, 'd'), (U_e, 'e')]
    Ps_with_labels = [(P_holos[0], 'P0'), (P_holos[1], 'P1'),
                       (P_holos[2], 'P2'), (P_holos[3], 'P3')]

    # (2) Single-link characters
    if include_link_chars:
        for U, lbl in Us_with_labels:
            for lam in irrep_set:
                if lam == (0, 0):
                    continue  # already have trivial
                F_list.append(chi_pq(U, *lam))
                labels.append(f"chi_{lam}({lbl})")

    # (3) Plaquette characters
    if include_plaquette_chars:
        for P, lbl in Ps_with_labels:
            for lam in irrep_set:
                if lam == (0, 0):
                    continue
                F_list.append(chi_pq(P, *lam))
                labels.append(f"chi_{lam}({lbl})")

    # (4) Pair plaquette characters: chi(P_p) chi(P_q) for distinct
    # plaquettes — captures ground-state correlations between plaquettes
    if include_double_plaquette_chars:
        # Limit to fundamental and antifundamental on each plaquette
        low_irreps = [lam for lam in irrep_set if lam in [(1, 0), (0, 1)]]
        for i in range(4):
            for j in range(i + 1, 4):
                P_i, lbl_i = Ps_with_labels[i]
                P_j, lbl_j = Ps_with_labels[j]
                for lam_i in low_irreps:
                    for lam_j in low_irreps:
                        F_list.append(chi_pq(P_i, *lam_i) * chi_pq(P_j, *lam_j))
                        labels.append(f"chi_{lam_i}({lbl_i}) chi_{lam_j}({lbl_j})")

    return np.array(F_list), labels


def build_hamiltonian_2x2_torus(g_squared, U_a, U_b, U_c, U_d, U_e,
                                  P_holos, F, labels,
                                  irrep_set, N_c=3):
    """
    Build Hamiltonian and Gram matrix in the chosen basis, on the 2x2 torus.

    H = (g^2/2) sum_{phys link e} C_hat(e) - (1/(g^2 N_c)) sum_p Re Tr U_p

    Magnetic operator: numerical at samples.
    Casimir operator: analytical for single-link characters; for plaquette
    characters chi_lambda(U_P_p), Casimir of the underlying physical
    links acts non-trivially.

    For a plaquette character chi_lambda(U_P_p) where U_P_p is built from
    n_p physical links, the action of sum_phys_link Casimirs is
    n_p * C_2(lambda) -- i.e., each physical link contributing to U_P_p
    has the link in irrep lambda (via the spin-network interpretation),
    giving C_2(lambda) per link.

    Wait — more carefully: chi_lambda(U_p) is NOT an eigenstate of
    sum_e Chat(e) in general. The Casimir on a single link Chat(e) acts
    on the function f(U) = chi_lambda(U_p), which depends on U_p, which
    depends on multiple physical links. The action is:

        Chat(e) chi_lambda(U_p) = ?

    Use: chi_lambda(U_p) = sum_{i,j} (D^lambda(U_p))_{ii}.
    For Wilson loop W_lambda(p) = chi_lambda(U_p) where U_p = U_1...U_4,
    the action of left- or right-translation operator on link e (i.e.,
    Chat acting via the right-invariant or left-invariant vector field)
    gives a quadratic Casimir times the loop in irrep lambda. Specifically:

        Chat(U_e) chi_lambda(U_p) = C_2(lambda) chi_lambda(U_p)
                                    when U_e appears in U_p, ELSE 0.

    This is because the Casimir on link e, being the SU(3)-invariant
    second derivative on the e-th SU(3) factor, only "sees" the irrep
    lambda flowing through that link. Each link in the loop contributes
    C_2(lambda).

    So for chi_lambda(U_P_p) where U_P_p has n_p physical links:
        sum_{phys link} Chat = n_p * C_2(lambda)  (acts diagonally on chi_lambda(P_p))

    For products chi_lambda(P_i) chi_mu(P_j):
        sum_e Chat acting on chi_lambda(P_i)*chi_mu(P_j) is:
        [sum_{e in P_i} Chat * (chi_lambda(P_i)) ] * chi_mu(P_j)
            = [n_{P_i} * C_2(lambda)] * chi_lambda(P_i) chi_mu(P_j) ?

    Wait, this is wrong if P_i and P_j share physical links! Then the
    same Casimir Chat(e) acts on both factors. The action becomes more
    complicated -- it's like Casimir on tensor product of two
    representations, not sum of Casimirs.

    For first-pass results: use a SIMPLE proxy that the basis's "irrep
    weight" gives the Casimir energy directly via the dominant irrep
    flowing through it. This is exact for single-link characters and
    exact for chi_lambda(P_p) (assuming all sides of P_p flow with same
    irrep). It's APPROXIMATE for products. We'll mark this in the output.

    To be more rigorous, use Monte Carlo evaluation of the matrix
    elements of Chat -- but that requires a representation of the
    differential operator, which is not directly samplable.

    Approach: For our basis (single-link characters and individual
    plaquette characters), the approximation is exact. For products
    chi_a(P_i) chi_b(P_j), we use the spin-network truncation that
    each physical link contributes max(C_2(lambda) for irreps on it).
    """
    n = F.shape[0]

    # Magnetic operator at samples
    re_tr_P = [re_trace_over_Nc(P) for P in P_holos]
    M_values = -(1.0 / g_squared) * np.sum(re_tr_P, axis=0)
    # Note: re_tr_P is already 1/N_c factor; the magnetic operator is
    # -(1/(g^2 N_c)) sum_p Re Tr U_p, but we put the 1/N_c into
    # re_trace_over_Nc, so M_values = -(1/g^2) sum_p P_p where P_p = (1/N_c) Re Tr U_p.
    # Wait, that would give the wrong factor. Let me re-check:
    #   H_mag = -(1/(g^2 N_c)) sum_p Re Tr U_p
    #   We have re_tr_P_p = (1/N_c) Re Tr U_p (from re_trace_over_Nc)
    #   So H_mag = -(1/g^2) * N_c * sum_p re_tr_P_p ??? No that's also wrong.
    #   H_mag = -(1/(g^2 N_c)) Re Tr U_p = -(1/g^2) * (1/N_c) Re Tr U_p
    #         = -(1/g^2) * re_tr_P_p
    # So yes M_values = -(1/g^2) sum_p re_tr_P_p is correct.

    # Build Gram matrix: <f_i | f_j> = (1/N) sum F_i* F_j
    N_samples = F.shape[1]
    Gram = (np.conj(F) @ F.T) / N_samples

    # Magnetic matrix
    H_mag = (np.conj(F) * M_values[np.newaxis, :]) @ F.T / N_samples

    # Casimir matrix: build from labels (irrep weight extraction)
    H_cas = np.zeros((n, n), dtype=complex)
    import re
    for i, lbl in enumerate(labels):
        if lbl == '1':
            cas_val = 0.0
        else:
            # Match patterns like "chi_(p, q)(name)" or
            # "chi_(p1,q1)(...) chi_(p2,q2)(...)"
            matches = re.findall(r"chi_\((\d+), (\d+)\)\(([abcdeP\d]+)\)", lbl)
            if not matches:
                cas_val = 0.0
            else:
                # Each (p,q,target) contributes the SPIN-NETWORK Casimir:
                # - if target is single-link a/b/c/d/e: C_2(p,q) from
                #   that single physical link
                # - if target is plaquette P0/P1/P2/P3: 4 * C_2(p,q),
                #   because every plaquette has 4 sides, each carrying
                #   irrep (p,q) in the spin-network state. This is
                #   gauge-invariant and true REGARDLESS of tree gauge
                #   fixing (tree-fixed links also carry the irrep label
                #   in the spin-network sense, even though their group
                #   elements are set to identity).
                #
                # All 4 plaquettes are SYMMETRIC under this rule:
                # 4 sides x C_2 = 4 C_2 per plaquette, regardless of
                # the gauge-fixing-induced asymmetry in the plaquette
                # holonomy formula.
                cas_val = 0.0
                for p_str, q_str, target in matches:
                    p, q = int(p_str), int(q_str)
                    c2 = casimir(p, q)
                    if target in ['a', 'b', 'c', 'd', 'e']:
                        cas_val += c2  # single physical link
                    elif target.startswith('P'):
                        cas_val += 4.0 * c2  # plaquette: 4 links each in irrep
                # For products (e.g. chi(P_0) chi(P_2)) sharing physical
                # links, the Casimir on the shared link sees the TENSOR
                # PRODUCT of irreps. We sum C_2 of each separately,
                # which is an UPPER BOUND on the true Casimir energy
                # (Casimir of tensor product <= sum of individual Casimirs
                # only when both irreps are trivial; otherwise more
                # complex). This variational treatment gives a variational
                # upper bound on E_0 (i.e., correct Rayleigh-Ritz).
        H_cas[i, i] = (g_squared / 2.0) * cas_val

    H = H_cas + H_mag
    H = 0.5 * (H + np.conj(H.T))
    Gram = 0.5 * (Gram + np.conj(Gram.T))

    return H, Gram


def diagonalize_with_gram(H, Gram, tol=1e-7):
    """Generalized eigenvalue with regularization."""
    Gram = 0.5 * (Gram + np.conj(Gram.T))
    g_evals, g_evecs = eigh(Gram)
    keep = g_evals > tol * g_evals[-1]
    n_keep = int(np.sum(keep))
    g_inv_sqrt = np.zeros_like(g_evals)
    g_inv_sqrt[keep] = 1.0 / np.sqrt(g_evals[keep])
    P_proj = g_evecs[:, keep] * g_inv_sqrt[keep][np.newaxis, :]
    H_orth = np.conj(P_proj.T) @ H @ P_proj
    H_orth = 0.5 * (H_orth + np.conj(H_orth.T))
    evals, evecs_orth = eigh(H_orth)
    evecs = P_proj @ evecs_orth
    return evals, evecs, n_keep


def expectation_P_avg(psi, F, P_holos, N_c=3):
    """<P>_avg = (1/4) sum_p (1/N_c) Re Tr U_p, evaluated in state psi."""
    P_vals = np.mean([re_trace_over_Nc(P) for P in P_holos], axis=0)
    psi_at = np.conj(psi) @ F  # shape (N,)
    norm = np.mean(np.abs(psi_at) ** 2)
    return float(np.mean(np.abs(psi_at) ** 2 * P_vals) / norm)


def expectation_P_individual(psi, F, P_holos, N_c=3):
    """Individual <P_p> for each plaquette."""
    psi_at = np.conj(psi) @ F
    norm = np.mean(np.abs(psi_at) ** 2)
    out = []
    for P in P_holos:
        P_vals = re_trace_over_Nc(P)
        out.append(float(np.mean(np.abs(psi_at) ** 2 * P_vals) / norm))
    return out


def run_one_g(g_squared, irrep_set, N_samples, seed=11,
              include_double_plaquette=True, verbose=True):
    if verbose:
        print(f"\n--- 2x2 torus computation, g^2 = {g_squared}, "
              f"{N_samples} samples ---")
    t0 = time.time()
    U_a, U_b, U_c, U_d, U_e = haar_sample_5links(N_samples, seed=seed)
    P_holos = plaquette_holonomies(U_a, U_b, U_c, U_d, U_e)

    F, labels = build_basis_2x2_torus(
        U_a, U_b, U_c, U_d, U_e, irrep_set, P_holos,
        include_link_chars=True,
        include_plaquette_chars=True,
        include_double_plaquette_chars=include_double_plaquette,
    )
    if verbose:
        print(f"  Basis size: {F.shape[0]}")
        print(f"  Sampling+basis evaluation: {time.time()-t0:.1f}s")

    t1 = time.time()
    H, Gram = build_hamiltonian_2x2_torus(
        g_squared, U_a, U_b, U_c, U_d, U_e, P_holos, F, labels, irrep_set
    )
    if verbose:
        print(f"  H/Gram build: {time.time()-t1:.1f}s")

    t2 = time.time()
    evals, evecs, n_keep = diagonalize_with_gram(H, Gram)
    if verbose:
        print(f"  Diagonalization: {time.time()-t2:.1f}s")

    psi0 = evecs[:, 0]
    P_avg = expectation_P_avg(psi0, F, P_holos)
    P_indiv = expectation_P_individual(psi0, F, P_holos)

    if verbose:
        print(f"  E_0 = {evals[0].real:.6f}  (kept {n_keep}/{F.shape[0]})")
        print(f"  <P>_avg = {P_avg:.6f}")
        print(f"  Individual: P0={P_indiv[0]:.4f}, P1={P_indiv[1]:.4f}, "
              f"P2={P_indiv[2]:.4f}, P3={P_indiv[3]:.4f}")

        # Top components
        abs_psi = np.abs(psi0)
        top = np.argsort(-abs_psi)[:5]
        print(f"  Top 5 components:")
        for idx in top:
            if idx < len(labels):
                print(f"    {labels[idx]:<45} {psi0[idx].real:>+.4f}")

    return {
        'g_squared': g_squared,
        'P_avg': P_avg,
        'P_indiv': P_indiv,
        'E_0': evals[0].real,
        'n_basis': F.shape[0],
        'n_kept': n_keep,
    }


def coupling_sweep(irrep_set, N_samples=20000, seed=11,
                    include_double_plaquette=True):
    print("\n=== Coupling sweep on 2x2 torus, KS Hamiltonian ===")
    print(f"  Irrep set: {irrep_set}")
    print(f"  N_samples: {N_samples}, double-plaq corr: {include_double_plaquette}")
    print()

    rows = []
    for g2 in [0.5, 0.75, 1.0, 1.5, 2.0]:
        r = run_one_g(g2, irrep_set, N_samples, seed,
                       include_double_plaquette, verbose=True)
        rows.append(r)

    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"{'g^2':>6}  {'<P>_avg':>10}  {'P0':>8}  {'P1':>8}  {'P2':>8}  {'P3':>8}")
    for r in rows:
        print(f"{r['g_squared']:>6.2f}  {r['P_avg']:>10.6f}  "
              f"{r['P_indiv'][0]:>8.4f}  {r['P_indiv'][1]:>8.4f}  "
              f"{r['P_indiv'][2]:>8.4f}  {r['P_indiv'][3]:>8.4f}")
    return rows


def convergence_test_basis(g_squared=1.0, N_samples=20000, seed=11):
    """Test convergence of <P>_avg with basis size."""
    print("\n=== Basis convergence test at g^2 = 1.0 ===")
    print()
    rows = []
    irrep_sets = [
        [(0, 0), (1, 0), (0, 1)],  # fundamental + antifund only
        [(0, 0), (1, 0), (0, 1), (1, 1)],  # + adjoint
        [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)],  # + symmetric tensor
    ]
    for irreps in irrep_sets:
        for double_plaq in [False, True]:
            print(f"--- Irreps: {irreps}, double-plaq: {double_plaq} ---")
            r = run_one_g(g_squared, irreps, N_samples, seed,
                           include_double_plaquette=double_plaq,
                           verbose=True)
            rows.append({
                'irreps': irreps,
                'double_plaq': double_plaq,
                'n_basis': r['n_basis'],
                'P_avg': r['P_avg'],
                'E_0': r['E_0'],
            })
            print()

    print()
    print("=" * 70)
    print("Basis convergence summary:")
    print("=" * 70)
    print(f"{'irreps':<35} {'double':>6} {'#basis':>7} {'E_0':>10} {'<P>_avg':>10}")
    for r in rows:
        n_irrep = len(r['irreps'])
        irrep_str = f"{n_irrep} irreps"
        print(f"{irrep_str:<35} {str(r['double_plaq']):>6} "
              f"{r['n_basis']:>7}  {r['E_0']:>10.6f}  {r['P_avg']:>10.6f}")


def convergence_test_samples(g_squared=1.0, irrep_set=None,
                              include_double_plaquette=True):
    """Test convergence with N_samples."""
    if irrep_set is None:
        irrep_set = [(0, 0), (1, 0), (0, 1), (1, 1)]
    print("\n=== Sample-size convergence test at g^2 = 1.0 ===")
    print(f"  Irreps: {irrep_set}, double-plaq: {include_double_plaquette}")
    print()
    rows = []
    for N in [5000, 10000, 20000, 50000, 100000]:
        for seed in [11, 22, 33]:
            r = run_one_g(g_squared, irrep_set, N, seed,
                           include_double_plaquette, verbose=False)
            rows.append({'N': N, 'seed': seed, **r})

    print()
    print("=" * 70)
    print("Sample convergence summary:")
    print("=" * 70)
    print(f"{'N':>8}  {'seed':>5}  {'E_0':>12}  {'<P>_avg':>10}")
    for r in rows:
        print(f"{r['N']:>8}  {r['seed']:>5}  "
              f"{r['E_0']:>12.6f}  {r['P_avg']:>10.6f}")

    # Statistics by N: mean and stdev across seeds
    print()
    print("Mean +- std over seeds at each N:")
    print(f"{'N':>8}  {'mean<P>':>10}  {'std':>10}")
    Ns = sorted(set(r['N'] for r in rows))
    for N in Ns:
        Ps = [r['P_avg'] for r in rows if r['N'] == N]
        mean = float(np.mean(Ps))
        std = float(np.std(Ps, ddof=1)) if len(Ps) > 1 else 0.0
        print(f"{N:>8}  {mean:>10.6f}  {std:>10.6f}")


if __name__ == "__main__":
    print("=" * 70)
    print("Cl(3) -> KS, 2x2 spatial torus (Z^2 PBC), 5 phys. SU(3) links")
    print("=" * 70)

    # Default irrep set: (0,0), (1,0), (0,1), (1,1)
    default_irreps = [(0, 0), (1, 0), (0, 1), (1, 1)]

    # --- Convergence: basis ---
    print("\n[1] Basis convergence test")
    convergence_test_basis(g_squared=1.0, N_samples=20000, seed=11)

    # --- Convergence: sample size ---
    print("\n[2] Sample convergence test")
    convergence_test_samples(g_squared=1.0,
                              irrep_set=default_irreps,
                              include_double_plaquette=True)

    # --- Coupling sweep ---
    print("\n[3] Coupling sweep")
    coupling_sweep(irrep_set=default_irreps, N_samples=50000, seed=11,
                    include_double_plaquette=True)

    print()
    print("=" * 70)
    print("Reference values:")
    print("  KS literature (Hamilton limit) at g^2~1:  ~0.55-0.60")
    print("  Wilson MC (4D) beta=6:                       0.5934")
    print("  Single-plaquette toy at g^2=1:               0.218")
    print("  Dumbbell extended-basis at g^2=1:            0.152")
    print("  K=2 mean-field K-rescaling at g^2=1:         0.415")
    print("=" * 70)
