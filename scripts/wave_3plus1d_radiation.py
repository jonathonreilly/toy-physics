#!/usr/bin/env python3
"""(3+1)D wave-equation radiation: full spatial Laplacian.

Promotes the (2+1)D wave equation (Lanes 5-7) to (3+1)D by adding a
third spatial axis w. The PDE becomes
    (1/c^2) d^2f/dt^2 - (d^2/dy^2 + d^2/dz^2 + d^2/dw^2) f = source(t,y,z,w)
with x as time, c = 1 lattice cell per layer.

Decisive observable: radiation slope.
  (2+1)D textbook: |f| ~ 1/sqrt(r), slope = -0.5 (Lane 7 measured -0.47)
  (3+1)D textbook: |f| ~ 1/r, slope = -1.0 (this lane)

Tests:
  1. Lightcone with delta pulse (mirror of Lane 5 in 3D)
  2. Sinusoidal radiation: peak |f| vs r, log-log slope
  3. Slope vs drive frequency (should stay ~ -1)
  4. DFT at detectors (drive frequency dominates)
  5. Static reference (f=0): no radiation
  6. Static source long-time profile vs Poisson 3D shape (sanity)
"""

from __future__ import annotations

import math

H = 0.5
NL = 30
PW = 4.5       # half-width; nw = 2*ceil(PW/H)+1 = 19
S0 = 0.04


def _laplacian_3d(f, nw):
    """7-point stencil on (nw, nw, nw) grid."""
    lap = [[[0.0] * nw for _ in range(nw)] for _ in range(nw)]
    for ix in range(1, nw - 1):
        for iy in range(1, nw - 1):
            for iz in range(1, nw - 1):
                lap[ix][iy][iz] = (
                    f[ix - 1][iy][iz] + f[ix + 1][iy][iz]
                    + f[ix][iy - 1][iz] + f[ix][iy + 1][iz]
                    + f[ix][iy][iz - 1] + f[ix][iy][iz + 1]
                    - 6.0 * f[ix][iy][iz]
                )
    return lap


def _zero_grid(nw):
    return [[[0.0] * nw for _ in range(nw)] for _ in range(nw)]


def _solve_wave_3d(strength_fn, src_layer):
    """Wave evolution with source at center cell, strength = strength_fn(t).

    Returns history[t] = 3D grid of f values at time-step t.
    """
    nw = int(2 * math.ceil(PW / H) + 1)
    sc = nw // 2  # source cell index in each axis
    f_prev = _zero_grid(nw)
    f_curr = _zero_grid(nw)
    history = [_zero_grid(nw), _zero_grid(nw)]
    h2 = H * H
    for t in range(2, NL):
        drive = strength_fn(t) if t >= src_layer else 0.0
        lap = _laplacian_3d(f_curr, nw)
        f_next = _zero_grid(nw)
        for ix in range(nw):
            for iy in range(nw):
                for iz in range(nw):
                    src = drive if (ix == sc and iy == sc and iz == sc) else 0.0
                    f_next[ix][iy][iz] = (
                        2.0 * f_curr[ix][iy][iz]
                        - f_prev[ix][iy][iz]
                        + h2 * (lap[ix][iy][iz] + src)
                    )
        f_prev = f_curr
        f_curr = f_next
        history.append([[row[:] for row in plane] for plane in f_curr])
    return history, nw


def _at(history, t, ix, iy, iz, nw):
    sc = nw // 2
    sx, sy, sz = ix + sc, iy + sc, iz + sc
    if 0 <= t < NL and 0 <= sx < nw and 0 <= sy < nw and 0 <= sz < nw:
        return history[t][sx][sy][sz]
    return 0.0


def _peak_amp(history, src_layer, offset, nw):
    pk = 0.0
    for t in range(src_layer, NL):
        v = abs(_at(history, t, 0, 0, offset, nw))
        if v > pk:
            pk = v
    return pk


def _first_arrival(history, src_layer, offset, eps, nw):
    for dt in range(0, NL - src_layer):
        v = abs(_at(history, src_layer + dt, 0, 0, offset, nw))
        if v > eps:
            return dt
    return None


def _dft_at(history, src_layer, offset, freqs, nw):
    series = [_at(history, t, 0, 0, offset, nw) for t in range(src_layer, NL)]
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


def main():
    print("=" * 70)
    print("(3+1)D WAVE-EQUATION RADIATION HARNESS")
    nw = int(2 * math.ceil(PW / H) + 1)
    print(f"NL={NL}, transverse grid = {nw}^3, S0={S0}")
    print("=" * 70)

    src_layer = 4
    offsets = [2, 3, 4, 5, 6, 7, 8]

    # 1. Lightcone with delta pulse
    print("\n1. LIGHTCONE (delta pulse, eps=1e-6)")
    pulse_layer = src_layer

    def pulse_strength(t):
        return 100.0 * S0 if t == pulse_layer else 0.0

    h_pulse, _ = _solve_wave_3d(pulse_strength, src_layer)
    print(f"  {'r':>4s} {'first dt':>10s}")
    for r in offsets:
        dt = _first_arrival(h_pulse, src_layer, r, 1e-6, nw)
        marker = "OK" if dt == r else "FAIL"
        print(f"  {r:4d} {str(dt):>10s}  ({marker})")

    # 2. Radiation slope (sinusoidal drive)
    f_drive = 0.10
    print(f"\n2. RADIATION SLOPE (drive f={f_drive})")

    def osc_strength(t):
        return S0 * math.sin(2.0 * math.pi * f_drive * (t - src_layer) * H)

    h_osc, _ = _solve_wave_3d(osc_strength, src_layer)
    print(f"  {'r':>4s} {'peak |f|':>14s}")
    pks = []
    for r in offsets:
        pk = _peak_amp(h_osc, src_layer, r, nw)
        pks.append(pk)
        print(f"  {r:4d} {pk:14.6e}")
    if all(p > 0 for p in pks):
        slope = _slope([float(r) for r in offsets], pks)
        print(f"  log-log slope = {slope:.3f}")
        print("  (3+1)D textbook: -1.0 = radiation; (2+1)D was -0.5; near-field ~ -2")
        if -1.3 < slope < -0.7:
            verdict = "RADIATING (3+1)D — slope consistent with -1"
        elif -0.7 < slope < -0.3:
            verdict = "(2+1)D-like — slope still near -0.5"
        elif slope <= -1.5:
            verdict = "NEAR-FIELD-LIKE"
        else:
            verdict = "WEAK / non-monotone"
        print(f"  verdict: {verdict}")

    # 3. Slope vs drive frequency
    print("\n3. SLOPE vs DRIVE FREQUENCY")
    print(f"  {'f':>6s} {'slope':>10s}")
    for f in [0.05, 0.10, 0.15, 0.20]:
        def s_fn(t, ff=f):
            return S0 * math.sin(2.0 * math.pi * ff * (t - src_layer) * H)
        h, _ = _solve_wave_3d(s_fn, src_layer)
        ps = [_peak_amp(h, src_layer, r, nw) for r in offsets]
        if all(p > 0 for p in ps):
            sl = _slope([float(r) for r in offsets], ps)
            print(f"  {f:6.2f} {sl:10.3f}")
        else:
            print(f"  {f:6.2f} {'(zero)':>10s}")

    # 4. DFT at detectors
    print(f"\n4. DFT at detectors (drive f={f_drive})")
    freqs = [0.05, 0.10, 0.15, 0.20, 0.30]
    print(f"  {'r':>4s} " + " ".join(f"{'f='+f'{f:.2f}':>10s}" for f in freqs))
    for r in offsets:
        dft = _dft_at(h_osc, src_layer, r, freqs, nw)
        row = " ".join(f"{v:10.4e}" for v in dft)
        print(f"  {r:4d} {row}")
    print(f"  (peak should be at f={f_drive})")

    # 5. Static reference (f=0)
    print("\n5. STATIC REFERENCE (f=0, no source motion)")

    def zero_strength(t):
        return 0.0

    h_zero, _ = _solve_wave_3d(zero_strength, src_layer)
    print(f"  {'r':>4s} {'peak |f|':>14s}")
    for r in offsets:
        pk = _peak_amp(h_zero, src_layer, r, nw)
        print(f"  {r:4d} {pk:14.6e}")
    print("  (should be exactly 0.0)")

    # 6. Static-source long-time profile (sanity vs Poisson 3D)
    print("\n6. STATIC SOURCE long-time profile (radial)")

    def static_strength(t):
        return S0

    h_stat, _ = _solve_wave_3d(static_strength, src_layer)
    print(f"  {'r':>4s} {'|f| at NL-1':>14s}")
    rs, fs = [], []
    for r in offsets:
        v = abs(_at(h_stat, NL - 1, 0, 0, r, nw))
        print(f"  {r:4d} {v:14.6e}")
        if v > 0:
            rs.append(float(r))
            fs.append(v)
    if len(rs) >= 3:
        slope_static = _slope(rs, fs)
        print(f"  static slope = {slope_static:.3f}")
        print("  (Poisson 3D static is ~ -1; near source can be flatter)")


if __name__ == "__main__":
    main()
