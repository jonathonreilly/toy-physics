#!/usr/bin/env python3
"""
3D Chiral Walk Gravity Convergence Test
========================================
The only honest test: does the sign of gravitational deflection
converge across multiple 3D lattice sizes at fixed step count N?

Grid: n_values x N_values = 6x6 = 36 runs
"""

import numpy as np
import time

def run_one(n, n_layers, theta0, strength, mass_offset):
    """Run 3D chiral walk with and without mass, return z-centroid shift."""
    center = n // 2
    mass_z = center + mass_offset

    # Build gravitational field (periodic minimum-image)
    y, z, w = np.meshgrid(np.arange(n), np.arange(n), np.arange(n), indexing='ij')
    dy = np.minimum(np.abs(y - center), n - np.abs(y - center))
    dz = np.minimum(np.abs(z - mass_z), n - np.abs(z - mass_z))
    dw = np.minimum(np.abs(w - center), n - np.abs(w - center))
    r = np.sqrt(dy**2 + dz**2 + dw**2)
    field = strength / (r + 0.1)

    # Initialize balanced source at center
    state = np.zeros((n, n, n, 6), dtype=complex)
    state[center, center, center, :] = 1.0 / np.sqrt(6)
    state_flat = state.copy()

    # Propagate
    for layer in range(n_layers):
        for st, fld in [(state, field), (state_flat, np.zeros_like(field))]:
            s = st.reshape(-1, 6)
            f = fld.flatten()
            t = theta0 * (1 - f)
            ct = np.cos(t)
            ist = 1j * np.sin(t)
            # Apply 2x2 coin to each pair
            for p in [(0, 1), (2, 3), (4, 5)]:
                a, b = s[:, p[0]].copy(), s[:, p[1]].copy()
                s[:, p[0]] = ct * a + ist * b
                s[:, p[1]] = ist * a + ct * b
            st_3d = s.reshape(n, n, n, 6)
            # Shift each component along its axis (periodic via np.roll)
            new = np.zeros_like(st_3d)
            new[:, :, :, 0] = np.roll(st_3d[:, :, :, 0], 1, axis=0)   # +y
            new[:, :, :, 1] = np.roll(st_3d[:, :, :, 1], -1, axis=0)  # -y
            new[:, :, :, 2] = np.roll(st_3d[:, :, :, 2], 1, axis=1)   # +z
            new[:, :, :, 3] = np.roll(st_3d[:, :, :, 3], -1, axis=1)  # -z
            new[:, :, :, 4] = np.roll(st_3d[:, :, :, 4], 1, axis=2)   # +w
            new[:, :, :, 5] = np.roll(st_3d[:, :, :, 5], -1, axis=2)  # -w
            if fld is field:
                state = new
            else:
                state_flat = new

    # Measure z-centroid (axis=1 is the z-axis with mass_offset)
    prob_m = np.sum(np.abs(state)**2, axis=-1)
    prob_f = np.sum(np.abs(state_flat)**2, axis=-1)
    z_coords = np.arange(n)
    cm = np.sum(prob_m * z_coords[None, :, None]) / np.sum(prob_m)
    cf = np.sum(prob_f * z_coords[None, :, None]) / np.sum(prob_f)
    return cm - cf


def main():
    theta0 = 0.3
    strength = 5e-4
    mass_offset = 3

    n_values = [11, 13, 15, 17, 19, 21]
    N_values = [10, 12, 14, 16, 18, 20]

    results = np.zeros((len(n_values), len(N_values)))

    print("3D Chiral Walk Gravity — Convergence Test")
    print("=" * 60)
    print(f"theta0={theta0}, strength={strength}, mass_offset={mass_offset}")
    print(f"Coin: symmetric Lorentzian [[cos(t), i*sin(t)], [i*sin(t), cos(t)]]")
    print(f"Lattice sizes n: {n_values}")
    print(f"Step counts  N: {N_values}")
    print(f"Total runs: {len(n_values) * len(N_values)}")
    print()

    t0 = time.time()
    for i, n in enumerate(n_values):
        for j, N in enumerate(N_values):
            t1 = time.time()
            delta = run_one(n, N, theta0, strength, mass_offset)
            dt = time.time() - t1
            results[i, j] = delta
            sign = "+" if delta > 0 else "-"
            print(f"  n={n:2d}, N={N:2d}: delta={delta:+.6e}  ({sign})  [{dt:.2f}s]")
        print()

    total_time = time.time() - t0
    print(f"Total time: {total_time:.1f}s")
    print()

    # === SIGN GRID ===
    print("SIGN GRID (+ = TOWARD mass, - = AWAY from mass)")
    print("=" * 60)
    header = "      " + "".join(f"  N={N:<4d}" for N in N_values)
    print(header)
    for i, n in enumerate(n_values):
        row = f"n={n:2d}  "
        for j in range(len(N_values)):
            sign = "  +   " if results[i, j] > 0 else "  -   "
            row += sign
        print(row)
    print()

    # === MAGNITUDE GRID ===
    print("MAGNITUDE GRID (delta values, scientific notation)")
    print("=" * 60)
    header = "      " + "".join(f"   N={N:<4d}  " for N in N_values)
    print(header)
    for i, n in enumerate(n_values):
        row = f"n={n:2d}  "
        for j in range(len(N_values)):
            row += f" {results[i, j]:+.2e} "
        print(row)
    print()

    # === CONVERGENCE ANALYSIS ===
    print("CONVERGENCE ANALYSIS")
    print("=" * 60)
    for j, N in enumerate(N_values):
        signs = [results[i, j] > 0 for i in range(len(n_values))]
        all_same = all(s == signs[0] for s in signs)
        direction = "TOWARD" if signs[-1] else "AWAY"
        vals = [results[i, j] for i in range(len(n_values))]
        # Check if last 3 lattice sizes agree in sign
        last3_same = all(s == signs[-1] for s in signs[-3:])
        status = "CONVERGED" if last3_same else "NOT CONVERGED"
        print(f"  N={N:2d}: {status} — direction={direction}")
        print(f"         deltas: {['%.2e' % v for v in vals]}")
        # Check magnitude convergence (ratio of last two)
        if abs(vals[-2]) > 1e-15:
            ratio = abs(vals[-1] / vals[-2])
            print(f"         |delta(n=21)/delta(n=19)| = {ratio:.3f}")
    print()

    # === COLUMN CONSISTENCY ===
    print("COLUMN CONSISTENCY (does sign hold across all n for each N?)")
    print("=" * 60)
    for j, N in enumerate(N_values):
        signs = ["+" if results[i, j] > 0 else "-" for i in range(len(n_values))]
        consistent = len(set(signs)) == 1
        print(f"  N={N:2d}: signs={signs}  {'CONSISTENT' if consistent else 'INCONSISTENT'}")
    print()

    # === ROW CONSISTENCY ===
    print("ROW CONSISTENCY (does sign hold across all N for each n?)")
    print("=" * 60)
    for i, n in enumerate(n_values):
        signs = ["+" if results[i, j] > 0 else "-" for j in range(len(N_values))]
        consistent = len(set(signs)) == 1
        print(f"  n={n:2d}: signs={signs}  {'CONSISTENT' if consistent else 'INCONSISTENT'}")
    print()

    # === VERDICT ===
    print("VERDICT")
    print("=" * 60)
    # Count how many columns are fully consistent
    col_consistent = 0
    for j in range(len(N_values)):
        signs = [results[i, j] > 0 for i in range(len(n_values))]
        if all(s == signs[0] for s in signs):
            col_consistent += 1

    # Check if large lattices (n>=17) all agree
    large_n_consistent = True
    for j in range(len(N_values)):
        large_signs = [results[i, j] > 0 for i in range(3, len(n_values))]  # n=17,19,21
        if not all(s == large_signs[0] for s in large_signs):
            large_n_consistent = False

    if col_consistent == len(N_values):
        print("  ALL columns consistent — sign converged at ALL lattice sizes.")
    elif large_n_consistent:
        print(f"  Large lattices (n>=17) consistent — convergence emerging.")
        print(f"  {col_consistent}/{len(N_values)} columns fully consistent.")
    else:
        print(f"  OSCILLATION PERSISTS — only {col_consistent}/{len(N_values)} columns consistent.")
        print(f"  Large lattices (n>=17) {'agree' if large_n_consistent else 'DISAGREE'}.")
        print("  Result is NOT converged. Sign depends on lattice size.")


if __name__ == "__main__":
    main()
