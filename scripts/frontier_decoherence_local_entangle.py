#!/usr/bin/env python3
"""Local entangling decoherence vs Caldeira-Leggett bath.

HYPOTHESIS: Local entangling gives purity ~ exp(-alpha*N), breaking the
CL power-law ceiling where purity -> 1 as N grows.

APPROACH:
  Build rectangular DAGs with a barrier + two slits. Propagate amplitude
  from each slit separately to get psi_A(y) and psi_B(y) at the detector.

  CL bath (current):
    Bin detector amplitudes into N_YBINS. Compute contrast S.
    D = exp(-lambda^2 * S). Purity from Gram matrix.

  Local entanglement (new):
    Divide post-barrier region into environment zones (layers).
    At each zone, decoherence factor = eps_0 * |psi_A - psi_B|^2 locally.
    D_total = exp(-eps_0 * sum_zones |Delta_psi|^2)
    Key: sum of LOCAL contrasts grows with N (more zones), so D -> 0.

FALSIFICATION: If local model also shows power-law purity decay,
the ceiling is fundamental.

PStack experiment: decoherence-local-entangle
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# Pure-Python linear algebra helpers (no numpy)
# ---------------------------------------------------------------------------

def vec_norm(v):
    """L2 norm of a list of complex numbers."""
    return math.sqrt(sum(abs(x)**2 for x in v))


def vec_scale(v, s):
    return [x * s for x in v]


def vec_diff_sq_sum(a, b):
    """sum |a_i - b_i|^2"""
    return sum(abs(ai - bi)**2 for ai, bi in zip(a, b))


def vec_dot(a, b):
    """<a|b> = sum a_i* b_i"""
    return sum(ai.conjugate() * bi for ai, bi in zip(a, b))


def gram_purity_2slit(psi_a, psi_b, D):
    """Compute Tr(rho^2) for the 2-slit density matrix.

    rho = (|a><a| + |b><b| + D(|a><b| + |b><a|)) / Tr(...)
    Tr(rho^2) can be computed from the overlaps without building the full matrix.

    Let s = <a|b>. Then:
      Tr(rho) = 2 + 2D Re(s)
      Tr(rho^2) = (2 + 2D^2|s|^2 + 4D Re(s)) / Tr(rho)^2
    Wait -- that's for un-normalized rho. Let's derive properly.

    rho_unnorm = |a><a| + |b><b| + D|a><b| + D|b><a|
    Tr(rho_unnorm) = <a|a> + <b|b> + D<b|a> + D<a|b>
                   = 1 + 1 + 2D Re(s)  [assuming psi normalized]
                   = 2 + 2D Re(s)
    rho = rho_unnorm / T  where T = 2 + 2D Re(s)

    Tr(rho^2) = Tr(rho_unnorm^2) / T^2

    rho_unnorm^2 = |a><a|a><a| + |a><a|b><b| + D|a><a|a><b| + D|a><a|b><a|
                 + |b><b|a><a| + |b><b|b><b| + D|b><b|a><b| + D|b><b|b><a|
                 + D|a><b|a><a| + D|a><b|b><b| + D^2|a><b|a><b| + D^2|a><b|b><a|
                 + D|b><a|a><a| + D|b><a|b><b| + D^2|b><a|a><b| + D^2|b><a|b><a|

    Tr(rho_unnorm^2) = <a|a> + <a|b><b|a> + D<a|a><b|a> + D<a|b><a|a>
                      + <b|a><a|b> + <b|b> + D<b|a><b|b> + D<b|b><a|b>
                      + D<b|a><a|a> + D<b|b><a|b> + D^2<b|a><a|b> + D^2<b|b><a|a>
                      ... this is getting complicated. Let me use the formula:

    Tr(rho_unnorm^2) = sum_{ij} |rho_unnorm_{ij}|^2  [since rho is Hermitian]

    Actually for a rank-at-most-2 matrix, it's simpler:
    Tr(X^2) where X = |a><a| + |b><b| + D(|a><b| + |b><a|)

    Using |a>, |b> as (possibly non-orthogonal) basis:
    The Gram matrix G of rho_unnorm in this basis is:
      G = [[1+D*s, s+D], [s*+D, 1+D*s*]]
    where s = <a|b>.

    Actually, let me just use: Tr(X^2) = Tr(X)^2 requires computing
    the matrix elements. For efficiency, note:

    Tr(rho_unnorm^2) = (1 + |s|^2 + 2D Re(s)) + (|s|^2 + 1 + 2D Re(s))
                       + D^2(|s|^2 + 1) + ... no, let me do it right.

    Let s = <a|b>. Then:
      <a|rho_unnorm|a> = 1 + |s|^2 + 2D Re(s)
      <b|rho_unnorm|b> = |s|^2 + 1 + 2D Re(s)
      <a|rho_unnorm|b> = s + s|s|^2... no.

    Let me just compute it the direct way for small vectors.
    """
    n = len(psi_a)
    s = vec_dot(psi_a, psi_b)  # <a|b>
    re_s = s.real
    abs_s2 = abs(s)**2

    T = 2.0 + 2.0 * D * re_s
    if abs(T) < 1e-30:
        return 1.0

    # Tr(rho_unnorm^2):
    # Expanding: each term |x><y| contributes <y|z><w|x> from |z><w|
    # Tr(AB) = sum_i (AB)_{ii} = sum_i sum_j A_{ij} B_{ji}
    # For A = B = rho_unnorm = sum of rank-1 terms:
    # |a><a|, |b><b|, D|a><b|, D|b><a|
    #
    # Tr(rho^2) = sum over all pairs of rank-1 terms P, Q: Tr(PQ)
    # Tr(|u><v| |w><x|) = <v|w><x|u>
    #
    # 16 terms:
    # (aa,aa): <a|a><a|a> = 1
    # (aa,bb): <a|b><b|a> = |s|^2
    # (aa,D ab): D<a|a><b|a> = D s*
    # (aa,D ba): D<a|b><a|a> = D s
    # (bb,aa): <b|a><a|b> = |s|^2
    # (bb,bb): <b|b><b|b> = 1
    # (bb,D ab): D<b|a><b|b> = D s*
    # (bb,D ba): D<b|b><a|b> = D s
    # (D ab,aa): D<b|a><a|a> = D s*
    # (D ab,bb): D<b|b><b|a> = D s*
    # (D ab,D ab): D^2<b|a><b|a> = D^2 (s*)^2
    # (D ab,D ba): D^2<b|b><a|a> = D^2
    # (D ba,aa): D<a|a><a|b> = D s
    # (D ba,bb): D<a|b><b|b> = D s
    # (D ba,D ab): D^2<a|a><b|b> = D^2
    # (D ba,D ba): D^2<a|b><a|b> = D^2 s^2

    tr_sq = (1.0 + abs_s2 + D*s.conjugate() + D*s
             + abs_s2 + 1.0 + D*s.conjugate() + D*s
             + D*s.conjugate() + D*s.conjugate() + D**2 * s.conjugate()**2 + D**2
             + D*s + D*s + D**2 + D**2 * s**2)

    tr_sq_real = tr_sq.real  # should be real for Hermitian matrix
    purity = tr_sq_real / (T * T)
    return max(0.0, min(1.0, purity))


def simple_polyfit_1d(xs, ys):
    """Least-squares fit y = a*x + b. Returns (a, b)."""
    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxx = sum(x*x for x in xs)
    sxy = sum(x*y for x, y in zip(xs, ys))
    denom = n * sxx - sx * sx
    if abs(denom) < 1e-30:
        return 0.0, sy / n if n else 0.0
    a = (n * sxy - sx * sy) / denom
    b = (sy - a * sx) / n
    return a, b


# ---------------------------------------------------------------------------
# DAG construction: rectangular lattice with barrier + two slits
# ---------------------------------------------------------------------------

def build_rectangular_dag(width, height):
    """Build a rectangular DAG: nodes on integer grid, edges go right."""
    positions = []
    node_id = {}
    for x in range(width):
        for y in range(height):
            idx = len(positions)
            positions.append((float(x), float(y)))
            node_id[(x, y)] = idx

    adj = defaultdict(list)
    for x in range(width - 1):
        for y in range(height):
            src = node_id[(x, y)]
            for dy in [-1, 0, 1]:
                ny = y + dy
                if 0 <= ny < height:
                    tgt = node_id[(x + 1, ny)]
                    adj[src].append(tgt)

    return positions, dict(adj), node_id


def setup_two_slit(width, height, node_id):
    """Place barrier at x = width//3, with two slits."""
    barrier_x = width // 3

    slit_a_y = height // 4
    slit_b_y = 3 * height // 4

    blocked = set()
    slit_a = []
    slit_b = []
    for y in range(height):
        nid = node_id.get((barrier_x, y))
        if nid is None:
            continue
        if abs(y - slit_a_y) <= 1:
            slit_a.append(nid)
        elif abs(y - slit_b_y) <= 1:
            slit_b.append(nid)
        else:
            blocked.add(nid)

    sources = [node_id[(0, y)] for y in range(height)]
    detectors = [node_id[(width - 1, y)] for y in range(height)]

    return sources, detectors, blocked, slit_a, slit_b, barrier_x


# ---------------------------------------------------------------------------
# Propagation
# ---------------------------------------------------------------------------

def full_propagate(positions, adj, sources, blocked, k):
    """Propagate amplitude, return all node amplitudes as dict."""
    n = len(positions)
    in_deg = [0] * n
    for i, nbs in adj.items():
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

    amp = defaultdict(complex)
    n_src = len([s for s in sources if s not in blocked])
    if n_src == 0:
        return {}
    init = 1.0 / n_src
    for s in sources:
        if s not in blocked:
            amp[s] = init

    for i in order:
        if i in blocked or abs(amp[i]) < 1e-30:
            continue
        a = amp[i]
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            L = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            if L < 1e-10:
                continue
            phase = cmath.exp(1j * k * L) / L
            amp[j] += a * phase

    return dict(amp)


# ---------------------------------------------------------------------------
# Decoherence models
# ---------------------------------------------------------------------------

def cl_bath_purity(det_amps_a, det_amps_b, det_nodes, lam=1.0):
    """Caldeira-Leggett bath model purity."""
    psi_a = [det_amps_a.get(d, 0.0+0j) for d in det_nodes]
    psi_b = [det_amps_b.get(d, 0.0+0j) for d in det_nodes]

    na = vec_norm(psi_a)
    nb = vec_norm(psi_b)
    if na < 1e-30 or nb < 1e-30:
        return 1.0

    psi_a = vec_scale(psi_a, 1.0/na)
    psi_b = vec_scale(psi_b, 1.0/nb)

    # Contrast: S = sum |psi_a - psi_b|^2
    contrast = vec_diff_sq_sum(psi_a, psi_b)

    D = math.exp(-lam**2 * contrast)

    return gram_purity_2slit(psi_a, psi_b, D)


def local_entangle_purity(positions, adj, sources, blocked, slit_a, slit_b,
                           height, barrier_x, width, det_nodes, k=5.0, eps0=0.5):
    """Local entanglement model.

    Propagate through each slit separately, measure per-layer contrast,
    accumulate D = exp(-eps0 * sum_zones local_contrast).
    """
    # Build node_at map
    node_at = {}
    for idx, (x, y) in enumerate(positions):
        node_at[(int(round(x)), int(round(y)))] = idx

    barrier_nodes = set()
    for y in range(height):
        nid = node_at.get((barrier_x, y))
        if nid is not None:
            barrier_nodes.add(nid)

    blocked_a = blocked | (barrier_nodes - set(slit_a))
    blocked_b = blocked | (barrier_nodes - set(slit_b))

    amp_a = full_propagate(positions, adj, sources, blocked_a, k)
    amp_b = full_propagate(positions, adj, sources, blocked_b, k)

    # Per-layer local contrast
    total_local_contrast = 0.0
    n_zones = 0

    for lx in range(barrier_x + 1, width):
        prof_a = [amp_a.get(node_at.get((lx, y), -1), 0.0+0j) for y in range(height)]
        prof_b = [amp_b.get(node_at.get((lx, y), -1), 0.0+0j) for y in range(height)]

        na = vec_norm(prof_a)
        nb = vec_norm(prof_b)
        if na < 1e-30 or nb < 1e-30:
            n_zones += 1
            continue

        pa = vec_scale(prof_a, 1.0/na)
        pb = vec_scale(prof_b, 1.0/nb)
        local_contrast = vec_diff_sq_sum(pa, pb)
        total_local_contrast += local_contrast
        n_zones += 1

    # Decoherence factor
    if total_local_contrast > 500:
        D_local = 0.0
    else:
        D_local = math.exp(-eps0 * total_local_contrast)

    # Purity using detector-layer amplitudes
    psi_a_det = [amp_a.get(d, 0.0+0j) for d in det_nodes]
    psi_b_det = [amp_b.get(d, 0.0+0j) for d in det_nodes]

    na = vec_norm(psi_a_det)
    nb = vec_norm(psi_b_det)
    if na < 1e-30 or nb < 1e-30:
        return 1.0, n_zones, total_local_contrast

    psi_a_det = vec_scale(psi_a_det, 1.0/na)
    psi_b_det = vec_scale(psi_b_det, 1.0/nb)

    purity = gram_purity_2slit(psi_a_det, psi_b_det, D_local)
    return purity, n_zones, total_local_contrast


# ---------------------------------------------------------------------------
# Main scaling test
# ---------------------------------------------------------------------------

def run_single(N, k=5.0, lam_cl=1.0, eps0=0.5):
    """Run both models for a single graph size N."""
    width = N
    height = max(N // 3, 6)

    positions, adj, node_id = build_rectangular_dag(width, height)
    sources, detectors, blocked, slit_a, slit_b, barrier_x = setup_two_slit(
        width, height, node_id
    )

    det_nodes = detectors

    # Build blocked sets for each slit
    node_at = {}
    for idx, (x, y) in enumerate(positions):
        node_at[(int(round(x)), int(round(y)))] = idx

    barrier_nodes = set()
    for y in range(height):
        nid = node_at.get((barrier_x, y))
        if nid is not None:
            barrier_nodes.add(nid)

    blocked_a = blocked | (barrier_nodes - set(slit_a))
    blocked_b = blocked | (barrier_nodes - set(slit_b))

    # CL bath: propagate from each slit separately
    det_amps_a = full_propagate(positions, adj, sources, blocked_a, k)
    det_amps_b = full_propagate(positions, adj, sources, blocked_b, k)

    pur_cl = cl_bath_purity(det_amps_a, det_amps_b, det_nodes, lam=lam_cl)

    # Local entanglement
    pur_local, n_zones, total_contrast = local_entangle_purity(
        positions, adj, sources, blocked, slit_a, slit_b,
        height, barrier_x, width, det_nodes, k=k, eps0=eps0
    )

    return pur_cl, pur_local, n_zones, total_contrast


def main():
    print("=" * 78)
    print("LOCAL ENTANGLING DECOHERENCE vs CALDEIRA-LEGGETT BATH")
    print("  Hypothesis: local entanglement breaks CLT purity ceiling")
    print("  D_local = exp(-eps0 * sum_zones |Delta_psi|^2)")
    print("  As N grows, n_zones grows => D -> 0 exponentially")
    print("=" * 78)
    print()

    sizes = [10, 20, 30, 40, 60, 80, 100]
    k = 5.0
    lam_cl = 1.0
    eps0 = 0.5

    results = []

    print(f"  {'N':>5s}  {'height':>6s}  {'n_zones':>7s}  "
          f"{'pur_CL':>8s}  {'pur_local':>10s}  {'sum_contrast':>12s}  "
          f"{'D_local':>8s}")
    print(f"  {'-' * 72}")

    for N in sizes:
        height = max(N // 3, 6)
        try:
            pur_cl, pur_local, n_zones, total_contrast = run_single(
                N, k=k, lam_cl=lam_cl, eps0=eps0
            )
            D_local = math.exp(-eps0 * total_contrast) if total_contrast < 500 else 0.0
            results.append((N, height, n_zones, pur_cl, pur_local, total_contrast, D_local))
            print(f"  {N:5d}  {height:6d}  {n_zones:7d}  "
                  f"{pur_cl:8.4f}  {pur_local:10.4f}  {total_contrast:12.4f}  "
                  f"{D_local:8.6f}")
        except Exception as e:
            import traceback
            print(f"  {N:5d}  {height:6d}  FAILED: {e}")
            traceback.print_exc()

    if len(results) < 3:
        print("\nInsufficient data for fitting.")
        return

    print()

    # ---------------------------------------------------------------------------
    # Fit scaling laws
    # ---------------------------------------------------------------------------
    Ns = [r[0] for r in results]
    pur_cls = [r[3] for r in results]
    pur_locals = [r[4] for r in results]
    n_zones_arr = [r[2] for r in results]
    contrasts = [r[5] for r in results]

    print("=" * 78)
    print("SCALING ANALYSIS")
    print("=" * 78)

    # CL decoherence = 1 - purity
    decoh_cl = [max(1.0 - p, 1e-15) for p in pur_cls]
    decoh_local = [max(1.0 - p, 1e-15) for p in pur_locals]

    # Log-log fit for CL (power law: decoh ~ N^alpha)
    valid_cl_idx = [i for i, d in enumerate(decoh_cl) if d > 1e-10]
    if len(valid_cl_idx) >= 2:
        xs = [math.log(Ns[i]) for i in valid_cl_idx]
        ys = [math.log(decoh_cl[i]) for i in valid_cl_idx]
        alpha_cl, _ = simple_polyfit_1d(xs, ys)
        print(f"\n  CL bath: (1-purity) ~ N^{alpha_cl:.3f}  (power-law fit in log-log)")
    else:
        alpha_cl = None
        print(f"\n  CL bath: insufficient decoherence data for fit")

    # Local: exponential fit log(decoh) vs N
    valid_local_idx = [i for i, d in enumerate(decoh_local) if d > 1e-10]
    if len(valid_local_idx) >= 2:
        xs_exp = [float(Ns[i]) for i in valid_local_idx]
        ys_exp = [math.log(decoh_local[i]) for i in valid_local_idx]
        beta_local, _ = simple_polyfit_1d(xs_exp, ys_exp)
        print(f"  Local entangle: (1-purity) ~ exp({beta_local:.5f}*N)  (exp fit)")

        # Also power law
        xs_pow = [math.log(Ns[i]) for i in valid_local_idx]
        ys_pow = [math.log(decoh_local[i]) for i in valid_local_idx]
        alpha_local, _ = simple_polyfit_1d(xs_pow, ys_pow)
        print(f"  Local entangle: (1-purity) ~ N^{alpha_local:.3f}  (power-law fit)")
    else:
        beta_local = None
        alpha_local = None
        print(f"  Local entangle: insufficient decoherence data for fit")

    # Contrast scaling
    if len(contrasts) >= 2:
        xs_c = [math.log(float(n)) for n in Ns]
        ys_c = [math.log(c + 1e-30) for c in contrasts]
        slope_c, _ = simple_polyfit_1d(xs_c, ys_c)
        xs_z = [math.log(float(n)) for n in Ns]
        ys_z = [math.log(float(z)) for z in n_zones_arr]
        slope_z, _ = simple_polyfit_1d(xs_z, ys_z)
        print(f"\n  Sum of local contrasts ~ N^{slope_c:.3f}")
        print(f"  n_zones ~ N^{slope_z:.3f}")

    # ---------------------------------------------------------------------------
    # Verdict
    # ---------------------------------------------------------------------------
    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)

    if len(results) >= 2:
        last_cl = results[-1][3]
        last_local = results[-1][4]
        first_cl = results[0][3]
        first_local = results[0][4]

        print(f"\n  At N={results[0][0]:3d}: pur_CL={first_cl:.4f}, pur_local={first_local:.4f}")
        print(f"  At N={results[-1][0]:3d}: pur_CL={last_cl:.4f}, pur_local={last_local:.4f}")

        cl_drops = first_cl - last_cl > 0.01
        local_drops = first_local - last_local > 0.01
        local_beats_cl = last_local < last_cl

        if local_drops and local_beats_cl:
            print(f"\n  PASS: Local entanglement model achieves lower purity ({last_local:.4f})")
            print(f"        than CL bath ({last_cl:.4f}) at large N.")
            if beta_local is not None and beta_local > 0:
                print(f"        Decoherence grows exponentially with N (beta={beta_local:.5f}).")
                print(f"        => BREAKS the CLT ceiling.")
            elif alpha_local is not None and alpha_local > 0:
                print(f"        Decoherence grows as power law N^{alpha_local:.3f}.")
                if alpha_cl is not None and alpha_local > alpha_cl:
                    print(f"        Faster than CL (N^{alpha_cl:.3f}). Partial improvement.")
                else:
                    print(f"        Similar scaling to CL. Ceiling may persist.")
        elif not local_drops:
            print(f"\n  FAIL: Local model purity does NOT decrease with N.")
            print(f"        The CLT ceiling appears fundamental.")
        else:
            print(f"\n  MIXED: Both models show decoherence, but local does not beat CL.")
            print(f"        CL={last_cl:.4f}, local={last_local:.4f}")

    # Detail table
    print()
    print("  Purity ratio (local/CL) at each N:")
    for r in results:
        ratio = r[4] / r[3] if r[3] > 1e-10 else float('inf')
        print(f"    N={r[0]:3d}: ratio={ratio:.4f}  "
              f"(CL={r[3]:.4f}, local={r[4]:.4f}, zones={r[2]})")


if __name__ == "__main__":
    main()
