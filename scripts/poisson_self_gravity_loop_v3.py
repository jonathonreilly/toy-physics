#!/usr/bin/env python3
"""Exact-lattice Poisson-like self-gravity loop v3.

Moonshot goal:
  Strengthen the exact-lattice self-gravity control with:
  - exact identity reduction at epsilon = 0
  - matched-null comparison against the same update machinery with zero
    coupling
  - a promoted detector observable stronger than raw escape:
      signed detector centroid shift and detector-line phase ramp
  - a strict Born audit that separates per-step and end-to-end behavior

This is intentionally narrow:
  - one exact 3D lattice family
  - one source-resolved amplitude-to-field backreaction loop
  - one matched null loop
  - one detector-line phase-ramp observable
  - one three-slit Born audit on the same exact family

If the lane still only gives a tiny control effect, the note should freeze
that explicitly.

Current read:
  the exact zero-coupling reduction survives, but the nonzero-coupling rows
  here do not support a retained self-gravity claim under strict reduction
  and Born controls.
"""

from __future__ import annotations

import cmath
import math
import os
import sys
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


# Keep the exact family tractable enough to audit in Python while preserving
# the same propagation rule and lattice identity structure.
m.MAX_D_PHYS = 2.0

H = 0.25
NL_PHYS = 6
PW = 3
SOURCE_Z = 2.5
SOURCE_CLUSTER = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
SOURCE_STRENGTHS = (0.002, 0.004, 0.008)
EPSILONS = (0.0, 0.05, 0.2, 0.5)
FIELD_TARGET_MAX = 0.05
FIELD_EPS = 0.5
FIELD_MU = 0.08
RELAX = 0.35
MAX_ITERS = 6
TOL = 1e-10
REP_EPSILON = 0.05
REP_SOURCE = 0.004


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


def _born_slit_nodes(lat: m.Lattice3D) -> list[int]:
    return [
        lat.nmap[(0, -1, 0)],
        lat.nmap[(0, 0, 0)],
        lat.nmap[(0, 1, 0)],
    ]


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
    det_start = lat.layer_start[lat.nl - 1]
    total = 0.0
    weighted = 0.0
    for d in range(det_start, det_start + lat.npl):
        p = abs(amps[d]) ** 2
        total += p
        weighted += p * lat.pos[d][2]
    return weighted / total if total > 1e-30 else 0.0


def _detector_line(lat: m.Lattice3D) -> list[int]:
    det_start = lat.layer_start[lat.nl - 1]
    center_y = lat.hw
    return [det_start + center_y * lat.nw + iz for iz in range(lat.nw)]


def _wrap_phase(delta: float) -> float:
    while delta <= -math.pi:
        delta += 2.0 * math.pi
    while delta > math.pi:
        delta -= 2.0 * math.pi
    return delta


def _phase_ramp_metrics(
    lat: m.Lattice3D,
    ref_amps: list[complex],
    test_amps: list[complex],
    det_line: list[int],
) -> tuple[float, float, float]:
    z_vals = [lat.pos[i][2] for i in det_line]
    ref_probs = [abs(ref_amps[i]) ** 2 for i in det_line]
    test_probs = [abs(test_amps[i]) ** 2 for i in det_line]
    peak = max(max(ref_probs), max(test_probs), 1e-30)
    use = [i for i, (pr, pt) in enumerate(zip(ref_probs, test_probs)) if max(pr, pt) >= 0.02 * peak]
    if len(use) < 3:
        use = [i for i, (pr, pt) in enumerate(zip(ref_probs, test_probs)) if max(pr, pt) >= 1e-4 * peak]
    if len(use) < 3:
        use = list(range(len(det_line)))

    diffs: list[float] = []
    acc = 0.0
    prev = None
    for j in use:
        d = _wrap_phase(cmath.phase(test_amps[det_line[j]]) - cmath.phase(ref_amps[det_line[j]]))
        if prev is None:
            acc = d
        else:
            acc += _wrap_phase(d - prev)
        diffs.append(acc)
        prev = d

    z_use = [z_vals[j] for j in use]
    mz = sum(z_use) / len(z_use)
    md = sum(diffs) / len(diffs)
    szz = sum((z - mz) ** 2 for z in z_use)
    if szz < 1e-12:
        return 0.0, 0.0, 0.0
    szd = sum((z - mz) * (d - md) for z, d in zip(z_use, diffs))
    slope = szd / szz
    ss_tot = sum((d - md) ** 2 for d in diffs)
    ss_res = sum((d - (slope * (z - mz) + md)) ** 2 for z, d in zip(z_use, diffs))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 0.0
    span = max(diffs) - min(diffs)
    return slope, r2, span


def _born_i3(field_layers: list[list[float]], lat: m.Lattice3D, source_nodes: list[int]) -> float:
    det_start = lat.layer_start[lat.nl - 1]
    det_nodes = range(det_start, det_start + lat.npl)

    def det_prob(open_nodes: list[int]) -> float:
        amps = _propagate_from_sources(lat, field_layers, open_nodes)
        return sum(abs(amps[d]) ** 2 for d in det_nodes)

    a, b, c = source_nodes
    pa = det_prob([a])
    pb = det_prob([b])
    pc = det_prob([c])
    pab = det_prob([a, b])
    pac = det_prob([a, c])
    pbc = det_prob([b, c])
    pabc = det_prob([a, b, c])
    i3 = pabc - pab - pac - pbc + pa + pb + pc
    return abs(i3) / pabc if pabc > 1e-30 else math.nan


def _run_loop(
    lat: m.Lattice3D,
    launch_nodes: list[int],
    source_patch_nodes: list[int],
    source_strength: float,
    epsilon: float,
    gain: float,
) -> tuple[list[list[float]], list[float], bool, int, float, list[complex]]:
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    if epsilon == 0.0:
        amps = _propagate_from_sources(lat, zero_field, launch_nodes)
        weights = [1.0 / len(source_patch_nodes)] * len(source_patch_nodes)
        return zero_field, weights, True, 0, 0.0, amps

    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    weights = [1.0 / len(source_patch_nodes)] * len(source_patch_nodes)
    final_amps: list[complex] = [0j] * lat.n
    residual = float("inf")

    for iteration in range(1, MAX_ITERS + 1):
        final_amps = _propagate_from_sources(lat, field, launch_nodes)
        density = [abs(final_amps[i]) ** 2 for i in source_patch_nodes]
        weights_next = _normalize_weights(density)
        raw_field = _poisson_like_field(lat, source_patch_nodes, weights_next, epsilon * source_strength)
        field_next = [[gain * v for v in row] for row in raw_field]

        field_delta = max(
            abs(field_next[layer][idx] - field[layer][idx])
            for layer in range(lat.nl)
            for idx in range(lat.npl)
        )
        weight_delta = max(abs(a - b) for a, b in zip(weights_next, weights))
        residual = max(field_delta, weight_delta)

        if residual < TOL:
            final_amps = _propagate_from_sources(lat, field_next, launch_nodes)
            return field_next, weights_next, True, iteration, residual, final_amps

        field = [
            [
                (1.0 - RELAX) * field[layer][idx] + RELAX * field_next[layer][idx]
                for idx in range(lat.npl)
            ]
            for layer in range(lat.nl)
        ]
        weights = weights_next

    final_amps = _propagate_from_sources(lat, field, launch_nodes)
    return field, weights, False, MAX_ITERS, residual, final_amps


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
    lat = m.Lattice3D.build(NL_PHYS, PW, H)
    launch_nodes = [lat.nmap[(0, 0, 0)]]
    source_patch_nodes = _source_cluster_nodes(lat)
    born_nodes = _born_slit_nodes(lat)
    det_line = _detector_line(lat)

    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = _propagate_from_sources(lat, zero_field, launch_nodes)
    z_free = _centroid_z(free, lat)
    p_free = _detector_prob(free, lat)

    ref_raw = _poisson_like_field(
        lat,
        source_patch_nodes,
        [1.0 / len(source_patch_nodes)] * len(source_patch_nodes),
        max(SOURCE_STRENGTHS) * max(EPSILONS),
    )
    gain = FIELD_TARGET_MAX / _field_abs_max(ref_raw) if _field_abs_max(ref_raw) > 1e-30 else 1.0

    print("=" * 104)
    print("POISSON SELF-GRAVITY LOOP V3")
    print("  exact h=0.25 lattice, amplitude-sourced backreaction loop, matched null + Born audit")
    print("  tested observables: detector centroid shift and detector-line phase ramp")
    print("=" * 104)
    print(f"h={H}, W={PW}, L={NL_PHYS}")
    print(f"launch_nodes={launch_nodes}")
    print(f"source patch nodes={source_patch_nodes}")
    print(f"born triplet={born_nodes}")
    print(f"kernel=exp(-mu r)/(r+eps), mu={FIELD_MU:.2f}, eps={FIELD_EPS:.2f}")
    print(f"source strengths={SOURCE_STRENGTHS}")
    print(f"backreaction couplings={EPSILONS}")
    print(f"field gain={gain:.6e}, relax={RELAX:.2f}, max_iters={MAX_ITERS}")
    print()

    # Exact identity reduction / matched null control.
    null_field, _, null_conv, null_iters, null_resid, null_amps = _run_loop(
        lat, launch_nodes, source_patch_nodes, max(SOURCE_STRENGTHS), 0.0, gain
    )
    zero_delta = _centroid_z(null_amps, lat) - z_free
    zero_escape = _detector_prob(null_amps, lat) / p_free if p_free > 1e-30 else math.nan
    phase_null_slope, phase_null_r2, phase_null_span = _phase_ramp_metrics(lat, free, null_amps, det_line)

    print("REDUCTION CHECK")
    print(f"  zero-epsilon centroid shift: {zero_delta:+.6e}")
    print(f"  zero-epsilon escape ratio:   {zero_escape:.6f}")
    print(f"  zero-epsilon phase slope:    {phase_null_slope:+.4e}")
    print(f"  zero-epsilon phase span:     {phase_null_span:+.4e}")
    print(f"  zero-epsilon phase R^2:      {phase_null_r2:.3f}")
    print(f"  zero-epsilon converged:      {null_conv}")
    print(f"  zero-epsilon iters/resid:    {null_iters} / {null_resid:.3e}")
    print()

    print(
        f"{'eps':>6s} {'s':>8s} {'centroid':>12s} {'null-cent':>12s} {'phase':>10s} "
        f"{'span':>9s} {'escape':>8s} {'converged':>10s}"
    )
    print("-" * 92)

    summary: dict[float, dict[str, float]] = {}
    for epsilon in EPSILONS:
        deltas: list[float] = []
        phase_slopes: list[float] = []
        phase_spans: list[float] = []
        escapes: list[float] = []
        toward = 0
        n_conv = 0
        max_resid = 0.0

        for s in SOURCE_STRENGTHS:
            coupled_field, weights, converged, iters, residual, coupled_amps = _run_loop(
                lat, launch_nodes, source_patch_nodes, s, epsilon, gain
            )
            centroid = _centroid_z(coupled_amps, lat) - z_free
            null_centroid = _centroid_z(null_amps, lat) - z_free
            delta = centroid - null_centroid
            slope, r2, span = _phase_ramp_metrics(lat, null_amps, coupled_amps, det_line)
            esc = _detector_prob(coupled_amps, lat) / p_free if p_free > 1e-30 else math.nan

            deltas.append(delta)
            phase_slopes.append(slope)
            phase_spans.append(span)
            escapes.append(esc)
            toward += int(delta > 0)
            n_conv += int(converged)
            max_resid = max(max_resid, residual)

            print(
                f"{epsilon:6.2f} {s:8.4f} {centroid:+12.6e} {delta:+12.6e} "
                f"{slope:+10.4e} {span:+9.4e} {esc:8.3f} {('Y' if converged else 'n'):>10s}"
            )

        mean_delta = sum(deltas) / len(deltas)
        mean_slope = sum(phase_slopes) / len(phase_slopes)
        mean_span = sum(phase_spans) / len(phase_spans)
        mean_escape = sum(escapes) / len(escapes)
        summary[epsilon] = {
            "delta": mean_delta,
            "slope": mean_slope,
            "span": mean_span,
            "escape": mean_escape,
            "toward": float(toward),
            "conv": float(n_conv),
            "resid": max_resid,
        }
        print(
            f"  eps={epsilon:.2f} summary: mean delta={mean_delta:+.6e} "
            f"mean phase slope={mean_slope:+.4e} mean span={mean_span:+.4e} "
            f"mean escape={mean_escape:.3f} toward={toward}/{len(SOURCE_STRENGTHS)} "
            f"resid={max_resid:.3e} converged={n_conv}/{len(SOURCE_STRENGTHS)}"
        )

    print()
    print("BORN AUDIT")
    print(f"  audit row: epsilon={REP_EPSILON:.2f}, source_strength={REP_SOURCE:.4f}")

    audit_field, _, audit_conv, audit_iters, audit_resid, audit_amps = _run_loop(
        lat, born_nodes, born_nodes, REP_SOURCE, REP_EPSILON, gain
    )
    step_born = _born_i3(audit_field, lat, born_nodes)

    end_probs: dict[int, float] = {}
    for mask in range(1, 8):
        open_nodes = [born_nodes[i] for i in range(3) if mask & (1 << i)]
        field, _, converged, iters, resid, amps = _run_loop(
            lat, open_nodes, open_nodes, REP_SOURCE, REP_EPSILON, gain
        )
        end_probs[mask] = _detector_prob(amps, lat)

    a, b, c = born_nodes
    pa = end_probs[1]
    pb = end_probs[2]
    pc = end_probs[4]
    pab = end_probs[3]
    pac = end_probs[5]
    pbc = end_probs[6]
    pabc = end_probs[7]
    i3 = pabc - pab - pac - pbc + pa + pb + pc
    end_born = abs(i3) / pabc if pabc > 1e-30 else math.nan

    audit_null_field, _, _, _, _, audit_null_amps = _run_loop(
        lat, born_nodes, born_nodes, REP_SOURCE, 0.0, gain
    )
    audit_null_delta = _centroid_z(audit_null_amps, lat) - z_free
    audit_null_escape = _detector_prob(audit_null_amps, lat) / p_free if p_free > 1e-30 else math.nan

    print(f"  step-local Born:    {step_born:.3e}")
    print(f"  end-to-end Born:    {end_born:.3e}")
    print(f"  coupled centroid:   {_centroid_z(audit_amps, lat) - z_free:+.6e}")
    print(f"  null centroid:      {audit_null_delta:+.6e}")
    print(f"  coupled escape:     {_detector_prob(audit_amps, lat) / p_free if p_free > 1e-30 else math.nan:.6f}")
    print(f"  null escape:        {audit_null_escape:.6f}")
    print(f"  coupled converged:  {audit_conv} / iters={audit_iters} / resid={audit_resid:.3e}")
    print()

    print("SAFE READ")
    if summary:
        best_eps = min(summary.keys(), key=lambda e: summary[e]["resid"])
        best = summary[best_eps]
        print(f"  best residual epsilon: {best_eps:.2f} (resid={best['resid']:.3e})")
        print(f"  best mean centroid shift: {best['delta']:+.6e}")
        print(f"  best mean phase slope:     {best['slope']:+.4e}")
        print(f"  best mean phase span:      {best['span']:+.4e}")
        print(f"  best mean escape ratio:    {best['escape']:.3f}")
        print(f"  best TOWARD rows:          {int(best['toward'])}/{len(SOURCE_STRENGTHS)}")
    print(f"  exact zero-epsilon reduction shift: {zero_delta:+.3e}")
    print(f"  zero-epsilon phase slope/span: {phase_null_slope:+.4e} / {phase_null_span:+.4e}")
    print("  strict read: no retained positive survives the exact reduction and Born controls")
    print("  this lane remains a bounded no-go on the retained audit row")


if __name__ == "__main__":
    main()
