#!/usr/bin/env python3
"""Systematic investigation of angular kernel w(theta) on the 3D lattice.

Hypothesis: "There exists a simpler angular kernel than exp(-0.8*theta^2)
that passes Born + gravity + k=0 tests while having better rotational
isotropy."

Falsification: "If NO tested alternative passes all three core tests,
exp(-0.8*theta^2) is the minimum viable kernel despite its anisotropy."

Tests for each kernel:
  1. Born rule (3-slit Sorkin |I3|/P < 1e-10)
  2. Gravity sign (centroid shift TOWARD mass at z=3)
  3. k=0 control (gravity vanishes at k=0)
  4. Rotational isotropy (mass at z=3 vs 45-degree, anisotropy %)
  5. Amplitude norm (total detector probability finite and nonzero)
"""
from __future__ import annotations
import math
import time

import numpy as np

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
K = 5.0
STRENGTH = 5e-5
PHYS_W = 6
PHYS_L = 12
H = 0.5
MAX_D_PHYS = 3


# ---------------------------------------------------------------------------
# Lattice3D — adapted to accept a weight_fn parameter
# ---------------------------------------------------------------------------
class Lattice3D:
    def __init__(self, phys_l, phys_w, h, weight_fn):
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
                w = weight_fn(theta)
                self._off.append((dy, dz, L, w))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        n = self.n
        hw = self.hw
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
            sa = amps[ls:ls + self.npl].copy()
            sa[blocked[ls:ls + self.npl]] = 0
            if np.max(np.abs(sa)) < 1e-30:
                continue
            sf = field[ls:ls + self.npl]
            df = field[ld:ld + self.npl]
            db = blocked[ld:ld + self.npl]
            for dy, dz, L, w in self._off:
                ym = max(0, -dy)
                yM = min(nw, nw - dy)
                zm = max(0, -dz)
                zM = min(nw, nw - dz)
                if ym >= yM or zm >= zM:
                    continue
                yr = np.arange(ym, yM)
                zr = np.arange(zm, zM)
                siy, siz = np.meshgrid(yr, zr, indexing='ij')
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
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def make_field(lat, z_mass_phys, strength):
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    mx, my, mz = lat.pos[mi]
    r = np.sqrt(
        (lat.pos[:, 0] - mx) ** 2
        + (lat.pos[:, 1] - my) ** 2
        + (lat.pos[:, 2] - mz) ** 2
    ) + 0.1
    return strength / r, mi


def make_field_yz(lat, y_mass_phys, z_mass_phys, strength):
    """Place mass at EXACT physical (y, z) — no grid snapping.

    Uses exact floating-point coordinates for the 1/r field center,
    ensuring identical field strength at beam axis regardless of angle.
    """
    x_phys = (2 * lat.nl // 3) * lat.h
    r = np.sqrt(
        (lat.pos[:, 0] - x_phys) ** 2
        + (lat.pos[:, 1] - y_mass_phys) ** 2
        + (lat.pos[:, 2] - z_mass_phys) ** 2
    ) + 0.1
    iy = round(y_mass_phys / lat.h)
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, iy, iz))
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


# ---------------------------------------------------------------------------
# Kernel definitions
# ---------------------------------------------------------------------------
KERNELS = [
    ("uniform",          lambda theta: 1.0),
    ("cos(theta)",       lambda theta: math.cos(theta)),
    ("cos^2(theta)",     lambda theta: math.cos(theta) ** 2),
    ("exp(-0.8*t^2)",    lambda theta: math.exp(-0.8 * theta * theta)),
    ("exp(-0.4*t^2)",    lambda theta: math.exp(-0.4 * theta * theta)),
    ("exp(-1.6*t^2)",    lambda theta: math.exp(-1.6 * theta * theta)),
    ("linear_falloff",   lambda theta: max(0.0, 1.0 - theta / (math.pi / 2))),
]


# ---------------------------------------------------------------------------
# Test suite for one kernel
# ---------------------------------------------------------------------------
def test_kernel(name, weight_fn):
    t0 = time.time()
    lat = Lattice3D(PHYS_L, PHYS_W, H, weight_fn)
    det = [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]
    pos = lat.pos
    field_f = np.zeros(lat.n)
    bi, sa, sb, blocked, bl = setup_slits(lat)

    # Free propagation baseline
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d]) ** 2 for d in det)
    zf = sum(abs(af[d]) ** 2 * pos[d, 2] for d in det) / pf if pf > 1e-30 else 0

    # --- Test 1: Born rule (3-slit Sorkin) ---
    upper = sorted([i for i in bi if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [i for i in bi if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1]
    born = float('nan')
    if upper and lower and middle:
        s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
        all_s = set(s_a + s_b + s_c)
        other = set(bi) - all_s
        probs = {}
        for key, open_set in [
            ('abc', all_s),
            ('ab', set(s_a + s_b)),
            ('ac', set(s_a + s_c)),
            ('bc', set(s_b + s_c)),
            ('a', set(s_a)),
            ('b', set(s_b)),
            ('c', set(s_c)),
        ]:
            bl2 = other | (all_s - open_set)
            a = lat.propagate(field_f, K, bl2)
            probs[key] = np.array([abs(a[d]) ** 2 for d in det])
        I3 = 0.0
        P = 0.0
        for di in range(len(det)):
            i3 = (
                probs['abc'][di]
                - probs['ab'][di]
                - probs['ac'][di]
                - probs['bc'][di]
                + probs['a'][di]
                + probs['b'][di]
                + probs['c'][di]
            )
            I3 += abs(i3)
            P += probs['abc'][di]
        born = I3 / P if P > 1e-30 else float('nan')

    # --- Test 2: Gravity sign (mass at z=3) ---
    field_m3, _ = make_field(lat, 3, STRENGTH)
    am3 = lat.propagate(field_m3, K, blocked)
    pm3 = sum(abs(am3[d]) ** 2 for d in det)
    grav = 0.0
    if pm3 > 1e-30:
        zm3 = sum(abs(am3[d]) ** 2 * pos[d, 2] for d in det) / pm3
        grav = zm3 - zf

    # --- Test 3: k=0 control ---
    am0 = lat.propagate(field_m3, 0.0, blocked)
    af0 = lat.propagate(field_f, 0.0, blocked)
    pm0 = sum(abs(am0[d]) ** 2 for d in det)
    pf0 = sum(abs(af0[d]) ** 2 for d in det)
    gk0 = 0.0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (
            sum(abs(am0[d]) ** 2 * pos[d, 2] for d in det) / pm0
            - sum(abs(af0[d]) ** 2 * pos[d, 2] for d in det) / pf0
        )

    # --- Test 4: Rotational isotropy ---
    # Mass at (y=0, z=3) vs mass at 45-degree (y~2.12, z~2.12)
    r45 = 3.0 / math.sqrt(2)
    field_45, mi45 = make_field_yz(lat, r45, r45, STRENGTH)
    aniso = float('nan')
    if mi45 is not None:
        a45 = lat.propagate(field_45, K, blocked)
        p45 = sum(abs(a45[d]) ** 2 for d in det)
        if p45 > 1e-30:
            # Measure deflection magnitude in yz-plane
            yz_z3 = abs(grav)  # z-axis deflection magnitude
            y45 = sum(abs(a45[d]) ** 2 * pos[d, 1] for d in det) / p45
            z45 = sum(abs(a45[d]) ** 2 * pos[d, 2] for d in det) / p45
            defl_45 = math.sqrt(y45**2 + (z45 - zf)**2) if pf > 1e-30 else 0
            # Anisotropy: how different are the two deflection magnitudes?
            avg = 0.5 * (yz_z3 + defl_45)
            if avg > 1e-15:
                aniso = 100.0 * abs(yz_z3 - defl_45) / avg

    # --- Test 5: Amplitude norm ---
    det_prob = pf

    elapsed = time.time() - t0
    return {
        'name': name,
        'born': born,
        'grav': grav,
        'gk0': gk0,
        'aniso': aniso,
        'det_prob': det_prob,
        'time': elapsed,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 90)
    print("ANGULAR KERNEL INVESTIGATION")
    print("=" * 90)
    print()
    print("Hypothesis: There exists a simpler angular kernel than exp(-0.8*theta^2)")
    print("  that passes Born + gravity + k=0 tests with better rotational isotropy.")
    print()
    print("Falsification: If NO tested alternative passes all three core tests,")
    print("  exp(-0.8*theta^2) is the minimum viable kernel despite its anisotropy.")
    print()
    print(f"Parameters: h={H}, W={PHYS_W}, L={PHYS_L}, k={K}, strength={STRENGTH}")
    print(f"Action: S = L(1-f), Kernel: 1/L^2, h^2 measure")
    print()
    print("Pass criteria:")
    print("  Born:     |I3|/P < 1e-10")
    print("  Gravity:  centroid shift > 0 (TOWARD)")
    print("  k=0:      |shift| < 1e-6")
    print("  Isotropy: lower anisotropy% is better (no hard threshold)")
    print("  DetProb:  must be finite and > 0")
    print()

    results = []
    for name, wfn in KERNELS:
        print(f"  Testing: {name} ...", flush=True)
        r = test_kernel(name, wfn)
        results.append(r)
        born_pass = r['born'] < 1e-10
        grav_pass = r['grav'] > 0
        k0_pass = abs(r['gk0']) < 1e-6
        prob_ok = r['det_prob'] > 0 and np.isfinite(r['det_prob'])
        verdict = "PASS" if (born_pass and grav_pass and k0_pass and prob_ok) else "FAIL"
        tags = []
        if not born_pass:
            tags.append("born")
        if not grav_pass:
            tags.append("grav")
        if not k0_pass:
            tags.append("k=0")
        if not prob_ok:
            tags.append("prob")
        fail_str = f" [{','.join(tags)}]" if tags else ""
        print(f"    -> {verdict}{fail_str}  ({r['time']:.0f}s)")

    # Summary table
    print()
    print("=" * 90)
    print(f"{'kernel':<20s} | {'Born I3/P':>12s} | {'grav sign':>10s} | {'k=0':>10s} | {'aniso%':>8s} | {'det_prob':>10s} | VERDICT")
    print("-" * 90)
    for r in results:
        born_pass = r['born'] < 1e-10
        grav_pass = r['grav'] > 0
        k0_pass = abs(r['gk0']) < 1e-6
        prob_ok = r['det_prob'] > 0 and np.isfinite(r['det_prob'])
        all_pass = born_pass and grav_pass and k0_pass and prob_ok

        grav_str = f"{r['grav']:+.6f}" if r['grav'] != 0 else "0"
        grav_dir = "T" if r['grav'] > 0 else "A" if r['grav'] < 0 else "-"
        aniso_str = f"{r['aniso']:.1f}" if not math.isnan(r['aniso']) else "N/A"
        verdict = "PASS" if all_pass else "FAIL"

        print(
            f"{r['name']:<20s} | {r['born']:>12.2e} | {grav_str:>8s}({grav_dir}) | {r['gk0']:>+10.2e} | {aniso_str:>8s} | {r['det_prob']:>10.4e} | {verdict}"
        )

    print("-" * 90)

    # Analysis
    print()
    print("ANALYSIS")
    print("-" * 40)
    passing = [r for r in results if r['born'] < 1e-10 and r['grav'] > 0 and abs(r['gk0']) < 1e-6]
    if not passing:
        print("No kernel passes all three core tests.")
        print("FALSIFIED: exp(-0.8*theta^2) may be uniquely required,")
        print("  or the test parameters are too restrictive.")
    else:
        print(f"{len(passing)} kernel(s) pass all three core tests:")
        for r in passing:
            aniso_str = f"{r['aniso']:.1f}%" if not math.isnan(r['aniso']) else "N/A"
            print(f"  - {r['name']:<20s}  anisotropy={aniso_str}  grav={r['grav']:+.6f}")

        # Find best isotropy among passing
        iso_pass = [r for r in passing if not math.isnan(r['aniso'])]
        if iso_pass:
            best = min(iso_pass, key=lambda r: r['aniso'])
            default = next((r for r in results if r['name'] == 'exp(-0.8*t^2)'), None)
            print()
            print(f"Best isotropy among passing: {best['name']} ({best['aniso']:.1f}%)")
            if default and not math.isnan(default['aniso']):
                print(f"Default exp(-0.8*t^2):       anisotropy={default['aniso']:.1f}%")
                if best['aniso'] < default['aniso']:
                    print(f"HYPOTHESIS SUPPORTED: {best['name']} is simpler and more isotropic.")
                else:
                    print(f"Default has equal or better isotropy among passing kernels.")

    # Detailed notes on each kernel
    print()
    print("DETAILED NOTES")
    print("-" * 40)
    for r in results:
        born_p = "PASS" if r['born'] < 1e-10 else "FAIL"
        grav_p = "PASS" if r['grav'] > 0 else "FAIL"
        k0_p = "PASS" if abs(r['gk0']) < 1e-6 else "FAIL"
        print(f"{r['name']}:")
        print(f"  Born={r['born']:.2e}({born_p})  grav={r['grav']:+.6f}({grav_p})  k0={r['gk0']:+.2e}({k0_p})")
        if not math.isnan(r['aniso']):
            print(f"  anisotropy={r['aniso']:.1f}%  det_prob={r['det_prob']:.4e}")
        else:
            print(f"  anisotropy=N/A  det_prob={r['det_prob']:.4e}")
        print()


if __name__ == "__main__":
    main()
