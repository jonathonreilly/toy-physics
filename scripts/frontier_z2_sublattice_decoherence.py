#!/usr/bin/env python3
"""
Z2 Sublattice Decoherence Protection on 2D Staggered Lattice
==============================================================
Tests whether the staggered sublattice parity (even/odd sites) provides
decoherence protection similar to the mirror Z2 on DAGs (MI=0.773, 6x random).

The staggered lattice has a built-in Z2: even sites (eps=+1) vs odd (eps=-1).
If this Z2 provides channel preservation, the mirror program's strongest
result transfers to the staggered architecture.

Protocol:
  For each lattice size (side = 8, 10, 12):
    Prepare three initial states:
      - psi_even: localized on EVEN sublattice only
      - psi_odd:  localized on ODD sublattice only
      - psi_mix:  uniform over all sites
    Evolve under free and self-gravity Hamiltonians for 40 steps.
    Measure sublattice purity, mutual information (left/right), decoherence.

Key test: sublattice-polarized states should maintain higher MI and lower
decoherence than the mixed state, indicating Z2 protection.

Compare MI to mirror Z2 result: MI = 0.773 at N=80 in 2D.
"""

from __future__ import annotations
import numpy as np
from scipy.sparse import lil_matrix, eye as speye
from scipy.sparse.linalg import spsolve

MASS = 0.30
MU2 = 0.22
DT = 0.12
G = 10.0
N_STEPS = 40


# ── Lattice construction ─────────────────────────────────────────────

def make_periodic_lattice(side):
    """2D periodic (torus) lattice with checkerboard coloring."""
    n = side * side
    pos = np.zeros((n, 2))
    col = np.zeros(n, dtype=int)
    for x in range(side):
        for y in range(side):
            idx = x * side + y
            pos[idx] = [x, y]
            col[idx] = (x + y) % 2
    adj = {}
    for x in range(side):
        for y in range(side):
            i = x * side + y
            nbs = []
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx_, ny_ = (x + dx) % side, (y + dy) % side
                nbs.append(nx_ * side + ny_)
            adj[i] = nbs
    return pos, col, adj, n


# ── Physics tools ─────────────────────────────────────────────────────

def laplacian(adj, n):
    L = lil_matrix((n, n), dtype=float)
    for i, nbs in adj.items():
        for j in nbs:
            if i < j:
                L[i, j] -= 1.0
                L[j, i] -= 1.0
                L[i, i] += 1.0
                L[j, j] += 1.0
    return L.tocsr()


def solve_phi(L, n, rho):
    if np.allclose(rho, 0):
        return np.zeros(n)
    A = (L + MU2 * speye(n, format='csr')).tocsc()
    return spsolve(A, rho)


def build_H(col, adj, n, mass, phi):
    """Staggered Hamiltonian with parity coupling: H_diag = (mass + phi) * eps."""
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

def sublattice_state(col, n, target_color, sigma=2.0, side=None):
    """Gaussian envelope restricted to one sublattice (even=0 or odd=1)."""
    if side is None:
        side = int(np.sqrt(n))
    center = side / 2.0
    psi = np.zeros(n, dtype=complex)
    for i in range(n):
        x = i // side
        y = i % side
        if col[i] == target_color:
            psi[i] = np.exp(-((x - center) ** 2 + (y - center) ** 2) / (2 * sigma ** 2))
    norm = np.linalg.norm(psi)
    if norm > 0:
        psi /= norm
    return psi


def mixed_state(n, sigma=2.0, side=None):
    """Gaussian envelope on all sites."""
    if side is None:
        side = int(np.sqrt(n))
    center = side / 2.0
    psi = np.zeros(n, dtype=complex)
    for i in range(n):
        x = i // side
        y = i % side
        psi[i] = np.exp(-((x - center) ** 2 + (y - center) ** 2) / (2 * sigma ** 2))
    psi /= np.linalg.norm(psi)
    return psi


# ── Observables ──────────────────────────────────────────────────────

def sublattice_purity(psi, col, target_color):
    """Fraction of probability on the target sublattice."""
    prob = np.abs(psi) ** 2
    return float(np.sum(prob[col == target_color]))


def mutual_information(psi, n, side):
    """MI between left and right halves via Schmidt decomposition.

    For a pure state |psi> on n sites, partition into L (x < side/2)
    and R (x >= side/2). Reshape into matrix M[L, R].
    Schmidt values from SVD of M give S(rho_L).
    MI = 2 * S(rho_L) for a pure state.
    """
    left_idx = []
    right_idx = []
    for i in range(n):
        x = i // side
        if x < side // 2:
            left_idx.append(i)
        else:
            right_idx.append(i)

    n_left = len(left_idx)
    n_right = len(right_idx)

    # Reshape psi into matrix M[left, right]
    M = np.zeros((n_left, n_right), dtype=complex)
    # Map site indices to local indices
    left_map = {site: loc for loc, site in enumerate(left_idx)}
    right_map = {site: loc for loc, site in enumerate(right_idx)}

    for i in range(n):
        x = i // side
        if x < side // 2:
            # This site is in the left partition
            # Its contribution to M depends on which right site it pairs with
            # For a 1D bipartition of a product Hilbert space, we need to
            # think of the state in the tensor product basis.
            pass

    # Direct approach: the state lives in C^n. The bipartition is L vs R sites.
    # The Hilbert space is C^n (single particle), NOT a tensor product.
    # For a single-particle state, the reduced density matrix rho_L is:
    #   rho_L[i,j] = psi[i] * conj(psi[j])  for i,j in L
    # This is a rank-1 matrix, so S(rho_L) = 0 for a pure single-particle state.
    #
    # BUT: for decoherence studies, the relevant MI is the CLASSICAL mutual
    # information of the probability distribution p(x) = |psi(x)|^2,
    # partitioned into L and R marginals.
    #
    # Classical MI: I(L;R) = H(L) + H(R) - H(L,R)
    # where H is Shannon entropy.

    prob = np.abs(psi) ** 2
    prob /= np.sum(prob)  # normalize

    # Joint entropy H(L, R) = H(full distribution)
    H_joint = -np.sum(prob[prob > 0] * np.log(prob[prob > 0]))

    # Marginal over L
    p_left = np.zeros(n_left)
    for loc, site in enumerate(left_idx):
        p_left[loc] = prob[site]
    # Coarse-grain: bin by x-coordinate for L
    # Actually, for single-particle, marginals are just sums over the other partition
    p_L = float(np.sum(p_left))
    p_R = 1.0 - p_L

    # For a more informative MI, bin each half by y-coordinate
    n_bins = side
    p_Ly = np.zeros(n_bins)
    p_Ry = np.zeros(n_bins)
    p_joint = np.zeros((n_bins, n_bins))

    for site in left_idx:
        y = site % side
        p_Ly[y] += prob[site]

    for site in right_idx:
        y = site % side
        p_Ry[y] += prob[site]

    # Joint distribution: p(y_L, y_R)
    # For single-particle, the particle is either on the left or the right,
    # so the joint distribution over (y_L, y_R) doesn't factor naturally.
    # Instead, use the spatial structure:
    # Bin the full distribution into a 2D grid: (x_bin, y_bin)
    n_xbins = 2  # left vs right
    p_xy = np.zeros((n_xbins, n_bins))
    for i in range(n):
        x = i // side
        y = i % side
        x_bin = 0 if x < side // 2 else 1
        p_xy[x_bin, y] += prob[i]

    # MI = H(X) + H(Y) - H(X,Y) where X = left/right, Y = y-bin
    # H(X)
    p_x = np.sum(p_xy, axis=1)
    H_X = -np.sum(p_x[p_x > 0] * np.log(p_x[p_x > 0]))

    # H(Y)
    p_y = np.sum(p_xy, axis=0)
    H_Y = -np.sum(p_y[p_y > 0] * np.log(p_y[p_y > 0]))

    # H(X,Y)
    p_flat = p_xy.flatten()
    H_XY = -np.sum(p_flat[p_flat > 0] * np.log(p_flat[p_flat > 0]))

    mi = H_X + H_Y - H_XY
    return float(mi), H_X, H_Y, H_XY


def sublattice_coherence(psi, col):
    """Off-diagonal coherence between sublattices.

    C = |sum_{even i} conj(psi[i]) * sum_{odd j} psi[j]|
    Measures quantum coherence between the two sublattice sectors.
    """
    even_amp = np.sum(psi[col == 0])
    odd_amp = np.sum(psi[col == 1])
    return float(np.abs(np.conj(even_amp) * odd_amp))


# ── Main simulation ──────────────────────────────────────────────────

def run_for_side(side):
    print(f"\n{'=' * 72}")
    print(f"  SIDE = {side}  (N = {side * side})")
    print(f"{'=' * 72}")

    pos, col, adj, n = make_periodic_lattice(side)
    L = laplacian(adj, n)
    H_free = build_H(col, adj, n, MASS, np.zeros(n))

    init_states = {
        "even": sublattice_state(col, n, 0, sigma=side / 4, side=side),
        "odd": sublattice_state(col, n, 1, sigma=side / 4, side=side),
        "mix": mixed_state(n, sigma=side / 4, side=side),
    }
    results = {}

    for label, psi0 in init_states.items():
        for grav_label, use_gravity in [("free", False), ("gravity", True)]:
            tag = f"{label}/{grav_label}"
            print(f"\n  --- {tag} ---")

            psi = psi0.copy()
            purities = []
            mis = []
            coherences = []
            norms = []

            # Initial color for sublattice purity tracking
            init_color = 0 if label == "even" else (1 if label == "odd" else -1)

            for step in range(N_STEPS):
                if use_gravity:
                    rho_density = np.abs(psi) ** 2
                    phi = solve_phi(L, n, G * rho_density)
                    H = build_H(col, adj, n, MASS, phi)
                else:
                    H = H_free

                psi = cn_step(H, psi, DT)

                # Observables
                norms.append(float(np.linalg.norm(psi)))

                if init_color >= 0:
                    purities.append(sublattice_purity(psi, col, init_color))
                else:
                    # For mixed state, track even sublattice fraction
                    purities.append(sublattice_purity(psi, col, 0))

                mi_val, _, _, _ = mutual_information(psi, n, side)
                mis.append(mi_val)

                coherences.append(sublattice_coherence(psi, col))

            # Report
            print(f"    Norm: {norms[0]:.6f} -> {norms[-1]:.6f}")
            print(f"    Sublattice purity (init sublattice):")
            init_pur = sublattice_purity(psi0, col, max(init_color, 0))
            print(f"      t=0:  {init_pur:.4f}")
            print(f"      t=10: {purities[9]:.4f}")
            print(f"      t=20: {purities[19]:.4f}")
            print(f"      t=40: {purities[-1]:.4f}")
            print(f"    Mutual information (left/right):")
            print(f"      t=1:  {mis[0]:.6f}")
            print(f"      t=10: {mis[9]:.6f}")
            print(f"      t=20: {mis[19]:.6f}")
            print(f"      t=40: {mis[-1]:.6f}")
            print(f"    Sublattice coherence:")
            print(f"      t=1:  {coherences[0]:.6f}")
            print(f"      t=10: {coherences[9]:.6f}")
            print(f"      t=20: {coherences[19]:.6f}")
            print(f"      t=40: {coherences[-1]:.6f}")

            # Store for summary
            results[tag] = {
                "purities": purities,
                "mis": mis,
                "coherences": coherences,
                "norms": norms,
            }

    return results


def summarize(all_results):
    print(f"\n{'=' * 72}")
    print("  SUMMARY: Z2 Sublattice Decoherence Protection")
    print(f"{'=' * 72}")

    for side, results in all_results.items():
        n = side * side
        print(f"\n  Side={side} (N={n})")
        print(f"  {'State':<15} {'Mode':<10} {'MI(t=40)':<12} {'Purity(t=40)':<14} {'Coh(t=40)':<12}")
        print(f"  {'-' * 63}")
        for tag, data in sorted(results.items()):
            label, mode = tag.split("/")
            mi_final = data["mis"][-1]
            pur_final = data["purities"][-1]
            coh_final = data["coherences"][-1]
            print(f"  {label:<15} {mode:<10} {mi_final:<12.6f} {pur_final:<14.4f} {coh_final:<12.6f}")

    # Key comparison: sublattice-polarized vs mixed under gravity
    print(f"\n  KEY TEST: Does sublattice polarization preserve information?")
    print(f"  (Higher MI = better channel preservation)")
    print(f"  Mirror Z2 reference: MI = 0.773 at N=80 in 2D")
    print()

    for side, results in all_results.items():
        n = side * side
        even_grav = results.get("even/gravity", {})
        odd_grav = results.get("odd/gravity", {})
        mix_grav = results.get("mix/gravity", {})
        even_free = results.get("even/free", {})
        mix_free = results.get("mix/free", {})

        if even_grav and mix_grav:
            mi_even = even_grav["mis"][-1]
            mi_odd = odd_grav["mis"][-1] if odd_grav else 0
            mi_mix = mix_grav["mis"][-1]
            mi_even_free = even_free["mis"][-1] if even_free else 0
            mi_mix_free = mix_free["mis"][-1] if mix_free else 0

            ratio = mi_even / mi_mix if mi_mix > 1e-10 else float('inf')
            grav_boost = mi_even / mi_even_free if mi_even_free > 1e-10 else float('inf')

            print(f"  Side={side}: MI(even/grav)={mi_even:.4f}  MI(mix/grav)={mi_mix:.4f}  "
                  f"ratio={ratio:.2f}x")
            print(f"           MI(even/free)={mi_even_free:.4f}  gravity boost={grav_boost:.2f}x")

            protected = mi_even > mi_mix * 1.2
            print(f"           Z2 protection: {'YES' if protected else 'NO'} "
                  f"(even MI > 1.2x mix MI)")


def main():
    print("Z2 Sublattice Decoherence Protection")
    print("=" * 72)
    print(f"Parameters: MASS={MASS}, MU2={MU2}, DT={DT}, G={G}, N_STEPS={N_STEPS}")
    print(f"Parity coupling: H_diag = (MASS + phi) * eps")
    print(f"Comparing sublattice-polarized vs mixed states")
    print(f"Reference: Mirror Z2 MI = 0.773 at N=80")

    all_results = {}
    for side in (8, 10, 12):
        all_results[side] = run_for_side(side)

    summarize(all_results)


if __name__ == "__main__":
    main()
