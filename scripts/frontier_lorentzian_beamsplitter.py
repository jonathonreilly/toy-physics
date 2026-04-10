#!/usr/bin/env python3
"""Lorentzian beam-splitter: systematic search for TOWARD gravity + Born.

THE IDEA:
  The local beam-splitter unitary (frontier_local_unitary_propagator.py)
  passes Born + norm + locality but gravity is AWAY. The fix: try all
  Lorentzian phase/mixing conventions to find TOWARD gravity.

BEAM-SPLITTER HAS TWO STEPS PER LAYER:
  Step A: Phase kick (causal direction) - 3 variants
  Step B: Mixing (spatial direction) - 4 variants

  3 x 4 = 12 combinations tested for Born, gravity, norm.

PHASE KICK VARIANTS:
  P1: exp(i*k*(1-f))      current Euclidean VL
  P2: exp(i*k*(1+f))      reversed: more phase near mass
  P3: exp(i*k*f)          field-only phase (no free-space part)

MIXING VARIANTS:
  M1: alpha constant              current: no field coupling
  M2: alpha*(1+f)                 more mixing near mass
  M3: alpha*(1-f)                 less mixing near mass
  M4: alpha + field phase in U    mixing gets complex phase from field

HYPOTHESIS: "At least one Lorentzian (phase, mixing) combination gives
TOWARD gravity while preserving Born."
FALSIFICATION: "If NO combination gives TOWARD + Born simultaneously."
"""
from __future__ import annotations

import math
import time
import numpy as np

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
HEIGHT = 8
N_Y = 2 * HEIGHT + 1   # 17
N_LAYERS = 20
ALPHA = 0.3
STRENGTH = 5e-4
MASS_X = 10
MASS_Y = HEIGHT + 4     # y=12, offset from center=8
K_DEFAULT = 5.0
EPS = 0.01

PHASE_MODES = ["P1", "P2", "P3"]
MIXING_MODES = ["M1", "M2", "M3", "M4"]

# ---------------------------------------------------------------------------
# Field construction
# ---------------------------------------------------------------------------
def make_field_flat(n_layers, n_y):
    return np.zeros((n_layers, n_y))


def make_field_mass(n_layers, n_y, x_mass, y_mass, strength):
    field = np.zeros((n_layers, n_y))
    for x in range(n_layers):
        for y in range(n_y):
            r2 = (x - x_mass) ** 2 + (y - y_mass) ** 2
            field[x, y] = strength / math.sqrt(r2 + EPS)
    return field


# ---------------------------------------------------------------------------
# Propagator with configurable phase and mixing modes
# ---------------------------------------------------------------------------
def propagate(n_y, n_layers, k, field, alpha_base, phase_mode, mixing_mode,
              blocked=None):
    """Beam-splitter propagator with configurable Lorentzian conventions.

    Args:
        phase_mode: P1, P2, P3
        mixing_mode: M1, M2, M3, M4
        blocked: dict mapping layer -> set of blocked sites
    """
    if blocked is None:
        blocked = {}

    psi = np.zeros(n_y, dtype=complex)
    psi[n_y // 2] = 1.0

    history = [psi.copy()]

    for layer in range(n_layers):
        f = field[layer, :]

        # Step A: Phase kick
        if phase_mode == "P1":
            psi *= np.exp(1j * k * (1.0 - f))
        elif phase_mode == "P2":
            psi *= np.exp(1j * k * (1.0 + f))
        elif phase_mode == "P3":
            psi *= np.exp(1j * k * f)

        # Apply barrier
        if layer in blocked:
            for y in blocked[layer]:
                psi[y] = 0.0

        # Helper for 2x2 mixing
        def mix_pair(y, f_local):
            if mixing_mode == "M1":
                a = alpha_base
            elif mixing_mode == "M2":
                a = alpha_base * (1.0 + f_local)
            elif mixing_mode == "M3":
                a = alpha_base * (1.0 - f_local)
            elif mixing_mode == "M4":
                # Field-dependent phase in mixing unitary
                # U = [[cos(a)*e^{i*phi}, -sin(a)], [sin(a), cos(a)*e^{-i*phi}]]
                a = alpha_base
                phi = k * f_local
                ca = math.cos(a)
                sa = math.sin(a)
                ep = np.exp(1j * phi)
                em = np.exp(-1j * phi)
                v1, v2 = psi[y], psi[y + 1]
                psi[y] = ca * ep * v1 - sa * v2
                psi[y + 1] = sa * v1 + ca * em * v2
                return

            ca = math.cos(a)
            sa = math.sin(a)
            v1, v2 = psi[y], psi[y + 1]
            psi[y] = ca * v1 - sa * v2
            psi[y + 1] = sa * v1 + ca * v2

        # Step B: Even pairs
        even_max = n_y - 1 if n_y % 2 == 0 else n_y - 2
        for y in range(0, even_max, 2):
            if layer in blocked and (y in blocked[layer] or (y + 1) in blocked[layer]):
                continue
            f_mid = 0.5 * (field[layer, y] + field[layer, y + 1])
            mix_pair(y, f_mid)

        # Step C: Odd pairs
        for y in range(1, n_y - 1, 2):
            if layer in blocked and (y in blocked[layer] or (y + 1) in blocked[layer]):
                continue
            f_mid = 0.5 * (field[layer, y] + field[layer, y + 1])
            mix_pair(y, f_mid)

        history.append(psi.copy())

    return history


# ---------------------------------------------------------------------------
# Measurements
# ---------------------------------------------------------------------------
def centroid(psi, n_y):
    probs = np.abs(psi) ** 2
    total = probs.sum()
    if total < 1e-30:
        return n_y / 2.0
    return np.dot(np.arange(n_y, dtype=float), probs) / total


def detection_prob(psi):
    return np.sum(np.abs(psi) ** 2)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_norm(n_y, n_layers, k, field, alpha, phase_mode, mixing_mode):
    """Check norm preservation."""
    history = propagate(n_y, n_layers, k, field, alpha, phase_mode, mixing_mode)
    norms = [np.sum(np.abs(psi) ** 2) for psi in history]
    max_dev = max(abs(n - 1.0) for n in norms)
    # M4 uses a non-standard unitary - check if it's still unitary
    return max_dev < 1e-6, max_dev


def test_born(n_y, n_layers, k, field, alpha, phase_mode, mixing_mode):
    """3-slit Sorkin I3 test."""
    x_barrier = n_layers // 3
    center = n_y // 2
    slit_A = center - 3
    slit_B = center
    slit_C = center + 3
    all_sites = set(range(n_y))

    def make_blocked(open_slits):
        return {x_barrier: all_sites - set(open_slits)}

    configs = {
        "ABC": [slit_A, slit_B, slit_C],
        "AB":  [slit_A, slit_B],
        "AC":  [slit_A, slit_C],
        "BC":  [slit_B, slit_C],
        "A":   [slit_A],
        "B":   [slit_B],
        "C":   [slit_C],
    }

    probs = {}
    for name, open_slits in configs.items():
        blocked = make_blocked(open_slits)
        history = propagate(n_y, n_layers, k, field, alpha, phase_mode,
                            mixing_mode, blocked=blocked)
        probs[name] = detection_prob(history[-1])

    I3 = (probs["ABC"]
          - probs["AB"] - probs["AC"] - probs["BC"]
          + probs["A"] + probs["B"] + probs["C"])

    # Normalize by max probability
    p_max = max(probs.values())
    if p_max > 1e-30:
        I3_norm = abs(I3) / p_max
    else:
        I3_norm = abs(I3)

    passed = I3_norm < 0.01
    return passed, I3, I3_norm


def test_gravity(n_y, n_layers, k, alpha, phase_mode, mixing_mode):
    """Measure gravity direction: centroid shift toward or away from mass."""
    field_flat = make_field_flat(n_layers, n_y)
    field_mass = make_field_mass(n_layers, n_y, MASS_X, MASS_Y, STRENGTH)

    history_flat = propagate(n_y, n_layers, k, field_flat, alpha, phase_mode,
                             mixing_mode)
    history_mass = propagate(n_y, n_layers, k, field_mass, alpha, phase_mode,
                             mixing_mode)

    c_flat = centroid(history_flat[-1], n_y)
    c_mass = centroid(history_mass[-1], n_y)

    shift = c_mass - c_flat
    # Mass is at y=12, center at y=8. TOWARD means shift > 0.
    direction = "TOWARD" if shift > 1e-10 else ("AWAY" if shift < -1e-10 else "ZERO")
    return direction, shift, c_flat, c_mass


def test_gravity_spectral(n_y, n_layers, alpha, phase_mode, mixing_mode,
                          k_values=None):
    """Spectral-averaged gravity: average over multiple k values."""
    if k_values is None:
        k_values = np.linspace(1.0, 10.0, 20)

    field_flat = make_field_flat(n_layers, n_y)
    field_mass = make_field_mass(n_layers, n_y, MASS_X, MASS_Y, STRENGTH)

    shifts = []
    for k in k_values:
        h_flat = propagate(n_y, n_layers, k, field_flat, alpha, phase_mode,
                           mixing_mode)
        h_mass = propagate(n_y, n_layers, k, field_mass, alpha, phase_mode,
                           mixing_mode)
        c_flat = centroid(h_flat[-1], n_y)
        c_mass = centroid(h_mass[-1], n_y)
        shifts.append(c_mass - c_flat)

    avg_shift = np.mean(shifts)
    direction = "TOWARD" if avg_shift > 1e-10 else ("AWAY" if avg_shift < -1e-10 else "ZERO")
    toward_count = sum(1 for s in shifts if s > 1e-10)
    return direction, avg_shift, toward_count, len(k_values), shifts


def test_gravity_scaling(n_y, n_layers, k, alpha, phase_mode, mixing_mode):
    """Check if deflection scales with field strength (F proportional to M)."""
    field_flat = make_field_flat(n_layers, n_y)
    c_flat = centroid(propagate(n_y, n_layers, k, field_flat, alpha, phase_mode,
                                mixing_mode)[-1], n_y)

    strengths = [STRENGTH * m for m in [1, 2, 4, 8]]
    shifts = []
    for s in strengths:
        field_m = make_field_mass(n_layers, n_y, MASS_X, MASS_Y, s)
        h = propagate(n_y, n_layers, k, field_m, alpha, phase_mode, mixing_mode)
        shifts.append(centroid(h[-1], n_y) - c_flat)

    return strengths, shifts


# ---------------------------------------------------------------------------
# Main sweep
# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("=" * 80)
    print("FRONTIER: Lorentzian Beam-Splitter Phase/Mixing Sweep")
    print("=" * 80)
    print(f"  N_Y={N_Y}, N_LAYERS={N_LAYERS}, alpha={ALPHA}, k={K_DEFAULT}")
    print(f"  Mass at ({MASS_X}, {MASS_Y}), strength={STRENGTH}")
    print(f"  Center at y={N_Y // 2}")
    print(f"  Phase modes: {PHASE_MODES}")
    print(f"  Mixing modes: {MIXING_MODES}")
    print()

    field_mass = make_field_mass(N_LAYERS, N_Y, MASS_X, MASS_Y, STRENGTH)

    # Phase 1: Full 12-combination sweep
    print("-" * 80)
    print("PHASE 1: Full 3x4 sweep (Born + Gravity + Norm)")
    print("-" * 80)
    header = f"{'Phase':>5} | {'Mix':>3} | {'Born I3':>12} | {'I3_norm':>10} | {'Born':>5} | {'Grav shift':>12} | {'Dir':>6} | {'Norm dev':>10} | {'Norm':>5}"
    print(header)
    print("-" * len(header))

    winners = []  # (phase, mix) combos with TOWARD + Born PASS

    for pm in PHASE_MODES:
        for mm in MIXING_MODES:
            # Norm test
            norm_pass, norm_dev = test_norm(N_Y, N_LAYERS, K_DEFAULT,
                                            field_mass, ALPHA, pm, mm)

            # Born test (use flat field for purity - Born should hold regardless)
            field_flat = make_field_flat(N_LAYERS, N_Y)
            born_pass, I3, I3_norm = test_born(N_Y, N_LAYERS, K_DEFAULT,
                                                field_flat, ALPHA, pm, mm)

            # Gravity test
            grav_dir, grav_shift, c_flat, c_mass = test_gravity(
                N_Y, N_LAYERS, K_DEFAULT, ALPHA, pm, mm)

            tag = ""
            if grav_dir == "TOWARD" and born_pass:
                tag = " *** WINNER ***"
                winners.append((pm, mm))
            elif grav_dir == "TOWARD":
                tag = " (TOWARD but Born FAIL)"

            print(f"{pm:>5} | {mm:>3} | {I3:>12.2e} | {I3_norm:>10.2e} | "
                  f"{'PASS' if born_pass else 'FAIL':>5} | {grav_shift:>12.6f} | "
                  f"{grav_dir:>6} | {norm_dev:>10.2e} | "
                  f"{'PASS' if norm_pass else 'FAIL':>5}{tag}")

    print()

    # Phase 2: Also test Born with mass field (not just flat)
    print("-" * 80)
    print("PHASE 2: Born test WITH mass field (harder test)")
    print("-" * 80)
    header2 = f"{'Phase':>5} | {'Mix':>3} | {'Born I3 (mass)':>15} | {'I3_norm':>10} | {'Born':>5} | {'Dir':>6}"
    print(header2)
    print("-" * len(header2))

    winners_mass = []

    for pm in PHASE_MODES:
        for mm in MIXING_MODES:
            born_pass, I3, I3_norm = test_born(N_Y, N_LAYERS, K_DEFAULT,
                                                field_mass, ALPHA, pm, mm)
            grav_dir, grav_shift, _, _ = test_gravity(N_Y, N_LAYERS, K_DEFAULT,
                                                       ALPHA, pm, mm)
            tag = ""
            if grav_dir == "TOWARD" and born_pass:
                tag = " *** WINNER ***"
                winners_mass.append((pm, mm))

            print(f"{pm:>5} | {mm:>3} | {I3:>15.2e} | {I3_norm:>10.2e} | "
                  f"{'PASS' if born_pass else 'FAIL':>5} | {grav_dir:>6}{tag}")

    print()

    # Phase 3: Deep analysis of winners
    all_winners = list(set(winners + winners_mass))
    if all_winners:
        print("=" * 80)
        print(f"PHASE 3: Deep analysis of {len(all_winners)} winner(s)")
        print("=" * 80)

        for pm, mm in all_winners:
            print(f"\n  --- {pm} + {mm} ---")

            # Spectral averaging
            print(f"\n  Spectral gravity (k=1..10, 20 values):")
            direction, avg_shift, toward_ct, total_k, shifts = \
                test_gravity_spectral(N_Y, N_LAYERS, ALPHA, pm, mm)
            print(f"    Average shift: {avg_shift:.8f}")
            print(f"    Direction: {direction}")
            print(f"    TOWARD at {toward_ct}/{total_k} k-values")

            # k-sweep detail
            k_vals = np.linspace(1.0, 10.0, 20)
            print(f"\n  k-sweep detail:")
            for i, (kv, sh) in enumerate(zip(k_vals, shifts)):
                d = "TOWARD" if sh > 1e-10 else ("AWAY" if sh < -1e-10 else "ZERO")
                print(f"    k={kv:5.2f}: shift={sh:+.8f}  {d}")

            # F proportional to M scaling
            print(f"\n  F ~ M scaling:")
            strengths, g_shifts = test_gravity_scaling(
                N_Y, N_LAYERS, K_DEFAULT, ALPHA, pm, mm)
            for s, gs in zip(strengths, g_shifts):
                d = "TOWARD" if gs > 1e-10 else ("AWAY" if gs < -1e-10 else "ZERO")
                print(f"    strength={s:.1e}: shift={gs:+.8f}  {d}")

            # Check linearity
            if len(g_shifts) >= 2 and abs(g_shifts[0]) > 1e-15:
                ratios = [gs / g_shifts[0] for gs in g_shifts]
                expected = [s / strengths[0] for s in strengths]
                print(f"    Shift ratios:    {[f'{r:.3f}' for r in ratios]}")
                print(f"    Expected (lin):  {[f'{e:.3f}' for e in expected]}")

            # Born with mass field
            print(f"\n  Born with mass field:")
            bp, I3, I3n = test_born(N_Y, N_LAYERS, K_DEFAULT, field_mass,
                                     ALPHA, pm, mm)
            print(f"    I3 = {I3:.6e}, I3_norm = {I3n:.6e}, {'PASS' if bp else 'FAIL'}")

    else:
        print("=" * 80)
        print("NO WINNERS: No (phase, mixing) combination gives TOWARD + Born PASS")
        print("=" * 80)

        # Additional analysis: which combos get closest?
        print("\nClosest-to-winning analysis:")
        print("  Combos with TOWARD gravity (even if Born fails):")
        for pm in PHASE_MODES:
            for mm in MIXING_MODES:
                grav_dir, grav_shift, _, _ = test_gravity(
                    N_Y, N_LAYERS, K_DEFAULT, ALPHA, pm, mm)
                if grav_dir == "TOWARD":
                    _, I3, I3_norm = test_born(N_Y, N_LAYERS, K_DEFAULT,
                                               make_field_flat(N_LAYERS, N_Y),
                                               ALPHA, pm, mm)
                    print(f"    {pm}+{mm}: shift={grav_shift:+.8f}, "
                          f"I3_norm={I3_norm:.2e}")

        print("\n  Combos with Born PASS (even if gravity wrong):")
        for pm in PHASE_MODES:
            for mm in MIXING_MODES:
                field_flat = make_field_flat(N_LAYERS, N_Y)
                born_pass, I3, I3_norm = test_born(N_Y, N_LAYERS, K_DEFAULT,
                                                    field_flat, ALPHA, pm, mm)
                if born_pass:
                    grav_dir, grav_shift, _, _ = test_gravity(
                        N_Y, N_LAYERS, K_DEFAULT, ALPHA, pm, mm)
                    print(f"    {pm}+{mm}: dir={grav_dir}, shift={grav_shift:+.8f}")

    # Phase 4: Extended search - vary alpha
    print("\n" + "=" * 80)
    print("PHASE 4: Alpha sweep for promising combos")
    print("=" * 80)

    # Test all combos at different alpha values
    alphas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.785]  # pi/4 ~ 0.785
    print(f"{'Phase':>5} | {'Mix':>3} | ", end="")
    for a in alphas:
        print(f"  a={a:.2f}  ", end="")
    print()
    print("-" * (15 + len(alphas) * 12))

    for pm in PHASE_MODES:
        for mm in MIXING_MODES:
            print(f"{pm:>5} | {mm:>3} | ", end="")
            for a in alphas:
                grav_dir, grav_shift, _, _ = test_gravity(
                    N_Y, N_LAYERS, K_DEFAULT, a, pm, mm)
                norm_pass, _ = test_norm(N_Y, N_LAYERS, K_DEFAULT,
                                         field_mass, a, pm, mm)
                symbol = "T" if grav_dir == "TOWARD" else ("A" if grav_dir == "AWAY" else "0")
                if not norm_pass:
                    symbol = "X"  # norm broken
                print(f"  {symbol:>1} {grav_shift:+.4f}", end="")
            print()

    # Phase 5: Larger field strength test
    print("\n" + "=" * 80)
    print("PHASE 5: Larger field strength (5e-3) sweep")
    print("=" * 80)

    big_field = make_field_mass(N_LAYERS, N_Y, MASS_X, MASS_Y, 5e-3)
    header5 = f"{'Phase':>5} | {'Mix':>3} | {'Grav shift':>12} | {'Dir':>6} | {'Born I3_norm':>12} | {'Norm dev':>10}"
    print(header5)
    print("-" * len(header5))

    for pm in PHASE_MODES:
        for mm in MIXING_MODES:
            grav_dir, grav_shift, _, _ = test_gravity(
                N_Y, N_LAYERS, K_DEFAULT, ALPHA, pm, mm)
            # Use bigger field for gravity
            field_flat = make_field_flat(N_LAYERS, N_Y)
            h_flat = propagate(N_Y, N_LAYERS, K_DEFAULT, field_flat, ALPHA, pm, mm)
            h_mass = propagate(N_Y, N_LAYERS, K_DEFAULT, big_field, ALPHA, pm, mm)
            c_flat = centroid(h_flat[-1], N_Y)
            c_mass = centroid(h_mass[-1], N_Y)
            big_shift = c_mass - c_flat
            big_dir = "TOWARD" if big_shift > 1e-10 else ("AWAY" if big_shift < -1e-10 else "ZERO")

            _, I3, I3_norm = test_born(N_Y, N_LAYERS, K_DEFAULT,
                                        big_field, ALPHA, pm, mm)
            norm_pass, norm_dev = test_norm(N_Y, N_LAYERS, K_DEFAULT,
                                            big_field, ALPHA, pm, mm)

            tag = " ***" if big_dir == "TOWARD" and I3_norm < 0.01 else ""
            print(f"{pm:>5} | {mm:>3} | {big_shift:>12.6f} | {big_dir:>6} | "
                  f"{I3_norm:>12.2e} | {norm_dev:>10.2e}{tag}")

    elapsed = time.time() - t0
    print(f"\n{'=' * 80}")
    print(f"Total runtime: {elapsed:.1f}s")
    print(f"{'=' * 80}")

    # Final verdict
    print("\nVERDICT:")
    if all_winners:
        print(f"  HYPOTHESIS SUPPORTED: {len(all_winners)} combination(s) give "
              f"TOWARD + Born PASS")
        for pm, mm in all_winners:
            print(f"    {pm} + {mm}")
    else:
        print("  HYPOTHESIS FALSIFIED: No combination gives TOWARD + Born simultaneously")
        print("  The beam-splitter sign convention alone cannot fix gravity direction.")


if __name__ == "__main__":
    main()
