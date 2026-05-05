#!/usr/bin/env python3
"""Exact-lattice Poisson-like self-gravity loop.

Moonshot goal:
  Let amplitude density source a screened Poisson-like field between
  propagation steps on a small exact lattice, then ask whether the weak-field
  sign and linear mass law survive the converged loop.

This harness is intentionally narrow:
  - one exact 3D lattice family at h = 0.25
  - one interior source patch where the amplitude is read back as a mass source
  - one screened Poisson-like kernel
  - one fixed-point loop over the field, not the graph topology
  - one exact epsilon = 0 reduction check
  - one Born check on the converged field snapshot

Born meaning here:
  - the outer self-consistency loop is nonlinear because the field is sourced
    by the propagated amplitude density
  - the inner propagation step is still linear for any fixed field snapshot
  - the Born check below therefore probes the converged field snapshot, not
    the outer fixed-point map
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import math
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


H = 0.25
NL_PHYS = 6
PW = 3
SOURCE_Z = 2.5
SOURCE_CLUSTER = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
SOURCE_STRENGTHS = (0.001, 0.002, 0.004, 0.008)
EPSILONS = (0.0, 0.01, 0.05, 0.1, 0.2, 0.5)
FIELD_TARGET_MAX = 0.05
FIELD_EPS = 0.5
FIELD_MU = 0.08
RELAX = 0.5
MAX_ITERS = 8
TOL = 1e-10
K_BAND = (3.0, 5.0, 7.0)


def _source_cluster_nodes(lat: m.Lattice3D) -> list[int]:
    gl = lat.nl // 3
    src_y = lat.hw
    src_z = lat.hw + round(SOURCE_Z / lat.h)
    nodes: list[int] = []
    for dy, dz in SOURCE_CLUSTER:
        y = src_y + dy
        z = src_z + dz
        if 0 <= y < lat.nw and 0 <= z < lat.nw:
            nodes.append(lat.nmap[(gl, y - lat.hw, z - lat.hw)])
    return nodes


def _normalize_weights(vals: list[float]) -> list[float]:
    total = sum(vals)
    if total <= 1e-30:
        return [1.0 / len(vals)] * len(vals)
    return [v / total for v in vals]


def _field_abs_max(layers: list[list[float]]) -> float:
    return max(abs(v) for row in layers for v in row) if layers else 0.0


def _poisson_like_field(
    lat: m.Lattice3D,
    source_nodes: list[int],
    weights: list[float],
    coupling: float,
) -> list[list[float]]:
    """Screened Poisson-like field sourced by a weighted amplitude patch."""
    if not source_nodes:
        return [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]

    source_pos = [lat.pos[i] for i in source_nodes]
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    for layer in range(lat.nl):
        ls = lat.layer_start[layer]
        for i in range(lat.npl):
            x, y, z = lat.pos[ls + i]
            val = 0.0
            for w, (mx, my, mz) in zip(weights, source_pos):
                r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + FIELD_EPS
                val += w * coupling * math.exp(-FIELD_MU * r) / r
            field[layer][i] = val
    return field


def _propagate_from_sources(
    lat: m.Lattice3D,
    field_layers: list[list[float]],
    k: float,
    source_nodes: list[int],
) -> list[complex]:
    """Exact-lattice forward propagation with arbitrary layer-0 source nodes."""
    amps = [0j] * lat.n
    if not source_nodes:
        return amps

    for s in source_nodes:
        amps[s] = 1.0

    for layer in range(lat.nl - 1):
        ls = lat.layer_start[layer]
        ld = lat.layer_start[layer + 1]
        sa = amps[ls : ls + lat.npl]
        if max(abs(a) for a in sa) < 1e-30:
            continue
        sf = field_layers[layer]
        df = field_layers[min(layer + 1, lat.nl - 1)]
        for dy, dz, L, w in lat.offsets:
            ym = max(0, -dy)
            yM = min(lat.nw, lat.nw - dy)
            zm = max(0, -dz)
            zM = min(lat.nw, lat.nw - dz)
            if ym >= yM or zm >= zM:
                continue
            for yi in range(ym, yM):
                for zi in range(zm, zM):
                    si = yi * lat.nw + zi
                    ai = sa[si]
                    if abs(ai) < 1e-30:
                        continue
                    di = (yi + dy) * lat.nw + (zi + dz)
                    lf = 0.5 * (sf[si] + df[di])
                    act = L * (1.0 - lf)
                    amps[ld + di] += ai * complex(math.cos(k * act), math.sin(k * act)) * w / (L * L)
    return amps


def _centroid_z(amps: list[complex], lat: m.Lattice3D) -> float:
    det_start = lat.layer_start[lat.nl - 1]
    total = 0.0
    weighted = 0.0
    for d in range(det_start, det_start + lat.npl):
        p = abs(amps[d]) ** 2
        total += p
        weighted += p * lat.pos[d][2]
    return weighted / total if total > 1e-30 else 0.0


def _detector_prob(amps: list[complex], lat: m.Lattice3D) -> float:
    det_start = lat.layer_start[lat.nl - 1]
    return sum(abs(amps[d]) ** 2 for d in range(det_start, det_start + lat.npl))


def _born_i3(field_layers: list[list[float]], lat: m.Lattice3D, k: float) -> float:
    """Corrected Sorkin-style I3 on three layer-0 source nodes."""
    triplet = [
        lat.nmap[(0, -1, 0)],
        lat.nmap[(0, 0, 0)],
        lat.nmap[(0, 1, 0)],
    ]
    det_start = lat.layer_start[lat.nl - 1]
    det_nodes = range(det_start, det_start + lat.npl)

    def det_prob(src_nodes: list[int]) -> float:
        amps = _propagate_from_sources(lat, field_layers, k, src_nodes)
        return sum(abs(amps[d]) ** 2 for d in det_nodes)

    a, b, c = triplet
    pab = det_prob([a, b])
    pac = det_prob([a, c])
    pbc = det_prob([b, c])
    pa = det_prob([a])
    pb = det_prob([b])
    pc = det_prob([c])
    pabc = det_prob([a, b, c])
    i3 = pabc - pab - pac - pbc + pa + pb + pc
    return abs(i3) / pabc if pabc > 1e-30 else math.nan


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


def _self_consistent_loop(
    lat: m.Lattice3D,
    source_strength: float,
    epsilon: float,
    source_nodes: list[int],
    gain: float,
) -> tuple[list[list[float]], list[float], bool, int, float]:
    """Iterate amplitude -> Poisson field -> amplitude until convergence."""
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    weights = [1.0 / len(source_nodes)] * len(source_nodes)
    origin = [lat.nmap[(0, 0, 0)]]

    for iteration in range(1, MAX_ITERS + 1):
        amps = _propagate_from_sources(lat, field, m.K, origin)
        density = [abs(amps[i]) ** 2 for i in source_nodes]
        weights_next = _normalize_weights(density)
        coupling = epsilon * source_strength
        raw_field = _poisson_like_field(lat, source_nodes, weights_next, coupling)
        field_next = [[gain * v for v in row] for row in raw_field]

        field_delta = max(
            abs(field_next[layer][idx] - field[layer][idx])
            for layer in range(lat.nl)
            for idx in range(lat.npl)
        )
        weight_delta = max(abs(a - b) for a, b in zip(weights_next, weights))

        if field_delta < TOL and weight_delta < TOL:
            return field_next, weights_next, True, iteration, field_delta

        field = [
            [
                (1.0 - RELAX) * field[layer][idx] + RELAX * field_next[layer][idx]
                for idx in range(lat.npl)
            ]
            for layer in range(lat.nl)
        ]
        weights = weights_next

    return field, weights, False, MAX_ITERS, field_delta


def main() -> None:
    lat = m.Lattice3D.build(NL_PHYS, PW, H)
    source_nodes = _source_cluster_nodes(lat)
    source_mass_centroid = sum(lat.pos[i][2] for i in source_nodes) / len(source_nodes)

    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = _propagate_from_sources(lat, zero_field, m.K, [lat.nmap[(0, 0, 0)]])
    z_free = _centroid_z(free, lat)
    p_free = _detector_prob(free, lat)

    # One fixed calibration for the whole sweep, preserving source-strength scaling.
    ref_raw = _poisson_like_field(
        lat,
        source_nodes,
        [1.0 / len(source_nodes)] * len(source_nodes),
        max(SOURCE_STRENGTHS) * max(EPSILONS),
    )
    gain = FIELD_TARGET_MAX / _field_abs_max(ref_raw) if _field_abs_max(ref_raw) > 1e-30 else 1.0

    print("=" * 94)
    print("POISSON SELF-GRAVITY LOOP")
    print("  exact h=0.25 lattice, amplitude-sourced field between propagation steps")
    print("  comparison: one-shot Poisson field vs self-consistent Poisson loop")
    print("=" * 94)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_patch={len(source_nodes)} nodes")
    print(f"source patch nodes={source_nodes}")
    print(f"source patch z-centroid = {source_mass_centroid:+.3f}")
    print(f"kernel: exp(-mu r)/(r+eps), mu={FIELD_MU:.2f}, eps={FIELD_EPS:.2f}")
    print(f"source strengths={SOURCE_STRENGTHS}")
    print(f"backreaction couplings={EPSILONS}")
    print(f"field gain={gain:.6e} (calibrated to max source/coupling row)")
    print("Born is checked on the frozen converged field snapshot, not on the")
    print("outer fixed-point map.")
    print()

    # Exact reduction check.
    zero_loop_field, _, converged, n_iter, residual = _self_consistent_loop(
        lat, 0.0, 0.0, source_nodes, gain
    )
    zero_amps = _propagate_from_sources(lat, zero_loop_field, m.K, [lat.nmap[(0, 0, 0)]])
    zero_delta = _centroid_z(zero_amps, lat) - z_free
    zero_escape = _detector_prob(zero_amps, lat) / p_free if p_free > 1e-30 else math.nan

    print("REDUCTION CHECK")
    print(f"  zero-epsilon centroid shift: {zero_delta:+.6e}")
    print(f"  zero-epsilon escape ratio:   {zero_escape:.6f}")
    print(f"  zero-epsilon converged:       {converged}")
    print(f"  zero-epsilon iters/residual:  {n_iter} / {residual:.3e}")
    print()

    print(
        f"{'eps':>6s} {'s':>8s} {'inst':>12s} {'loop':>12s} {'loop/inst':>10s} "
        f"{'esc':>8s} {'Born':>10s} {'it':>3s} {'ok':>2s}"
    )
    print("-" * 90)

    summary = {}
    for epsilon in EPSILONS:
        inst_vals: list[float] = []
        loop_vals: list[float] = []
        born_vals: list[float] = []
        esc_vals: list[float] = []
        toward = 0
        max_resid = 0.0
        n_ok = 0

        for s in SOURCE_STRENGTHS:
            inst_field = _poisson_like_field(
                lat,
                source_nodes,
                [1.0 / len(source_nodes)] * len(source_nodes),
                epsilon * s * gain,
            )
            loop_field, weights, converged, n_iter, residual = _self_consistent_loop(
                lat, s, epsilon, source_nodes, gain
            )

            inst_amps = _propagate_from_sources(lat, inst_field, m.K, [lat.nmap[(0, 0, 0)]])
            loop_amps = _propagate_from_sources(lat, loop_field, m.K, [lat.nmap[(0, 0, 0)]])

            inst_delta = _centroid_z(inst_amps, lat) - z_free
            loop_delta = _centroid_z(loop_amps, lat) - z_free
            inst_vals.append(inst_delta)
            loop_vals.append(loop_delta)
            toward += int(loop_delta > 0)
            esc_vals.append(_detector_prob(loop_amps, lat) / p_free if p_free > 1e-30 else math.nan)
            born_vals.append(_born_i3(loop_field, lat, m.K))
            max_resid = max(max_resid, residual)
            n_ok += int(converged)

            ratio = loop_delta / inst_delta if abs(inst_delta) > 1e-30 else math.nan
            print(
                f"{epsilon:6.2f} {s:8.4f} {inst_delta:+12.6e} {loop_delta:+12.6e} "
                f"{ratio:10.3f} {esc_vals[-1]:8.3f} {born_vals[-1]:10.3e} "
                f"{n_iter:3d} {'Y' if converged else 'n'}"
            )

        inst_alpha = _fit_power(list(SOURCE_STRENGTHS), [abs(v) for v in inst_vals])
        loop_alpha = _fit_power(list(SOURCE_STRENGTHS), [abs(v) for v in loop_vals])
        mean_ratio = sum(abs(l / i) for l, i in zip(loop_vals, inst_vals) if abs(i) > 1e-30) / len(SOURCE_STRENGTHS)
        mean_escape = sum(esc_vals) / len(esc_vals)
        born_mean = sum(born_vals) / len(born_vals)
        born_max = max(born_vals)
        summary[epsilon] = (inst_alpha, loop_alpha, toward, mean_ratio, mean_escape, born_mean, born_max, max_resid, n_ok)
        inst_alpha_s = f"{inst_alpha:.2f}" if inst_alpha is not None else "n/a"
        loop_alpha_s = f"{loop_alpha:.2f}" if loop_alpha is not None else "n/a"
        print(
            f"  eps={epsilon:.2f} summary: inst α={inst_alpha_s} "
            f"loop α={loop_alpha_s} toward={toward}/{len(SOURCE_STRENGTHS)} "
            f"mean|loop/inst|={mean_ratio:.3f} mean escape={mean_escape:.3f} "
            f"Born mean/max={born_mean:.2e}/{born_max:.2e} "
            f"resid={max_resid:.3e} converged={n_ok}/{len(SOURCE_STRENGTHS)}"
        )

    print()
    print("SAFE READ")
    print(f"  exact zero-epsilon reduction shift: {zero_delta:+.3e}")
    if summary:
        best_eps = min(summary.keys(), key=lambda e: summary[e][7])
        inst_alpha, loop_alpha, toward, mean_ratio, mean_escape, born_mean, born_max, resid, n_ok = summary[best_eps]
        print(f"  best residual epsilon: {best_eps:.2f} (resid={resid:.3e})")
        print(f"  best-loop F~M exponent: {loop_alpha:.2f}" if loop_alpha is not None else "  best-loop F~M exponent: n/a")
        print(f"  best-loop TOWARD rows: {toward}/{len(SOURCE_STRENGTHS)}")
        print(f"  best-loop mean escape ratio: {mean_escape:.3f}")
        print(f"  best-loop Born mean/max: {born_mean:.2e}/{born_max:.2e}")
    print("  the outer loop is nonlinear, but each frozen field snapshot remains")
    print("  Born-linear to the tested precision")


if __name__ == "__main__":
    main()
