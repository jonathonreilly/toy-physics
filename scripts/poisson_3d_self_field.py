#!/usr/bin/env python3
"""Poisson 3D self-field: full 3D field derived from a single local equation.

Solves laplacian_3D(f) = -source on the (x, y, z) lattice with a delta
source at the mass position. NO explicit longitudinal factor — both
transverse and longitudinal falloff emerge from the same PDE.

Tests:
  1. Field profile: 1/r law along x and z axes from source
  2. Gravity TOWARD across 3 families
  3. F~M across 3 families
  4. Born test on the derived field
  5. Null at s=0
"""

from __future__ import annotations

import math
import random

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3
H = 0.5
NL = 30
PW = 8
MASS_Z = 3.0
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


def _solve_poisson_3d(nx, nw, src_ix, src_iy, src_iz, strength, n_iter=200):
    """Gauss-Seidel for laplacian_3D(f) = -source on (nx, nw, nw) grid.

    6-point stencil: f[i,j,k] = (sum of 6 neighbors + h^2*src) / 6
    """
    f = [[[0.0] * nw for _ in range(nw)] for _ in range(nx)]
    sy = src_iy + nw // 2
    sz = src_iz + nw // 2
    sx = src_ix
    for _ in range(n_iter):
        for ix in range(1, nx - 1):
            for iy in range(1, nw - 1):
                for iz in range(1, nw - 1):
                    rhs = strength if (ix == sx and iy == sy and iz == sz) else 0.0
                    f[ix][iy][iz] = (
                        f[ix - 1][iy][iz]
                        + f[ix + 1][iy][iz]
                        + f[ix][iy - 1][iz]
                        + f[ix][iy + 1][iz]
                        + f[ix][iy][iz - 1]
                        + f[ix][iy][iz + 1]
                        + rhs
                    ) / 6.0
    return f


def _make_poisson_3d_field(s, z_src):
    hw = int(PW / H)
    nw = 2 * hw + 1
    gl = NL // 3
    iz_src = round(z_src / H)
    # strength chosen so source delta has unit lattice weight; calibration absorbed in s
    strength = s * H * H * 6.0
    return _solve_poisson_3d(NL, nw, gl, 0, iz_src, strength)


def _field_at(fl3, layer, iy, iz):
    hw = int(PW / H)
    nw = 2 * hw + 1
    sy = iy + nw // 2
    sz = iz + nw // 2
    if 0 <= layer < NL and 0 <= sy < nw and 0 <= sz < nw:
        return fl3[layer][sy][sz]
    return 0.0


def _prop_beam(pos, adj, nmap, fl3, k, sources=None):
    n = len(pos)
    hw = int(PW / H)
    nw = 2 * hw + 1
    field = [0.0] * n
    if fl3 is not None:
        for layer in range(NL):
            for iy in range(-hw, hw + 1):
                for iz in range(-hw, hw + 1):
                    idx = nmap.get((layer, iy, iz))
                    if idx is not None:
                        field[idx] = _field_at(fl3, layer, iy, iz)
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
    print("POISSON 3D SELF-FIELD HARNESS")
    print(f"NL={NL}, W={PW}, s={S}, z_src={MASS_Z}")
    print("=" * 70)

    print("\nSolving 3D Poisson (this is slower than 2D)...")
    fl3 = _make_poisson_3d_field(S, MASS_Z)

    # 1. Field profile along x and z axes
    gl = NL // 3
    iz_src = round(MASS_Z / H)
    print("\n1a. FIELD PROFILE along z (source layer x=gl)")
    print(f"  {'iz':>4s} {'f_3D':>14s} {'~1/r':>14s}")
    for iz in range(-3, 8):
        f = _field_at(fl3, gl, 0, iz)
        r = abs(iz * H - MASS_Z) + 0.1
        print(f"  {iz:4d} {f:+14.6f} {S/r:14.6f}")

    print("\n1b. FIELD PROFILE along x (transverse iy=iz=0)")
    print(f"  {'layer':>5s} {'f_3D':>14s} {'~1/dx':>14s}")
    for layer in [gl - 4, gl - 2, gl, gl + 2, gl + 4, gl + 8]:
        if 0 <= layer < NL:
            f = _field_at(fl3, layer, 0, iz_src)
            dx = abs(layer - gl) * H + 0.1
            print(f"  {layer:5d} {f:+14.6f} {S/dx:14.6f}")

    fl_zero = None  # signals no field

    # 2. Gravity TOWARD across families
    print("\n2. GRAVITY across families")
    for label, drift, restore in FAMILIES:
        pos, adj, nmap = grow(0, drift, restore)
        free = _prop_beam(pos, adj, nmap, None, K)
        z_free = _cz(free, pos)
        g = _prop_beam(pos, adj, nmap, fl3, K)
        delta = _cz(g, pos) - z_free
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"  {label}: delta={delta:+.6f} {direction}")

    # 3. F~M
    print("\n3. F~M across families")
    strengths = [0.001, 0.002, 0.004, 0.008]
    fls = [_make_poisson_3d_field(s, MASS_Z) for s in strengths]
    for label, drift, restore in FAMILIES:
        pos, adj, nmap = grow(0, drift, restore)
        free = _prop_beam(pos, adj, nmap, None, K)
        z_free = _cz(free, pos)
        deltas = []
        for fl in fls:
            g = _prop_beam(pos, adj, nmap, fl, K)
            deltas.append(abs(_cz(g, pos) - z_free))
        lx = [math.log(x) for x in strengths]
        ly = [math.log(y) for y in deltas if y > 1e-15]
        if len(ly) >= 3:
            mx = sum(lx[: len(ly)]) / len(ly)
            my = sum(ly) / len(ly)
            sxx = sum((x - mx) ** 2 for x in lx[: len(ly)])
            fm = sum((x - mx) * (y - my) for x, y in zip(lx[: len(ly)], ly)) / sxx
            print(f"  {label}: F~M = {fm:.4f}")

    # 4. Born on derived 3D field
    print("\n4. BORN TEST (Fam1, seed=0, 3D Poisson field)")
    pos, adj, nmap = grow(0, 0.2, 0.7)
    slits = [-1, 0, 1]

    def pb(sl):
        srcs = [(nmap.get((0, s, 0)) or nmap.get((1, s, 0)), 1.0 + 0j) for s in sl]
        srcs = [(i, a) for i, a in srcs if i is not None]
        return _dp(_prop_beam(pos, adj, nmap, fl3, K, sources=srcs), pos)

    p123 = pb(slits)
    p12 = pb([-1, 0])
    p13 = pb([-1, 1])
    p23 = pb([0, 1])
    p1 = pb([-1])
    p2 = pb([0])
    p3 = pb([1])
    i3 = p123 - p12 - p13 - p23 + p1 + p2 + p3
    born = abs(i3) / max(p123, 1e-300)
    print(f"  Born |I3|/P = {born:.2e}")

    # 5. Null at s=0
    print("\n5. NULL TEST")
    pos, adj, nmap = grow(0, 0.2, 0.7)
    free = _prop_beam(pos, adj, nmap, None, K)
    z_free = _cz(free, pos)
    fl0 = _make_poisson_3d_field(0.0, MASS_Z)
    g0 = _prop_beam(pos, adj, nmap, fl0, K)
    print(f"  s=0: delta = {_cz(g0, pos) - z_free:+.6e}")


if __name__ == "__main__":
    main()
