#!/usr/bin/env python3
"""
Spectral Radius vs Dimension — Propagator Normalization Check
=============================================================

QUESTION: Does the path-sum propagator's transfer matrix have bounded
spectral radius at d=3 but unbounded at d>3?  If rho(M) > 1, amplitudes
GROW with each layer and the propagator is non-normalizable, giving a
hard selection of d <= 3.

PHYSICS: The single-layer transfer matrix M maps transverse amplitudes
from one x-slice to the next:

    M_{ij} = exp(i k S) * w(theta) * h^{d-1} / L^p

where L is the hop length, S = L*(1-f) is the action, theta is the
off-axis angle, and h^{d-1} is the (d-1)-dimensional lattice measure.

In d spatial dimensions the transverse space is (d-1)-dimensional, so
the number of transverse neighbors grows rapidly with d.  If the sum
of |M_{ij}| over j exceeds 1, the spectral radius rho(M) > 1 and
amplitudes blow up.

EXPERIMENT:
  For d = 1, 2, 3, 4, 5:
    1. Build lattice with side ~ (target_sites)^{1/d}
    2. Build single-layer transfer matrix M
    3. Compute spectral radius rho = max|eigenvalue|
    4. Compute condition number kappa = sigma_max / sigma_min
    5. Vary wavenumber k and field strength f for robustness

PREDICTION: rho(M) <= 1 for d <= 3 (normalizable), rho(M) > 1 for
d > 3 (divergent), selecting d <= 3 spatial dimensions.

PStack experiment: frontier-spectral-radius-dimension
"""

from __future__ import annotations

import sys
import time

import numpy as np
from numpy.linalg import eig, svd

# ============================================================================
# Kernel definitions
# ============================================================================

KERNELS = {
    "gauss":  lambda theta: np.exp(-0.8 * theta**2),
    "cos2":   lambda theta: np.cos(theta)**2,
    "flat":   lambda theta: np.ones_like(theta),
}


# ============================================================================
# Transfer matrix builder for arbitrary dimension
# ============================================================================

def build_transfer_matrix_nd(d: int, side: int, k: float, p: float,
                             f: float, h: float, kernel_fn,
                             max_transverse_hop: int | None = None) -> np.ndarray:
    """Build the single-layer transfer matrix for a d-dimensional lattice.

    The "forward" direction is one axis; the remaining (d-1) axes are
    transverse.  M maps amplitudes on one (d-1)-dimensional slice to the
    next slice one step forward.

    For d=1 there is no transverse space, so M is 1x1.
    For d=2 the transverse space is a 1D line of `side` sites.
    For d=3 it is a 2D grid of side x side sites.
    etc.

    M[j, i] = exp(i*k*S) * w(theta) * h^{d-1} / L^p

    where the hop goes from transverse site i to transverse site j,
    advancing one step (h) in the forward direction.
    """
    d_transverse = d - 1

    if d_transverse == 0:
        # d=1: single site, forward hop only
        L = h
        S = L * (1.0 - f)
        theta = 0.0
        w = kernel_fn(np.array([theta]))[0]
        amp = np.exp(1j * k * S) * w * 1.0 / (L ** p)
        return np.array([[amp]], dtype=complex)

    # Transverse grid: (d-1)-dimensional with `side` sites per axis
    trans_shape = tuple([side] * d_transverse)
    n_trans = int(np.prod(trans_shape))

    # Enumerate all transverse sites as multi-index arrays
    indices = np.indices(trans_shape).reshape(d_transverse, -1).T  # (n_trans, d_transverse)

    # Build M by computing the hop from every site i to every site j
    M = np.zeros((n_trans, n_trans), dtype=complex)

    for i in range(n_trans):
        pos_i = indices[i]  # (d_transverse,) integer coords
        for j in range(n_trans):
            pos_j = indices[j]

            # Transverse displacement in lattice units
            delta_lattice = pos_j - pos_i
            if max_transverse_hop is not None:
                if np.max(np.abs(delta_lattice)) > max_transverse_hop:
                    continue

            # Physical displacement in transverse directions
            delta = delta_lattice.astype(float) * h

            # Forward step is always h in the forward direction
            L = np.sqrt(h**2 + np.dot(delta, delta))
            S = L * (1.0 - f)
            theta = np.arctan2(np.sqrt(np.dot(delta, delta)), h)

            w = kernel_fn(np.array([theta]))[0]
            # Lattice measure: h^{d-1} for the (d-1)-dimensional transverse integral
            amplitude = np.exp(1j * k * S) * w * (h ** d_transverse) / (L ** p)
            M[j, i] = amplitude

    return M


# ============================================================================
# Spectral analysis
# ============================================================================

def analyze_matrix(M: np.ndarray) -> dict:
    """Compute spectral radius, condition number, and row-sum bound."""
    eigenvalues = eig(M)[0]
    rho = np.max(np.abs(eigenvalues))

    # Singular values for condition number
    singular_values = svd(M, compute_uv=False)
    sigma_max = singular_values[0]
    sigma_min = singular_values[-1]
    kappa = sigma_max / sigma_min if sigma_min > 1e-15 else np.inf

    # Row-sum bound (Gershgorin): max over rows of sum of |M_{ij}|
    row_sums = np.sum(np.abs(M), axis=1)
    row_bound = np.max(row_sums)

    return {
        "rho": rho,
        "kappa": kappa,
        "sigma_max": sigma_max,
        "sigma_min": sigma_min,
        "row_bound": row_bound,
        "n": M.shape[0],
    }


# ============================================================================
# Main experiment
# ============================================================================

def main():
    t0 = time.time()

    print("=" * 72)
    print("SPECTRAL RADIUS vs DIMENSION -- Propagator Normalization Check")
    print("=" * 72)
    print()

    # Lattice parameters: choose side so total transverse sites are manageable
    # d=1: 1 site (no transverse), d=2: side sites, d=3: side^2, etc.
    # We want the FULL lattice to have ~1000 sites total, but the transfer
    # matrix acts on the transverse slice (side^{d-1} sites).
    # Keep side small enough that side^{d-1} fits in memory for dense eig.

    configs = {
        1: {"side": 1,   "label": "d=1 (1 trans site)"},
        2: {"side": 32,  "label": "d=2 (32 trans sites)"},
        3: {"side": 10,  "label": "d=3 (100 trans sites)"},
        4: {"side": 6,   "label": "d=4 (216 trans sites)"},
        5: {"side": 4,   "label": "d=5 (256 trans sites)"},
    }

    k_values = [1.0, 3.0, 5.0, 10.0]
    f_values = [0.0, 0.1]
    p_atten = 1.0
    h_lattice = 1.0
    kernel_name = "cos2"
    kernel_fn = KERNELS[kernel_name]

    # ── Experiment 1: spectral radius vs dimension ──────────────────────
    print("EXPERIMENT 1: Spectral radius rho(M) vs spatial dimension d")
    print(f"  kernel={kernel_name}, p={p_atten}, h={h_lattice}")
    print("-" * 72)
    print(f"{'d':>3}  {'n_trans':>8}  {'k':>6}  {'f':>5}  {'rho(M)':>10}  "
          f"{'row_bound':>10}  {'kappa':>12}  {'rho>1?':>6}")
    print("-" * 72)

    results_by_d = {}

    for d in sorted(configs.keys()):
        cfg = configs[d]
        side = cfg["side"]
        results_by_d[d] = []

        for k in k_values:
            for f in f_values:
                M = build_transfer_matrix_nd(d, side, k, p_atten, f, h_lattice, kernel_fn)
                stats = analyze_matrix(M)
                diverges = "YES" if stats["rho"] > 1.0 else "no"
                results_by_d[d].append({**stats, "k": k, "f": f})

                print(f"{d:>3}  {stats['n']:>8}  {k:>6.1f}  {f:>5.2f}  "
                      f"{stats['rho']:>10.6f}  {stats['row_bound']:>10.4f}  "
                      f"{stats['kappa']:>12.2f}  {diverges:>6}")

    # ── Experiment 2: vary p (attenuation power) ────────────────────────
    print()
    print("EXPERIMENT 2: Spectral radius vs attenuation power p")
    print(f"  kernel={kernel_name}, k=5.0, f=0.0, h={h_lattice}")
    print("-" * 72)
    print(f"{'d':>3}  {'p':>5}  {'rho(M)':>10}  {'row_bound':>10}  {'rho>1?':>6}")
    print("-" * 72)

    p_values = [0.5, 1.0, 1.5, 2.0]
    k_fixed = 5.0
    f_fixed = 0.0

    for d in sorted(configs.keys()):
        cfg = configs[d]
        side = cfg["side"]
        for p in p_values:
            M = build_transfer_matrix_nd(d, side, k_fixed, p, f_fixed, h_lattice, kernel_fn)
            stats = analyze_matrix(M)
            diverges = "YES" if stats["rho"] > 1.0 else "no"
            print(f"{d:>3}  {p:>5.1f}  {stats['rho']:>10.6f}  "
                  f"{stats['row_bound']:>10.4f}  {diverges:>6}")

    # ── Experiment 3: vary h (lattice spacing) to check continuum limit ─
    print()
    print("EXPERIMENT 3: Spectral radius vs lattice spacing h (continuum limit)")
    print(f"  kernel={kernel_name}, k=5.0, f=0.0, p={p_atten}")
    print("-" * 72)
    print(f"{'d':>3}  {'h':>6}  {'side':>5}  {'n_trans':>8}  {'rho(M)':>10}  {'rho>1?':>6}")
    print("-" * 72)

    h_values = [1.0, 0.5, 0.25]

    for d in [2, 3, 4]:
        cfg = configs[d]
        for h in h_values:
            # Scale side with h to keep physical extent fixed
            # Physical extent = side * h, keep ~ configs[d]["side"]
            phys_extent = configs[d]["side"]
            side_h = max(3, int(phys_extent / h))
            # Cap to keep matrix size reasonable
            n_trans_target = side_h ** (d - 1)
            if n_trans_target > 500:
                side_h = int(500 ** (1.0 / (d - 1)))
            M = build_transfer_matrix_nd(d, side_h, k_fixed, p_atten, f_fixed, h, kernel_fn)
            stats = analyze_matrix(M)
            diverges = "YES" if stats["rho"] > 1.0 else "no"
            print(f"{d:>3}  {h:>6.2f}  {side_h:>5}  {stats['n']:>8}  "
                  f"{stats['rho']:>10.6f}  {diverges:>6}")

    # ── Experiment 4: kernel comparison ─────────────────────────────────
    print()
    print("EXPERIMENT 4: Spectral radius across kernels")
    print(f"  k=5.0, f=0.0, p={p_atten}, h={h_lattice}")
    print("-" * 72)
    print(f"{'d':>3}  {'kernel':>8}  {'rho(M)':>10}  {'row_bound':>10}  {'rho>1?':>6}")
    print("-" * 72)

    for d in sorted(configs.keys()):
        cfg = configs[d]
        side = cfg["side"]
        for kname, kfn in KERNELS.items():
            M = build_transfer_matrix_nd(d, side, k_fixed, p_atten, f_fixed, h_lattice, kfn)
            stats = analyze_matrix(M)
            diverges = "YES" if stats["rho"] > 1.0 else "no"
            print(f"{d:>3}  {kname:>8}  {stats['rho']:>10.6f}  "
                  f"{stats['row_bound']:>10.4f}  {diverges:>6}")

    # ── Experiment 5: normalized transfer matrix ──────────────────────
    # The physical propagator should be normalized so the forward-hop
    # (no transverse displacement) has unit amplitude.  This isolates
    # the GROWTH from off-axis paths.
    print()
    print("EXPERIMENT 5: Normalized spectral radius (M / M_forward)")
    print(f"  kernel={kernel_name}, k=5.0, f=0.0, p={p_atten}, h={h_lattice}")
    print("-" * 72)
    print(f"{'d':>3}  {'n_trans':>8}  {'rho_raw':>10}  {'rho_norm':>10}  "
          f"{'M_fwd':>10}  {'rho_norm>1?':>11}")
    print("-" * 72)

    for d in sorted(configs.keys()):
        cfg = configs[d]
        side = cfg["side"]
        M = build_transfer_matrix_nd(d, side, k_fixed, p_atten, f_fixed, h_lattice, kernel_fn)
        stats_raw = analyze_matrix(M)

        # Forward hop amplitude: M for zero transverse displacement
        # In the matrix, the diagonal element (center -> center)
        center = M.shape[0] // 2
        M_fwd = np.abs(M[center, center])
        if M_fwd > 1e-15:
            M_norm = M / M_fwd
        else:
            M_norm = M
        stats_norm = analyze_matrix(M_norm)
        diverges = "YES" if stats_norm["rho"] > 1.0 else "no"
        print(f"{d:>3}  {stats_raw['n']:>8}  {stats_raw['rho']:>10.6f}  "
              f"{stats_norm['rho']:>10.6f}  {M_fwd:>10.6f}  {diverges:>11}")

    # ── Experiment 6: row-sum scaling with dimension ────────────────────
    # The row sum = sum_j |M_{ij}| bounds rho.  Track how it scales with d.
    print()
    print("EXPERIMENT 6: Row-sum scaling with dimension (Gershgorin bound)")
    print(f"  kernel={kernel_name}, k=5.0, f=0.0, p={p_atten}")
    print("-" * 72)
    print(f"{'d':>3}  {'n_trans':>8}  {'row_sum':>10}  {'row_sum/n':>10}  "
          f"{'log_ratio':>10}")
    print("-" * 72)

    prev_rs = None
    for d in sorted(configs.keys()):
        cfg = configs[d]
        side = cfg["side"]
        M = build_transfer_matrix_nd(d, side, k_fixed, p_atten, f_fixed, h_lattice, kernel_fn)
        row_sums = np.sum(np.abs(M), axis=1)
        rs = np.max(row_sums)
        n = M.shape[0]
        ratio_str = ""
        if prev_rs is not None and prev_rs > 0:
            ratio_str = f"{np.log(rs / prev_rs):.4f}"
        prev_rs = rs
        print(f"{d:>3}  {n:>8}  {rs:>10.4f}  {rs / n:>10.6f}  {ratio_str:>10}")

    # ── Experiment 7: nearest-neighbor transfer matrix ────────────────
    # On a physical lattice, each hop connects to nearest neighbors only
    # (max transverse displacement = 1 lattice unit per step).
    # This is the correct transfer matrix for the lattice path-sum.
    print()
    print("EXPERIMENT 7: Nearest-neighbor transfer matrix (max_hop=1)")
    print(f"  kernel={kernel_name}, k=5.0, f=0.0, p={p_atten}, h={h_lattice}")
    print("-" * 72)
    print(f"{'d':>3}  {'n_trans':>8}  {'rho_nn':>10}  {'rho_all':>10}  "
          f"{'row_nn':>10}  {'rho_nn>1?':>9}")
    print("-" * 72)

    for d in sorted(configs.keys()):
        cfg = configs[d]
        side = cfg["side"]
        M_nn = build_transfer_matrix_nd(d, side, k_fixed, p_atten, f_fixed,
                                         h_lattice, kernel_fn, max_transverse_hop=1)
        M_all = build_transfer_matrix_nd(d, side, k_fixed, p_atten, f_fixed,
                                          h_lattice, kernel_fn)
        s_nn = analyze_matrix(M_nn)
        s_all = analyze_matrix(M_all)
        diverges = "YES" if s_nn["rho"] > 1.0 else "no"
        print(f"{d:>3}  {s_nn['n']:>8}  {s_nn['rho']:>10.6f}  {s_all['rho']:>10.6f}  "
              f"{s_nn['row_bound']:>10.4f}  {diverges:>9}")

    # ── Experiment 8: NN rho scaling with lattice size ──────────────────
    # Does rho_nn converge as side -> infinity?  If it grows, propagator
    # diverges in the thermodynamic limit.
    print()
    print("EXPERIMENT 8: NN spectral radius vs lattice size (thermodynamic limit)")
    print(f"  kernel={kernel_name}, k=5.0, f=0.0, p={p_atten}, h={h_lattice}")
    print("-" * 72)
    print(f"{'d':>3}  {'side':>5}  {'n_trans':>8}  {'rho_nn':>10}  {'row_nn':>10}")
    print("-" * 72)

    size_sweeps = {
        2: [8, 16, 32, 64, 128, 256],
        3: [4, 6, 8, 10, 14, 18],
        4: [3, 4, 5, 6, 7],
        5: [3, 4, 5],
    }

    for d in [2, 3, 4, 5]:
        for side in size_sweeps[d]:
            n_trans = side ** (d - 1)
            if n_trans > 1000:
                continue
            M_nn = build_transfer_matrix_nd(d, side, k_fixed, p_atten, f_fixed,
                                             h_lattice, kernel_fn, max_transverse_hop=1)
            s = analyze_matrix(M_nn)
            print(f"{d:>3}  {side:>5}  {s['n']:>8}  {s['rho']:>10.6f}  "
                  f"{s['row_bound']:>10.4f}")

    # ── Experiment 9: critical p for NN transfer matrix ─────────────────
    print()
    print("EXPERIMENT 9: Critical attenuation p_c for NN matrix (rho=1)")
    print(f"  kernel={kernel_name}, k=5.0, f=0.0, h={h_lattice}")
    print("-" * 72)
    print(f"{'d':>3}  {'side':>5}  {'p_c':>8}  {'rho_at_pc':>10}  "
          f"{'coordination':>12}")
    print("-" * 72)

    for d in sorted(configs.keys()):
        if d == 1:
            print(f"{d:>3}  {'1':>5}  {'0.0000':>8}  {'1.000000':>10}  {'2':>12}")
            continue
        cfg = configs[d]
        side = cfg["side"]
        # Coordination number for NN: center site has 3^{d-1} - 1 off-diagonal neighbors
        # plus 1 self (forward hop)
        coord = 3 ** (d - 1)

        p_lo, p_hi = 0.0, 20.0
        for _ in range(50):
            p_mid = (p_lo + p_hi) / 2.0
            M = build_transfer_matrix_nd(d, side, k_fixed, p_mid, f_fixed,
                                          h_lattice, kernel_fn, max_transverse_hop=1)
            stats = analyze_matrix(M)
            if stats["rho"] > 1.0:
                p_lo = p_mid
            else:
                p_hi = p_mid
        p_c = (p_lo + p_hi) / 2.0
        M = build_transfer_matrix_nd(d, side, k_fixed, p_c, f_fixed,
                                      h_lattice, kernel_fn, max_transverse_hop=1)
        stats = analyze_matrix(M)
        print(f"{d:>3}  {side:>5}  {p_c:>8.4f}  {stats['rho']:>10.6f}  {coord:>12}")

    # ── Summary ─────────────────────────────────────────────────────────
    print()
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)

    # Collect rho at k=5, f=0 for the primary comparison
    print()
    print(f"{'d':>3}  {'rho(M) [k=5, f=0]':>18}  {'row_bound':>10}  {'status':>20}")
    print("-" * 55)

    for d in sorted(configs.keys()):
        # Find the k=5, f=0 entry
        for r in results_by_d[d]:
            if abs(r["k"] - 5.0) < 0.01 and abs(r["f"]) < 0.01:
                rho = r["rho"]
                rb = r["row_bound"]
                if rho > 1.0:
                    status = "DIVERGENT (rho > 1)"
                elif rho > 0.99:
                    status = "MARGINAL"
                else:
                    status = "BOUNDED (rho < 1)"
                print(f"{d:>3}  {rho:>18.8f}  {rb:>10.4f}  {status:>20}")
                break

    # ── Theoretical bound ───────────────────────────────────────────────
    print()
    print("THEORETICAL ANALYSIS:")
    print()
    print("The row-sum of |M| bounds the spectral radius via Gershgorin:")
    print("  rho(M) <= max_j sum_i |M_{ij}|")
    print()
    print("For the cos^2 kernel with p=1 attenuation:")
    print("  |M_{ij}| = cos^2(theta) * h^{d-1} / L")
    print("  where L = h*sqrt(1 + |delta|^2/h^2)")
    print()
    print("In d dimensions, the number of transverse neighbors at distance")
    print("r scales as r^{d-2} (surface of (d-2)-sphere). The row sum is:")
    print("  sum ~ integral cos^2(theta) * r^{d-2} dr / sqrt(1+r^2)")
    print("  ~ integral cos^2(arctan r) * r^{d-2} / sqrt(1+r^2) dr")
    print()
    print("For d <= 3: the integrand decays fast enough -> convergent")
    print("For d > 3: the volume factor r^{d-2} wins -> divergent")
    print()

    elapsed = time.time() - t0
    print(f"Total runtime: {elapsed:.1f}s")
    print()

    # ── Verdict ─────────────────────────────────────────────────────────
    # Check if any d>3 has rho>1 and all d<=3 have rho<=1
    bounded_dims = []
    divergent_dims = []
    for d in sorted(configs.keys()):
        for r in results_by_d[d]:
            if abs(r["k"] - 5.0) < 0.01 and abs(r["f"]) < 0.01:
                if r["rho"] > 1.0:
                    divergent_dims.append(d)
                else:
                    bounded_dims.append(d)
                break

    print("VERDICT:")
    if divergent_dims and all(d > 3 for d in divergent_dims):
        if all(d <= 3 for d in bounded_dims):
            print("  STRONG SELECTION: rho <= 1 for d <= 3, rho > 1 for d > 3")
            print("  The propagator is normalizable ONLY in d <= 3 spatial dimensions.")
            print("  This is a hard dimension selection from propagator self-consistency.")
        else:
            print(f"  PARTIAL SELECTION: bounded at d={bounded_dims}, divergent at d={divergent_dims}")
    elif divergent_dims:
        print(f"  DIVERGENT dimensions: {divergent_dims}")
        print(f"  BOUNDED dimensions: {bounded_dims}")
        print("  Dimension selection is more nuanced than predicted.")
    else:
        print("  NO DIVERGENCE detected at any tested dimension.")
        print("  The spectral radius is bounded for all d=1..5.")
        print("  Dimension selection must arise from a different mechanism.")
        print("  (Possible: need larger lattice, different p, or normalization differs.)")

    print()


if __name__ == "__main__":
    main()
