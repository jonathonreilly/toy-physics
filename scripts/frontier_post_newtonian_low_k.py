#!/usr/bin/env python3
"""Post-Newtonian low-k regime: test whether sign reversal is phase wrapping.

CONTEXT:
  The post-Newtonian experiment (frontier_post_newtonian_detection.py) found
  the f^2 correction is detectable at s=5e-2 (max f=0.5, 3% deviation), but
  with an UNEXPECTED sign: PN suppresses gravity instead of enhancing it.

HYPOTHESIS:
  At k=5 and max f=0.5, the phase k*S can exceed pi, entering a
  non-perturbative regime. At low k (max_phase < pi), the PN action
  should ENHANCE gravity because both -f and -f^2/2 contribute same-sign
  phase deficit.

FALSIFICATION:
  If PN still suppresses gravity even at k=0.5 (max_phase << pi), the
  sign reversal is fundamental, not phase wrapping.

EXPERIMENT:
  1. Sweep k in {0.5, 1.0, 2.0, 5.0, 10.0} at fixed s=5e-2
  2. For k=1.0, sweep s from 5e-6 to 5e-2
  3. Report max_phase = k * max(|act|) and regime classification
"""

from __future__ import annotations
import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc

BETA = 0.8
MAX_D_PHYS = 3


class Lattice3D:
    """3D ordered lattice -- copied from frontier_post_newtonian_detection.py."""

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

    def propagate(self, field, k, blocked_set, action_mode="valley_linear"):
        """Propagate with selectable action variant."""
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
                siy, siz = np.meshgrid(yr, zr, indexing="ij")
                si = siy.ravel() * nw + siz.ravel()
                di = (siy.ravel() + dy) * nw + (siz.ravel() + dz)
                a = sa[si]
                nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue
                lf = 0.5 * (sf[si[nz]] + df[di[nz]])

                if action_mode == "valley_linear":
                    act = L * (1 - lf)
                elif action_mode == "post_newtonian":
                    act = L * (1 - lf - 0.5 * lf * lf)
                elif action_mode == "control_plus":
                    act = L * (1 - lf + 0.5 * lf * lf)
                else:
                    raise ValueError(f"Unknown action_mode: {action_mode}")

                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


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


def measure_gravity(lat, field, k, blocked, det, zf, action_mode):
    """Return centroid shift delta_z for given action mode."""
    amps = lat.propagate(field, k, blocked, action_mode=action_mode)
    prob = sum(abs(amps[d]) ** 2 for d in det)
    if prob < 1e-30:
        return 0.0
    z_centroid = sum(abs(amps[d]) ** 2 * lat.pos[d, 2] for d in det) / prob
    return z_centroid - zf


def compute_max_phase(lat, field, k, action_mode):
    """Compute max |k * act| across all edges to check for phase wrapping."""
    max_act = 0.0
    for dy, dz, L, w in lat._off:
        # Sample field at a few representative points near the mass
        # We just need the maximum action value
        pass
    # Simpler: compute action for all field values
    f_vals = field[field > 1e-10]
    if len(f_vals) == 0:
        return 0.0
    max_f = np.max(f_vals)
    # The edge with minimum L (=h) and maximum f gives max action deviation
    h = lat.h
    if action_mode == "valley_linear":
        act_at_max_f = h * (1 - max_f)
    elif action_mode == "post_newtonian":
        act_at_max_f = h * (1 - max_f - 0.5 * max_f * max_f)
    elif action_mode == "control_plus":
        act_at_max_f = h * (1 - max_f + 0.5 * max_f * max_f)
    else:
        act_at_max_f = h
    return abs(k * act_at_max_f)


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
    return blocked


def flat_centroid(lat, k, blocked, det):
    """Get flat-field centroid for a given k."""
    field_flat = np.zeros(lat.n)
    amps = lat.propagate(field_flat, k, blocked, action_mode="valley_linear")
    prob = sum(abs(amps[d]) ** 2 for d in det)
    if prob < 1e-30:
        return 0.0
    return sum(abs(amps[d]) ** 2 * lat.pos[d, 2] for d in det) / prob


def main():
    print("=" * 78)
    print("POST-NEWTONIAN LOW-k REGIME: PHASE WRAPPING TEST")
    print("=" * 78)
    print()
    print("HYPOTHESIS: At low k (max_phase < pi), PN enhances gravity.")
    print("            The sign reversal at k=5 is phase wrapping.")
    print()
    print("FALSIFICATION: If PN still suppresses gravity at k=0.5")
    print("               (max_phase << pi), the sign reversal is fundamental.")
    print()

    h = 0.5
    phys_w = 6
    phys_l = 12

    t0 = time.time()
    lat = Lattice3D(phys_l, phys_w, h)
    print(f"Lattice: h={h}, W={phys_w}, L={phys_l}")
    print(f"  {lat.n:,} nodes, {lat.nl} layers")

    det = [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]
    blocked = setup_slits(lat)
    print(f"  Setup time: {time.time()-t0:.1f}s")
    print()

    # ================================================================
    # EXPERIMENT 1: Sweep k at fixed s = 5e-2
    # ================================================================
    print("=" * 78)
    print("EXPERIMENT 1: k-sweep at s = 5e-2")
    print("=" * 78)
    print()

    s_fixed = 5e-2
    field_s, _ = make_field(lat, 3, s_fixed)
    max_f = np.max(field_s)
    print(f"Field: s = {s_fixed}, max f = {max_f:.5f}")
    print()

    k_values = [0.5, 1.0, 2.0, 5.0, 10.0]
    modes = ["valley_linear", "post_newtonian", "control_plus"]
    mode_short = {"valley_linear": "VL", "post_newtonian": "PN", "control_plus": "CTL"}

    header = (f"{'k':>6} | {'max_phase':>10} | {'regime':>12} | "
              f"{'VL shift':>12} | {'PN shift':>12} | {'CTL shift':>12} | "
              f"{'PN/VL':>8} | {'PN-VL%':>8}")
    print(header)
    print("-" * len(header))

    k_results = []
    for k in k_values:
        # Flat centroid depends on k
        zf = flat_centroid(lat, k, blocked, det)

        # Max phase for VL action
        max_phase_vl = compute_max_phase(lat, field_s, k, "valley_linear")
        max_phase_pn = compute_max_phase(lat, field_s, k, "post_newtonian")
        # Use the VL max phase as the reference
        regime = "perturbative" if max_phase_vl < math.pi else "WRAPPING"

        shifts = {}
        for mode in modes:
            shifts[mode] = measure_gravity(lat, field_s, k, blocked, det, zf, mode)

        vl = shifts["valley_linear"]
        pn = shifts["post_newtonian"]
        ctl = shifts["control_plus"]

        ratio_pn = pn / vl if abs(vl) > 1e-12 else float("nan")
        pct_diff = 100 * (pn - vl) / abs(vl) if abs(vl) > 1e-12 else float("nan")

        row = (f"{k:>6.1f} | {max_phase_vl:>10.4f} | {regime:>12s} | "
               f"{vl:>+12.8f} | {pn:>+12.8f} | {ctl:>+12.8f} | "
               f"{ratio_pn:>8.4f} | {pct_diff:>+8.2f}%")
        print(row)

        k_results.append({
            "k": k, "max_phase": max_phase_vl, "regime": regime,
            "vl": vl, "pn": pn, "ctl": ctl,
            "ratio": ratio_pn, "pct": pct_diff,
        })

    print()

    # ================================================================
    # EXPERIMENT 2: s-sweep at k = 1.0 (perturbative regime)
    # ================================================================
    print("=" * 78)
    print("EXPERIMENT 2: s-sweep at k = 1.0 (perturbative regime)")
    print("=" * 78)
    print()

    k_fixed = 1.0
    zf_k1 = flat_centroid(lat, k_fixed, blocked, det)
    print(f"k = {k_fixed}, flat centroid z = {zf_k1:.6f}")
    print()

    strengths = [5e-6, 5e-5, 5e-4, 5e-3, 5e-2]

    header2 = (f"{'s':>10} | {'max_f':>8} | {'max_phase':>10} | "
               f"{'VL shift':>12} | {'PN shift':>12} | {'CTL shift':>12} | "
               f"{'PN/VL':>8} | {'PN-VL%':>8}")
    print(header2)
    print("-" * len(header2))

    s_results = []
    for s in strengths:
        field_s2, _ = make_field(lat, 3, s)
        mf = np.max(field_s2)
        max_phase = compute_max_phase(lat, field_s2, k_fixed, "valley_linear")

        shifts = {}
        for mode in modes:
            shifts[mode] = measure_gravity(lat, field_s2, k_fixed, blocked, det, zf_k1, mode)

        vl = shifts["valley_linear"]
        pn = shifts["post_newtonian"]
        ctl = shifts["control_plus"]

        ratio_pn = pn / vl if abs(vl) > 1e-12 else float("nan")
        pct_diff = 100 * (pn - vl) / abs(vl) if abs(vl) > 1e-12 else float("nan")

        row = (f"{s:>10.0e} | {mf:>8.5f} | {max_phase:>10.4f} | "
               f"{vl:>+12.8f} | {pn:>+12.8f} | {ctl:>+12.8f} | "
               f"{ratio_pn:>8.4f} | {pct_diff:>+8.2f}%")
        print(row)

        s_results.append({
            "s": s, "max_f": mf, "max_phase": max_phase,
            "vl": vl, "pn": pn, "ctl": ctl,
            "ratio": ratio_pn, "pct": pct_diff,
        })

    print()

    # ================================================================
    # ANALYSIS
    # ================================================================
    print("=" * 78)
    print("ANALYSIS")
    print("=" * 78)
    print()

    # Experiment 1 analysis
    print("--- Experiment 1: k-dependence at s=5e-2 ---")
    print()

    sign_flip_k = None
    for r in k_results:
        sign_str = "ENHANCES" if r["pct"] > 0 else "SUPPRESSES"
        print(f"  k={r['k']:>5.1f}: max_phase={r['max_phase']:.3f} "
              f"({r['regime']:<12s})  PN {sign_str} by {abs(r['pct']):.2f}%")
        if sign_flip_k is None and r["pct"] < 0:
            sign_flip_k = r["k"]

    print()
    # Check the prediction
    perturbative_results = [r for r in k_results if r["regime"] == "perturbative"]
    wrapping_results = [r for r in k_results if r["regime"] == "WRAPPING"]

    pn_enhances_in_perturbative = all(r["pct"] > 0 for r in perturbative_results) if perturbative_results else False
    pn_suppresses_in_wrapping = any(r["pct"] < 0 for r in wrapping_results) if wrapping_results else False

    print("--- Experiment 2: s-dependence at k=1.0 ---")
    print()
    for r in s_results:
        if abs(r["vl"]) > 1e-12:
            sign_str = "ENHANCES" if r["pct"] > 0 else "SUPPRESSES"
            print(f"  s={r['s']:.0e}: max_f={r['max_f']:.5f}  "
                  f"PN {sign_str} by {abs(r['pct']):.2f}%  "
                  f"(max_phase={r['max_phase']:.4f})")
        else:
            print(f"  s={r['s']:.0e}: VL shift ~ 0 (below noise)")

    # ================================================================
    # VERDICT
    # ================================================================
    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    print()

    if pn_enhances_in_perturbative and pn_suppresses_in_wrapping:
        print("  HYPOTHESIS CONFIRMED: Phase wrapping explains the sign reversal.")
        print()
        print("  In the perturbative regime (max_phase < pi):")
        for r in perturbative_results:
            print(f"    k={r['k']:.1f}: PN enhances gravity by {r['pct']:+.2f}%")
        print()
        print("  In the wrapping regime (max_phase > pi):")
        for r in wrapping_results:
            print(f"    k={r['k']:.1f}: PN {'suppresses' if r['pct']<0 else 'enhances'} "
                  f"gravity by {r['pct']:+.2f}%")
        print()
        print("  The f^2 correction has the PREDICTED sign (-f^2/2 enhances gravity)")
        print("  when the lattice operates in the perturbative regime.")
    elif pn_enhances_in_perturbative:
        print("  HYPOTHESIS PARTIALLY CONFIRMED: PN enhances in perturbative regime,")
        print("  but no clear wrapping regime observed.")
        for r in k_results:
            print(f"    k={r['k']:.1f}: PN-VL = {r['pct']:+.2f}% "
                  f"(max_phase={r['max_phase']:.3f})")
    else:
        # Check if ALL suppress
        all_suppress = all(r["pct"] < 0 for r in k_results if abs(r["vl"]) > 1e-12)
        all_enhance = all(r["pct"] > 0 for r in k_results if abs(r["vl"]) > 1e-12)

        if all_suppress:
            print("  HYPOTHESIS FALSIFIED: PN suppresses gravity at ALL k values,")
            print("  including the perturbative regime (max_phase << pi).")
            print()
            print("  The sign reversal is NOT phase wrapping -- it is fundamental.")
            print("  The -f^2/2 term reduces the action deficit near the mass,")
            print("  which REDUCES (not enhances) the phase gradient that drives")
            print("  gravitational deflection.")
            print()
            print("  This means: PN action makes the field LESS curved, not more.")
        elif all_enhance:
            print("  HYPOTHESIS CONFIRMED (strongly): PN enhances gravity at ALL k.")
            print("  The original k=5 result may have been a numerical artifact.")
            for r in k_results:
                print(f"    k={r['k']:.1f}: PN-VL = {r['pct']:+.2f}%")
        else:
            print("  MIXED RESULTS: sign depends on k but not cleanly on regime.")
            print()
            for r in k_results:
                print(f"    k={r['k']:.1f}: PN-VL = {r['pct']:+.2f}% "
                      f"(max_phase={r['max_phase']:.3f}, {r['regime']})")
            print()
            print("  The relationship between phase magnitude and sign is more")
            print("  complex than simple perturbative vs wrapping classification.")

    elapsed = time.time() - t0
    print()
    print(f"Total runtime: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
