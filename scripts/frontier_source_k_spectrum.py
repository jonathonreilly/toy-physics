#!/usr/bin/env python3
"""Source k-spectrum from persistent patterns (Axiom 2).

IDEA: "Stable objects are persistent self-maintaining patterns." A persistent
pattern has a characteristic frequency set by its internal structure -- the
self-maintenance cycle rate. If that characteristic k falls in the attractive
window, the source NATURALLY emits in the gravity-producing regime.

APPROACH:
  Part 1 -- Characteristic k from cluster geometry.
    A cluster of N persistent nodes at spacing h has standing-wave modes
    with k_n = n*pi/(N*h). Compute these for clusters of various sizes and
    check whether any fall in the known attractive window.

  Part 2 -- Source-emitted spectrum (spectral modification by source).
    For each k in a fine sweep, propagate through a lattice WITH and WITHOUT
    a persistent-node cluster. The ratio |psi_with|^2 / |psi_without|^2 at
    the detector gives the spectral modification: which k values are
    enhanced or suppressed by the source's presence.

  Part 3 -- Use measured source spectrum as spectral weight.
    Take the spectral modification from Part 2 and use it as the weight in
    the spectral-averaging gravity test. If the source enhances attractive-
    window k values and suppresses the dominant AWAY mode at k~0.5,
    broadband gravity might work.

  Part 4 -- Gravity test with source-derived weights.
    Full two-slit gravity test: compare source-weighted spectral average
    against flat spectrum and Gaussian baselines.

PARAMETERS:
  3D ordered lattice (Lattice3D, h=0.5, W=6, L=12), Euclidean VL action.
  Spatial-only 1/r field.

HYPOTHESIS: "Persistent patterns have a characteristic k in the attractive
  window."
FALSIFICATION: "If the source spectrum is flat (no k-selection) or peaks
  outside the attractive window."
"""

from __future__ import annotations

import math
import time

import numpy as np

BETA = 0.8
MAX_D_PHYS = 3
STRENGTH = 5e-5
PHYS_W = 6
PHYS_L = 12
H = 0.5


class Lattice3D:
    """3D ordered lattice with Euclidean action S = L*(1-f)."""

    def __init__(self, phys_l: float, phys_w: float, h: float) -> None:
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
                theta = math.atan2(math.sqrt(dyp ** 2 + dzp ** 2), h)
                w = math.exp(-BETA * theta * theta)
                self._off.append((dy, dz, L, w))
        self._nw = nw

    def propagate(self, field: np.ndarray, k: float, blocked_set: set[int]) -> np.ndarray:
        n = self.n
        nl = self.nl
        nw = self._nw
        hm = self._hm
        amps = np.zeros(n, dtype=np.complex128)
        src = self.nmap.get((0, 0, 0), 0)
        amps[src] = 1.0

        blocked = np.zeros(n, dtype=bool)
        for b in blocked_set:
            blocked[b] = True

        for layer in range(nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer + 1] if layer + 1 < nl else n
            sa = amps[ls: ls + self.npl].copy()
            sa[blocked[ls: ls + self.npl]] = 0
            if np.max(np.abs(sa)) < 1e-30:
                continue

            sf = field[ls: ls + self.npl]
            df = field[ld: ld + self.npl]
            db = blocked[ld: ld + self.npl]

            for dy, dz, L, w in self._off:
                ym = max(0, -dy)
                yM = min(nw, nw - dy)
                zm = max(0, -dz)
                zM = min(nw, nw - dz)
                if ym >= yM or zm >= zM:
                    continue

                yr = np.arange(ym, yM)
                zr = np.arange(zm, zM)
                siy, siz = np.meshgrid(yr, zr, indexing="ij")
                si = siy.ravel() * nw + siz.ravel()
                di = (siy.ravel() + dy) * nw + (siz.ravel() + dz)
                a = sa[si]
                nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue

                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld: ld + self.npl], di[nz], c)

        return amps


def make_field_spatial(lat: Lattice3D, z_mass_phys: float, strength: float) -> tuple[np.ndarray, int | None]:
    """Spatial-only 1/r field centred at (2/3 * L, 0, z_mass)."""
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    my, mz = lat.pos[mi, 1], lat.pos[mi, 2]
    r = np.sqrt((lat.pos[:, 1] - my) ** 2 + (lat.pos[:, 2] - mz) ** 2) + 0.1
    return strength / r, mi


def setup_slits(lat: Lattice3D) -> set[int]:
    """Standard double-slit barrier at 1/3 of lattice length."""
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
    return blocked


def detector_indices(lat: Lattice3D) -> list[int]:
    dl = lat.nl - 1
    return [
        lat.nmap[(dl, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (dl, iy, iz) in lat.nmap
    ]


def centroid_z(amps: np.ndarray, det: list[int], pos: np.ndarray) -> tuple[float, float]:
    prob = np.abs(amps[det]) ** 2
    total = prob.sum()
    if total < 1e-30:
        return 0.0, total
    zc = np.sum(prob * pos[det, 2]) / total
    return float(zc), float(total)


def make_persistent_cluster(lat: Lattice3D, center_layer: int, center_iz: int, radius_nodes: int) -> set[int]:
    """Create a cluster of 'persistent' (blocked) nodes around a centre.

    These represent a stable self-maintaining pattern. In the propagation,
    they act as scatterers that modify the field.
    """
    cluster = set()
    for dy in range(-radius_nodes, radius_nodes + 1):
        for dz in range(-radius_nodes, radius_nodes + 1):
            if dy * dy + dz * dz <= radius_nodes * radius_nodes:
                idx = lat.nmap.get((center_layer, dy, center_iz + dz))
                if idx is not None:
                    cluster.add(idx)
    return cluster


def main() -> None:
    print("=" * 78)
    print("SOURCE k-SPECTRUM FROM PERSISTENT PATTERNS (Axiom 2)")
    print("=" * 78)
    print()
    print("Idea: persistent self-maintaining patterns have characteristic")
    print("frequencies from their internal structure. If these fall in the")
    print("attractive window, sources naturally emit gravity-producing k.")
    print()

    t0 = time.time()
    lat = Lattice3D(PHYS_L, PHYS_W, H)
    blocked_slits = setup_slits(lat)
    field_flat = np.zeros(lat.n)
    field_mass, _ = make_field_spatial(lat, 3.0, STRENGTH)
    det = detector_indices(lat)
    pos = lat.pos

    print(f"Lattice: {lat.n:,} nodes, {lat.nl} layers, h={H}")
    print(f"Mass at z=3, strength={STRENGTH}")
    print(f"Setup: {time.time() - t0:.1f}s")
    print()

    # ==================================================================
    # PART 1: Characteristic k from cluster geometry
    # ==================================================================
    print("=" * 78)
    print("PART 1: Characteristic k from cluster geometry")
    print("=" * 78)
    print()
    print("Standing-wave modes of a cluster of N nodes at spacing h:")
    print("  k_n = n * pi / (N * h)   for n = 1, 2, 3, ...")
    print()
    print("Known attractive windows (Euclidean, h=0.5):")
    print("  Primary:  k ~ 1.0 to 6.0")
    print("  (from single-k sweeps on retained lattice)")
    print()

    cluster_sizes = [1, 3, 5, 7, 9, 13]
    print(f"{'N nodes':>8} | {'cluster extent':>14} | {'k_1':>6} | {'k_2':>6} | {'k_3':>6} | {'in window?'}")
    print("-" * 75)

    for N in cluster_sizes:
        extent = N * H
        modes = [n * math.pi / extent for n in range(1, 4)]
        in_window = any(1.0 <= m <= 6.0 for m in modes)
        flag = "YES" if in_window else "no"
        print(f"{N:>8} | {extent:>12.1f}h | {modes[0]:>6.2f} | {modes[1]:>6.2f} | {modes[2]:>6.2f} | {flag}")

    print()
    print("Also: a compact cluster has a characteristic k ~ 2*pi/diameter")
    print()
    print(f"{'N nodes':>8} | {'diameter':>8} | {'k_char':>8} | {'in window?'}")
    print("-" * 45)
    for N in cluster_sizes:
        diam = max(1, N) * H
        k_char = 2 * math.pi / diam
        in_window = 1.0 <= k_char <= 6.0
        flag = "YES" if in_window else "no"
        print(f"{N:>8} | {diam:>8.2f} | {k_char:>8.2f} | {flag}")

    # ==================================================================
    # PART 2: Source-emitted spectrum (spectral modification)
    # ==================================================================
    print()
    print("=" * 78)
    print("PART 2: Spectral modification by persistent cluster")
    print("=" * 78)
    print()
    print("Propagate at each k WITH and WITHOUT a persistent cluster.")
    print("The cluster scatters the propagating amplitude, modifying")
    print("which k values reach the detector efficiently.")
    print()

    # Place persistent cluster at middle of lattice, off-axis (like a mass)
    cluster_layer = lat.nl // 2
    cluster_iz = round(2.0 / H)  # offset in z
    cluster_radius = 3  # nodes

    cluster_nodes = make_persistent_cluster(lat, cluster_layer, cluster_iz, cluster_radius)
    print(f"Cluster: {len(cluster_nodes)} nodes at layer {cluster_layer}, "
          f"iz_offset={cluster_iz}, radius={cluster_radius} nodes")

    # The cluster acts as additional blocked nodes
    blocked_with_cluster = blocked_slits | cluster_nodes
    blocked_without = blocked_slits

    k_sweep = np.arange(0.5, 12.01, 0.25)
    print(f"Sweeping {len(k_sweep)} k values from {k_sweep[0]} to {k_sweep[-1]}...")
    print()

    t1 = time.time()
    prob_with = {}
    prob_without = {}
    ratio = {}

    for k in k_sweep:
        amps_with = lat.propagate(field_flat, k, blocked_with_cluster)
        amps_without = lat.propagate(field_flat, k, blocked_without)

        p_with = np.sum(np.abs(amps_with[det]) ** 2)
        p_without = np.sum(np.abs(amps_without[det]) ** 2)

        prob_with[k] = p_with
        prob_without[k] = p_without
        ratio[k] = p_with / p_without if p_without > 1e-30 else 0.0

    print(f"  Sweep done in {time.time() - t1:.0f}s")
    print()

    print(f"{'k':>6} | {'P_without':>12} | {'P_with':>12} | {'ratio':>8} | {'modification'}")
    print("-" * 65)

    for k in k_sweep:
        r = ratio[k]
        mod = "ENHANCED" if r > 1.05 else "SUPPRESSED" if r < 0.95 else "~same"
        print(f"{k:>6.2f} | {prob_without[k]:>12.3e} | {prob_with[k]:>12.3e} | {r:>8.4f} | {mod}")

    # Identify peaks
    k_arr = np.array(list(ratio.keys()))
    r_arr = np.array(list(ratio.values()))

    peak_idx = np.argmax(r_arr)
    trough_idx = np.argmin(r_arr)
    print(f"\n  Peak enhancement:   k={k_arr[peak_idx]:.2f}, ratio={r_arr[peak_idx]:.4f}")
    print(f"  Peak suppression:   k={k_arr[trough_idx]:.2f}, ratio={r_arr[trough_idx]:.4f}")

    # Check if enhancement falls in attractive window
    enhanced_in_window = any(
        1.0 <= k <= 6.0 and ratio[k] > 1.05 for k in k_sweep
    )
    suppressed_low_k = any(
        k <= 1.0 and ratio[k] < 0.95 for k in k_sweep
    )
    print(f"\n  Enhanced k in attractive window [1-6]: {enhanced_in_window}")
    print(f"  Suppressed low-k (k<=1, AWAY regime):  {suppressed_low_k}")

    # ==================================================================
    # PART 3: Source-weighted spectral gravity test
    # ==================================================================
    print()
    print("=" * 78)
    print("PART 3: Gravity test with source-derived spectral weights")
    print("=" * 78)
    print()
    print("Use the spectral modification ratio as w(k) for coherent")
    print("spectral averaging in the two-slit gravity test.")
    print()

    # Pre-compute all gravity propagations (with mass field, standard slits)
    t2 = time.time()
    flat_det_amps = {}
    mass_det_amps = {}
    single_k_deltas = {}

    print(f"Pre-computing gravity propagations for {len(k_sweep)} k values...")

    for k in k_sweep:
        af = lat.propagate(field_flat, k, blocked_slits)
        am = lat.propagate(field_mass, k, blocked_slits)

        flat_det_amps[k] = af[det].copy()
        mass_det_amps[k] = am[det].copy()

        zf, pf = centroid_z(af, det, pos)
        zm, pm = centroid_z(am, det, pos)
        single_k_deltas[k] = zm - zf

    print(f"  Done in {time.time() - t2:.0f}s")
    print()

    # Show single-k reference
    print("Single-k reference (gravity direction):")
    print(f"{'k':>6} | {'delta':>12} | {'direction':>9}")
    print("-" * 35)
    for k in k_sweep[::2]:  # every other for brevity
        d = single_k_deltas[k]
        direction = "TOWARD" if d > 1e-10 else "AWAY" if d < -1e-10 else "~zero"
        print(f"{k:>6.2f} | {d:>+12.6f} | {direction:>9}")
    print()

    # Define weighting schemes
    pos_det = pos[det]

    def coherent_delta(weights: dict[float, float]) -> tuple[float, str]:
        """Compute gravity delta from coherent spectral sum."""
        w_sum = sum(abs(w) for w in weights.values())
        if w_sum < 1e-30:
            return 0.0, "~zero"
        norm_w = {k: w / w_sum for k, w in weights.items()}

        flat_sum = sum(norm_w[k] * flat_det_amps[k] for k in k_sweep)
        mass_sum = sum(norm_w[k] * mass_det_amps[k] for k in k_sweep)

        pf = np.sum(np.abs(flat_sum) ** 2)
        pm = np.sum(np.abs(mass_sum) ** 2)

        if pf < 1e-30 or pm < 1e-30:
            return 0.0, "~zero"

        zf = np.sum(np.abs(flat_sum) ** 2 * pos_det[:, 2]) / pf
        zm = np.sum(np.abs(mass_sum) ** 2 * pos_det[:, 2]) / pm
        delta = float(zm - zf)
        direction = "TOWARD" if delta > 1e-10 else "AWAY" if delta < -1e-10 else "~zero"
        return delta, direction

    # A) Flat spectrum (baseline)
    flat_w = {k: 1.0 for k in k_sweep}
    d_flat, dir_flat = coherent_delta(flat_w)

    # B) Source-ratio weights (the key test)
    source_w = {k: ratio[k] for k in k_sweep}
    d_source, dir_source = coherent_delta(source_w)

    # C) Source-ratio SQUARED (amplify the effect)
    source_sq_w = {k: ratio[k] ** 2 for k in k_sweep}
    d_source_sq, dir_source_sq = coherent_delta(source_sq_w)

    # D) Inverse source (suppress what cluster enhances)
    inv_source_w = {k: 1.0 / max(ratio[k], 0.01) for k in k_sweep}
    d_inv, dir_inv = coherent_delta(inv_source_w)

    # E) Only attractive-window k (k=1-6, as reference)
    window_w = {k: (1.0 if 1.0 <= k <= 6.0 else 0.0) for k in k_sweep}
    d_window, dir_window = coherent_delta(window_w)

    # F) Gaussian at k=3 (centre of attractive window)
    gauss3_w = {k: math.exp(-((k - 3.0) ** 2) / (2 * 1.5 ** 2)) for k in k_sweep}
    d_gauss3, dir_gauss3 = coherent_delta(gauss3_w)

    # G) Source-ratio, but only for k in attractive window
    source_window_w = {k: (ratio[k] if 1.0 <= k <= 6.0 else 0.0) for k in k_sweep}
    d_sw, dir_sw = coherent_delta(source_window_w)

    # H) log(ratio) weights -- treat ratio as a probability density
    log_source_w = {k: max(0.0, math.log(max(ratio[k], 0.01))) for k in k_sweep}
    d_log, dir_log = coherent_delta(log_source_w)

    print("Spectral gravity results (coherent sum):")
    print(f"{'weighting':<30} | {'delta':>12} | {'direction':>9}")
    print("-" * 58)
    results = [
        ("A) flat (baseline)", d_flat, dir_flat),
        ("B) source-ratio w(k)", d_source, dir_source),
        ("C) source-ratio^2", d_source_sq, dir_source_sq),
        ("D) inverse source-ratio", d_inv, dir_inv),
        ("E) window-only [1-6]", d_window, dir_window),
        ("F) Gaussian(k0=3, s=1.5)", d_gauss3, dir_gauss3),
        ("G) source*window [1-6]", d_sw, dir_sw),
        ("H) log(source-ratio)", d_log, dir_log),
    ]
    for label, d, direction in results:
        print(f"{label:<30} | {d:>+12.6f} | {direction:>9}")

    # ==================================================================
    # PART 4: Cluster size scan
    # ==================================================================
    print()
    print("=" * 78)
    print("PART 4: Cluster size scan -- does larger cluster shift spectrum?")
    print("=" * 78)
    print()

    radii = [1, 2, 3, 4, 5]
    k_coarse = np.arange(0.5, 12.01, 0.5)

    print(f"{'radius':>6} | {'n_nodes':>7} | {'peak_k':>7} | {'peak_ratio':>10} | "
          f"{'mean_ratio_window':>17} | {'mean_ratio_outside':>18}")
    print("-" * 80)

    for rad in radii:
        cl = make_persistent_cluster(lat, cluster_layer, cluster_iz, rad)
        bl = blocked_slits | cl

        ratios_r = {}
        for k in k_coarse:
            aw = lat.propagate(field_flat, k, bl)
            ao = lat.propagate(field_flat, k, blocked_slits)
            pw = np.sum(np.abs(aw[det]) ** 2)
            po = np.sum(np.abs(ao[det]) ** 2)
            ratios_r[k] = pw / po if po > 1e-30 else 0.0

        k_c = np.array(list(ratios_r.keys()))
        r_c = np.array(list(ratios_r.values()))

        pk_idx = np.argmax(r_c)
        peak_k = k_c[pk_idx]
        peak_r = r_c[pk_idx]

        in_w = [ratios_r[k] for k in k_coarse if 1.0 <= k <= 6.0]
        out_w = [ratios_r[k] for k in k_coarse if k < 1.0 or k > 6.0]
        mean_in = np.mean(in_w) if in_w else 0.0
        mean_out = np.mean(out_w) if out_w else 0.0

        print(f"{rad:>6} | {len(cl):>7} | {peak_k:>7.2f} | {peak_r:>10.4f} | "
              f"{mean_in:>17.4f} | {mean_out:>18.4f}")

    # ==================================================================
    # PART 5: Gravity with cluster-specific source weights
    # ==================================================================
    print()
    print("=" * 78)
    print("PART 5: Gravity test per cluster radius")
    print("=" * 78)
    print()
    print("For each cluster radius, compute source-ratio weights on k_coarse,")
    print("then run spectral gravity test.")
    print()

    print(f"{'radius':>6} | {'flat_delta':>11} {'dir':>6} | {'src_delta':>11} {'dir':>6} | "
          f"{'src*win_delta':>13} {'dir':>6}")
    print("-" * 75)

    # Need gravity propagations at k_coarse
    flat_det_c = {}
    mass_det_c = {}
    for k in k_coarse:
        af = lat.propagate(field_flat, k, blocked_slits)
        am = lat.propagate(field_mass, k, blocked_slits)
        flat_det_c[k] = af[det].copy()
        mass_det_c[k] = am[det].copy()

    def coherent_delta_coarse(weights: dict[float, float]) -> tuple[float, str]:
        w_sum = sum(abs(w) for w in weights.values())
        if w_sum < 1e-30:
            return 0.0, "~zero"
        norm_w = {k: w / w_sum for k, w in weights.items()}

        flat_sum = sum(norm_w[k] * flat_det_c[k] for k in k_coarse)
        mass_sum = sum(norm_w[k] * mass_det_c[k] for k in k_coarse)

        pf = np.sum(np.abs(flat_sum) ** 2)
        pm = np.sum(np.abs(mass_sum) ** 2)

        if pf < 1e-30 or pm < 1e-30:
            return 0.0, "~zero"

        zf = np.sum(np.abs(flat_sum) ** 2 * pos_det[:, 2]) / pf
        zm = np.sum(np.abs(mass_sum) ** 2 * pos_det[:, 2]) / pm
        delta = float(zm - zf)
        direction = "TOWARD" if delta > 1e-10 else "AWAY" if delta < -1e-10 else "~zero"
        return delta, direction

    flat_w_c = {k: 1.0 for k in k_coarse}
    d_flat_c, dir_flat_c = coherent_delta_coarse(flat_w_c)

    for rad in radii:
        cl = make_persistent_cluster(lat, cluster_layer, cluster_iz, rad)
        bl = blocked_slits | cl

        ratios_r = {}
        for k in k_coarse:
            aw = lat.propagate(field_flat, k, bl)
            ao = lat.propagate(field_flat, k, blocked_slits)
            pw = np.sum(np.abs(aw[det]) ** 2)
            po = np.sum(np.abs(ao[det]) ** 2)
            ratios_r[k] = pw / po if po > 1e-30 else 0.0

        src_w = {k: ratios_r[k] for k in k_coarse}
        d_src, dir_src = coherent_delta_coarse(src_w)

        sw_w = {k: (ratios_r[k] if 1.0 <= k <= 6.0 else 0.0) for k in k_coarse}
        d_sw_r, dir_sw_r = coherent_delta_coarse(sw_w)

        print(f"{rad:>6} | {d_flat_c:>+11.6f} {dir_flat_c:>6} | "
              f"{d_src:>+11.6f} {dir_src:>6} | "
              f"{d_sw_r:>+13.6f} {dir_sw_r:>6}")

    # ==================================================================
    # VERDICT
    # ==================================================================
    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    print()

    # Check Part 1
    small_clusters_in_window = sum(
        1 for N in cluster_sizes
        if any(1.0 <= n * math.pi / (N * H) <= 6.0 for n in range(1, 4))
    )
    print(f"Part 1: {small_clusters_in_window}/{len(cluster_sizes)} cluster sizes have "
          f"standing-wave modes in [1,6]")

    # Check Part 2
    n_enhanced_window = sum(1 for k in k_sweep if 1.0 <= k <= 6.0 and ratio[k] > 1.05)
    n_total_window = sum(1 for k in k_sweep if 1.0 <= k <= 6.0)
    print(f"Part 2: {n_enhanced_window}/{n_total_window} window k-values enhanced by cluster "
          f"(ratio>1.05)")
    print(f"        Suppressed at low-k: {suppressed_low_k}")

    # Check Part 3
    n_toward = sum(1 for _, _, d in results if d == "TOWARD")
    n_away = sum(1 for _, _, d in results if d == "AWAY")
    print(f"Part 3: {n_toward} TOWARD, {n_away} AWAY out of {len(results)} weighting schemes")

    # Hypothesis test
    source_gives_toward = dir_source == "TOWARD"
    print()
    if source_gives_toward and enhanced_in_window:
        print("HYPOTHESIS SUPPORTED:")
        print("  Source-ratio weights produce TOWARD, and the cluster enhances")
        print("  k-values in the attractive window. Persistent patterns may")
        print("  naturally emit in the gravity-producing regime.")
    elif enhanced_in_window and not source_gives_toward:
        print("MIXED RESULT:")
        print("  Cluster enhances attractive-window k, but source-ratio weights")
        print("  still give AWAY in the coherent sum. Enhancement alone is")
        print("  insufficient -- the phase structure still matters.")
    elif not enhanced_in_window:
        print("HYPOTHESIS FALSIFIED:")
        print("  The persistent cluster does NOT selectively enhance k-values")
        print("  in the attractive window. The source spectrum is either flat")
        print("  or peaks outside the window.")
    else:
        print("INCONCLUSIVE: results are ambiguous.")

    print(f"\nTotal time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
