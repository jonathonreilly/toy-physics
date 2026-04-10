#!/usr/bin/env python3
"""
Frontier: Chiral Spin — Does Chirality Act as Spin?
=====================================================
The chiral walk has two components (psi_+, psi_-) at each site.
Does this internal DOF behave like spin-1/2?

Tests:
  1. Chirality conservation in flat space
  2. Stern-Gerlach: field gradient separates psi_+ from psi_-
  3. Chirality precession in uniform field
  4. Chirality-dependent deflection by localized mass

Uses Lorentzian chiral walk: theta(y) = theta_0 * (1 - f(y)),
reflecting boundaries.

HYPOTHESIS: "Chirality acts as a spin-like DOF: field gradient
separates psi_+ from psi_-."
FALSIFICATION: "If psi_+ and psi_- always have the same spatial
distribution regardless of field configuration."
"""

from __future__ import annotations
import numpy as np
import time


# ── Parameters ──────────────────────────────────────────────────────
N_Y = 31
N_LAYERS = 24
THETA_0 = 0.3
K = 5.0
STRENGTH = 5e-4
SOURCE_Y = N_Y // 2  # = 15
MASS_Y = 19           # offset 4 from center


# ── Core Propagator ─────────────────────────────────────────────────

def propagate_chiral(n_y, n_layers, theta_0, field, source_y,
                     source_plus=1.0, source_minus=0.0):
    """
    Lorentzian chiral walk.

    theta(y) = theta_0 * (1 - f(x,y))
    Reflecting boundaries.

    Returns: psi array of shape (2*n_y,) complex
             psi[2*y] = psi_+(y), psi[2*y+1] = psi_-(y)
    """
    psi = np.zeros(2 * n_y, dtype=complex)
    psi[2 * source_y] = source_plus
    psi[2 * source_y + 1] = source_minus

    # Normalize initial state
    norm0 = np.sqrt(abs(source_plus)**2 + abs(source_minus)**2)
    if norm0 > 1e-30:
        psi[2 * source_y] /= norm0
        psi[2 * source_y + 1] /= norm0

    for x in range(n_layers):
        # Step 1: Coin at each site
        for y in range(n_y):
            f = field[x, y] if field is not None else 0.0
            th = theta_0 * (1.0 - f)
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi[idx_p], psi[idx_m]
            c, s = np.cos(th), np.sin(th)
            psi[idx_p] = c * pp - s * pm
            psi[idx_m] = s * pp + c * pm

        # Step 2: Shift with reflecting boundaries
        new_psi = np.zeros_like(psi)
        for y in range(n_y):
            # Right-mover (psi_+) shifts right
            if y + 1 < n_y:
                new_psi[2 * (y + 1)] += psi[2 * y]
            else:
                new_psi[2 * y + 1] += psi[2 * y]  # reflect: becomes left-mover
            # Left-mover (psi_-) shifts left
            if y - 1 >= 0:
                new_psi[2 * (y - 1) + 1] += psi[2 * y + 1]
            else:
                new_psi[2 * y] += psi[2 * y + 1]  # reflect: becomes right-mover
        psi = new_psi

    return psi


# ── Field Constructors ──────────────────────────────────────────────

def make_field_flat(n_layers, n_y):
    """Zero field everywhere."""
    return np.zeros((n_layers, n_y))


def make_field_gradient(n_layers, n_y, gradient):
    """Linear field: f(y) = gradient * (y - center)."""
    center = n_y // 2
    field = np.zeros((n_layers, n_y))
    for y in range(n_y):
        field[:, y] = gradient * (y - center)
    return field


def make_field_uniform(n_layers, n_y, f_const):
    """Uniform field: f = constant everywhere."""
    return np.full((n_layers, n_y), f_const)


def make_field_mass(n_layers, n_y, mass_y, strength):
    """1/r field from localized mass."""
    field = np.zeros((n_layers, n_y))
    for y in range(n_y):
        field[:, y] = strength / (abs(y - mass_y) + 0.1)
    return field


# ── Measurement Utilities ───────────────────────────────────────────

def chirality_probs(psi, n_y):
    """Return (P_plus[y], P_minus[y]) arrays."""
    P_plus = np.zeros(n_y)
    P_minus = np.zeros(n_y)
    for y in range(n_y):
        P_plus[y] = abs(psi[2 * y]) ** 2
        P_minus[y] = abs(psi[2 * y + 1]) ** 2
    return P_plus, P_minus


def total_probs(psi, n_y):
    """P(y) = |psi_+(y)|^2 + |psi_-(y)|^2."""
    P_plus, P_minus = chirality_probs(psi, n_y)
    return P_plus + P_minus


def centroid(probs):
    """Probability-weighted centroid."""
    ys = np.arange(len(probs))
    total = probs.sum()
    if total < 1e-30:
        return len(probs) / 2.0
    return np.dot(ys, probs) / total


def chirality_fraction(psi, n_y):
    """Return (total_plus, total_minus, fraction_plus)."""
    P_plus, P_minus = chirality_probs(psi, n_y)
    tp = P_plus.sum()
    tm = P_minus.sum()
    total = tp + tm
    if total < 1e-30:
        return tp, tm, 0.5
    return tp, tm, tp / total


# ── TEST 1: Chirality Conservation in Flat Space ────────────────────

def test_chirality_conservation():
    print("=" * 70)
    print("TEST 1: CHIRALITY CONSERVATION IN FLAT SPACE")
    print("=" * 70)
    print("  Propagate pure psi_+ in flat space.")
    print("  If chirality is conserved, psi_+ fraction stays near initial.\n")

    field = make_field_flat(N_LAYERS, N_Y)

    # Pure psi_+ source
    psi = propagate_chiral(N_Y, N_LAYERS, THETA_0, field, SOURCE_Y,
                           source_plus=1.0, source_minus=0.0)
    tp, tm, frac_plus = chirality_fraction(psi, N_Y)

    print(f"  Initial chirality: 100% psi_+")
    print(f"  Final P(psi_+) = {tp:.6f}")
    print(f"  Final P(psi_-) = {tm:.6f}")
    print(f"  Fraction psi_+: {frac_plus:.6f}")
    print(f"  Total norm: {tp + tm:.6f}")

    # Also check psi_- source
    psi_m = propagate_chiral(N_Y, N_LAYERS, THETA_0, field, SOURCE_Y,
                             source_plus=0.0, source_minus=1.0)
    tp_m, tm_m, frac_plus_m = chirality_fraction(psi_m, N_Y)

    print(f"\n  Pure psi_- source:")
    print(f"  Final P(psi_+) = {tp_m:.6f}")
    print(f"  Final P(psi_-) = {tm_m:.6f}")
    print(f"  Fraction psi_+: {frac_plus_m:.6f}")

    # Check layer-by-layer evolution
    print(f"\n  Layer-by-layer chirality fraction (psi_+ source):")
    psi_evo = np.zeros(2 * N_Y, dtype=complex)
    psi_evo[2 * SOURCE_Y] = 1.0
    field_flat = make_field_flat(N_LAYERS, N_Y)
    fracs = []
    for x in range(N_LAYERS):
        for y in range(N_Y):
            th = THETA_0
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi_evo[idx_p], psi_evo[idx_m]
            c, s = np.cos(th), np.sin(th)
            psi_evo[idx_p] = c * pp - s * pm
            psi_evo[idx_m] = s * pp + c * pm
        new_psi = np.zeros_like(psi_evo)
        for y in range(N_Y):
            if y + 1 < N_Y:
                new_psi[2 * (y + 1)] += psi_evo[2 * y]
            else:
                new_psi[2 * y + 1] += psi_evo[2 * y]
            if y - 1 >= 0:
                new_psi[2 * (y - 1) + 1] += psi_evo[2 * y + 1]
            else:
                new_psi[2 * y] += psi_evo[2 * y + 1]
        psi_evo = new_psi
        tp_x = sum(abs(psi_evo[2*y])**2 for y in range(N_Y))
        tm_x = sum(abs(psi_evo[2*y+1])**2 for y in range(N_Y))
        tot_x = tp_x + tm_x
        frac_x = tp_x / tot_x if tot_x > 1e-30 else 0.5
        fracs.append(frac_x)
        if x < 10 or x == N_LAYERS - 1:
            print(f"    Layer {x+1:2d}: frac_+ = {frac_x:.6f}, "
                  f"P_+ = {tp_x:.6f}, P_- = {tm_x:.6f}")

    conserved = abs(frac_plus - 1.0) < 0.01
    # Actually check if chirality is NOT conserved (mixing happens)
    mixing = abs(frac_plus - 1.0)
    print(f"\n  Chirality mixing: {mixing:.6f}")
    if conserved:
        print(f"  *** CONSERVED (mixing < 1%) ***")
    else:
        print(f"  *** NOT CONSERVED (mixing = {mixing*100:.1f}%) ***")
        print(f"  The coin mixes psi_+ and psi_- every layer.")

    return frac_plus, fracs


# ── TEST 2: Stern-Gerlach — Field Gradient Separates Chiralities ────

def test_stern_gerlach():
    print("\n" + "=" * 70)
    print("TEST 2: STERN-GERLACH (Field Gradient)")
    print("=" * 70)
    print("  Apply linear gradient: f = gradient * (y - center)")
    print("  Mixed source (equal psi_+ and psi_-).")
    print("  Measure centroid separation of psi_+ vs psi_-.\n")

    gradients = [0.0, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2]

    results = []
    for grad in gradients:
        field = make_field_gradient(N_LAYERS, N_Y, grad)

        # Mixed source: equal psi_+ and psi_-
        psi = propagate_chiral(N_Y, N_LAYERS, THETA_0, field, SOURCE_Y,
                               source_plus=1.0, source_minus=1.0)

        P_plus, P_minus = chirality_probs(psi, N_Y)
        c_plus = centroid(P_plus)
        c_minus = centroid(P_minus)
        c_total = centroid(P_plus + P_minus)
        separation = c_plus - c_minus

        results.append({
            'gradient': grad,
            'c_plus': c_plus,
            'c_minus': c_minus,
            'c_total': c_total,
            'separation': separation,
            'P_plus_total': P_plus.sum(),
            'P_minus_total': P_minus.sum(),
        })

        print(f"  gradient={grad:.1e}: c_+ = {c_plus:.4f}, c_- = {c_minus:.4f}, "
              f"sep = {separation:+.6f}, P_+ = {P_plus.sum():.4f}, P_- = {P_minus.sum():.4f}")

    # Check if separation increases with gradient
    seps = [r['separation'] for r in results]
    seps_nonzero = [r for r in results if r['gradient'] > 0]
    if len(seps_nonzero) >= 2:
        sep_magnitudes = [abs(r['separation']) for r in seps_nonzero]
        increasing = all(sep_magnitudes[i+1] >= sep_magnitudes[i] * 0.9
                        for i in range(len(sep_magnitudes)-1))
    else:
        increasing = False

    max_sep = max(abs(r['separation']) for r in results)
    print(f"\n  Max |separation|: {max_sep:.6f}")
    print(f"  Separation increases with gradient: {increasing}")

    if max_sep > 0.01:
        print(f"  *** STERN-GERLACH EFFECT DETECTED ***")
        print(f"  Field gradient separates psi_+ from psi_-.")
        status = "DETECTED"
    else:
        print(f"  *** NO SIGNIFICANT SEPARATION ***")
        print(f"  psi_+ and psi_- have similar spatial distributions.")
        status = "NOT_DETECTED"

    # Detailed profile for strongest gradient
    print(f"\n  Spatial profile at gradient={gradients[-1]:.1e}:")
    field_strong = make_field_gradient(N_LAYERS, N_Y, gradients[-1])
    psi_strong = propagate_chiral(N_Y, N_LAYERS, THETA_0, field_strong, SOURCE_Y,
                                   source_plus=1.0, source_minus=1.0)
    P_p, P_m = chirality_probs(psi_strong, N_Y)
    for y in range(N_Y):
        if P_p[y] > 1e-6 or P_m[y] > 1e-6:
            ratio = P_p[y] / P_m[y] if P_m[y] > 1e-15 else float('inf')
            print(f"    y={y:2d}: P_+={P_p[y]:.6f}, P_-={P_m[y]:.6f}, +/- ratio={ratio:.3f}")

    return results, status


# ── TEST 3: Chirality Precession in Uniform Field ───────────────────

def test_chirality_precession():
    print("\n" + "=" * 70)
    print("TEST 3: CHIRALITY PRECESSION (Uniform Field)")
    print("=" * 70)
    print("  Uniform field: f = constant everywhere.")
    print("  Pure psi_+ source. Measure psi_+/psi_- ratio vs f*L.\n")

    f_values = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5]

    results = []
    for f_const in f_values:
        field = make_field_uniform(N_LAYERS, N_Y, f_const)

        # Pure psi_+ source
        psi = propagate_chiral(N_Y, N_LAYERS, THETA_0, field, SOURCE_Y,
                               source_plus=1.0, source_minus=0.0)
        tp, tm, frac_plus = chirality_fraction(psi, N_Y)
        fL = f_const * N_LAYERS

        results.append({
            'f_const': f_const,
            'fL': fL,
            'frac_plus': frac_plus,
            'P_plus': tp,
            'P_minus': tm,
            'norm': tp + tm,
        })

        print(f"  f={f_const:.3f}, f*L={fL:6.2f}: frac_+ = {frac_plus:.6f}, "
              f"P_+ = {tp:.6f}, P_- = {tm:.6f}, norm = {tp+tm:.6f}")

    # Check if fraction depends on f
    fracs = [r['frac_plus'] for r in results]
    frac_range = max(fracs) - min(fracs)
    frac_flat = frac_range < 0.01

    # Check if there's precession-like oscillation
    # In true precession, frac_+ = cos^2(f*L * something)
    print(f"\n  Fraction range: {frac_range:.6f}")
    print(f"  Flat-space fraction: {fracs[0]:.6f}")

    if frac_range > 0.05:
        print(f"  *** PRECESSION-LIKE BEHAVIOR ***")
        print(f"  Chirality fraction depends on uniform field strength.")
        # Check if it follows cos^2 pattern
        print(f"\n  Checking cos^2(theta_eff * f * L) fit:")
        fLs = np.array([r['fL'] for r in results if r['f_const'] > 0])
        fps = np.array([r['frac_plus'] for r in results if r['f_const'] > 0])
        # In the Lorentzian model, theta -> theta*(1-f), so effective mixing
        # changes. The psi_+/psi_- ratio depends on accumulated mixing.
        status = "PRECESSION"
    elif frac_range > 0.01:
        print(f"  *** WEAK DEPENDENCE ***")
        print(f"  Some chirality rotation but not strong precession.")
        status = "WEAK"
    else:
        print(f"  *** NO PRECESSION ***")
        print(f"  Chirality fraction independent of uniform field.")
        status = "NONE"

    return results, status


# ── TEST 4: Chirality-Dependent Deflection ──────────────────────────

def test_chirality_deflection():
    print("\n" + "=" * 70)
    print("TEST 4: CHIRALITY-DEPENDENT DEFLECTION")
    print("=" * 70)
    print(f"  Localized mass at y={MASS_Y} (offset {MASS_Y - SOURCE_Y} from center).")
    print(f"  Compare deflection of psi_+, psi_-, and mixed sources.\n")

    field_mass = make_field_mass(N_LAYERS, N_Y, MASS_Y, STRENGTH)
    field_flat = make_field_flat(N_LAYERS, N_Y)

    # Reference: no field
    psi_ref_p = propagate_chiral(N_Y, N_LAYERS, THETA_0, field_flat, SOURCE_Y,
                                  source_plus=1.0, source_minus=0.0)
    psi_ref_m = propagate_chiral(N_Y, N_LAYERS, THETA_0, field_flat, SOURCE_Y,
                                  source_plus=0.0, source_minus=1.0)
    psi_ref_mix = propagate_chiral(N_Y, N_LAYERS, THETA_0, field_flat, SOURCE_Y,
                                    source_plus=1.0, source_minus=1.0)

    c_ref_p = centroid(total_probs(psi_ref_p, N_Y))
    c_ref_m = centroid(total_probs(psi_ref_m, N_Y))
    c_ref_mix = centroid(total_probs(psi_ref_mix, N_Y))

    # With mass field
    psi_mass_p = propagate_chiral(N_Y, N_LAYERS, THETA_0, field_mass, SOURCE_Y,
                                   source_plus=1.0, source_minus=0.0)
    psi_mass_m = propagate_chiral(N_Y, N_LAYERS, THETA_0, field_mass, SOURCE_Y,
                                   source_plus=0.0, source_minus=1.0)
    psi_mass_mix = propagate_chiral(N_Y, N_LAYERS, THETA_0, field_mass, SOURCE_Y,
                                     source_plus=1.0, source_minus=1.0)

    c_mass_p = centroid(total_probs(psi_mass_p, N_Y))
    c_mass_m = centroid(total_probs(psi_mass_m, N_Y))
    c_mass_mix = centroid(total_probs(psi_mass_mix, N_Y))

    delta_p = c_mass_p - c_ref_p
    delta_m = c_mass_m - c_ref_m
    delta_mix = c_mass_mix - c_ref_mix

    # Mass at y=19, source at y=15, so TOWARD means delta > 0
    dir_p = "TOWARD" if delta_p > 1e-8 else ("AWAY" if delta_p < -1e-8 else "NONE")
    dir_m = "TOWARD" if delta_m > 1e-8 else ("AWAY" if delta_m < -1e-8 else "NONE")
    dir_mix = "TOWARD" if delta_mix > 1e-8 else ("AWAY" if delta_mix < -1e-8 else "NONE")

    print(f"  Source type       | ref centroid | mass centroid | delta      | direction")
    print(f"  " + "-" * 75)
    print(f"  Pure psi_+        | {c_ref_p:12.6f} | {c_mass_p:13.6f} | {delta_p:+10.6e} | {dir_p}")
    print(f"  Pure psi_-        | {c_ref_m:12.6f} | {c_mass_m:13.6f} | {delta_m:+10.6e} | {dir_m}")
    print(f"  Mixed (equal)     | {c_ref_mix:12.6f} | {c_mass_mix:13.6f} | {delta_mix:+10.6e} | {dir_mix}")

    # Check chirality-dependent force
    diff_pm = delta_p - delta_m
    avg_pm = 0.5 * (delta_p + delta_m)

    print(f"\n  Deflection difference (delta_+ - delta_-): {diff_pm:+.6e}")
    print(f"  Average deflection (delta_+ + delta_-)/2:  {avg_pm:+.6e}")
    print(f"  Mixed deflection delta_mix:                {delta_mix:+.6e}")
    print(f"  Deviation from average: {abs(delta_mix - avg_pm):.6e}")

    # Chirality-resolved analysis of the mass-field case
    print(f"\n  Chirality-resolved analysis (with mass):")
    for label, psi_test in [("psi_+ source", psi_mass_p),
                             ("psi_- source", psi_mass_m),
                             ("mixed source", psi_mass_mix)]:
        Pp, Pm = chirality_probs(psi_test, N_Y)
        c_chirp = centroid(Pp)
        c_chirm = centroid(Pm)
        tp_tot = Pp.sum()
        tm_tot = Pm.sum()
        print(f"    {label:15s}: c(+)={c_chirp:.4f}, c(-)={c_chirm:.4f}, "
              f"P_+={tp_tot:.4f}, P_-={tm_tot:.4f}, "
              f"sep={c_chirp - c_chirm:+.6f}")

    if abs(diff_pm) > 1e-6:
        print(f"\n  *** CHIRALITY-DEPENDENT DEFLECTION DETECTED ***")
        print(f"  psi_+ and psi_- experience different gravitational deflection.")
        status = "DETECTED"
    else:
        print(f"\n  *** CHIRALITY-INDEPENDENT DEFLECTION ***")
        print(f"  psi_+ and psi_- deflect identically.")
        status = "INDEPENDENT"

    # Scan over multiple mass positions
    print(f"\n  Mass position scan (delta_+ vs delta_-):")
    print(f"  {'mass_y':>6} | {'delta_+':>12} | {'delta_-':>12} | {'diff':>12} | {'dir_+':>6} | {'dir_-':>6}")
    print(f"  " + "-" * 70)
    for my in [SOURCE_Y + 2, SOURCE_Y + 4, SOURCE_Y + 6, SOURCE_Y + 8]:
        if my >= N_Y:
            continue
        fm = make_field_mass(N_LAYERS, N_Y, my, STRENGTH)
        psi_p = propagate_chiral(N_Y, N_LAYERS, THETA_0, fm, SOURCE_Y,
                                  source_plus=1.0, source_minus=0.0)
        psi_m = propagate_chiral(N_Y, N_LAYERS, THETA_0, fm, SOURCE_Y,
                                  source_plus=0.0, source_minus=1.0)
        dp = centroid(total_probs(psi_p, N_Y)) - c_ref_p
        dm = centroid(total_probs(psi_m, N_Y)) - c_ref_m
        d_p = "TOWARD" if dp > 1e-8 else ("AWAY" if dp < -1e-8 else "NONE")
        d_m = "TOWARD" if dm > 1e-8 else ("AWAY" if dm < -1e-8 else "NONE")
        print(f"  {my:6d} | {dp:+12.6e} | {dm:+12.6e} | {dp-dm:+12.6e} | {d_p:>6} | {d_m:>6}")

    return delta_p, delta_m, delta_mix, status


# ── TEST 5: Chirality as Conserved Quantum Number? ──────────────────

def test_chirality_quantum_number():
    print("\n" + "=" * 70)
    print("TEST 5: CHIRALITY COMMUTATION WITH HAMILTONIAN")
    print("=" * 70)
    print("  Check if chirality operator C = sum_y (|+><+| - |-><-|)")
    print("  commutes with the evolution. If [H, C] = 0, chirality is conserved.\n")

    field = make_field_flat(N_LAYERS, N_Y)

    # Track chirality expectation value layer-by-layer for different initial states
    init_states = [
        ("pure_+", 1.0, 0.0),
        ("pure_-", 0.0, 1.0),
        ("equal_mix", 1.0, 1.0),
        ("phase_mix", 1.0, 1j),
        ("anti_mix", 1.0, -1.0),
    ]

    for label, sp, sm in init_states:
        # Normalize
        norm = np.sqrt(abs(sp)**2 + abs(sm)**2)
        sp_n, sm_n = sp / norm, sm / norm

        psi = np.zeros(2 * N_Y, dtype=complex)
        psi[2 * SOURCE_Y] = sp_n
        psi[2 * SOURCE_Y + 1] = sm_n

        chirality_vals = []
        for x in range(N_LAYERS):
            # Measure chirality: <C> = sum_y (|psi_+(y)|^2 - |psi_-(y)|^2)
            c_val = sum(abs(psi[2*y])**2 - abs(psi[2*y+1])**2 for y in range(N_Y))
            chirality_vals.append(c_val)

            # Coin
            for y in range(N_Y):
                th = THETA_0
                idx_p = 2 * y
                idx_m = 2 * y + 1
                pp, pm = psi[idx_p], psi[idx_m]
                c, s = np.cos(th), np.sin(th)
                psi[idx_p] = c * pp - s * pm
                psi[idx_m] = s * pp + c * pm

            # Shift
            new_psi = np.zeros_like(psi)
            for y in range(N_Y):
                if y + 1 < N_Y:
                    new_psi[2 * (y + 1)] += psi[2 * y]
                else:
                    new_psi[2 * y + 1] += psi[2 * y]
                if y - 1 >= 0:
                    new_psi[2 * (y - 1) + 1] += psi[2 * y + 1]
                else:
                    new_psi[2 * y] += psi[2 * y + 1]
            psi = new_psi

        # Final chirality
        c_final = sum(abs(psi[2*y])**2 - abs(psi[2*y+1])**2 for y in range(N_Y))
        chirality_vals.append(c_final)

        c_range = max(chirality_vals) - min(chirality_vals)
        print(f"  {label:15s}: <C> initial = {chirality_vals[0]:+.6f}, "
              f"final = {chirality_vals[-1]:+.6f}, "
              f"range = {c_range:.6f}")

    # Now with mass field
    print(f"\n  With mass field (strength={STRENGTH}):")
    field_mass = make_field_mass(N_LAYERS, N_Y, MASS_Y, STRENGTH)

    for label, sp, sm in init_states[:3]:
        norm = np.sqrt(abs(sp)**2 + abs(sm)**2)
        sp_n, sm_n = sp / norm, sm / norm

        psi = np.zeros(2 * N_Y, dtype=complex)
        psi[2 * SOURCE_Y] = sp_n
        psi[2 * SOURCE_Y + 1] = sm_n

        chirality_vals = []
        for x in range(N_LAYERS):
            c_val = sum(abs(psi[2*y])**2 - abs(psi[2*y+1])**2 for y in range(N_Y))
            chirality_vals.append(c_val)

            for y in range(N_Y):
                f = field_mass[x, y]
                th = THETA_0 * (1.0 - f)
                idx_p = 2 * y
                idx_m = 2 * y + 1
                pp, pm = psi[idx_p], psi[idx_m]
                c, s = np.cos(th), np.sin(th)
                psi[idx_p] = c * pp - s * pm
                psi[idx_m] = s * pp + c * pm

            new_psi = np.zeros_like(psi)
            for y in range(N_Y):
                if y + 1 < N_Y:
                    new_psi[2 * (y + 1)] += psi[2 * y]
                else:
                    new_psi[2 * y + 1] += psi[2 * y]
                if y - 1 >= 0:
                    new_psi[2 * (y - 1) + 1] += psi[2 * y + 1]
                else:
                    new_psi[2 * y] += psi[2 * y + 1]
            psi = new_psi

        c_final = sum(abs(psi[2*y])**2 - abs(psi[2*y+1])**2 for y in range(N_Y))
        chirality_vals.append(c_final)
        c_range = max(chirality_vals) - min(chirality_vals)
        print(f"  {label:15s}: <C> initial = {chirality_vals[0]:+.6f}, "
              f"final = {chirality_vals[-1]:+.6f}, "
              f"range = {c_range:.6f}")


# ── MAIN ────────────────────────────────────────────────────────────

def main():
    t0 = time.time()
    print("FRONTIER: CHIRAL SPIN — Does Chirality Act as Spin?")
    print(f"Parameters: n_y={N_Y}, n_layers={N_LAYERS}, theta_0={THETA_0}")
    print(f"Source at y={SOURCE_Y}, mass at y={MASS_Y}")
    print(f"Strength={STRENGTH}")
    print()

    # Test 1: Conservation
    frac_plus, fracs = test_chirality_conservation()

    # Test 2: Stern-Gerlach
    sg_results, sg_status = test_stern_gerlach()

    # Test 3: Precession
    prec_results, prec_status = test_chirality_precession()

    # Test 4: Chirality-dependent deflection
    delta_p, delta_m, delta_mix, defl_status = test_chirality_deflection()

    # Test 5: Commutation check
    test_chirality_quantum_number()

    # ── SUMMARY ─────────────────────────────────────────────────────
    elapsed = time.time() - t0
    print(f"\n{'=' * 70}")
    print(f"SUMMARY (runtime: {elapsed:.1f}s)")
    print(f"{'=' * 70}")

    print(f"\n  Test 1 — Chirality conservation (flat):")
    print(f"    Final psi_+ fraction from pure psi_+ source: {frac_plus:.6f}")
    mixing_pct = abs(frac_plus - 1.0) * 100
    if mixing_pct < 1:
        print(f"    CONSERVED (mixing {mixing_pct:.1f}% < 1%)")
    else:
        print(f"    NOT CONSERVED (mixing {mixing_pct:.1f}%)")
        print(f"    Coin mixes chiralities at every step (like spin precession in B-field).")

    print(f"\n  Test 2 — Stern-Gerlach (field gradient):")
    print(f"    Status: {sg_status}")
    if sg_status == "DETECTED":
        max_sep = max(abs(r['separation']) for r in sg_results)
        print(f"    Max centroid separation: {max_sep:.6f}")
    else:
        print(f"    No spatial separation of chiralities by gradient.")

    print(f"\n  Test 3 — Chirality precession (uniform field):")
    print(f"    Status: {prec_status}")
    if prec_status in ("PRECESSION", "WEAK"):
        fracs_p = [r['frac_plus'] for r in prec_results]
        print(f"    Fraction range: {min(fracs_p):.6f} to {max(fracs_p):.6f}")

    print(f"\n  Test 4 — Chirality-dependent deflection:")
    print(f"    Status: {defl_status}")
    print(f"    delta_+ = {delta_p:+.6e}")
    print(f"    delta_- = {delta_m:+.6e}")
    print(f"    delta_mix = {delta_mix:+.6e}")
    print(f"    Difference (delta_+ - delta_-) = {delta_p - delta_m:+.6e}")

    # Overall verdict
    print(f"\n  VERDICT:")
    spin_like = (sg_status == "DETECTED" or
                 prec_status in ("PRECESSION", "WEAK") or
                 defl_status == "DETECTED")

    if spin_like:
        print(f"    HYPOTHESIS SUPPORTED: Chirality has spin-like properties.")
        if sg_status == "DETECTED":
            print(f"    - Field gradient spatially separates psi_+ from psi_-.")
        if prec_status in ("PRECESSION", "WEAK"):
            print(f"    - Uniform field rotates chirality (precession).")
        if defl_status == "DETECTED":
            print(f"    - Gravitational deflection depends on chirality.")
        if mixing_pct > 1:
            print(f"    CAVEAT: Chirality is NOT conserved in flat space either!")
            print(f"    The coin always mixes chiralities, so chirality is not a")
            print(f"    good quantum number. It is more like a DYNAMICAL variable")
            print(f"    than a conserved charge.")
    else:
        print(f"    HYPOTHESIS FALSIFIED: Chirality does not behave as spin.")
        print(f"    psi_+ and psi_- have the same spatial distribution")
        print(f"    regardless of field configuration.")


if __name__ == "__main__":
    main()
