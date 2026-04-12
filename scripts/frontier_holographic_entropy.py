#!/usr/bin/env python3
"""Holographic entropy: area vs volume scaling test.

Does the entanglement entropy of the path-sum propagator across a 2D
surface in a 3D lattice scale as area (L^2, holographic) or volume (L^3)?

Method:
  1. Build a 3D cubic lattice of side N.
  2. Propagate from each source on the x=0 face to the midplane x=N//2.
  3. The propagator creates an amplitude matrix M[yz_mid, yz_src] on the
     2D cross-section at x=N//2.
  4. Bipartition the midplane into A (y >= 0) and B (y < 0).
     - The reduced density matrix for A is obtained by reshaping M and
       tracing over the B indices.
  5. Compute Renyi-2 entropy: S_2 = -ln(Tr(rho_A^2)).
  6. Vary N and fit S_2 vs area (boundary perimeter L) and vs
     volume (number of sites in A).

Key prediction: S_2 ~ L^(d-1) = L^2 (area law, holographic)
                vs S_2 ~ L^d = L^3 (volume law, non-holographic).

Also test: does a gravitational field source change the entropy scaling?

Computational notes:
  - Renyi-2 avoids full diagonalization: Tr(rho_A^2) = sum_ij |rho_A[i,j]|^2
    where rho_A is obtained from the propagator matrix.
  - For tractability, use small lattices N = 6, 8, 10, 12, 14.
  - Pure Python with no numpy dependency.

PStack experiment: frontier-holographic-entropy
"""

from __future__ import annotations

import cmath
import math
import time
from collections import defaultdict, deque
from typing import Any

# ── Constants ─────────────────────────────────────────────────────────
BETA = 0.8       # directional measure width
K_DEFAULT = 4.0  # phase per action
FIELD_ITERS = 60 # Laplacian relaxation iterations for gravitational field


# ── 3D Lattice builder ───────────────────────────────────────────────

def build_3d_lattice(n_side: int) -> dict[str, Any]:
    """Build a cubic lattice with side length n_side.

    Nodes at integer coordinates (x, y, z) where:
      x in [0, n_side-1], y in [-(n_side//2), n_side//2],
      z in [-(n_side//2), n_side//2].
    Edges: forward only (dx=1), transverse |dy|<=1, |dz|<=1.

    Returns dict with positions, adjacency, layer info, and node mapping.
    """
    hw = n_side // 2  # half-width for y, z
    positions: dict[int, tuple[float, float, float]] = {}
    adj: dict[int, list[int]] = defaultdict(list)
    node_id: dict[tuple[int, int, int], int] = {}
    layer_nodes: dict[int, list[int]] = defaultdict(list)

    idx = 0
    for x in range(n_side):
        for y in range(-hw, hw + 1):
            for z in range(-hw, hw + 1):
                positions[idx] = (float(x), float(y), float(z))
                node_id[(x, y, z)] = idx
                layer_nodes[x].append(idx)
                idx += 1

    n_total = idx

    # Forward edges: dx=1, |dy|<=1, |dz|<=1
    for x in range(n_side - 1):
        for y in range(-hw, hw + 1):
            for z in range(-hw, hw + 1):
                src = node_id[(x, y, z)]
                for dy in [-1, 0, 1]:
                    for dz in [-1, 0, 1]:
                        ny2, nz2 = y + dy, z + dz
                        if -hw <= ny2 <= hw and -hw <= nz2 <= hw:
                            dst = node_id[(x + 1, ny2, nz2)]
                            adj[src].append(dst)

    return {
        "positions": positions,
        "adj": dict(adj),
        "node_id": node_id,
        "layer_nodes": dict(layer_nodes),
        "n_total": n_total,
        "hw": hw,
        "n_side": n_side,
    }


# ── Gravitational field ──────────────────────────────────────────────

def compute_field(lattice: dict, mass_ids: list[int]) -> dict[int, float]:
    """Laplacian-relaxed scalar field on the lattice for mass source."""
    adj = lattice["adj"]
    n = lattice["n_total"]

    # Build undirected adjacency for relaxation
    undirected: dict[int, list[int]] = defaultdict(list)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].append(j)
            undirected[j].append(i)

    ms = set(mass_ids)
    field = {i: (1.0 if i in ms else 0.0) for i in range(n)}

    for _ in range(FIELD_ITERS):
        nf = {}
        for i in range(n):
            if i in ms:
                nf[i] = 1.0
            elif undirected.get(i):
                nf[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
            else:
                nf[i] = 0.0
        field = nf

    return field


# ── Propagator on 3D lattice ─────────────────────────────────────────

def propagate_to_midplane(
    lattice: dict,
    source_ids: list[int],
    field: dict[int, float],
    k: float,
    cut_x: int,
) -> dict[int, dict[int, complex]]:
    """Propagate from each source independently to the midplane.

    Returns: dict mapping source_id -> {midplane_node_id: amplitude}.
    """
    positions = lattice["positions"]
    adj = lattice["adj"]
    n = lattice["n_total"]

    # Topological sort (DAG is layered by x-coordinate)
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)

    # Only keep nodes up to and including cut_x
    order = [i for i in order if positions[i][0] <= cut_x]

    midplane_ids = set(lattice["layer_nodes"].get(cut_x, []))

    result: dict[int, dict[int, complex]] = {}

    for src in source_ids:
        amps = [0j] * n
        amps[src] = 1.0 + 0j

        for i in order:
            if abs(amps[i]) < 1e-30:
                continue
            if i in midplane_ids:
                continue  # don't propagate beyond midplane
            px = positions[i][0]
            if px >= cut_x:
                continue

            for j in adj.get(i, []):
                pi = positions[i]
                pj = positions[j]
                dx = pj[0] - pi[0]
                dy = pj[1] - pi[1]
                dz = pj[2] - pi[2]
                L = math.sqrt(dx * dx + dy * dy + dz * dz)
                if L < 1e-10:
                    continue
                # Directional measure
                cos_theta = dx / L
                theta = math.acos(min(max(cos_theta, -1.0), 1.0))
                w = math.exp(-BETA * theta * theta)
                # Field-modified action
                lf = 0.5 * (field.get(i, 0.0) + field.get(j, 0.0))
                dl = L * (1.0 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0.0))
                act = dl - ret
                ea = cmath.exp(1j * k * act) * w / L
                amps[j] += amps[i] * ea

        # Collect midplane amplitudes
        mid_amps: dict[int, complex] = {}
        for mid_id in midplane_ids:
            if abs(amps[mid_id]) > 1e-30:
                mid_amps[mid_id] = amps[mid_id]

        if mid_amps:
            result[src] = mid_amps

    return result


# ── Bipartition and entropy ──────────────────────────────────────────

def bipartition_midplane(
    lattice: dict,
    cut_x: int,
) -> tuple[list[int], list[int]]:
    """Split midplane nodes into A (y >= 0) and B (y < 0).

    Returns (A_ids, B_ids) as sorted lists.
    """
    positions = lattice["positions"]
    mid_nodes = lattice["layer_nodes"].get(cut_x, [])

    region_a = sorted(i for i in mid_nodes if positions[i][1] >= 0)
    region_b = sorted(i for i in mid_nodes if positions[i][1] < 0)

    return region_a, region_b


def compute_renyi2_entropy(
    propagator: dict[int, dict[int, complex]],
    region_a: list[int],
    region_b: list[int],
) -> dict[str, float]:
    """Compute Renyi-2 entropy of the reduced density matrix for region A.

    The state on the midplane is:
      |psi> = sum_{src} |midplane amplitudes from src>
    represented as M[mid_id, src_id].

    We reshape M into M[a, b, src] where a indexes region_a sites and
    b indexes region_b sites, then trace over B to get:
      rho_A[a, a'] = sum_{b, src, src'} M[a,b,src] * conj(M[a',b,src'])

    But actually, we use the propagator matrix directly:
      M[mid, src] = amplitude at mid from source src
    The full state (unnormalized) is |psi> with amplitudes M[mid, src]
    in the (mid, src) product space. Tracing over src gives:
      rho_mid[mid, mid'] = sum_src M[mid, src] conj(M[mid', src])
    Then tracing over B subset of mid gives:
      rho_A[a, a'] = sum_{b in B_union_A} ... no, the correct procedure is:

    The propagator creates a bipartite entangled state between source face
    and midplane. The midplane state (tracing over sources) is:
      rho_mid = M @ M^dag (where M is the amplitude matrix).
    Then rho_A = Tr_B(rho_mid) -- trace over the B subset of the midplane.

    For Renyi-2: S_2 = -ln(Tr(rho_A^2)).
    Tr(rho_A^2) = sum_{a,a'} |rho_A[a,a']|^2.
    """
    sources = sorted(propagator.keys())
    all_mid = sorted(set().union(*(propagator[s].keys() for s in sources)))

    if not sources or not all_mid:
        return {"S2": 0.0, "tr_rho2": 1.0, "rank_est": 0, "n_A": 0, "n_B": 0}

    a_set = set(region_a)
    b_set = set(region_b)
    a_in_mid = sorted(a_set & set(all_mid))
    b_in_mid = sorted(b_set & set(all_mid))

    n_a = len(a_in_mid)
    n_b = len(b_in_mid)
    n_src = len(sources)

    if n_a == 0:
        return {"S2": 0.0, "tr_rho2": 1.0, "rank_est": 0, "n_A": 0, "n_B": n_b}

    # Build M matrix: M[mid_idx, src_idx]
    # Index mapping
    a_idx = {nid: i for i, nid in enumerate(a_in_mid)}
    b_idx = {nid: i for i, nid in enumerate(b_in_mid)}
    src_idx = {sid: j for j, sid in enumerate(sources)}

    # Build the full midplane amplitude matrix
    # M_full[mid, src] for all midplane nodes
    # Then compute rho_mid = M_full @ M_full^dag
    # Then trace over B to get rho_A

    # For efficiency, compute rho_A directly:
    # rho_A[a, a'] = sum_b sum_{s,s'} M[(a,b),s] * conj(M[(a',b),s'])
    # But midplane nodes aren't in a product (a,b) space --
    # they're individual sites. The trace over B means:
    # rho_A[a, a'] = sum_s M[a, s] * conj(M[a', s])
    #              + delta(a, a') * sum_{b in B} sum_s |M[b, s]|^2
    # NO -- that's wrong. Let me think more carefully.
    #
    # The density matrix on the full midplane is:
    #   rho_mid[i, j] = sum_s M[i, s] * conj(M[j, s])
    # where i, j are midplane node IDs.
    #
    # The partial trace over B gives:
    #   rho_A[a, a'] = rho_mid[a, a']    for a, a' in A
    #
    # because Tr_B(|i><j|) = delta_{i_B, j_B} * |i_A><j_A|
    # and since midplane nodes are individual sites (not tensor products),
    # tracing over B just means restricting to the A x A block.
    #
    # Wait -- this is the critical subtlety. The midplane Hilbert space
    # is a SINGLE particle space (amplitude at each site), not a tensor
    # product. For a single-particle state, tracing over a spatial region
    # means projecting onto the subspace:
    #   rho_A[a, a'] = rho_mid[a, a']   (just the A-block!)
    #
    # This is correct for single-particle entanglement entropy.
    # The entropy measures how spread the particle is between A and B.

    # Build rho_A[a, a'] = sum_s M[a, s] * conj(M[a', s])
    # This is the A-block of rho_mid = M @ M^dag

    # First normalize: Tr(rho_mid) = sum_i sum_s |M[i,s]|^2 = 1
    norm_sq = 0.0
    for s in sources:
        for mid_id, amp in propagator[s].items():
            norm_sq += abs(amp) ** 2
    norm = math.sqrt(norm_sq) if norm_sq > 1e-30 else 1.0

    # Build rho_A (n_a x n_a)
    rho_a: list[list[complex]] = [[0j] * n_a for _ in range(n_a)]

    for si, s in enumerate(sources):
        # Get normalized amplitudes at A sites from this source
        a_amps: list[complex] = [0j] * n_a
        for mid_id, amp in propagator[s].items():
            if mid_id in a_idx:
                a_amps[a_idx[mid_id]] = amp / norm

        # Outer product contribution: rho_A += a_amps @ a_amps^dag
        for i in range(n_a):
            if abs(a_amps[i]) < 1e-30:
                continue
            for j in range(n_a):
                rho_a[i][j] += a_amps[i] * a_amps[j].conjugate()

    # Tr(rho_A) should be < 1 (the probability of finding particle in A)
    tr_a = sum(rho_a[i][i].real for i in range(n_a))

    # Renyi-2: S_2 = -ln(Tr(rho_A^2))
    # But we need to normalize rho_A first: rho_A_norm = rho_A / Tr(rho_A)
    # Then S_2 = -ln(Tr(rho_A_norm^2))
    if tr_a < 1e-30:
        return {"S2": 0.0, "tr_rho2": 1.0, "rank_est": 0, "n_A": n_a, "n_B": n_b}

    # Normalize
    for i in range(n_a):
        for j in range(n_a):
            rho_a[i][j] /= tr_a

    # Tr(rho_A^2) = sum_{i,j} |rho_A[i,j]|^2
    tr_rho2 = 0.0
    for i in range(n_a):
        for j in range(n_a):
            tr_rho2 += abs(rho_a[i][j]) ** 2

    s2 = -math.log(max(tr_rho2, 1e-30))

    # Estimate effective rank from Tr(rho^2) ~ 1/r_eff
    rank_est = 1.0 / max(tr_rho2, 1e-30)

    return {
        "S2": s2,
        "tr_rho2": tr_rho2,
        "rank_est": rank_est,
        "n_A": n_a,
        "n_B": n_b,
        "tr_A_unnorm": tr_a,
    }


# Also compute von Neumann entropy for comparison on small matrices
def von_neumann_entropy_from_rho(
    propagator: dict[int, dict[int, complex]],
    region_a: list[int],
    region_b: list[int],
) -> float:
    """Compute S_vN for the reduced density matrix of region A.

    Uses Jacobi eigenvalue solver. Only practical for small n_A.
    """
    sources = sorted(propagator.keys())
    all_mid = sorted(set().union(*(propagator[s].keys() for s in sources)))

    if not sources or not all_mid:
        return 0.0

    a_set = set(region_a)
    a_in_mid = sorted(a_set & set(all_mid))
    n_a = len(a_in_mid)
    if n_a == 0 or n_a > 80:  # skip if too large for Jacobi
        return -1.0

    a_idx = {nid: i for i, nid in enumerate(a_in_mid)}

    # Normalization
    norm_sq = 0.0
    for s in sources:
        for mid_id, amp in propagator[s].items():
            norm_sq += abs(amp) ** 2
    norm = math.sqrt(norm_sq) if norm_sq > 1e-30 else 1.0

    # Build rho_A
    rho_a: list[list[complex]] = [[0j] * n_a for _ in range(n_a)]
    for s in sources:
        a_amps = [0j] * n_a
        for mid_id, amp in propagator[s].items():
            if mid_id in a_idx:
                a_amps[a_idx[mid_id]] = amp / norm
        for i in range(n_a):
            if abs(a_amps[i]) < 1e-30:
                continue
            for j in range(n_a):
                rho_a[i][j] += a_amps[i] * a_amps[j].conjugate()

    tr_a = sum(rho_a[i][i].real for i in range(n_a))
    if tr_a < 1e-30:
        return 0.0
    for i in range(n_a):
        for j in range(n_a):
            rho_a[i][j] /= tr_a

    # Jacobi eigenvalue decomposition
    eigenvalues = hermitian_eigenvalues(rho_a)
    entropy = 0.0
    for lam in eigenvalues:
        if lam > 1e-15:
            entropy -= lam * math.log(lam)
    return entropy


def hermitian_eigenvalues(h: list[list[complex]], max_iter: int = 500) -> list[float]:
    """Eigenvalues of a complex Hermitian matrix via Jacobi rotations."""
    n = len(h)
    if n == 0:
        return []
    if n == 1:
        return [h[0][0].real]

    a = [[h[i][j] for j in range(n)] for i in range(n)]

    for i in range(n):
        a[i][i] = complex(a[i][i].real, 0.0)
        for j in range(i + 1, n):
            avg = 0.5 * (a[i][j] + a[j][i].conjugate())
            a[i][j] = avg
            a[j][i] = avg.conjugate()

    for _sweep in range(max_iter):
        max_val = 0.0
        p, q = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                mag = abs(a[i][j])
                if mag > max_val:
                    max_val = mag
                    p, q = i, j
        if max_val < 1e-14:
            break

        z = a[p][q]
        mag_z = abs(z)
        if mag_z < 1e-30:
            continue

        phase = z / mag_z
        phase_conj = phase.conjugate()

        app = a[p][p].real
        aqq = a[q][q].real
        diff = app - aqq

        if abs(diff) < 1e-30:
            theta = math.pi / 4
        else:
            theta = 0.5 * math.atan2(2.0 * mag_z, diff)

        c = math.cos(theta)
        s = math.sin(theta)

        for i in range(n):
            if i == p or i == q:
                continue
            aip = a[i][p]
            aiq = a[i][q]
            a[i][p] = c * aip + s * phase_conj * aiq
            a[p][i] = a[i][p].conjugate()
            a[i][q] = -s * phase * aip + c * aiq
            a[q][i] = a[i][q].conjugate()

        new_pp = c * c * app + 2 * c * s * mag_z + s * s * aqq
        new_qq = s * s * app - 2 * c * s * mag_z + c * c * aqq
        a[p][p] = complex(new_pp, 0.0)
        a[q][q] = complex(new_qq, 0.0)
        a[p][q] = 0j
        a[q][p] = 0j

    return sorted(a[i][i].real for i in range(n))


# ── Fitting utilities ─────────────────────────────────────────────────

def linear_fit(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    """Return (slope, intercept, R^2) for y = slope*x + intercept."""
    n = len(xs)
    if n < 2:
        return 0.0, 0.0, 0.0
    x_mean = sum(xs) / n
    y_mean = sum(ys) / n
    ss_xx = sum((x - x_mean) ** 2 for x in xs)
    ss_yy = sum((y - y_mean) ** 2 for y in ys)
    ss_xy = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    if ss_xx < 1e-30:
        return 0.0, y_mean, 0.0
    slope = ss_xy / ss_xx
    intercept = y_mean - slope * x_mean
    r2 = (ss_xy ** 2) / (ss_xx * ss_yy) if ss_yy > 1e-30 else 0.0
    return slope, intercept, r2


# ── Main experiment ───────────────────────────────────────────────────

def run_single(
    n_side: int,
    k: float,
    with_mass: bool = False,
) -> dict[str, Any]:
    """Run holographic entropy measurement for a single lattice size."""
    t0 = time.time()

    lattice = build_3d_lattice(n_side)
    cut_x = n_side // 2
    hw = lattice["hw"]

    # Sources: all nodes on x=0 face
    source_ids = lattice["layer_nodes"][0]

    # Field
    if with_mass:
        # Mass cluster near center of midplane
        node_id = lattice["node_id"]
        mass_ids = []
        cx, cy, cz = cut_x, 0, 0
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                key = (cx, cy + dy, cz + dz)
                if key in node_id:
                    mass_ids.append(node_id[key])
        field = compute_field(lattice, mass_ids)
    else:
        field = {i: 0.0 for i in range(lattice["n_total"])}

    # Propagate from each source to midplane
    propagator = propagate_to_midplane(lattice, source_ids, field, k, cut_x)

    # Bipartition midplane
    region_a, region_b = bipartition_midplane(lattice, cut_x)

    # Compute Renyi-2 entropy
    renyi = compute_renyi2_entropy(propagator, region_a, region_b)

    # Compute von Neumann entropy for small lattices
    s_vn = von_neumann_entropy_from_rho(propagator, region_a, region_b)

    elapsed = time.time() - t0

    # Geometric quantities
    n_mid = len(lattice["layer_nodes"].get(cut_x, []))
    # Boundary between A and B: nodes in A adjacent to nodes in B
    # In our bipartition (y >= 0 vs y < 0), the boundary is the
    # set of A-nodes with y = 0 (adjacent to B-nodes with y = -1)
    positions = lattice["positions"]
    boundary_count = sum(
        1 for nid in region_a
        if abs(positions[nid][1]) < 0.5  # y = 0 row
    )

    return {
        "n_side": n_side,
        "n_mid": n_mid,
        "n_A": renyi["n_A"],
        "n_B": renyi["n_B"],
        "boundary": boundary_count,
        "S2": renyi["S2"],
        "S_vN": s_vn,
        "tr_rho2": renyi["tr_rho2"],
        "rank_est": renyi["rank_est"],
        "tr_A_unnorm": renyi.get("tr_A_unnorm", 0.0),
        "with_mass": with_mass,
        "elapsed": elapsed,
    }


def main() -> None:
    print("=" * 80)
    print("HOLOGRAPHIC ENTROPY: AREA vs VOLUME SCALING TEST")
    print("=" * 80)
    print()
    print("Method:")
    print("  - 3D cubic lattice, corrected propagator with directional measure")
    print("  - Propagate from x=0 face to midplane x=N//2")
    print("  - Bipartition midplane: A = {y >= 0}, B = {y < 0}")
    print("  - Compute Renyi-2 entropy S_2 = -ln(Tr(rho_A^2))")
    print("  - Also compute S_vN via Jacobi eigenvalues (small lattices)")
    print()
    print("Prediction: S ~ L^(d-1) = L^2 (area law / holographic)")
    print("         vs S ~ L^d    = L^3 (volume law)")
    print()

    k = K_DEFAULT
    # Use modest sizes for tractability in pure Python
    sizes = [4, 6, 8, 10, 12]

    print(f"Parameters: k={k}, beta={BETA}, field_iters={FIELD_ITERS}")
    print(f"Lattice sizes: {sizes}")
    print()

    # ===================================================================
    # Experiment A: Free space, vary lattice size
    # ===================================================================
    print("EXPERIMENT A: Free space -- vary lattice size")
    print("-" * 78)
    header = (f"{'N':>3} {'n_mid':>6} {'n_A':>5} {'n_B':>5} {'bnd':>4} "
              f"{'S_2':>10} {'S_vN':>10} {'Tr(rho2)':>10} {'r_eff':>6} "
              f"{'P(A)':>6} {'t(s)':>6}")
    print(header)
    print("-" * len(header))

    results_free: list[dict] = []
    for n_side in sizes:
        r = run_single(n_side, k, with_mass=False)
        results_free.append(r)
        svn_str = f"{r['S_vN']:.6f}" if r["S_vN"] >= 0 else "   N/A"
        print(f"{r['n_side']:>3} {r['n_mid']:>6} {r['n_A']:>5} {r['n_B']:>5} "
              f"{r['boundary']:>4} "
              f"{r['S2']:>10.6f} {svn_str:>10} {r['tr_rho2']:>10.6f} "
              f"{r['rank_est']:>6.1f} {r['tr_A_unnorm']:>6.4f} "
              f"{r['elapsed']:>6.1f}")

    # ===================================================================
    # Experiment B: With mass source
    # ===================================================================
    print()
    print("EXPERIMENT B: With gravitational mass at midplane center")
    print("-" * 78)
    print(header)
    print("-" * len(header))

    results_mass: list[dict] = []
    for n_side in sizes:
        r = run_single(n_side, k, with_mass=True)
        results_mass.append(r)
        svn_str = f"{r['S_vN']:.6f}" if r["S_vN"] >= 0 else "   N/A"
        print(f"{r['n_side']:>3} {r['n_mid']:>6} {r['n_A']:>5} {r['n_B']:>5} "
              f"{r['boundary']:>4} "
              f"{r['S2']:>10.6f} {svn_str:>10} {r['tr_rho2']:>10.6f} "
              f"{r['rank_est']:>6.1f} {r['tr_A_unnorm']:>6.4f} "
              f"{r['elapsed']:>6.1f}")

    # ===================================================================
    # Scaling analysis
    # ===================================================================
    print()
    print("=" * 80)
    print("SCALING ANALYSIS")
    print("=" * 80)

    # Extract scaling data
    s2_free = [r["S2"] for r in results_free]
    s2_mass = [r["S2"] for r in results_mass]
    n_a_vals = [float(r["n_A"]) for r in results_free]
    bnd_vals = [float(r["boundary"]) for r in results_free]
    n_side_vals = [float(r["n_side"]) for r in results_free]

    # Log-log fits for power law
    # S vs n_A (should be area=n_A^(2/3) for volume law n_A^1)
    # S vs boundary (should be ~boundary^1 for area law)

    # Filter out zeros
    valid = [(i, s) for i, s in enumerate(s2_free) if s > 1e-10]
    if len(valid) >= 3:
        vi = [v[0] for v in valid]

        # Log-log: S_2 vs boundary (area proxy)
        log_bnd = [math.log(bnd_vals[i]) for i in vi if bnd_vals[i] > 0]
        log_s2 = [math.log(s2_free[i]) for i in vi if bnd_vals[i] > 0]
        if len(log_bnd) >= 3:
            alpha_bnd, _, r2_bnd = linear_fit(log_bnd, log_s2)
            print(f"\n  FREE SPACE:")
            print(f"    S_2 vs boundary (log-log): exponent = {alpha_bnd:.3f}, R^2 = {r2_bnd:.4f}")

        # Log-log: S_2 vs n_A (volume proxy)
        log_na = [math.log(n_a_vals[i]) for i in vi if n_a_vals[i] > 0]
        log_s2_na = [math.log(s2_free[i]) for i in vi if n_a_vals[i] > 0]
        if len(log_na) >= 3:
            alpha_vol, _, r2_vol = linear_fit(log_na, log_s2_na)
            print(f"    S_2 vs n_A (volume, log-log): exponent = {alpha_vol:.3f}, R^2 = {r2_vol:.4f}")

        # Log-log: S_2 vs N (side length)
        log_n = [math.log(n_side_vals[i]) for i in vi]
        log_s2_n = [math.log(s2_free[i]) for i in vi]
        if len(log_n) >= 3:
            alpha_n, _, r2_n = linear_fit(log_n, log_s2_n)
            print(f"    S_2 vs N (side, log-log): exponent = {alpha_n:.3f}, R^2 = {r2_n:.4f}")
            print()
            print(f"    Interpretation:")
            print(f"      Area law (holographic): S ~ N^2 => exponent ~ 2")
            print(f"      Volume law:             S ~ N^3 => exponent ~ 3")
            print(f"      Sub-area (1D boundary): S ~ N^1 => exponent ~ 1")
            print(f"      Measured exponent:       {alpha_n:.2f}")
            if 1.5 < alpha_n < 2.5 and r2_n > 0.8:
                print(f"      ==> AREA LAW SCALING (holographic)")
            elif alpha_n > 2.5 and r2_n > 0.8:
                print(f"      ==> SUPER-AREA / VOLUME LAW SCALING")
            elif 0.5 < alpha_n < 1.5 and r2_n > 0.8:
                print(f"      ==> SUB-AREA LAW (logarithmic or 1D)")
            elif alpha_n < 0.5:
                print(f"      ==> SATURATING (entropy bounded)")
            else:
                print(f"      ==> INCONCLUSIVE (R^2={r2_n:.3f})")

    # Mass comparison
    valid_mass = [(i, s) for i, s in enumerate(s2_mass) if s > 1e-10]
    if len(valid_mass) >= 3:
        vi_m = [v[0] for v in valid_mass]
        log_n_m = [math.log(n_side_vals[i]) for i in vi_m]
        log_s2_m = [math.log(s2_mass[i]) for i in vi_m]
        if len(log_n_m) >= 3:
            alpha_n_m, _, r2_n_m = linear_fit(log_n_m, log_s2_m)
            print(f"\n  WITH MASS:")
            print(f"    S_2 vs N (side, log-log): exponent = {alpha_n_m:.3f}, R^2 = {r2_n_m:.4f}")

    # Delta S
    print(f"\n  GRAVITATIONAL ENTROPY SHIFT:")
    print(f"  {'N':>3} {'S2_free':>10} {'S2_mass':>10} {'dS2':>10}")
    print(f"  {'-'*36}")
    for rf, rm in zip(results_free, results_mass):
        ds = rm["S2"] - rf["S2"]
        print(f"  {rf['n_side']:>3} {rf['S2']:>10.6f} {rm['S2']:>10.6f} {ds:>+10.6f}")

    ds_vals = [rm["S2"] - rf["S2"] for rf, rm in zip(results_free, results_mass)]
    ds_mean = sum(ds_vals) / len(ds_vals) if ds_vals else 0.0

    # ===================================================================
    # Experiment C: Fixed lattice, vary cut position
    # ===================================================================
    print()
    print("=" * 80)
    print("EXPERIMENT C: Fixed N=10, vary bipartition asymmetry")
    print("=" * 80)
    print()
    print("Test: does S depend on HOW we cut, not just the boundary size?")
    print("For a y-bipartition at different y_cut values, boundary size is")
    print("the same but the ratio n_A/n_B changes.")
    print()

    n_fixed = 10
    lattice_c = build_3d_lattice(n_fixed)
    cut_x_c = n_fixed // 2
    hw_c = lattice_c["hw"]

    source_ids_c = lattice_c["layer_nodes"][0]
    field_c = {i: 0.0 for i in range(lattice_c["n_total"])}
    prop_c = propagate_to_midplane(lattice_c, source_ids_c, field_c, k, cut_x_c)

    positions_c = lattice_c["positions"]
    mid_nodes_c = lattice_c["layer_nodes"].get(cut_x_c, [])

    print(f"  {'y_cut':>5} {'n_A':>5} {'n_B':>5} {'bnd':>4} {'S_2':>10} {'S_vN':>10}")
    print(f"  {'-'*44}")

    # Vary the bipartition: A = {y >= y_cut}, B = {y < y_cut}
    for y_cut in range(-hw_c + 1, hw_c + 1):
        region_a_c = sorted(
            nid for nid in mid_nodes_c if positions_c[nid][1] >= y_cut
        )
        region_b_c = sorted(
            nid for nid in mid_nodes_c if positions_c[nid][1] < y_cut
        )
        if not region_a_c or not region_b_c:
            continue

        renyi_c = compute_renyi2_entropy(prop_c, region_a_c, region_b_c)
        svn_c = von_neumann_entropy_from_rho(prop_c, region_a_c, region_b_c)

        # Boundary: A-nodes with y = y_cut (adjacent to B at y = y_cut - 1)
        bnd_c = sum(
            1 for nid in region_a_c
            if abs(positions_c[nid][1] - y_cut) < 0.5
        )
        svn_str = f"{svn_c:.6f}" if svn_c >= 0 else "   N/A"
        print(f"  {y_cut:>5} {renyi_c['n_A']:>5} {renyi_c['n_B']:>5} "
              f"{bnd_c:>4} {renyi_c['S2']:>10.6f} {svn_str:>10}")

    # ===================================================================
    # Summary
    # ===================================================================
    print()
    print("=" * 80)
    print("SUMMARY AND INTERPRETATION")
    print("=" * 80)

    print()
    print("1. ENTROPY SCALING (Experiment A, free space):")
    if len(valid) >= 3:
        print(f"   S_2 vs N power law exponent: {alpha_n:.2f} (R^2={r2_n:.3f})")
        if 1.5 < alpha_n < 2.5 and r2_n > 0.8:
            print(f"   RESULT: Area law scaling (S ~ N^2, holographic)")
            print(f"   This is consistent with the holographic principle:")
            print(f"   entanglement entropy scales as the boundary area, not volume.")
        elif alpha_n > 2.5 and r2_n > 0.8:
            print(f"   RESULT: Volume or super-area scaling (S ~ N^{alpha_n:.1f})")
            print(f"   The propagator creates volume-law entanglement,")
            print(f"   which is NOT holographic.")
        elif 0.5 < alpha_n < 1.5 and r2_n > 0.8:
            print(f"   RESULT: Sub-area scaling (S ~ N^{alpha_n:.1f})")
            print(f"   Below the area law, possibly logarithmic correction.")
        else:
            print(f"   RESULT: Inconclusive (exponent={alpha_n:.2f}, R^2={r2_n:.3f})")
    else:
        print(f"   Insufficient data for scaling fit.")

    print(f"\n2. GRAVITATIONAL EFFECT (Experiments A vs B):")
    print(f"   Mean dS_2 (mass - free) = {ds_mean:+.6f}")
    if abs(ds_mean) > 0.01:
        direction = "increases" if ds_mean > 0 else "decreases"
        print(f"   Mass {direction} entanglement entropy by {abs(ds_mean):.4f}")
        if ds_mean > 0:
            print(f"   Consistent with: gravity enhances correlations across boundary")
        else:
            print(f"   Consistent with: gravity focuses the wavepacket (less spread)")
    else:
        print(f"   Negligible gravitational effect on entropy (|dS| < 0.01)")

    print(f"\n3. BIPARTITION DEPENDENCE (Experiment C):")
    print(f"   Symmetric cut should maximize entropy (confirmed if S peaks at y=0)")
    print(f"   Entropy should drop as the cut becomes more asymmetric")

    print(f"\n4. OVERCLAIMING GUARD:")
    print(f"   - Single-particle entanglement entropy is a PROXY, not full QFT")
    print(f"   - Area law in free lattice propagator is a NECESSARY condition")
    print(f"     for holographic behavior, not sufficient")
    print(f"   - The d=3 lattice sizes ({sizes}) are modest; finite-size")
    print(f"     effects may be significant")
    print(f"   - Gravitational entropy shift is qualitative, not quantitative")
    print()


if __name__ == "__main__":
    main()
