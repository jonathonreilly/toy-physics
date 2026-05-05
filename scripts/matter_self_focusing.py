#!/usr/bin/env python3
"""Matter closure attempt #2: self-focusing via nonlinear self-field.

The previous attempt (matter_inertial_closure.py) failed the equivalence
principle at 123% because Gaussian packets spread differently (narrow
packet 4.68x, wide 1.08x) and the spreading determined the response
to a linear field gradient rather than inertial mass.

The hypothesis for this lane: a **nonlinear self-focusing mechanism**
that stabilizes packet width should restore equivalence. If the packet
maintains its initial width through the propagation, all packets feel
the same field gradient range and should respond with the same slope.

Mechanism: **two-pass propagator with amplitude-density self-field**.

  Pass 1: propagate the packet freely, record |amp[i]|^2 at each node
  Pass 2: propagate with a modified action
            S = L * (1 - f_external - lambda * (|amp1[i]|^2 + |amp1[j]|^2)/2)
          where lambda is the self-focusing strength.

Physical interpretation: the packet's own amplitude density acts as
an attractive field (like Schrödinger-Newton or Gross-Pitaevskii
self-gravity). Where the packet is densest, the effective phase is
smallest, so paths through high-density regions interfere more
constructively, focusing the packet toward its own centroid.

Tests:
  1. Persistence: does lambda > 0 reduce sigma_det spreading?
  2. Equivalence: for the best lambda, do slopes across packets converge?
  3. Null: lambda > 0 with g=0 still gives delta_z = 0
  4. Family portability
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

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
    return [-g * p[2] for p in pos]


def prop_beam(pos, adj, nmap, field, k, sources, self_density=None, lam=0.0):
    """Propagator with optional self-density nonlinear field.

    The effective action per edge is
        S = L * (1 - f_external - lam * (density[i] + density[j]) / 2)
    When lam=0 or self_density=None, reduces to the standard propagator.
    """
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
            f_self = 0.0
            if self_density is not None and lam != 0.0:
                f_self = lam * 0.5 * (self_density[i] + self_density[j])
            phase = k * L * (1.0 - f - f_self)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * w * h2 / (L * L)
    return amps


def two_pass_propagate(pos, adj, nmap, field, k, sources, lam):
    """Run two-pass self-focusing propagation."""
    amps1 = prop_beam(pos, adj, nmap, field, k, sources)
    density = [abs(a) ** 2 for a in amps1]
    amps2 = prop_beam(pos, adj, nmap, field, k, sources, self_density=density, lam=lam)
    return amps2


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
    print("MATTER SELF-FOCUSING HARNESS")
    print(f"NL={NL}, PW={PW}, K={K_PHASE}")
    print("Two-pass propagator: pass1 records density, pass2 uses it as self-field")
    print("Action: S = L * (1 - f_external - lambda * density)")
    print("=" * 100)

    packets = [("narrow", 0.5), ("medium", 1.0), ("wide", 1.5)]
    g_values = [0.0, 0.001, 0.002, 0.004, 0.008]
    lam_values = [0.0, 1.0, 10.0, 100.0, 500.0]

    pos, adj, nmap = grow(0, 0.20, 0.70)

    # === 1. Persistence scan over lambda ===
    print("\n1. PERSISTENCE vs LAMBDA (free propagation)")
    print(f"  {'lambda':>8s} {'packet':>8s} {'sigma_0':>8s} {'sigma_det':>10s} {'ratio':>8s}")
    for lam in lam_values:
        for p_name, sigma in packets:
            srcs = gaussian_packet_sources(nmap, sigma)
            amps = two_pass_propagate(pos, adj, nmap, None, K_PHASE, srcs, lam)
            _, _, sig_det = detector_stats(amps, pos, NL, PW)
            ratio = sig_det / max(sigma, 1e-6)
            print(f"  {lam:8.1f} {p_name:>8s} {sigma:8.3f} {sig_det:10.3f} {ratio:8.2f}")
        print()

    # === 2. Equivalence principle at each lambda ===
    print("\n2. EQUIVALENCE PRINCIPLE at each lambda (slopes across packets)")
    print(f"  {'lambda':>8s} {'narrow slope':>14s} {'medium slope':>14s} {'wide slope':>14s} {'rel dev':>10s}")
    best_lambda = None
    best_rel = float("inf")
    for lam in lam_values:
        slopes = []
        for p_name, sigma in packets:
            srcs = gaussian_packet_sources(nmap, sigma)
            amps0 = two_pass_propagate(pos, adj, nmap, None, K_PHASE, srcs, lam)
            _, cz_0, _ = detector_stats(amps0, pos, NL, PW)
            deltas = []
            for g in g_values:
                field = uniform_force_field(pos, g)
                amps = two_pass_propagate(pos, adj, nmap, field, K_PHASE, srcs, lam)
                _, cz_g, _ = detector_stats(amps, pos, NL, PW)
                deltas.append(cz_g - cz_0)
            slope, _, _ = linear_fit(g_values, deltas)
            slopes.append(slope)
        mean_slope = sum(slopes) / len(slopes)
        max_dev = max(abs(s - mean_slope) for s in slopes)
        rel_dev = max_dev / max(abs(mean_slope), 1e-12)
        print(f"  {lam:8.1f} {slopes[0]:14.3f} {slopes[1]:14.3f} {slopes[2]:14.3f} {rel_dev:10.2%}")
        if rel_dev < best_rel:
            best_rel = rel_dev
            best_lambda = lam

    print(f"\n  best lambda (min equivalence rel dev): {best_lambda} at {best_rel:.2%}")

    # === 3. Null at best lambda ===
    print(f"\n3. NULL TEST at lambda={best_lambda}")
    for p_name, sigma in packets:
        srcs = gaussian_packet_sources(nmap, sigma)
        # baseline WITH self-focusing (lambda > 0 gives nonzero "cz0" which we use as reference)
        amps0 = two_pass_propagate(pos, adj, nmap, None, K_PHASE, srcs, best_lambda)
        _, cz_0, _ = detector_stats(amps0, pos, NL, PW)
        field = uniform_force_field(pos, 0.0)  # zero force
        amps = two_pass_propagate(pos, adj, nmap, field, K_PHASE, srcs, best_lambda)
        _, cz_g, _ = detector_stats(amps, pos, NL, PW)
        delta = cz_g - cz_0
        print(f"  {p_name}: delta_z(g=0) = {delta:+.2e}  "
              f"{'OK' if abs(delta) < 1e-6 else 'FAIL'}")

    # === 4. Family portability at best lambda (medium packet) ===
    print(f"\n4. FAMILY PORTABILITY at lambda={best_lambda} (medium packet)")
    fam_slopes = []
    for fam_name, drift, restore in FAMILIES:
        pos_f, adj_f, nmap_f = grow(0, drift, restore)
        srcs = gaussian_packet_sources(nmap_f, 1.0)
        amps0 = two_pass_propagate(pos_f, adj_f, nmap_f, None, K_PHASE, srcs, best_lambda)
        _, cz_0, _ = detector_stats(amps0, pos_f, NL, PW)
        deltas_f = []
        for g in g_values:
            field = uniform_force_field(pos_f, g)
            amps = two_pass_propagate(pos_f, adj_f, nmap_f, field, K_PHASE, srcs, best_lambda)
            _, cz_g, _ = detector_stats(amps, pos_f, NL, PW)
            deltas_f.append(cz_g - cz_0)
        slope_f, _, r2_f = linear_fit(g_values, deltas_f)
        fam_slopes.append(slope_f)
        print(f"  {fam_name}: slope={slope_f:.4f}  R²={r2_f:.4f}")
    mean_fam = sum(fam_slopes) / len(fam_slopes)
    max_fam = max(abs(s - mean_fam) for s in fam_slopes)
    fam_rel = max_fam / max(abs(mean_fam), 1e-12)
    print(f"  family rel dev: {fam_rel:.2%}")

    # === 5. Summary ===
    print("\n" + "=" * 100)
    print("SUMMARY VERDICT")
    print("=" * 100)
    print(f"  best lambda: {best_lambda}")
    print(f"  equivalence rel dev at best lambda: {best_rel:.2%}")
    ep_ok = best_rel < 0.10
    print(f"  equivalence principle (<10%): {'OK' if ep_ok else 'FAIL'}")
    print(f"  previous attempt (lambda=0) rel dev: look at the lambda=0 row above")
    if ep_ok:
        print("\n  MATTER CLOSURE via self-focusing: PASS")
    elif best_rel < 0.50:
        print("\n  MATTER CLOSURE via self-focusing: PARTIAL IMPROVEMENT")
    else:
        print("\n  MATTER CLOSURE via self-focusing: NEGATIVE — self-focusing does not restore equivalence")


if __name__ == "__main__":
    main()
