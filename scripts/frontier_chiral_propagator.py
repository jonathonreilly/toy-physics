#!/usr/bin/env python3
"""
Frontier: Chiral Propagator
============================
Discrete chiral walk with field-dependent phase in the chirality-flip coin.

Architecture:
  State = 2*n_y vector: [psi_+(0), psi_-(0), psi_+(1), psi_-(1), ...]
  Per layer:
    Step 1 (Coin): local 2x2 unitary at each site with field in off-diagonal phase
    Step 2 (Shift): psi_+ moves right, psi_- moves left, reflecting boundaries

HYPOTHESIS: "The chiral propagator preserves Born, norm, and produces
TOWARD gravity with F proportional to M = 1.00."
FALSIFICATION: "If Born I3 > 1e-6, or F proportional to M deviates by >20%,
or gravity is AWAY at all k."
"""

import numpy as np
from itertools import combinations

# ── Parameters ──────────────────────────────────────────────────────
N_Y = 17
N_LAYERS = 20
K_DEFAULT = 5.0
STRENGTH = 5e-4
THETA = 0.3          # bare mixing angle
MASS_X = 10
MASS_Y = 4
SOURCE_Y = 8         # center

# ── Core propagator ─────────────────────────────────────────────────

def make_field(n_layers, n_y, strength, mass_y):
    """1/r field from a mass at mass_y."""
    field = np.zeros((n_layers, n_y))
    for x in range(n_layers):
        for y in range(n_y):
            field[x, y] = strength / (abs(y - mass_y) + 0.1)
    return field


def chiral_propagate(n_y, n_layers, k, field_2d, theta, source_y,
                     blocked_sites=None, theta_field=None):
    """
    Propagate chiral walk.

    blocked_sites: set of y indices where propagation is blocked (barrier).
                   At blocked sites, coin = identity and shift is suppressed.
    theta_field: if provided, 2d array of theta(x,y) overriding constant theta.
    """
    psi = np.zeros(2 * n_y, dtype=complex)
    psi[2 * source_y] = 1.0  # right-mover at source

    norms = []
    for x in range(n_layers):
        # Step 1: Coin at each site
        for y in range(n_y):
            if blocked_sites and y in blocked_sites:
                continue  # identity coin at blocked sites
            phi = k * field_2d[x, y]
            th = theta_field[x, y] if theta_field is not None else theta
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi[idx_p], psi[idx_m]
            psi[idx_p] = np.cos(th) * pp - np.sin(th) * np.exp(1j * phi) * pm
            psi[idx_m] = np.sin(th) * np.exp(-1j * phi) * pp + np.cos(th) * pm

        # Step 2: Shift
        new_psi = np.zeros_like(psi)
        for y in range(n_y):
            if blocked_sites and y in blocked_sites:
                # blocked site: amplitude stays (no shift)
                new_psi[2 * y] += psi[2 * y]
                new_psi[2 * y + 1] += psi[2 * y + 1]
                continue
            # Right-mover shifts right
            if y + 1 < n_y:
                if blocked_sites and (y + 1) in blocked_sites:
                    new_psi[2 * y + 1] += psi[2 * y]  # reflect off barrier
                else:
                    new_psi[2 * (y + 1)] += psi[2 * y]
            else:
                new_psi[2 * y + 1] += psi[2 * y]  # reflect at boundary
            # Left-mover shifts left
            if y - 1 >= 0:
                if blocked_sites and (y - 1) in blocked_sites:
                    new_psi[2 * y] += psi[2 * y + 1]  # reflect off barrier
                else:
                    new_psi[2 * (y - 1) + 1] += psi[2 * y + 1]
            else:
                new_psi[2 * y] += psi[2 * y + 1]  # reflect at boundary
        psi = new_psi
        norms.append(np.sum(np.abs(psi) ** 2))

    return psi, norms


def detector_probs(psi, n_y):
    """Probability at each y: P(y) = |psi_+(y)|^2 + |psi_-(y)|^2."""
    probs = np.zeros(n_y)
    for y in range(n_y):
        probs[y] = abs(psi[2 * y]) ** 2 + abs(psi[2 * y + 1]) ** 2
    return probs


def centroid(probs):
    """Probability-weighted centroid."""
    ys = np.arange(len(probs))
    total = probs.sum()
    if total < 1e-30:
        return len(probs) / 2.0
    return np.sum(ys * probs) / total


# ── TEST 1: Norm preservation ───────────────────────────────────────

def test_norm():
    print("=" * 70)
    print("TEST 1: NORM PRESERVATION")
    print("=" * 70)
    field = make_field(N_LAYERS, N_Y, STRENGTH, MASS_Y)
    psi, norms = chiral_propagate(N_Y, N_LAYERS, K_DEFAULT, field, THETA, SOURCE_Y)
    norms = np.array(norms)
    max_dev = np.max(np.abs(norms - 1.0))
    print(f"  Norms per layer: {norms}")
    print(f"  Max deviation from 1.0: {max_dev:.2e}")
    status = "PASS" if max_dev < 1e-12 else "FAIL"
    print(f"  *** {status} ***")
    return status == "PASS"


# ── TEST 2: Born rule (3-slit I3) ──────────────────────────────────

def test_born():
    print("\n" + "=" * 70)
    print("TEST 2: BORN RULE (3-slit I3)")
    print("=" * 70)

    # Use zero field for Born test (pure quantum walk)
    field = np.zeros((N_LAYERS, N_Y))

    # 3 slits centered around source_y
    slit_positions = [SOURCE_Y - 2, SOURCE_Y, SOURCE_Y + 2]
    all_sites = set(range(N_Y))
    slit_set = set(slit_positions)

    # Barrier: block everything except slit positions
    # The barrier is placed at a specific layer range
    # For simplicity: blocked sites = all sites NOT in the open slits
    barrier_all_blocked = all_sites - slit_set

    def run_config(open_slits):
        """Run with only open_slits unblocked."""
        blocked = all_sites - set(open_slits)
        psi, _ = chiral_propagate(N_Y, N_LAYERS, 0.0, field, THETA, SOURCE_Y,
                                   blocked_sites=blocked)
        return detector_probs(psi, N_Y)

    slits = slit_positions
    A, B, C = slits

    # All 7 configurations
    P_ABC = run_config([A, B, C])
    P_AB = run_config([A, B])
    P_AC = run_config([A, C])
    P_BC = run_config([B, C])
    P_A = run_config([A])
    P_B = run_config([B])
    P_C = run_config([C])

    # Sorkin parameter: I3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C
    I3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C
    I3_max = np.max(np.abs(I3))
    I3_sum = np.sum(np.abs(I3))

    print(f"  Slit positions: {slit_positions}")
    print(f"  I3 max:  {I3_max:.2e}")
    print(f"  I3 sum:  {I3_sum:.2e}")
    print(f"  I3 profile: {I3}")

    status = "PASS" if I3_max < 1e-6 else "FAIL"
    print(f"  *** {status} (threshold 1e-6) ***")
    return status == "PASS"


# ── TEST 3: Gravity direction (single k) ───────────────────────────

def test_gravity():
    print("\n" + "=" * 70)
    print("TEST 3: GRAVITY DIRECTION (single k)")
    print("=" * 70)

    results = {}
    for k in [3.0, 5.0, 7.0, 10.0]:
        # With field
        field = make_field(N_LAYERS, N_Y, STRENGTH, MASS_Y)
        psi_f, _ = chiral_propagate(N_Y, N_LAYERS, k, field, THETA, SOURCE_Y)
        P_f = detector_probs(psi_f, N_Y)
        c_f = centroid(P_f)

        # Without field
        field0 = np.zeros((N_LAYERS, N_Y))
        psi_0, _ = chiral_propagate(N_Y, N_LAYERS, k, field0, THETA, SOURCE_Y)
        P_0 = detector_probs(psi_0, N_Y)
        c_0 = centroid(P_0)

        delta = c_f - c_0
        direction = "TOWARD" if delta < 0 else ("AWAY" if delta > 0 else "NONE")
        # mass at y=4, source at y=8, so TOWARD means delta < 0
        results[k] = (c_0, c_f, delta, direction)
        print(f"  k={k:5.1f}: centroid_0={c_0:.6f}, centroid_f={c_f:.6f}, "
              f"delta={delta:+.6e}, {direction}")

    all_toward = all(r[3] == "TOWARD" for r in results.values())
    any_toward = any(r[3] == "TOWARD" for r in results.values())
    status = "PASS" if all_toward else ("PARTIAL" if any_toward else "FAIL")
    print(f"  *** {status} (all TOWARD = {all_toward}) ***")
    return all_toward


# ── TEST 4: F proportional to M scaling ─────────────────────────────

def test_f_prop_m():
    print("\n" + "=" * 70)
    print("TEST 4: F PROPORTIONAL TO M SCALING")
    print("=" * 70)

    strengths = [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]
    k = K_DEFAULT

    # Reference (no field)
    field0 = np.zeros((N_LAYERS, N_Y))
    psi_0, _ = chiral_propagate(N_Y, N_LAYERS, k, field0, THETA, SOURCE_Y)
    c_0 = centroid(detector_probs(psi_0, N_Y))

    deltas = []
    for s in strengths:
        field = make_field(N_LAYERS, N_Y, s, MASS_Y)
        psi_f, _ = chiral_propagate(N_Y, N_LAYERS, k, field, THETA, SOURCE_Y)
        c_f = centroid(detector_probs(psi_f, N_Y))
        delta = c_f - c_0
        deltas.append(delta)
        print(f"  strength={s:.1e}: delta={delta:+.6e}")

    # Fit log-log: delta = A * strength^alpha
    deltas = np.array(deltas)
    log_s = np.log10(np.array(strengths))

    # Handle sign: if all same sign, fit magnitude
    signs = np.sign(deltas)
    if np.all(signs == signs[0]) and signs[0] != 0:
        log_d = np.log10(np.abs(deltas))
        coeffs = np.polyfit(log_s, log_d, 1)
        alpha = coeffs[0]
        # R^2
        pred = np.polyval(coeffs, log_s)
        ss_res = np.sum((log_d - pred) ** 2)
        ss_tot = np.sum((log_d - np.mean(log_d)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        print(f"\n  Power law fit: alpha = {alpha:.4f} (want 1.00)")
        print(f"  R^2 = {r2:.6f}")
        status = "PASS" if abs(alpha - 1.0) < 0.20 and r2 > 0.95 else "FAIL"
    else:
        print(f"\n  Mixed signs in deltas: {signs}")
        print(f"  Cannot fit clean power law")
        alpha, r2 = float('nan'), 0.0
        status = "FAIL"

    print(f"  *** {status} ***")
    return status == "PASS", alpha, r2


# ── TEST 5: Spectral averaging ──────────────────────────────────────

def test_spectral():
    print("\n" + "=" * 70)
    print("TEST 5: SPECTRAL AVERAGING")
    print("=" * 70)

    ks = np.arange(0.5, 10.5, 0.5)
    field = make_field(N_LAYERS, N_Y, STRENGTH, MASS_Y)
    field0 = np.zeros((N_LAYERS, N_Y))

    # Accumulate detector amplitudes (coherent sum with equal amplitude)
    P_sum_f = np.zeros(N_Y)
    P_sum_0 = np.zeros(N_Y)

    toward_count = 0
    away_count = 0

    for k in ks:
        psi_f, _ = chiral_propagate(N_Y, N_LAYERS, k, field, THETA, SOURCE_Y)
        psi_0, _ = chiral_propagate(N_Y, N_LAYERS, k, field0, THETA, SOURCE_Y)
        P_f = detector_probs(psi_f, N_Y)
        P_0 = detector_probs(psi_0, N_Y)
        P_sum_f += P_f
        P_sum_0 += P_0

        c_f = centroid(P_f)
        c_0 = centroid(P_0)
        delta = c_f - c_0
        if delta < 0:
            toward_count += 1
        elif delta > 0:
            away_count += 1

    c_avg_f = centroid(P_sum_f)
    c_avg_0 = centroid(P_sum_0)
    delta_avg = c_avg_f - c_avg_0
    direction = "TOWARD" if delta_avg < 0 else ("AWAY" if delta_avg > 0 else "NONE")

    print(f"  k range: {ks[0]:.1f} to {ks[-1]:.1f}, {len(ks)} values")
    print(f"  Per-k: {toward_count} TOWARD, {away_count} AWAY")
    print(f"  Averaged centroid_0 = {c_avg_0:.6f}")
    print(f"  Averaged centroid_f = {c_avg_f:.6f}")
    print(f"  Averaged delta = {delta_avg:+.6e}")
    print(f"  Direction: {direction}")

    status = "PASS" if direction == "TOWARD" else "FAIL"
    print(f"  *** {status} ***")
    return status == "PASS"


# ── TEST 6: Signal speed ────────────────────────────────────────────

def test_signal_speed():
    print("\n" + "=" * 70)
    print("TEST 6: SIGNAL SPEED")
    print("=" * 70)

    n_y_big = 41
    n_layers_big = 20
    source = 20  # center
    field = np.zeros((n_layers_big, n_y_big))

    psi = np.zeros(2 * n_y_big, dtype=complex)
    psi[2 * source] = 1.0

    edges = []
    for x in range(n_layers_big):
        # Coin
        for y in range(n_y_big):
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi[idx_p], psi[idx_m]
            psi[idx_p] = np.cos(THETA) * pp - np.sin(THETA) * pm
            psi[idx_m] = np.sin(THETA) * pp + np.cos(THETA) * pm

        # Shift
        new_psi = np.zeros_like(psi)
        for y in range(n_y_big):
            if y + 1 < n_y_big:
                new_psi[2 * (y + 1)] += psi[2 * y]
            else:
                new_psi[2 * y + 1] += psi[2 * y]
            if y - 1 >= 0:
                new_psi[2 * (y - 1) + 1] += psi[2 * y + 1]
            else:
                new_psi[2 * y] += psi[2 * y + 1]
        psi = new_psi

        # Find edge of nonzero amplitude
        probs = np.array([abs(psi[2*y])**2 + abs(psi[2*y+1])**2
                          for y in range(n_y_big)])
        nonzero = np.where(probs > 1e-30)[0]
        if len(nonzero) > 0:
            edge_right = nonzero[-1] - source
            edge_left = source - nonzero[0]
            edge = max(edge_right, edge_left)
        else:
            edge = 0
        edges.append(edge)

    layers = np.arange(1, n_layers_big + 1)
    edges = np.array(edges)

    # Fit: edge = v * layer
    # Signal speed should be <= 1
    if np.any(edges > 0):
        v = np.polyfit(layers, edges, 1)[0]
    else:
        v = 0.0

    print(f"  Layer:  {list(layers[:10])}...")
    print(f"  Edges:  {list(edges[:10])}...")
    print(f"  Fitted speed v = {v:.4f} sites/layer")
    print(f"  Expected: v <= 1.0")

    status = "PASS" if 0.5 < v <= 1.05 else "FAIL"
    print(f"  *** {status} ***")
    return status == "PASS"


# ── TEST 7: Lorentzian split (field-dependent theta) ────────────────

def test_lorentzian():
    print("\n" + "=" * 70)
    print("TEST 7: LORENTZIAN SPLIT (field-dependent theta)")
    print("=" * 70)

    # Lorentzian version: theta(y) = theta0 * (1 - f(y))
    # Near mass, less mixing = more forward-directed = time dilation
    field = make_field(N_LAYERS, N_Y, STRENGTH, MASS_Y)
    field0 = np.zeros((N_LAYERS, N_Y))

    # Build theta field
    theta_field = np.full((N_LAYERS, N_Y), THETA)
    for x in range(N_LAYERS):
        for y in range(N_Y):
            theta_field[x, y] = THETA * (1.0 - field[x, y])

    results = {}
    for k in [3.0, 5.0, 7.0, 10.0]:
        # Lorentzian with field
        psi_f, _ = chiral_propagate(N_Y, N_LAYERS, k, field, THETA, SOURCE_Y,
                                     theta_field=theta_field)
        P_f = detector_probs(psi_f, N_Y)
        c_f = centroid(P_f)

        # Reference: no field, constant theta
        psi_0, _ = chiral_propagate(N_Y, N_LAYERS, k, field0, THETA, SOURCE_Y)
        P_0 = detector_probs(psi_0, N_Y)
        c_0 = centroid(P_0)

        delta = c_f - c_0
        direction = "TOWARD" if delta < 0 else ("AWAY" if delta > 0 else "NONE")
        results[k] = (c_0, c_f, delta, direction)
        print(f"  k={k:5.1f}: centroid_0={c_0:.6f}, centroid_f={c_f:.6f}, "
              f"delta={delta:+.6e}, {direction}")

    # Also test F-prop-M for Lorentzian
    print("\n  Lorentzian F-prop-M scan:")
    strengths = [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]
    k = K_DEFAULT
    c_0_ref = centroid(detector_probs(
        chiral_propagate(N_Y, N_LAYERS, k, field0, THETA, SOURCE_Y)[0], N_Y))

    deltas_lor = []
    for s in strengths:
        f = make_field(N_LAYERS, N_Y, s, MASS_Y)
        tf = np.full((N_LAYERS, N_Y), THETA)
        for x in range(N_LAYERS):
            for y in range(N_Y):
                tf[x, y] = THETA * (1.0 - f[x, y])
        psi_f, _ = chiral_propagate(N_Y, N_LAYERS, k, f, THETA, SOURCE_Y,
                                     theta_field=tf)
        c_f = centroid(detector_probs(psi_f, N_Y))
        delta = c_f - c_0_ref
        deltas_lor.append(delta)
        print(f"    strength={s:.1e}: delta={delta:+.6e}")

    deltas_lor = np.array(deltas_lor)
    signs = np.sign(deltas_lor)
    if np.all(signs == signs[0]) and signs[0] != 0:
        log_s = np.log10(np.array(strengths))
        log_d = np.log10(np.abs(deltas_lor))
        coeffs = np.polyfit(log_s, log_d, 1)
        alpha_lor = coeffs[0]
        pred = np.polyval(coeffs, log_s)
        ss_res = np.sum((log_d - pred) ** 2)
        ss_tot = np.sum((log_d - np.mean(log_d)) ** 2)
        r2_lor = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        print(f"  Lorentzian alpha = {alpha_lor:.4f}, R^2 = {r2_lor:.6f}")
    else:
        alpha_lor, r2_lor = float('nan'), 0.0
        print(f"  Lorentzian: mixed signs, no clean fit")

    all_toward = all(r[3] == "TOWARD" for r in results.values())
    any_toward = any(r[3] == "TOWARD" for r in results.values())
    status = "PASS" if all_toward else ("PARTIAL" if any_toward else "FAIL")
    print(f"  *** {status} (all TOWARD = {all_toward}) ***")
    return status == "PASS"


# ── MAIN ────────────────────────────────────────────────────────────

def main():
    print("FRONTIER: CHIRAL PROPAGATOR")
    print("Architecture: discrete chiral walk, field in coin phase")
    print(f"Parameters: n_y={N_Y}, n_layers={N_LAYERS}, k={K_DEFAULT}, "
          f"theta={THETA}, strength={STRENGTH}")
    print(f"Mass at y={MASS_Y}, source at y={SOURCE_Y}")
    print()

    results = {}

    results['norm'] = test_norm()
    results['born'] = test_born()
    results['gravity'] = test_gravity()
    fm_pass, alpha, r2 = test_f_prop_m()
    results['f_prop_m'] = fm_pass
    results['spectral'] = test_spectral()
    results['signal_speed'] = test_signal_speed()
    results['lorentzian'] = test_lorentzian()

    # ── Summary ─────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for name, passed in results.items():
        tag = "PASS" if passed else "FAIL"
        print(f"  {name:20s}: {tag}")

    all_pass = all(results.values())
    core_pass = results['norm'] and results['born']
    gravity_pass = results['gravity'] and results['f_prop_m']

    print(f"\n  Core (norm + Born):     {'PASS' if core_pass else 'FAIL'}")
    print(f"  Gravity (dir + F-M):   {'PASS' if gravity_pass else 'FAIL'}")
    print(f"  ALL TESTS:             {'PASS' if all_pass else 'FAIL'}")

    if all_pass:
        print("\n  HYPOTHESIS CONFIRMED: Chiral propagator passes all tests.")
    elif core_pass and not gravity_pass:
        print(f"\n  HYPOTHESIS PARTIALLY FALSIFIED: Born OK but gravity fails.")
        print(f"  F-prop-M alpha = {alpha:.4f}, R^2 = {r2:.6f}")
    elif not core_pass:
        print(f"\n  HYPOTHESIS FALSIFIED: Core tests fail.")
    else:
        print(f"\n  MIXED RESULTS: see individual tests above.")


if __name__ == "__main__":
    main()
