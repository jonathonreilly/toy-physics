"""
Full SU(3) spin-network exact diagonalization on 2x2 spatial torus.
Version W1.exactv2: loop-supporting active-link enumeration.

Authority role
--------------
Source-note proposal -- audit verdict and downstream status set only by
the independent audit lane.

Strategy (over W1.exact)
========================
The W1.exact runner broke the W1.full Lambda=2, max_active=4 frontier
via:
  1. Bug fix in expectation_P (psi -> Psi multiplication, not conj(psi))
  2. Permutation-canonical vertex Q caching
  3. Random-vector injection for high-D invariant subspace projection
  4. Closed-form Haar-refinement loop on Q

The new bottleneck is BASIS ENUMERATION: at Lambda=3, M=4 the raw config
count exceeds 140000, with most configs forbidden by vertex gauge
invariance (n_inv = 0 at some vertex).

The W1.exactv2 runner adds:

  Path A: Loop-supporting active-link enumeration. We pre-filter the
    C(8, M) tuples of active links to "loop-supporting" subsets
    (every vertex visited even number of times by active links).
    Vertex gauge invariance forces this: configurations whose active
    links don't form closed loops have n_inv = 0 at the vertex visited
    an odd number of times (cannot fuse fundamental in trivial leg
    presence).

  Casimir cap: optional total-Casimir threshold to prune high-irrep
    configs at large Lambda.

Implementation
==============
"""

from __future__ import annotations

import sys
import time
import json
import os
from itertools import product as iproduct, combinations

import numpy as np
from numpy.linalg import eigh

# Add scripts directory to path for module imports
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from cl3_ks_su3_rep_infrastructure_2026_05_07_w1full import (
    casimir_su3,
    dim_su3,
    sample_su3,
    D_pq_batch,
    conjugate,
)
from cl3_ks_su3_clebsch_gordan_2026_05_07_w1full import (
    n_invariant,
    tensor_decomp,
)
from cl3_ks_full_spinnet_geometry_2026_05_07_w1full import (
    LINK_KEYS,
    PLAQUETTE_KEYS,
    PLAQUETTE_BOUNDARY,
    VERTEX_KEYS,
    VERTEX_INCIDENT,
    decode_link_config,
)


def fl():
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# Loop-supporting active-link enumeration (Path A)
# ---------------------------------------------------------------------------
#
# Vertex gauge invariance forces every admissible configuration to have all
# active links forming a 1-cycle (Eulerian subgraph). Each vertex must have
# an EVEN number of incident active links.

def vertex_degrees(active_links):
    """Compute degree of each vertex in the subgraph spanned by active_links."""
    deg = {v: 0 for v in VERTEX_KEYS}
    for link in active_links:
        for v, incs in VERTEX_INCIDENT.items():
            for l, _ in incs:
                if l == link:
                    deg[v] += 1
    return deg


def is_loop_supporting(active_links):
    """Return True if every vertex has even degree in active_links subgraph."""
    deg = vertex_degrees(active_links)
    return all(d % 2 == 0 for d in deg.values())


def enumerate_loop_supporting_subsets(max_active):
    """Enumerate all loop-supporting subsets of LINK_KEYS with size <= max_active.

    Returns list of tuples of link keys, sorted by size."""
    out = []
    for n_act in range(0, max_active + 1):
        for subset in combinations(LINK_KEYS, n_act):
            if is_loop_supporting(subset):
                out.append(subset)
    return out


# ---------------------------------------------------------------------------
# Vertex intertwiner via Haar projection (with caching, refinement)
# ---------------------------------------------------------------------------

def _D_at_leg(samples, lam, dirn):
    D = D_pq_batch(samples, *lam)
    return D if dirn == +1 else np.conj(D)


def build_vertex_Q(legs_with_dir, n_inv_expected, N_haar=200, seed=42,
                   refine_passes=4):
    """Build orthonormal basis Q for invariant subspace at vertex.

    Uses random-vector injection for D_total > 256 then Haar refinement.
    """
    if n_inv_expected == 0:
        D_total = 1
        for lam, _ in legs_with_dir:
            D_total *= dim_su3(*lam)
        return np.zeros((D_total, 0), dtype=complex)

    D_total = 1
    for lam, _ in legs_with_dir:
        D_total *= dim_su3(*lam)

    if D_total <= 256:
        # Cheap dense eigh path
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
        # Random-vector injection: build invariant subspace via Haar projection
        # of n_inv random column vectors.
        rng = np.random.default_rng(seed)
        Z = rng.standard_normal((D_total, n_inv_expected)) + \
            1j * rng.standard_normal((D_total, n_inv_expected))
        Q = Z / np.linalg.norm(Z, axis=0)[np.newaxis, :]

        # Haar projection of Q: Q -> mean(D_legs ⊗ ... Q over Haar)
        for pass_idx in range(refine_passes):
            samples = sample_su3(N_haar, seed=seed + 100 * (pass_idx + 1))
            D_legs = [_D_at_leg(samples, lam, dirn) for (lam, dirn) in legs_with_dir]

            leg_dims = [D.shape[1] for D in D_legs]
            Q_T = Q.reshape(*leg_dims, n_inv_expected)

            # For each sample, contract D_legs[i] with axis i. Average over samples.
            Q_avg = np.zeros_like(Q_T)
            for s_idx in range(N_haar):
                Q_temp = Q_T
                for li, D in enumerate(D_legs):
                    Q_temp = np.tensordot(D[s_idx], Q_temp, axes=[[1], [li]])
                    perm = list(range(Q_temp.ndim))
                    perm.pop(0)
                    perm.insert(li, 0)
                    Q_temp = np.transpose(Q_temp, perm)
                Q_avg = Q_avg + Q_temp
            Q_avg = Q_avg / N_haar

            Q_avg = Q_avg.reshape(D_total, n_inv_expected)
            Q_clean, _ = np.linalg.qr(Q_avg)
            Q = Q_clean[:, :n_inv_expected]

    return Q


_VQ_CACHE = {}
_NINV_CACHE = {}


def canonical_legs_key(legs_with_dir):
    """Sort legs by (lam[0], lam[1], dirn) for permutation-canonical caching."""
    indexed = sorted(enumerate(legs_with_dir),
                     key=lambda x: (x[1][0][0], x[1][0][1], x[1][1]))
    perm = tuple(i for i, _ in indexed)
    sorted_legs = tuple(legs_with_dir[i] for i in perm)
    return sorted_legs, perm


def cached_Q(legs_with_dir, n_inv, N_haar=200):
    """Cached, permutation-canonical vertex Q."""
    sorted_legs, perm = canonical_legs_key(legs_with_dir)
    key = sorted_legs
    if key not in _VQ_CACHE:
        _VQ_CACHE[key] = build_vertex_Q(
            sorted_legs, n_inv, N_haar=N_haar,
            seed=42 + (hash(key) % 10000)
        )

    Q_canon = _VQ_CACHE[key]
    if Q_canon.shape[1] == 0:
        leg_dims_orig = [dim_su3(*lam) for lam, _ in legs_with_dir]
        return np.zeros((int(np.prod(leg_dims_orig)), 0), dtype=complex)

    leg_dims_canon = [dim_su3(*lam) for lam, _ in sorted_legs]
    n_inv_actual = Q_canon.shape[1]
    Q_T = Q_canon.reshape(*leg_dims_canon, n_inv_actual)
    inv_perm = [0] * len(perm)
    for i, p in enumerate(perm):
        inv_perm[p] = i
    new_axes = inv_perm + [len(perm)]
    Q_T_orig = np.transpose(Q_T, new_axes)
    leg_dims_orig = [dim_su3(*lam) for lam, _ in legs_with_dir]
    return Q_T_orig.reshape(int(np.prod(leg_dims_orig)), n_inv_actual)


def vertex_n_inv(legs_with_dir):
    sorted_legs, _ = canonical_legs_key(legs_with_dir)
    key = sorted_legs
    if key not in _NINV_CACHE:
        irreps = []
        for (p, q), dirn in sorted_legs:
            irreps.append((p, q) if dirn == +1 else (q, p))
        _NINV_CACHE[key] = n_invariant(irreps)
    return _NINV_CACHE[key]


def legs_at(link_irreps, v):
    return tuple((link_irreps[link], dirn)
                  for (link, dirn) in VERTEX_INCIDENT[v])


# ---------------------------------------------------------------------------
# Spin-network basis with loop-supporting active-link enumeration
# ---------------------------------------------------------------------------

class SpinNetworkBasisLoopSupp:
    """Spin-network basis with loop-supporting active-link enumeration.

    Filters configs by:
      1. Active link subset has even degree at every vertex (loop-supporting)
      2. Vertex gauge invariance (n_inv > 0 at every vertex), exact via CG.
      3. N_active <= max_active.
      4. Optional: total Casimir <= cas_cap.
    """

    def __init__(self, irrep_cutoff, max_active=4, max_basis_dim=2000,
                 cas_cap=None, N_haar_inv=200, verbose=True):
        self.irrep_cutoff = irrep_cutoff
        self.max_active = max_active
        self.max_basis_dim = max_basis_dim
        self.cas_cap = cas_cap
        self.N_haar_inv = N_haar_inv

        self.irreps = []
        for p in range(irrep_cutoff + 1):
            for q in range(irrep_cutoff + 1):
                if p + q <= irrep_cutoff:
                    self.irreps.append((p, q))

        self.nontriv_irreps = [lam for lam in self.irreps if lam != (0, 0)]

        self.loop_subsets = enumerate_loop_supporting_subsets(max_active)

        if verbose:
            print(f"  Basis: irreps p+q <= {irrep_cutoff} ({len(self.irreps)} irreps), "
                  f"max_active = {max_active}, cas_cap = {cas_cap}")
            print(f"    irreps: {self.irreps}")
            print(f"    Loop-supporting subsets up to size {max_active}: {len(self.loop_subsets)}")
            size_count = {}
            for s in self.loop_subsets:
                size_count[len(s)] = size_count.get(len(s), 0) + 1
            print(f"    by size: {dict(sorted(size_count.items()))}")
            fl()

        self.configs = []
        self.flat_index = []

        self._enumerate(verbose=verbose)

    def _enumerate(self, verbose=True):
        n_kept = 0
        n_basis_total = 0
        n_raw_attempted = 0

        for active_links in self.loop_subsets:
            n_act = len(active_links)
            if n_basis_total >= self.max_basis_dim:
                break

            for assignment in iproduct(self.nontriv_irreps, repeat=n_act):
                n_raw_attempted += 1
                link_irreps = {l: (0, 0) for l in LINK_KEYS}
                for link, lam in zip(active_links, assignment):
                    link_irreps[link] = lam

                if self.cas_cap is not None:
                    cas_total = sum(casimir_su3(*lam) for lam in link_irreps.values())
                    if cas_total > self.cas_cap:
                        continue

                vertex_n_invs = []
                valid = True
                for v in VERTEX_KEYS:
                    legs = legs_at(link_irreps, v)
                    n = vertex_n_inv(legs)
                    if n == 0:
                        valid = False
                        break
                    vertex_n_invs.append(n)
                if not valid:
                    continue

                n_states = int(np.prod(vertex_n_invs))
                if n_basis_total + n_states > self.max_basis_dim:
                    if verbose:
                        print(f"    Hit max_basis_dim={self.max_basis_dim}; "
                              f"stopping at {n_kept} configs.")
                        fl()
                    self.n_total = len(self.flat_index)
                    self.n_raw_attempted = n_raw_attempted
                    return

                c = tuple(link_irreps[k] for k in LINK_KEYS)
                self.configs.append((c, vertex_n_invs, n_states))
                for iota_tuple in iproduct(*[range(d) for d in vertex_n_invs]):
                    self.flat_index.append((len(self.configs) - 1, iota_tuple))
                n_kept += 1
                n_basis_total += n_states

        self.n_total = len(self.flat_index)
        self.n_raw_attempted = n_raw_attempted
        if verbose:
            print(f"  Final: {n_kept} configs ({n_raw_attempted} raw attempts), "
                  f"total basis dim = {self.n_total}")
            fl()


# ---------------------------------------------------------------------------
# Wavefunction evaluation
# ---------------------------------------------------------------------------

def evaluate_wavefunctions(basis, link_samples, verbose=True):
    """Evaluate Psi_alpha at samples for all states alpha."""
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
        print(f"    D-matrix cache: {sum(1 for _ in D_cache.values())} entries")
        fl()

    config_Qs = []
    t_q_total = 0.0
    n_q_built = 0
    for cidx, (c, vertex_n_invs, n_states) in enumerate(basis.configs):
        link_irreps = decode_link_config(c)
        Qs = []
        for v_idx, v in enumerate(VERTEX_KEYS):
            legs = legs_at(link_irreps, v)
            t_q0 = time.time()
            Q = cached_Q(legs, vertex_n_invs[v_idx], N_haar=basis.N_haar_inv)
            t_q_total += time.time() - t_q0
            n_q_built += 1
            Qs.append(Q)
        config_Qs.append(Qs)
        if verbose and cidx % 100 == 0 and cidx > 0:
            print(f"      Q-build progress: {cidx}/{len(basis.configs)}, "
                  f"unique Q={len(_VQ_CACHE)}, t_q={t_q_total:.1f}s")
            fl()

    if verbose:
        print(f"    Built {len(_VQ_CACHE)} unique vertex Q matrices, "
              f"{n_q_built} lookups in {t_q_total:.1f}s")
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
            ch = char_pool[chars_used]
            chars_used += 1
            return ch

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

            leg_subs = []
            kept_axes = []
            kept_leg_subs = []
            for li, (link, dirn) in enumerate(VERTEX_INCIDENT[v]):
                if link_irreps[link] == (0, 0):
                    pass
                else:
                    if dirn == +1:
                        leg_subs.append(link_src[link])
                    else:
                        leg_subs.append(link_sink[link])
                    kept_axes.append(li)
                    kept_leg_subs.append(leg_subs[-1])

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

        if verbose and cidx % 100 == 0 and cidx > 0:
            elapsed = time.time() - t0
            avg = elapsed / cidx
            est = avg * len(basis.configs)
            print(f"      ({cidx}/{len(basis.configs)} configs in {elapsed:.1f}s; "
                  f"est total {est:.1f}s)")
            fl()

    if verbose:
        print(f"    Wavefunction eval: {time.time() - t0:.1f}s total")
        fl()

    return Psi


# ---------------------------------------------------------------------------
# Build Hamiltonian and diagonalize
# ---------------------------------------------------------------------------

def build_H_and_diag(basis, g_squared, link_samples, verbose=True, N_c=3,
                     use_lanczos=False, n_lanczos=15):
    Psi = evaluate_wavefunctions(basis, link_samples, verbose=verbose)
    N_samples = next(iter(link_samples.values())).shape[0]

    if verbose:
        print(f"  Building H and Gram ({basis.n_total} basis)...")
        fl()
    t0 = time.time()

    Gram = (np.conj(Psi) @ Psi.T) / N_samples

    M_values = np.zeros(N_samples)
    plaq_traces = {}
    for plaq, boundary in PLAQUETTE_BOUNDARY.items():
        U_p = None
        for link, dirn in boundary:
            U_link = link_samples[link]
            if dirn == -1:
                U_link = np.conj(U_link.transpose(0, 2, 1))
            U_p = U_link if U_p is None else np.einsum('nij,njk->nik', U_p, U_link)
        plaq_traces[plaq] = np.trace(U_p, axis1=1, axis2=2).real
        M_values += plaq_traces[plaq]
    M_values *= -1.0 / (g_squared * N_c)
    H_mag = (np.conj(Psi) * M_values[np.newaxis, :]) @ Psi.T / N_samples

    cas_per_config = np.array([sum(casimir_su3(*lam) for lam in c)
                                 for c, _, _ in basis.configs])
    cas_per_state = np.zeros(basis.n_total)
    for fi, (cidx, _) in enumerate(basis.flat_index):
        cas_per_state[fi] = cas_per_config[cidx]
    H_C = (g_squared / 2.0) * Gram * cas_per_state[np.newaxis, :]

    H = H_C + H_mag
    H = 0.5 * (H + np.conj(H.T))
    Gram = 0.5 * (Gram + np.conj(Gram.T))
    if verbose:
        print(f"  H/Gram: {time.time() - t0:.1f}s")
        fl()

    if verbose:
        print(f"  Diagonalizing (lanczos={use_lanczos})...")
        fl()
    t0 = time.time()

    g_evals, g_evecs = eigh(Gram)
    tol = 1e-7 * max(g_evals[-1], 1e-12) if len(g_evals) > 0 else 1e-12
    keep_mask = g_evals > tol
    n_keep = int(np.sum(keep_mask))
    g_inv_sqrt = np.zeros_like(g_evals)
    g_inv_sqrt[keep_mask] = 1.0 / np.sqrt(g_evals[keep_mask])
    P_proj = g_evecs[:, keep_mask] * g_inv_sqrt[keep_mask][np.newaxis, :]
    H_orth = np.conj(P_proj.T) @ H @ P_proj
    H_orth = 0.5 * (H_orth + np.conj(H_orth.T))

    if use_lanczos and n_keep > 50:
        try:
            from scipy.sparse.linalg import eigsh
            evals_l, evecs_orth_l = eigsh(H_orth, k=min(n_lanczos, n_keep - 1),
                                           which='SA')
            order = np.argsort(evals_l.real)
            evals = evals_l[order]
            evecs_orth = evecs_orth_l[:, order]
            evals_full = np.full(n_keep, np.nan)
            evals_full[:len(evals)] = evals
        except ImportError:
            evals, evecs_orth = eigh(H_orth)
            evals_full = evals
    else:
        evals, evecs_orth = eigh(H_orth)
        evals_full = evals

    evecs = P_proj @ evecs_orth
    if verbose:
        print(f"  Diag: {time.time() - t0:.1f}s")
        fl()

    return {
        'evals': evals_full,
        'evecs': evecs,
        'Psi': Psi,
        'Gram': Gram,
        'plaq_traces': plaq_traces,
        'n_keep': n_keep,
    }


def expectation_P(psi, Psi, plaq_traces, N_c=3):
    """Corrected expectation: physical wavefunction phys(U) = psi @ Psi
    (NOT conj(psi))."""
    psi_at = psi @ Psi
    norm = np.mean(np.abs(psi_at) ** 2)
    P_total = sum(plaq_traces[p] for p in PLAQUETTE_KEYS) / (len(PLAQUETTE_KEYS) * N_c)
    return float(np.mean(np.abs(psi_at) ** 2 * P_total) / norm)


def expectation_P_per_plaq(psi, Psi, plaq_traces, N_c=3):
    psi_at = psi @ Psi
    norm = np.mean(np.abs(psi_at) ** 2)
    return [float(np.mean(np.abs(psi_at) ** 2 * plaq_traces[p] / N_c) / norm)
             for p in PLAQUETTE_KEYS]


def run_one(g_squared, irrep_cutoff, max_active=4, N_samples=4000, seed=11,
              max_basis_dim=2000, N_haar_inv=200, cas_cap=None,
              use_lanczos=False, verbose=True):
    if verbose:
        print(f"\n--- SN-ED w1exactv2, g^2={g_squared}, p+q<={irrep_cutoff}, "
              f"max_active={max_active}, cas_cap={cas_cap}, N={N_samples} ---")
        fl()
    t_total = time.time()

    basis = SpinNetworkBasisLoopSupp(
        irrep_cutoff=irrep_cutoff,
        max_active=max_active,
        max_basis_dim=max_basis_dim,
        cas_cap=cas_cap,
        N_haar_inv=N_haar_inv,
        verbose=verbose,
    )
    if basis.n_total == 0:
        return None

    link_samples = {link: sample_su3(N_samples, seed=seed + i)
                    for i, link in enumerate(LINK_KEYS)}

    result = build_H_and_diag(basis, g_squared, link_samples,
                              verbose=verbose, use_lanczos=use_lanczos)
    psi0 = result['evecs'][:, 0]
    P_avg = expectation_P(psi0, result['Psi'], result['plaq_traces'])
    P_per = expectation_P_per_plaq(psi0, result['Psi'], result['plaq_traces'])

    if verbose:
        print(f"  E_0 = {result['evals'][0].real:.6f}  ({result['n_keep']}/{basis.n_total} kept)")
        print(f"  <P>_avg = {P_avg:.6f}")
        print(f"  per-plaq P = [{P_per[0]:.4f}, {P_per[1]:.4f}, "
              f"{P_per[2]:.4f}, {P_per[3]:.4f}]")
        print(f"  Runtime: {time.time() - t_total:.1f}s")
        fl()

    return {
        'g_squared': g_squared,
        'irrep_cutoff': irrep_cutoff,
        'max_active': max_active,
        'cas_cap': cas_cap,
        'N_samples': N_samples,
        'P_avg': P_avg,
        'P_per_plaq': P_per,
        'E_0': float(result['evals'][0].real),
        'eigenvalues_5': [float(e) for e in result['evals'][:5].real],
        'n_basis': int(basis.n_total),
        'n_kept': int(result['n_keep']),
        'n_configs': len(basis.configs),
        'n_loop_subsets': len(basis.loop_subsets),
        'n_raw_attempted': basis.n_raw_attempted,
        'runtime_s': time.time() - t_total,
    }


# ---------------------------------------------------------------------------
# Main: convergence sweeps
# ---------------------------------------------------------------------------

OUTPUT_DIR = '/Users/jonreilly/Projects/Physics/.claude/worktrees/' \
              'confident-robinson-5c47a5/outputs/action_first_principles_2026_05_07/' \
              'w1exact_v2_basis_scaling'


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', default='quick',
                          choices=['quick', 'sweep_max_active', 'sweep_irrep',
                                   'sweep_g', 'single', 'frontier', 'self_test'])
    parser.add_argument('--N', type=int, default=4000)
    parser.add_argument('--max_active', type=int, default=4)
    parser.add_argument('--irrep_cutoff', type=int, default=1)
    parser.add_argument('--g_squared', type=float, default=1.0)
    parser.add_argument('--max_basis_dim', type=int, default=4000)
    parser.add_argument('--cas_cap', type=float, default=None)
    parser.add_argument('--N_haar_inv', type=int, default=200)
    parser.add_argument('--lanczos', action='store_true',
                        help='Use Lanczos for ground-state extraction')
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 72)
    print("Full SU(3) spin-network ED w1exactv2 (loop-supporting enumeration)")
    print("=" * 72)
    fl()

    if args.mode == 'self_test':
        print("\n[1] Loop-supporting subset enumeration self-test")
        for max_act in [0, 2, 4, 6, 8]:
            ls = enumerate_loop_supporting_subsets(max_act)
            size_count = {}
            for s in ls:
                size_count[len(s)] = size_count.get(len(s), 0) + 1
            print(f"  max_active = {max_act}: {len(ls)} loop-supporting subsets, "
                  f"by size: {dict(sorted(size_count.items()))}")
        ls4 = enumerate_loop_supporting_subsets(4)
        print(f"\n  Detail at max_active=4: {len(ls4)}")
        for s in ls4:
            print(f"    {len(s)}: {s}")

    elif args.mode == 'quick':
        print("\n[Quick test]")
        r0 = run_one(g_squared=1.0, irrep_cutoff=0, max_active=0,
                      N_samples=2000, max_basis_dim=10, verbose=True)
        r1 = run_one(g_squared=1.0, irrep_cutoff=1, max_active=4,
                      N_samples=2000, max_basis_dim=500, verbose=True)
        print(f"\nSummary at g^2=1:")
        print(f"  Lambda=0, max_active=0: <P> = {r0['P_avg']:.4f}, n={r0['n_basis']}")
        print(f"  Lambda=1, max_active=4: <P> = {r1['P_avg']:.4f}, n={r1['n_basis']}")

    elif args.mode == 'single':
        r = run_one(g_squared=args.g_squared, irrep_cutoff=args.irrep_cutoff,
                    max_active=args.max_active, N_samples=args.N,
                    max_basis_dim=args.max_basis_dim,
                    cas_cap=args.cas_cap, N_haar_inv=args.N_haar_inv,
                    use_lanczos=args.lanczos, verbose=True)
        if r:
            cap_str = f'_cap{args.cas_cap}' if args.cas_cap else ''
            fname = f'single_irrep{args.irrep_cutoff}_maxact{args.max_active}_g{args.g_squared}{cap_str}.json'
            with open(os.path.join(OUTPUT_DIR, fname), 'w') as f:
                json.dump(r, f, indent=2)

    elif args.mode == 'sweep_max_active':
        print(f"\n[Sweep max_active at irrep_cutoff={args.irrep_cutoff}, g^2={args.g_squared}]")
        results = []
        for ma in [0, 2, 4, 6, 8]:
            r = run_one(g_squared=args.g_squared, irrep_cutoff=args.irrep_cutoff,
                          max_active=ma, N_samples=args.N,
                          max_basis_dim=args.max_basis_dim,
                          cas_cap=args.cas_cap, N_haar_inv=args.N_haar_inv,
                          use_lanczos=args.lanczos, verbose=True)
            if r is not None:
                results.append(r)
                print(f"  max_active={ma}: <P>={r['P_avg']:.4f}, "
                      f"n_basis={r['n_basis']}, n_configs={r['n_configs']}, "
                      f"E_0={r['E_0']:.4f}, runtime={r['runtime_s']:.1f}s")
                fl()
        with open(os.path.join(OUTPUT_DIR,
                                f'sweep_max_active_cutoff{args.irrep_cutoff}.json'), 'w') as f:
            json.dump(results, f, indent=2)

    elif args.mode == 'sweep_irrep':
        print(f"\n[Sweep irrep_cutoff at max_active={args.max_active}, g^2={args.g_squared}]")
        results = []
        for cut in [1, 2, 3]:
            r = run_one(g_squared=args.g_squared, irrep_cutoff=cut,
                          max_active=args.max_active, N_samples=args.N,
                          max_basis_dim=args.max_basis_dim,
                          cas_cap=args.cas_cap, N_haar_inv=args.N_haar_inv,
                          use_lanczos=args.lanczos, verbose=True)
            if r is not None:
                results.append(r)
                print(f"  cutoff={cut}: <P>={r['P_avg']:.4f}, "
                      f"n_basis={r['n_basis']}, n_configs={r['n_configs']}, "
                      f"E_0={r['E_0']:.4f}, runtime={r['runtime_s']:.1f}s")
                fl()
        with open(os.path.join(OUTPUT_DIR,
                                f'sweep_irrep_max{args.max_active}.json'), 'w') as f:
            json.dump(results, f, indent=2)

    elif args.mode == 'sweep_g':
        print(f"\n[Sweep g^2 at irrep_cutoff={args.irrep_cutoff}, "
              f"max_active={args.max_active}]")
        results = []
        for g2 in [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]:
            r = run_one(g_squared=g2, irrep_cutoff=args.irrep_cutoff,
                          max_active=args.max_active, N_samples=args.N,
                          max_basis_dim=args.max_basis_dim,
                          cas_cap=args.cas_cap, N_haar_inv=args.N_haar_inv,
                          use_lanczos=args.lanczos, verbose=True)
            if r is not None:
                results.append(r)
                print(f"  g^2={g2:.2f}: <P>={r['P_avg']:.4f}, "
                      f"n_basis={r['n_basis']}, n_configs={r['n_configs']}, "
                      f"E_0={r['E_0']:.4f}, runtime={r['runtime_s']:.1f}s")
                fl()
        with open(os.path.join(OUTPUT_DIR,
                f'sweep_g_cutoff{args.irrep_cutoff}_max{args.max_active}.json'), 'w') as f:
            json.dump(results, f, indent=2)

    elif args.mode == 'frontier':
        print("\n[Frontier sweep]")
        results = []
        cases = [
            (1, 4, 4000, None, 'Lambda=1, M=4 baseline'),
            (1, 6, 4000, None, 'Lambda=1, M=6'),
            (2, 4, 6000, None, 'Lambda=2, M=4'),
            (3, 4, 4000, 12.0, 'Lambda=3, M=4 (cap=12)'),
        ]
        for cut, ma, mbd, cap, label in cases:
            print(f"\n  [{label}]")
            t0 = time.time()
            try:
                r = run_one(g_squared=args.g_squared, irrep_cutoff=cut,
                              max_active=ma, N_samples=args.N,
                              max_basis_dim=mbd,
                              cas_cap=cap, N_haar_inv=args.N_haar_inv,
                              use_lanczos=args.lanczos, verbose=True)
                if r is not None:
                    results.append(r)
                    print(f"    DONE in {time.time() - t0:.1f}s: <P>={r['P_avg']:.4f}, "
                          f"n_basis={r['n_basis']}")
                    fl()
            except Exception as e:
                print(f"    FAILED: {e}")
                fl()
                results.append({
                    'irrep_cutoff': cut, 'max_active': ma, 'failed': str(e),
                    'runtime_s': time.time() - t0,
                })
        with open(os.path.join(OUTPUT_DIR, 'frontier_sweep.json'), 'w') as f:
            json.dump(results, f, indent=2)
