#!/usr/bin/env python3
"""Wave-equation radiation: oscillating source emits a propagating field.

Drive a source whose STRENGTH oscillates sinusoidally:
    src(t) = S0 * sin(2*pi*f*t*H)  for t >= src_layer
through the discrete (2+1)D wave equation
    (1/c^2) d^2f/dt^2 - laplacian_yz(f) = src(t, y, z),
with x as time, c = 1 lattice cell per layer.

Tests:
  1. First-arrival dt vs distance r (lightcone)
  2. Peak amplitude vs distance (far-field falloff slope)
     Note: this is (2+1)D scalar wave; the textbook far-field
     amplitude law in 2 spatial dims is ~ 1/sqrt(r), not 1/r.
     Expected slope ~ -0.5 for true radiation, ~ -2 for near-field
     static profile.
  3. Frequency content at detectors via DFT — should peak at drive f
  4. Static reference (f=0): no radiation
  5. Multiple drive frequencies: 1/r law (slope) should be f-independent
  6. F~M and Born sanity on the radiating field
  7. Family portability of the slope

This tests whether the wave equation has genuine radiating solutions
(propagating disturbances at finite c with the correct geometric
falloff), distinct from the static near-field used for retarded gravity.
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
NL = 60
PW = 12
S0 = 0.04
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


def _solve_wave_osc(strength, freq, src_layer):
    """Wave evolution with oscillating monopole source at (iy=0, iz=0)."""
    hw = int(PW / H)
    nw = 2 * hw + 1
    sy = nw // 2
    sz = nw // 2
    f_prev = [[0.0] * nw for _ in range(nw)]
    f_curr = [[0.0] * nw for _ in range(nw)]
    history = [
        [[0.0] * nw for _ in range(nw)],
        [[0.0] * nw for _ in range(nw)],
    ]
    h2 = H * H
    for t in range(2, NL):
        if t >= src_layer:
            drive = strength * math.sin(2.0 * math.pi * freq * (t - src_layer) * H)
        else:
            drive = 0.0
        lap = _laplacian_yz(f_curr, nw)
        f_next = [[0.0] * nw for _ in range(nw)]
        for iy in range(nw):
            for iz in range(nw):
                src = drive if (iy == sy and iz == sz) else 0.0
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


def _peak_amp(history, src_layer, offset):
    """Peak |f| over time at (iy=0, iz=offset)."""
    pk = 0.0
    for t in range(src_layer, NL):
        v = abs(_field_at(history, t, 0, offset))
        if v > pk:
            pk = v
    return pk


def _first_arrival(history, src_layer, offset, eps):
    for dt in range(0, NL - src_layer):
        v = abs(_field_at(history, src_layer + dt, 0, offset))
        if v > eps:
            return dt
    return None


def _dft_at(history, src_layer, offset, freqs):
    """DFT magnitude at trial frequencies for the time series at offset."""
    series = [_field_at(history, t, 0, offset) for t in range(src_layer, NL)]
    n = len(series)
    out = []
    for f in freqs:
        re = sum(series[k] * math.cos(2 * math.pi * f * k * H) for k in range(n))
        im = sum(series[k] * math.sin(2 * math.pi * f * k * H) for k in range(n))
        out.append(math.sqrt(re * re + im * im) * 2.0 / n)
    return out


def _slope(xs, ys):
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    n = len(lx)
    mx = sum(lx) / n
    my = sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in lx)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx if sxx > 0 else 0.0


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


def main():
    print("=" * 70)
    print("WAVE-EQUATION RADIATION HARNESS")
    print(f"NL={NL}, W={PW}, S0={S0}")
    print("=" * 70)

    src_layer = 5
    offsets = [2, 4, 6, 8, 10, 12]
    f_drive = 0.10

    # 1. Lightcone arrivals
    print(f"\n1. LIGHTCONE ARRIVALS (drive f={f_drive})")
    history = _solve_wave_osc(S0, f_drive, src_layer)
    print(f"  {'r':>4s} {'first dt':>10s}")
    for r in offsets:
        dt = _first_arrival(history, src_layer, r, 1e-8)
        marker = "OK" if dt == r else "FAIL"
        print(f"  {r:4d} {str(dt):>10s}  ({marker})")

    # 2. Peak amplitude vs distance (far-field falloff)
    print(f"\n2. PEAK AMPLITUDE vs DISTANCE (drive f={f_drive})")
    print(f"  {'r':>4s} {'peak |f|':>14s}")
    pks = []
    for r in offsets:
        pk = _peak_amp(history, src_layer, r)
        pks.append(pk)
        print(f"  {r:4d} {pk:14.6e}")
    slope = _slope([float(r) for r in offsets], pks)
    print(f"  log-log slope = {slope:.3f}")
    print("  (2+1D scalar wave: ~ -0.5 = radiation, ~ -2 = near-field)")
    if slope < -0.2 and slope > -1.2:
        verdict = "RADIATING (consistent with 2+1D wave)"
    elif slope <= -1.5:
        verdict = "NEAR-FIELD-LIKE (~ 1/r^2)"
    else:
        verdict = "WEAK FALLOFF or non-monotone"
    print(f"  verdict: {verdict}")

    # 3. Frequency content at detectors via DFT
    print(f"\n3. DFT FREQUENCY CONTENT at offsets (drive f={f_drive})")
    freqs = [0.05, 0.10, 0.15, 0.20, 0.30]
    print(f"  {'r':>4s} " + " ".join(f"{'f='+f'{f:.2f}':>10s}" for f in freqs))
    for r in offsets:
        dft = _dft_at(history, src_layer, r, freqs)
        row = " ".join(f"{v:10.4e}" for v in dft)
        print(f"  {r:4d} {row}")
    print(f"  (peak should be at f={f_drive}, the drive frequency)")

    # 4. Static reference (f=0): no radiation
    print("\n4. STATIC REFERENCE (f=0, no radiation expected)")
    history_static = _solve_wave_osc(S0, 0.0, src_layer)
    print(f"  {'r':>4s} {'peak |f|':>14s}")
    for r in offsets:
        pk = _peak_amp(history_static, src_layer, r)
        print(f"  {r:4d} {pk:14.6e}")

    # 5. Multi-frequency slope
    print("\n5. SLOPE vs DRIVE FREQUENCY")
    print(f"  {'f':>6s} {'slope':>10s}")
    for f in [0.05, 0.10, 0.15, 0.20]:
        h = _solve_wave_osc(S0, f, src_layer)
        ps = [_peak_amp(h, src_layer, r) for r in offsets]
        if all(p > 0 for p in ps):
            sl = _slope([float(r) for r in offsets], ps)
            print(f"  {f:6.2f} {sl:10.3f}")
        else:
            print(f"  {f:6.2f} {'(zero amp)':>10s}")

    # 6. F~M and Born sanity on the radiating field
    print(f"\n6. F~M / BORN / NULL on radiating field (drive f={f_drive})")
    pos, adj, nmap = grow(0, 0.2, 0.7)
    free = _prop_beam(pos, adj, nmap, None, K)
    z_free = _cz(free, pos)

    strengths = [0.01, 0.02, 0.04, 0.08]
    fls = [_solve_wave_osc(s, f_drive, src_layer) for s in strengths]
    deltas = []
    for fl in fls:
        g = _prop_beam(pos, adj, nmap, fl, K)
        deltas.append(abs(_cz(g, pos) - z_free))
    print(f"  delta_z by strength: {[f'{d:.4e}' for d in deltas]}")
    if all(d > 1e-15 for d in deltas):
        sl = _slope(strengths, deltas)
        print(f"  F~M = {sl:.4f}")

    # Born
    slits = [-1, 0, 1]
    h_born = _solve_wave_osc(S0, f_drive, src_layer)

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

    # Null
    h_null = _solve_wave_osc(0.0, f_drive, src_layer)
    g_null = _prop_beam(pos, adj, nmap, h_null, K)
    print(f"  Null (S0=0): delta_z = {_cz(g_null, pos) - z_free:+.6e}")

    # 7. Family portability — F~M of radiating field across grown geometries
    # The radiation slope is a property of the wave PDE alone (no beam),
    # so it is the same for every family by construction. The quantity
    # that DOES vary with grown geometry is the beam-side F~M scaling on
    # the radiating field. Test that across all three families.
    print(f"\n7. FAMILY PORTABILITY (F~M on radiating field, drive f={f_drive})")
    strengths_fp = [0.01, 0.02, 0.04, 0.08]
    fls_fp = [_solve_wave_osc(s, f_drive, src_layer) for s in strengths_fp]
    print(f"  {'family':>6s} {'F~M':>10s}")
    for label, drift, restore in FAMILIES:
        p, a, nm = grow(0, drift, restore)
        zf = _cz(_prop_beam(p, a, nm, None, K), p)
        deltas_fp = []
        for fl in fls_fp:
            g = _prop_beam(p, a, nm, fl, K)
            deltas_fp.append(abs(_cz(g, p) - zf))
        if all(d > 1e-15 for d in deltas_fp):
            sl_fp = _slope(strengths_fp, deltas_fp)
            print(f"  {label:>6s} {sl_fp:10.4f}")
        else:
            print(f"  {label:>6s} {'(zero)':>10s}")


if __name__ == "__main__":
    main()
