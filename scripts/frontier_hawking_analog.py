#!/usr/bin/env python3
"""Thermal spectrum test on detector wavefunction in a discrete DAG.

NOTE: This is NOT a true Hawking radiation test. The field does not trap
amplitude (detector probability INCREASES with field strength), so the
setup does not produce "escaped radiation from a trapping region."

What this script DOES test: whether the Fourier power spectrum of the
detector wavefunction has a thermal (Boltzmann-like) shape, and whether
the fitted temperature scales with field strength.

Hypothesis:
    The Fourier spectrum |psi_k|^2 satisfies ln(|psi_k|^2) = a - b*k^2
    (R^2 > 0.9 => thermal shape), and T ~ 1/(2b) scales as 1/M.

Falsification:
    If R^2 < 0.5 for the thermal fit, the spectrum is not thermal-shaped.
    If T is constant across field strengths, Hawking scaling is falsified.

Infrastructure:
    Uses the 2D rectangular DAG propagator from toy_event_physics.py.
    A cluster of persistent nodes at the graph center generates a
    gravitational field via Laplacian relaxation.  Amplitude is propagated
    from the left boundary to the right boundary (detector).
"""

from __future__ import annotations

import cmath
import math
import sys
import time

sys.path.insert(
    0, "/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf"
)

from toy_event_physics import (
    RulePostulates,
    build_causal_dag,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
    local_edge_properties,
)


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

WIDTH = 20
HEIGHT = 10
SOURCE = (0, 0)
PHASE_K = 6.0
ATTENUATION_POWER = 0.5

FIELD_STRENGTHS = [1e-4, 5e-4, 1e-3, 5e-3, 1e-2]

# Mass cluster: a block of persistent nodes near center of graph
MASS_CENTER_X = 10
MASS_CENTER_Y = 0
MASS_RADIUS = 2  # Chebyshev radius of the cluster


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_mass_cluster(
    cx: int, cy: int, radius: int, nodes: set[tuple[int, int]]
) -> frozenset[tuple[int, int]]:
    """Build a square cluster of persistent nodes within the graph."""
    cluster = set()
    for x in range(cx - radius, cx + radius + 1):
        for y in range(cy - radius, cy + radius + 1):
            if (x, y) in nodes:
                cluster.add((x, y))
    return frozenset(cluster)


def propagate_amplitude(
    dag: dict[tuple[int, int], list[tuple[int, int]]],
    source: tuple[int, int],
    rule,
    node_field: dict[tuple[int, int], float],
) -> dict[tuple[int, int], complex]:
    """Sum-over-paths amplitude propagation on a causal DAG.

    Each node accumulates the sum of amplitudes arriving along all
    causal edges.  The amplitude along each edge picks up a phase
    from the action and an attenuation factor.
    """
    psi: dict[tuple[int, int], complex] = {source: 1.0 + 0j}

    # Topological order: sort by arrival time (encoded in DAG structure).
    # Since `dag` is built from arrival times, a BFS from source gives
    # a valid topological order.
    from collections import deque

    visited_order: list[tuple[int, int]] = []
    visited: set[tuple[int, int]] = set()
    queue = deque([source])
    visited.add(source)
    while queue:
        node = queue.popleft()
        visited_order.append(node)
        for child in dag.get(node, []):
            if child not in visited:
                visited.add(child)
                queue.append(child)

    # Propagate in topological order
    for node in visited_order:
        amp = psi.get(node, 0j)
        if amp == 0j:
            continue
        for child in dag.get(node, []):
            _delay, _action, edge_amp = local_edge_properties(
                node, child, rule, node_field
            )
            psi[child] = psi.get(child, 0j) + amp * edge_amp

    return psi


def extract_detector_amplitudes(
    psi: dict[tuple[int, int], complex],
    detector_x: int,
    height: int,
) -> list[tuple[int, complex]]:
    """Extract amplitudes at the detector boundary x = detector_x."""
    result = []
    for y in range(-height, height + 1):
        node = (detector_x, y)
        if node in psi:
            result.append((y, psi[node]))
    return result


def discrete_fourier_transform(
    amplitudes: list[tuple[int, complex]],
) -> list[tuple[int, complex]]:
    """Compute DFT of the detector wavefunction.

    Returns (k_index, psi_k) pairs for integer k from 0 to N-1.
    """
    # Extract just the complex values, ordered by y
    ys = [y for y, _ in amplitudes]
    vals = [a for _, a in amplitudes]
    n = len(vals)
    if n == 0:
        return []

    result = []
    for k in range(n):
        psi_k = 0j
        for j in range(n):
            psi_k += vals[j] * cmath.exp(-2j * math.pi * k * j / n)
        result.append((k, psi_k))
    return result


def power_spectrum(
    dft: list[tuple[int, complex]],
) -> list[tuple[int, float]]:
    """Compute |psi_k|^2 for each Fourier mode."""
    return [(k, abs(a) ** 2) for k, a in dft]


def linear_regression(
    xs: list[float], ys: list[float]
) -> tuple[float, float, float]:
    """Simple OLS: y = a + b*x.  Returns (a, b, R^2)."""
    n = len(xs)
    if n < 2:
        return 0.0, 0.0, 0.0

    sx = sum(xs)
    sy = sum(ys)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    syy = sum(y * y for y in ys)

    denom = n * sxx - sx * sx
    if abs(denom) < 1e-30:
        return 0.0, 0.0, 0.0

    b = (n * sxy - sx * sy) / denom
    a = (sy - b * sx) / n

    ss_res = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    y_mean = sy / n
    ss_tot = sum((y - y_mean) ** 2 for y in ys)

    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0
    return a, b, r_squared


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------


def run_experiment():
    t0 = time.time()
    print("=" * 72)
    print("HAWKING-ANALOG RADIATION FROM AMPLITUDE TRAPPING")
    print("=" * 72)
    print()
    print(f"Grid:  {WIDTH} x {2*HEIGHT+1}  (x=0..{WIDTH}, y={-HEIGHT}..{HEIGHT})")
    print(f"Source: {SOURCE}")
    print(f"Detector: x = {WIDTH}")
    print(f"Mass cluster center: ({MASS_CENTER_X}, {MASS_CENTER_Y}), radius={MASS_RADIUS}")
    print(f"Phase wavenumber: {PHASE_K}")
    print(f"Attenuation power: {ATTENUATION_POWER}")
    print(f"Field strengths: {FIELD_STRENGTHS}")
    print()

    nodes = build_rectangular_nodes(width=WIDTH, height=HEIGHT)
    mass_cluster = make_mass_cluster(
        MASS_CENTER_X, MASS_CENTER_Y, MASS_RADIUS, nodes
    )
    print(f"Mass cluster: {len(mass_cluster)} persistent nodes")
    print()

    # -----------------------------------------------------------------------
    # Part 0: Baseline (no field)
    # -----------------------------------------------------------------------
    print("-" * 72)
    print("PART 0: BASELINE (no field)")
    print("-" * 72)

    postulates_free = RulePostulates(
        phase_per_action=PHASE_K,
        attenuation_power=ATTENUATION_POWER,
        action_mode="spent_delay",
        field_mode="none",
    )
    rule_free = derive_local_rule(frozenset(), postulates_free)
    arrival_free = infer_arrival_times_from_source(nodes, SOURCE, rule_free)
    dag_free = build_causal_dag(nodes, arrival_free)
    node_field_free = {n: 0.0 for n in nodes}
    psi_free = propagate_amplitude(dag_free, SOURCE, rule_free, node_field_free)

    det_free = extract_detector_amplitudes(psi_free, WIDTH, HEIGHT)
    p_total_free = sum(abs(a) ** 2 for _, a in det_free)
    print(f"  Total detector probability (free): {p_total_free:.6e}")

    # Field-free spectral control
    dft_free = discrete_fourier_transform(det_free)
    ps_free = power_spectrum(dft_free)
    n_modes_free = len(ps_free)
    half_free = n_modes_free // 2
    pos_modes_free = [(k, p) for k, p in ps_free if 0 < k <= half_free]
    valid_free = [(k, p) for k, p in pos_modes_free if p > 0]
    if len(valid_free) >= 3:
        xs_free = [float(k * k) for k, _ in valid_free]
        ys_free = [math.log(p) for _, p in valid_free]
        a_free, b_free, r2_free = linear_regression(xs_free, ys_free)
        t_free = 1.0 / (2.0 * abs(b_free)) if abs(b_free) > 1e-30 else float("inf")
        label_free = "THERMAL" if r2_free > 0.9 else ("marginal" if r2_free > 0.5 else "NOT thermal")
        print(f"  Free-field spectrum: a={a_free:+.4f} b={b_free:+.6f} "
              f"R^2={r2_free:.4f} T={t_free:.4f} [{label_free}]")
        print(f"  ==> This is the CONTROL: if free-field is also thermal-shaped,")
        print(f"      the shape is geometric (lattice structure), not field-induced.")
    else:
        r2_free = 0.0
        print(f"  Free-field spectrum: too few modes for fit")
    print()

    # -----------------------------------------------------------------------
    # Part 1: Field-enhanced throughput (not trapping)
    # -----------------------------------------------------------------------
    print("-" * 72)
    print("PART 1: DETECTOR THROUGHPUT vs FIELD STRENGTH")
    print("  NOTE: 'trapped fraction' is negative at all tested strengths,")
    print("  meaning the field ENHANCES detector probability (no trapping).")
    print("-" * 72)

    results = {}  # field_strength -> dict of results

    for s in FIELD_STRENGTHS:
        # Scale the field by multiplying the postulates' phase wavenumber
        # is not the right approach. Instead, we need to scale the actual
        # field values. The field from derive_node_field gives values in
        # [0, 1] based on persistence support and relaxation. We need to
        # scale these to control the trapping strength.
        #
        # Strategy: use field_mode="relaxed" to get the shape, then scale
        # the field values by a coupling constant.

        postulates = RulePostulates(
            phase_per_action=PHASE_K,
            attenuation_power=ATTENUATION_POWER,
            action_mode="spent_delay",
            field_mode="relaxed",
        )
        rule = derive_local_rule(mass_cluster, postulates)

        # Get the raw relaxed field (values in [0, ~1])
        raw_field = derive_node_field(nodes, rule)

        # Scale field by strength parameter s
        # The field enters as: delay = link_length * (1 + field)
        # So we want field values ~ s to get controllable trapping.
        # Raw field max is O(1), so we scale: effective_field = s * raw_field / max(raw_field)
        raw_max = max(raw_field.values())
        if raw_max > 0:
            scaled_field = {n: s * raw_field[n] / raw_max for n in nodes}
        else:
            scaled_field = {n: 0.0 for n in nodes}

        # Build arrival times with scaled field
        # We need to bypass the standard functions and use the scaled field directly.
        # Use infer_arrival_times_with_field indirectly by creating a rule
        # whose field we override.
        from toy_event_physics import infer_arrival_times_with_field

        # For arrival times, we need a rule that will produce our scaled field.
        # But derive_node_field is called inside infer_arrival_times_from_source.
        # Instead, call infer_arrival_times_with_field directly with our scaled field.
        arrival_times = infer_arrival_times_with_field(
            nodes, SOURCE, rule, scaled_field
        )
        dag = build_causal_dag(nodes, arrival_times)

        # Propagate amplitude with the scaled field
        psi = propagate_amplitude(dag, SOURCE, rule, scaled_field)

        det = extract_detector_amplitudes(psi, WIDTH, HEIGHT)
        p_total = sum(abs(a) ** 2 for _, a in det)
        trapped_fraction = 1.0 - p_total / p_total_free if p_total_free > 0 else 0.0

        # Store results
        results[s] = {
            "det_amplitudes": det,
            "p_total": p_total,
            "trapped_fraction": trapped_fraction,
            "scaled_field": scaled_field,
            "psi": psi,
        }

        print(f"  s = {s:.0e}:  P_det = {p_total:.6e}  "
              f"trapped = {trapped_fraction:+.4f}")

    print()

    # -----------------------------------------------------------------------
    # Part 2: Spectral analysis of escaped amplitude
    # -----------------------------------------------------------------------
    print("-" * 72)
    print("PART 2: FOURIER POWER SPECTRUM OF ESCAPED AMPLITUDE")
    print("-" * 72)

    spectra = {}  # s -> list of (k, |psi_k|^2)

    for s in FIELD_STRENGTHS:
        det = results[s]["det_amplitudes"]
        dft = discrete_fourier_transform(det)
        ps = power_spectrum(dft)

        # Use only positive frequency modes (k = 1 to N//2)
        n_modes = len(ps)
        half = n_modes // 2
        pos_modes = [(k, p) for k, p in ps if 0 < k <= half]

        spectra[s] = pos_modes

        print(f"\n  s = {s:.0e}:  {len(pos_modes)} positive frequency modes")
        for k, pk in pos_modes[:5]:
            log_pk = math.log(pk) if pk > 0 else float("-inf")
            print(f"    k={k:3d}  |psi_k|^2 = {pk:.4e}  ln = {log_pk:+.2f}")
        if len(pos_modes) > 5:
            print(f"    ... ({len(pos_modes) - 5} more modes)")

    print()

    # -----------------------------------------------------------------------
    # Part 3: Test for thermal spectrum
    # -----------------------------------------------------------------------
    print("-" * 72)
    print("PART 3: THERMAL SPECTRUM TEST  (ln|psi_k|^2  vs  k^2)")
    print("-" * 72)
    print()
    print("  Fit:  ln(|psi_k|^2) = a - b * k^2")
    print("  Thermal if R^2 > 0.9;  falsified if R^2 < 0.5")
    print()

    fit_results = {}  # s -> (a, b, r2)

    for s in FIELD_STRENGTHS:
        pos_modes = spectra[s]

        # Filter out zero-power modes
        valid = [(k, p) for k, p in pos_modes if p > 0]
        if len(valid) < 3:
            print(f"  s = {s:.0e}:  Too few valid modes ({len(valid)}), skipping")
            fit_results[s] = (0.0, 0.0, 0.0)
            continue

        xs = [float(k * k) for k, _ in valid]
        ys = [math.log(p) for _, p in valid]

        a, b, r2 = linear_regression(xs, ys)
        fit_results[s] = (a, b, r2)

        thermal_label = "THERMAL" if r2 > 0.9 else ("marginal" if r2 > 0.5 else "NOT thermal")
        temp = 1.0 / (2.0 * abs(b)) if abs(b) > 1e-30 else float("inf")

        print(f"  s = {s:.0e}:  a = {a:+.4f}  b = {b:+.6f}  "
              f"R^2 = {r2:.4f}  T = {temp:.4f}  [{thermal_label}]")

    print()

    # -----------------------------------------------------------------------
    # Part 4: Temperature vs mass scaling
    # -----------------------------------------------------------------------
    print("-" * 72)
    print("PART 4: TEMPERATURE vs FIELD STRENGTH (Hawking: T ~ 1/M)")
    print("-" * 72)
    print()
    print("  If T ~ 1/s (inverse mass), then b ~ s (linear).")
    print("  Fit:  b = c0 + c1 * s")
    print()

    # Collect (s, b) pairs where the fit was meaningful
    sb_pairs = []
    for s in FIELD_STRENGTHS:
        a, b, r2 = fit_results[s]
        if r2 > 0.3 and abs(b) > 1e-30:
            sb_pairs.append((s, abs(b)))
            print(f"  s = {s:.0e}:  |b| = {abs(b):.6f}  T = {1/(2*abs(b)):.4f}")

    print()

    if len(sb_pairs) >= 3:
        ss = [x[0] for x in sb_pairs]
        bs = [x[1] for x in sb_pairs]
        c0, c1, r2_scaling = linear_regression(ss, bs)
        print(f"  Linear fit:  |b| = {c0:.6f} + {c1:.4f} * s")
        print(f"  R^2(b vs s) = {r2_scaling:.4f}")

        if r2_scaling > 0.9:
            print("  => b scales linearly with s: CONSISTENT with T ~ 1/M (Hawking)")
        elif r2_scaling > 0.5:
            print("  => Marginal linear scaling")
        else:
            print("  => b does NOT scale linearly with s: Hawking scaling FALSIFIED")

        # Also test b ~ s^alpha via log-log
        if all(x > 0 for x in ss) and all(x > 0 for x in bs):
            log_ss = [math.log(x) for x in ss]
            log_bs = [math.log(x) for x in bs]
            log_a, alpha, r2_power = linear_regression(log_ss, log_bs)
            print()
            print(f"  Power-law fit:  ln|b| = {log_a:.4f} + {alpha:.4f} * ln(s)")
            print(f"  R^2(log-log) = {r2_power:.4f}")
            print(f"  Exponent alpha = {alpha:.4f}  (Hawking predicts alpha = 1)")
    else:
        print("  Too few valid (s, b) pairs for scaling analysis.")

    # -----------------------------------------------------------------------
    # Part 5: Detector probability distribution P(y)
    # -----------------------------------------------------------------------
    print()
    print("-" * 72)
    print("PART 5: DETECTOR PROBABILITY DISTRIBUTION P(y)")
    print("-" * 72)
    print()

    # Show for selected field strengths
    for s in [FIELD_STRENGTHS[0], FIELD_STRENGTHS[-1]]:
        det = results[s]["det_amplitudes"]
        print(f"  s = {s:.0e}:")
        p_total = results[s]["p_total"]
        for y_val, amp in det:
            p = abs(amp) ** 2
            bar = "#" * int(50 * p / max(abs(a) ** 2 for _, a in det)) if p > 0 else ""
            print(f"    y={y_val:+3d}  P={p:.4e}  {bar}")
        print()

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print()

    any_thermal = False
    for s in FIELD_STRENGTHS:
        a, b, r2 = fit_results[s]
        if r2 > 0.9:
            any_thermal = True

    print("HYPOTHESIS: Escaped amplitude has a thermal energy spectrum.")
    print()

    thermal_count = sum(1 for s in FIELD_STRENGTHS if fit_results[s][2] > 0.9)
    marginal_count = sum(1 for s in FIELD_STRENGTHS if 0.5 < fit_results[s][2] <= 0.9)
    not_thermal_count = sum(1 for s in FIELD_STRENGTHS if fit_results[s][2] <= 0.5)

    print(f"  Thermal (R^2 > 0.9):      {thermal_count}/{len(FIELD_STRENGTHS)}")
    print(f"  Marginal (0.5 < R^2 < 0.9): {marginal_count}/{len(FIELD_STRENGTHS)}")
    print(f"  Not thermal (R^2 < 0.5):  {not_thermal_count}/{len(FIELD_STRENGTHS)}")
    print()

    if thermal_count == len(FIELD_STRENGTHS):
        print("VERDICT: ALL field strengths show thermal spectrum. Hypothesis SUPPORTED.")
    elif thermal_count > 0:
        print(f"VERDICT: {thermal_count}/{len(FIELD_STRENGTHS)} thermal. "
              "Partial support; regime-dependent.")
    elif marginal_count > 0:
        print("VERDICT: No clean thermal fits. Marginal evidence only.")
    else:
        print("VERDICT: Hypothesis FALSIFIED. No thermal spectra observed.")

    # Hawking scaling verdict
    if len(sb_pairs) >= 3:
        _, _, r2_s = linear_regression(
            [x[0] for x in sb_pairs], [x[1] for x in sb_pairs]
        )
        print()
        if r2_s > 0.9:
            print("HAWKING SCALING (T ~ 1/M): SUPPORTED (R^2 = {:.4f})".format(r2_s))
        elif r2_s > 0.5:
            print("HAWKING SCALING (T ~ 1/M): MARGINAL (R^2 = {:.4f})".format(r2_s))
        else:
            print("HAWKING SCALING (T ~ 1/M): FALSIFIED (R^2 = {:.4f})".format(r2_s))

    elapsed = time.time() - t0
    print()
    print(f"Total runtime: {elapsed:.1f}s")
    print("=" * 72)


if __name__ == "__main__":
    run_experiment()
