#!/usr/bin/env python3
"""3D chiral Born barrier/slit test on a local absorptive harness.

State per transverse site (y, z):
  - +y, -y, +z, -z chiral components

Propagation per layer:
  1. local pairwise coin on (+y,-y) and (+z,-z)
  2. nearest-neighbor shift with reflecting boundaries

Barrier:
  - one absorptive layer at x = BARRIER_LAYER
  - blocked sites have all four components zeroed

This is a real 7-configuration Sorkin test in the 3D chiral state space.
"""

from __future__ import annotations

import math

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc


N_YZ = 15
N_LAYERS = 18
THETA0 = 0.30
SOURCE_Y = 7
SOURCE_Z = 7
BARRIER_LAYER = 8
SLITS = [(5, 7), (7, 5), (9, 7)]


def site_base(n_yz: int, y: int, z: int) -> int:
    return 4 * (y * n_yz + z)


def propagate_3d(open_slits: set[tuple[int, int]]) -> np.ndarray:
    """3D chiral walk with a one-layer absorptive slit barrier."""
    dim = 4 * N_YZ * N_YZ
    psi = np.zeros(dim, dtype=complex)
    base = site_base(N_YZ, SOURCE_Y, SOURCE_Z)
    psi[base + 0] = 1.0 / math.sqrt(2.0)
    psi[base + 2] = 1.0 / math.sqrt(2.0)

    c = math.cos(THETA0)
    s = math.sin(THETA0)

    for x in range(N_LAYERS):
        # Coin
        for y in range(N_YZ):
            for z in range(N_YZ):
                base = site_base(N_YZ, y, z)
                p_py, p_my = psi[base + 0], psi[base + 1]
                p_pz, p_mz = psi[base + 2], psi[base + 3]
                psi[base + 0] = c * p_py - s * p_my
                psi[base + 1] = s * p_py + c * p_my
                psi[base + 2] = c * p_pz - s * p_mz
                psi[base + 3] = s * p_pz + c * p_mz

        # Absorptive barrier
        if x == BARRIER_LAYER:
            for y in range(N_YZ):
                for z in range(N_YZ):
                    if (y, z) not in open_slits:
                        base = site_base(N_YZ, y, z)
                        psi[base:base + 4] = 0.0

        # Shift
        new_psi = np.zeros_like(psi)
        for y in range(N_YZ):
            for z in range(N_YZ):
                base = site_base(N_YZ, y, z)

                # +y
                if y + 1 < N_YZ:
                    dst = site_base(N_YZ, y + 1, z)
                    new_psi[dst + 0] += psi[base + 0]
                else:
                    new_psi[base + 1] += psi[base + 0]

                # -y
                if y - 1 >= 0:
                    dst = site_base(N_YZ, y - 1, z)
                    new_psi[dst + 1] += psi[base + 1]
                else:
                    new_psi[base + 0] += psi[base + 1]

                # +z
                if z + 1 < N_YZ:
                    dst = site_base(N_YZ, y, z + 1)
                    new_psi[dst + 2] += psi[base + 2]
                else:
                    new_psi[base + 3] += psi[base + 2]

                # -z
                if z - 1 >= 0:
                    dst = site_base(N_YZ, y, z - 1)
                    new_psi[dst + 3] += psi[base + 3]
                else:
                    new_psi[base + 2] += psi[base + 3]

        psi = new_psi

    return psi


def detector_probs_3d(psi: np.ndarray) -> np.ndarray:
    probs = np.zeros((N_YZ, N_YZ), dtype=float)
    for y in range(N_YZ):
        for z in range(N_YZ):
            base = site_base(N_YZ, y, z)
            probs[y, z] = float(np.sum(np.abs(psi[base:base + 4]) ** 2))
    return probs


def run_config(open_slits: list[tuple[int, int]]) -> np.ndarray:
    return detector_probs_3d(propagate_3d(set(open_slits)))


def main() -> None:
    print("FRONTIER: CHIRAL 3D BORN / SLIT TEST")
    print(f"Grid: {N_YZ} x {N_YZ}, layers={N_LAYERS}")
    print(f"Source: ({SOURCE_Y}, {SOURCE_Z})")
    print(f"Barrier layer: {BARRIER_LAYER}")
    print(f"Slits: {SLITS}")
    print("Parity caveat: slit sites are chosen with the same parity as the source.")
    print()

    a, b, c = SLITS
    p_abc = run_config([a, b, c])
    p_ab = run_config([a, b])
    p_ac = run_config([a, c])
    p_bc = run_config([b, c])
    p_a = run_config([a])
    p_b = run_config([b])
    p_c = run_config([c])

    i3 = p_abc - p_ab - p_ac - p_bc + p_a + p_b + p_c
    i3_max = float(np.max(np.abs(i3)))
    p_total = float(np.sum(p_abc))
    i3_norm = i3_max / p_total if p_total > 1e-30 else float("inf")

    print(f"P(ABC) total: {p_total:.6f}")
    print(f"|I3| max:     {i3_max:.3e}")
    print(f"|I3| / P:     {i3_norm:.3e}")
    print("Transmission totals:")
    print(f"  ABC = {np.sum(p_abc):.6f}")
    print(f"  AB  = {np.sum(p_ab):.6f}")
    print(f"  AC  = {np.sum(p_ac):.6f}")
    print(f"  BC  = {np.sum(p_bc):.6f}")
    print(f"  A   = {np.sum(p_a):.6f}")
    print(f"  B   = {np.sum(p_b):.6f}")
    print(f"  C   = {np.sum(p_c):.6f}")

    ok = i3_norm < 1e-6
    print(f"\nVerdict: {'PASS' if ok else 'FAIL'}")
    print("Note: absorption is linear but not norm-preserving by design.")


if __name__ == "__main__":
    main()
