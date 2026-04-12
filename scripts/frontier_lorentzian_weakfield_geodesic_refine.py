#!/usr/bin/env python3
"""Weak-field geodesic refinement on the exact retained split-delay action.

This is the review-driven follow-up to the earlier Lorentzian geodesic result.

The older geodesic artifact showed TOWARD only at strong field, and used a
split not identical to the retained 3D closure-card action. This script fixes
both problems:

  1. it uses the exact retained split-delay form
       delay = L * (1 - f * cos(2*theta))
  2. it measures weak-field asymmetry with a detector-layer arrival-time
     gradient, not a coarse path-center diagnostic

Review-safe question:
  in the actual closure-card weak-field regime, does the exact retained
  Lorentzian delay show a measurable TOWARD geodesic asymmetry under
  refinement, or does it remain unresolved / effectively absent?
"""

from __future__ import annotations

import math
import time

import numpy as np

MAX_D_PHYS = 3
STRENGTHS = (5e-5, 5e-4, 5e-3)
CASES = (
    (1.0, 6, 12),
    (0.5, 6, 12),
    (0.25, 6, 12),
    (0.25, 8, 12),
)
Z_MASS = 3.0


class ArrivalLattice3D:
    """Layered 3D lattice for arrival-time propagation."""

    def __init__(self, phys_l: float, phys_w: float, h: float) -> None:
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS / h))
        nw = 2 * self.hw + 1
        self.npl = nw**2
        self.n = self.nl * self.npl
        self.pos = np.zeros((self.n, 3))
        self.nmap = {}
        self._ls = np.zeros(self.nl, dtype=np.int64)
        idx = 0
        for layer in range(self.nl):
            self._ls[layer] = idx
            x = layer * h
            for iy in range(-self.hw, self.hw + 1):
                for iz in range(-self.hw, self.hw + 1):
                    self.pos[idx] = (x, iy * h, iz * h)
                    self.nmap[(layer, iy, iz)] = idx
                    idx += 1

        self._off = []
        for dy in range(-self.max_d, self.max_d + 1):
            for dz in range(-self.max_d, self.max_d + 1):
                dyp = dy * h
                dzp = dz * h
                L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
                theta = math.atan2(math.sqrt(dyp**2 + dzp**2), h)
                lf_factor = math.cos(2 * theta)
                self._off.append((dy, dz, L, lf_factor))
        self._nw = nw

    def field_spatial(self, z_mass_phys: float, strength: float) -> np.ndarray:
        gl = 2 * self.nl // 3
        iz = round(z_mass_phys / self.h)
        mi = self.nmap.get((gl, 0, iz))
        field = np.zeros(self.n)
        if mi is None:
            return field
        my, mz = self.pos[mi, 1], self.pos[mi, 2]
        r = np.sqrt((self.pos[:, 1] - my) ** 2 + (self.pos[:, 2] - mz) ** 2) + 0.1
        field[:] = strength / r
        return field

    def arrivals(self, field: np.ndarray, mode: str) -> np.ndarray:
        """Dynamic-programming arrivals on the layered DAG."""
        nw = self._nw
        arrival = np.full(self.n, np.inf)
        src = self.nmap[(0, 0, 0)]
        arrival[src] = 0.0

        for layer in range(self.nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer + 1]
            arr_src = arrival[ls : ls + self.npl].reshape(nw, nw)
            arr_dst = arrival[ld : ld + self.npl].reshape(nw, nw)
            sf = field[ls : ls + self.npl].reshape(nw, nw)
            df = field[ld : ld + self.npl].reshape(nw, nw)

            for dy, dz, L, lf_factor in self._off:
                ym = max(0, -dy)
                yM = min(nw, nw - dy)
                zm = max(0, -dz)
                zM = min(nw, nw - dz)
                if ym >= yM or zm >= zM:
                    continue

                src_view = arr_src[ym:yM, zm:zM]
                dst_view = arr_dst[ym + dy : yM + dy, zm + dz : zM + dz]
                lf = 0.5 * (
                    sf[ym:yM, zm:zM] + df[ym + dy : yM + dy, zm + dz : zM + dz]
                )

                if mode == "flat":
                    delay = L
                elif mode == "euclidean":
                    delay = L * (1.0 + lf)
                elif mode == "lorentzian":
                    delay = L * (1.0 - lf * lf_factor)
                else:
                    raise ValueError(mode)

                cand = src_view + delay
                np.minimum(dst_view, cand, out=dst_view)

        return arrival


def detector_slice(lat: ArrivalLattice3D, arrival: np.ndarray, layer: int | None = None) -> list[tuple[float, float]]:
    if layer is None:
        layer = lat.nl - 1
    rows = []
    for iz in range(-lat.hw, lat.hw + 1):
        idx = lat.nmap.get((layer, 0, iz))
        if idx is None:
            continue
        t = float(arrival[idx])
        if math.isfinite(t):
            rows.append((iz * lat.h, t))
    return rows


def fit_slope(rows: list[tuple[float, float]]) -> float:
    if len(rows) < 3:
        return 0.0
    z = np.array([r[0] for r in rows], dtype=float)
    t = np.array([r[1] for r in rows], dtype=float)
    zc = z - z.mean()
    denom = float(np.dot(zc, zc))
    if denom < 1e-30:
        return 0.0
    return float(np.dot(zc, t - t.mean()) / denom)


def near_far_asym(rows_flat: list[tuple[float, float]], rows_field: list[tuple[float, float]], z_probe: float) -> tuple[float, float, float]:
    flat = {z: t for z, t in rows_flat}
    field = {z: t for z, t in rows_field}
    z_near = z_probe
    z_far = -z_probe
    diff_near = field[z_near] - flat[z_near]
    diff_far = field[z_far] - flat[z_far]
    return diff_near, diff_far, diff_near - diff_far


def main() -> None:
    print("=" * 88)
    print("WEAK-FIELD LORENTZIAN GEODESIC REFINEMENT")
    print("=" * 88)
    print()
    print("Exact retained delay law:")
    print("  Euclidean   : delay = L * (1 + f)")
    print("  Lorentzian  : delay = L * (1 - f*cos(2θ))")
    print()
    print("Metric:")
    print("  detector-layer arrival-delay slope on the y=0 slice")
    print("  positive slope  -> mass side more delayed -> AWAY")
    print("  negative slope  -> mass side less delayed -> TOWARD")
    print()

    t0 = time.time()
    print(
        f"{'h':>5} {'W':>3} {'s':>8} | "
        f"{'euc_slope':>11} {'dir':>7} | {'lor_slope':>11} {'dir':>7} | "
        f"{'pair_asym':>11} {'dir':>7}"
    )
    print("-" * 88)

    for h, phys_w, phys_l in CASES:
        lat = ArrivalLattice3D(phys_l, phys_w, h)
        flat = lat.arrivals(np.zeros(lat.n), "flat")
        flat_rows = detector_slice(lat, flat)
        available_z = [abs(z) for z, _ in flat_rows if abs(z) > 0]
        z_probe = min(Z_MASS, max(available_z)) if available_z else 0.0
        for strength in STRENGTHS:
            field = lat.field_spatial(Z_MASS, strength)
            arr_e = lat.arrivals(field, "euclidean")
            arr_l = lat.arrivals(field, "lorentzian")
            rows_e = detector_slice(lat, arr_e)
            rows_l = detector_slice(lat, arr_l)

            shift_e = [(z, te - tf) for (z, tf), (_, te) in zip(flat_rows, rows_e)]
            shift_l = [(z, tl - tf) for (z, tf), (_, tl) in zip(flat_rows, rows_l)]

            slope_e = fit_slope(shift_e)
            slope_l = fit_slope(shift_l)
            dir_e = "AWAY" if slope_e > 1e-12 else "TOWARD" if slope_e < -1e-12 else "NONE"
            dir_l = "AWAY" if slope_l > 1e-12 else "TOWARD" if slope_l < -1e-12 else "NONE"

            _, _, asym_l = near_far_asym(flat_rows, rows_l, z_probe)
            dir_pair = "AWAY" if asym_l > 1e-12 else "TOWARD" if asym_l < -1e-12 else "NONE"

            print(
                f"{h:>5.2f} {int(phys_w):>3d} {strength:>8.0e} | "
                f"{slope_e:>+11.3e} {dir_e:>7} | "
                f"{slope_l:>+11.3e} {dir_l:>7} | "
                f"{asym_l:>+11.3e} {dir_pair:>7}"
            )

        print("-" * 88)

    print()
    print(f"Total time: {time.time() - t0:.1f}s")
    print("Read:")
    print("  - If Lorentzian slopes stay ~0 at weak field under refinement, geometric TOWARD is unresolved.")
    print("  - If Lorentzian slopes turn robustly negative while Euclidean stays positive or ~0,")
    print("    weak-field geometric attraction is real on the retained lane.")


if __name__ == "__main__":
    main()
