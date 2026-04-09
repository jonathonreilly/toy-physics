#!/usr/bin/env python3
"""Resonance k-sweep: 2+1D vs 3+1D comparison.

Does the gravity resonance structure shift with spacetime dimension?

HYPOTHESIS: 3+1D has a different resonance window than 2+1D.
FALSIFICATION: If resonance structure is identical across dimensions.

Setup:
  2+1D: Lattice3D, h=0.5, W=6, L=12, spatial-only 1/r field, mass at z=3
  3+1D: Lattice4D, h=0.5, W=3, L=10, spatial-only 1/r^2 field, mass at z=2

k values: {0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0}

For each k: propagate flat + with mass, measure centroid shift.
"""

from __future__ import annotations
import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy required") from exc


# ---------------------------------------------------------------------------
# 2+1D Lattice (from lattice_3d_valley_linear_card.py)
# ---------------------------------------------------------------------------
BETA = 0.8
MAX_D_PHYS_3D = 3

class Lattice3D:
    def __init__(self, phys_l, phys_w, h):
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS_3D / h))
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
        n = self.n; nl = self.nl; nw = self._nw; hm = self._hm
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


# ---------------------------------------------------------------------------
# 3+1D Lattice (from frontier_3plus1d_closure_card.py)
# ---------------------------------------------------------------------------
MAX_D_PHYS_4D = 2
POWER_4D = 3

class Lattice4D:
    def __init__(self, phys_l, h, phys_w):
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS_4D / h))
        nw = 2 * self.hw + 1
        self.npl = nw ** 3
        self.n = self.nl * self.npl
        self._hm = h ** 3

        self.pos = np.zeros((self.n, 4))
        self.nmap = {}
        self._ls = np.zeros(self.nl, dtype=np.int64)
        idx = 0
        for layer in range(self.nl):
            self._ls[layer] = idx
            x = layer * h
            for iy in range(-self.hw, self.hw + 1):
                for iz in range(-self.hw, self.hw + 1):
                    for iw in range(-self.hw, self.hw + 1):
                        self.pos[idx] = (x, iy * h, iz * h, iw * h)
                        self.nmap[(layer, iy, iz, iw)] = idx
                        idx += 1

        self._off = []
        md = self.max_d
        for dy in range(-md, md + 1):
            for dz in range(-md, md + 1):
                for dw in range(-md, md + 1):
                    dyp, dzp, dwp = dy * h, dz * h, dw * h
                    L = math.sqrt(h*h + dyp*dyp + dzp*dzp + dwp*dwp)
                    r_trans = math.sqrt(dyp**2 + dzp**2 + dwp**2)
                    theta = math.atan2(r_trans, h)
                    w = math.exp(-BETA * theta * theta)
                    self._off.append((dy, dz, dw, L, w))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        n = self.n; nl = self.nl; nw = self._nw; hm = self._hm
        amps = np.zeros(n, dtype=np.complex128)
        src = self.nmap.get((0, 0, 0, 0), 0)
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

            for dy, dz, dw, L, w in self._off:
                ym = max(0, -dy); yM = min(nw, nw - dy)
                zm = max(0, -dz); zM = min(nw, nw - dz)
                wm = max(0, -dw); wM = min(nw, nw - dw)
                if ym >= yM or zm >= zM or wm >= wM:
                    continue
                yr = np.arange(ym, yM)
                zr = np.arange(zm, zM)
                wr = np.arange(wm, wM)
                siy, siz, siw = np.meshgrid(yr, zr, wr, indexing='ij')
                si = siy.ravel()*nw*nw + siz.ravel()*nw + siw.ravel()
                di = ((siy.ravel()+dy)*nw*nw + (siz.ravel()+dz)*nw + (siw.ravel()+dw))
                a = sa[si]; nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue
                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L ** POWER_4D)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


# ---------------------------------------------------------------------------
# Spatial-only fields
# ---------------------------------------------------------------------------
def make_field_3d_spatial(lat, z_mass_phys, strength):
    """2+1D spatial-only field: 1/r using (y,z) only, no causal x."""
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    my, mz = lat.pos[mi, 1], lat.pos[mi, 2]
    r = np.sqrt((lat.pos[:, 1] - my)**2 + (lat.pos[:, 2] - mz)**2) + 0.1
    return strength / r, mi


def make_field_4d_spatial(lat, z_mass_phys, strength):
    """3+1D spatial-only field: 1/r^2 using (y,z,w) only, no causal x."""
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz, 0))
    if mi is None:
        return np.zeros(lat.n), None
    my, mz, mw = lat.pos[mi, 1], lat.pos[mi, 2], lat.pos[mi, 3]
    r = np.sqrt(
        (lat.pos[:, 1] - my)**2 +
        (lat.pos[:, 2] - mz)**2 +
        (lat.pos[:, 3] - mw)**2
    ) + 0.1
    return strength / (r ** 2), mi


# ---------------------------------------------------------------------------
# Slit setup
# ---------------------------------------------------------------------------
def setup_slits_3d(lat):
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


def setup_slits_4d(lat):
    bl = lat.nl // 3
    bi = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            for iw in range(-lat.hw, lat.hw + 1):
                idx = lat.nmap.get((bl, iy, iz, iw))
                if idx is not None:
                    bi.append(idx)
    sa = [i for i in bi if lat.pos[i, 1] >= 0.5]
    sb = [i for i in bi if lat.pos[i, 1] <= -0.5]
    blocked = set(bi) - set(sa + sb)
    return blocked


# ---------------------------------------------------------------------------
# k-sweep
# ---------------------------------------------------------------------------
K_VALUES = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0]
STRENGTH = 5e-5


def sweep_2plus1d():
    """k-sweep on 2+1D lattice."""
    print("=" * 70)
    print("  2+1D k-SWEEP: h=0.5, W=6, L=12, mass at z=3")
    print("  Field: spatial-only 1/r, strength=5e-5")
    print("=" * 70)

    t0 = time.time()
    lat = Lattice3D(phys_l=12, phys_w=6, h=0.5)
    blocked = setup_slits_3d(lat)
    det = [lat.nmap[(lat.nl-1, iy, iz)]
           for iy in range(-lat.hw, lat.hw+1)
           for iz in range(-lat.hw, lat.hw+1)
           if (lat.nl-1, iy, iz) in lat.nmap]
    pos = lat.pos
    print(f"  Lattice: {lat.n:,} nodes, {lat.nl} layers, {lat.npl} nodes/layer")
    print(f"  Build time: {time.time()-t0:.1f}s")
    print()

    results = []
    for k in K_VALUES:
        t1 = time.time()
        # Flat
        af = lat.propagate(np.zeros(lat.n), k, blocked)
        pf = sum(abs(af[d])**2 for d in det)
        if pf < 1e-30:
            print(f"  k={k:5.1f}  NO SIGNAL")
            results.append((k, 0.0, "NONE"))
            continue
        zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf

        # With mass
        field, _ = make_field_3d_spatial(lat, 3.0, STRENGTH)
        am = lat.propagate(field, k, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        if pm < 1e-30:
            print(f"  k={k:5.1f}  NO SIGNAL (mass)")
            results.append((k, 0.0, "NONE"))
            continue
        zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
        delta = zm - zf
        direction = "TOWARD" if delta > 0 else "AWAY"
        dt = time.time() - t1
        print(f"  k={k:5.1f}  delta={delta:+.8f}  {direction:<6s}  ({dt:.1f}s)")
        results.append((k, delta, direction))

    return results


def sweep_3plus1d():
    """k-sweep on 3+1D lattice."""
    print()
    print("=" * 70)
    print("  3+1D k-SWEEP: h=0.5, W=3, L=10, mass at z=2")
    print("  Field: spatial-only 1/r^2, strength=5e-5")
    print("=" * 70)

    t0 = time.time()
    lat = Lattice4D(phys_l=10, h=0.5, phys_w=3)
    blocked = setup_slits_4d(lat)
    det = [lat.nmap[(lat.nl-1, iy, iz, iw)]
           for iy in range(-lat.hw, lat.hw+1)
           for iz in range(-lat.hw, lat.hw+1)
           for iw in range(-lat.hw, lat.hw+1)
           if (lat.nl-1, iy, iz, iw) in lat.nmap]
    pos = lat.pos
    print(f"  Lattice: {lat.n:,} nodes, {lat.nl} layers, {lat.npl} nodes/layer")
    print(f"  Build time: {time.time()-t0:.1f}s")
    print()

    results = []
    for k in K_VALUES:
        t1 = time.time()
        # Flat
        af = lat.propagate(np.zeros(lat.n), k, blocked)
        pf = sum(abs(af[d])**2 for d in det)
        if pf < 1e-30:
            print(f"  k={k:5.1f}  NO SIGNAL")
            results.append((k, 0.0, "NONE"))
            continue
        zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf

        # With mass
        field, _ = make_field_4d_spatial(lat, 2.0, STRENGTH)
        am = lat.propagate(field, k, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        if pm < 1e-30:
            print(f"  k={k:5.1f}  NO SIGNAL (mass)")
            results.append((k, 0.0, "NONE"))
            continue
        zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
        delta = zm - zf
        direction = "TOWARD" if delta > 0 else "AWAY"
        dt = time.time() - t1
        print(f"  k={k:5.1f}  delta={delta:+.8f}  {direction:<6s}  ({dt:.1f}s)")
        results.append((k, delta, direction))

    return results


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
def analyze(res_2d, res_3d):
    print()
    print("=" * 70)
    print("  COMPARISON TABLE")
    print("=" * 70)
    print()
    print(f"  {'k':>5s}  |  {'2+1D delta':>14s}  {'dir':>6s}  |  {'3+1D delta':>14s}  {'dir':>6s}")
    print(f"  {'-'*5}  +  {'-'*14}  {'-'*6}  +  {'-'*14}  {'-'*6}")

    for (k2, d2, dir2), (k3, d3, dir3) in zip(res_2d, res_3d):
        print(f"  {k2:5.1f}  |  {d2:+14.8f}  {dir2:>6s}  |  {d3:+14.8f}  {dir3:>6s}")

    # Identify sign-change windows
    print()
    print("=" * 70)
    print("  RESONANCE ANALYSIS")
    print("=" * 70)

    for label, results in [("2+1D", res_2d), ("3+1D", res_3d)]:
        print(f"\n  {label}:")
        attract = [(k, d) for k, d, dr in results if dr == "TOWARD"]
        repel = [(k, d) for k, d, dr in results if dr == "AWAY"]
        if attract:
            k_min = min(k for k, _ in attract)
            k_max = max(k for k, _ in attract)
            peak_k, peak_d = max(attract, key=lambda x: x[1])
            print(f"    Attractive window: k in [{k_min:.1f}, {k_max:.1f}]")
            print(f"    Peak attraction:   k={peak_k:.1f}, delta={peak_d:+.8f}")
        else:
            print(f"    No attractive k values found!")
        if repel:
            print(f"    Repulsive k values: {[k for k, _ in repel]}")

        # Find sign changes
        signs = [(k, 1 if d > 0 else -1) for k, d, _ in results if d != 0]
        changes = []
        for i in range(len(signs) - 1):
            if signs[i][1] != signs[i+1][1]:
                changes.append((signs[i][0], signs[i+1][0]))
        if changes:
            print(f"    Sign changes between: {changes}")

    # Period analysis
    print()
    print("=" * 70)
    print("  OSCILLATION PERIOD COMPARISON")
    print("=" * 70)
    for label, results in [("2+1D", res_2d), ("3+1D", res_3d)]:
        deltas = [(k, d) for k, d, _ in results if abs(d) > 1e-12]
        signs = [(k, 1 if d > 0 else -1) for k, d in deltas]
        changes = []
        for i in range(len(signs) - 1):
            if signs[i][1] != signs[i+1][1]:
                mid = 0.5 * (signs[i][0] + signs[i+1][0])
                changes.append(mid)
        if len(changes) >= 2:
            periods = [changes[i+1] - changes[i] for i in range(len(changes)-1)]
            avg_period = sum(periods) / len(periods)
            print(f"  {label}: sign-change k-values ~{changes}, avg period ~{avg_period:.1f}")
        elif len(changes) == 1:
            print(f"  {label}: single sign change at k~{changes[0]:.1f}")
        else:
            print(f"  {label}: no sign changes detected (monotonic)")

    # Key questions
    print()
    print("=" * 70)
    print("  KEY QUESTIONS")
    print("=" * 70)

    # Q1: Same resonance period?
    # (Answered by period comparison above)

    # Q2: Does attractive window shift?
    attract_2d = [(k, d) for k, d, dr in res_2d if dr == "TOWARD"]
    attract_3d = [(k, d) for k, d, dr in res_3d if dr == "TOWARD"]
    if attract_2d and attract_3d:
        center_2d = sum(k*abs(d) for k, d in attract_2d) / sum(abs(d) for _, d in attract_2d)
        center_3d = sum(k*abs(d) for k, d in attract_3d) / sum(abs(d) for _, d in attract_3d)
        print(f"  Q2: Weighted center of attraction:")
        print(f"      2+1D: k={center_2d:.2f}")
        print(f"      3+1D: k={center_3d:.2f}")
        shift = center_3d - center_2d
        print(f"      Shift: {shift:+.2f}")
        if abs(shift) > 0.5:
            print(f"      -> Window SHIFTS with dimension")
        else:
            print(f"      -> Window roughly SAME across dimensions")
    elif attract_2d:
        print(f"  Q2: 2+1D has attraction, 3+1D does NOT -> strongly shifted or absent")
    elif attract_3d:
        print(f"  Q2: 3+1D has attraction, 2+1D does NOT -> strongly shifted or absent")
    else:
        print(f"  Q2: Neither dimension has attraction!")

    # Q3: Is k=5.0 in the attractive window for 3+1D?
    k5_3d = next(((k, d, dr) for k, d, dr in res_3d if k == 5.0), None)
    if k5_3d:
        print(f"  Q3: k=5.0 in 3+1D: delta={k5_3d[1]:+.8f} ({k5_3d[2]})")
        if k5_3d[2] == "TOWARD":
            print(f"      -> YES, k=5.0 is in the attractive window")
        else:
            print(f"      -> NO, k=5.0 is NOT in the attractive window")
    else:
        print(f"  Q3: k=5.0 not found in sweep results")

    # Verdict
    print()
    print("=" * 70)
    print("  VERDICT")
    print("=" * 70)

    signs_2d = set(dr for _, _, dr in res_2d if dr != "NONE")
    signs_3d = set(dr for _, _, dr in res_3d if dr != "NONE")
    has_resonance_2d = len(signs_2d) > 1
    has_resonance_3d = len(signs_3d) > 1

    if has_resonance_2d and has_resonance_3d:
        print("  Both 2+1D and 3+1D show resonance structure (sign changes in k).")
        if attract_2d and attract_3d:
            center_2d = sum(k*abs(d) for k, d in attract_2d) / sum(abs(d) for _, d in attract_2d)
            center_3d = sum(k*abs(d) for k, d in attract_3d) / sum(abs(d) for _, d in attract_3d)
            if abs(center_3d - center_2d) > 0.5:
                print("  HYPOTHESIS SUPPORTED: Resonance window shifts with dimension.")
            else:
                print("  HYPOTHESIS FALSIFIED: Resonance window is similar across dimensions.")
        else:
            print("  Mixed — resonance exists but attraction pattern differs.")
    elif has_resonance_2d and not has_resonance_3d:
        print("  2+1D has resonance, 3+1D is monotonic -> dimensions differ fundamentally.")
        print("  HYPOTHESIS SUPPORTED (stronger than expected).")
    elif has_resonance_3d and not has_resonance_2d:
        print("  3+1D has resonance, 2+1D is monotonic -> dimensions differ fundamentally.")
        print("  HYPOTHESIS SUPPORTED (stronger than expected).")
    else:
        print("  Neither dimension shows resonance -> no oscillatory structure.")
        print("  HYPOTHESIS FALSIFIED: No resonance in either dimension.")


def main():
    print("=" * 70)
    print("FRONTIER: RESONANCE k-SWEEP — 2+1D vs 3+1D")
    print("=" * 70)
    print()
    print("Does the gravity resonance structure shift with spacetime dimension?")
    print()
    print("HYPOTHESIS: 3+1D has a different resonance window than 2+1D.")
    print("FALSIFICATION: If resonance structure is identical across dimensions.")
    print()

    t_total = time.time()
    res_2d = sweep_2plus1d()
    res_3d = sweep_3plus1d()
    analyze(res_2d, res_3d)

    print()
    print(f"  Total runtime: {time.time()-t_total:.0f}s")
    print()


if __name__ == "__main__":
    main()
