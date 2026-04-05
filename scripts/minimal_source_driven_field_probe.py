#!/usr/bin/env python3
"""Minimal source-driven field probe on the 3D lattice.

Moonshot goal:
  Replace imposed retarded scheduling with the smallest stable local field
  evolution rule that is actually generated from a source on the lattice, then
  check whether the weak-field gravity lane survives.

This is intentionally narrow:
  - one family: exact 3D lattice
  - one source: static mass source
  - one field rule: damped local telegraph-style evolution on the yz plane
  - one comparison: source-driven field vs instantaneous 1/r field
  - one reduction check: zero source recovers free propagation exactly
"""

from __future__ import annotations

import math
from dataclasses import dataclass


BETA = 0.8
K = 5.0
MAX_D_PHYS = 3.0
H = 0.5
NL_PHYS = 30
PW = 6
SOURCE_Z = 3.0
SOURCE_STRENGTHS = (0.001, 0.002, 0.004, 0.008)

# Stable damped field-evolution parameters.
C_FIELD = 0.45
DAMP = 0.35


@dataclass
class Lattice3D:
    h: float
    nl: int
    hw: int
    max_d: int
    npl: int
    n: int
    pos: list[tuple[float, float, float]]
    nmap: dict[tuple[int, int, int], int]
    layer_start: list[int]
    offsets: list[tuple[int, int, float, float]]
    nw: int

    @classmethod
    def build(cls, phys_l: int, phys_w: int, h: float) -> "Lattice3D":
        nl = int(phys_l / h) + 1
        hw = int(phys_w / h)
        max_d = max(1, round(MAX_D_PHYS / h))
        nw = 2 * hw + 1
        npl = nw * nw
        n = nl * npl
        pos: list[tuple[float, float, float]] = []
        nmap: dict[tuple[int, int, int], int] = {}
        layer_start = [0] * nl

        idx = 0
        for layer in range(nl):
            layer_start[layer] = idx
            x = layer * h
            for iy in range(-hw, hw + 1):
                for iz in range(-hw, hw + 1):
                    pos.append((x, iy * h, iz * h))
                    nmap[(layer, iy, iz)] = idx
                    idx += 1

        offsets: list[tuple[int, int, float, float]] = []
        for dy in range(-max_d, max_d + 1):
            for dz in range(-max_d, max_d + 1):
                dyp = dy * h
                dzp = dz * h
                L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
                theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), h)
                offsets.append((dy, dz, L, math.exp(-BETA * theta * theta)))

        return cls(h, nl, hw, max_d, npl, n, pos, nmap, layer_start, offsets, nw)

    def propagate(self, field_layers: list[list[float]], k: float) -> list[complex]:
        amps = [0j] * self.n
        src = self.nmap[(0, 0, 0)]
        amps[src] = 1.0

        for layer in range(self.nl - 1):
            ls = self.layer_start[layer]
            ld = self.layer_start[layer + 1]
            sa = amps[ls : ls + self.npl]
            if max(abs(a) for a in sa) < 1e-30:
                continue
            sf = field_layers[layer]
            df = field_layers[min(layer + 1, self.nl - 1)]
            for dy, dz, L, w in self.offsets:
                ym = max(0, -dy)
                yM = min(self.nw, self.nw - dy)
                zm = max(0, -dz)
                zM = min(self.nw, self.nw - dz)
                if ym >= yM or zm >= zM:
                    continue
                for yi in range(ym, yM):
                    for zi in range(zm, zM):
                        si = yi * self.nw + zi
                        ai = sa[si]
                        if abs(ai) < 1e-30:
                            continue
                        di = (yi + dy) * self.nw + (zi + dz)
                        lf = 0.5 * (sf[si] + df[di])
                        act = L * (1.0 - lf)
                        amps[ld + di] += ai * complex(math.cos(k * act), math.sin(k * act)) * w / (L * L)
        return amps


def _centroid_z(amps: list[complex], lat: Lattice3D) -> float:
    det_start = lat.layer_start[lat.nl - 1]
    det_nodes = range(det_start, det_start + lat.npl)
    total = 0.0
    weighted = 0.0
    for d in det_nodes:
        p = abs(amps[d]) ** 2
        total += p
        weighted += p * lat.pos[d][2]
    return weighted / total if total > 1e-30 else 0.0


def _instantaneous_field_layers(lat: Lattice3D, source_strength: float, z_src: float) -> list[list[float]]:
    gl = lat.nl // 3
    src_idx = lat.nmap[(gl, 0, round(z_src / lat.h))]
    sx, sy, sz = lat.pos[src_idx]
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    for layer in range(lat.nl):
        ls = lat.layer_start[layer]
        for i in range(lat.npl):
            x, y, z = lat.pos[ls + i]
            r = math.sqrt((x - sx) ** 2 + (y - sy) ** 2 + (z - sz) ** 2) + 0.1
            field[layer][i] = source_strength / r
    return field


def _laplacian_2d(arr: list[list[float]]) -> list[list[float]]:
    n = len(arr)
    out = [[0.0 for _ in range(n)] for _ in range(n)]
    for y in range(1, n - 1):
        for z in range(1, n - 1):
            out[y][z] = (
                arr[y - 1][z]
                + arr[y + 1][z]
                + arr[y][z - 1]
                + arr[y][z + 1]
                - 4.0 * arr[y][z]
            )
    return out


def _source_driven_field_layers(lat: Lattice3D, source_strength: float, z_src: float) -> list[list[float]]:
    """Damped local field evolution generated by a static source."""
    gl = lat.nl // 3
    src_y = lat.hw
    src_z = lat.hw + round(z_src / lat.h)
    lam = C_FIELD * C_FIELD

    prev = [[0.0 for _ in range(lat.nw)] for _ in range(lat.nw)]
    curr = [[0.0 for _ in range(lat.nw)] for _ in range(lat.nw)]
    layers = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]

    for layer in range(lat.nl):
        layers[layer] = [curr[y][z] for y in range(lat.nw) for z in range(lat.nw)]
        lap = _laplacian_2d(curr)
        nxt = [[0.0 for _ in range(lat.nw)] for _ in range(lat.nw)]
        for y in range(lat.nw):
            for z in range(lat.nw):
                nxt[y][z] = (2.0 - DAMP) * curr[y][z] - (1.0 - DAMP) * prev[y][z] + lam * lap[y][z]
        if layer >= gl:
            nxt[src_y][src_z] += source_strength
        prev, curr = curr, nxt

    # Normalize into a weak-field regime comparable to the instantaneous lane.
    mx = 0.0
    for row in layers:
        for v in row:
            mx = max(mx, abs(v))
    if mx > 1e-30:
        scale = 0.08 / mx
        for layer in range(lat.nl):
            for i in range(lat.npl):
                layers[layer][i] *= scale
    return layers


def _fit_power(xs: list[float], ys: list[float]) -> float | None:
    pairs = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(pairs) < 3:
        return None
    lx = [math.log(x) for x, _ in pairs]
    ly = [math.log(y) for _, y in pairs]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def main() -> None:
    lat = Lattice3D.build(NL_PHYS, PW, H)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, K)
    z_free = _centroid_z(free, lat)

    print("=" * 76)
    print("MINIMAL SOURCE-DRIVEN FIELD PROBE")
    print("  exact 3D lattice, static source, local damped field evolution")
    print("  comparison: source-driven field vs instantaneous 1/r field")
    print("=" * 76)
    print()

    # Reduction check.
    zero_dynamic = _source_driven_field_layers(lat, 0.0, SOURCE_Z)
    zero_amps = lat.propagate(zero_dynamic, K)
    zero_delta = _centroid_z(zero_amps, lat) - z_free

    print("REDUCTION CHECK")
    print(f"  zero-source dynamic shift: {zero_delta:+.6e}")
    print()

    print(f"{'s':>8s} {'inst':>12s} {'dyn':>12s} {'dyn/inst':>10s} {'max|f_dyn|':>12s}")
    print("-" * 62)

    inst_vals: list[float] = []
    dyn_vals: list[float] = []

    for s in SOURCE_STRENGTHS:
        inst_field = _instantaneous_field_layers(lat, s, SOURCE_Z)
        dyn_field = _source_driven_field_layers(lat, s, SOURCE_Z)

        inst_amps = lat.propagate(inst_field, K)
        dyn_amps = lat.propagate(dyn_field, K)

        inst_delta = _centroid_z(inst_amps, lat) - z_free
        dyn_delta = _centroid_z(dyn_amps, lat) - z_free

        inst_vals.append(inst_delta)
        dyn_vals.append(dyn_delta)

        ratio = dyn_delta / inst_delta if abs(inst_delta) > 1e-30 else math.nan
        dyn_max = max(abs(v) for row in dyn_field for v in row)
        print(f"{s:8.4f} {inst_delta:+12.6e} {dyn_delta:+12.6e} {ratio:10.3f} {dyn_max:12.6e}")

    inst_alpha = _fit_power(list(SOURCE_STRENGTHS), inst_vals)
    dyn_alpha = _fit_power(list(SOURCE_STRENGTHS), dyn_vals)

    toward_inst = sum(1 for v in inst_vals if v > 0)
    toward_dyn = sum(1 for v in dyn_vals if v > 0)

    print()
    print("SAFE READ")
    print(f"  instantaneous TOWARD rows: {toward_inst}/{len(inst_vals)}")
    print(f"  source-driven TOWARD rows: {toward_dyn}/{len(dyn_vals)}")
    if inst_alpha is not None:
        print(f"  instantaneous F~M exponent: {inst_alpha:.2f}")
    if dyn_alpha is not None:
        print(f"  source-driven F~M exponent: {dyn_alpha:.2f}")
    print("  zero-source dynamic field should recover free propagation exactly.")
    print("  If the source-driven rows lose TOWARD or linear mass response, freeze this as a no-go.")


if __name__ == "__main__":
    main()
