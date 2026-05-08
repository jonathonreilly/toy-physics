"""
W1.exact — Full SU(3) Spin-Network ED with engineering optimizations.

This is the W1.full v4 runner with two engineering optimizations to break
through the Λ=2, max_active=4 compute frontier:

1. **Matrix-free Lanczos vertex Q construction**: replaces the dense
   `eigh` on the (8^4)×(8^4) = 4096×4096 projector matrix at the
   `(1,1)^4` vertex with a matrix-free Lanczos eigensolver that uses
   tensor-product matvec.  Reduces O(N³) memory and time to O(N²) per
   matvec × O(n_inv·log) iterations.

2. **Sparse Hamiltonian + sparse eigsh ground-state finder**: replaces
   the dense `eigh` on the H matrix with `scipy.sparse.linalg.eigsh`
   to compute only the lowest few eigenvalues.

Goal: reach Λ=2, max_active=4 (n_basis ~ 439) and demonstrate
convergence trend toward KS literature value `⟨P⟩(g²=1) ~ 0.55-0.60`.

Honest scope: if convergence to literature value is not achieved at
this cutoff, the higher cutoffs (Λ=2 m=5, Λ=3 m=4) document the
trend.

Date: 2026-05-07
Authority role: source-note proposal — audit verdict and downstream
status set only by independent audit lane.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from itertools import combinations, product as iproduct
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

# Import the W1.full SU(3) infrastructure (already validated)
sys.path.insert(0, str(Path(__file__).parent))
from cl3_ks_su3_rep_infrastructure_2026_05_07_w1full import (
    D_pq_batch,
    dim_su3,
    sample_su3,
    casimir_su3 as casimir_pq,
)
from cl3_ks_su3_clebsch_gordan_2026_05_07_w1full import n_invariant
from cl3_ks_full_spinnet_geometry_2026_05_07_w1full import (
    LINK_KEYS,
    VERTEX_KEYS,
    VERTEX_INCIDENT,
    PLAQUETTE_KEYS,
    PLAQUETTE_BOUNDARY,
    encode_link_config,
    decode_link_config,
)
PLAQUETTES = [PLAQUETTE_BOUNDARY[k] for k in PLAQUETTE_KEYS]


def fl():
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# Vertex intertwiner Q via matrix-free Lanczos
# ---------------------------------------------------------------------------

def _D_at_leg(samples, lam, dirn):
    """D^lam(U) or D^lam(U)^* depending on direction."""
    D = D_pq_batch(samples, *lam)
    return D if dirn == +1 else np.conj(D)


def build_vertex_Q_matrixfree(legs_with_dir, n_inv_expected, N_haar=200,
                               seed=42):
    """Build orthonormal Q via matrix-free Lanczos.

    P_inv = (1/N_haar) Σ_g (⊗_legs D^lam(g))

    Acts on v of shape (d_1, d_2, ..., d_k):
        (P_inv v)[i_1, ..., i_k] = (1/N) Σ_g Σ_{j_1, ..., j_k}
                                    Π_a D^lam_a(g)[i_a, j_a] v[j_1, ..., j_k]

    Tensor-product matvec via einsum, never materialises the full P_inv.

    Algorithm:
        - Use scipy.sparse.linalg.eigsh as a LinearOperator
        - Find the top `n_inv_expected` eigenvalues (which should be ≈ 1
          for invariant subspace, 0 for non-invariant)
        - Eigenvectors give Q

    Falls back to dense eigh for small total-dim cases.
    """
    leg_dims = [dim_su3(*lam) for lam, _ in legs_with_dir]
    D_total = int(np.prod(leg_dims))

    if n_inv_expected == 0:
        return np.zeros((D_total, 0), dtype=complex)

    # For small dim, use dense eigh (faster for small matrices)
    if D_total <= 256:
        samples = sample_su3(N_haar, seed=seed)
        D_legs = [_D_at_leg(samples, lam, dirn) for (lam, dirn) in legs_with_dir]
        T = D_legs[0]
        for D in D_legs[1:]:
            a = T.shape[1]
            d = D.shape[1]
            T = (T[:, :, None, :, None] * D[:, None, :, None, :]).reshape(
                T.shape[0], a * d, a * d
            )
        P_inv = np.mean(T, axis=0)
        P_inv = 0.5 * (P_inv + np.conj(P_inv.T))
        evals, evecs = np.linalg.eigh(P_inv)
        Q = evecs[:, -n_inv_expected:]
    else:
        # Matrix-free Lanczos for D_total > 256
        samples = sample_su3(N_haar, seed=seed)
        D_legs = [_D_at_leg(samples, lam, dirn) for (lam, dirn) in legs_with_dir]
        # Each D_legs[a] has shape (N_haar, d_a, d_a)

        def matvec(v_flat):
            """Apply P_inv to v_flat, returning result_flat."""
            v = v_flat.reshape(*leg_dims)
            # For each Haar sample g: result_g = ⊗_legs D^lam_a(g) · v
            # then average over g.
            result = np.zeros_like(v, dtype=complex)
            for g_idx in range(N_haar):
                w = v.copy()
                for a, leg_dim in enumerate(leg_dims):
                    D_a = D_legs[a][g_idx]  # shape (d_a, d_a)
                    # Apply D_a to axis a of w
                    w = np.tensordot(D_a, w, axes=([1], [a]))
                    # tensordot moves the contracted axis to position 0
                    # Move it back to position a
                    w = np.moveaxis(w, 0, a)
                result += w
            result /= N_haar
            return result.flatten()

        op = spla.LinearOperator(
            shape=(D_total, D_total),
            matvec=matvec,
            dtype=complex,
        )
        # Find top n_inv eigenvalues + a safety margin
        k = min(n_inv_expected + 2, D_total - 1)
        try:
            evals, evecs = spla.eigsh(op, k=k, which='LA',
                                       maxiter=200, tol=1e-8)
        except spla.ArpackNoConvergence as e:
            # Use whatever converged
            evals = e.eigenvalues
            evecs = e.eigenvectors

        # Take top n_inv eigenvalues (Lanczos returns sorted ascending)
        # Sort descending
        idx = np.argsort(-evals)
        Q = evecs[:, idx[:n_inv_expected]]

    # Refine via second Haar projection
    samples2 = sample_su3(2 * N_haar, seed=seed + 1)
    D_legs2 = [_D_at_leg(samples2, lam, dirn) for (lam, dirn) in legs_with_dir]

    if D_total <= 256:
        T2 = D_legs2[0]
        for D in D_legs2[1:]:
            a = T2.shape[1]
            d = D.shape[1]
            T2 = (T2[:, :, None, :, None] * D[:, None, :, None, :]).reshape(
                T2.shape[0], a * d, a * d
            )
        Q_avg = np.mean(np.einsum('nij,jk->nik', T2, Q), axis=0)
    else:
        # Matrix-free refinement
        Q_avg = np.zeros_like(Q)
        for col in range(Q.shape[1]):
            v = Q[:, col].reshape(*leg_dims)
            avg = np.zeros_like(v, dtype=complex)
            for g_idx in range(2 * N_haar):
                w = v.copy()
                for a, leg_dim in enumerate(leg_dims):
                    D_a = D_legs2[a][g_idx]
                    w = np.tensordot(D_a, w, axes=([1], [a]))
                    w = np.moveaxis(w, 0, a)
                avg += w
            avg /= (2 * N_haar)
            Q_avg[:, col] = avg.flatten()

    Q_clean, _ = np.linalg.qr(Q_avg)
    return Q_clean[:, :n_inv_expected]


_VQ_CACHE = {}


def cached_Q(legs_with_dir, n_inv, N_haar=200):
    key = tuple(legs_with_dir)
    if key not in _VQ_CACHE:
        _VQ_CACHE[key] = build_vertex_Q_matrixfree(
            legs_with_dir, n_inv, N_haar=N_haar,
            seed=42 + (hash(key) % 10000)
        )
    return _VQ_CACHE[key]


_NINV_CACHE = {}


def vertex_n_inv(legs_with_dir):
    key = tuple(legs_with_dir)
    if key not in _NINV_CACHE:
        irreps = []
        for (p, q), dirn in legs_with_dir:
            irreps.append((p, q) if dirn == +1 else (q, p))
        _NINV_CACHE[key] = n_invariant(irreps)
    return _NINV_CACHE[key]


def legs_at(link_irreps, v):
    return tuple((link_irreps[link], dirn)
                  for (link, dirn) in VERTEX_INCIDENT[v])


# ---------------------------------------------------------------------------
# Spin-network basis (matches v4 logic; just imports infrastructure)
# ---------------------------------------------------------------------------

class SpinNetworkBasisExact:
    """Spin-network basis with active-link truncation."""

    def __init__(self, irrep_cutoff, max_active=4, max_basis_dim=2000,
                 N_haar_inv=200, verbose=True):
        self.irrep_cutoff = irrep_cutoff
        self.max_active = max_active
        self.max_basis_dim = max_basis_dim
        self.N_haar_inv = N_haar_inv

        self.irreps = []
        for p in range(irrep_cutoff + 1):
            for q in range(irrep_cutoff + 1):
                if p + q <= irrep_cutoff:
                    self.irreps.append((p, q))
        self.nontriv_irreps = [lam for lam in self.irreps if lam != (0, 0)]

        if verbose:
            print(f"  Basis: irreps p+q ≤ {irrep_cutoff} ({len(self.irreps)} irreps), "
                  f"max_active = {max_active}")
            print(f"    irreps: {self.irreps}")
            fl()

        self.configs = []
        self.flat_index = []
        self._enumerate(verbose=verbose)

    def _enumerate(self, verbose=True):
        n_basis_total = 0
        for n_act in range(0, self.max_active + 1):
            if n_basis_total >= self.max_basis_dim:
                break
            if verbose:
                print(f"    Trying n_active = {n_act}...")
                fl()

            for active_links in combinations(LINK_KEYS, n_act):
                for assignment in iproduct(self.nontriv_irreps, repeat=n_act):
                    link_irreps = {l: (0, 0) for l in LINK_KEYS}
                    for link, lam in zip(active_links, assignment):
                        link_irreps[link] = lam

                    vertex_n_invs = []
                    valid = True
                    for v in VERTEX_KEYS:
                        legs = legs_at(link_irreps, v)
                        n_inv = vertex_n_inv(legs)
                        if n_inv == 0:
                            valid = False
                            break
                        vertex_n_invs.append(n_inv)
                    if not valid:
                        continue

                    n_states = int(np.prod(vertex_n_invs))
                    if n_basis_total + n_states > self.max_basis_dim:
                        if verbose:
                            print(f"    Stopped at n_active={n_act}: "
                                  f"basis dim cap {self.max_basis_dim} reached")
                            fl()
                        return

                    config = encode_link_config(link_irreps)
                    self.configs.append((config, vertex_n_invs, n_states))
                    for s in range(n_states):
                        self.flat_index.append((len(self.configs) - 1, s))
                    n_basis_total += n_states

        if verbose:
            print(f"  Configs enumerated: {len(self.configs)}, "
                  f"basis dim: {n_basis_total}")
            fl()

    @property
    def n_total(self):
        return len(self.flat_index)


# ---------------------------------------------------------------------------
# Wavefunction evaluation (reuses v4 logic — see W1.full v4 file)
# ---------------------------------------------------------------------------

def evaluate_wavefunctions(basis, link_samples, verbose=True):
    """Evaluate Ψ_α at samples for all states α."""
    N_samples = next(iter(link_samples.values())).shape[0]
    Psi = np.zeros((basis.n_total, N_samples), dtype=complex)

    unique_lams = {link: set() for link in LINK_KEYS}
    for c, _, _ in basis.configs:
        link_irreps = decode_link_config(c)
        for link, lam in link_irreps.items():
            unique_lams[link].add(lam)
    D_cache = {}
    for link in LINK_KEYS:
        for lam in unique_lams[link]:
            D_cache[(link, lam)] = D_pq_batch(link_samples[link], *lam)

    if verbose:
        print(f"    D-matrix cache: {len(D_cache)} entries")
        fl()

    config_Qs = []
    t_q = time.time()
    for cidx, (c, vertex_n_invs, n_states) in enumerate(basis.configs):
        link_irreps = decode_link_config(c)
        Qs = []
        for v_idx, v in enumerate(VERTEX_KEYS):
            legs = legs_at(link_irreps, v)
            Q = cached_Q(legs, vertex_n_invs[v_idx], N_haar=basis.N_haar_inv)
            Qs.append(Q)
        config_Qs.append(Qs)
        if verbose and cidx > 0 and cidx % 50 == 0:
            elapsed = time.time() - t_q
            avg = elapsed / cidx
            est = avg * len(basis.configs)
            print(f"      Q-build ({cidx}/{len(basis.configs)} configs in "
                  f"{elapsed:.1f}s; est total {est:.1f}s, "
                  f"VQ_cache size {len(_VQ_CACHE)})")
            fl()

    if verbose:
        print(f"    Q-build: {time.time() - t_q:.1f}s, "
              f"{len(_VQ_CACHE)} unique vertex Q matrices")
        fl()

    config_starts = {}
    for fi, (cidx, _) in enumerate(basis.flat_index):
        if cidx not in config_starts:
            config_starts[cidx] = fi

    if verbose:
        print(f"    Evaluating wavefunctions for {len(basis.configs)} configs...")
        fl()
    t0 = time.time()
    path_cache = {}
    for cidx, (c, vertex_n_invs, n_states) in enumerate(basis.configs):
        link_irreps = decode_link_config(c)

        if all(lam == (0, 0) for lam in c):
            Psi[config_starts[cidx]:config_starts[cidx] + n_states, :] = 1.0
            continue

        active_links = [link for link in LINK_KEYS if link_irreps[link] != (0, 0)]
        ops = []
        subscripts = []
        char_pool = list("abcdefghijklmopqrstuvwxyzABCDEFGHIJKLMOPQRSTUVWXYZ")
        chars_used = 0

        def take_char():
            nonlocal chars_used
            cc = char_pool[chars_used]
            chars_used += 1
            return cc

        link_src = {}
        link_sink = {}
        for link in active_links:
            link_src[link] = take_char()
            link_sink[link] = take_char()
        v_letters = [take_char() for _ in range(4)]

        for link in active_links:
            D = D_cache[(link, link_irreps[link])]
            ops.append(D)
            subscripts.append('N' + link_src[link] + link_sink[link])

        for v_idx, v in enumerate(VERTEX_KEYS):
            legs = legs_at(link_irreps, v)
            leg_dims = [dim_su3(*lam) for lam, _ in legs]
            Q = config_Qs[cidx][v_idx]
            Q_tensor = Q.reshape(*leg_dims, vertex_n_invs[v_idx])

            kept_axes = []
            kept_leg_subs = []
            for li, (link, dirn) in enumerate(VERTEX_INCIDENT[v]):
                if link_irreps[link] != (0, 0):
                    if dirn == +1:
                        kept_leg_subs.append(link_src[link])
                    else:
                        kept_leg_subs.append(link_sink[link])
                    kept_axes.append(li)

            if not kept_axes:
                Q_squeezed = Q_tensor.squeeze()
                if Q_squeezed.ndim == 0:
                    Q_squeezed = Q_squeezed[None]
                ops.append(Q_squeezed)
                subscripts.append(v_letters[v_idx])
            else:
                squeeze_axes = [li for li in range(len(VERTEX_INCIDENT[v]))
                                  if li not in kept_axes]
                Q_squeezed = Q_tensor
                for ax in sorted(squeeze_axes, reverse=True):
                    Q_squeezed = Q_squeezed.squeeze(axis=ax)
                ops.append(Q_squeezed)
                subscripts.append(''.join(kept_leg_subs) + v_letters[v_idx])

        output = 'N' + ''.join(v_letters)
        einsum_str = ','.join(subscripts) + '->' + output
        path_key = (einsum_str, tuple(o.shape for o in ops))
        if path_key not in path_cache:
            path_cache[path_key], _ = np.einsum_path(
                einsum_str, *ops, optimize='greedy'
            )
        result = np.einsum(einsum_str, *ops, optimize=path_cache[path_key])
        n_states_actual = int(np.prod(vertex_n_invs))
        Psi[config_starts[cidx]:config_starts[cidx] + n_states_actual, :] \
            = result.reshape(N_samples, n_states_actual).T

        if verbose and cidx > 0 and cidx % 50 == 0:
            elapsed = time.time() - t0
            avg = elapsed / cidx
            est = avg * len(basis.configs)
            print(f"      Ψ-eval ({cidx}/{len(basis.configs)} configs in "
                  f"{elapsed:.1f}s; est total {est:.1f}s)")
            fl()

    if verbose:
        print(f"    Ψ-eval: {time.time() - t0:.1f}s")
        fl()
    return Psi


# ---------------------------------------------------------------------------
# Build H, sparse-eigsh ground state, expectation values
# ---------------------------------------------------------------------------

def build_H_and_diag_sparse(basis, g_squared, link_samples, verbose=True,
                              N_c=3):
    """Build H via MC matrix elements; sparse eigsh for ground state."""
    if verbose:
        print(f"  Evaluating wavefunctions...")
        fl()
    Psi = evaluate_wavefunctions(basis, link_samples, verbose=verbose)
    n = basis.n_total
    N_samples = Psi.shape[1]
    if verbose:
        print(f"  Psi shape: {Psi.shape}, building MC matrix elements...")
        fl()

    # Gram (matching v4 convention: Gram[α,β] = ⟨Ψ_α|Ψ_β⟩_MC)
    Gram = (np.conj(Psi) @ Psi.T) / N_samples

    # Magnetic operator (matching v4 convention)
    plaq_traces_dict = {}
    M_values = np.zeros(N_samples)
    for pidx, (plaq_key, plaq_boundary) in enumerate(
            zip(PLAQUETTE_KEYS, PLAQUETTES)):
        U_p = None
        for link_key, dirn in plaq_boundary:
            U_link = link_samples[link_key]
            if dirn == -1:
                U_link = np.conj(U_link.transpose(0, 2, 1))
            U_p = U_link if U_p is None else np.einsum('nij,njk->nik',
                                                         U_p, U_link)
        plaq_traces_dict[plaq_key] = np.trace(U_p, axis1=1, axis2=2).real
        M_values += plaq_traces_dict[plaq_key]
    M_values *= -1.0 / (g_squared * N_c)
    H_mag = (np.conj(Psi) * M_values[np.newaxis, :]) @ Psi.T / N_samples

    # Casimir term: H_C[α,β] = (g²/2) Σ_e C_2(λ_e) Gram[α,β] for matching basis
    cas_per_config = np.array([
        sum(casimir_pq(*lam) for lam in decode_link_config(c).values())
        for c, _, _ in basis.configs
    ])
    cas_per_state = np.zeros(basis.n_total)
    for fi, (cidx, _) in enumerate(basis.flat_index):
        cas_per_state[fi] = cas_per_config[cidx]
    H_C = (g_squared / 2.0) * Gram * cas_per_state[np.newaxis, :]

    H = H_C + H_mag
    H = 0.5 * (H + np.conj(H.T))
    Gram = 0.5 * (Gram + np.conj(Gram.T))

    # Build plaq_traces array for expectation_P
    plaq_traces = np.array([plaq_traces_dict[k] for k in PLAQUETTE_KEYS])

    if verbose:
        print(f"  H shape: {H.shape}, calling sparse eigsh...")
        fl()
    # Generalized eigenvalue: H ψ = λ Gram ψ
    # Use dense eigh on (Gram^-1/2 H Gram^-1/2) — better numerical stability
    # than sparse for small n
    g_evals, g_evecs = np.linalg.eigh(Gram)
    tol = max(1e-8, g_evals.max() * 1e-12)
    keep = g_evals > tol
    g_inv_sqrt = np.zeros_like(g_evals)
    g_inv_sqrt[keep] = 1.0 / np.sqrt(g_evals[keep])
    P = g_evecs[:, keep] * g_inv_sqrt[keep][np.newaxis, :]
    H_orth = np.conj(P.T) @ H @ P
    H_orth = 0.5 * (H_orth + np.conj(H_orth.T))
    n_kept = H_orth.shape[0]
    if n_kept > 100:
        # Sparse eigsh for 6 lowest eigenvalues
        H_orth_sp = sp.csr_matrix(H_orth)
        try:
            evals_orth, evecs_orth = spla.eigsh(H_orth_sp, k=min(6, n_kept - 1),
                                                  which='SA', tol=1e-9,
                                                  maxiter=3000)
            idx = np.argsort(evals_orth)
            evals_orth = evals_orth[idx]
            evecs_orth = evecs_orth[:, idx]
        except Exception:
            evals_orth, evecs_orth = np.linalg.eigh(H_orth)
    else:
        evals_orth, evecs_orth = np.linalg.eigh(H_orth)
    evecs = P @ evecs_orth
    return evals_orth, evecs, n_kept, plaq_traces, Psi


def expectation_P(psi, Psi, plaq_traces, N_c=3):
    psi_at = np.conj(psi) @ Psi
    norm = np.mean(np.abs(psi_at) ** 2)
    P_per_sample = np.real(plaq_traces).mean(axis=0) / N_c
    return float(np.mean(np.abs(psi_at) ** 2 * P_per_sample) / norm)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run_one(g_squared, irrep_cutoff, max_active, N_samples=4000,
            seed=11, max_basis_dim=2000, N_haar_inv=200, verbose=True):
    print(f"\n--- W1.exact: g²={g_squared}, Λ={irrep_cutoff}, "
          f"max_active={max_active}, N={N_samples} ---")
    fl()
    t0 = time.time()
    rng = np.random.default_rng(seed)
    link_samples = {}
    for link in LINK_KEYS:
        link_samples[link] = sample_su3(N_samples, seed=int(rng.integers(0, 10**8)))

    basis = SpinNetworkBasisExact(irrep_cutoff=irrep_cutoff,
                                    max_active=max_active,
                                    max_basis_dim=max_basis_dim,
                                    N_haar_inv=N_haar_inv,
                                    verbose=verbose)
    if basis.n_total == 0:
        return None
    evals, evecs, n_kept, plaq_traces, Psi = build_H_and_diag_sparse(
        basis, g_squared, link_samples, verbose=verbose
    )
    psi0 = evecs[:, 0]
    P = expectation_P(psi0, Psi, plaq_traces)

    runtime = time.time() - t0
    print(f"  E_0 = {evals[0]:.4f}  (kept {n_kept}/{basis.n_total})")
    print(f"  ⟨P⟩_avg = {P:.4f}")
    print(f"  Runtime: {runtime:.1f}s, "
          f"VQ cache: {len(_VQ_CACHE)} unique shapes")
    fl()
    return {
        'g²': g_squared,
        'irrep_cutoff': irrep_cutoff,
        'max_active': max_active,
        'N_samples': N_samples,
        'n_basis': basis.n_total,
        'n_kept': n_kept,
        'E_0': float(evals[0]),
        'P_avg': P,
        'runtime_s': runtime,
        'n_vertex_Q_unique': len(_VQ_CACHE),
    }


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--mode', default='quick',
                    choices=['quick', 'sweep_max_active', 'sweep_irrep',
                             'sweep_g', 'lambda2_max4'])
    p.add_argument('--N', type=int, default=4000)
    p.add_argument('--irrep_cutoff', type=int, default=1)
    p.add_argument('--max_active', type=int, default=4)
    p.add_argument('--g2', type=float, default=1.0)
    p.add_argument('--max_basis_dim', type=int, default=2000)
    args = p.parse_args()

    if args.mode == 'quick':
        # Sanity: reproduces W1.full v4 result at Λ=1, max_active=4, g²=1
        r = run_one(g_squared=1.0, irrep_cutoff=1, max_active=4,
                    N_samples=4000, max_basis_dim=200)
        print(f"\nSanity-check (should reproduce W1.full v4: ⟨P⟩ ≈ 0.023):")
        print(f"  ⟨P⟩(g²=1, Λ=1, max_active=4) = {r['P_avg']:.4f}")
    elif args.mode == 'lambda2_max4':
        # The W1.full compute frontier — does the matrix-free Lanczos break it?
        print("=" * 70)
        print("W1.exact lambda2_max4: testing if matrix-free Lanczos breaks the")
        print("compute frontier at Λ=2, max_active=4 (W1.full was blocked here)")
        print("=" * 70)
        for cfg in [(1, 4), (2, 2), (2, 3), (2, 4)]:
            cutoff, m_act = cfg
            r = run_one(g_squared=1.0, irrep_cutoff=cutoff, max_active=m_act,
                        N_samples=args.N, max_basis_dim=args.max_basis_dim)
            if r is None:
                print(f"  Λ={cutoff}, max_active={m_act}: skipped")
                continue
            print(f"\n  Λ={cutoff}, max_active={m_act}: ⟨P⟩={r['P_avg']:.4f}, "
                  f"basis_dim={r['n_basis']}, runtime={r['runtime_s']:.1f}s, "
                  f"n_VQ={r['n_vertex_Q_unique']}")
    elif args.mode == 'sweep_g':
        cutoff, m_act = args.irrep_cutoff, args.max_active
        results = []
        for g2 in [0.5, 0.75, 1.0, 1.5, 2.0]:
            r = run_one(g_squared=g2, irrep_cutoff=cutoff, max_active=m_act,
                        N_samples=args.N, max_basis_dim=args.max_basis_dim)
            if r is not None:
                results.append(r)
        print(f"\n=== Coupling sweep at Λ={cutoff}, max_active={m_act} ===")
        print(f"{'g²':>6}  {'⟨P⟩':>8}  {'E_0':>10}  {'n_basis':>8}  {'time(s)':>8}")
        for r in results:
            print(f"{r['g²']:>6.2f}  {r['P_avg']:>8.4f}  {r['E_0']:>10.4f}  "
                   f"{r['n_basis']:>8d}  {r['runtime_s']:>8.1f}")
