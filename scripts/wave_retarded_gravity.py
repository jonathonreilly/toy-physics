#!/usr/bin/env python3
"""Retarded gravity from a moving source on the wave-equation field.

Drive a source that translates in z with constant velocity v through
the discrete wave equation (x = time, c = 1 cell/dt). Propagate the
beam through the resulting time-dependent field and measure detector
deflection.

Decisive test:
  Compare moving-source deflection against three frozen references:
    A. frozen at z_start (initial position)
    B. frozen at z_end (final position)
    C. frozen at z_mid (instantaneous-average position)
  Newton: deflection should match B (the "current" position when the
          beam crosses).
  Retarded (finite c): deflection should be closer to A or to a
          retarded-time average, NOT to B.

Tests:
  1. Static reference: v=0 should reproduce wave_equation_self_field static
  2. Moving source (v>0) deflection vs frozen-A / frozen-B / frozen-C
  3. f-symmetry: +v vs -v
  4. F~M holds on moving-source field
  5. Born preserved on moving-source field
  6. Null at s=0 with moving source
  7. Family portability
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
K = 5.0
MAX_D_PHYS = 3
H = 0.5
NL = 30
PW = 8
S = 0.004
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


def _laplacian_yz(f, nw):
    lap = [[0.0] * nw for _ in range(nw)]
    for iy in range(1, nw - 1):
        for iz in range(1, nw - 1):
            lap[iy][iz] = f[iy - 1][iz] + f[iy + 1][iz] + f[iy][iz - 1] + f[iy][iz + 1] - 4.0 * f[iy][iz]
    return lap


def _solve_wave_moving(strength, src_layer_start, iz_of_t):
    """Wave evolution with source at (iy=0, iz=iz_of_t(t)) for t >= src_layer_start.

    iz_of_t: function from layer index -> integer iz offset (relative to grid center)
    Source is on for all layers t >= src_layer_start.
    """
    hw = int(PW / H)
    nw = 2 * hw + 1
    f_prev = [[0.0] * nw for _ in range(nw)]
    f_curr = [[0.0] * nw for _ in range(nw)]
    history = [
        [[0.0] * nw for _ in range(nw)],
        [[0.0] * nw for _ in range(nw)],
    ]
    h2 = H * H
    for t in range(2, NL):
        active = t >= src_layer_start
        iz_now = iz_of_t(t)
        sy = 0 + nw // 2
        sz = iz_now + nw // 2
        lap = _laplacian_yz(f_curr, nw)
        f_next = [[0.0] * nw for _ in range(nw)]
        for iy in range(nw):
            for iz in range(nw):
                src = strength if (active and iy == sy and iz == sz) else 0.0
                f_next[iy][iz] = 2.0 * f_curr[iy][iz] - f_prev[iy][iz] + h2 * (lap[iy][iz] + src)
        f_prev = f_curr
        f_curr = f_next
        history.append([row[:] for row in f_curr])
    return history


def _field_at(history, layer, iy, iz):
    hw = int(PW / H)
    nw = 2 * hw + 1
    sy = iy + nw // 2
    sz = iz + nw // 2
    if 0 <= layer < NL and 0 <= sy < nw and 0 <= sz < nw:
        return history[layer][sy][sz]
    return 0.0


def _prop_beam(pos, adj, nmap, history, k, sources=None):
    n = len(pos)
    hw = int(PW / H)
    nw = 2 * hw + 1
    field = [0.0] * n
    if history is not None:
        for layer in range(NL):
            for iy in range(-hw, hw + 1):
                for iz in range(-hw, hw + 1):
                    idx = nmap.get((layer, iy, iz))
                    if idx is not None:
                        field[idx] = _field_at(history, layer, iy, iz)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    if sources is None:
        amps[0] = 1.0
    else:
        for idx, amp in sources:
            amps[idx] = amp
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
            lf = 0.5 * (field[i] + field[j])
            phase = k * L * (1.0 - lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * w * h2 / (L * L)
    return amps


def _cz(amps, pos):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds = len(pos) - npl
    n = len(pos)
    t = sum(abs(amps[i]) ** 2 for i in range(ds, n))
    if t <= 0:
        return 0.0
    return sum(abs(amps[i]) ** 2 * pos[i][2] for i in range(ds, n)) / t


def _dp(amps, pos):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds = len(pos) - npl
    return sum(abs(amps[i]) ** 2 for i in range(ds, len(pos)))


def _make_field(s, iz_of_t):
    return _solve_wave_moving(s, NL // 3, iz_of_t)


def _frozen(iz_const):
    return lambda t: iz_const


def _moving(iz_start, v_cells_per_layer):
    src_layer_start = NL // 3
    return lambda t: iz_start + int(round(v_cells_per_layer * (t - src_layer_start)))


def _make_instantaneous(s, iz_of_t):
    """Build a stitched 'instantaneous' field history.

    At each layer t, the field everywhere on that layer is set to the
    LATE-TIME stationary slice of a static solve with the source frozen
    at iz_of_t(t). This is the comparator that says: what if the field
    everywhere always tracked the CURRENT source position with no
    propagation delay? It is the c=infinity limit of the wave equation.
    """
    hw = int(PW / H)
    nw = 2 * hw + 1
    src_layer_start = NL // 3
    cache = {}
    history = [[[0.0] * nw for _ in range(nw)] for _ in range(NL)]
    for t in range(NL):
        if t < src_layer_start:
            continue
        iz_now = iz_of_t(t)
        if iz_now not in cache:
            full = _solve_wave_moving(s, src_layer_start, _frozen(iz_now))
            cache[iz_now] = [row[:] for row in full[NL - 1]]
        history[t] = [row[:] for row in cache[iz_now]]
    return history


def main():
    print("=" * 70)
    print("WAVE RETARDED GRAVITY HARNESS")
    print(f"NL={NL}, W={PW}, s={S}")
    print("=" * 70)

    iz_start = 6   # corresponds to z=3.0
    iz_end = 0     # source moves down to z=0 over the run
    src_layer_start = NL // 3
    n_active = NL - src_layer_start
    v = (iz_end - iz_start) / n_active   # cells per layer (~ -0.3)
    iz_mid = (iz_start + iz_end) // 2

    print(f"\nSource motion: iz from {iz_start} to {iz_end} over {n_active} layers")
    print(f"v = {v:.4f} cells/layer (|v|/c = {abs(v):.4f})")

    # 1. Static reference (v=0): match the wave equation static result
    print("\n1. STATIC REFERENCE (v=0, frozen at iz_start)")
    h_static = _make_field(S, _frozen(iz_start))
    pos, adj, nmap = grow(0, 0.2, 0.7)
    free = _prop_beam(pos, adj, nmap, None, K)
    z_free = _cz(free, pos)
    g_static = _prop_beam(pos, adj, nmap, h_static, K)
    delta_static = _cz(g_static, pos) - z_free
    print(f"  delta_z (static, iz=iz_start={iz_start}) = {delta_static:+.6f}")

    # 2. Decisive comparison: retarded vs PROPER instantaneous comparator
    print("\n2. RETARDED vs INSTANTANEOUS MOVING-SOURCE (Fam1, seed=0)")
    print("   Frozen references kept as intuition aids; the decisive")
    print("   pairing is M (retarded) vs I (instantaneous, c=infinity).")
    h_A = _make_field(S, _frozen(iz_start))
    h_B = _make_field(S, _frozen(iz_end))
    h_C = _make_field(S, _frozen(iz_mid))
    h_M = _make_field(S, _moving(iz_start, v))
    h_I = _make_instantaneous(S, _moving(iz_start, v))

    cz_A = _cz(_prop_beam(pos, adj, nmap, h_A, K), pos)
    cz_B = _cz(_prop_beam(pos, adj, nmap, h_B, K), pos)
    cz_C = _cz(_prop_beam(pos, adj, nmap, h_C, K), pos)
    cz_M = _cz(_prop_beam(pos, adj, nmap, h_M, K), pos)
    cz_I = _cz(_prop_beam(pos, adj, nmap, h_I, K), pos)
    delta_A = cz_A - z_free
    delta_B = cz_B - z_free
    delta_C = cz_C - z_free
    delta_M = cz_M - z_free
    delta_I = cz_I - z_free

    print(f"  {'reference':>40s} {'delta_z':>12s}")
    print(f"  {'A: frozen at z_start (intuition)':>40s} {delta_A:+12.6f}")
    print(f"  {'B: frozen at z_end (intuition)':>40s} {delta_B:+12.6f}")
    print(f"  {'C: frozen at z_mid (intuition)':>40s} {delta_C:+12.6f}")
    print(f"  {'M: moving source (RETARDED)':>40s} {delta_M:+12.6f}")
    print(f"  {'I: moving source (INSTANTANEOUS)':>40s} {delta_I:+12.6f}")

    diff_MI = delta_M - delta_I
    rel_MI = abs(diff_MI) / max(abs(delta_M), abs(delta_I), 1e-12)
    print(f"\n  decisive: M - I = {diff_MI:+.6f}  (relative {rel_MI:.2%})")
    if rel_MI > 0.05:
        verdict = "RETARDED != INSTANTANEOUS — finite-c effect resolved"
    else:
        verdict = "RETARDED ~= INSTANTANEOUS — finite-c effect unresolved at this v/c"
    print(f"  verdict: {verdict}")

    # 3. v-symmetry: +v vs -v
    print("\n3. v-SYMMETRY (+v vs -v, Fam1)")
    h_plus = _make_field(S, _moving(iz_start, +abs(v)))
    h_minus = _make_field(S, _moving(iz_start, -abs(v)))
    cz_p = _cz(_prop_beam(pos, adj, nmap, h_plus, K), pos)
    cz_m = _cz(_prop_beam(pos, adj, nmap, h_minus, K), pos)
    print(f"  +v: delta_z = {cz_p - z_free:+.6f}")
    print(f"  -v: delta_z = {cz_m - z_free:+.6f}")

    # 4. F~M on moving-source field
    print("\n4. F~M on MOVING-SOURCE FIELD across families")
    strengths = [0.001, 0.002, 0.004, 0.008]
    fls = [_make_field(s, _moving(iz_start, v)) for s in strengths]
    for label, drift, restore in FAMILIES:
        p, a, nm = grow(0, drift, restore)
        free_l = _prop_beam(p, a, nm, None, K)
        z_free_l = _cz(free_l, p)
        deltas = []
        for fl in fls:
            g = _prop_beam(p, a, nm, fl, K)
            deltas.append(abs(_cz(g, p) - z_free_l))
        lx = [math.log(x) for x in strengths]
        ly = [math.log(y) for y in deltas if y > 1e-15]
        if len(ly) >= 3:
            mx = sum(lx[: len(ly)]) / len(ly)
            my = sum(ly) / len(ly)
            sxx = sum((x - mx) ** 2 for x in lx[: len(ly)])
            fm = sum((x - mx) * (y - my) for x, y in zip(lx[: len(ly)], ly)) / sxx
            print(f"  {label}: F~M = {fm:.4f}")

    # 5. Born on moving-source field
    print("\n5. BORN TEST on moving-source field (Fam1)")
    slits = [-1, 0, 1]
    h_born = _make_field(S, _moving(iz_start, v))

    def pb(sl):
        srcs = [(nmap.get((0, s2, 0)) or nmap.get((1, s2, 0)), 1.0 + 0j) for s2 in sl]
        srcs = [(i, a2) for i, a2 in srcs if i is not None]
        return _dp(_prop_beam(pos, adj, nmap, h_born, K, sources=srcs), pos)

    p123 = pb(slits)
    p12 = pb([-1, 0]); p13 = pb([-1, 1]); p23 = pb([0, 1])
    p1 = pb([-1]); p2 = pb([0]); p3 = pb([1])
    i3 = p123 - p12 - p13 - p23 + p1 + p2 + p3
    born = abs(i3) / max(p123, 1e-300)
    print(f"  Born |I3|/P = {born:.2e}")

    # 6. Null at s=0 with moving source
    print("\n6. NULL TEST (s=0, moving source)")
    h_null = _make_field(0.0, _moving(iz_start, v))
    g_null = _prop_beam(pos, adj, nmap, h_null, K)
    print(f"  delta_z = {_cz(g_null, pos) - z_free:+.6e}")

    # 7. Family portability — M vs I across families
    print("\n7. FAMILY PORTABILITY (M vs I across families)")
    print(f"  {'family':>6s} {'dM':>12s} {'dI':>12s} {'M-I':>12s} {'rel':>8s}")
    for label, drift, restore in FAMILIES:
        p, a, nm = grow(0, drift, restore)
        zf = _cz(_prop_beam(p, a, nm, None, K), p)
        dM_l = _cz(_prop_beam(p, a, nm, h_M, K), p) - zf
        dI_l = _cz(_prop_beam(p, a, nm, h_I, K), p) - zf
        rel = abs(dM_l - dI_l) / max(abs(dM_l), abs(dI_l), 1e-12)
        print(f"  {label:>6s} {dM_l:+12.6f} {dI_l:+12.6f} {dM_l-dI_l:+12.6f} {rel:8.2%}")


if __name__ == "__main__":
    main()
