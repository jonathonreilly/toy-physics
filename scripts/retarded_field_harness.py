#!/usr/bin/env python3
"""Retarded gravitational field harness.

Tests the causal structure of gravity: the field propagates at finite
speed, and the beam only responds to the field that has reached it.

Measures:
  1. Retarded vs instantaneous deflection (sudden turn-on)
  2. Retarded oscillating source vs static source
  3. Tail decay rate as function of oscillation period
"""

from __future__ import annotations
import cmath
import math
import time

try:
    import numpy as np
except ModuleNotFoundError:
    raise SystemExit("numpy required")

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3
H = 0.5
STRENGTH = 1e-2
NL_PHYS = 30
PW = 6


class Lattice3D:
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
        for l in range(self.nl):
            self._ls[l] = idx
            x = l * h
            for iy in range(-self.hw, self.hw + 1):
                for iz in range(-self.hw, self.hw + 1):
                    self.pos[idx] = (x, iy * h, iz * h)
                    self.nmap[(l, iy, iz)] = idx
                    idx += 1
        self._off = []
        for dy in range(-self.max_d, self.max_d + 1):
            for dz in range(-self.max_d, self.max_d + 1):
                dyp = dy * h
                dzp = dz * h
                L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
                theta = math.atan2(math.sqrt(dyp ** 2 + dzp ** 2), h)
                self._off.append((dy, dz, L, math.exp(-BETA * theta ** 2)))
        self._nw = nw

    def propagate(self, fields, k):
        n = self.n
        nw = self._nw
        nl = self.nl
        hm = self._hm
        amps = np.zeros(n, dtype=np.complex128)
        src = self.nmap.get((0, 0, 0), 0)
        amps[src] = 1.0
        for layer in range(nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer + 1] if layer + 1 < nl else n
            sa = amps[ls:ls + self.npl].copy()
            if np.max(np.abs(sa)) < 1e-30:
                continue
            sf = fields[layer][ls:ls + self.npl]
            df = fields[min(layer + 1, len(fields) - 1)][ld:ld + self.npl]
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
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def build_retarded(lat, gl, c_field, period, A_osc, s):
    n = lat.n
    pos = lat.pos
    fields = []
    for l in range(lat.nl):
        field_l = np.zeros(n)
        ls = lat._ls[l]
        for i in range(lat.npl):
            node = ls + i
            y_n = pos[node, 1]
            z_n = pos[node, 2]
            r_approx = math.sqrt(y_n ** 2 + (z_n - 3) ** 2) + 0.1
            t_ret = l - r_approx / (c_field * H)
            if t_ret >= gl and t_ret < lat.nl:
                z_src = 3 + A_osc * math.sin(2 * math.pi * t_ret / period)
                r_ret = math.sqrt(y_n ** 2 + (z_n - z_src) ** 2) + 0.1
                field_l[node] = s / r_ret
        fields.append(field_l)
    return fields


def main():
    t_total = time.time()
    lat = Lattice3D(NL_PHYS, PW, H)
    det = [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]
    pos = lat.pos
    n = lat.n
    gl = lat.nl // 3

    ff = [np.zeros(n)] * lat.nl
    a_free = lat.propagate(ff, K)
    pf = sum(abs(a_free[d]) ** 2 for d in det)
    zf = sum(abs(a_free[d]) ** 2 * pos[d, 2] for d in det) / pf

    print("=" * 60)
    print("RETARDED GRAVITATIONAL FIELD HARNESS")
    print(f"  h={H}, W={PW}, L={NL_PHYS}, s={STRENGTH}")
    print("=" * 60)

    # Test 1: Retarded vs instantaneous
    mi = lat.nmap.get((gl, 0, round(3 / H)))
    r_mi = np.sqrt(
        (pos[:, 0] - pos[mi, 0]) ** 2
        + (pos[:, 1] - pos[mi, 1]) ** 2
        + (pos[:, 2] - pos[mi, 2]) ** 2
    ) + 0.1

    inst_fields = [STRENGTH / r_mi] * lat.nl

    c_field = 0.8
    ret_fields = []
    for l in range(lat.nl):
        field_l = np.zeros(n)
        if l >= gl:
            max_reach = (l - gl) * c_field * H
            for i in range(n):
                dist = math.sqrt(
                    (pos[i, 1] - pos[mi, 1]) ** 2 + (pos[i, 2] - pos[mi, 2]) ** 2
                )
                if dist <= max_reach + 0.1:
                    field_l[i] = STRENGTH / r_mi[i]
        ret_fields.append(field_l)

    a_inst = lat.propagate(inst_fields, K)
    a_ret = lat.propagate(ret_fields, K)

    p_inst = sum(abs(a_inst[d]) ** 2 for d in det)
    p_ret = sum(abs(a_ret[d]) ** 2 for d in det)
    z_inst = sum(abs(a_inst[d]) ** 2 * pos[d, 2] for d in det) / p_inst
    z_ret = sum(abs(a_ret[d]) ** 2 * pos[d, 2] for d in det) / p_ret

    print(f"\n  1. RETARDED vs INSTANTANEOUS (sudden turn-on, c={c_field})")
    print(f"     Instantaneous: defl = {z_inst - zf:+.6f}")
    print(f"     Retarded:      defl = {z_ret - zf:+.6f}")
    print(f"     Ratio: {(z_ret - zf) / (z_inst - zf):.2f}")

    # Test 2: Oscillating source with retardation
    print(f"\n  2. OSCILLATING SOURCE (retarded, c={c_field})")
    for period in [4, 8, 16]:
        fields = build_retarded(lat, gl, c_field, period, 2.0, STRENGTH)
        a = lat.propagate(fields, K)
        p = sum(abs(a[d]) ** 2 for d in det)
        z = sum(abs(a[d]) ** 2 * pos[d, 2] for d in det) / p
        print(f"     T={period:2d}: defl = {z - zf:+.6f}")

    # Test 3: Tail decay fingerprint
    print(f"\n  3. TAIL DECAY FINGERPRINT")
    for period in [4, 8, 16]:
        fields = build_retarded(lat, gl, c_field, period, 2.0, STRENGTH)
        a = lat.propagate(fields, K)
        tail = []
        for l in range(lat.nl - 6, lat.nl, 2):
            ls = lat._ls[l]
            layer_nodes = list(range(ls, ls + lat.npl))
            pw_l = sum(abs(a[d]) ** 2 for d in layer_nodes)
            pf_l = sum(abs(a_free[d]) ** 2 for d in layer_nodes)
            if pw_l > 1e-30 and pf_l > 1e-30:
                zw = sum(abs(a[d]) ** 2 * pos[d, 2] for d in layer_nodes) / pw_l
                zf_l = sum(abs(a_free[d]) ** 2 * pos[d, 2] for d in layer_nodes) / pf_l
                tail.append(zw - zf_l)
        if len(tail) >= 2:
            decay = (tail[0] - tail[-1]) / tail[0] if tail[0] > 1e-10 else 0
            print(f"     T={period:2d}: tail decay = {decay:.1%}")

    print(f"\n  Total time: {time.time() - t_total:.0f}s")


if __name__ == "__main__":
    main()
