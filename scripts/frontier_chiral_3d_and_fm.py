#!/usr/bin/env python3
"""
Frontier: 3D Chiral Propagator + F-prop-M Diagnosis
=====================================================

TWO TESTS IN ONE SCRIPT:

Part 1: 3D Chiral Propagator (2+1D spacetime)
  Extend the chiral walk to 2 transverse dimensions (y, z).
  State at each (y,z): 4 components (psi_+y, psi_-y, psi_+z, psi_-z).
  Per layer:
    Step 1: Coin at each site -- pairwise 2x2 mixings
    Step 2: Shift -- each chirality moves 1 step in its direction

Part 2: F-prop-M Diagnosis
  Phase coupling: field enters exp(i*k*f) -- probability |exp(ikf)|^2=1
    -> first-order centroid shift vanishes, leading effect is O(f^2) -> alpha=2
  Theta coupling: field enters sin(theta*(1-f)) -- changes magnitude directly
    -> first-order centroid shift proportional to f -> alpha=1
  Verify numerically with sweeps.

HYPOTHESIS: "3D chiral walk gives TOWARD gravity with F-prop-M=1.0
(Lorentzian theta coupling)."
FALSIFICATION: "If 3D is AWAY or F-prop-M deviates."
"""

import numpy as np

# ====================================================================
# PART 1: 3D CHIRAL PROPAGATOR
# ====================================================================

# ── Parameters ─────────────────────────────────────────────────────
N_YZ = 13          # 13x13 transverse grid
N_LAYERS_3D = 15   # fewer layers for speed
K_DEFAULT = 5.0
THETA_0 = 0.3
STRENGTH_3D = 5e-4
MASS_Z = 3          # mass at z=3 (spatial field in z only)
SOURCE_Y = 6        # center-ish
SOURCE_Z = 6


def make_field_3d(n_layers, n_yz, strength, mass_z):
    """1/r field from a mass at z=mass_z (spatial only, no y dependence)."""
    field = np.zeros((n_layers, n_yz, n_yz))
    for x in range(n_layers):
        for y in range(n_yz):
            for z in range(n_yz):
                field[x, y, z] = strength / (abs(z - mass_z) + 0.1)
    return field


def chiral_propagate_3d(n_yz, n_layers, k, field_3d, theta_0, source_y, source_z,
                        mode="theta"):
    """
    Propagate 3D chiral walk with 4 components per site.

    State vector: length 4*n_yz*n_yz
    Index: 4*(y*n_yz + z) + c, where c in {0,1,2,3}
      c=0: psi_+y (right in y)
      c=1: psi_-y (left in y)
      c=2: psi_+z (right in z)
      c=3: psi_-z (left in z)

    mode: "theta" (Lorentzian, field in theta) or "phase" (field in exp(ikf))
    """
    dim = 4 * n_yz * n_yz
    psi = np.zeros(dim, dtype=complex)
    # Initialize: equal superposition of +y and +z at source
    src_idx = 4 * (source_y * n_yz + source_z)
    psi[src_idx + 0] = 1.0 / np.sqrt(2)  # +y
    psi[src_idx + 2] = 1.0 / np.sqrt(2)  # +z

    norms = []
    for x in range(n_layers):
        # Step 1: Coin at each site
        for y in range(n_yz):
            for z in range(n_yz):
                f = field_3d[x, y, z]
                base = 4 * (y * n_yz + z)

                if mode == "theta":
                    th_y = theta_0 * (1.0 - f)
                    th_z = theta_0 * (1.0 - f)
                    phi_y = 0.0
                    phi_z = 0.0
                elif mode == "phase":
                    th_y = theta_0
                    th_z = theta_0
                    phi_y = k * f
                    phi_z = k * f
                else:
                    th_y = theta_0
                    th_z = theta_0
                    phi_y = 0.0
                    phi_z = 0.0

                # Mix (psi_+y, psi_-y) with theta_y, phi_y
                p_py = psi[base + 0]
                p_my = psi[base + 1]
                psi[base + 0] = (np.cos(th_y) * p_py
                                 - np.sin(th_y) * np.exp(1j * phi_y) * p_my)
                psi[base + 1] = (np.sin(th_y) * np.exp(-1j * phi_y) * p_py
                                 + np.cos(th_y) * p_my)

                # Mix (psi_+z, psi_-z) with theta_z, phi_z
                p_pz = psi[base + 2]
                p_mz = psi[base + 3]
                psi[base + 2] = (np.cos(th_z) * p_pz
                                 - np.sin(th_z) * np.exp(1j * phi_z) * p_mz)
                psi[base + 3] = (np.sin(th_z) * np.exp(-1j * phi_z) * p_pz
                                 + np.cos(th_z) * p_mz)

        # Step 2: Shift
        new_psi = np.zeros_like(psi)
        for y in range(n_yz):
            for z in range(n_yz):
                base = 4 * (y * n_yz + z)

                # psi_+y moves to (y+1, z)
                if y + 1 < n_yz:
                    dst = 4 * ((y + 1) * n_yz + z)
                    new_psi[dst + 0] += psi[base + 0]
                else:
                    # Reflect: +y becomes -y at same site
                    new_psi[base + 1] += psi[base + 0]

                # psi_-y moves to (y-1, z)
                if y - 1 >= 0:
                    dst = 4 * ((y - 1) * n_yz + z)
                    new_psi[dst + 1] += psi[base + 1]
                else:
                    new_psi[base + 0] += psi[base + 1]

                # psi_+z moves to (y, z+1)
                if z + 1 < n_yz:
                    dst = 4 * (y * n_yz + (z + 1))
                    new_psi[dst + 2] += psi[base + 2]
                else:
                    new_psi[base + 3] += psi[base + 2]

                # psi_-z moves to (y, z-1)
                if z - 1 >= 0:
                    dst = 4 * (y * n_yz + (z - 1))
                    new_psi[dst + 3] += psi[base + 3]
                else:
                    new_psi[base + 2] += psi[base + 3]

        psi = new_psi
        norms.append(np.sum(np.abs(psi) ** 2))

    return psi, norms


def detector_probs_3d(psi, n_yz):
    """Probability at each (y, z): sum over all 4 chiralities."""
    probs = np.zeros((n_yz, n_yz))
    for y in range(n_yz):
        for z in range(n_yz):
            base = 4 * (y * n_yz + z)
            probs[y, z] = sum(abs(psi[base + c]) ** 2 for c in range(4))
    return probs


def centroid_z(probs_2d):
    """Probability-weighted centroid in z direction."""
    n_y, n_z = probs_2d.shape
    total = probs_2d.sum()
    if total < 1e-30:
        return n_z / 2.0
    z_marginal = probs_2d.sum(axis=0)  # sum over y -> P(z)
    zs = np.arange(n_z)
    return np.sum(zs * z_marginal) / total


def centroid_y(probs_2d):
    """Probability-weighted centroid in y direction."""
    n_y, n_z = probs_2d.shape
    total = probs_2d.sum()
    if total < 1e-30:
        return n_y / 2.0
    y_marginal = probs_2d.sum(axis=1)  # sum over z -> P(y)
    ys = np.arange(n_y)
    return np.sum(ys * y_marginal) / total


# ── TEST 1a: 3D Norm preservation ──────────────────────────────────

def test_3d_norm():
    print("=" * 70)
    print("TEST 1a: 3D NORM PRESERVATION")
    print("=" * 70)
    field = make_field_3d(N_LAYERS_3D, N_YZ, STRENGTH_3D, MASS_Z)
    psi, norms = chiral_propagate_3d(N_YZ, N_LAYERS_3D, K_DEFAULT, field,
                                      THETA_0, SOURCE_Y, SOURCE_Z, mode="theta")
    norms = np.array(norms)
    max_dev = np.max(np.abs(norms - 1.0))
    print(f"  Norms (first 5): {norms[:5]}")
    print(f"  Norms (last 5):  {norms[-5:]}")
    print(f"  Max deviation from 1.0: {max_dev:.2e}")
    status = "PASS" if max_dev < 1e-12 else "FAIL"
    print(f"  *** {status} ***")
    return status == "PASS"


# ── TEST 1b: 3D Gravity direction ─────────────────────────────────

def test_3d_gravity():
    print("\n" + "=" * 70)
    print("TEST 1b: 3D GRAVITY DIRECTION (Lorentzian theta)")
    print("=" * 70)

    field = make_field_3d(N_LAYERS_3D, N_YZ, STRENGTH_3D, MASS_Z)
    field0 = np.zeros((N_LAYERS_3D, N_YZ, N_YZ))

    results = {}
    for k in [3.0, 5.0, 7.0, 10.0]:
        psi_f, _ = chiral_propagate_3d(N_YZ, N_LAYERS_3D, k, field,
                                        THETA_0, SOURCE_Y, SOURCE_Z, mode="theta")
        P_f = detector_probs_3d(psi_f, N_YZ)
        cz_f = centroid_z(P_f)
        cy_f = centroid_y(P_f)

        psi_0, _ = chiral_propagate_3d(N_YZ, N_LAYERS_3D, k, field0,
                                        THETA_0, SOURCE_Y, SOURCE_Z, mode="theta")
        P_0 = detector_probs_3d(psi_0, N_YZ)
        cz_0 = centroid_z(P_0)
        cy_0 = centroid_y(P_0)

        delta_z = cz_f - cz_0
        delta_y = cy_f - cy_0
        # Mass at z=3, source at z=6, so TOWARD means delta_z < 0
        direction = "TOWARD" if delta_z < 0 else ("AWAY" if delta_z > 0 else "NONE")
        results[k] = (cz_0, cz_f, delta_z, direction)
        print(f"  k={k:5.1f}: cz_0={cz_0:.6f}, cz_f={cz_f:.6f}, "
              f"dz={delta_z:+.6e}, dy={delta_y:+.6e}, {direction}")

    all_toward = all(r[3] == "TOWARD" for r in results.values())
    any_toward = any(r[3] == "TOWARD" for r in results.values())
    status = "PASS" if all_toward else ("PARTIAL" if any_toward else "FAIL")
    print(f"  *** {status} (all TOWARD = {all_toward}) ***")
    return all_toward


# ── TEST 1c: 3D F-prop-M ──────────────────────────────────────────

def test_3d_f_prop_m():
    print("\n" + "=" * 70)
    print("TEST 1c: 3D F-PROP-M (Lorentzian theta)")
    print("=" * 70)

    strengths = [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]
    k = K_DEFAULT

    field0 = np.zeros((N_LAYERS_3D, N_YZ, N_YZ))
    psi_0, _ = chiral_propagate_3d(N_YZ, N_LAYERS_3D, k, field0,
                                    THETA_0, SOURCE_Y, SOURCE_Z, mode="theta")
    c_0 = centroid_z(detector_probs_3d(psi_0, N_YZ))

    deltas = []
    for s in strengths:
        field = make_field_3d(N_LAYERS_3D, N_YZ, s, MASS_Z)
        psi_f, _ = chiral_propagate_3d(N_YZ, N_LAYERS_3D, k, field,
                                        THETA_0, SOURCE_Y, SOURCE_Z, mode="theta")
        c_f = centroid_z(detector_probs_3d(psi_f, N_YZ))
        delta = c_f - c_0
        deltas.append(delta)
        print(f"  strength={s:.1e}: delta_z={delta:+.6e}")

    deltas = np.array(deltas)
    signs = np.sign(deltas)
    if np.all(signs == signs[0]) and signs[0] != 0:
        log_s = np.log10(np.array(strengths))
        log_d = np.log10(np.abs(deltas))
        coeffs = np.polyfit(log_s, log_d, 1)
        alpha = coeffs[0]
        pred = np.polyval(coeffs, log_s)
        ss_res = np.sum((log_d - pred) ** 2)
        ss_tot = np.sum((log_d - np.mean(log_d)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        print(f"\n  Power law fit: alpha = {alpha:.4f} (want 1.00)")
        print(f"  R^2 = {r2:.6f}")
        status = "PASS" if abs(alpha - 1.0) < 0.20 and r2 > 0.95 else "FAIL"
    else:
        print(f"\n  Mixed signs in deltas: {signs}")
        alpha, r2 = float('nan'), 0.0
        status = "FAIL"

    print(f"  *** {status} ***")
    return status == "PASS", alpha, r2


# ====================================================================
# PART 2: F-PROP-M DIAGNOSIS
# ====================================================================

# Use the 1D chiral walk for speed (same physics, clearer signal)
N_Y_1D = 17
N_LAYERS_1D = 20
THETA_1D = 0.3
SOURCE_1D = 8
MASS_1D = 4


def make_field_1d(n_layers, n_y, strength, mass_y):
    """1/r field in 1D."""
    field = np.zeros((n_layers, n_y))
    for x in range(n_layers):
        for y in range(n_y):
            field[x, y] = strength / (abs(y - mass_y) + 0.1)
    return field


def chiral_propagate_1d(n_y, n_layers, k, field, theta_0, source_y,
                        mode="theta"):
    """
    1D chiral walk.
    mode: "theta" = field in theta, "phase" = field in exp(ikf),
          "both" = field in both theta and phase
    """
    psi = np.zeros(2 * n_y, dtype=complex)
    psi[2 * source_y] = 1.0

    for x in range(n_layers):
        for y in range(n_y):
            f = field[x, y]
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi[idx_p], psi[idx_m]

            if mode == "theta":
                th = theta_0 * (1.0 - f)
                phi = 0.0
            elif mode == "phase":
                th = theta_0
                phi = k * f
            elif mode == "both":
                th = theta_0 * (1.0 - f)
                phi = k * f
            else:
                th = theta_0
                phi = 0.0

            psi[idx_p] = np.cos(th) * pp - np.sin(th) * np.exp(1j * phi) * pm
            psi[idx_m] = np.sin(th) * np.exp(-1j * phi) * pp + np.cos(th) * pm

        # Shift
        new_psi = np.zeros_like(psi)
        for y in range(n_y):
            if y + 1 < n_y:
                new_psi[2 * (y + 1)] += psi[2 * y]
            else:
                new_psi[2 * y + 1] += psi[2 * y]
            if y - 1 >= 0:
                new_psi[2 * (y - 1) + 1] += psi[2 * y + 1]
            else:
                new_psi[2 * y] += psi[2 * y + 1]
        psi = new_psi

    return psi


def detector_probs_1d(psi, n_y):
    probs = np.zeros(n_y)
    for y in range(n_y):
        probs[y] = abs(psi[2 * y]) ** 2 + abs(psi[2 * y + 1]) ** 2
    return probs


def centroid_1d(probs):
    ys = np.arange(len(probs))
    total = probs.sum()
    if total < 1e-30:
        return len(probs) / 2.0
    return np.sum(ys * probs) / total


def fit_power_law(strengths, deltas, label):
    """Fit |delta| = A * strength^alpha. Returns alpha, r2."""
    deltas = np.array(deltas)
    signs = np.sign(deltas)
    if not (np.all(signs == signs[0]) and signs[0] != 0):
        print(f"    {label}: Mixed signs {signs}, no clean fit")
        return float('nan'), 0.0

    log_s = np.log10(np.array(strengths))
    log_d = np.log10(np.abs(deltas))
    coeffs = np.polyfit(log_s, log_d, 1)
    alpha = coeffs[0]
    pred = np.polyval(coeffs, log_s)
    ss_res = np.sum((log_d - pred) ** 2)
    ss_tot = np.sum((log_d - np.mean(log_d)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    print(f"    {label}: alpha = {alpha:.4f}, R^2 = {r2:.6f}")
    return alpha, r2


# ── TEST 2a: Phase-only coupling (expect alpha~2.0) ───────────────

def test_phase_coupling():
    print("\n" + "=" * 70)
    print("TEST 2a: PHASE-ONLY COUPLING (expect alpha ~ 2.0)")
    print("=" * 70)
    print("  Theory: |exp(ikf)|^2 = 1, no first-order probability change")
    print("  -> centroid shift is O(f^2) -> alpha = 2.0")

    strengths = [1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4]
    k = K_DEFAULT

    field0 = np.zeros((N_LAYERS_1D, N_Y_1D))
    psi_0 = chiral_propagate_1d(N_Y_1D, N_LAYERS_1D, k, field0, THETA_1D,
                                 SOURCE_1D, mode="phase")
    c_0 = centroid_1d(detector_probs_1d(psi_0, N_Y_1D))

    deltas = []
    for s in strengths:
        field = make_field_1d(N_LAYERS_1D, N_Y_1D, s, MASS_1D)
        psi_f = chiral_propagate_1d(N_Y_1D, N_LAYERS_1D, k, field, THETA_1D,
                                     SOURCE_1D, mode="phase")
        c_f = centroid_1d(detector_probs_1d(psi_f, N_Y_1D))
        delta = c_f - c_0
        deltas.append(delta)
        direction = "TOWARD" if delta < 0 else "AWAY"
        print(f"  s={s:.1e}: delta={delta:+.6e} ({direction})")

    alpha, r2 = fit_power_law(strengths, deltas, "Phase-only")
    status = "PASS" if abs(alpha - 2.0) < 0.30 else "FAIL"
    print(f"  Expected alpha ~ 2.0, got {alpha:.4f}")
    print(f"  *** {status} ***")
    return alpha, r2


# ── TEST 2b: Theta-only coupling (expect alpha~1.0) ───────────────

def test_theta_coupling():
    print("\n" + "=" * 70)
    print("TEST 2b: THETA-ONLY COUPLING (expect alpha ~ 1.0)")
    print("=" * 70)
    print("  Theory: sin(theta*(1-f)) changes magnitude directly")
    print("  -> first-order probability change proportional to f -> alpha = 1.0")

    strengths = [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]
    k = K_DEFAULT

    field0 = np.zeros((N_LAYERS_1D, N_Y_1D))
    psi_0 = chiral_propagate_1d(N_Y_1D, N_LAYERS_1D, k, field0, THETA_1D,
                                 SOURCE_1D, mode="theta")
    c_0 = centroid_1d(detector_probs_1d(psi_0, N_Y_1D))

    deltas = []
    for s in strengths:
        field = make_field_1d(N_LAYERS_1D, N_Y_1D, s, MASS_1D)
        psi_f = chiral_propagate_1d(N_Y_1D, N_LAYERS_1D, k, field, THETA_1D,
                                     SOURCE_1D, mode="theta")
        c_f = centroid_1d(detector_probs_1d(psi_f, N_Y_1D))
        delta = c_f - c_0
        deltas.append(delta)
        direction = "TOWARD" if delta < 0 else "AWAY"
        print(f"  s={s:.1e}: delta={delta:+.6e} ({direction})")

    alpha, r2 = fit_power_law(strengths, deltas, "Theta-only")
    status = "PASS" if abs(alpha - 1.0) < 0.20 else "FAIL"
    print(f"  Expected alpha ~ 1.0, got {alpha:.4f}")
    print(f"  *** {status} ***")
    return alpha, r2


# ── TEST 2c: Mixed coupling (both phase + theta) ──────────────────

def test_mixed_coupling():
    print("\n" + "=" * 70)
    print("TEST 2c: MIXED COUPLING (phase + theta)")
    print("=" * 70)
    print("  Both channels active: what alpha emerges?")

    strengths = [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]
    k = K_DEFAULT

    field0 = np.zeros((N_LAYERS_1D, N_Y_1D))
    psi_0 = chiral_propagate_1d(N_Y_1D, N_LAYERS_1D, k, field0, THETA_1D,
                                 SOURCE_1D, mode="both")
    c_0 = centroid_1d(detector_probs_1d(psi_0, N_Y_1D))

    deltas = []
    for s in strengths:
        field = make_field_1d(N_LAYERS_1D, N_Y_1D, s, MASS_1D)
        psi_f = chiral_propagate_1d(N_Y_1D, N_LAYERS_1D, k, field, THETA_1D,
                                     SOURCE_1D, mode="both")
        c_f = centroid_1d(detector_probs_1d(psi_f, N_Y_1D))
        delta = c_f - c_0
        deltas.append(delta)
        direction = "TOWARD" if delta < 0 else "AWAY"
        print(f"  s={s:.1e}: delta={delta:+.6e} ({direction})")

    alpha, r2 = fit_power_law(strengths, deltas, "Mixed")
    print(f"  Got alpha = {alpha:.4f}")
    print(f"  (If theta dominates: alpha~1.0; if phase dominates: alpha~2.0)")
    return alpha, r2


# ── TEST 2d: Analytic verification ────────────────────────────────

def test_analytic():
    print("\n" + "=" * 70)
    print("TEST 2d: ANALYTIC VERIFICATION")
    print("=" * 70)

    print("\n  Phase coupling analysis:")
    print("  -------------------------")
    print("  Coin matrix element: -sin(theta)*exp(i*k*f)")
    print("  Probability: |sin(theta)*exp(ikf)|^2 = sin^2(theta)")
    print("  -> No f-dependence in probability at ANY order!")
    print("  -> Gravity must come from INTERFERENCE between paths")
    print("  -> Interference term: Re(psi_1* psi_2) involves phases from")
    print("     different sites, giving O(f) in AMPLITUDE but O(f^2) in PROB")
    print()

    print("  Theta coupling analysis:")
    print("  -------------------------")
    print("  Coin: sin(theta0*(1-f)) = sin(theta0) - f*theta0*cos(theta0) + ...")
    print("  Probability: sin^2(theta0*(1-f))")
    print("    = sin^2(theta0) - 2f*theta0*sin(theta0)*cos(theta0) + O(f^2)")
    print("    = sin^2(theta0) - f*theta0*sin(2*theta0) + O(f^2)")
    print("  -> First-order f-dependence in probability!")
    print("  -> Centroid shift proportional to f -> alpha = 1.0")
    print()

    # Numerical check: single-step coin probability
    theta0 = 0.3
    f_vals = [0.0, 0.001, 0.01, 0.1]
    print("  Single-coin probability check:")
    print(f"  {'f':>8s}  {'|sin(th*(1-f))|^2':>20s}  {'|sin(th)*exp(ikf)|^2':>22s}")
    for f in f_vals:
        prob_theta = np.sin(theta0 * (1 - f)) ** 2
        prob_phase = np.abs(np.sin(theta0) * np.exp(1j * K_DEFAULT * f)) ** 2
        print(f"  {f:8.4f}  {prob_theta:20.10f}  {prob_phase:22.10f}")

    print("\n  Key insight: phase coupling probability is EXACTLY f-independent")
    print("  while theta coupling probability varies linearly with f.")


# ── TEST 2e: k-dependence of alpha ────────────────────────────────

def test_alpha_vs_k():
    print("\n" + "=" * 70)
    print("TEST 2e: ALPHA VS K (both modes)")
    print("=" * 70)

    strengths = [1e-5, 2e-5, 5e-5, 1e-4, 2e-4]
    ks = [2.0, 5.0, 8.0, 12.0]

    print(f"\n  {'k':>5s}  {'alpha_phase':>12s}  {'alpha_theta':>12s}")
    print("  " + "-" * 35)

    for k in ks:
        # Phase mode
        field0 = np.zeros((N_LAYERS_1D, N_Y_1D))
        psi_0 = chiral_propagate_1d(N_Y_1D, N_LAYERS_1D, k, field0, THETA_1D,
                                     SOURCE_1D, mode="phase")
        c_0_phase = centroid_1d(detector_probs_1d(psi_0, N_Y_1D))

        deltas_phase = []
        for s in strengths:
            field = make_field_1d(N_LAYERS_1D, N_Y_1D, s, MASS_1D)
            psi_f = chiral_propagate_1d(N_Y_1D, N_LAYERS_1D, k, field, THETA_1D,
                                         SOURCE_1D, mode="phase")
            c_f = centroid_1d(detector_probs_1d(psi_f, N_Y_1D))
            deltas_phase.append(c_f - c_0_phase)

        # Theta mode
        psi_0 = chiral_propagate_1d(N_Y_1D, N_LAYERS_1D, k, field0, THETA_1D,
                                     SOURCE_1D, mode="theta")
        c_0_theta = centroid_1d(detector_probs_1d(psi_0, N_Y_1D))

        deltas_theta = []
        for s in strengths:
            field = make_field_1d(N_LAYERS_1D, N_Y_1D, s, MASS_1D)
            psi_f = chiral_propagate_1d(N_Y_1D, N_LAYERS_1D, k, field, THETA_1D,
                                         SOURCE_1D, mode="theta")
            c_f = centroid_1d(detector_probs_1d(psi_f, N_Y_1D))
            deltas_theta.append(c_f - c_0_theta)

        # Fit
        d_p = np.array(deltas_phase)
        d_t = np.array(deltas_theta)
        log_s = np.log10(np.array(strengths))

        alpha_p = float('nan')
        if np.all(np.sign(d_p) == np.sign(d_p[0])) and np.sign(d_p[0]) != 0:
            alpha_p = np.polyfit(log_s, np.log10(np.abs(d_p)), 1)[0]

        alpha_t = float('nan')
        if np.all(np.sign(d_t) == np.sign(d_t[0])) and np.sign(d_t[0]) != 0:
            alpha_t = np.polyfit(log_s, np.log10(np.abs(d_t)), 1)[0]

        print(f"  {k:5.1f}  {alpha_p:12.4f}  {alpha_t:12.4f}")


# ====================================================================
# MAIN
# ====================================================================

def main():
    print("FRONTIER: 3D CHIRAL PROPAGATOR + F-PROP-M DIAGNOSIS")
    print("=" * 70)
    print(f"3D params: n_yz={N_YZ}, layers={N_LAYERS_3D}, k={K_DEFAULT}, "
          f"theta0={THETA_0}")
    print(f"3D mass at z={MASS_Z}, source at (y,z)=({SOURCE_Y},{SOURCE_Z})")
    print(f"1D params: n_y={N_Y_1D}, layers={N_LAYERS_1D}, theta={THETA_1D}")
    print(f"1D mass at y={MASS_1D}, source at y={SOURCE_1D}")
    print()

    results = {}

    # Part 1: 3D tests
    print("PART 1: 3D CHIRAL PROPAGATOR")
    print("=" * 70)
    results['3d_norm'] = test_3d_norm()
    results['3d_gravity'] = test_3d_gravity()
    fm3d_pass, alpha_3d, r2_3d = test_3d_f_prop_m()
    results['3d_f_prop_m'] = fm3d_pass

    # Part 2: F-prop-M diagnosis
    print("\n\nPART 2: F-PROP-M DIAGNOSIS")
    print("=" * 70)
    alpha_phase, r2_phase = test_phase_coupling()
    alpha_theta, r2_theta = test_theta_coupling()
    alpha_mixed, r2_mixed = test_mixed_coupling()
    test_analytic()
    test_alpha_vs_k()

    # ── Summary ─────────────────────────────────────────────────────
    print("\n\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print("\n  PART 1: 3D Chiral Walk (Lorentzian theta coupling)")
    print(f"    Norm:     {'PASS' if results['3d_norm'] else 'FAIL'}")
    print(f"    Gravity:  {'PASS (TOWARD)' if results['3d_gravity'] else 'FAIL'}")
    print(f"    F-prop-M: {'PASS' if results['3d_f_prop_m'] else 'FAIL'} "
          f"(alpha={alpha_3d:.4f}, R^2={r2_3d:.6f})")

    print("\n  PART 2: F-prop-M Mechanism")
    print(f"    Phase-only alpha:  {alpha_phase:.4f} (expect ~2.0)")
    print(f"    Theta-only alpha:  {alpha_theta:.4f} (expect ~1.0)")
    print(f"    Mixed alpha:       {alpha_mixed:.4f}")

    print("\n  EXPLANATION:")
    print("    Phase coupling: |exp(ikf)|^2 = 1 exactly.")
    print("    No first-order probability change -> centroid shift is O(f^2) -> alpha=2")
    print("    Theta coupling: sin^2(theta*(1-f)) has first-order f term.")
    print("    Direct probability change -> centroid shift is O(f) -> alpha=1")

    # Overall hypothesis
    hypothesis_3d = results['3d_norm'] and results['3d_gravity'] and results['3d_f_prop_m']
    hypothesis_fm = (abs(alpha_phase - 2.0) < 0.30 and abs(alpha_theta - 1.0) < 0.20)

    print(f"\n  HYPOTHESIS (3D TOWARD + F-prop-M=1): "
          f"{'CONFIRMED' if hypothesis_3d else 'FALSIFIED'}")
    print(f"  HYPOTHESIS (phase=quad, theta=lin): "
          f"{'CONFIRMED' if hypothesis_fm else 'FALSIFIED'}")

    if hypothesis_3d and hypothesis_fm:
        print("\n  BOTH HYPOTHESES CONFIRMED.")
        print("  3D chiral walk: TOWARD gravity with linear F-prop-M.")
        print("  F-prop-M mechanism: theta coupling gives O(f) probability,")
        print("  phase coupling gives O(f^2) via interference only.")
    elif hypothesis_3d:
        print("\n  3D walk confirmed, F-prop-M mechanism needs refinement.")
    elif hypothesis_fm:
        print("\n  F-prop-M mechanism confirmed, 3D walk needs work.")
    else:
        print("\n  Both hypotheses need revision.")


if __name__ == "__main__":
    main()
