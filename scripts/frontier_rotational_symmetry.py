#!/usr/bin/env python3
"""
Frontier test: Rotational symmetry breaking vs lattice spacing h.

HYPOTHESIS: The 8.2% rotational symmetry breaking decreases with finer
lattice spacing h.

FALSIFICATION: If anisotropy does NOT decrease from h=1.0 to h=0.25,
the directional measure itself introduces preferred directions.
"""

import math
import time
import numpy as np

# ── Constants ────────────────────────────────────────────────────────
BETA = 0.8
K = 5.0
MAX_D_PHYS = 3
STRENGTH = 5e-5
MASS_D_PHYS = 3.0  # physical distance from beam axis to mass


class Lattice3D:
    def __init__(self, phys_l, phys_w, h):
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS / h))
        nw = 2 * self.hw + 1
        self.npl = nw ** 2
        self.n = self.nl * self.npl
        self._hm = h * h

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
                w = math.exp(-BETA * theta * theta)
                self._off.append((dy, dz, L, w))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        n = self.n; hw = self.hw; nl = self.nl; nw = self._nw; hm = self._hm
        amps = np.zeros(n, dtype=np.complex128)
        src = self.nmap.get((0, 0, 0), 0)
        amps[src] = 1.0
        blocked = np.zeros(n, dtype=bool)
        for b in blocked_set:
            blocked[b] = True
        for layer in range(nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer + 1] if layer + 1 < nl else n
            sa = amps[ls:ls + self.npl].copy()
            sa[blocked[ls:ls + self.npl]] = 0
            if np.max(np.abs(sa)) < 1e-30:
                continue
            sf = field[ls:ls + self.npl]
            df = field[ld:ld + self.npl]
            db = blocked[ld:ld + self.npl]
            for dy, dz, L, w in self._off:
                ym = max(0, -dy); yM = min(nw, nw - dy)
                zm = max(0, -dz); zM = min(nw, nw - dz)
                if ym >= yM or zm >= zM:
                    continue
                yr = np.arange(ym, yM); zr = np.arange(zm, zM)
                siy, siz = np.meshgrid(yr, zr, indexing='ij')
                si = siy.ravel() * nw + siz.ravel()
                di = (siy.ravel() + dy) * nw + (siz.ravel() + dz)
                a = sa[si]; nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue
                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field_at_position(lat, y_phys, z_phys, strength):
    """Place mass at (2*nl//3, iy, iz) and return 1/r field."""
    iy = round(y_phys / lat.h)
    iz = round(z_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, iy, iz))
    if mi is None:
        print(f"  WARNING: mass position ({2*lat.nl//3}, {iy}, {iz}) out of bounds")
        return np.zeros(lat.n), None
    mx, my, mz = lat.pos[mi]
    r = np.sqrt((lat.pos[:, 0] - mx)**2 + (lat.pos[:, 1] - my)**2 +
                (lat.pos[:, 2] - mz)**2) + 0.1
    return strength / r, mi


def setup_slits(lat):
    bl = lat.nl // 3
    bi = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap.get((bl, iy, iz))
            if idx is not None:
                bi.append(idx)
    sa = [i for i in bi if lat.pos[i, 1] >= 0.5]
    sb = [i for i in bi if lat.pos[i, 1] <= -0.5]
    blocked = set(bi) - set(sa + sb)
    return bi, sa, sb, blocked, bl


def detector_stats(lat, amps):
    """Return detector-layer y, z arrays and probability."""
    dl = lat.nl - 1
    ls = lat._ls[dl]
    det_amps = amps[ls:ls + lat.npl]
    P = np.abs(det_amps)**2
    det_pos = lat.pos[ls:ls + lat.npl]
    y = det_pos[:, 1]
    z = det_pos[:, 2]
    return y, z, P


def run_experiment():
    print(__doc__)
    print("=" * 72)

    h_values = [1.0, 0.5, 0.25]
    results = []

    for h in h_values:
        t0 = time.time()
        print(f"\n--- h = {h} ---")

        lat = Lattice3D(phys_l=12, phys_w=10, h=h)
        print(f"  Grid: {lat.nl} layers x {lat.npl} nodes/layer = {lat.n} total")

        _, _, _, blocked, _ = setup_slits(lat)

        # ── Flat-field baseline ──────────────────────────────────
        flat_field = np.zeros(lat.n)
        amps_flat = lat.propagate(flat_field, K, blocked)
        y_det, z_det, P_flat = detector_stats(lat, amps_flat)

        total_P_flat = P_flat.sum()
        if total_P_flat < 1e-30:
            print("  WARNING: no signal at detector (flat). Skipping h.")
            results.append((h, np.nan, np.nan, np.nan, np.nan, 0))
            continue

        # Baselines
        z_flat = np.sum(P_flat * z_det) / total_P_flat
        yz_flat = np.sum(P_flat * (y_det + z_det) / np.sqrt(2)) / total_P_flat
        print(f"  Flat baselines: z_centroid={z_flat:.6f}, "
              f"yz_centroid={yz_flat:.6f}")

        # ── On-axis mass (z-only offset) ─────────────────────────
        field_on, mi_on = make_field_at_position(lat, 0.0, MASS_D_PHYS, STRENGTH)
        if mi_on is not None:
            print(f"  On-axis mass at node {mi_on}, "
                  f"pos={lat.pos[mi_on]}")

        amps_on = lat.propagate(field_on, K, blocked)
        _, _, P_on = detector_stats(lat, amps_on)
        total_P_on = P_on.sum()
        z_on = np.sum(P_on * z_det) / total_P_on
        delta_on = z_on - z_flat

        # ── 45-degree mass (y=z offset) ──────────────────────────
        d45 = MASS_D_PHYS / np.sqrt(2)
        field_45, mi_45 = make_field_at_position(lat, d45, d45, STRENGTH)
        if mi_45 is not None:
            print(f"  45-deg mass at node {mi_45}, "
                  f"pos={lat.pos[mi_45]}")

        amps_45 = lat.propagate(field_45, K, blocked)
        _, _, P_45 = detector_stats(lat, amps_45)
        total_P_45 = P_45.sum()
        yz_45 = np.sum(P_45 * (y_det + z_det) / np.sqrt(2)) / total_P_45
        delta_45 = yz_45 - yz_flat

        # ── Field diagnostics ────────────────────────────────────
        # Check field strength at beam axis near mass layer
        beam_idx = lat.nmap.get((2 * lat.nl // 3, 0, 0))
        if beam_idx is not None:
            print(f"  Field at beam axis: on-axis={field_on[beam_idx]:.3e}, "
                  f"45-deg={field_45[beam_idx]:.3e}")

        elapsed = time.time() - t0

        if abs(delta_on) > 1e-15:
            ratio = delta_45 / delta_on
            aniso = abs(1 - ratio) * 100
        else:
            ratio = np.nan
            aniso = np.nan

        results.append((h, delta_on, delta_45, ratio, aniso, elapsed))

        print(f"  on-axis shift = {delta_on:.6e}")
        print(f"  45-deg  shift = {delta_45:.6e}")
        print(f"  ratio 45/on   = {ratio:.4f}")
        print(f"  anisotropy    = {aniso:.2f}%")
        print(f"  elapsed       = {elapsed:.1f}s")

    # ── Summary table ────────────────────────────────────────────
    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"{'h':>6} | {'on-axis shift':>14} | {'45-deg shift':>13} | "
          f"{'ratio 45/on':>12} | {'anisotropy%':>12} | {'time(s)':>8}")
    print("-" * 72)
    for h, d_on, d_45, ratio, aniso, t in results:
        print(f"{h:6.2f} | {d_on:14.6e} | {d_45:13.6e} | "
              f"{ratio:12.4f} | {aniso:12.2f}% | {t:8.1f}")

    # ── Verdict ──────────────────────────────────────────────────
    print("\n" + "=" * 72)
    print("VERDICT")
    print("=" * 72)

    valid = [(h, aniso) for h, _, _, _, aniso, _ in results
             if not np.isnan(aniso)]

    # Check for sign-flip at coarsest grid (signals grid too coarse)
    sign_flips = [(h, r) for h, _, _, r, _, _ in results
                  if not np.isnan(r) and r < 0]
    if sign_flips:
        print(f"NOTE: Sign-flip in ratio detected at h={sign_flips[0][0]} "
              f"(ratio={sign_flips[0][1]:.4f}).")
        print("This indicates h=1.0 is too coarse for meaningful comparison.")
        print("Restricting analysis to h values with positive ratio.\n")
        valid = [(h, aniso) for h, _, _, ratio, aniso, _ in results
                 if not np.isnan(aniso) and ratio > 0]

    if len(valid) >= 2:
        aniso_first = valid[0][1]
        aniso_last = valid[-1][1]

        # Check monotonicity
        aniso_vals = [a for _, a in valid]
        monotone = all(aniso_vals[i] >= aniso_vals[i+1]
                       for i in range(len(aniso_vals)-1))

        if monotone and aniso_last < aniso_first:
            print(f"CONSISTENT WITH hypothesis: anisotropy monotonically "
                  f"decreased from {aniso_first:.2f}% (h={valid[0][0]}) to "
                  f"{aniso_last:.2f}% (h={valid[-1][0]}).")
            print("Finer lattice spacing reduces rotational symmetry breaking.")
        elif aniso_last < aniso_first:
            print(f"MIXED: anisotropy decreased overall from "
                  f"{aniso_first:.2f}% (h={valid[0][0]}) to "
                  f"{aniso_last:.2f}% (h={valid[-1][0]}),")
            print("but the trend is NOT monotonic across all h values.")
            print("Further h values needed to establish convergence direction.")
        else:
            print(f"NOT SUPPORTED: anisotropy did NOT decrease from "
                  f"{aniso_first:.2f}% (h={valid[0][0]}) to "
                  f"{aniso_last:.2f}% (h={valid[-1][0]}).")
            print("The directional measure may itself introduce preferred directions,")
            print("or the lattice symmetry breaking is not purely a discretization artifact.")
    else:
        print("Insufficient valid data points for verdict.")


if __name__ == "__main__":
    run_experiment()
