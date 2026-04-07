#!/usr/bin/env python3
"""Velocity sweep on the wave-retardation lane.

The Lane 6 / Lane 8b retardation result was a single point: at
v/c = 0.23 (source moving in z over 26 layers), the retarded field M
and the instantaneous comparator I differ in beam deflection by
26-31% across three grown families.

For an honest experimental prediction card, we need the SCALING of
(M - I) with v/c. The candidate scalings are:

  (v/c)^0  — constant; trivial
  (v/c)^1  — linear; matches first-order post-Newtonian retardation
  (v/c)^2  — quadratic; matches relativistic corrections
  exp(-1/(v/c)) — non-perturbative

This lane runs the wave-retardation harness at v/c ∈ {0.05, 0.10,
0.15, 0.20, 0.25, 0.30, 0.40} and reports:
  - dM, dI for each velocity on Fam1
  - relative gap (dM - dI) / max(|dM|, |dI|)
  - log-log fit of |dM - dI| vs v/c
  - inferred scaling exponent

The exponent determines whether the effect is observable at lab v/c
(typically 10^-9 to 10^-3 depending on platform) or sits in the
relativistic-only regime.
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Reuse the wave_retarded_gravity machinery
import wave_retarded_gravity as wrg

# Constants from wrg
NL = wrg.NL
PW = wrg.PW
H = wrg.H
S = wrg.S
K = wrg.K


def slope_log(xs, ys):
    """Log-log linear fit slope."""
    valid = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(valid) < 2:
        return 0.0, 0.0
    lx = [math.log(x) for x, _ in valid]
    ly = [math.log(y) for _, y in valid]
    n = len(lx)
    mx = sum(lx) / n
    my = sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in lx)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    a = sxy / sxx if sxx > 0 else 0.0
    b = my - a * mx
    return a, b


def measure_at_velocity(pos, adj, nmap, v_per_layer, src_layer_start):
    """Compute dM, dI for a single velocity."""
    iz_start = 6
    iz_of_t = lambda t: iz_start + int(round(v_per_layer * (t - src_layer_start)))

    h_M = wrg._make_field(S, iz_of_t)
    h_I = wrg._make_instantaneous(S, iz_of_t)

    free = wrg._prop_beam(pos, adj, nmap, None, K)
    z_free = wrg._cz(free, pos)

    cz_M = wrg._cz(wrg._prop_beam(pos, adj, nmap, h_M, K), pos)
    cz_I = wrg._cz(wrg._prop_beam(pos, adj, nmap, h_I, K), pos)
    dM = cz_M - z_free
    dI = cz_I - z_free
    return dM, dI


def main():
    print("=" * 100)
    print("WAVE RETARDATION VELOCITY SWEEP")
    print(f"NL={NL}, PW={PW}, S={S}, base s_layer = NL // 3 = {NL // 3}")
    print("Source motion: linear translation in z; v varies")
    print("=" * 100)

    src_layer_start = NL // 3
    n_active = NL - src_layer_start

    # Velocities expressed as cells/layer; v/c with c = 1 lattice cell/layer
    # v_per_layer = (iz_end - iz_start) / n_active where iz_start=6
    # For a fixed motion range, v varies inversely with sweep duration.
    # Here we vary v_per_layer directly and let iz_end follow.
    velocities = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40]

    pos, adj, nmap = wrg.grow(0, 0.20, 0.70)

    results = []
    print(f"\n{'v/c':>6s} {'iz_end':>8s} {'dM':>12s} {'dI':>12s} "
          f"{'M-I':>12s} {'rel':>10s}")
    print("-" * 80)
    for v in velocities:
        # negative sign so source moves in -z (matching the original lane)
        v_signed = -v
        dM, dI = measure_at_velocity(pos, adj, nmap, v_signed, src_layer_start)
        diff = dM - dI
        rel = abs(diff) / max(abs(dM), abs(dI), 1e-12)
        iz_end_implied = 6 + int(round(v_signed * n_active))
        results.append((v, dM, dI, diff, rel))
        print(f"  {v:.3f} {iz_end_implied:>8d} {dM:+12.6f} {dI:+12.6f} "
              f"{diff:+12.6f} {rel:10.2%}")

    # Log-log fit of |M-I| vs v/c
    vs = [r[0] for r in results]
    diffs_abs = [abs(r[3]) for r in results]
    rels = [r[4] for r in results]

    print(f"\nLog-log fit of |M - I| vs v/c:")
    slope_diff, intercept_diff = slope_log(vs, diffs_abs)
    print(f"  slope = {slope_diff:+.3f}  intercept = {intercept_diff:+.3f}")
    print(f"  -> |M - I| ~ (v/c)^{slope_diff:.2f}")

    print(f"\nLog-log fit of relative gap (|M-I|/max(|M|,|I|)) vs v/c:")
    slope_rel, intercept_rel = slope_log(vs, rels)
    print(f"  slope = {slope_rel:+.3f}  intercept = {intercept_rel:+.3f}")
    print(f"  -> rel_gap ~ (v/c)^{slope_rel:.2f}")

    # Verdict on scaling
    print("\n" + "=" * 100)
    print("SCALING VERDICT")
    print("=" * 100)
    if abs(slope_diff - 1.0) < 0.2:
        print(f"  LINEAR scaling: |M - I| ∝ v/c (slope = {slope_diff:.2f})")
        print("  Matches first-order post-Newtonian retardation behavior.")
    elif abs(slope_diff - 2.0) < 0.3:
        print(f"  QUADRATIC scaling: |M - I| ∝ (v/c)² (slope = {slope_diff:.2f})")
        print("  Matches second-order relativistic corrections.")
    elif slope_diff < 0.5:
        print(f"  WEAKER than linear (slope = {slope_diff:.2f})")
        print("  Effect saturates or is largely v-independent in this range.")
    elif slope_diff > 2.5:
        print(f"  STRONGER than quadratic (slope = {slope_diff:.2f})")
        print("  Suggests a regime change or crossover.")
    else:
        print(f"  Intermediate scaling (slope = {slope_diff:.2f})")

    # Lab-scale extrapolation
    print("\n" + "=" * 100)
    print("LAB EXTRAPOLATION (assuming the fitted scaling)")
    print("=" * 100)
    # Pick a representative lab velocity
    lab_vc = [
        ("cold atom interferometer (1 m/s)", 1.0 / 3e8),
        ("rotating tungsten rotor (100 m/s)", 100.0 / 3e8),
        ("centrifuge edge (300 m/s)", 300.0 / 3e8),
        ("LIGO test-mass scale (1 mm/s)", 1e-3 / 3e8),
        ("binary pulsar (250 km/s)", 2.5e5 / 3e8),
    ]
    diff_at_v23 = abs([r[3] for r in results if abs(r[0] - 0.20) < 0.01][0] if any(
        abs(r[0] - 0.20) < 0.01 for r in results
    ) else results[3][3])
    rel_at_v23 = [r[4] for r in results if abs(r[0] - 0.20) < 0.01][0] if any(
        abs(r[0] - 0.20) < 0.01 for r in results
    ) else results[3][4]
    print(f"  Reference lattice point: v/c = 0.20 -> rel_gap = {rel_at_v23:.2%}")
    print(f"  Predicted lab gap (using slope {slope_rel:.2f}):")
    for name, vlab in lab_vc:
        ratio = (vlab / 0.20) ** slope_rel
        predicted = rel_at_v23 * ratio
        print(f"    {name:40s}  v/c = {vlab:.2e}  rel_gap ≈ {predicted:.2e}")

    print("\nThese are dimensionless predictions for the M vs I beam-deflection ratio")
    print("on the (3+1)D wave equation. They translate to a measurable phase shift")
    print("in any interferometer that maps to the path-sum + linear-field setup.")

    # ========================================================================
    # SECOND SWEEP: disentangle velocity from trajectory geometry
    # Fix iz_start=6, iz_end=0 (always traverse 6 cells); vary v by varying
    # n_active (the duration of the source motion) within a longer NL
    # ========================================================================
    print("\n" + "=" * 100)
    print("SECOND SWEEP: TRAJECTORY-FIXED, VELOCITY-VARYING")
    print("Fixed source trajectory iz: 6 -> 0 (always 6 cells)")
    print("Velocity = 6 / n_active where n_active varies")
    print("=" * 100)

    original_NL = wrg.NL
    durations = [60, 30, 20, 15, 12, 10, 8]
    print(f"\n{'n_act':>6s} {'NL_total':>9s} {'v/c':>8s} {'dM':>12s} {'dI':>12s} "
          f"{'M-I':>12s} {'rel':>10s}")
    print("-" * 90)
    sweep2 = []
    for n_active in durations:
        wrg.NL = (original_NL // 3) + n_active + 4
        try:
            pos2, adj2, nmap2 = wrg.grow(0, 0.20, 0.70)
            v_per_layer = -6.0 / n_active
            src_layer = wrg.NL // 3
            iz_of_t = lambda t, sl=src_layer, v=v_per_layer: 6 + int(round(v * (t - sl)))
            h_M = wrg._make_field(S, iz_of_t)
            h_I = wrg._make_instantaneous(S, iz_of_t)
            free = wrg._prop_beam(pos2, adj2, nmap2, None, K)
            z_free = wrg._cz(free, pos2)
            cz_M = wrg._cz(wrg._prop_beam(pos2, adj2, nmap2, h_M, K), pos2)
            cz_I = wrg._cz(wrg._prop_beam(pos2, adj2, nmap2, h_I, K), pos2)
            dM = cz_M - z_free
            dI = cz_I - z_free
            diff = dM - dI
            rel = abs(diff) / max(abs(dM), abs(dI), 1e-12)
            sweep2.append((n_active, abs(v_per_layer), dM, dI, rel))
            print(f"  {n_active:>6d} {wrg.NL:>9d} {abs(v_per_layer):8.4f} "
                  f"{dM:+12.6f} {dI:+12.6f} {diff:+12.6f} {rel:10.2%}")
        except Exception as e:
            print(f"  {n_active:>6d}  ERROR: {e}")
        finally:
            wrg.NL = original_NL

    if len(sweep2) >= 3:
        vs2 = [r[1] for r in sweep2]
        rels2 = [r[4] for r in sweep2]
        slope2, _ = slope_log(vs2, rels2)
        print(f"\nLog-log fit of trajectory-fixed rel_gap vs v/c:")
        print(f"  slope = {slope2:+.3f}")
        print(f"  -> rel_gap (trajectory-fixed) ~ (v/c)^{slope2:.2f}")
        print(f"\nThis is the PURE velocity scaling with trajectory geometry held constant.")
        print(f"Compare to first sweep slope of {slope_rel:.2f} which conflated v with range.")


if __name__ == "__main__":
    main()
