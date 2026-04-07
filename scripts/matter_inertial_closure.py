#!/usr/bin/env python3
"""Matter / inertial closure on the grown-DAG propagator.

The classifier program is closed (Update 3). The remaining gap on the
harshest-critique row is "fields but no matter" — the program has wave
equations, retardation, and radiation, but no persistent localized
objects with inertial response.

This lane attempts the closure directly. The program is:

  1. DEFINE persistent objects as Gaussian amplitude packets at the
     source layer with variable width sigma.
  2. MEASURE persistence: propagate a packet under no field across
     NL layers, measure how much its identity (centroid, width) is
     preserved. A packet is persistent if its detector width is
     bounded and comparable to its initial width.
  3. DEFINE a uniform force as a linear field f(y, z) = -g * z.
     Under the phase factor exp(i k L (1 - f)), this gives a constant
     phase gradient in z, which is the model analogue of a uniform
     force in the +z direction.
  4. MEASURE Newton's second law: for fixed packet, plot
     delta_z = cz(g) - cz(0) vs g. Should be linear; slope = 1/m
     (model inertial mass up to propagator normalization).
  5. TEST equivalence principle: is the slope the same across packets
     with different initial widths? If yes, all persistent objects
     fall at the same rate under the uniform force — the equivalence
     principle holds at the persistent-object level.
  6. FAMILY PORTABILITY: repeat on Fam1, Fam2, Fam3.
  7. NULL: g = 0 must give zero deflection (sanity).

PASS criteria for "matter/inertial closure":
  - Persistence: detector width bounded (< 4 * initial width)
  - Newton: delta_z(g) linear in g with R² > 0.99
  - Equivalence: slopes of different packets agree within 10%
  - Family portability: same result on all three families
  - Null: |delta_z(g=0)| < 1e-6
"""

from __future__ import annotations

import math
import random

BETA = 0.8
K_PHASE = 5.0
H = 0.5
NL = 30
PW = 6
MAX_D_PHYS = 3
FAMILIES = [("Fam1", 0.20, 0.70), ("Fam2", 0.05, 0.30), ("Fam3", 0.50, 0.90)]


def grow(seed, drift, restore):
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(MAX_D_PHYS / H))
    pos = []
    adj = {}
    nmap = {}
    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    for layer in range(1, NL):
        x = layer * H
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                if layer == 1:
                    y, z = iy * H, iz * H
                else:
                    prev = nmap.get((layer - 1, iy, iz))
                    if prev is None:
                        continue
                    _, py, pz = pos[prev]
                    y = py + rng.gauss(0, drift * H)
                    z = pz + rng.gauss(0, drift * H)
                    y = y * (1 - restore) + (iy * H) * restore
                    z = z * (1 - restore) + (iz * H) * restore
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer - 1, iy, iz))
                if si is None:
                    continue
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            adj.setdefault(si, []).append(di)
    return pos, adj, nmap


def gaussian_packet_sources(nmap, sigma):
    """Gaussian amplitude distribution on layer 1, centered at (0,0)."""
    hw = int(PW / H)
    sources = []
    total_w = 0.0
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            r2 = (iy * H) ** 2 + (iz * H) ** 2
            amp = math.exp(-r2 / (2.0 * sigma ** 2))
            idx = nmap.get((1, iy, iz))
            if idx is not None and amp > 1e-6:
                sources.append((idx, complex(amp)))
                total_w += amp ** 2
    norm = 1.0 / math.sqrt(total_w) if total_w > 0 else 1.0
    return [(i, a * norm) for i, a in sources]


def uniform_force_field(pos, g):
    """f(y, z) = -g * z — constant force in +z direction."""
    return [-g * p[2] for p in pos]


def prop_beam(pos, adj, nmap, field, k, sources):
    n = len(pos)
    amps = [0j] * n
    for idx, amp in sources:
        amps[idx] = amp
    order = sorted(range(n), key=lambda i: pos[i][0])
    h2 = H * H
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            f = 0.0
            if field is not None:
                f = 0.5 * (field[i] + field[j])
            phase = k * L * (1.0 - f)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * w * h2 / (L * L)
    return amps


def detector_stats(amps, pos, NL, PW):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds = n - npl
    weights = [abs(amps[i]) ** 2 for i in range(ds, n)]
    zs = [pos[i][2] for i in range(ds, n)]
    total = sum(weights)
    if total <= 0:
        return 0.0, 0.0, 0.0
    cz = sum(w * z for w, z in zip(weights, zs)) / total
    var = sum(w * (z - cz) ** 2 for w, z in zip(weights, zs)) / total
    return total, cz, math.sqrt(var)


def linear_fit(xs, ys):
    """Linear fit y = a*x + b; returns (a, b, r2)."""
    n = len(xs)
    if n < 2:
        return 0.0, 0.0, 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 0:
        return 0.0, my, 0.0
    a = sxy / sxx
    b = my - a * mx
    r2 = (sxy * sxy) / (sxx * syy) if syy > 0 else 1.0
    return a, b, r2


def main():
    print("=" * 100)
    print("MATTER / INERTIAL CLOSURE HARNESS")
    print(f"NL={NL}, PW={PW}, K={K_PHASE}")
    print("Persistent objects = Gaussian packets of width sigma")
    print("Force = uniform linear field f(y,z) = -g*z")
    print("=" * 100)

    packets = [("narrow", 0.5), ("medium", 1.0), ("wide", 1.5)]
    g_values = [0.0, 0.001, 0.002, 0.004, 0.008]

    # === 1. Persistence: how much does a free packet spread? ===
    print("\n1. PERSISTENCE (free propagation, no force)")
    print(f"  {'family':>6s} {'packet':>8s} {'sigma_0':>8s} {'sigma_det':>10s} {'ratio':>8s}")
    persist_ok_all = True
    pos_F1, adj_F1, nmap_F1 = grow(0, 0.20, 0.70)
    for p_name, sigma in packets:
        srcs = gaussian_packet_sources(nmap_F1, sigma)
        amps = prop_beam(pos_F1, adj_F1, nmap_F1, None, K_PHASE, srcs)
        p_tot, cz, sig_det = detector_stats(amps, pos_F1, NL, PW)
        ratio = sig_det / max(sigma, 1e-6)
        persist_ok = ratio < 4.0
        if not persist_ok:
            persist_ok_all = False
        print(f"  {'Fam1':>6s} {p_name:>8s} {sigma:8.3f} {sig_det:10.3f} {ratio:8.2f}")
    print(f"  persistence verdict: {'OK' if persist_ok_all else 'PACKETS SPREAD TOO MUCH'}")

    # === 2. Newton's F: delta_z vs g for each packet ===
    print("\n2. NEWTON'S LAW (delta_z vs g, fixed packet)")
    results_F1 = {}
    for p_name, sigma in packets:
        print(f"\n  {p_name} (sigma={sigma}):")
        srcs = gaussian_packet_sources(nmap_F1, sigma)
        # baseline (g=0) cz
        amps0 = prop_beam(pos_F1, adj_F1, nmap_F1, None, K_PHASE, srcs)
        _, cz_0, _ = detector_stats(amps0, pos_F1, NL, PW)
        print(f"    baseline cz at g=0: {cz_0:+.6f}")
        deltas = []
        for g in g_values:
            field = uniform_force_field(pos_F1, g)
            amps = prop_beam(pos_F1, adj_F1, nmap_F1, field, K_PHASE, srcs)
            _, cz_g, _ = detector_stats(amps, pos_F1, NL, PW)
            delta = cz_g - cz_0
            deltas.append(delta)
            print(f"    g={g:.4f}  cz={cz_g:+.6f}  delta_z={delta:+.6f}")
        slope, intercept, r2 = linear_fit(g_values, deltas)
        results_F1[p_name] = {
            "sigma": sigma,
            "deltas": deltas,
            "slope": slope,
            "intercept": intercept,
            "r2": r2,
        }
        print(f"    linear fit: delta_z = {slope:.4f} * g + {intercept:+.6f}  (R²={r2:.4f})")

    # === 3. Equivalence principle: do slopes agree? ===
    print("\n3. EQUIVALENCE PRINCIPLE (slope across packets)")
    slopes = [results_F1[p_name]["slope"] for p_name, _ in packets]
    print(f"  slopes: {[f'{s:.3f}' for s in slopes]}")
    if slopes:
        mean_slope = sum(slopes) / len(slopes)
        max_dev = max(abs(s - mean_slope) for s in slopes)
        rel_dev = max_dev / max(abs(mean_slope), 1e-12)
        ep_ok = rel_dev < 0.10
        print(f"  mean slope: {mean_slope:.4f}")
        print(f"  max relative deviation: {rel_dev:.2%}")
        print(f"  equivalence principle: {'OK (<10%)' if ep_ok else 'VIOLATED'}")

    # === 4. Null: g=0 gives zero deflection ===
    print("\n4. NULL (g=0 must give delta_z = 0)")
    for p_name, sigma in packets:
        delta0 = results_F1[p_name]["deltas"][0]
        null_ok = abs(delta0) < 1e-6
        print(f"  {p_name}: delta_z(g=0) = {delta0:+.2e}  "
              f"{'OK' if null_ok else 'FAIL'}")

    # === 5. Family portability ===
    print("\n5. FAMILY PORTABILITY (medium packet, across Fam1/2/3)")
    fam_slopes = []
    for fam_name, drift, restore in FAMILIES:
        pos_f, adj_f, nmap_f = grow(0, drift, restore)
        srcs = gaussian_packet_sources(nmap_f, 1.0)
        amps0 = prop_beam(pos_f, adj_f, nmap_f, None, K_PHASE, srcs)
        _, cz_0, _ = detector_stats(amps0, pos_f, NL, PW)
        deltas_f = []
        for g in g_values:
            field = uniform_force_field(pos_f, g)
            amps = prop_beam(pos_f, adj_f, nmap_f, field, K_PHASE, srcs)
            _, cz_g, _ = detector_stats(amps, pos_f, NL, PW)
            deltas_f.append(cz_g - cz_0)
        slope_f, _, r2_f = linear_fit(g_values, deltas_f)
        fam_slopes.append(slope_f)
        print(f"  {fam_name}: slope={slope_f:.4f}  R²={r2_f:.4f}  "
              f"deltas={[f'{d:+.4f}' for d in deltas_f]}")

    mean_fam = sum(fam_slopes) / len(fam_slopes)
    max_fam = max(abs(s - mean_fam) for s in fam_slopes)
    fam_rel = max_fam / max(abs(mean_fam), 1e-12)
    fam_port_ok = fam_rel < 0.10
    print(f"  family slope rel dev: {fam_rel:.2%}")
    print(f"  family portability: {'OK' if fam_port_ok else 'VARIES'}")

    # === 6. Summary verdict ===
    print("\n" + "=" * 100)
    print("SUMMARY VERDICT")
    print("=" * 100)
    r2s = [results_F1[p]["r2"] for p, _ in packets]
    newton_ok = all(r2 > 0.99 for r2 in r2s)
    mean_slope_F1 = sum(slopes) / len(slopes)
    ep_ok = (max(abs(s - mean_slope_F1) for s in slopes) /
             max(abs(mean_slope_F1), 1e-12)) < 0.10
    null_ok = all(abs(results_F1[p]["deltas"][0]) < 1e-6 for p, _ in packets)

    print(f"  persistence        : {'OK' if persist_ok_all else 'FAIL'}")
    print(f"  Newton linear (R²) : {'OK' if newton_ok else 'FAIL'}  "
          f"(min R² = {min(r2s):.4f})")
    print(f"  equivalence (slopes within 10%) : {'OK' if ep_ok else 'FAIL'}  "
          f"(rel dev = {max(abs(s - mean_slope_F1) for s in slopes) / abs(mean_slope_F1):.2%})")
    print(f"  null (g=0 delta)   : {'OK' if null_ok else 'FAIL'}")
    print(f"  family portability : {'OK' if fam_port_ok else 'FAIL'}  "
          f"(rel dev = {fam_rel:.2%})")

    all_ok = persist_ok_all and newton_ok and ep_ok and null_ok and fam_port_ok
    if all_ok:
        print("\n  MATTER / INERTIAL CLOSURE: PASS")
        print("  persistent objects exhibit Newton's law, equivalence principle,")
        print("  exact null, and family portability on grown-DAG.")
    else:
        print("\n  MATTER / INERTIAL CLOSURE: PARTIAL / FAIL")
        print("  see failing criteria above.")


if __name__ == "__main__":
    main()
