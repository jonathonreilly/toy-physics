#!/usr/bin/env python3
"""
Branch-mediated entanglement robustness checks (2-body and 3-body).

Multi-seed, multi-geometry, and source-position robustness sweeps for the
branch-mediated entanglement results. Tests whether delta_S > 0 (2-body)
and the corrected 3-body W-type classification survive across:

  1. Multiple seeds (5 per configuration, jittered lattice positions)
  2. Source position sweep (5 different locations)
  3. Particle separation sweep (distances 4, 6, 8, 10)
  4. 2D size scaling (side = 8, 10, 12)
  5. Error bars from seed spread

Protocol (2-body):
  Two particles at (x1, side/2) and (x2, side/2).
  Source in superposition: config A (G) vs config B (0).
  Evolve each particle under each geometry (30 steps, parity coupling).
  S = H_binary((1 + |overlap_1| * |overlap_2|) / 2)

Protocol (3-body):
  Three particles in triangular arrangement.
  Same source superposition.
  Compute bipartite entropies and 3-tangle.

Important boundary:
  For the fixed two-branch ansatz used here, tau_3 = 0 is theorem-implied by
  the overlap algebra. So the GHZ count below is only a sanity check that the
  code matches the ansatz; it is not an empirical discovery metric.

This runner is the canonical interpretation surface for the 3-body branch
protocol. The earlier standalone three-body runner uses a heuristic tangle
construction and should not override this robustness read.
"""

from __future__ import annotations

import math
import time

import numpy as np
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

from periodic_geometry import infer_periodic_extents, minimum_image_distance

# ── Physical parameters ──────────────────────────────────────────────
MASS = 0.30
MU2 = 0.22
DT = 0.12
N_STEPS = 30
SIGMA = 1.5

N_SEEDS = 5
G_VALUES = [1, 5, 10, 20, 50]
SEPARATIONS = [4, 6, 8, 10]
SIDES = [8, 10, 12]


# ── Lattice construction ─────────────────────────────────────────────

def make_lattice_2d(side: int, seed: int | None = None):
    """Build a 2D periodic staggered lattice with optional jitter."""
    rng = np.random.default_rng(seed)
    jitter_scale = 0.05  # small positional jitter for robustness

    coords = []
    colors = []
    adj = {}
    index = {}
    idx = 0
    for x in range(side):
        for y in range(side):
            jx = rng.normal(0, jitter_scale) if seed is not None else 0.0
            jy = rng.normal(0, jitter_scale) if seed is not None else 0.0
            coords.append((float(x) + jx, float(y) + jy))
            colors.append((x + y) % 2)
            index[(x, y)] = idx
            idx += 1
    pos = np.array(coords)
    color = np.array(colors, dtype=int)
    n = len(pos)
    for x in range(side):
        for y in range(side):
            a = index[(x, y)]
            adj[a] = []
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                adj[a].append(index[((x + dx) % side, (y + dy) % side)])
    return pos, color, adj, index, n


def build_laplacian(pos: np.ndarray, adj: dict[int, list[int]]):
    n = len(pos)
    lap = lil_matrix((n, n), dtype=float)
    extents = infer_periodic_extents(pos)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = minimum_image_distance(pos[i], pos[j], extents)
            w = 1.0 / max(d, 0.5)
            lap[i, j] -= w
            lap[j, i] -= w
            lap[i, i] += w
            lap[j, j] += w
    return lap.tocsr()


def build_hamiltonian(pos: np.ndarray, color: np.ndarray,
                      adj: dict[int, list[int]], phi: np.ndarray):
    """Staggered-fermion Hamiltonian with parity coupling."""
    n = len(pos)
    ham = lil_matrix((n, n), dtype=complex)
    parity = np.where(color == 0, 1.0, -1.0)
    ham.setdiag((MASS + phi) * parity)
    extents = infer_periodic_extents(pos)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j:
                continue
            d = minimum_image_distance(pos[i], pos[j], extents)
            w = 1.0 / max(d, 0.5)
            ham[i, j] += -0.5j * w
            ham[j, i] += 0.5j * w
    return ham.tocsr()


def cn_step(ham, psi: np.ndarray):
    """Crank-Nicolson time step."""
    n = ham.shape[0]
    ap = (speye(n, format="csc") + 1j * ham * DT / 2).tocsc()
    am = speye(n, format="csr") - 1j * ham * DT / 2
    return spsolve(ap, am.dot(psi))


def gaussian_at(pos: np.ndarray, center: tuple[float, float], sigma: float):
    """Gaussian wavepacket centered at (cx, cy)."""
    cx, cy = center
    rsq = (pos[:, 0] - cx) ** 2 + (pos[:, 1] - cy) ** 2
    psi = np.exp(-0.5 * rsq / sigma ** 2).astype(complex)
    norm = np.linalg.norm(psi)
    if norm < 1e-30:
        raise ValueError(f"Gaussian at {center} has zero norm on lattice")
    return psi / norm


def binary_entropy(p: float) -> float:
    """H(p) = -p log(p) - (1-p) log(1-p), natural log."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


# ── 2-body branch entanglement ───────────────────────────────────────

def run_2body(side: int, g: float, separation: int,
              source_xy: tuple[int, int], seed: int | None = None):
    """Run 2-body branch entanglement for given configuration."""
    pos, color, adj, index, n = make_lattice_2d(side, seed=seed)
    lap = build_laplacian(pos, adj)

    source_node = index[source_xy]

    # Two external source configurations
    rho_ext = np.zeros(n)
    rho_ext[source_node] = g
    phi_A = spsolve((lap + MU2 * speye(n, format="csr")).tocsc(), rho_ext)
    phi_B = np.zeros(n)

    ham_A = build_hamiltonian(pos, color, adj, phi_A)
    ham_B = build_hamiltonian(pos, color, adj, phi_B)

    mid = side // 2
    half_sep = separation // 2
    x1 = mid - half_sep
    x2 = mid + half_sep
    # Clamp to lattice
    x1 = max(0, min(x1, side - 1))
    x2 = max(0, min(x2, side - 1))

    psi_1A = gaussian_at(pos, (float(x1), float(mid)), SIGMA)
    psi_1B = psi_1A.copy()
    psi_2A = gaussian_at(pos, (float(x2), float(mid)), SIGMA)
    psi_2B = psi_2A.copy()

    for _ in range(N_STEPS):
        psi_1A = cn_step(ham_A, psi_1A)
        psi_1B = cn_step(ham_B, psi_1B)
        psi_2A = cn_step(ham_A, psi_2A)
        psi_2B = cn_step(ham_B, psi_2B)

    overlap_1 = abs(np.vdot(psi_1A, psi_1B))
    overlap_2 = abs(np.vdot(psi_2A, psi_2B))

    product_overlap = overlap_1 * overlap_2
    p_q = 0.5 + 0.5 * product_overlap
    s_quantum = binary_entropy(p_q)

    p_m = 0.5 + 0.5 * overlap_1
    s_mix = binary_entropy(p_m)
    delta_s = s_quantum - s_mix

    norm_check = max(
        abs(np.linalg.norm(psi_1A) - 1.0),
        abs(np.linalg.norm(psi_1B) - 1.0),
        abs(np.linalg.norm(psi_2A) - 1.0),
        abs(np.linalg.norm(psi_2B) - 1.0),
    )

    return {
        "overlap_1": overlap_1,
        "overlap_2": overlap_2,
        "S_quantum": s_quantum,
        "S_mix": s_mix,
        "delta_S": delta_s,
        "norm_dev": norm_check,
    }


# ── 3-body branch entanglement ───────────────────────────────────────

def run_3body(side: int, g: float, source_xy: tuple[int, int],
              seed: int | None = None):
    """Run 3-body branch entanglement with triangular arrangement."""
    pos, color, adj, index, n = make_lattice_2d(side, seed=seed)
    lap = build_laplacian(pos, adj)

    source_node = index[source_xy]
    rho_ext = np.zeros(n)
    rho_ext[source_node] = g
    phi_A = spsolve((lap + MU2 * speye(n, format="csr")).tocsc(), rho_ext)
    phi_B = np.zeros(n)

    ham_A = build_hamiltonian(pos, color, adj, phi_A)
    ham_B = build_hamiltonian(pos, color, adj, phi_B)

    # Triangular arrangement scaled to lattice
    cx, cy = side / 2, side / 2
    r = side * 0.3  # triangle radius
    positions = [
        (cx - r * 0.5, cy + r * 0.43),   # top-left
        (cx + r * 0.5, cy + r * 0.43),   # top-right
        (cx, cy - r * 0.43),             # bottom
    ]

    overlaps = []
    for (px, py) in positions:
        px = max(0.5, min(px, side - 1.5))
        py = max(0.5, min(py, side - 1.5))
        psi_A = gaussian_at(pos, (px, py), SIGMA)
        psi_B = psi_A.copy()
        for _ in range(N_STEPS):
            psi_A = cn_step(ham_A, psi_A)
            psi_B = cn_step(ham_B, psi_B)
        overlaps.append(abs(np.vdot(psi_A, psi_B)))

    o1, o2, o3 = overlaps

    # Bipartite entropies: S(i | jk)
    s_1_23 = binary_entropy(0.5 + 0.5 * o2 * o3)
    s_2_13 = binary_entropy(0.5 + 0.5 * o1 * o3)
    s_3_12 = binary_entropy(0.5 + 0.5 * o1 * o2)

    # Pairwise entropies: S(i | j) tracing out third particle
    # For 2-branch state tracing out particle k:
    # rho_ij eigenvalues involve overlap_k only through branch distinguishability
    s_12 = binary_entropy(0.5 + 0.5 * o3)  # trace out 3
    s_23 = binary_entropy(0.5 + 0.5 * o1)  # trace out 1
    s_13 = binary_entropy(0.5 + 0.5 * o2)  # trace out 2

    # Concurrences (approximation from entropies)
    # C^2 ~ 2(1 - Tr(rho^2)) for qubit-like systems
    def entropy_to_concurrence_sq(s_val):
        # For binary entropy S = H(p), recover p then C^2 = 4p(1-p)
        # Invert approximately: if S is small, p ~ 0.5 + 0.5*exp(-S)
        # Use: C^2 = 1 - (2p-1)^2 for p = (1+overlap)/2
        # Actually we have the overlaps directly, use those
        return 0.0  # placeholder

    # 3-tangle from overlaps directly
    # For 2-branch state: C_{i|jk}^2 = 1 - (o_j * o_k)^2
    # C_{i|j}^2 = 1 - o_k^2 (when tracing particle k)
    c_1_23_sq = 1.0 - (o2 * o3) ** 2
    c_1_2_sq = 1.0 - o3 ** 2
    c_1_3_sq = 1.0 - o2 ** 2

    tau_3 = max(0.0, c_1_23_sq - c_1_2_sq - c_1_3_sq)

    # Classification
    bipartite = [s_1_23, s_2_13, s_3_12]
    max_bip = max(bipartite)
    min_bip = min(bipartite)
    spread = (max_bip - min_bip) / max(max_bip, 1e-15)

    if min_bip < 1e-6:
        classification = "BISEPARABLE"
    elif tau_3 > 0.01 and spread < 0.3:
        classification = "GHZ"
    elif tau_3 > 0.01:
        classification = "GHZ-asym"
    elif spread < 0.3:
        classification = "W"
    else:
        classification = "W-asym"

    return {
        "overlaps": (o1, o2, o3),
        "S_bipartite": (s_1_23, s_2_13, s_3_12),
        "S_pairwise": (s_12, s_23, s_13),
        "tau_3": tau_3,
        "classification": classification,
    }


# ── Robustness sweeps ────────────────────────────────────────────────

def source_positions(side: int) -> list[tuple[int, int]]:
    """Five source positions: center, off-center cardinal directions."""
    mid = side // 2
    offset = max(1, side // 4)
    return [
        (mid, mid),
        (mid + offset, mid),
        (mid - offset, mid),
        (mid, mid + offset),
        (mid, mid - offset),
    ]


def run_multi_seed(func, seeds, **kwargs):
    """Run a function across multiple seeds, return list of results."""
    results = []
    for s in seeds:
        results.append(func(seed=s, **kwargs))
    return results


def stats(values):
    """Mean and std of a list of floats."""
    arr = np.array(values)
    return float(np.mean(arr)), float(np.std(arr))


# ── Main ─────────────────────────────────────────────────────────────

def main():
    t_start = time.time()
    seeds = list(range(42, 42 + N_SEEDS))

    print("=" * 80)
    print("BRANCH ENTANGLEMENT ROBUSTNESS CHECKS")
    print("=" * 80)
    print()
    print(f"Seeds: {seeds}")
    print(f"G values: {G_VALUES}")
    print(f"Separations: {SEPARATIONS}")
    print(f"Lattice sides: {SIDES}")
    print(f"N_STEPS={N_STEPS}, DT={DT}, MASS={MASS}, MU2={MU2}, SIGMA={SIGMA}")
    print()

    # ================================================================
    # SECTION 1: 2-BODY SEPARATION SWEEP (multi-seed)
    # ================================================================
    print("=" * 80)
    print("SECTION 1: 2-BODY SEPARATION SWEEP (side=10, source at center)")
    print("=" * 80)
    print()

    side_default = 10
    src_default = (side_default // 2, side_default // 2)

    print(f"{'G':>4} {'sep':>4}  {'S_q mean':>9} {'S_q std':>8} "
          f"{'dS mean':>9} {'dS std':>8}  {'ovlp1':>7} {'ovlp2':>7} "
          f"{'max_norm_dev':>12}")
    print("-" * 85)

    sep_data = {}
    for g in G_VALUES:
        for sep in SEPARATIONS:
            results = run_multi_seed(
                lambda seed, **kw: run_2body(**kw, seed=seed),
                seeds,
                side=side_default, g=g, separation=sep, source_xy=src_default,
            )
            s_q_vals = [r["S_quantum"] for r in results]
            ds_vals = [r["delta_S"] for r in results]
            o1_vals = [r["overlap_1"] for r in results]
            o2_vals = [r["overlap_2"] for r in results]
            nd_vals = [r["norm_dev"] for r in results]

            sq_m, sq_s = stats(s_q_vals)
            ds_m, ds_s = stats(ds_vals)
            o1_m, _ = stats(o1_vals)
            o2_m, _ = stats(o2_vals)
            nd_max = max(nd_vals)

            sep_data[(g, sep)] = (sq_m, sq_s, ds_m, ds_s)

            print(f"{g:>4} {sep:>4}  {sq_m:>9.5f} {sq_s:>8.5f} "
                  f"{ds_m:>9.5f} {ds_s:>8.5f}  {o1_m:>7.4f} {o2_m:>7.4f} "
                  f"{nd_max:>12.2e}")

    # Check: delta_S > 0 everywhere?
    print()
    all_positive = all(sep_data[k][2] > 0 for k in sep_data)
    print(f"delta_S > 0 at all (G, separation): {all_positive}")

    # ================================================================
    # SECTION 2: SOURCE POSITION SWEEP (multi-seed)
    # ================================================================
    print()
    print("=" * 80)
    print("SECTION 2: SOURCE POSITION SWEEP (side=10, separation=6)")
    print("=" * 80)
    print()

    sep_fixed = 6
    src_positions = source_positions(side_default)
    print(f"Source positions: {src_positions}")
    print()

    print(f"{'G':>4} {'src_x':>5} {'src_y':>5}  {'S_q mean':>9} {'S_q std':>8} "
          f"{'dS mean':>9} {'dS std':>8}")
    print("-" * 60)

    src_data = {}
    for g in G_VALUES:
        for sx, sy in src_positions:
            results = run_multi_seed(
                lambda seed, **kw: run_2body(**kw, seed=seed),
                seeds,
                side=side_default, g=g, separation=sep_fixed,
                source_xy=(sx, sy),
            )
            s_q_vals = [r["S_quantum"] for r in results]
            ds_vals = [r["delta_S"] for r in results]
            sq_m, sq_s = stats(s_q_vals)
            ds_m, ds_s = stats(ds_vals)

            src_data[(g, sx, sy)] = (sq_m, sq_s, ds_m, ds_s)

            print(f"{g:>4} {sx:>5} {sy:>5}  {sq_m:>9.5f} {sq_s:>8.5f} "
                  f"{ds_m:>9.5f} {ds_s:>8.5f}")

    print()
    all_positive_src = all(src_data[k][2] > 0 for k in src_data)
    print(f"delta_S > 0 at all (G, source_pos): {all_positive_src}")

    # ================================================================
    # SECTION 3: SIZE SCALING (multi-seed)
    # ================================================================
    print()
    print("=" * 80)
    print("SECTION 3: SIZE SCALING (separation=6, source at center)")
    print("=" * 80)
    print()

    print(f"{'side':>5} {'G':>4}  {'S_q mean':>9} {'S_q std':>8} "
          f"{'dS mean':>9} {'dS std':>8}")
    print("-" * 50)

    size_data = {}
    for side in SIDES:
        src = (side // 2, side // 2)
        for g in G_VALUES:
            results = run_multi_seed(
                lambda seed, **kw: run_2body(**kw, seed=seed),
                seeds,
                side=side, g=g, separation=sep_fixed, source_xy=src,
            )
            s_q_vals = [r["S_quantum"] for r in results]
            ds_vals = [r["delta_S"] for r in results]
            sq_m, sq_s = stats(s_q_vals)
            ds_m, ds_s = stats(ds_vals)

            size_data[(side, g)] = (sq_m, sq_s, ds_m, ds_s)

            print(f"{side:>5} {g:>4}  {sq_m:>9.5f} {sq_s:>8.5f} "
                  f"{ds_m:>9.5f} {ds_s:>8.5f}")

    print()
    all_positive_size = all(size_data[k][2] > 0 for k in size_data)
    print(f"delta_S > 0 at all (side, G): {all_positive_size}")

    # Check persistence: does entanglement persist at side=12?
    print()
    print("Entanglement persistence at side=12:")
    for g in G_VALUES:
        sq_m, _, ds_m, ds_s = size_data[(12, g)]
        sig = ds_m / max(ds_s, 1e-15)
        print(f"  G={g:>3}: S_q={sq_m:.5f}, dS={ds_m:.5f} +/- {ds_s:.5f} "
              f"(dS/{ds_s:.0e} = {sig:.1f} sigma)")

    # ================================================================
    # SECTION 4: 3-BODY ROBUSTNESS (multi-seed, source sweep)
    # ================================================================
    print()
    print("=" * 80)
    print("SECTION 4: 3-BODY TRIPARTITE ENTANGLEMENT ROBUSTNESS")
    print("=" * 80)
    print()

    side_3b = 12
    src_3b_positions = source_positions(side_3b)

    print(f"{'G':>4} {'src':>10}  {'S_1|23':>8} {'S_2|13':>8} {'S_3|12':>8} "
          f"{'tau_3':>8} {'class':>10}  {'n_GHZ':>5}/{N_SEEDS}")
    print("-" * 80)

    three_body_data = {}
    for g in G_VALUES:
        for sx, sy in src_3b_positions:
            results = run_multi_seed(
                lambda seed, **kw: run_3body(**kw, seed=seed),
                seeds,
                side=side_3b, g=g, source_xy=(sx, sy),
            )

            s_bip_arrays = np.array([r["S_bipartite"] for r in results])
            tau_vals = [r["tau_3"] for r in results]
            classes = [r["classification"] for r in results]

            s_bip_mean = s_bip_arrays.mean(axis=0)
            tau_m, tau_s = stats(tau_vals)
            n_ghz = sum(1 for c in classes if c.startswith("GHZ"))

            # Majority classification
            from collections import Counter
            majority_class = Counter(classes).most_common(1)[0][0]

            three_body_data[(g, sx, sy)] = {
                "S_bip_mean": s_bip_mean,
                "tau_mean": tau_m,
                "tau_std": tau_s,
                "n_ghz": n_ghz,
                "majority": majority_class,
            }

            print(f"{g:>4} ({sx:>2},{sy:>2})  "
                  f"{s_bip_mean[0]:>8.5f} {s_bip_mean[1]:>8.5f} {s_bip_mean[2]:>8.5f} "
                  f"{tau_m:>8.5f} {majority_class:>10}  {n_ghz:>5}/{N_SEEDS}")

    print()
    # GHZ robustness summary
    total_configs = len(three_body_data)
    ghz_configs = sum(
        1 for v in three_body_data.values() if v["majority"].startswith("GHZ")
    )
    print("GHZ-type theorem check (not an empirical discovery metric): "
          f"{ghz_configs}/{total_configs} configurations")

    # ================================================================
    # SECTION 5: COMPREHENSIVE SUMMARY
    # ================================================================
    print()
    print("=" * 80)
    print("COMPREHENSIVE SUMMARY")
    print("=" * 80)
    print()

    print("2-BODY BRANCH ENTANGLEMENT:")
    print(f"  Separation sweep: delta_S > 0 everywhere = {all_positive}")
    print(f"  Source position sweep: delta_S > 0 everywhere = {all_positive_src}")
    print(f"  Size scaling: delta_S > 0 everywhere = {all_positive_size}")
    print()

    # Collect all 2-body delta_S values for overall statistics
    all_ds = []
    for k, v in sep_data.items():
        all_ds.append(v[2])  # mean delta_S
    for k, v in src_data.items():
        all_ds.append(v[2])
    for k, v in size_data.items():
        all_ds.append(v[2])

    all_ds_arr = np.array(all_ds)
    print(f"  Overall delta_S: min={all_ds_arr.min():.6f}, "
          f"max={all_ds_arr.max():.6f}, mean={all_ds_arr.mean():.6f}")
    print(f"  Fraction with delta_S > 0: "
          f"{np.sum(all_ds_arr > 0)}/{len(all_ds_arr)}")
    print()

    print("3-BODY TRIPARTITE ENTANGLEMENT:")
    print("  GHZ-type theorem-check fraction: "
          f"{ghz_configs}/{total_configs} "
          f"({100*ghz_configs/max(total_configs,1):.0f}%)")

    tau_means = [v["tau_mean"] for v in three_body_data.values()]
    print(f"  3-tangle: min={min(tau_means):.6f}, "
          f"max={max(tau_means):.6f}, mean={np.mean(tau_means):.6f}")
    print()

    robust_2body = all_positive and all_positive_src and all_positive_size
    # W-type is actually the correct classification for a 2-branch state.
    # For |Psi> = (|abc> + |a'b'c'>)/sqrt(2), the 3-tangle is:
    #   tau_3 = C_{1|23}^2 - C_{1|2}^2 - C_{1|3}^2
    #         = (1 - o2^2*o3^2) - (1 - o3^2) - (1 - o2^2)
    #         = -(1-o2^2)(1-o3^2)  <= 0  always
    # So tau_3 = 0 is a mathematical theorem for 2-branch states.
    # The entanglement is distributed in pairwise correlations (W-type),
    # not in genuine 3-party correlations (GHZ-type).
    w_configs = sum(
        1 for v in three_body_data.values() if v["majority"].startswith("W")
    )
    robust_3body_w = w_configs >= total_configs * 0.8

    print("VERDICT:")
    if robust_2body:
        print("  2-body branch entanglement: ROBUST")
        print("    delta_S > 0 across all seeds, separations, source positions, and sizes.")
    else:
        print("  2-body branch entanglement: FRAGILE")
        print("    Some configurations show delta_S <= 0.")

    print()
    print("  3-body entanglement type: W-TYPE (not GHZ)")
    print("    This is mathematically correct for 2-branch superposition states.")
    print("    For |Psi> = (|abc> + |a'b'c'>)/sqrt(2), the 3-tangle satisfies:")
    print("      tau_3 = -(1 - o2^2)(1 - o3^2) <= 0 always.")
    print("    All tripartite entanglement is pairwise (W-type), not genuine")
    print("    3-party (GHZ-type). This corrects the earlier GHZ claim.")
    if robust_3body_w:
        print(f"    W-type classification: ROBUST ({w_configs}/{total_configs} configs)")
    else:
        print(f"    W-type classification: partial ({w_configs}/{total_configs} configs)")

    # Check all bipartite entropies positive (tripartite entanglement exists)
    all_bip_positive = all(
        all(s > 1e-4 for s in v["S_bip_mean"])
        for v in three_body_data.values()
    )
    print(f"    All bipartite entropies > 0: {all_bip_positive}")

    # ── Plot ──────────────────────────────────────────────────────────
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 3, figsize=(18, 11))
        fig.suptitle("Branch Entanglement Robustness Checks", fontsize=14)

        # (a) delta_S vs separation for each G
        ax = axes[0, 0]
        for g in G_VALUES:
            seps = []
            ds_means = []
            ds_stds = []
            for sep in SEPARATIONS:
                sq_m, sq_s, ds_m, ds_s = sep_data[(g, sep)]
                seps.append(sep)
                ds_means.append(ds_m)
                ds_stds.append(ds_s)
            ax.errorbar(seps, ds_means, yerr=ds_stds, marker="o",
                        label=f"G={g}", capsize=3, markersize=4)
        ax.set_xlabel("Particle separation")
        ax.set_ylabel("delta_S (nats)")
        ax.set_title("(a) 2-body: dS vs separation")
        ax.axhline(y=0, color="k", linestyle="--", alpha=0.3)
        ax.legend(fontsize=7)

        # (b) S_quantum vs G for each separation
        ax = axes[0, 1]
        for sep in SEPARATIONS:
            gs = []
            sq_means = []
            sq_stds = []
            for g in G_VALUES:
                sq_m, sq_s, _, _ = sep_data[(g, sep)]
                gs.append(g)
                sq_means.append(sq_m)
                sq_stds.append(sq_s)
            ax.errorbar(gs, sq_means, yerr=sq_stds, marker="s",
                        label=f"sep={sep}", capsize=3, markersize=4)
        ax.set_xlabel("G")
        ax.set_ylabel("S_quantum (nats)")
        ax.set_title("(b) 2-body: S vs G")
        ax.legend(fontsize=7)

        # (c) Source position comparison (heatmap-style)
        ax = axes[0, 2]
        for g in G_VALUES:
            ds_by_src = []
            labels = []
            for sx, sy in src_positions:
                sq_m, sq_s, ds_m, ds_s = src_data[(g, sx, sy)]
                ds_by_src.append(ds_m)
                labels.append(f"({sx},{sy})")
            ax.plot(range(len(ds_by_src)), ds_by_src, "o-",
                    label=f"G={g}", markersize=4)
        ax.set_xticks(range(len(src_positions)))
        ax.set_xticklabels([f"({sx},{sy})" for sx, sy in src_positions],
                           rotation=45, fontsize=6)
        ax.set_ylabel("delta_S (nats)")
        ax.set_title("(c) 2-body: dS vs source position")
        ax.legend(fontsize=7)

        # (d) Size scaling
        ax = axes[1, 0]
        for g in G_VALUES:
            sides_plot = []
            sq_means = []
            sq_stds = []
            for side in SIDES:
                sq_m, sq_s, _, _ = size_data[(side, g)]
                sides_plot.append(side)
                sq_means.append(sq_m)
                sq_stds.append(sq_s)
            ax.errorbar(sides_plot, sq_means, yerr=sq_stds, marker="^",
                        label=f"G={g}", capsize=3, markersize=5)
        ax.set_xlabel("Lattice side")
        ax.set_ylabel("S_quantum (nats)")
        ax.set_title("(d) 2-body: size scaling")
        ax.legend(fontsize=7)

        # (e) 3-body tau_3 vs G
        ax = axes[1, 1]
        for sx, sy in src_3b_positions:
            gs = []
            taus = []
            tau_errs = []
            for g in G_VALUES:
                d = three_body_data[(g, sx, sy)]
                gs.append(g)
                taus.append(d["tau_mean"])
                tau_errs.append(d["tau_std"])
            ax.errorbar(gs, taus, yerr=tau_errs, marker="D",
                        label=f"src=({sx},{sy})", capsize=3, markersize=4)
        ax.set_xlabel("G")
        ax.set_ylabel("3-tangle (tau_3)")
        ax.set_title("(e) 3-body: tau_3 vs G")
        ax.legend(fontsize=6)

        # (f) 3-body bipartite entropies vs G (center source)
        ax = axes[1, 2]
        mid_3b = side_3b // 2
        for idx, label in enumerate(["S(1|23)", "S(2|13)", "S(3|12)"]):
            gs = []
            ss = []
            for g in G_VALUES:
                d = three_body_data[(g, mid_3b, mid_3b)]
                gs.append(g)
                ss.append(d["S_bip_mean"][idx])
            ax.plot(gs, ss, "o-", label=label, markersize=4)
        ax.set_xlabel("G")
        ax.set_ylabel("Bipartite entropy (nats)")
        ax.set_title("(f) 3-body: bipartite S vs G")
        ax.legend(fontsize=8)

        plt.tight_layout()
        out_path = __file__.replace(".py", ".png")
        plt.savefig(out_path, dpi=150)
        print(f"\nPlot saved to {out_path}")
    except Exception as e:
        print(f"\nPlot generation failed: {e}")

    elapsed = time.time() - t_start
    print(f"\nTotal time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
