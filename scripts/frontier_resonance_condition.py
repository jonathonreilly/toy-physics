#!/usr/bin/env python3
"""Derive the exact resonance condition for gravity oscillations from path-length differences.

THE PHYSICS
  Gravity in the model oscillates between attractive and repulsive as k*H varies,
  with period ~pi/2. This suggests partial-wave interference between paths of
  different lengths. Goal: derive the exact resonance condition analytically.

THE MATH
  On a 2D lattice with spacing h, forward path (dy=0) has length L0 = h per edge.
  First diagonal (dy=+/-1) has length L1 = h*sqrt(2). Path-length difference:
    dL = L1 - L0 = h*(sqrt(2) - 1) ~ 0.414h

  Phase difference:  dphi = k * dL = k*h*(sqrt(2) - 1)
  Constructive when: dphi = 2n*pi  =>  k*h = 2n*pi/(sqrt(2)-1) ~ 15.2n
  Destructive when:  dphi = (2n+1)*pi  =>  k*h ~ 7.6*(2n+1)

  Observed period ~1.5 in k*h is much shorter => multi-path interference.

  For a single transverse step spread over n layers: dy=1 over n hops,
    dL(n) = n*h*(sqrt(1+1/n^2) - 1) ~ h/(2n) for large n
    dphi(n) = k*h/(2n)

APPROACH
  Part 1: Two-path interference model (analytic predictions)
  Part 2: Numerical k-sweep measuring gravity signal oscillation
  Part 3: Path-length decomposition -- extract dominant dL from FFT of signal

HYPOTHESIS: The gravity oscillation period in k is 2*pi/dL where dL is a
  specific geometric path-length difference.
FALSIFICATION: If the period is not constant or doesn't match any geometric dL.
"""

from __future__ import annotations
import cmath
import math
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
    infer_arrival_times_with_field,
    build_causal_dag,
    local_edge_properties,
)


# ── Helpers ───────────────────────────────────────────────────────

def analytic_spatial_field(nodes, mass_y, strength):
    """Spatial-only 1/r field: depends only on |y - y_mass|."""
    field = {}
    for n in nodes:
        r = abs(n[1] - mass_y) + 0.1
        field[n] = strength / r
    return field


def propagate_with_field(nodes, source, node_field, width, k, p=1):
    """Valley-linear propagation on a flat-space DAG with field in the action.

    S = L*(1-f), kernel = 1/L^p, phase = k*S.
    DAG built from flat space to isolate action effect.
    """
    flat_field = {n: 0.0 for n in nodes}
    rule = derive_local_rule(frozenset(), RulePostulates(
        phase_per_action=k, attenuation_power=p))
    arrival = infer_arrival_times_with_field(nodes, source, rule, flat_field)
    dag = build_causal_dag(nodes, arrival)
    order = sorted(arrival, key=arrival.get)

    states = defaultdict(complex)
    states[source] = 1.0 + 0j
    detector = {}

    for node in order:
        amp = states.get(node, 0j)
        if abs(amp) < 1e-30:
            continue
        if node[0] == width:
            detector[node[1]] = detector.get(node[1], 0j) + amp
            continue
        for neighbor in dag.get(node, []):
            L = math.dist(node, neighbor)
            f = 0.5 * (node_field.get(node, 0.0) + node_field.get(neighbor, 0.0))
            act = L * (1.0 - f)
            edge_amp = cmath.exp(1j * k * act) / (L ** p)
            states[neighbor] += amp * edge_amp

    return detector


def centroid(det):
    total = sum(abs(a) ** 2 for a in det.values())
    if total < 1e-30:
        return 0.0, total
    return sum(y * abs(a) ** 2 for y, a in det.items()) / total, total


def gravity_signal(nodes, source, width, mass_y, field_strength, k, p=1):
    """Return centroid shift (positive = toward mass at +y)."""
    flat_field = {n: 0.0 for n in nodes}
    mass_field = analytic_spatial_field(nodes, mass_y, field_strength)

    det_flat = propagate_with_field(nodes, source, flat_field, width, k, p)
    det_mass = propagate_with_field(nodes, source, mass_field, width, k, p)

    c_flat, _ = centroid(det_flat)
    c_mass, _ = centroid(det_mass)
    return c_mass - c_flat


# ── Part 1: Analytic two-path model ──────────────────────────────

def part1_analytic_predictions():
    """Compute expected resonance conditions from path-length differences."""
    print("=" * 72)
    print("PART 1: ANALYTIC TWO-PATH INTERFERENCE MODEL")
    print("=" * 72)

    h = 1.0  # lattice spacing

    # Forward path: all edges have length h
    # Diagonal path: edges at 45 degrees have length h*sqrt(2)
    L_forward = h
    L_diagonal = h * math.sqrt(2)
    dL_single_hop = L_diagonal - L_forward

    print(f"\nSingle-hop path-length differences (h={h}):")
    print(f"  Forward edge length:  L0 = {L_forward:.4f}")
    print(f"  Diagonal edge length: L1 = {L_diagonal:.4f}")
    print(f"  dL (single hop) = {dL_single_hop:.4f}")
    print(f"  Predicted period in k: 2*pi/dL = {2*math.pi/dL_single_hop:.4f}")

    # Multi-hop: one diagonal step spread over n forward hops
    print(f"\nMulti-hop path-length differences:")
    print(f"  {'n hops':>8s}  {'dL':>10s}  {'period=2pi/dL':>14s}  {'dL approx h/(2n)':>16s}")
    for n in [1, 2, 3, 4, 5, 6, 8, 10, 15, 20]:
        # Path with dy=1 over n steps: each step has dx=1, dy=1/n
        # But on a lattice we can only step to integer coords.
        # A path of n hops forward + 1 diagonal = n+1 hops total,
        # vs n+1 forward hops.
        # L_with_diag = n*h + h*sqrt(2) = h*(n + sqrt(2))
        # L_all_forward = (n+1)*h
        # dL = h*(sqrt(2) - 1)  -- same as single hop!
        #
        # Better: compare paths that arrive at the SAME endpoint.
        # Forward path: n hops straight = n*h
        # One-step-off path: (n-1) forward + 1 diagonal = (n-1)*h + h*sqrt(2)
        #   = h*(n - 1 + sqrt(2))
        # dL = h*(sqrt(2) - 1) -- ALWAYS the same regardless of n!
        #
        # For a smooth diagonal: n hops each (dx=1, dy=1/n) interpolated
        # Total length = n * sqrt(h^2 + (h/n)^2) = n*h*sqrt(1 + 1/n^2)
        # vs n*h forward
        # dL = n*h*(sqrt(1+1/n^2) - 1) ~ h/(2n)
        dL_smooth = n * h * (math.sqrt(1 + 1.0 / n**2) - 1)
        dL_approx = h / (2 * n)
        period = 2 * math.pi / dL_smooth if dL_smooth > 0 else float('inf')
        print(f"  {n:>8d}  {dL_smooth:>10.6f}  {period:>14.4f}  {dL_approx:>16.6f}")

    # The key insight: on a lattice, paths differ by EXACTLY one diagonal
    # substitution. The dL is always h*(sqrt(2)-1) per substitution.
    dL_sub = h * (math.sqrt(2) - 1)
    period_sub = 2 * math.pi / dL_sub
    print(f"\nKey result: ONE diagonal substitution always gives dL = {dL_sub:.6f}")
    print(f"  => Period in k = 2*pi/dL = {period_sub:.4f}")
    print(f"  => Half-period (sign change) = {period_sub/2:.4f}")

    # But the action is NOT just path length. With spent_delay:
    # S = L - sqrt(L^2 - L^2) = L for flat space (delay = L when f=0).
    # So action = path length in flat space. The resonance in k
    # should be exactly 2*pi/dL.

    # With field: S = L*(1-f), so dS = dL*(1-f) - L*df ≈ dL for small f.
    # The gravity signal comes from the f-dependent part, but the
    # OSCILLATION in k comes from the dL part.

    print(f"\nWith valley-linear action S = L*(1-f):")
    print(f"  In flat space: action per edge = L (same as path length)")
    print(f"  Phase per forward hop: k*{L_forward}")
    print(f"  Phase per diagonal hop: k*{L_diagonal:.4f}")
    print(f"  Phase difference per substitution: k*{dL_sub:.6f}")
    print(f"  Constructive: k*dL = 2n*pi => k = {2*math.pi/dL_sub:.4f}*n")
    print(f"  Destructive:  k*dL = (2n+1)*pi => k = {math.pi/dL_sub:.4f}*(2n+1)")

    return dL_sub, period_sub


# ── Part 2: Numerical k-sweep ────────────────────────────────────

def part2_k_sweep(width=20, height=8, field_strength=1e-3, p=1):
    """Fine k-sweep to measure gravity oscillation period."""
    print(f"\n{'=' * 72}")
    print("PART 2: NUMERICAL k-SWEEP OF GRAVITY SIGNAL")
    print(f"  Grid: {width}x{2*height+1}, field_strength={field_strength}")
    print(f"  Kernel: 1/L^{p}")
    print("=" * 72)

    nodes = build_rectangular_nodes(width, height)
    source = (0, 0)
    mass_y = height // 2  # mass above center

    k_values = [0.5 + 0.1 * i for i in range(96)]  # k from 0.5 to 10.0
    signals = []

    print(f"\n  Mass at y={mass_y}, source at y=0")
    print(f"  Sweeping k from {k_values[0]:.1f} to {k_values[-1]:.1f} "
          f"in {len(k_values)} steps...")

    for i, k in enumerate(k_values):
        sig = gravity_signal(nodes, source, width, mass_y, field_strength, k, p)
        signals.append(sig)
        if i % 20 == 0:
            direction = "TOWARD" if sig > 0 else "AWAY"
            print(f"    k={k:5.1f}  signal={sig:+.6e}  {direction}")

    # Print full table
    print(f"\n  Full k-sweep results:")
    print(f"  {'k':>6s}  {'signal':>14s}  {'direction':>9s}")
    print(f"  {'-'*6}  {'-'*14}  {'-'*9}")
    for k, sig in zip(k_values, signals):
        direction = "TOWARD" if sig > 0 else "AWAY"
        print(f"  {k:6.2f}  {sig:+14.6e}  {direction}")

    # Find zero-crossings (sign changes)
    crossings = []
    for i in range(len(signals) - 1):
        if signals[i] * signals[i + 1] < 0:
            # Linear interpolation for crossing point
            k0, s0 = k_values[i], signals[i]
            k1, s1 = k_values[i + 1], signals[i + 1]
            k_cross = k0 - s0 * (k1 - k0) / (s1 - s0)
            crossings.append(k_cross)

    print(f"\n  Zero-crossings (sign changes) at k =")
    for i, kc in enumerate(crossings):
        print(f"    crossing {i+1}: k = {kc:.4f}")

    # Compute periods between consecutive crossings
    if len(crossings) >= 2:
        half_periods = [crossings[i+1] - crossings[i]
                        for i in range(len(crossings) - 1)]
        full_periods = [crossings[i+2] - crossings[i]
                        for i in range(len(crossings) - 2)]

        print(f"\n  Half-periods (between consecutive crossings):")
        for i, hp in enumerate(half_periods):
            dL_implied = math.pi / hp if hp > 0 else float('inf')
            print(f"    {hp:.4f}  (implies dL = pi/half_period = {dL_implied:.4f})")

        if full_periods:
            print(f"\n  Full periods (between every-other crossing):")
            for i, fp in enumerate(full_periods):
                dL_implied = 2 * math.pi / fp if fp > 0 else float('inf')
                print(f"    {fp:.4f}  (implies dL = 2*pi/period = {dL_implied:.4f})")

            avg_period = sum(full_periods) / len(full_periods)
            dL_measured = 2 * math.pi / avg_period
            print(f"\n  Average full period: {avg_period:.4f}")
            print(f"  Implied path-length difference: dL = {dL_measured:.6f}")
        else:
            avg_period = None
            dL_measured = None
    else:
        print("  (fewer than 2 crossings found)")
        avg_period = None
        dL_measured = None

    return k_values, signals, crossings, avg_period, dL_measured


# ── Part 3: FFT-based period extraction ──────────────────────────

def part3_fft_analysis(k_values, signals, dL_analytic):
    """Use FFT to extract dominant oscillation frequency in k-space."""
    print(f"\n{'=' * 72}")
    print("PART 3: FFT ANALYSIS OF GRAVITY SIGNAL vs k")
    print("=" * 72)

    n = len(signals)
    dk = k_values[1] - k_values[0]

    # Remove mean
    mean_sig = sum(signals) / n
    centered = [s - mean_sig for s in signals]

    # Manual DFT (no numpy dependency)
    # Frequency bins: f_j = j / (n * dk) for j = 0..n/2
    # The "frequency in k-space" f maps to a path-length difference:
    #   signal oscillates as cos(dL * k)
    #   = cos(2*pi * (dL/(2*pi)) * k)
    #   so frequency in k = dL/(2*pi)
    #   => dL = 2*pi * f

    max_j = n // 2
    power_spectrum = []

    print(f"\n  Computing DFT of {n} points, dk={dk:.4f}...")

    for j in range(1, max_j + 1):
        # DFT coefficient
        re = sum(centered[i] * math.cos(2 * math.pi * j * i / n)
                 for i in range(n))
        im = sum(centered[i] * math.sin(2 * math.pi * j * i / n)
                 for i in range(n))
        power = re * re + im * im
        freq_k = j / (n * dk)  # frequency in k-space
        dL_candidate = 2 * math.pi * freq_k  # implied path-length difference
        period_k = 1.0 / freq_k if freq_k > 0 else float('inf')
        power_spectrum.append((j, freq_k, dL_candidate, period_k, power))

    # Sort by power
    power_spectrum.sort(key=lambda x: -x[4])

    print(f"\n  Top 10 FFT peaks (sorted by power):")
    print(f"  {'bin':>4s}  {'freq_k':>8s}  {'dL':>10s}  {'period_k':>10s}  {'power':>14s}")
    print(f"  {'-'*4}  {'-'*8}  {'-'*10}  {'-'*10}  {'-'*14}")
    for j, fk, dL, pk, power in power_spectrum[:10]:
        marker = " <-- DOMINANT" if power == power_spectrum[0][4] else ""
        print(f"  {j:4d}  {fk:8.4f}  {dL:10.4f}  {pk:10.4f}  {power:14.4e}{marker}")

    # Dominant peak
    dom = power_spectrum[0]
    dL_fft = dom[2]
    period_fft = dom[3]

    print(f"\n  Dominant FFT peak:")
    print(f"    Frequency in k-space: {dom[1]:.6f}")
    print(f"    Implied dL: {dL_fft:.6f}")
    print(f"    Implied period in k: {period_fft:.4f}")

    # Compare with analytic prediction
    print(f"\n  Comparison with analytic predictions:")
    print(f"    dL (single diagonal substitution) = {dL_analytic:.6f}")
    print(f"    dL (FFT dominant peak)            = {dL_fft:.6f}")
    if dL_analytic > 0:
        ratio = dL_fft / dL_analytic
        print(f"    Ratio FFT/analytic = {ratio:.4f}")
        # Check if it's a simple fraction
        for num in range(1, 10):
            for den in range(1, 10):
                if abs(ratio - num / den) < 0.05:
                    print(f"    Close to {num}/{den} = {num/den:.4f}")

    return dL_fft, period_fft


# ── Part 4: Geometric path-length census ──────────────────────────

def part4_path_length_census(width=20, height=8):
    """Enumerate actual path-length differences on the lattice.

    On a lattice, each edge is either forward (L=1) or diagonal (L=sqrt(2)).
    A path of W hops from x=0 to x=W consists of some number d of diagonal
    edges and (W-d) forward edges (since each hop advances x by 1).
    Actually: forward means dx=1,dy=0; diagonal means dx=1,dy=+/-1.
    Every path from source to detector has exactly W edges (since each
    edge has dx=1 in the DAG).

    Path length = d*sqrt(2) + (W-d)*1 = W + d*(sqrt(2)-1)

    So path-length differences are always multiples of (sqrt(2)-1).
    """
    print(f"\n{'=' * 72}")
    print("PART 4: GEOMETRIC PATH-LENGTH CENSUS")
    print("=" * 72)

    sqrt2 = math.sqrt(2)
    dL_unit = sqrt2 - 1  # ~0.4142

    print(f"\n  On the DAG, each edge has dx=1 (forward in causal direction).")
    print(f"  Edge types: forward (dy=0, L=1) or diagonal (dy=+/-1, L=sqrt(2))")
    print(f"  A path of W={width} hops has d diagonal edges and (W-d) forward edges.")
    print(f"  Path length = W + d*(sqrt(2)-1) = {width} + d*{dL_unit:.6f}")
    print(f"  All path-length differences are multiples of dL = {dL_unit:.6f}")
    print(f"\n  Phase difference for d extra diagonals: dphi = k * d * {dL_unit:.6f}")
    print(f"  Full cycle: k * dL = 2*pi => k = {2*math.pi/dL_unit:.4f}")

    # Now: on the actual DAG, how many diagonals does a typical path have?
    # A path to detector y=0 from source y=0 must have equal up and down
    # diagonals. If it has d_up up-diagonals and d_down down-diagonals,
    # then d_up = d_down (to return to y=0), so d = 2*d_up.
    # Path length = W + 2*d_up*(sqrt(2)-1)

    # A path to detector y=m from source y=0 needs d_up - d_down = m,
    # so d = d_up + d_down >= |m|, and d - |m| is even.

    # The gravity signal compares paths arriving at different y values.
    # Paths to y=+1 vs y=-1 differ by having one more up-diagonal.
    # But both are compared to the same flat-space baseline.

    # Actually the key interference is at a FIXED detector y.
    # At detector y=0, paths with d=0 (all forward) have length W.
    # Paths with d=2 (one up + one down) have length W + 2*dL_unit.
    # Phase difference = k * 2 * dL_unit.

    print(f"\n  At detector y=0 (same as source):")
    print(f"  {'d diags':>8s}  {'path length':>12s}  {'dL from d=0':>12s}  "
          f"{'dphi/k':>10s}  {'constructive when k=':>22s}")
    for d in range(0, min(width, 2 * height) + 1, 2):
        pl = width + d * dL_unit
        dl = d * dL_unit
        dphi_per_k = dl
        if dl > 0:
            k_constr = 2 * math.pi / dl
            print(f"  {d:>8d}  {pl:>12.4f}  {dl:>12.4f}  "
                  f"{dphi_per_k:>10.4f}  k = {k_constr:>10.4f} / n")
        else:
            print(f"  {d:>8d}  {pl:>12.4f}  {dl:>12.4f}  "
                  f"{dphi_per_k:>10.4f}  (reference)")

    # The dominant interference: d=0 vs d=2 gives dL = 2*(sqrt(2)-1) = 0.828
    # d=0 vs d=4 gives dL = 4*(sqrt(2)-1) = 1.657
    # But d=2 vs d=4 also gives dL = 2*(sqrt(2)-1) = 0.828
    # So the fundamental is dL = 2*(sqrt(2)-1) for central detector.

    dL_fundamental_center = 2 * dL_unit
    period_center = 2 * math.pi / dL_fundamental_center

    print(f"\n  Fundamental dL at center: 2*(sqrt(2)-1) = {dL_fundamental_center:.6f}")
    print(f"  Period in k: {period_center:.4f}")

    # For detector y=1 (one step off center):
    # Minimum diagonals: d=1 (one up-diagonal, no down-diagonal)
    # Next: d=3 (two up + one down, or similar)
    # dL between consecutive: 2*(sqrt(2)-1) again

    print(f"\n  At detector y=1:")
    print(f"  Min diagonals: d=1, path length = {width + dL_unit:.4f}")
    print(f"  Next: d=3, path length = {width + 3*dL_unit:.4f}")
    print(f"  Spacing: 2*(sqrt(2)-1) = {dL_fundamental_center:.6f}")

    # But the gravity signal is the difference between mass-side and
    # no-mass side. The field modifies the action, not the path lengths.
    # So the oscillation in k should still come from the path-length
    # spacing.

    return dL_unit, dL_fundamental_center


# ── Part 5: Verify with different grid sizes ─────────────────────

def part5_grid_size_check():
    """Check if oscillation period depends on grid size (it shouldn't if geometric)."""
    print(f"\n{'=' * 72}")
    print("PART 5: GRID SIZE INDEPENDENCE CHECK")
    print("=" * 72)

    configs = [
        (12, 4, 1e-3),
        (16, 6, 1e-3),
        (20, 8, 1e-3),
        (24, 10, 1e-3),
    ]

    dL_unit = math.sqrt(2) - 1

    for width, height, fs in configs:
        nodes = build_rectangular_nodes(width, height)
        source = (0, 0)
        mass_y = height // 2

        k_values = [0.5 + 0.1 * i for i in range(96)]
        signals = []
        for k in k_values:
            sig = gravity_signal(nodes, source, width, mass_y, fs, k)
            signals.append(sig)

        # Find crossings
        crossings = []
        for i in range(len(signals) - 1):
            if signals[i] * signals[i + 1] < 0:
                k0, s0 = k_values[i], signals[i]
                k1, s1 = k_values[i + 1], signals[i + 1]
                k_cross = k0 - s0 * (k1 - k0) / (s1 - s0)
                crossings.append(k_cross)

        if len(crossings) >= 3:
            full_periods = [crossings[i+2] - crossings[i]
                            for i in range(len(crossings) - 2)]
            avg_period = sum(full_periods) / len(full_periods)
            dL_measured = 2 * math.pi / avg_period
        else:
            avg_period = float('nan')
            dL_measured = float('nan')

        n_crossings = len(crossings)
        print(f"\n  Grid {width}x{2*height+1}:  "
              f"{n_crossings} crossings, "
              f"avg period = {avg_period:.4f}, "
              f"dL = {dL_measured:.4f}")
        print(f"    Ratio dL/dL_unit = {dL_measured/dL_unit:.4f}  "
              f"(expect integer if clean)")
        if crossings:
            print(f"    First 5 crossings: "
                  f"{', '.join(f'{c:.3f}' for c in crossings[:5])}")


# ── Part 6: Action-based analysis ────────────────────────────────

def part6_action_analysis():
    """Compare path-length resonance with action-based resonance.

    In flat space with spent_delay action mode:
      delay = L (when field=0)
      retained = sqrt(delay^2 - L^2) = 0
      action = delay - retained = L

    So action = path length. But with valley-linear S = L*(1-f):
      action per edge = L*(1-f)

    The action difference between two paths is:
      dS = dL*(1-f_avg) - sum(L_i * df_i)

    The first term gives the geometric oscillation.
    The second term is the gravity-producing part.
    """
    print(f"\n{'=' * 72}")
    print("PART 6: ACTION vs PATH-LENGTH RESONANCE")
    print("=" * 72)

    h = 1.0
    sqrt2 = math.sqrt(2)
    dL = sqrt2 - 1  # per diagonal substitution

    print(f"\n  Valley-linear action: S = L*(1-f)")
    print(f"  For two paths differing by one diagonal substitution:")
    print(f"    dS = dL*(1-f_avg) = {dL:.4f}*(1-f)")
    print(f"    At f=0: dS = dL = {dL:.4f}")
    print(f"    At f=0.01: dS = {dL*0.99:.4f}")
    print(f"    At f=0.1: dS = {dL*0.9:.4f}")
    print(f"\n  The oscillation period shifts slightly with field strength:")
    print(f"    period(f) = 2*pi/(dL*(1-f))")
    print(f"    At f=0: period = {2*math.pi/dL:.4f}")
    print(f"    At f=0.01: period = {2*math.pi/(dL*0.99):.4f}")
    print(f"    At f=0.1: period = {2*math.pi/(dL*0.9):.4f}")

    # With spent_delay action mode (the default):
    # delay = L*(1+f), retained = sqrt(delay^2 - L^2) = L*sqrt((1+f)^2 - 1)
    # = L*sqrt(f^2 + 2f) ~ L*sqrt(2f) for small f
    # action = delay - retained = L*(1+f) - L*sqrt(f^2+2f)
    # For small f: action ~ L*(1+f) - L*sqrt(2f) = L*(1 + f - sqrt(2f))
    # This is NOT the valley-linear form!

    print(f"\n  With spent_delay action mode (default in toy_event_physics):")
    print(f"    delay = L*(1+f)")
    print(f"    retained = L*sqrt((1+f)^2 - 1) = L*sqrt(f^2+2f)")
    print(f"    action = delay - retained")
    for f_val in [0, 0.001, 0.01, 0.1]:
        for L in [1.0, sqrt2]:
            delay = L * (1 + f_val)
            retained = L * math.sqrt(max((1 + f_val)**2 - 1, 0))
            action = delay - retained
            label = "fwd" if abs(L - 1) < 0.01 else "diag"
            print(f"    f={f_val:.3f}, L={L:.4f} ({label}): "
                  f"delay={delay:.4f}, retained={retained:.4f}, "
                  f"action={action:.6f}")

    # Action difference at f=0: forward action = 1, diagonal action = sqrt(2)
    # dS = sqrt(2) - 1 = same as dL. Good.
    print(f"\n  At f=0: action = L for all edges (retained = 0)")
    print(f"  => Action difference = path-length difference = {dL:.6f}")
    print(f"  => Resonance condition is purely geometric")


# ── MAIN ─────────────────────────────────────────────────────────

def main():
    print("*" * 72)
    print("FRONTIER: RESONANCE CONDITION FOR GRAVITY OSCILLATIONS")
    print("Derive exact resonance from path-length differences")
    print("*" * 72)

    dL_analytic, period_analytic = part1_analytic_predictions()
    k_values, signals, crossings, avg_period, dL_measured = part2_k_sweep()
    dL_fft, period_fft = part3_fft_analysis(k_values, signals, dL_analytic)
    dL_unit, dL_fundamental = part4_path_length_census()
    part5_grid_size_check()
    part6_action_analysis()

    # ── Summary ───────────────────────────────────────────────────
    print(f"\n{'=' * 72}")
    print("SUMMARY: RESONANCE CONDITION")
    print("=" * 72)

    print(f"\n  Analytic prediction (single diagonal substitution):")
    print(f"    dL = sqrt(2) - 1 = {dL_analytic:.6f}")
    print(f"    Period in k = 2*pi/dL = {period_analytic:.4f}")

    print(f"\n  Path-length census (center detector, d=0 vs d=2):")
    print(f"    dL = 2*(sqrt(2)-1) = {dL_fundamental:.6f}")
    print(f"    Period in k = 2*pi/dL = {2*math.pi/dL_fundamental:.4f}")

    if dL_measured is not None:
        print(f"\n  Numerical measurement (zero-crossing method):")
        print(f"    Average period = {avg_period:.4f}")
        print(f"    Implied dL = {dL_measured:.6f}")
        print(f"    Ratio to dL_unit = {dL_measured/dL_analytic:.4f}")

    print(f"\n  FFT measurement:")
    print(f"    Dominant period = {period_fft:.4f}")
    print(f"    Implied dL = {dL_fft:.6f}")
    print(f"    Ratio to dL_unit = {dL_fft/dL_analytic:.4f}")

    # Verdict
    print(f"\n  HYPOTHESIS TEST:")
    # Check if dL_measured or dL_fft is close to an integer multiple of dL_unit
    for label, dL_val in [("zero-crossing", dL_measured),
                          ("FFT", dL_fft)]:
        if dL_val is None or math.isnan(dL_val):
            print(f"    {label}: insufficient data")
            continue
        ratio = dL_val / dL_analytic
        nearest_int = round(ratio)
        residual = abs(ratio - nearest_int)
        if residual < 0.15:
            print(f"    {label}: dL = {nearest_int} * dL_unit "
                  f"(residual {residual:.3f}) => CONFIRMED")
            print(f"      Resonance: k * {nearest_int} * (sqrt(2)-1) = 2*n*pi")
            print(f"      => k = {2*math.pi/(nearest_int*dL_analytic):.4f} * n")
        else:
            print(f"    {label}: ratio = {ratio:.3f}, "
                  f"nearest integer = {nearest_int}, "
                  f"residual = {residual:.3f} => FALSIFIED (not integer multiple)")

    # Check number of crossings for consistency
    if crossings and len(crossings) >= 2:
        print(f"\n  Total zero-crossings found: {len(crossings)}")
        print(f"  k range: {k_values[0]:.1f} to {k_values[-1]:.1f}")
        expected_from_analytic = (k_values[-1] - k_values[0]) / (period_analytic / 2)
        print(f"  Expected crossings from period {period_analytic:.1f}: "
              f"~{expected_from_analytic:.1f}")


if __name__ == "__main__":
    main()
