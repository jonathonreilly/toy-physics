#!/usr/bin/env python3
"""Gate B grown propagating-field v3.

This is a materially different follow-up to the closed memory, transport,
and beam-sourced grown-row propagating-field variants.

Goal:
  Test whether a self-consistent frontier-echo field on the retained grown row
  can produce a matched-null causal observable while reducing exactly back to
  the frozen grown baseline when the feedback coupling chi = 0.

Architecture:
  - retained grown geometry row only: drift=0.2, restore=0.7
  - one static source-resolved baseline field
  - one structural trap slab on the retained row
  - one matched-null control slab with the same cardinality but a frontier-
    shell placement
  - a self-consistent frontier-echo field driven by the signal-minus-control
    detector shell / phase observables
  - exact chi = 0 reduction to the frozen trap/control baseline

Observable:
  - matched detector escape shift
  - matched detector shell-contrast shift
  - matched detector phase-slope shift
  - weak-field mass-scaling exponent as a sanity check

The claim surface is intentionally narrow:
  if the frontier-echo field does not produce a coherent matched-null
  observable while keeping the exact chi = 0 reduction, the correct outcome is
  a bounded no-go for this more radical grown-row architecture.
"""

from __future__ import annotations

import cmath
import math
import random
import statistics
import time
from dataclasses import dataclass

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3
H = 0.5
NL = 25
PW = 8
DRIFT = 0.2
RESTORE = 0.7
SEEDS = list(range(4))
CHIS = [0.0, 0.05, 0.1, 0.2, 0.35, 0.5]
SOURCE_STRENGTHS = [1e-6, 1e-5, 5e-5]
Z_MASS = 3.0
FIELD_STRENGTH = 5e-5
FIELD_EPS = 0.1

TRAP_ETA = 0.35
TRAP_LAYERS = {NL // 2 - 1, NL // 2, NL // 2 + 1}
TRAP_RADIUS = 2.0
CONTROL_BAND = 1.5

FEEDBACK_TARGET_MAX = 0.08
FEEDBACK_WAVE_SPEED2 = 0.24
FEEDBACK_DAMP = 0.12
FEEDBACK_SELF = 0.64
FEEDBACK_RELAX = 0.65
FEEDBACK_REAL_GAIN = 1.0
FEEDBACK_IMAG_GAIN = 0.80
FEEDBACK_ESCAPE_GAIN = 0.35
FEEDBACK_PHASE_GAIN = 0.90
FEEDBACK_ITERATIONS = 3


@dataclass(frozen=True)
class GeomMetrics:
    escape_ratio: float
    delta_z: float
    shell_shift: float
    phase_slope: float
    phase_r2: float
    phase_span: float


@dataclass(frozen=True)
class SeedResult:
    seed: int
    signal: dict[float, GeomMetrics]
    control: dict[float, GeomMetrics]
    matched_escape_shift: dict[float, float]
    matched_delta_z_shift: dict[float, float]
    matched_shell_shift: dict[float, float]
    matched_phase_slope_shift: dict[float, float]
    matched_phase_span_shift: dict[float, float]
    residual: dict[float, float]
    fm_chi0: float | None
    fm_chi05: float | None
    exact_chi0: float


def _mean(values):
    return sum(values) / len(values) if values else math.nan


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


def grow(seed: int):
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(MAX_D_PHYS / H))
    pos: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = {}
    nmap: dict[tuple[int, int, int], int] = {}
    layers: list[list[int]] = []

    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    layers.append([0])

    for layer in range(1, NL):
        x = layer * H
        nodes: list[int] = []
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                if layer == 1:
                    y = iy * H
                    z = iz * H
                else:
                    prev = nmap.get((layer - 1, iy, iz))
                    if prev is None:
                        continue
                    _, py, pz = pos[prev]
                    y = py + rng.gauss(0.0, DRIFT * H)
                    z = pz + rng.gauss(0.0, DRIFT * H)
                    y = y * (1.0 - RESTORE) + (iy * H) * RESTORE
                    z = z * (1.0 - RESTORE) + (iz * H) * RESTORE
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx
                nodes.append(idx)
        layers.append(nodes)

        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer - 1, iy, iz))
                if si is None:
                    continue
                edges: list[int] = []
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            edges.append(di)
                adj[si] = adj.get(si, []) + edges

    return pos, adj, layers, nmap


def _static_field(pos, source_idx):
    mx, my, mz = pos[source_idx]
    field = [0.0] * len(pos)
    for i, (x, y, z) in enumerate(pos):
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + FIELD_EPS
        field[i] = FIELD_STRENGTH / r
    return field


def _layer_laplacian(values: list[complex], hw: int) -> list[complex]:
    grid_n = 2 * hw + 1
    out = [0j] * len(values)
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            k = (iy + hw) * grid_n + (iz + hw)
            center = values[k]
            total = 0j
            degree = 0
            for dy, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny = iy + dy
                nz = iz + dz
                if -hw <= ny <= hw and -hw <= nz <= hw:
                    nk = (ny + hw) * grid_n + (nz + hw)
                    total += values[nk]
                    degree += 1
            out[k] = total - degree * center
    return out


def _flatten_layers(layer_values: list[list[complex]], layers: list[list[int]], n: int) -> list[complex]:
    out = [0j] * n
    for layer_idx, layer_nodes in enumerate(layers):
        row = layer_values[layer_idx]
        for k, idx in enumerate(layer_nodes):
            out[idx] = row[k]
    return out


def _source_field_layers(pos, source_idx, source_strength):
    mx, my, mz = pos[source_idx]
    field = []
    for x, y, z in pos:
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + FIELD_EPS
        field.append(source_strength / r)
    return field


def _phase_ramp_metrics(pos, det, ref_amps, test_amps):
    z_vals = [pos[i][2] for i in det]
    ref_probs = [abs(ref_amps[i]) ** 2 for i in det]
    test_probs = [abs(test_amps[i]) ** 2 for i in det]
    peak = max(max(ref_probs), max(test_probs), 1e-30)
    use = [i for i, (pr, pt) in enumerate(zip(ref_probs, test_probs)) if max(pr, pt) >= 0.02 * peak]
    if len(use) < 3:
        use = [i for i, (pr, pt) in enumerate(zip(ref_probs, test_probs)) if max(pr, pt) >= 1e-4 * peak]
    if len(use) < 3:
        use = list(range(len(det)))

    diffs = []
    prev = None
    acc = 0.0
    for j in use:
        d = cmath.phase(test_amps[det[j]]) - cmath.phase(ref_amps[det[j]])
        while d <= -math.pi:
            d += 2.0 * math.pi
        while d > math.pi:
            d -= 2.0 * math.pi
        if prev is None:
            acc = d
        else:
            step = d - prev
            while step <= -math.pi:
                step += 2.0 * math.pi
            while step > math.pi:
                step -= 2.0 * math.pi
            acc += step
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


def _trap_masks(pos, layers):
    signal = set()
    for layer in TRAP_LAYERS:
        if layer < 0 or layer >= len(layers):
            continue
        for idx in layers[layer]:
            _, y, z = pos[idx]
            if math.sqrt(y * y + z * z) <= TRAP_RADIUS:
                signal.add(idx)

    target = len(signal)
    control_candidates: list[tuple[float, float, float, int]] = []
    for layer in TRAP_LAYERS:
        if layer < 0 or layer >= len(layers):
            continue
        for idx in layers[layer]:
            if idx in signal:
                continue
            _, y, z = pos[idx]
            r = math.sqrt(y * y + z * z)
            if r > TRAP_RADIUS:
                control_candidates.append((r, abs(z), abs(y), idx))

    control_candidates.sort()
    control = {idx for _, _, _, idx in control_candidates[:target]}
    if len(control) < target:
        # Rare fallback: broaden to any outer-node candidates on the trap layers.
        extras = []
        for layer in TRAP_LAYERS:
            if layer < 0 or layer >= len(layers):
                continue
            for idx in layers[layer]:
                if idx in signal or idx in control:
                    continue
                _, y, z = pos[idx]
                r = math.sqrt(y * y + z * z)
                extras.append((r, abs(z), abs(y), idx))
        extras.sort()
        for _, _, _, idx in extras:
            control.add(idx)
            if len(control) >= target:
                break

    return signal, control


def _detector_profiles(pos, det):
    ordered = sorted(det, key=lambda i: (abs(pos[i][2]), pos[i][1], i))
    q = max(1, len(ordered) // 4)
    inner = set(ordered[:q])
    outer = set(ordered[-q:])

    z_vals = [pos[i][2] for i in det]
    mz = sum(z_vals) / len(z_vals)
    span = max(max(z_vals) - mz, mz - min(z_vals), 1e-9)

    shell_profile = [0.0] * len(det)
    phase_profile = [0.0] * len(det)
    for k, idx in enumerate(det):
        if idx in inner:
            shell_profile[k] = -1.0
        elif idx in outer:
            shell_profile[k] = 1.0
        phase_profile[k] = (pos[idx][2] - mz) / span
    return shell_profile, phase_profile


def _detector_shell_contrast(amps, det, pos):
    ordered = sorted(det, key=lambda i: (abs(pos[i][2]), pos[i][1], i))
    q = max(1, len(ordered) // 4)
    inner = set(ordered[:q])
    outer = set(ordered[-q:])
    p_inner = sum(abs(amps[d]) ** 2 for d in inner)
    p_outer = sum(abs(amps[d]) ** 2 for d in outer)
    p_det = sum(abs(amps[d]) ** 2 for d in det)
    return (p_outer - p_inner) / p_det if p_det > 1e-30 else 0.0


def _measure_geom(amps, ref_amps, pos, det):
    p_test = sum(abs(amps[d]) ** 2 for d in det)
    p_ref = sum(abs(ref_amps[d]) ** 2 for d in det)
    z_test = sum(abs(amps[d]) ** 2 * pos[d][2] for d in det) / p_test if p_test > 1e-30 else 0.0
    z_ref = sum(abs(ref_amps[d]) ** 2 * pos[d][2] for d in det) / p_ref if p_ref > 1e-30 else 0.0
    shell_test = _detector_shell_contrast(amps, det, pos)
    shell_ref = _detector_shell_contrast(ref_amps, det, pos)
    slope, r2, span = _phase_ramp_metrics(pos, det, ref_amps, amps)
    return GeomMetrics(
        escape_ratio=p_test / p_ref if p_ref > 1e-30 else 0.0,
        delta_z=z_test - z_ref,
        shell_shift=shell_test - shell_ref,
        phase_slope=slope,
        phase_r2=r2,
        phase_span=span,
    )


def propagate(pos, adj, field, trap_mask):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H

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
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            act = L * (1.0 - lf.real)
            phase = FEEDBACK_IMAG_GAIN * lf.imag
            contrib = amps[i] * cmath.exp(1j * (K * act + phase)) * w * hm / (L * L)
            if j in trap_mask:
                contrib *= (1.0 - TRAP_ETA)
            amps[j] += contrib
    return amps


def _flatten_complex_layers(layer_values: list[list[complex]], layers, n: int) -> list[complex]:
    return _flatten_layers(layer_values, layers, n)


def _backward_frontier_echo(source_layers: list[list[complex]], hw: int) -> list[list[complex]]:
    nlayer = len(source_layers)
    if nlayer == 0:
        return []
    npl = len(source_layers[-1])
    echo = [[0j for _ in row] for row in source_layers]
    echo[-1] = [complex(v) for v in source_layers[-1]]
    if nlayer > 1:
        echo[-2] = [FEEDBACK_SELF * v for v in echo[-1]]
    if nlayer > 2:
        for layer_idx in reversed(range(1, nlayer - 2)):
            lap = _layer_laplacian(echo[layer_idx + 1], hw)
            prev = echo[layer_idx + 2]
            echo[layer_idx] = [
                (2.0 - FEEDBACK_DAMP) * echo[layer_idx + 1][k]
                - (1.0 - FEEDBACK_DAMP) * prev[k]
                + FEEDBACK_WAVE_SPEED2 * lap[k]
                for k in range(npl)
            ]
    if nlayer == 1:
        return echo
    echo[0] = [sum(echo[1]) / len(echo[1]) if echo[1] else 0j]
    return echo


def _normalize_field_layers(layer_values: list[list[complex]]) -> list[list[complex]]:
    mx = max((abs(v) for row in layer_values for v in row), default=0.0)
    if mx < 1e-30:
        return [[0j for _ in row] for row in layer_values]
    return [[v / mx for v in row] for row in layer_values]


def _build_frontier_source(
    det: list[int],
    pos,
    matched_shell_shift: float,
    matched_phase_shift: float,
    matched_escape_shift: float,
):
    shell_profile, phase_profile = _detector_profiles(pos, det)
    source_layer = []
    for k in range(len(det)):
        real_drive = (
            FEEDBACK_REAL_GAIN * matched_shell_shift * shell_profile[k]
            + FEEDBACK_ESCAPE_GAIN * matched_escape_shift * shell_profile[k]
        )
        imag_drive = FEEDBACK_PHASE_GAIN * matched_phase_shift * phase_profile[k]
        source_layer.append(complex(real_drive, imag_drive))
    return source_layer


def _field_from_frontier_deltas(
    pos,
    layers,
    det,
    chi: float,
    matched_shell_shift: float,
    matched_phase_shift: float,
    matched_escape_shift: float,
    base_field: list[complex],
):
    if chi <= 0.0:
        return [complex(v) for v in base_field], 0.0

    hw = int(PW / H)
    source_layer = _build_frontier_source(
        det,
        pos,
        matched_shell_shift,
        matched_phase_shift,
        matched_escape_shift,
    )
    source_layers = [[0j for _ in layer_nodes] for layer_nodes in layers]
    source_layers[-1] = source_layer
    echo_layers = _backward_frontier_echo(source_layers, hw)
    echo_layers = _normalize_field_layers(echo_layers)
    echo = _flatten_complex_layers(echo_layers, layers, len(pos))

    field = [complex(v) for v in base_field]
    residual = 0.0
    for _ in range(FEEDBACK_ITERATIONS):
        target = [
            field[i] + chi * FEEDBACK_TARGET_MAX * echo[i]
            for i in range(len(field))
        ]
        diff = sum(abs(target[i] - field[i]) for i in range(len(field))) / max(1, len(field))
        field = [
            (1.0 - FEEDBACK_RELAX) * field[i] + FEEDBACK_RELAX * target[i]
            for i in range(len(field))
        ]
        residual = diff
    return field, residual


def _solve_frontier_feedback(
    pos,
    adj,
    layers,
    det,
    signal_mask,
    control_mask,
    base_field: list[complex],
    sig_ref_amps,
    ctrl_ref_amps,
    chi: float,
):
    if chi <= 0.0:
        sig_amps = propagate(pos, adj, base_field, signal_mask)
        ctrl_amps = propagate(pos, adj, base_field, control_mask)
        sig = _measure_geom(sig_amps, sig_ref_amps, pos, det)
        ctrl = _measure_geom(ctrl_amps, ctrl_ref_amps, pos, det)
        return (
            [complex(v) for v in base_field],
            0.0,
            sig,
            ctrl,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        )

    field = [complex(v) for v in base_field]
    residual = 0.0
    sig = _measure_geom(propagate(pos, adj, field, signal_mask), sig_ref_amps, pos, det)
    ctrl = _measure_geom(propagate(pos, adj, field, control_mask), ctrl_ref_amps, pos, det)
    m_escape = m_delta_z = m_shell = m_phase = m_span = 0.0
    for _ in range(FEEDBACK_ITERATIONS):
        sig_amps = propagate(pos, adj, field, signal_mask)
        ctrl_amps = propagate(pos, adj, field, control_mask)
        sig = _measure_geom(sig_amps, sig_ref_amps, pos, det)
        ctrl = _measure_geom(ctrl_amps, ctrl_ref_amps, pos, det)
        m_shell = (sig.shell_shift - ctrl.shell_shift)
        m_phase = (sig.phase_slope - ctrl.phase_slope)
        m_escape = ((sig.escape_ratio - 1.0) - (ctrl.escape_ratio - 1.0))
        m_delta_z = sig.delta_z - ctrl.delta_z
        m_span = sig.phase_span - ctrl.phase_span

        target_field, residual = _field_from_frontier_deltas(
            pos,
            layers,
            det,
            chi,
            m_shell,
            m_phase,
            m_escape,
            base_field,
        )
        field = [
            (1.0 - FEEDBACK_RELAX) * field[i] + FEEDBACK_RELAX * target_field[i]
            for i in range(len(field))
        ]

    sig_amps = propagate(pos, adj, field, signal_mask)
    ctrl_amps = propagate(pos, adj, field, control_mask)
    sig = _measure_geom(sig_amps, sig_ref_amps, pos, det)
    ctrl = _measure_geom(ctrl_amps, ctrl_ref_amps, pos, det)
    m_shell = (sig.shell_shift - ctrl.shell_shift)
    m_phase = (sig.phase_slope - ctrl.phase_slope)
    m_escape = ((sig.escape_ratio - 1.0) - (ctrl.escape_ratio - 1.0))
    m_delta_z = sig.delta_z - ctrl.delta_z
    m_span = sig.phase_span - ctrl.phase_span
    return field, residual, sig, ctrl, m_escape, m_delta_z, m_shell, m_phase, m_span


def _run_seed(seed: int):
    pos, adj, layers, nmap = grow(seed)
    det = layers[-1]
    signal_mask, control_mask = _trap_masks(pos, layers)

    gl = 2 * NL // 3
    source_idx = min(
        layers[gl],
        key=lambda i: (pos[i][1]) ** 2 + (pos[i][2] - Z_MASS) ** 2,
    )

    raw_base = _source_field_layers(pos, source_idx, FIELD_STRENGTH)
    ref_max = max(abs(v) for v in raw_base) if raw_base else 0.0
    gain = FEEDBACK_TARGET_MAX / ref_max if ref_max > 1e-30 else 1.0
    base_field = [complex(gain * v, 0.0) for v in raw_base]

    sig_ref_amps = propagate(pos, adj, base_field, signal_mask)
    ctrl_ref_amps = propagate(pos, adj, base_field, control_mask)

    sig_ref = _measure_geom(sig_ref_amps, sig_ref_amps, pos, det)
    ctrl_ref = _measure_geom(ctrl_ref_amps, ctrl_ref_amps, pos, det)

    signal: dict[float, GeomMetrics] = {}
    control: dict[float, GeomMetrics] = {}
    matched_escape_shift: dict[float, float] = {}
    matched_delta_z_shift: dict[float, float] = {}
    matched_shell_shift: dict[float, float] = {}
    matched_phase_slope_shift: dict[float, float] = {}
    matched_phase_span_shift: dict[float, float] = {}
    residual: dict[float, float] = {}

    signal[0.0] = sig_ref
    control[0.0] = ctrl_ref
    matched_escape_shift[0.0] = 0.0
    matched_delta_z_shift[0.0] = 0.0
    matched_shell_shift[0.0] = 0.0
    matched_phase_slope_shift[0.0] = 0.0
    matched_phase_span_shift[0.0] = 0.0
    residual[0.0] = 0.0

    for chi in CHIS[1:]:
        field, step_residual, sig, ctrl, m_escape, m_delta_z, m_shell, m_phase, m_span = _solve_frontier_feedback(
            pos,
            adj,
            layers,
            det,
            signal_mask,
            control_mask,
            base_field,
            sig_ref_amps,
            ctrl_ref_amps,
            chi,
        )

        signal[chi] = sig
        control[chi] = ctrl
        matched_escape_shift[chi] = m_escape
        matched_delta_z_shift[chi] = m_delta_z
        matched_shell_shift[chi] = m_shell
        matched_phase_slope_shift[chi] = m_phase
        matched_phase_span_shift[chi] = m_span
        residual[chi] = step_residual

    fm = {0.0: None, 0.5: None}
    for chi in fm:
        deltas = []
        strengths = []
        for s in SOURCE_STRENGTHS:
            raw = _source_field_layers(pos, source_idx, s)
            gain_s = FEEDBACK_TARGET_MAX / max((abs(v) for v in raw), default=1e-30)
            base_s = [complex(gain_s * v, 0.0) for v in raw]
            sig_ref_s = propagate(pos, adj, base_s, signal_mask)
            ctrl_ref_s = propagate(pos, adj, base_s, control_mask)
            sig_amps, _, _, _, _, _, _, _, _ = _solve_frontier_feedback(
                pos,
                adj,
                layers,
                det,
                signal_mask,
                control_mask,
                base_s,
                sig_ref_s,
                ctrl_ref_s,
                chi,
            )
            sig_amps = propagate(pos, adj, sig_amps, signal_mask)
            sig_delta = _measure_geom(sig_amps, sig_ref_s, pos, det).delta_z
            deltas.append(abs(sig_delta))
            strengths.append(s)
        fm[chi] = _fit_power(strengths, deltas)

    return SeedResult(
        seed=seed,
        signal=signal,
        control=control,
        matched_escape_shift=matched_escape_shift,
        matched_delta_z_shift=matched_delta_z_shift,
        matched_shell_shift=matched_shell_shift,
        matched_phase_slope_shift=matched_phase_slope_shift,
        matched_phase_span_shift=matched_phase_span_shift,
        residual=residual,
        fm_chi0=fm[0.0],
        fm_chi05=fm[0.5],
        exact_chi0=signal[0.0].escape_ratio,
    )


def main() -> None:
    t0 = time.time()
    print("=" * 112)
    print("GATE B GROWN PROPAGATING FIELD V3")
    print("  retained grown row, frontier-echo self-consistent field")
    print("  comparison: chi=0 matched-null baseline vs chi-activated feedback field")
    print("  structural null: signal trap slab vs matched frontier-shell control slab")
    print("=" * 112)
    print(f"row: drift={DRIFT}, restore={RESTORE}, seeds={SEEDS}")
    print(f"source z = {Z_MASS}, field strength = {FIELD_STRENGTH:.1e}, field eps = {FIELD_EPS}")
    print(f"trap eta = {TRAP_ETA}, trap layers = {sorted(TRAP_LAYERS)}, trap radius = {TRAP_RADIUS}")
    print(f"control band = {CONTROL_BAND}, chi sweep = {CHIS}")
    print(
        "frontier-echo constants: "
        f"target_max={FEEDBACK_TARGET_MAX}, wave_speed2={FEEDBACK_WAVE_SPEED2}, "
        f"damp={FEEDBACK_DAMP}, self={FEEDBACK_SELF}, relax={FEEDBACK_RELAX}, "
        f"real_gain={FEEDBACK_REAL_GAIN}, imag_gain={FEEDBACK_IMAG_GAIN}, "
        f"escape_gain={FEEDBACK_ESCAPE_GAIN}, phase_gain={FEEDBACK_PHASE_GAIN}"
    )
    print()

    rows: list[SeedResult] = []
    for seed in SEEDS:
        rows.append(_run_seed(seed))

    print("REDUCTION CHECK")
    print("  chi=0 reproduces the retained trap/control baseline exactly by construction")
    print("  all matched shifts vanish at chi=0")
    print()

    header = [
        "seed",
        "sigEsc(0.50)",
        "ctrlEsc(0.50)",
        "mEsc(0.50)",
        "mShell(0.50)",
        "mPhase(0.50)",
        "resid(0.50)",
        "F~M(0.0)",
        "F~M(0.5)",
    ]
    print(" ".join(f"{h:>15s}" for h in header))
    print("-" * 160)
    for row in rows:
        vals = [
            f"{row.seed:15d}",
            f"{row.signal[0.50].escape_ratio:15.3f}",
            f"{row.control[0.50].escape_ratio:15.3f}",
            f"{row.matched_escape_shift[0.50]:15.3f}",
            f"{row.matched_shell_shift[0.50]:15.4f}",
            f"{row.matched_phase_slope_shift[0.50]:15.4f}",
            f"{row.residual[0.50]:15.3e}",
            f"{row.fm_chi0:15.2f}" if row.fm_chi0 is not None else f"{'n/a':>15s}",
            f"{row.fm_chi05:15.2f}" if row.fm_chi05 is not None else f"{'n/a':>15s}",
        ]
        print(" ".join(vals))

    print()
    print("AGGREGATE")
    for chi in CHIS:
        sig = [r.signal[chi] for r in rows]
        ctrl = [r.control[chi] for r in rows]
        esc = [r.matched_escape_shift[chi] for r in rows]
        dz = [r.matched_delta_z_shift[chi] for r in rows]
        shell = [r.matched_shell_shift[chi] for r in rows]
        phase = [r.matched_phase_slope_shift[chi] for r in rows]
        span = [r.matched_phase_span_shift[chi] for r in rows]
        resid = [r.residual[chi] for r in rows]
        print(
            f"  chi={chi:>4.2f} "
            f"sigEsc={_mean([x.escape_ratio for x in sig]):.3f} "
            f"ctrlEsc={_mean([x.escape_ratio for x in ctrl]):.3f} "
            f"mEsc={_mean(esc):+.3f} "
            f"mZ={_mean(dz):+.6e} "
            f"mShell={_mean(shell):+.4f} "
            f"mPhase={_mean(phase):+.4f} "
            f"mSpan={_mean(span):+.4f} "
            f"resid={_mean(resid):.3e}"
        )

    fm0 = [r.fm_chi0 for r in rows if r.fm_chi0 is not None]
    fm05 = [r.fm_chi05 for r in rows if r.fm_chi05 is not None]
    print()
    print("WEAK-FIELD SANITY")
    print(
        f"  F~M exponent at chi=0: {statistics.mean(fm0):.3f}"
        if fm0
        else "  F~M exponent at chi=0: n/a"
    )
    print(
        f"  F~M exponent at chi=0.5: {statistics.mean(fm05):.3f}"
        if fm05
        else "  F~M exponent at chi=0.5: n/a"
    )

    print()
    print("SAFE READ")
    print("  chi=0 is an exact matched-null reduction to the retained trap/control baseline")
    print("  the promoted observables are the matched shell and phase shifts, not raw escape alone")
    print("  if the matched-null shifts stay small while residuals stay small, this remains a bounded no-go")
    print(f"\nTotal time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
