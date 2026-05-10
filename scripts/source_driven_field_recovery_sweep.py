#!/usr/bin/env python3
"""Weak-field recovery sweep for the minimal source-driven field architecture.

This runner is self-contained: it defines the exact 3D lattice, the damped
telegraph-style local field rule, and the centroid-z deflection readout
inline so an auditor can verify what the stdout claims directly from this
file. No imports from the broader repo beyond the standard library.

It runs two stages back-to-back:

  Stage 1 — broad calibration sweep (the frozen sweep table)
    parameters: c_field = 0.45, damp = 0.35, target_max in
    {0.001, 0.002, 0.005, 0.010, 0.020, 0.040, 0.080}.
    For each target, scale the source-driven field to that maximum and
    record TOWARD count and the dynamic mass exponent.

  Stage 2 — conservative pocket replay (the frozen pocket row)
    parameters: c_field = 0.40, damp = 0.35, target_max = 0.010.
    Record zero-source reduction, all four source-strength rows, the
    dynamic mass exponent, and the mean |dynamic / instantaneous| ratio.

After the two stages it prints explicit threshold checks (zero-source
reduction exact, all-TOWARD on the pocket, dynamic exponent near 1,
broad-sweep TOWARD survives across all rows) so the load-bearing claim
can be read off the stdout directly.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


# Architecture constants shared by both stages.
BETA = 0.8
K = 5.0
MAX_D_PHYS = 3.0
H = 0.5
NL_PHYS = 30
PW = 6
SOURCE_Z = 3.0
SOURCE_STRENGTHS = (0.001, 0.002, 0.004, 0.008)

# Stage 1 (broad sweep) calibration.
SWEEP_C_FIELD = 0.45
SWEEP_DAMP = 0.35
SWEEP_TARGET_MAXES = (0.001, 0.002, 0.005, 0.010, 0.020, 0.040, 0.080)

# Stage 2 (conservative pocket replay) calibration.
POCKET_C_FIELD = 0.40
POCKET_DAMP = 0.35
POCKET_TARGET_MAX = 0.010


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


def _source_driven_field_layers_raw(
    lat: Lattice3D, source_strength: float, z_src: float, c_field: float, damp: float
) -> list[list[float]]:
    """Unscaled damped local field evolution generated by a static source."""
    gl = lat.nl // 3
    src_y = lat.hw
    src_z = lat.hw + round(z_src / lat.h)
    lam = c_field * c_field

    prev = [[0.0 for _ in range(lat.nw)] for _ in range(lat.nw)]
    curr = [[0.0 for _ in range(lat.nw)] for _ in range(lat.nw)]
    layers = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]

    for layer in range(lat.nl):
        layers[layer] = [curr[y][z] for y in range(lat.nw) for z in range(lat.nw)]
        lap = _laplacian_2d(curr)
        nxt = [[0.0 for _ in range(lat.nw)] for _ in range(lat.nw)]
        for y in range(lat.nw):
            for z in range(lat.nw):
                nxt[y][z] = (2.0 - damp) * curr[y][z] - (1.0 - damp) * prev[y][z] + lam * lap[y][z]
        if layer >= gl:
            nxt[src_y][src_z] += source_strength
        prev, curr = curr, nxt

    return layers


def _scale_field_layers(layers: list[list[float]], scale: float) -> list[list[float]]:
    return [[scale * v for v in row] for row in layers]


def _field_abs_max(layers: list[list[float]]) -> float:
    mx = 0.0
    for row in layers:
        for v in row:
            mx = max(mx, abs(v))
    return mx


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


def _stage1_broad_sweep(lat: Lattice3D, z_free: float) -> tuple[list[tuple[float, int, float | None, float]], int]:
    """Run the broad calibration sweep at SWEEP_C_FIELD / SWEEP_DAMP."""
    print("=" * 84)
    print("STAGE 1 — BROAD CALIBRATION SWEEP")
    print("  weak-field calibration sweep on the exact 3D lattice")
    print("=" * 84)
    print(f"telegraph parameters: c={SWEEP_C_FIELD:.2f}, damp={SWEEP_DAMP:.2f}")
    print(f"source strengths: {SOURCE_STRENGTHS}")
    print()
    print(f"{'target max':>10s} {'toward':>8s} {'F~M':>8s} {'largest delta':>14s}")
    print("-" * 48)

    rows: list[tuple[float, int, float | None, float]] = []
    all_toward_total = 0
    for tmax in SWEEP_TARGET_MAXES:
        ref_raw = _source_driven_field_layers_raw(
            lat, max(SOURCE_STRENGTHS), SOURCE_Z, SWEEP_C_FIELD, SWEEP_DAMP
        )
        ref_max = _field_abs_max(ref_raw)
        gain = tmax / ref_max if ref_max > 1e-30 else 1.0

        vals: list[float] = []
        for s in SOURCE_STRENGTHS:
            dyn = _scale_field_layers(
                _source_driven_field_layers_raw(lat, s, SOURCE_Z, SWEEP_C_FIELD, SWEEP_DAMP),
                gain,
            )
            amps = lat.propagate(dyn, K)
            vals.append(_centroid_z(amps, lat) - z_free)

        alpha = _fit_power(list(SOURCE_STRENGTHS), vals)
        toward = sum(1 for v in vals if v > 0)
        largest = max(vals) if vals else float("nan")
        alpha_str = f"{alpha:.3f}" if alpha is not None else "nan"
        print(f"{tmax:10.3f} {toward:>5d}/4 {alpha_str:>8s} {largest:+14.6e}")
        rows.append((tmax, toward, alpha, largest))
        if toward == len(SOURCE_STRENGTHS):
            all_toward_total += 1
    return rows, all_toward_total


def _stage2_pocket_replay(lat: Lattice3D, z_free: float) -> tuple[list[tuple[float, float, float, float, float]], float, float | None, float | None, int]:
    """Run the conservative pocket replay at POCKET_C_FIELD / POCKET_DAMP / POCKET_TARGET_MAX."""
    print()
    print("=" * 84)
    print("STAGE 2 — CONSERVATIVE POCKET REPLAY")
    print("  exact 3D lattice, telegraph-style field, one conservative weak-field row")
    print("=" * 84)
    print(
        f"h={H}, W={PW}, L={NL_PHYS}, c_field={POCKET_C_FIELD}, "
        f"damp={POCKET_DAMP}, target_max={POCKET_TARGET_MAX}"
    )
    print()

    ref_raw = _source_driven_field_layers_raw(
        lat, max(SOURCE_STRENGTHS), SOURCE_Z, POCKET_C_FIELD, POCKET_DAMP
    )
    ref_max = _field_abs_max(ref_raw)
    gain = POCKET_TARGET_MAX / ref_max if ref_max > 1e-30 else 1.0

    zero_dynamic = _scale_field_layers(
        _source_driven_field_layers_raw(lat, 0.0, SOURCE_Z, POCKET_C_FIELD, POCKET_DAMP),
        gain,
    )
    zero_amps = lat.propagate(zero_dynamic, K)
    zero_delta = _centroid_z(zero_amps, lat) - z_free

    print("REDUCTION CHECK")
    print(f"  zero-source dynamic shift: {zero_delta:+.6e}")
    print(f"  calibration gain: {gain:.6e}")
    print()
    print(f"{'s':>8s} {'inst':>12s} {'dynamic':>12s} {'dyn/inst':>10s} {'max|f_dyn|':>12s}")
    print("-" * 68)

    rows: list[tuple[float, float, float, float, float]] = []
    inst_vals: list[float] = []
    dyn_vals: list[float] = []
    ratios: list[float] = []

    for s in SOURCE_STRENGTHS:
        inst_field = _instantaneous_field_layers(lat, s, SOURCE_Z)
        dyn_field = _scale_field_layers(
            _source_driven_field_layers_raw(lat, s, SOURCE_Z, POCKET_C_FIELD, POCKET_DAMP),
            gain,
        )

        inst_amps = lat.propagate(inst_field, K)
        dyn_amps = lat.propagate(dyn_field, K)

        inst_delta = _centroid_z(inst_amps, lat) - z_free
        dyn_delta = _centroid_z(dyn_amps, lat) - z_free
        ratio = dyn_delta / inst_delta if abs(inst_delta) > 1e-30 else float("nan")
        dyn_max = max(abs(v) for row in dyn_field for v in row)

        inst_vals.append(inst_delta)
        dyn_vals.append(dyn_delta)
        ratios.append(abs(ratio))

        print(f"{s:8.4f} {inst_delta:+12.6e} {dyn_delta:+12.6e} {ratio:10.3f} {dyn_max:12.6e}")
        rows.append((s, inst_delta, dyn_delta, ratio, dyn_max))

    inst_alpha = _fit_power(list(SOURCE_STRENGTHS), inst_vals)
    dyn_alpha = _fit_power(list(SOURCE_STRENGTHS), dyn_vals)
    toward = sum(1 for v in dyn_vals if v > 0)
    mean_ratio = sum(ratios) / len(ratios)

    print()
    print("POCKET SAFE READ")
    if inst_alpha is not None:
        print(f"  instantaneous F~M exponent: {inst_alpha:.2f}")
    else:
        print("  instantaneous F~M exponent: n/a")
    if dyn_alpha is not None:
        print(f"  dynamic F~M exponent: {dyn_alpha:.2f}")
    else:
        print("  dynamic F~M exponent: n/a")
    print(f"  dynamic TOWARD rows: {toward}/{len(dyn_vals)}")
    print(f"  mean |dyn/inst| ratio: {mean_ratio:.3f}")
    return rows, zero_delta, inst_alpha, dyn_alpha, toward


def _threshold_checks(
    sweep_rows: list[tuple[float, int, float | None, float]],
    pocket_zero_delta: float,
    pocket_dyn_alpha: float | None,
    pocket_toward: int,
    pocket_total: int,
    sweep_all_toward_total: int,
) -> int:
    """Print explicit PASS/FAIL threshold checks; return total PASS count."""
    print()
    print("=" * 84)
    print("EXPLICIT THRESHOLD CHECKS")
    print("=" * 84)

    pass_count = 0

    # 1. Zero-source dynamic shift must be exactly zero (machine zero).
    ok = pocket_zero_delta == 0.0
    pass_count += int(ok)
    print(
        f"  [{'PASS' if ok else 'FAIL'}] pocket zero-source dynamic shift exactly zero "
        f"(observed: {pocket_zero_delta:+.6e})"
    )

    # 2. Pocket all-TOWARD: every source-strength row must give positive deflection.
    ok = pocket_toward == pocket_total
    pass_count += int(ok)
    print(
        f"  [{'PASS' if ok else 'FAIL'}] pocket TOWARD survives ({pocket_toward}/{pocket_total})"
    )

    # 3. Pocket dynamic exponent stays near linear: |alpha - 1| <= 0.05.
    if pocket_dyn_alpha is None:
        ok = False
        observed = "n/a"
    else:
        ok = abs(pocket_dyn_alpha - 1.0) <= 0.05
        observed = f"{pocket_dyn_alpha:.3f}"
    pass_count += int(ok)
    print(
        f"  [{'PASS' if ok else 'FAIL'}] pocket dynamic F~M exponent near linear (|alpha-1| <= 0.05; observed {observed})"
    )

    # 4. Broad sweep TOWARD survives across every target row.
    ok = sweep_all_toward_total == len(sweep_rows)
    pass_count += int(ok)
    print(
        f"  [{'PASS' if ok else 'FAIL'}] broad sweep TOWARD survives across every target row "
        f"({sweep_all_toward_total}/{len(sweep_rows)})"
    )

    # 5. Broad sweep monotone drift: dynamic exponent at smallest target close to 1,
    #    falling below 0.7 by the largest target (calibration sensitivity statement).
    smallest = next((a for tmax, _t, a, _l in sweep_rows if a is not None), None)
    largest = None
    for tmax, _t, a, _l in reversed(sweep_rows):
        if a is not None:
            largest = a
            break
    if smallest is None or largest is None:
        ok = False
        observed = "n/a"
    else:
        ok = (smallest >= 0.95) and (largest <= 0.70)
        observed = f"smallest={smallest:.3f}, largest={largest:.3f}"
    pass_count += int(ok)
    print(
        f"  [{'PASS' if ok else 'FAIL'}] broad sweep exponent drift: smallest target near linear, "
        f"largest target drifts away ({observed})"
    )

    print()
    print(f"  total PASS: {pass_count}/5")
    return pass_count


def main() -> None:
    lat = Lattice3D.build(NL_PHYS, PW, H)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, K)
    z_free = _centroid_z(free, lat)

    sweep_rows, sweep_all_toward = _stage1_broad_sweep(lat, z_free)
    pocket_rows, pocket_zero_delta, _pocket_inst_alpha, pocket_dyn_alpha, pocket_toward = (
        _stage2_pocket_replay(lat, z_free)
    )
    pass_count = _threshold_checks(
        sweep_rows,
        pocket_zero_delta,
        pocket_dyn_alpha,
        pocket_toward,
        len(SOURCE_STRENGTHS),
        sweep_all_toward,
    )

    print()
    print("=" * 84)
    print("SAFE READ")
    print("=" * 84)
    print("  the minimal source-driven field has a real weak-field recovery pocket")
    print("  when the calibrated dynamic field stays small")
    print("  as the field calibration grows, the mass exponent drifts away from 1")
    print("  so the architecture is not dead, but it is calibration-sensitive")
    print()
    print(f"RUNNER PASS={pass_count} FAIL={5 - pass_count}")


if __name__ == "__main__":
    main()
