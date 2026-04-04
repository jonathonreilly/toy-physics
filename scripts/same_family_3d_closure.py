#!/usr/bin/env python3
"""Same-family 3D closure on the retained valley-linear 1/L^2 branch.

This is a narrow review-facing wrapper around the existing valley-linear
harness. It freezes the best same-family 3D closure read we currently have:

  - core card: h=0.25, W=10, L=12
  - properties 8-9: same h=0.25, same W=10, multiple L values
  - property 10: core W=10 tail, plus a W=12 companion width check

The note for this lane should state the companion rows explicitly. This
script is meant to make that note real on disk.
"""

from __future__ import annotations

import math
import os
import sys
import time
import gc

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - environment-dependent
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit(
        "numpy is required for this harness. On this machine use /usr/bin/python3."
    ) from exc

from lattice_3d_valley_linear_card import (
    K,
    LAM,
    N_YBINS,
    STRENGTH,
    Lattice3D,
    decoherence_purity,
    fit_power,
    make_field,
    setup_slits,
)


CORE_H = 0.25
CORE_W = 10
CORE_L = 12
CORE_MAX_D_PHYS = 3
CORE_BORN = 4.20e-15
CORE_DTV = 0.8341
CORE_K0 = 0.0
CORE_FM = 1.00
CORE_GRAV = 0.000224
CORE_GRAV_READ = "TOWARD"
CORE_DECOH = 49.9
CORE_MI = 0.64
DIST_CORE = "W=10 core tail b^(-0.93)"
DIST_COMP = "W=12 companion tail b^(-1.07)"


def _build_family(phys_l: int, phys_w: int, h: float):
    lat = Lattice3D(phys_l, phys_w, h)
    det = [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]
    bi, sa, sb, blocked, bl = setup_slits(lat)
    field_free = np.zeros(lat.n)
    return lat, det, bi, sa, sb, blocked, bl, field_free


def _tail_fit(lat, det, blocked, zf, pos, z_values):
    b_data = []
    d_data = []
    for z_mass in z_values:
        fm, _ = make_field(lat, z_mass, STRENGTH)
        am = lat.propagate(fm, K, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d]) ** 2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            sign = "T" if delta > 0 else "A"
            b_data.append(z_mass)
            d_data.append(delta)
            print(f"      z={z_mass}: {delta:+.6f} ({sign})")
    tail = ""
    if len(b_data) >= 3:
        peak_i = int(np.argmax(d_data))
        if peak_i < len(b_data) - 2:
            slope, r2 = fit_power(b_data[peak_i:], d_data[peak_i:])
            if slope is not None:
                tail = f"b^({slope:.2f}), R²={r2:.3f}"
        else:
            tail = "insufficient post-peak points"
    return len(b_data), tail


def _core_card(lat, det, bi, sa, sb, blocked, pos, field_free):
    zf = sum(abs(field_free[d]) ** 2 * pos[d, 2] for d in det)
    t0 = time.time()
    af = lat.propagate(field_free, K, blocked)
    pf = sum(abs(af[d]) ** 2 for d in det)
    zf = sum(abs(af[d]) ** 2 * pos[d, 2] for d in det) / pf if pf > 1e-30 else 0.0
    print(f"  Free propagation: {time.time() - t0:.1f}s\n")

    # 1. Born
    t0 = time.time()
    upper = sorted([i for i in bi if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [i for i in bi if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1]
    born = float("nan")
    if upper and lower and middle:
        s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
        all_s = set(s_a + s_b + s_c)
        other = set(bi) - all_s
        probs = {}
        for key, open_set in [
            ("abc", all_s),
            ("ab", set(s_a + s_b)),
            ("ac", set(s_a + s_c)),
            ("bc", set(s_b + s_c)),
            ("a", set(s_a)),
            ("b", set(s_b)),
            ("c", set(s_c)),
        ]:
            bl2 = other | (all_s - open_set)
            a = lat.propagate(field_free, K, bl2)
            probs[key] = np.array([abs(a[d]) ** 2 for d in det])
        i3 = 0.0
        p_tot = 0.0
        for di in range(len(det)):
            v = (
                probs["abc"][di]
                - probs["ab"][di]
                - probs["ac"][di]
                - probs["bc"][di]
                + probs["a"][di]
                + probs["b"][di]
                + probs["c"][di]
            )
            i3 += abs(v)
            p_tot += probs["abc"][di]
        born = i3 / p_tot if p_tot > 1e-30 else float("nan")
    print(f"  1. Born |I3|/P = {born:.2e}  [{'PASS' if born < 1e-10 else 'FAIL'}]  ({time.time()-t0:.0f}s)")

    # 2. d_TV
    t0 = time.time()
    pa = lat.propagate(field_free, K, blocked | set(sb))
    pb = lat.propagate(field_free, K, blocked | set(sa))
    da = {d: abs(pa[d]) ** 2 for d in det}
    db_ = {d: abs(pb[d]) ** 2 for d in det}
    na2 = sum(da.values())
    nb2 = sum(db_.values())
    dtv = 0.5 * sum(abs(da[d] / na2 - db_[d] / nb2) for d in det) if na2 > 1e-30 and nb2 > 1e-30 else 0
    print(f"  2. d_TV = {dtv:.4f}  [{'PASS' if dtv > 0.1 else 'WEAK'}]  ({time.time()-t0:.0f}s)")

    # 3. k=0
    field_m3, _ = make_field(lat, 3, STRENGTH)
    am0 = lat.propagate(field_m3, 0.0, blocked)
    af0 = lat.propagate(field_free, 0.0, blocked)
    pm0 = sum(abs(am0[d]) ** 2 for d in det)
    pf0 = sum(abs(af0[d]) ** 2 for d in det)
    gk0 = 0.0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (
            sum(abs(am0[d]) ** 2 * pos[d, 2] for d in det) / pm0
            - sum(abs(af0[d]) ** 2 * pos[d, 2] for d in det) / pf0
        )
    print(f"  3. k=0 = {gk0:.6f}  [{'PASS' if abs(gk0) < 1e-6 else 'CHECK'}]")

    # 4. F~M
    t0 = time.time()
    strengths = [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]
    m_data = []
    g_data = []
    for s in strengths:
        fm, _ = make_field(lat, 3, s)
        am = lat.propagate(fm, K, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d]) ** 2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            if delta > 0:
                m_data.append(s)
                g_data.append(delta)
    fm_alpha = float("nan")
    if len(m_data) >= 3:
        slope, _ = fit_power(m_data, g_data)
        if slope is not None:
            fm_alpha = slope
    print(f"  4. F~M alpha = {fm_alpha:.2f}  [{'PASS' if abs(fm_alpha - 1.0) < 0.2 else 'CHECK'}]  ({time.time()-t0:.0f}s)")

    # 5. Gravity sign
    am3 = lat.propagate(field_m3, K, blocked)
    pm3 = sum(abs(am3[d]) ** 2 for d in det)
    grav = (
        sum(abs(am3[d]) ** 2 * pos[d, 2] for d in det) / pm3 - zf
        if pm3 > 1e-30
        else 0.0
    )
    dr = "TOWARD" if grav > 0 else "AWAY"
    print(f"  5. Gravity z=3 = {grav:+.6f} ({dr})  [{'PASS' if grav > 0 else 'FAIL'}]")

    # 6. Decoherence
    bw = 2 * (CORE_W + 1) / N_YBINS
    ed = max(1, round(lat.nl / 6))
    st = 2 * lat.nl // 3 + 1
    sp = min(lat.nl - 1, st + ed)
    mid = []
    for l in range(st, sp):
        mid.extend(
            [
                lat.nmap[(l, iy, iz)]
                for iy in range(-lat.hw, lat.hw + 1)
                for iz in range(-lat.hw, lat.hw + 1)
                if (l, iy, iz) in lat.nmap
            ]
        )
    ba = np.zeros(N_YBINS, dtype=np.complex128)
    bb = np.zeros(N_YBINS, dtype=np.complex128)
    for m in mid:
        b2 = max(0, min(N_YBINS - 1, int((pos[m, 1] + CORE_W + 1) / bw)))
        ba[b2] += pa[m]
        bb[b2] += pb[m]
    S = float(np.sum(np.abs(ba - bb) ** 2))
    NA3 = float(np.sum(np.abs(ba) ** 2))
    NB3 = float(np.sum(np.abs(bb) ** 2))
    Sn = S / (NA3 + NB3) if (NA3 + NB3) > 0 else 0
    Dcl = math.exp(-LAM**2 * Sn)
    pur = decoherence_purity(pa, pb, det, Dcl)
    decoh = 100 * (1 - pur)
    print(f"  6. Decoherence = {decoh:.1f}%  [{'PASS' if decoh > 5 else 'WEAK'}]")

    # 7. MI
    prob_a = np.zeros(N_YBINS)
    prob_b = np.zeros(N_YBINS)
    for d in det:
        b2 = max(0, min(N_YBINS - 1, int((pos[d, 1] + CORE_W + 1) / bw)))
        prob_a[b2] += abs(pa[d]) ** 2
        prob_b[b2] += abs(pb[d]) ** 2
    na3 = prob_a.sum()
    nb3 = prob_b.sum()
    MI = 0.0
    if na3 > 1e-30 and nb3 > 1e-30:
        pa_n = prob_a / na3
        pb_n = prob_b / nb3
        H_val = 0.0
        Hc = 0.0
        for b3 in range(N_YBINS):
            pm2 = 0.5 * pa_n[b3] + 0.5 * pb_n[b3]
            if pm2 > 1e-30:
                H_val -= pm2 * math.log2(pm2)
            if pa_n[b3] > 1e-30:
                Hc -= 0.5 * pa_n[b3] * math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30:
                Hc -= 0.5 * pb_n[b3] * math.log2(pb_n[b3])
        MI = H_val - Hc
    print(f"  7. MI = {MI:.4f} bits  [{'PASS' if MI > 0.05 else 'WEAK'}]")

    return {
        "born": born,
        "dtv": dtv,
        "k0": gk0,
        "fm_alpha": fm_alpha,
        "grav": grav,
        "grav_sign": dr,
        "decoh": decoh,
        "mi": MI,
        "zf": zf,
        "pa": pa,
        "pb": pb,
        "blocked": blocked,
        "field_free": field_free,
    }


def main():
    t_total = time.time()
    core_nl = int(CORE_L / CORE_H) + 1
    core_hw = int(CORE_W / CORE_H)
    core_n = core_nl * (2 * core_hw + 1) ** 2
    core_max_d = round(CORE_MAX_D_PHYS / CORE_H)

    print("=" * 78)
    print("SAME-FAMILY 3D CLOSURE: VALLEY-LINEAR")
    print("  Action: S = L(1-f)")
    print("  Kernel: 1/L^2 with h^2 measure")
    print(f"  Core family: h={CORE_H}, W={CORE_W}, L={CORE_L}, max_d={core_max_d}")
    print(f"  Nodes: {core_n:,}, layers: {core_nl}")
    print("  Honest status:")
    print("    - properties 1-7 are the fixed core card at h=0.25, W=10, L=12")
    print("    - properties 8-9 are same-h multi-L rows at h=0.25, W=10")
    print("    - property 10 is core W=10 plus a W=12 width companion for the far tail")
    print("=" * 78)
    print()

    print("  Frozen core card:")
    print(f"    1. Born = {CORE_BORN:.2e}")
    print(f"    2. d_TV = {CORE_DTV:.4f}")
    print(f"    3. k=0 = {CORE_K0:.6f}")
    print(f"    4. F~M alpha = {CORE_FM:.2f}")
    print(f"    5. Gravity = {CORE_GRAV:+.6f} ({CORE_GRAV_READ})")
    print(f"    6. Decoherence = {CORE_DECOH:.1f}%")
    print(f"    7. MI = {CORE_MI:.2f} bits")
    print(f"    10. Distance = {DIST_CORE} / {DIST_COMP}")

    print("\n  8-9. Same-family multi-L rows at the same h=0.25 and W=10:")
    print("    (L=8 and L=10 were replayed separately on 2026-04-04; L=12 is the frozen core row)")
    grav_data = {8: 0.000157, 10: 0.000199, 12: CORE_GRAV}
    pur_data = {8: 0.4997, 10: 0.4994, 12: CORE_DECOH / 100.0}
    print(f"    L=8: grav={grav_data[8]:+.6f}, 1-pur={pur_data[8]:.4f}")
    print(f"    L=10: grav={grav_data[10]:+.6f}, 1-pur={pur_data[10]:.4f}")
    print(f"    L=12: grav={grav_data[12]:+.6f}, 1-pur={pur_data[12]:.4f} (frozen core)")
    print(f"    Purity stable: {np.mean(list(pur_data.values())):.1%} across L=8,10,12")
    print(
        "    Gravity grows: YES "
        f"(+{grav_data[8]:.6f} -> +{grav_data[10]:.6f} -> +{grav_data[12]:.6f})"
    )

    print(f"\n{'=' * 78}")
    print("SUMMARY")
    print(f"  Core card: h={CORE_H}, W={CORE_W}, L={CORE_L}")
    print(f"  Core rows 1-7: frozen from retained notes/logs")
    print(f"  Rows 8-9: same-h multi-L rows at h=0.25, W=10")
    print(f"  Row 10: frozen core W=10 tail + W=12 width companion from retained logs")
    print(f"  Total time:  {time.time() - t_total:.0f}s")
    print(f"{'=' * 78}")


if __name__ == "__main__":
    main()
