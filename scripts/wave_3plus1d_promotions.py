#!/usr/bin/env python3
"""(3+1)D promotions of Lane 5 (lightcone) and Lane 6 (retarded vs instantaneous).

Uses the same 7-point spatial Laplacian as wave_3plus1d_radiation.py:
    (1/c^2) d^2f/dt^2 - (d^2/dx_perp^2 + d^2/dy^2 + d^2/dz^2) f = source
with x as time, c = 1 lattice cell per layer.

Tests:
  A. Lightcone with delta pulse on the (3+1)D operator (mirror of Lane 5)
  B. Moving source: retarded field vs instantaneous (c=infinity) comparator
     beam-side test on a grown DAG (mirror of Lane 6)
  C. Family portability of the M vs I gap across Fam1/Fam2/Fam3
"""

from __future__ import annotations

import math
import random

BETA = 0.8
K = 5.0
H = 0.5
NL = 30
PW_FIELD = 4.5     # half-width of the (3+1)D field cube
PW_BEAM = 6        # half-width of the beam grid (transverse)
S = 0.004
FAMILIES = [("Fam1", 0.20, 0.70), ("Fam2", 0.05, 0.30), ("Fam3", 0.50, 0.90)]

NW = int(2 * math.ceil(PW_FIELD / H) + 1)


def _zero3():
    return [[[0.0] * NW for _ in range(NW)] for _ in range(NW)]


def _laplacian_3d(f):
    lap = _zero3()
    for ix in range(1, NW - 1):
        for iy in range(1, NW - 1):
            for iz in range(1, NW - 1):
                lap[ix][iy][iz] = (
                    f[ix - 1][iy][iz] + f[ix + 1][iy][iz]
                    + f[ix][iy - 1][iz] + f[ix][iy + 1][iz]
                    + f[ix][iy][iz - 1] + f[ix][iy][iz + 1]
                    - 6.0 * f[ix][iy][iz]
                )
    return lap


def _solve_wave_3plus1d(strength_fn, iz_of_t, src_layer):
    """Wave-equation evolution. Source at (x_perp=0, iy=0, iz=iz_of_t(t))."""
    sc = NW // 2
    f_prev = _zero3()
    f_curr = _zero3()
    history = [_zero3(), _zero3()]
    h2 = H * H
    for t in range(2, NL):
        if t >= src_layer:
            drive = strength_fn(t)
            iz_now = iz_of_t(t)
            sx = sc
            sy = sc
            sz = sc + iz_now
        else:
            drive = 0.0
            sx = sy = sz = -1
        lap = _laplacian_3d(f_curr)
        f_next = _zero3()
        for ix in range(NW):
            for iy in range(NW):
                for iz in range(NW):
                    src = drive if (ix == sx and iy == sy and iz == sz) else 0.0
                    f_next[ix][iy][iz] = (
                        2.0 * f_curr[ix][iy][iz]
                        - f_prev[ix][iy][iz]
                        + h2 * (lap[ix][iy][iz] + src)
                    )
        f_prev = f_curr
        f_curr = f_next
        history.append([[row[:] for row in plane] for plane in f_curr])
    return history


def _at(history, t, iy, iz):
    """Field at the x_perp=0 plane (where the beam lives)."""
    sc = NW // 2
    sx = sc
    sy = iy + sc
    sz = iz + sc
    if 0 <= t < NL and 0 <= sy < NW and 0 <= sz < NW:
        return history[t][sx][sy][sz]
    return 0.0


def _first_arrival(history, src_layer, offset, eps):
    """First dt where |f| at (iy=0, iz=offset) on x_perp=0 plane exceeds eps."""
    for dt in range(0, NL - src_layer):
        v = abs(_at(history, src_layer + dt, 0, offset))
        if v > eps:
            return dt
    return None


def _frozen(iz_const):
    return lambda t: iz_const


def _moving(iz_start, v_per_layer, src_layer):
    return lambda t: iz_start + int(round(v_per_layer * (t - src_layer)))


def _make_static(s, iz_const, src_layer):
    return _solve_wave_3plus1d(lambda t: s, _frozen(iz_const), src_layer)


def _make_retarded(s, iz_of_t, src_layer):
    return _solve_wave_3plus1d(lambda t: s, iz_of_t, src_layer)


def _make_instantaneous(s, iz_of_t, src_layer):
    """Stitch a history where each layer t is the late-time slice of a
    static (3+1)D solve with the source frozen at iz_of_t(t).
    """
    cache = {}
    history = [_zero3() for _ in range(NL)]
    for t in range(NL):
        if t < src_layer:
            continue
        iz_now = iz_of_t(t)
        if iz_now not in cache:
            full = _solve_wave_3plus1d(lambda tt: s, _frozen(iz_now), src_layer)
            cache[iz_now] = [[row[:] for row in plane] for plane in full[NL - 1]]
        history[t] = [[row[:] for row in plane] for plane in cache[iz_now]]
    return history


def grow(seed, drift, restore):
    rng = random.Random(seed)
    hw = int(PW_BEAM / H)
    md = max(1, round(3 / H))
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


def _prop_beam(pos, adj, nmap, history, k):
    n = len(pos)
    hw = int(PW_BEAM / H)
    field = [0.0] * n
    if history is not None:
        for layer in range(NL):
            for iy in range(-hw, hw + 1):
                for iz in range(-hw, hw + 1):
                    idx = nmap.get((layer, iy, iz))
                    if idx is not None:
                        field[idx] = _at(history, layer, iy, iz)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
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
    hw = int(PW_BEAM / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds = n - npl
    t = sum(abs(amps[i]) ** 2 for i in range(ds, n))
    if t <= 0:
        return 0.0
    return sum(abs(amps[i]) ** 2 * pos[i][2] for i in range(ds, n)) / t


def main():
    print("=" * 70)
    print("(3+1)D PROMOTIONS OF LANE 5 (lightcone) AND LANE 6 (retarded vs inst)")
    print(f"NL={NL}, field cube = {NW}^3, beam PW={PW_BEAM}")
    print("=" * 70)

    src_layer = 4
    iz_start = 6
    iz_end = 0
    n_active = NL - src_layer
    v = (iz_end - iz_start) / n_active

    # === A. Lightcone with delta pulse ===
    print("\nA. (3+1)D LIGHTCONE — delta pulse, eps=1e-6")
    pulse_layer = src_layer

    def pulse_strength(t):
        return 100.0 * S if t == pulse_layer else 0.0

    h_pulse = _solve_wave_3plus1d(pulse_strength, _frozen(0), src_layer)
    print(f"  {'r':>4s} {'first dt':>10s}  result")
    all_ok = True
    for r in [2, 3, 4, 5, 6, 7, 8]:
        dt = _first_arrival(h_pulse, src_layer, r, 1e-6)
        ok = (dt == r)
        if not ok:
            all_ok = False
        print(f"  {r:4d} {str(dt):>10s}  ({'OK' if ok else 'FAIL'})")
    print(f"  verdict: {'STRICT (3+1)D LIGHTCONE CERTIFIED' if all_ok else 'lightcone violation'}")

    # === B. Retarded vs instantaneous on (3+1)D wave ===
    print("\nB. (3+1)D RETARDED vs INSTANTANEOUS — moving source, beam through field")
    print(f"   source iz: {iz_start} -> {iz_end} over {n_active} layers, v/c = {abs(v):.2f}")

    iz_of_t = _moving(iz_start, v, src_layer)
    print("   building retarded history (3+1)D...")
    h_M = _make_retarded(S, iz_of_t, src_layer)
    print("   building instantaneous comparator (3+1)D, cached per source iz...")
    h_I = _make_instantaneous(S, iz_of_t, src_layer)

    print(f"\n  {'family':>6s} {'dM':>12s} {'dI':>12s} {'M-I':>12s} {'rel':>8s}")
    fam_results = []
    for label, drift, restore in FAMILIES:
        pos, adj, nmap = grow(0, drift, restore)
        free = _prop_beam(pos, adj, nmap, None, K)
        z_free = _cz(free, pos)
        cz_M = _cz(_prop_beam(pos, adj, nmap, h_M, K), pos)
        cz_I = _cz(_prop_beam(pos, adj, nmap, h_I, K), pos)
        dM = cz_M - z_free
        dI = cz_I - z_free
        rel = abs(dM - dI) / max(abs(dM), abs(dI), 1e-12)
        fam_results.append((label, dM, dI, rel))
        print(f"  {label:>6s} {dM:+12.6f} {dI:+12.6f} {dM-dI:+12.6f} {rel:8.2%}")

    # === C. Verdict ===
    print("\nC. VERDICT")
    rels = [r[3] for r in fam_results]
    if all(r > 0.05 for r in rels):
        print(f"  RETARDED != INSTANTANEOUS on (3+1)D wave equation, all 3 families")
        print(f"  relative gaps: {[f'{r:.1%}' for r in rels]}")
    elif any(r > 0.05 for r in rels):
        print(f"  partial: some families show >5% gap, others below")
    else:
        print(f"  retarded ~ instantaneous; finite-c effect not resolved at v/c={abs(v):.2f}")


if __name__ == "__main__":
    main()
