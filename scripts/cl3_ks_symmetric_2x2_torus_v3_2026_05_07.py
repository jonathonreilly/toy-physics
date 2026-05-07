"""
Cl(3) -> KS symmetric 2x2 torus, version 3.

CASIMIR-DIAGONAL BASIS APPROACH:

Use a basis of SINGLE Wilson-loop characters chi_lambda(W) for various
closed loops W on the 2x2 torus, in various SU(3) irreps lambda. Each
chi_lambda(W) is an eigenstate of the link Casimir sum:
    sum_e Chat(e) chi_lambda(W) = |W| * C_2(lambda) * chi_lambda(W)

where |W| is the number of links in W. This makes Casimir EXACTLY
diagonal in the basis.

Loops on 2x2 torus (8 links, 4 sites):
  - 4 plaquettes (length 4 each)
  - 4 non-contractible loops (length 2 each):
      X0 = U_x(0,0) U_x(1,0): wraps x at row 0
      X1 = U_x(0,1) U_x(1,1): wraps x at row 1
      Y0 = U_y(0,0) U_y(0,1): wraps y at col 0
      Y1 = U_y(1,0) U_y(1,1): wraps y at col 1
  - "Double loops" (length 6 = combine 2 adjacent plaquettes):
      P00 * P10 sharing U_y(1,0) with cancellation -- complex, skip
  - Longer Wilson loops up to length 8 (whole torus boundary)

For each chi_lambda(W), Casimir is exactly diagonal.

Products of DISJOINT loops are also Casimir-diagonal:
  X0 and X1 share links? X0 uses links x_00 + x_10. X1 uses x_01 + x_11.
  These are DISJOINT! Likewise Y0 and Y1 are disjoint, and X-loops and
  Y-loops are disjoint. So {X0, X1, Y0, Y1} are mutually disjoint.

  Plaquettes share links pairwise (each link is in 2 plaquettes).

Strategy:
  - Use single-loop characters chi_lambda(W) for W in {plaquettes,
    non-contractible} as the primary basis.
  - For each W, include irreps up to some C_2 cutoff (default C_2 <= 4
    or 5).
  - Products of DISJOINT non-contractible loops (X0*X1, Y0*Y1, etc.) ARE
    Casimir-diagonal and are added.
  - Avoid products of overlapping plaquette characters since these are
    NOT Casimir-diagonal in this basis.
  - Higher irreps on plaquettes (e.g., (1,1), (2,0), (0,2)) ENRICH the
    basis without violating Casimir diagonality.

Magnetic operator: numerical at samples.
"""

from __future__ import annotations

import time
import numpy as np
from numpy.linalg import eigh

from cl3_ks_single_plaquette_2026_05_07 import casimir, dim_irrep
from cl3_ks_two_plaquette_2026_05_07 import sample_su3, chi_pq


def haar_sample_8links(N: int, seed: int = 42):
    keys = ['x_00', 'x_10', 'x_01', 'x_11', 'y_00', 'y_10', 'y_01', 'y_11']
    samples = {}
    for k, key in enumerate(keys):
        samples[key] = sample_su3(N, seed=seed + k)
    return samples


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
# Wilson loop holonomies on 2x2 torus
# -------------------------------------------------------------------

def loop_holonomies(samples):
    """
    Compute all relevant Wilson-loop holonomies.

    Returns dict: name -> (N, 3, 3) holonomy matrices, and length dict.
    """
    holos = {}
    lengths = {}

    # Plaquettes (length 4 each)
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

    # Non-contractible loops (length 2 each, with PBC the "double-link" loop)
    for j in [0, 1]:
        holos[f'X{j}'] = matprod(samples[f'x_0{j}'], samples[f'x_1{j}'])
        lengths[f'X{j}'] = 2
    for i in [0, 1]:
        holos[f'Y{i}'] = matprod(samples[f'y_{i}0'], samples[f'y_{i}1'])
        lengths[f'Y{i}'] = 2

    # Length-4 "twisted" loops: combinations of X and Y wrap-arounds.
    # W_xy_ji = X_j · Y_i = (U_x(0,j) U_x(1,j)) · (U_y(i,0) U_y(i,1))
    # These are LENGTH-4 closed walks on the 2x2 PBC torus.
    # 4 such loops: (j, i) in {0,1}^2.
    for j in [0, 1]:
        for i in [0, 1]:
            W = matprod(samples[f'x_0{j}'], samples[f'x_1{j}'],
                         samples[f'y_{i}0'], samples[f'y_{i}1'])
            holos[f'W_xy_{j}{i}'] = W
            lengths[f'W_xy_{j}{i}'] = 4

    # Also: "anti-twisted" loops X_j · Y_i^{-1}
    for j in [0, 1]:
        for i in [0, 1]:
            W = matprod(samples[f'x_0{j}'], samples[f'x_1{j}'],
                         matinv(samples[f'y_{i}1']), matinv(samples[f'y_{i}0']))
            holos[f'W_xy_inv_{j}{i}'] = W
            lengths[f'W_xy_inv_{j}{i}'] = 4

    # Longer Wilson loops (length 6: combine plaquette + non-contractible)
    # P00 · X0 = (path going around P00 then around X0):
    #   P00 from (0,0): x_00, y_10, -x_01, -y_00  (returns to (0,0))
    #   X0 from (0,0): x_00, x_10  (returns to (0,0))
    # Concatenate: x_00, y_10, -x_01, -y_00, x_00, x_10  (length 6)
    L_P00_X0 = matprod(samples['x_00'], samples['y_10'],
                        matinv(samples['x_01']), matinv(samples['y_00']),
                        samples['x_00'], samples['x_10'])
    holos['L_P00_X0'] = L_P00_X0
    lengths['L_P00_X0'] = 6

    L_P00_Y0 = matprod(samples['x_00'], samples['y_10'],
                        matinv(samples['x_01']), matinv(samples['y_00']),
                        samples['y_00'], samples['y_01'])
    holos['L_P00_Y0'] = L_P00_Y0
    lengths['L_P00_Y0'] = 6

    return holos, lengths


# -------------------------------------------------------------------
# Basis construction: Casimir-diagonal Wilson-loop characters
# -------------------------------------------------------------------

def build_basis_casimir_diagonal(holos, lengths, irrep_set,
                                   include_plaquettes=True,
                                   include_noncontractible=False,
                                   include_longer_loops=False,
                                   include_disjoint_products=False):
    """
    Build basis from single Wilson-loop characters (Casimir-diagonal).

    Each basis element is chi_lambda(W) for a closed loop W and irrep lambda.
    Casimir eigenvalue: |W| * C_2(lambda).

    Returns: F (n_basis, N), labels list of dicts {'loops': [(W, lambda)], 'cas': float}.
    """
    N = next(iter(holos.values())).shape[0]
    F_list = [np.ones(N, dtype=complex)]
    labels = [{'loops': [], 'cas': 0.0}]  # trivial

    plaq_ids = [f'P{i}{j}' for i in [0, 1] for j in [0, 1]]
    nc_ids = ['X0', 'X1', 'Y0', 'Y1']
    twisted_ids = [f'W_xy_{j}{i}' for j in [0, 1] for i in [0, 1]] + \
                  [f'W_xy_inv_{j}{i}' for j in [0, 1] for i in [0, 1]]
    longer_ids = ['L_P00_X0', 'L_P00_Y0']

    if include_plaquettes:
        for W in plaq_ids:
            for lam in irrep_set:
                if lam == (0, 0):
                    continue
                F_list.append(chi_pq(holos[W], *lam))
                cas = lengths[W] * casimir(*lam)
                labels.append({'loops': [(W, lam)], 'cas': cas})

    if include_noncontractible:
        for W in nc_ids:
            for lam in irrep_set:
                if lam == (0, 0):
                    continue
                F_list.append(chi_pq(holos[W], *lam))
                cas = lengths[W] * casimir(*lam)
                labels.append({'loops': [(W, lam)], 'cas': cas})

    if include_longer_loops:
        # Add twisted length-4 loops (W_xy)
        for W in twisted_ids:
            for lam in irrep_set:
                if lam == (0, 0):
                    continue
                F_list.append(chi_pq(holos[W], *lam))
                cas = lengths[W] * casimir(*lam)
                labels.append({'loops': [(W, lam)], 'cas': cas})

        # Add length-6 loops
        for W in longer_ids:
            for lam in irrep_set:
                if lam == (0, 0):
                    continue
                F_list.append(chi_pq(holos[W], *lam))
                cas = lengths[W] * casimir(*lam)
                labels.append({'loops': [(W, lam)], 'cas': cas})

    if include_disjoint_products:
        # Disjoint pairs:
        # Among non-contractible loops:
        #   X0 (links x_00, x_10) is DISJOINT from X1 (x_01, x_11)
        #   Y0 (y_00, y_01) is DISJOINT from Y1 (y_10, y_11)
        #   X0 vs Y0: x_00, x_10 vs y_00, y_01 -- disjoint
        #   X0 vs Y1: x_00, x_10 vs y_10, y_11 -- disjoint
        #   etc. -- all X-Y pairs are disjoint.
        # Among plaquettes: NO disjoint pairs (each link in 2 plaquettes,
        # so any two plaquettes share at least 1 link).
        if include_noncontractible:
            disjoint_pairs = []
            disjoint_pairs.append(('X0', 'X1'))
            disjoint_pairs.append(('Y0', 'Y1'))
            for x_id in ['X0', 'X1']:
                for y_id in ['Y0', 'Y1']:
                    disjoint_pairs.append((x_id, y_id))
            low_irreps = [lam for lam in irrep_set if lam in [(1, 0), (0, 1)]]
            for W1, W2 in disjoint_pairs:
                for lam1 in low_irreps:
                    for lam2 in low_irreps:
                        F_list.append(
                            chi_pq(holos[W1], *lam1) * chi_pq(holos[W2], *lam2)
                        )
                        cas = (lengths[W1] * casimir(*lam1)
                                + lengths[W2] * casimir(*lam2))
                        labels.append({
                            'loops': [(W1, lam1), (W2, lam2)],
                            'cas': cas,
                        })

    F = np.array(F_list)
    return F, labels


# -------------------------------------------------------------------
# Hamiltonian
# -------------------------------------------------------------------

def build_H_v3(g_squared, samples, F, labels, holos, N_c=3):
    n = F.shape[0]
    N_samples = F.shape[1]

    plaqs_for_M = [holos[f'P{i}{j}'] for i in [0, 1] for j in [0, 1]]
    re_tr_p = sum(re_trace_over_Nc(p) for p in plaqs_for_M)
    M_values = -(1.0 / g_squared) * re_tr_p

    Gram = (np.conj(F) @ F.T) / N_samples
    H_mag = (np.conj(F) * M_values[np.newaxis, :]) @ F.T / N_samples

    H_cas = np.zeros((n, n), dtype=complex)
    for i, lbl in enumerate(labels):
        H_cas[i, i] = (g_squared / 2.0) * lbl['cas']

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


def run_one_g(g_squared, irrep_set, N_samples, seed=11,
               include_plaquettes=True,
               include_noncontractible=False,
               include_longer_loops=False,
               include_disjoint_products=False,
               verbose=True):
    if verbose:
        print(f"\n--- 2x2 torus v3 (Casimir-diag basis), g^2 = {g_squared}, "
              f"N = {N_samples} ---")
    t0 = time.time()
    samples = haar_sample_8links(N_samples, seed=seed)
    holos, lengths = loop_holonomies(samples)
    F, labels = build_basis_casimir_diagonal(
        holos, lengths, irrep_set,
        include_plaquettes=include_plaquettes,
        include_noncontractible=include_noncontractible,
        include_longer_loops=include_longer_loops,
        include_disjoint_products=include_disjoint_products,
    )
    if verbose:
        print(f"  Basis size: {F.shape[0]} (time: {time.time()-t0:.1f}s)")

    H, Gram = build_H_v3(g_squared, samples, F, labels, holos)
    evals, evecs, n_keep = diagonalize_with_gram(H, Gram)

    psi0 = evecs[:, 0]
    P_avg = expectation_P(psi0, F, holos)
    P_indiv = expectation_P_indiv(psi0, F, holos)

    if verbose:
        print(f"  E_0 = {evals[0].real:.6f}  (kept {n_keep}/{F.shape[0]})")
        print(f"  <P>_avg = {P_avg:.6f}")
        print(f"  Plaq: P00={P_indiv[0]:.4f}, P10={P_indiv[1]:.4f}, "
              f"P01={P_indiv[2]:.4f}, P11={P_indiv[3]:.4f}")
        abs_psi = np.abs(psi0)
        top = np.argsort(-abs_psi)[:5]
        for idx in top:
            lbl = labels[idx]
            loops_str = '+'.join(f"chi_{lam}({W})" for W, lam in lbl['loops'])
            if not loops_str:
                loops_str = '1'
            print(f"  {loops_str:<35} amp={psi0[idx].real:+.4f}, "
                  f"cas={lbl['cas']:.2f}")

    return {
        'g_squared': g_squared,
        'P_avg': P_avg,
        'P_indiv': P_indiv,
        'E_0': evals[0].real,
        'n_basis': F.shape[0],
        'n_kept': n_keep,
    }


def basis_convergence_test(g_squared=1.0, N_samples=20000, seed=11):
    print(f"\n=== Basis convergence at g^2 = {g_squared}, N = {N_samples} ===")
    print()
    rows = []

    test_cases = [
        ([(0, 0), (1, 0), (0, 1)],
         dict(),
         '3 irreps, plaq only'),
        ([(0, 0), (1, 0), (0, 1)],
         dict(include_noncontractible=True),
         '3 irreps, plaq + nc'),
        ([(0, 0), (1, 0), (0, 1)],
         dict(include_noncontractible=True,
              include_disjoint_products=True),
         '3 irreps, plaq+nc+disjoint products'),
        ([(0, 0), (1, 0), (0, 1), (1, 1)],
         dict(include_noncontractible=True,
              include_disjoint_products=True),
         '4 irreps, plaq+nc+disjoint products'),
        ([(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)],
         dict(include_noncontractible=True,
              include_disjoint_products=True),
         '6 irreps, plaq+nc+disjoint products'),
        ([(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)],
         dict(include_noncontractible=True,
              include_longer_loops=True,
              include_disjoint_products=True),
         '6 irreps, plaq+nc+longer+disjoint'),
    ]
    for irreps, opts, lbl in test_cases:
        print(f"--- {lbl} ---")
        r = run_one_g(g_squared, irreps, N_samples, seed,
                       include_plaquettes=True,
                       verbose=True, **opts)
        rows.append({**r, 'label': lbl})
        print()

    print()
    print(f"Convergence summary at g^2 = {g_squared}:")
    print(f"{'config':<45} {'#basis':>7} {'E_0':>10} {'<P>_avg':>10}")
    for r in rows:
        print(f"{r['label']:<45} {r['n_basis']:>7}  "
              f"{r['E_0']:>10.6f}  {r['P_avg']:>10.6f}")


def sample_convergence_test(irrep_set, **opts):
    print(f"\n=== Sample size convergence at g^2 = 1.0 ===")
    rows = []
    for N in [5000, 10000, 20000, 50000, 100000]:
        for seed in [11, 22, 33]:
            r = run_one_g(1.0, irrep_set, N, seed, verbose=False,
                           include_plaquettes=True, **opts)
            rows.append({'N': N, 'seed': seed, **r})

    print(f"\n{'N':>8}  {'seed':>5}  {'<P>_avg':>10}  {'E_0':>12}  "
          f"{'#basis':>7}")
    for r in rows:
        print(f"{r['N']:>8}  {r['seed']:>5}  {r['P_avg']:>10.6f}  "
              f"{r['E_0']:>12.6f}  {r['n_basis']:>7}")

    print()
    print(f"Mean +/- std over seeds:")
    print(f"{'N':>8}  {'mean<P>':>10}  {'stdev':>10}")
    Ns = sorted(set(r['N'] for r in rows))
    for N in Ns:
        Ps = [r['P_avg'] for r in rows if r['N'] == N]
        m = float(np.mean(Ps))
        s = float(np.std(Ps, ddof=1)) if len(Ps) > 1 else 0.0
        print(f"{N:>8}  {m:>10.6f}  {s:>10.6f}")


def coupling_sweep(irrep_set, N_samples=50000, seed=11, **opts):
    print(f"\n=== Coupling sweep ===")
    rows = []
    for g2 in [0.5, 0.75, 1.0, 1.5, 2.0]:
        r = run_one_g(g2, irrep_set, N_samples, seed,
                       include_plaquettes=True, verbose=True, **opts)
        rows.append(r)

    print()
    print("Coupling sweep summary:")
    print(f"{'g^2':>6}  {'E_0':>10}  {'<P>_avg':>10}  "
          f"{'plaq spread':>15}")
    for r in rows:
        std = float(np.std(r['P_indiv']))
        print(f"{r['g_squared']:>6.2f}  {r['E_0']:>10.6f}  "
              f"{r['P_avg']:>10.6f}  +-{std:>11.4f}")
    return rows


if __name__ == "__main__":
    print("=" * 70)
    print("Cl(3) -> KS, 2x2 torus v3 (Casimir-diagonal basis)")
    print("=" * 70)

    # [1] Basis convergence
    print("\n[1] Basis convergence")
    basis_convergence_test(g_squared=1.0, N_samples=20000, seed=11)

    # [2] Sample convergence (use largest reasonable basis)
    print("\n[2] Sample convergence")
    sample_convergence_test(
        irrep_set=[(0, 0), (1, 0), (0, 1), (1, 1)],
        include_noncontractible=True,
        include_disjoint_products=True,
    )

    # [3] Coupling sweep
    print("\n[3] Coupling sweep")
    coupling_sweep(
        irrep_set=[(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)],
        N_samples=80000, seed=11,
        include_noncontractible=True,
        include_longer_loops=True,
        include_disjoint_products=True,
    )

    print()
    print("=" * 70)
    print("Reference values for comparison:")
    print("  KS Hamilton limit (literature) at g^2~1:    ~0.55-0.60")
    print("  Wilson 4D MC at beta=6:                       0.5934")
    print("  Single-plaquette toy at g^2=1:                0.218")
    print("  Strong-coupling LO at g^2=1:                  0.0417 (=1/24)")
    print("  Mean-field K=4 (3D cubic):                    0.589")
    print()
    print("Note: 2x2 torus is FINITE-VOLUME and 2D-PBC; the literature")
    print("reference is THERMODYNAMIC LIMIT in 3D. Direct comparison is")
    print("not exact -- but tracking the trend matters.")
    print("=" * 70)
