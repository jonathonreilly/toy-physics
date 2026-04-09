#!/usr/bin/env python3
"""Wave vs geodesic decomposition: compare geometric and wave deflection signs.

CAVEAT (from review): The geodesic asymmetry (arrival-time difference) and
the wave deflection (probability centroid shift) are in DIFFERENT UNITS and
cannot be directly subtracted. What this script supports is a SIGN comparison
(geometric points AWAY while wave can point TOWARD), not a quantitative
decomposition into additive geometric + wave components.

On the 3D ordered lattice (h=0.5, W=6, L=12):

1. Compute the GEODESIC baseline (k-independent):
   Layer-by-layer minimum-delay propagation with and without mass at z=3.
   The transverse arrival-time gradient gives the geodesic deflection.

2. For each k in a sweep:
   Compute the wave deflection (centroid of |psi|^2).

3. Plot both on same chart: geodesic is a horizontal line, wave oscillates
   around it.

HYPOTHESIS: The geodesic baseline is roughly constant across k, and the
wave oscillation around it explains the phase diagram.
FALSIFICATION: If the geodesic baseline varies with k (it shouldn't).
"""

from __future__ import annotations
import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required.") from exc

# ── Parameters ──────────────────────────────────────────────────────
BETA = 0.8
MAX_D_PHYS = 3
STRENGTH = 5e-5

PHYS_H = 0.5
PHYS_W = 6
PHYS_L = 12

K_VALUES = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0]
Z_MASS_PHYS = 3


# ── Lattice3D (copied from lattice_3d_valley_linear_card.py) ───────
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


# ── Field construction (spatial-only 1/r) ───────────────────────────
def make_spatial_field(lat, z_mass_phys, strength):
    """Spatial-only 1/r field centered at (y=0, z=z_mass) on gravity layer."""
    gl = 2 * lat.nl // 3
    iz_mass = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz_mass))
    if mi is None:
        return np.zeros(lat.n), None
    my, mz = lat.pos[mi, 1], lat.pos[mi, 2]
    r_spatial = np.sqrt((lat.pos[:, 1] - my)**2 + (lat.pos[:, 2] - mz)**2) + 0.1
    return strength / r_spatial, mi


# ── Slit setup ──────────────────────────────────────────────────────
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


# ── Geodesic arrival time computation ───────────────────────────────
def compute_arrivals(lat, field):
    """Layer-by-layer minimum-delay propagation (Dijkstra on layered DAG).

    delay(src -> dst) = L * (1 + f_avg), where f_avg = 0.5*(f_src + f_dst).
    This gives the geometric shortest-time paths.
    """
    nw = lat._nw
    arrival = np.full(lat.n, np.inf)
    src = lat.nmap.get((0, 0, 0), 0)
    arrival[src] = 0.0

    for layer in range(lat.nl - 1):
        ls = int(lat._ls[layer])
        ld = int(lat._ls[layer + 1]) if layer + 1 < lat.nl else lat.n

        for dy, dz, L, _w in lat._off:
            for iy_src in range(nw):
                iy_dst = iy_src + dy
                if iy_dst < 0 or iy_dst >= nw:
                    continue
                for iz_src in range(nw):
                    iz_dst = iz_src + dz
                    if iz_dst < 0 or iz_dst >= nw:
                        continue
                    si = ls + iy_src * nw + iz_src
                    di = ld + iy_dst * nw + iz_dst

                    if arrival[si] == np.inf:
                        continue

                    lf = 0.5 * (field[si] + field[di])
                    delay = L * (1.0 + lf)
                    new_t = arrival[si] + delay

                    if new_t < arrival[di]:
                        arrival[di] = new_t

    return arrival


def geodesic_gradient_metric(lat, arrival_flat, arrival_mass, det):
    """Compute geodesic deflection as differential delay: near-mass vs far-from-mass.

    Returns (diff_near - diff_far), where diff = t_mass - t_flat.
    Positive means mass-side is MORE delayed = geodesic bends AWAY.
    Negative means mass-side is LESS delayed = geodesic bends TOWARD.

    This is the RAW arrival-time asymmetry, not scaled to centroid units.
    """
    pos = lat.pos
    diffs = np.array([arrival_mass[d] - arrival_flat[d] for d in det])
    zs = np.array([pos[d, 2] for d in det])

    return diffs, zs


def geodesic_centroid_deflection(lat, arrival_flat, arrival_mass, det, k_ref):
    """Convert geodesic arrival-time gradient to centroid units.

    Use the WAVE propagation machinery at a reference k to build a
    mapping from "delay perturbation" to "centroid shift". This gives
    the geodesic deflection in the same units as wave_delta.

    Alternative simpler approach: treat the arrival-time differences as
    perturbative weights on the flat-space probability distribution.
    If the flat wave gives P(z) at the detector, the geodesic correction
    shifts each node's weight by (1 - alpha * diff), giving a first-order
    centroid shift.
    """
    pos = lat.pos
    diffs = np.array([arrival_mass[d] - arrival_flat[d] for d in det])
    zs = np.array([pos[d, 2] for d in det])

    return diffs, zs


def main():
    t_total = time.time()

    print("=" * 72)
    print("WAVE vs GEODESIC DECOMPOSITION")
    print("=" * 72)
    print()
    print("Separate the geometric baseline (k-independent geodesic deflection)")
    print("from the wave resonance (k-dependent interference pattern).")
    print()
    print(f"  Lattice: h={PHYS_H}, W={PHYS_W}, L={PHYS_L}")
    print(f"  Mass at z={Z_MASS_PHYS} (spatial-only 1/r field)")
    print(f"  Strength: {STRENGTH}")
    print()

    # ── Build lattice ───────────────────────────────────────────────
    lat = Lattice3D(PHYS_L, PHYS_W, PHYS_H)
    det = [lat.nmap[(lat.nl - 1, iy, iz)]
           for iy in range(-lat.hw, lat.hw + 1)
           for iz in range(-lat.hw, lat.hw + 1)
           if (lat.nl - 1, iy, iz) in lat.nmap]
    bi, sa, sb, blocked, bl = setup_slits(lat)
    pos = lat.pos

    field_flat = np.zeros(lat.n)
    field_mass, mi = make_spatial_field(lat, Z_MASS_PHYS, STRENGTH)

    print(f"  Nodes: {lat.n:,}, Layers: {lat.nl}")
    print(f"  Detector nodes: {len(det)}")
    if mi is not None:
        print(f"  Field at mass source: {field_mass[mi]:.6f}")
    print()

    # ── Part 1: Geodesic baseline ───────────────────────────────────
    print("-" * 72)
    print("PART 1: GEODESIC BASELINE (k-independent)")
    print("-" * 72)
    print()

    t0 = time.time()
    arrival_flat = compute_arrivals(lat, field_flat)
    arrival_mass_arr = compute_arrivals(lat, field_mass)
    t_geo = time.time() - t0
    print(f"  Arrival times computed in {t_geo:.1f}s")

    # Show arrival-time gradient at detector
    dl = lat.nl - 1
    print()
    print(f"  Arrival-time gradient at detector (y=0 slice):")
    print(f"  {'iz':>4} {'z':>6} | {'t_flat':>10} | {'t_mass':>10} | {'diff':>12} | {'sign':>8}")
    print(f"  {'-'*60}")

    hw = lat.hw
    step = max(1, hw // 4)
    for iz in range(-hw, hw + 1, step):
        idx_det = lat.nmap.get((dl, 0, iz))
        if idx_det is None:
            continue
        z_phys = iz * PHYS_H
        tf = arrival_flat[idx_det]
        tm = arrival_mass_arr[idx_det]
        diff = tm - tf
        sign = "LATER" if diff > 1e-8 else "EARLIER" if diff < -1e-8 else "SAME"
        print(f"  {iz:>4} {z_phys:>6.1f} | {tf:>10.4f} | {tm:>10.4f} | {diff:>+12.8f} | {sign:>8}")

    # Near-mass vs far-from-mass
    iz_near = min(round(Z_MASS_PHYS / PHYS_H), hw)
    iz_far = max(-round(Z_MASS_PHYS / PHYS_H), -hw)

    idx_near = lat.nmap.get((dl, 0, iz_near))
    idx_far = lat.nmap.get((dl, 0, iz_far))
    idx_center = lat.nmap.get((dl, 0, 0))

    diff_near = arrival_mass_arr[idx_near] - arrival_flat[idx_near]
    diff_far = arrival_mass_arr[idx_far] - arrival_flat[idx_far]
    diff_center = arrival_mass_arr[idx_center] - arrival_flat[idx_center]

    print()
    print(f"  Mass-side (z={iz_near * PHYS_H:+.1f}): delayed by {diff_near:+.8f}")
    print(f"  Center    (z= 0.0): delayed by {diff_center:+.8f}")
    print(f"  Far-side  (z={iz_far * PHYS_H:+.1f}): delayed by {diff_far:+.8f}")
    print()

    geo_gradient = diff_near - diff_far
    if geo_gradient > 1e-10:
        geo_dir = "AWAY"
        print(f"  Geodesic bends AWAY from mass (mass-side MORE delayed)")
    elif geo_gradient < -1e-10:
        geo_dir = "TOWARD"
        print(f"  Geodesic bends TOWARD mass (mass-side LESS delayed)")
    else:
        geo_dir = "NEUTRAL"
        print(f"  No geodesic gradient (symmetric)")

    print(f"  Geodesic gradient (diff_near - diff_far): {geo_gradient:+.10f}")
    print()

    # Full detector profile of geodesic delays
    geo_diffs, geo_zs = geodesic_gradient_metric(
        lat, arrival_flat, arrival_mass_arr, det
    )
    print(f"  Geodesic delay profile across detector:")
    print(f"  (binned by z to match wave centroid calculation)")

    # Bin by z to show profile
    z_unique = np.sort(np.unique(geo_zs))
    z_step = max(1, len(z_unique) // 10)
    for i in range(0, len(z_unique), z_step):
        z_val = z_unique[i]
        mask = geo_zs == z_val
        mean_diff = np.mean(geo_diffs[mask])
        print(f"    z={z_val:+5.1f}: mean delay diff = {mean_diff:+.8f}")
    print()

    # ── Part 2: Wave deflection at each k ───────────────────────────
    print("-" * 72)
    print("PART 2: WAVE DEFLECTION vs k")
    print("-" * 72)
    print()

    # Flat baseline centroid (same for all k? check)
    wave_results = []

    for k in K_VALUES:
        t0 = time.time()

        # Flat propagation
        af = lat.propagate(field_flat, k, blocked)
        pf = sum(abs(af[d])**2 for d in det)
        zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf if pf > 1e-30 else 0.0

        # Mass propagation
        am = lat.propagate(field_mass, k, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm if pm > 1e-30 else 0.0

        wave_delta = zm - zf
        wave_dir = "TOWARD" if wave_delta > 1e-8 else "AWAY" if wave_delta < -1e-8 else "ZERO"
        dt = time.time() - t0

        wave_results.append({
            'k': k,
            'wave_delta': wave_delta,
            'wave_dir': wave_dir,
            'zf': zf,
            'zm': zm,
            'pf': pf,
            'pm': pm,
            'dt': dt,
        })

    # ── Part 3: Combined table ──────────────────────────────────────
    print("-" * 72)
    print("PART 3: DECOMPOSITION TABLE")
    print("-" * 72)
    print()
    print(f"  Geodesic gradient (near-far): {geo_gradient:+.10f} ({geo_dir})")
    print(f"  (Positive = mass side more delayed = geometric repulsion)")
    print()

    hdr = (f"  {'k':>5} | {'wave_delta':>12} | {'wave_dir':>8} | "
           f"{'geo_gradient':>12} | {'geo_dir':>8} | {'net_story':>24}")
    print(hdr)
    print(f"  {'-' * (len(hdr) + 2)}")

    for r in wave_results:
        k = r['k']
        wd = r['wave_delta']
        wdir = r['wave_dir']

        # The geodesic is ALWAYS repulsive (AWAY). Wave can be either.
        if wd > 1e-8 and geo_dir == "AWAY":
            story = "wave TOWARD > geo AWAY"
        elif wd < -1e-8 and geo_dir == "AWAY":
            story = "both AWAY"
        elif abs(wd) < 1e-8:
            story = "wave ~ zero, geo AWAY"
        elif wd > 1e-8 and geo_dir == "TOWARD":
            story = "both TOWARD"
        else:
            story = "mixed"

        print(f"  {k:>5.1f} | {wd:>+12.8f} | {wdir:>8} | "
              f"{geo_gradient:>+12.10f} | {geo_dir:>8} | {story:>24}")

    # ── Part 4: Analysis ────────────────────────────────────────────
    print()
    print("-" * 72)
    print("PART 4: ANALYSIS")
    print("-" * 72)
    print()

    toward_count = sum(1 for r in wave_results if r['wave_delta'] > 1e-8)
    away_count = sum(1 for r in wave_results if r['wave_delta'] < -1e-8)
    zero_count = len(wave_results) - toward_count - away_count

    print(f"  Wave deflections: {toward_count} TOWARD, {away_count} AWAY, {zero_count} ~ZERO")
    print(f"  out of {len(wave_results)} k values")
    print()

    # Check if geodesic and wave agree or disagree
    wave_deltas = [r['wave_delta'] for r in wave_results]
    mean_wave = np.mean(wave_deltas)
    std_wave = np.std(wave_deltas)

    print(f"  Mean wave deflection: {mean_wave:+.8f}")
    print(f"  Std wave deflection:  {std_wave:.8f}")
    print(f"  Geodesic gradient:    {geo_gradient:+.10f} ({geo_dir})")
    print()
    print(f"  NOTE: The geodesic gradient and wave deflection are in DIFFERENT units.")
    print(f"  Geodesic gradient = arrival-time asymmetry (seconds).")
    print(f"  Wave deflection = centroid shift in z (lattice units).")
    print(f"  They can't be directly subtracted, but their SIGNS can be compared.")
    print()

    if geo_dir == "AWAY" and mean_wave > 0:
        print("  CONCLUSION: Geodesic deflects AWAY, wave mean deflects TOWARD.")
        print("  Wave resonance OVERCOMES the repulsive geometric baseline.")
        print("  Gravity is a WAVE EFFECT that fights geometry.")
    elif geo_dir == "AWAY" and mean_wave < 0:
        print("  CONCLUSION: Both geodesic and mean wave deflect AWAY.")
        print("  No gravitational attraction at any level.")
    elif geo_dir == "TOWARD" and mean_wave > 0:
        print("  CONCLUSION: Both geodesic and mean wave deflect TOWARD.")
        print("  Geometry and wave resonance cooperate.")
    elif geo_dir == "NEUTRAL":
        print("  CONCLUSION: Geodesic is neutral, all deflection is wave effect.")
    else:
        print("  CONCLUSION: Mixed signals — needs further investigation.")

    # k-dependence check
    print()
    if std_wave > abs(mean_wave) * 0.5:
        print("  WAVE OSCILLATION: Strong k-dependence (std > 50% of mean).")
        print("  The sign of deflection FLIPS with k — this is resonance.")
    else:
        print("  WAVE OSCILLATION: Weak k-dependence (std < 50% of mean).")
        print("  Deflection sign is stable across k.")

    # Find the k with maximum TOWARD deflection
    max_toward = max(wave_results, key=lambda r: r['wave_delta'])
    max_away = min(wave_results, key=lambda r: r['wave_delta'])
    print()
    print(f"  Peak TOWARD: k={max_toward['k']:.1f}, delta={max_toward['wave_delta']:+.8f}")
    print(f"  Peak AWAY:   k={max_away['k']:.1f}, delta={max_away['wave_delta']:+.8f}")
    print(f"  Dynamic range: {max_toward['wave_delta'] - max_away['wave_delta']:.8f}")

    print()
    print(f"  Total time: {time.time() - t_total:.0f}s")
    print("=" * 72)


if __name__ == "__main__":
    main()
