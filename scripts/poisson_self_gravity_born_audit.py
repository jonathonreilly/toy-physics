#!/usr/bin/env python3
"""Born audit for an iterated Poisson-like self-gravity loop.

This is intentionally narrow:
  - one exact 3D lattice family at h = 0.25
  - one three-slit source set on the input layer
  - one screened Poisson-like backreaction loop
  - one exact zero-coupling reduction check
  - one per-step Born check on a frozen loop snapshot
  - one end-to-end Born check through the full iterated loop

The audit distinction is the key point:
  - per-step Born is evaluated on a fixed converged field snapshot
  - end-to-end Born is evaluated after running the full loop separately for
    1-slit, 2-slit, and 3-slit initial conditions
"""

from __future__ import annotations

import math
import os
import sys
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


H = 0.25
NL_PHYS = 6
PW = 3

SLIT_COORDS = [(-1, 0), (0, 0), (1, 0)]
SOURCE_STRENGTHS = (0.004,)
EPSILONS = (0.05,)

FIELD_EPS = 0.5
FIELD_MU = 0.08
FIELD_TARGET_MAX = 0.05
RELAX = 0.35
MAX_ITERS = 6
TOL = 1e-11


def _slit_nodes(lat: m.Lattice3D) -> list[int]:
    return [lat.nmap[(0, y, z)] for y, z in SLIT_COORDS]


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
    source_nodes: list[int],
) -> list[complex]:
    amps = [0j] * lat.n
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
                    amps[ld + di] += ai * complex(math.cos(m.K * act), math.sin(m.K * act)) * w / (L * L)
    return amps


def _detector_prob(amps: list[complex], lat: m.Lattice3D) -> float:
    det_start = lat.layer_start[lat.nl - 1]
    return sum(abs(amps[d]) ** 2 for d in range(det_start, det_start + lat.npl))


def _centroid_z(amps: list[complex], lat: m.Lattice3D) -> float:
    return m._centroid_z(amps, lat)


def _born_i3(field_layers: list[list[float]], lat: m.Lattice3D, slit_nodes: list[int]) -> float:
    det_start = lat.layer_start[lat.nl - 1]
    det_nodes = range(det_start, det_start + lat.npl)

    def det_prob(open_nodes: list[int]) -> float:
        amps = _propagate_from_sources(lat, field_layers, open_nodes)
        return sum(abs(amps[d]) ** 2 for d in det_nodes)

    a, b, c = slit_nodes
    pa = det_prob([a])
    pb = det_prob([b])
    pc = det_prob([c])
    pab = det_prob([a, b])
    pac = det_prob([a, c])
    pbc = det_prob([b, c])
    pabc = det_prob([a, b, c])
    i3 = pabc - pab - pac - pbc + pa + pb + pc
    return abs(i3) / pabc if pabc > 1e-30 else math.nan


def _iterate_loop(
    lat: m.Lattice3D,
    open_nodes: list[int],
    source_strength: float,
    epsilon: float,
    gain: float,
) -> tuple[list[list[float]], bool, int, float, list[complex]]:
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    weights = [1.0 / len(open_nodes)] * len(open_nodes)
    residual = float("inf")
    final_amps: list[complex] = [0j] * lat.n

    for iteration in range(1, MAX_ITERS + 1):
        final_amps = _propagate_from_sources(lat, field, open_nodes)
        density = [abs(final_amps[i]) ** 2 for i in open_nodes]
        weights_next = _normalize_weights(density)
        coupling = epsilon * source_strength
        raw_field = _poisson_like_field(lat, open_nodes, weights_next, coupling)
        field_next = [[gain * v for v in row] for row in raw_field]

        field_delta = max(
            abs(field_next[layer][idx] - field[layer][idx])
            for layer in range(lat.nl)
            for idx in range(lat.npl)
        )
        weight_delta = max(abs(a - b) for a, b in zip(weights_next, weights))
        residual = max(field_delta, weight_delta)

        if residual < TOL:
            return field_next, True, iteration, residual, final_amps

        field = [
            [
                (1.0 - RELAX) * field[layer][idx] + RELAX * field_next[layer][idx]
                for idx in range(lat.npl)
            ]
            for layer in range(lat.nl)
        ]
        weights = weights_next

    return field, False, MAX_ITERS, residual, final_amps


def main() -> None:
    lat = m.Lattice3D.build(NL_PHYS, PW, H)
    slit_nodes = _slit_nodes(lat)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free_slit_amps = _propagate_from_sources(lat, zero_field, slit_nodes)
    z_free = _centroid_z(free_slit_amps, lat)
    p_free = _detector_prob(free_slit_amps, lat)

    ref_raw = _poisson_like_field(
        lat,
        slit_nodes,
        [1.0 / len(slit_nodes)] * len(slit_nodes),
        max(SOURCE_STRENGTHS) * max(EPSILONS),
    )
    gain = FIELD_TARGET_MAX / _field_abs_max(ref_raw) if _field_abs_max(ref_raw) > 1e-30 else 1.0

    print("=" * 96)
    print("POISSON SELF-GRAVITY BORN AUDIT")
    print("  exact h=0.25 lattice, iterated amplitude-sourced backreaction loop")
    print("  audit target: per-step Born vs end-to-end Born through the full loop")
    print("=" * 96)
    print(f"h={H}, W={PW}, L={NL_PHYS}, slit_nodes={slit_nodes}")
    print(f"couplings={EPSILONS}, source strengths={SOURCE_STRENGTHS}")
    print(f"kernel=exp(-mu r)/(r+eps), mu={FIELD_MU:.2f}, eps={FIELD_EPS:.2f}")
    print(f"field gain={gain:.6e}, relax={RELAX:.2f}, max_iters={MAX_ITERS}")
    print()

    # Exact zero-coupling reduction.
    zero_field, zero_conv, zero_iters, zero_resid, zero_amps = _iterate_loop(
        lat, slit_nodes, max(SOURCE_STRENGTHS), 0.0, gain
    )
    zero_delta = _centroid_z(zero_amps, lat) - z_free
    zero_escape = _detector_prob(zero_amps, lat) / p_free if p_free > 1e-30 else math.nan
    zero_born = _born_i3(zero_field, lat, slit_nodes)

    print("REDUCTION CHECK")
    print(f"  zero-eps centroid shift: {zero_delta:+.6e}")
    print(f"  zero-eps escape ratio:   {zero_escape:.6f}")
    print(f"  zero-eps converged:      {zero_conv}")
    print(f"  zero-eps iters/resid:     {zero_iters} / {zero_resid:.3e}")
    print(f"  zero-eps Born (frozen):   {zero_born:.3e}")
    print()

    print(
        f"{'eps':>6s} {'s':>8s} {'stepBorn':>10s} {'endBorn':>10s} "
        f"{'stepConv':>8s} {'endConv':>8s} {'stepIters':>10s} {'endIters':>9s}"
    )
    print("-" * 92)

    for epsilon in EPSILONS:
        for source_strength in SOURCE_STRENGTHS:
            # Step-local Born: use the frozen field snapshot from the full abc loop.
            abc_field, step_conv, step_iters, step_resid, abc_amps = _iterate_loop(
                lat, slit_nodes, source_strength, epsilon, gain
            )
            step_born = _born_i3(abc_field, lat, slit_nodes)

            # End-to-end Born: run the full loop separately for each slit subset.
            subset_probs: dict[str, float] = {}
            subset_conv = {}
            subset_iters = {}
            for mask in (1, 2, 4, 3, 5, 6, 7):
                open_nodes = [slit_nodes[i] for i in range(3) if mask & (1 << i)]
                if not open_nodes:
                    subset_probs["empty"] = 0.0
                    continue
                field, converged, n_iter, resid, amps = _iterate_loop(
                    lat, open_nodes, source_strength, epsilon, gain
                )
                key = "".join(ch for ch, bit in zip("abc", (1, 2, 4)) if mask & bit)
                subset_probs[key] = _detector_prob(amps, lat)
                subset_conv[key] = converged
                subset_iters[key] = n_iter

            p_a = subset_probs["a"]
            p_b = subset_probs["b"]
            p_c = subset_probs["c"]
            p_ab = subset_probs["ab"]
            p_ac = subset_probs["ac"]
            p_bc = subset_probs["bc"]
            p_abc = subset_probs["abc"]
            end_i3 = abs(p_abc - p_ab - p_ac - p_bc + p_a + p_b + p_c) / p_abc if p_abc > 1e-30 else math.nan

            end_conv = all(subset_conv.values())
            end_iters = max(subset_iters.values()) if subset_iters else 0

            print(
                f"{epsilon:6.2f} {source_strength:8.4f} {step_born:10.3e} {end_i3:10.3e} "
                f"{str(step_conv):>8s} {str(end_conv):>8s} {step_iters:10d} {end_iters:9d}"
            )

    print()
    print("SAFE READ")
    print("  - exact eps = 0 reduction survives exactly")
    print("  - step-local Born is evaluated on a frozen field snapshot and is expected")
    print("    to remain machine-clean if the propagation step is linear")
    print("  - end-to-end Born is the real test of the nonlinear loop")
    print("  - if the end-to-end I3/P is also machine-clean, Born survives the full loop")
    print("  - if the end-to-end I3/P moves away from zero, Born survives only per-step")


if __name__ == "__main__":
    main()
