#!/usr/bin/env python3
"""
frontier_weak_field_lorentzian_geodesic.py

Test whether Lorentzian split-delay geodesic deflection resolves at weak field
using a 3D ordered lattice at finer grid spacing (h=0.25).

HYPOTHESIS: At h=0.25 with weak field (5e-5), the Lorentzian geodesic bends TOWARD mass.
FALSIFICATION: If TOWARD only appears at strong field even at h=0.25.
"""

import numpy as np
import math
import time

# ── Parameters ──────────────────────────────────────────────────────────
W = 10        # transverse extent: y,z in [0, W]
L = 12        # longitudinal extent: x in [0, L]
H_VALUES = [0.5, 0.25]
STRENGTHS = [5e-5, 5e-4, 5e-3, 5e-2]
MASS_Z = 3   # mass located at z=3 (near the low-z edge)


def run_test(h, strength):
    """
    Build 3D lattice at spacing h, compute Lorentzian arrival times
    with and without a 1/r field, measure transverse gradient.

    Returns (gradient, direction_str, n_layers, n_per_layer)
    """
    # Grid dimensions
    ny = int(W / h) + 1   # number of y grid points
    nz = int(W / h) + 1   # number of z grid points
    nl = int(L / h) + 1   # number of x layers (propagation direction)

    # y and z coordinates
    ys = np.arange(ny) * h
    zs = np.arange(nz) * h

    # Mass position: center in y, at z=MASS_Z
    mass_y = W / 2.0
    mass_z = MASS_Z

    # ── Field function: spatial-only 1/r ──
    def field_at(x, y, z):
        dy = y - mass_y
        dz = z - mass_z
        dx = x - 0.0  # mass at x=0 (source layer)
        r = math.sqrt(dx * dx + dy * dy + dz * dz)
        if r < h * 0.5:
            r = h * 0.5  # regularize
        return strength / r

    # ── Arrival time computation ──
    # t[iy, iz] = arrival time at current layer
    # Propagate layer by layer, taking min over predecessors

    def compute_arrival_times(use_field):
        """Compute arrival times at each layer via Dijkstra-like propagation."""
        # Start at layer 0 (x=0), source at center y
        source_iy = ny // 2
        source_iz = nz // 2

        # Initialize layer 0: all infinity except source
        t_prev = np.full((ny, nz), np.inf)
        t_prev[source_iy, source_iz] = 0.0

        # Neighbor offsets in (dy, dz): straight + diagonal
        offsets = []
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                offsets.append((dy, dz))

        for layer in range(1, nl):
            x_prev = (layer - 1) * h
            x_next = layer * h
            t_next = np.full((ny, nz), np.inf)

            for iy in range(ny):
                for iz in range(nz):
                    y_next = iy * h
                    z_next = iz * h

                    best = np.inf
                    for dy, dz in offsets:
                        iy_p = iy - dy  # predecessor index
                        iz_p = iz - dz
                        if iy_p < 0 or iy_p >= ny or iz_p < 0 or iz_p >= nz:
                            continue
                        if t_prev[iy_p, iz_p] == np.inf:
                            continue

                        # Edge length
                        edge_dy = dy * h
                        edge_dz = dz * h
                        edge_L = math.sqrt(h * h + edge_dy * edge_dy + edge_dz * edge_dz)

                        if use_field:
                            # Angle from forward direction
                            transverse = math.sqrt(edge_dy * edge_dy + edge_dz * edge_dz)
                            theta = math.atan2(transverse, h)

                            # Field at midpoint
                            mid_x = (x_prev + x_next) / 2.0
                            mid_y = (iy_p * h + y_next) / 2.0
                            mid_z = (iz_p * h + z_next) / 2.0
                            f = field_at(mid_x, mid_y, mid_z)

                            # Lorentzian delay: L * (1 - f * cos(2*theta))
                            delay = edge_L * (1.0 - f * math.cos(2.0 * theta))
                        else:
                            delay = edge_L

                        candidate = t_prev[iy_p, iz_p] + delay
                        if candidate < best:
                            best = candidate

                    t_next[iy, iz] = best

            t_prev = t_next

        return t_prev  # arrival times at final layer

    # Compute with and without field
    t_flat = compute_arrival_times(use_field=False)
    t_mass = compute_arrival_times(use_field=True)

    # ── Measure transverse gradient ──
    # Compare arrival time shift at z_near vs z_far (at center y)
    center_iy = ny // 2

    # z_near: closest to mass (z=MASS_Z → iz = MASS_Z/h)
    iz_near = int(MASS_Z / h)
    # z_far: opposite side (symmetric about center)
    iz_far = nz - 1 - iz_near

    # Clamp to valid range
    iz_near = max(0, min(ny - 1, iz_near))
    iz_far = max(0, min(ny - 1, iz_far))

    dt_near = t_mass[center_iy, iz_near] - t_flat[center_iy, iz_near]
    dt_far = t_mass[center_iy, iz_far] - t_flat[center_iy, iz_far]

    gradient = dt_near - dt_far

    if gradient < -1e-15:
        direction = "TOWARD"
    elif gradient > 1e-15:
        direction = "AWAY"
    else:
        direction = "FLAT"

    return gradient, direction, nl, ny * nz, iz_near, iz_far, dt_near, dt_far


# ── Main ────────────────────────────────────────────────────────────────
def main():
    print("=" * 78)
    print("FRONTIER: Weak-Field Lorentzian Geodesic Deflection (3D Lattice)")
    print("=" * 78)
    print(f"W={W}, L={L}, mass at z={MASS_Z}, center y={W/2}")
    print(f"Lorentzian delay: L*(1 - f*cos(2*theta))")
    print(f"  theta=0 (forward): faster near mass (time dilation)")
    print(f"  theta=pi/2 (transverse): slower near mass (spatial stretch)")
    print()

    results = {}

    for h in H_VALUES:
        print(f"{'─'*78}")
        print(f"  h = {h}  (grid: {int(L/h)+1} layers x {int(W/h)+1}x{int(W/h)+1} = "
              f"{(int(W/h)+1)**2} nodes/layer)")
        print(f"{'─'*78}")

        for strength in STRENGTHS:
            t0 = time.time()
            grad, direction, nl, npl, iz_near, iz_far, dt_near, dt_far = run_test(h, strength)
            elapsed = time.time() - t0

            results[(h, strength)] = (grad, direction)

            print(f"  f={strength:.0e}  |  grad={grad:+.6e}  |  {direction:6s}  |  "
                  f"dt_near={dt_near:+.6e}  dt_far={dt_far:+.6e}  |  "
                  f"iz_near={iz_near} iz_far={iz_far}  |  {elapsed:.1f}s")

        print()

    # ── Summary ─────────────────────────────────────────────────────────
    print("=" * 78)
    print("SUMMARY TABLE")
    print("=" * 78)
    print(f"{'h':>6s}  {'strength':>10s}  {'gradient':>14s}  {'direction':>9s}")
    print("-" * 50)
    for h in H_VALUES:
        for strength in STRENGTHS:
            grad, direction = results[(h, strength)]
            print(f"{h:6.2f}  {strength:10.0e}  {grad:+14.6e}  {direction:>9s}")
        print()

    # ── Resolution comparison ───────────────────────────────────────────
    print("=" * 78)
    print("RESOLUTION COMPARISON (h=0.5 vs h=0.25 at same strength)")
    print("=" * 78)
    for strength in STRENGTHS:
        g05, d05 = results[(0.5, strength)]
        g025, d025 = results[(0.25, strength)]
        ratio = g025 / g05 if abs(g05) > 1e-30 else float('inf')
        print(f"  f={strength:.0e}:  h=0.5 → {d05:6s} ({g05:+.4e})  "
              f"h=0.25 → {d025:6s} ({g025:+.4e})  ratio={ratio:.3f}")
    print()

    # ── Hypothesis check ────────────────────────────────────────────────
    print("=" * 78)
    print("HYPOTHESIS CHECK")
    print("=" * 78)
    weak_h025 = results[(0.25, 5e-5)]
    print(f"  h=0.25, f=5e-5: direction = {weak_h025[1]}, gradient = {weak_h025[0]:+.6e}")
    print()

    all_toward = all(results[(h, s)][1] == "TOWARD" for h in H_VALUES for s in STRENGTHS)
    toward_at_weak = weak_h025[1] == "TOWARD"

    if toward_at_weak:
        print("  RESULT: TOWARD at weak field (5e-5) with h=0.25")
        print("  >>> HYPOTHESIS SUPPORTED: Lorentzian geodesic bends toward mass")
        print("      even at closure-card regime field strength.")
    else:
        print(f"  RESULT: {weak_h025[1]} at weak field (5e-5) with h=0.25")
        print("  >>> HYPOTHESIS FALSIFIED: TOWARD does not appear at weak field.")

    if all_toward:
        print("  ALL combinations show TOWARD — geodesic deflection is robust.")
    else:
        # Show which ones aren't TOWARD
        non_toward = [(h, s, results[(h, s)][1]) for h in H_VALUES for s in STRENGTHS
                       if results[(h, s)][1] != "TOWARD"]
        print(f"  Non-TOWARD cases: {non_toward}")

    print()
    print("=" * 78)


if __name__ == "__main__":
    main()
