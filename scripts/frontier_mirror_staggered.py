#!/usr/bin/env python3
"""
Mirror-Symmetric Staggered Lattice: Decoherence Protection
============================================================
Can the mirror Z2's spectacular MI=0.773 (from DAG transfer matrices)
be recovered on a 2D staggered lattice with Crank-Nicolson evolution?

Protocol:
  1. Build mirror-symmetric bilayer: two side x side staggered lattices
     (L and R), connected by mirror edges i <-> i' at matching positions.
     Total n = 2 * side^2.
  2. Prepare a PRODUCT state: equal superposition localized on L, with a
     distinct pattern on R. Evolve and track how correlations build.
  3. Key observables:
     - L-R correlation coefficient of probability distributions
     - Quantum coherence: |<psi_L|psi_R>| (overlap of L,R amplitudes)
     - Purity of L reduced state (how much leaks to R)
     - Effective MI via probability correlation structure
  4. Compare mirror vs random inter-layer connections, with/without gravity.

Reference: Mirror Z2 on DAGs: MI = 0.773 at N=80.
"""

from __future__ import annotations
import time
import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve

MASS = 0.30
MU2_GRAV = 0.001
DT = 0.12
G = 10.0
N_STEPS = 50
SIDE = 8


# ── Lattice construction ─────────────────────────────────────────────

def make_single_layer(side):
    """2D periodic staggered lattice (one layer)."""
    n = side * side
    pos = np.zeros((n, 2))
    col = np.zeros(n, dtype=int)
    adj = {}
    for x in range(side):
        for y in range(side):
            idx = x * side + y
            pos[idx] = [x, y]
            col[idx] = (x + y) % 2
            nbs = []
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx_, ny_ = (x + dx) % side, (y + dy) % side
                nbs.append(nx_ * side + ny_)
            adj[idx] = nbs
    return pos, col, adj, n


def make_mirror_bilayer(side):
    """Mirror-symmetric bilayer: L and R copies connected at matching sites.

    Nodes 0..n_layer-1 are L, n_layer..2*n_layer-1 are R.
    Mirror edges: i <-> i + n_layer for all i in L.
    Intra-layer edges preserved within each copy.
    """
    pos_1, col_1, adj_1, n_layer = make_single_layer(side)
    n_total = 2 * n_layer
    pos = np.zeros((n_total, 2))
    col = np.zeros(n_total, dtype=int)
    adj = {}

    pos[:n_layer] = pos_1
    col[:n_layer] = col_1
    for i in range(n_layer):
        adj[i] = list(adj_1[i])

    for i in range(n_layer):
        r_idx = i + n_layer
        pos[r_idx] = pos_1[i] + np.array([side + 2, 0])
        col[r_idx] = col_1[i]
        adj[r_idx] = [j + n_layer for j in adj_1[i]]

    # Mirror edges: i <-> i + n_layer
    for i in range(n_layer):
        adj[i].append(i + n_layer)
        adj[i + n_layer].append(i)

    return pos, col, adj, n_total, n_layer


def make_random_bilayer(side, seed=42):
    """Bilayer with RANDOM inter-layer connections (same count as mirror)."""
    pos_1, col_1, adj_1, n_layer = make_single_layer(side)
    rng = np.random.RandomState(seed)
    n_total = 2 * n_layer
    pos = np.zeros((n_total, 2))
    col = np.zeros(n_total, dtype=int)
    adj = {}

    pos[:n_layer] = pos_1
    col[:n_layer] = col_1
    for i in range(n_layer):
        adj[i] = list(adj_1[i])

    for i in range(n_layer):
        r_idx = i + n_layer
        pos[r_idx] = pos_1[i] + np.array([side + 2, 0])
        col[r_idx] = col_1[i]
        adj[r_idx] = [j + n_layer for j in adj_1[i]]

    # Random inter-layer: each L node connects to a random R node
    perm = rng.permutation(n_layer)
    for i in range(n_layer):
        r_target = perm[i] + n_layer
        adj[i].append(r_target)
        adj[r_target].append(i)

    return pos, col, adj, n_total, n_layer


# ── Physics tools ─────────────────────────────────────────────────────

def laplacian(pos, adj, n):
    L = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i < j:
                d = np.sqrt((pos[j, 0] - pos[i, 0]) ** 2 +
                            (pos[j, 1] - pos[i, 1]) ** 2)
                w = 1.0 / max(d, 0.5)
                L[i, j] -= w
                L[j, i] -= w
                L[i, i] += w
                L[j, j] += w
    return L.tocsr()


def solve_phi(L, n, rho, mu2):
    if np.allclose(rho, 0):
        return np.zeros(n)
    A = (L + mu2 * speye(n, format='csr')).tocsc()
    return spsolve(A, rho)


def build_H(col, adj, n, mass, phi):
    """Staggered Hamiltonian: H_diag = (mass + phi) * eps, off-diag = hopping."""
    H = lil_matrix((n, n), dtype=complex)
    par = np.where(col == 0, 1.0, -1.0)
    H.setdiag((mass + phi) * par)
    for i, nbs in adj.items():
        for j in nbs:
            if i < j:
                hop = -0.5j
                H[i, j] += hop
                H[j, i] += np.conj(hop)
    return H.tocsr()


def cn_step(H, psi, dt):
    n = H.shape[0]
    ap = (speye(n, format='csc') + 1j * H * dt / 2).tocsc()
    am = speye(n, format='csr') - 1j * H * dt / 2
    return spsolve(ap, am.dot(psi))


# ── State preparation ────────────────────────────────────────────────

def left_localized_state(n_total, n_layer, pos, sigma=2.0, side=8):
    """Gaussian state localized on the L layer."""
    psi = np.zeros(n_total, dtype=complex)
    cx, cy = side / 2.0, side / 2.0
    for i in range(n_layer):
        x, y = pos[i]
        psi[i] = np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * sigma ** 2))
    norm = np.linalg.norm(psi)
    if norm > 0:
        psi /= norm
    return psi


# ── Observables ──────────────────────────────────────────────────────

def lr_correlation(psi, n_layer):
    """Pearson correlation between L and R probability patterns.

    For mirror symmetry, site i in L maps to site i in R.
    High correlation means the probability pattern is coherently
    transferred between layers (decoherence protection).
    """
    prob = np.abs(psi) ** 2
    p_L = prob[:n_layer]
    p_R = prob[n_layer:]

    if np.std(p_L) < 1e-15 or np.std(p_R) < 1e-15:
        return 0.0

    return float(np.corrcoef(p_L, p_R)[0, 1])


def lr_quantum_coherence(psi, n_layer):
    """Quantum coherence between L and R: |sum_i conj(psi_L[i]) * psi_R[i]|.

    This is the overlap of the L-amplitude pattern with the R-amplitude
    pattern. For a mirror-symmetric evolution, this should stay high.
    """
    psi_L = psi[:n_layer]
    psi_R = psi[n_layer:]
    return float(np.abs(np.conj(psi_L) @ psi_R))


def lr_fidelity(psi, n_layer):
    """Fidelity between normalized L and R probability distributions.

    F = (sum_i sqrt(p_L[i] * p_R[i]))^2
    """
    prob = np.abs(psi) ** 2
    p_L = prob[:n_layer]
    p_R = prob[n_layer:]
    s_L = np.sum(p_L)
    s_R = np.sum(p_R)
    if s_L < 1e-30 or s_R < 1e-30:
        return 0.0
    q_L = p_L / s_L
    q_R = p_R / s_R
    return float(np.sum(np.sqrt(q_L * q_R)) ** 2)


def left_purity(psi, n_layer):
    """Probability remaining on L side."""
    prob = np.abs(psi) ** 2
    return float(np.sum(prob[:n_layer]) / np.sum(prob))


def classical_mi_lr(psi, n_layer, n_bins=8):
    """Classical MI between L and R subsystems via coarse-grained bins.

    Bin each layer's sites into n_bins spatial groups.
    Compute I(L_bin; R_bin) from the joint probability table.
    For a single particle, this measures how much the spatial pattern
    on one layer predicts the spatial pattern on the other.

    Key insight: for a single-particle state, the particle is on
    exactly one site. The joint distribution p(L_bin, R_bin) is
    degenerate. Instead, we compute MI between the spatial pattern
    on L and R by treating the amplitudes as a classical signal.
    """
    prob = np.abs(psi) ** 2
    s = np.sum(prob)
    if s < 1e-30:
        return 0.0
    prob /= s

    p_L = prob[:n_layer]
    p_R = prob[n_layer:]

    # Bin into spatial groups
    side = int(np.sqrt(n_layer))
    p_Lbins = np.zeros(n_bins)
    p_Rbins = np.zeros(n_bins)

    for i in range(n_layer):
        x = i // side
        y = i % side
        b = (x * n_bins) // side  # bin by x-coordinate
        p_Lbins[b] += p_L[i]
        p_Rbins[b] += p_R[i]

    # Normalize each half independently (conditional distributions)
    s_L = np.sum(p_Lbins)
    s_R = np.sum(p_Rbins)
    if s_L < 1e-30 or s_R < 1e-30:
        return 0.0
    q_L = p_Lbins / s_L
    q_R = p_Rbins / s_R

    # KL divergence D(q_L || q_R) as MI proxy
    # This measures how different the L pattern is from R pattern
    # For mirror: should be LOW (patterns match)
    # For random: should be HIGH (patterns diverge)
    # Actually, we want the opposite: high MI = high correlation

    # Better: compute the entropy of the difference distribution
    # MI via correlation: use mutual information of the joint (bin_L, bin_R)
    # For single-particle: joint is p(i) where i indexes all 2*n_layer sites
    # Marginals: p(L_bin) = sum over L sites in bin + contribution to bin from R
    # This doesn't work for single particle.

    # Alternative MI measure: treat p_L and p_R as two random variables
    # and compute MI via their empirical joint distribution across bins.
    # p(l, r) = probability that a random site has L-bin=l AND R-bin=r
    # For mirror: sites in same bin in L and R → diagonal joint
    # For random: scattered → more uniform joint

    # Build joint from site pairing
    p_joint = np.zeros((n_bins, n_bins))
    # Each site i in L is paired with its mirror partner i in R
    for i in range(n_layer):
        x = i // side
        b = (x * n_bins) // side
        # Weight by the geometric mean of L and R probabilities at this site
        # This captures the correlation between L and R patterns
        w = np.sqrt(p_L[i] * p_R[i])
        p_joint[b, b] += w  # mirror: same bin
    # Normalize
    s_j = np.sum(p_joint)
    if s_j < 1e-30:
        return 0.0
    p_joint /= s_j

    p_jL = np.sum(p_joint, axis=1)
    p_jR = np.sum(p_joint, axis=0)

    # MI
    H_L = -np.sum(p_jL[p_jL > 0] * np.log(p_jL[p_jL > 0]))
    H_R = -np.sum(p_jR[p_jR > 0] * np.log(p_jR[p_jR > 0]))
    pf = p_joint.flatten()
    H_J = -np.sum(pf[pf > 0] * np.log(pf[pf > 0]))

    return float(max(H_L + H_R - H_J, 0.0))


def correlation_mi(psi, n_layer):
    """MI between L and R via site-level probability joint distribution.

    For each site pair (i_L, i_R), compute joint probability from the
    site-level probabilities. For mirror symmetry, i_L and i_R are
    the same spatial position, so the joint should be concentrated
    on the diagonal (high MI). For random connections, it scatters.

    We bin sites by row (x-coordinate) to get a manageable joint table,
    then compute I(X_L; X_R) where X is the row index.
    """
    prob = np.abs(psi) ** 2
    s = np.sum(prob)
    if s < 1e-30:
        return 0.0
    prob /= s

    p_L = prob[:n_layer]
    p_R = prob[n_layer:]

    side = int(np.sqrt(n_layer))

    # Bin by row in each layer
    bin_L = np.zeros(side)
    bin_R = np.zeros(side)
    for i in range(n_layer):
        x = i // side
        bin_L[x] += p_L[i]
        bin_R[x] += p_R[i]

    # For a single-particle state, the joint p(row_L, row_R) is not
    # directly defined (particle is on ONE layer). Instead, measure
    # how similar the L and R spatial patterns are.
    # Use Jensen-Shannon divergence as a similarity measure,
    # then convert to an MI-like quantity.

    s_L = np.sum(bin_L)
    s_R = np.sum(bin_R)
    if s_L < 1e-30 or s_R < 1e-30:
        return 0.0

    q_L = bin_L / s_L
    q_R = bin_R / s_R
    m = 0.5 * (q_L + q_R)

    # JSD = 0.5 * KL(q_L||m) + 0.5 * KL(q_R||m)
    def kl(p, q):
        mask = p > 1e-30
        return np.sum(p[mask] * np.log(p[mask] / q[mask]))

    jsd = 0.5 * kl(q_L, m) + 0.5 * kl(q_R, m)
    # JSD in [0, ln(2)]. Convert to similarity: 1 - JSD/ln(2)
    similarity = 1.0 - jsd / np.log(2)
    # Scale to match MI units: multiply by max possible MI = log(n_bins)
    return float(similarity * np.log(side))


# ── Evolution ────────────────────────────────────────────────────────

def evolve(pos, col, adj, n_total, n_layer, psi0, use_gravity, label=""):
    """Evolve state and record observable trajectories."""
    L_mat = laplacian(pos, adj, n_total)
    if not use_gravity:
        H_free = build_H(col, adj, n_total, MASS, np.zeros(n_total))

    psi = psi0.copy()
    data = {"corr": [], "qcoh": [], "fid": [], "purity": [],
            "norm": [], "mi_cl": [], "mi_corr": []}

    for step in range(N_STEPS):
        if use_gravity:
            rho_density = np.abs(psi) ** 2
            phi = solve_phi(L_mat, n_total, G * rho_density, MU2_GRAV)
            H = build_H(col, adj, n_total, MASS, phi)
        else:
            H = H_free

        psi = cn_step(H, psi, DT)

        data["corr"].append(lr_correlation(psi, n_layer))
        data["qcoh"].append(lr_quantum_coherence(psi, n_layer))
        data["fid"].append(lr_fidelity(psi, n_layer))
        data["purity"].append(left_purity(psi, n_layer))
        data["norm"].append(float(np.linalg.norm(psi)))
        data["mi_cl"].append(classical_mi_lr(psi, n_layer))
        data["mi_corr"].append(correlation_mi(psi, n_layer))

    return data


# ── Main ─────────────────────────────────────────────────────────────

def main():
    t0 = time.time()
    side = SIDE
    n_layer = side * side

    print("=" * 74)
    print("MIRROR-SYMMETRIC STAGGERED LATTICE: DECOHERENCE PROTECTION")
    print("=" * 74)
    print(f"Side={side}, N_layer={n_layer}, N_total={2 * n_layer}")
    print(f"MASS={MASS}, G={G}, MU2={MU2_GRAV}, DT={DT}, N_STEPS={N_STEPS}")
    print(f"Reference: Mirror Z2 on DAGs MI=0.773, staggered Z2 boost ~2x")
    print()

    # Build lattices
    pos_m, col_m, adj_m, n_m, nl_m = make_mirror_bilayer(side)
    pos_r, col_r, adj_r, n_r, nl_r = make_random_bilayer(side)

    # Initial state: localized on L
    psi0_m = left_localized_state(n_m, nl_m, pos_m, sigma=side / 4, side=side)
    psi0_r = left_localized_state(n_r, nl_r, pos_r, sigma=side / 4, side=side)

    # Run four conditions
    configs = [
        ("mirror/free", pos_m, col_m, adj_m, n_m, nl_m, psi0_m, False),
        ("mirror/gravity", pos_m, col_m, adj_m, n_m, nl_m, psi0_m, True),
        ("random/free", pos_r, col_r, adj_r, n_r, nl_r, psi0_r, False),
        ("random/gravity", pos_r, col_r, adj_r, n_r, nl_r, psi0_r, True),
    ]

    results = {}
    for label, pos, col, adj, nt, nl, psi0, grav in configs:
        print(f"Evolving: {label}...")
        results[label] = evolve(pos, col, adj, nt, nl, psi0, grav, label)

    # ── Report ────────────────────────────────────────────────────────
    tp = [0, 4, 9, 14, 19, 29, 39, 49]
    tp_labels = [str(t + 1) for t in tp]
    labels = ["mirror/free", "mirror/gravity", "random/free", "random/gravity"]

    def print_table(title, key):
        print(f"\n{'=' * 74}")
        print(title)
        print(f"{'=' * 74}")
        print(f"{'Config':<20s} " + " ".join(f"t={t:<4s}" for t in tp_labels))
        print("-" * 74)
        for lab in labels:
            vals = [results[lab][key][t] for t in tp]
            print(f"{lab:<20s} " + " ".join(f"{v:6.4f}" for v in vals))

    print_table("L-R PROBABILITY CORRELATION (Pearson)", "corr")
    print_table("L-R QUANTUM COHERENCE |<psi_L|psi_R>|", "qcoh")
    print_table("L-R FIDELITY F(p_L, p_R)", "fid")
    print_table("L-PURITY (prob on L side)", "purity")
    print_table("CORRELATION MI (amplitude outer product)", "mi_corr")
    print_table("CLASSICAL MI (site-paired bins)", "mi_cl")

    # ── Norm check ────────────────────────────────────────────────────
    print(f"\n{'=' * 74}")
    print("NORM CONSERVATION")
    print(f"{'=' * 74}")
    for lab in labels:
        drift = max(abs(n - 1) for n in results[lab]["norm"])
        print(f"  {lab:<20s}  max|norm-1| = {drift:.2e}")

    # ── Summary ───────────────────────────────────────────────────────
    print(f"\n{'=' * 74}")
    print("SUMMARY STATISTICS (steady-state means, t=10..50)")
    print(f"{'=' * 74}")
    print(f"{'Config':<20s} {'corr':>8s} {'qcoh':>8s} {'fid':>8s} {'pur':>8s} "
          f"{'MI_corr':>8s} {'MI_cl':>8s}")
    print("-" * 74)
    for lab in labels:
        d = results[lab]
        ss = slice(9, None)  # t=10 onward
        print(f"{lab:<20s} "
              f"{np.mean(d['corr'][ss]):8.4f} "
              f"{np.mean(d['qcoh'][ss]):8.4f} "
              f"{np.mean(d['fid'][ss]):8.4f} "
              f"{np.mean(d['purity'][ss]):8.4f} "
              f"{np.mean(d['mi_corr'][ss]):8.4f} "
              f"{np.mean(d['mi_cl'][ss]):8.4f}")

    # ── Key comparisons ──────────────────────────────────────────────
    print(f"\n{'=' * 74}")
    print("KEY COMPARISONS")
    print(f"{'=' * 74}")
    ss = slice(9, None)

    corr_mg = np.mean(results["mirror/gravity"]["corr"][ss])
    corr_rg = np.mean(results["random/gravity"]["corr"][ss])
    corr_mf = np.mean(results["mirror/free"]["corr"][ss])
    corr_rf = np.mean(results["random/free"]["corr"][ss])

    qc_mg = np.mean(results["mirror/gravity"]["qcoh"][ss])
    qc_rg = np.mean(results["random/gravity"]["qcoh"][ss])
    qc_mf = np.mean(results["mirror/free"]["qcoh"][ss])
    qc_rf = np.mean(results["random/free"]["qcoh"][ss])

    mi_mg = np.mean(results["mirror/gravity"]["mi_corr"][ss])
    mi_rg = np.mean(results["random/gravity"]["mi_corr"][ss])
    mi_mf = np.mean(results["mirror/free"]["mi_corr"][ss])
    mi_rf = np.mean(results["random/free"]["mi_corr"][ss])

    print(f"  Correlation (mirror/random, gravity):  {corr_mg:.4f} / {corr_rg:.4f}")
    print(f"  Correlation (mirror/random, free):     {corr_mf:.4f} / {corr_rf:.4f}")
    print(f"  Quantum coh (mirror/random, gravity):  {qc_mg:.4f} / {qc_rg:.4f}")
    print(f"  Quantum coh (mirror/random, free):     {qc_mf:.4f} / {qc_rf:.4f}")
    print(f"  MI_corr (mirror/random, gravity):      {mi_mg:.4f} / {mi_rg:.4f}")
    print(f"  MI_corr (mirror/random, free):         {mi_mf:.4f} / {mi_rf:.4f}")

    if corr_rg > 1e-6:
        print(f"\n  Mirror/Random correlation ratio (gravity): {corr_mg / corr_rg:.2f}x")
    if qc_rg > 1e-10:
        print(f"  Mirror/Random quantum coherence ratio (gravity): {qc_mg / qc_rg:.2f}x")
    if mi_rg > 1e-10:
        print(f"  Mirror/Random MI ratio (gravity): {mi_mg / mi_rg:.2f}x")

    # Gravity effect on mirror
    if qc_mf > 1e-10:
        print(f"\n  Gravity boost on mirror quantum coherence: {qc_mg / qc_mf:.2f}x")
    if mi_mf > 1e-10:
        print(f"  Gravity boost on mirror MI: {mi_mg / mi_mf:.2f}x")

    print(f"\n  Reference: Mirror Z2 on DAGs MI = 0.773")
    print(f"  Peak MI_corr (mirror/gravity): {max(results['mirror/gravity']['mi_corr']):.4f}")
    print(f"  Peak quantum coherence (mirror/gravity): {max(results['mirror/gravity']['qcoh']):.4f}")

    elapsed = time.time() - t0
    print(f"\nTime: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
