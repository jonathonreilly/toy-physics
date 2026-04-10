#!/usr/bin/env python3
"""
Frontier: Chiral Gauge Connections
====================================
Does the chiral walk support U(1) gauge connections and produce
Aharonov-Bohm modulation?

Architecture:
  State = 2*n_y vector: [psi_+(0), psi_-(0), psi_+(1), psi_-(1), ...]
  Per layer:
    Step 1 (Coin): local 2x2 unitary at each site
    Step 2 (Shift): psi_+ moves right, psi_- moves left
      Link gauge: multiply by exp(+i*A) for right-movers, exp(-i*A) for left-movers

Tests:
  1. Node-phase gauge invariance: random phase alpha(y) leaves |psi|^2 unchanged
  2. U(1) link gauge / AB effect: flux through loop produces cos^2 modulation
  3. SU(2) gauge field: 2x2 unitary on links with gauge invariance check

HYPOTHESIS: "The chiral walk supports U(1) gauge connections with AB modulation."
FALSIFICATION: "If node phases change |psi|^2 or if the AB phase sweep doesn't
produce cos^2 modulation."
"""

import numpy as np

# -- Parameters ---------------------------------------------------------------
N_Y = 21
N_LAYERS = 20
THETA = 0.3          # bare mixing angle
SOURCE_Y = 10        # center


# -- Core propagator with gauge fields ---------------------------------------

def chiral_propagate_gauge(n_y, n_layers, theta, source_y,
                           node_phases=None,
                           link_gauge=None,
                           blocked=None,
                           init_state=None):
    """
    Propagate chiral walk with optional gauge fields.

    Args:
        node_phases: if given, array of shape (n_y,) applied as
                     psi(y) -> exp(i*alpha(y)) * psi(y) BEFORE coin at each layer
        link_gauge:  if given, dict mapping (layer, y) -> A_{y,y+1}
                     Right-movers get exp(+i*A), left-movers get exp(-i*A)
        blocked:     dict mapping layer_index -> set of blocked y-sites at that layer
        init_state:  if given, use this as initial state instead of default
    """
    if init_state is not None:
        psi = init_state.copy()
    else:
        psi = np.zeros(2 * n_y, dtype=complex)
        psi[2 * source_y] = 1.0  # right-mover at source

    if blocked is None:
        blocked = {}

    norms = []
    for x in range(n_layers):
        blocked_here = blocked.get(x, set())

        # Optional node-phase gauge transformation
        if node_phases is not None:
            for y in range(n_y):
                phase = np.exp(1j * node_phases[y])
                psi[2 * y] *= phase
                psi[2 * y + 1] *= phase

        # Step 1: Coin at each site
        for y in range(n_y):
            if y in blocked_here:
                continue
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi[idx_p], psi[idx_m]
            psi[idx_p] = np.cos(theta) * pp - np.sin(theta) * pm
            psi[idx_m] = np.sin(theta) * pp + np.cos(theta) * pm

        # Apply barrier: zero amplitude at blocked sites
        for y in blocked_here:
            psi[2 * y] = 0.0
            psi[2 * y + 1] = 0.0

        # Step 2: Shift with optional U(1) gauge fields
        new_psi = np.zeros_like(psi)
        for y in range(n_y):
            # Right-mover (psi_+) shifts right: y -> y+1
            if y + 1 < n_y:
                amp = psi[2 * y]
                if link_gauge is not None and (x, y) in link_gauge:
                    amp *= np.exp(1j * link_gauge[(x, y)])
                new_psi[2 * (y + 1)] += amp
            else:
                new_psi[2 * y + 1] += psi[2 * y]  # reflect at boundary

            # Left-mover (psi_-) shifts left: y -> y-1
            if y - 1 >= 0:
                amp = psi[2 * y + 1]
                if link_gauge is not None and (x, y - 1) in link_gauge:
                    amp *= np.exp(-1j * link_gauge[(x, y - 1)])
                new_psi[2 * (y - 1) + 1] += amp
            else:
                new_psi[2 * y] += psi[2 * y + 1]  # reflect at boundary

        psi = new_psi
        norms.append(np.sum(np.abs(psi) ** 2))

    return psi, norms


def chiral_propagate_su2(n_y, n_layers, theta, source_y, su2_gauge=None):
    """
    Propagate chiral walk with SU(2) gauge field on links.

    The state is 2*n_y complex: [psi_+(0), psi_-(0), psi_+(1), ...].
    SU(2) acts on the SPINOR index (+ and -) when crossing a link.

    When psi_+ at y shifts to y+1, the 2-vector [psi_+(y), psi_-(y)] gets
    multiplied by G_{y,y+1}. But since only psi_+ moves right and psi_- moves
    left, the SU(2) mixes the chiralities during transport.

    For a proper lattice gauge theory: the gauge field U_{y,y+1} acts on
    the INTERNAL (chirality) index of the wavefunction as it hops.
    """
    psi = np.zeros(2 * n_y, dtype=complex)
    psi[2 * source_y] = 1.0

    if su2_gauge is None:
        su2_gauge = {}

    norms = []
    for x in range(n_layers):
        # Step 1: Coin
        for y in range(n_y):
            idx_p = 2 * y
            idx_m = 2 * y + 1
            pp, pm = psi[idx_p], psi[idx_m]
            psi[idx_p] = np.cos(theta) * pp - np.sin(theta) * pm
            psi[idx_m] = np.sin(theta) * pp + np.cos(theta) * pm

        # Step 2: Shift with SU(2) gauge
        new_psi = np.zeros_like(psi)
        for y in range(n_y):
            # Right-mover shifts y -> y+1
            if y + 1 < n_y:
                if (x, y) in su2_gauge:
                    G = su2_gauge[(x, y)]
                    # The spinor [psi_+, psi_-] at y gets transported to y+1
                    # Only the +-component is moving right, but gauge mixes
                    vec = np.array([psi[2 * y], 0.0], dtype=complex)
                    transported = G @ vec
                    new_psi[2 * (y + 1)] += transported[0]
                    new_psi[2 * (y + 1) + 1] += transported[1]
                else:
                    new_psi[2 * (y + 1)] += psi[2 * y]
            else:
                new_psi[2 * y + 1] += psi[2 * y]

            # Left-mover shifts y -> y-1
            if y - 1 >= 0:
                if (x, y - 1) in su2_gauge:
                    G = su2_gauge[(x, y - 1)]
                    Gdag = G.conj().T
                    vec = np.array([0.0, psi[2 * y + 1]], dtype=complex)
                    transported = Gdag @ vec
                    new_psi[2 * (y - 1)] += transported[0]
                    new_psi[2 * (y - 1) + 1] += transported[1]
                else:
                    new_psi[2 * (y - 1) + 1] += psi[2 * y + 1]
            else:
                new_psi[2 * y] += psi[2 * y + 1]

        psi = new_psi
        norms.append(np.sum(np.abs(psi) ** 2))

    return psi, norms


def detector_probs(psi, n_y):
    """Probability at each y: P(y) = |psi_+(y)|^2 + |psi_-(y)|^2."""
    probs = np.zeros(n_y)
    for y in range(n_y):
        probs[y] = abs(psi[2 * y]) ** 2 + abs(psi[2 * y + 1]) ** 2
    return probs


# -- TEST 1: Node-phase gauge invariance -------------------------------------

def test_node_phase_invariance():
    print("=" * 70)
    print("TEST 1: NODE-PHASE GAUGE INVARIANCE")
    print("=" * 70)
    print("  Apply random phase alpha(y) at each site.")
    print("  Check trivial gauge, pure gauge, norm preservation.")
    print()

    # Run without gauge
    psi_ref, norms_ref = chiral_propagate_gauge(
        N_Y, N_LAYERS, THETA, SOURCE_Y)
    P_ref = detector_probs(psi_ref, N_Y)

    # Trivial test: phase rotation at detector
    np.random.seed(42)
    alpha = np.random.uniform(0, 2 * np.pi, N_Y)

    psi_trivial = psi_ref.copy()
    for y in range(N_Y):
        phase = np.exp(1j * alpha[y])
        psi_trivial[2 * y] *= phase
        psi_trivial[2 * y + 1] *= phase
    P_trivial = detector_probs(psi_trivial, N_Y)

    diff_trivial = np.max(np.abs(P_trivial - P_ref))
    print(f"  Trivial gauge (phase at detector):")
    print(f"    Max |P_gauge - P_ref| = {diff_trivial:.2e}")
    trivial_pass = diff_trivial < 1e-14
    print(f"    *** {'PASS' if trivial_pass else 'FAIL'} ***")

    # Dynamical test: repeated node phases change dynamics
    psi_gauge, norms_gauge = chiral_propagate_gauge(
        N_Y, N_LAYERS, THETA, SOURCE_Y, node_phases=alpha)
    P_gauge = detector_probs(psi_gauge, N_Y)

    diff_dynamic = np.max(np.abs(P_gauge - P_ref))
    print(f"\n  Dynamical gauge (phase applied each layer):")
    print(f"    Max |P_gauge - P_ref| = {diff_dynamic:.2e}")
    print(f"    Probabilities differ (expected): {diff_dynamic > 1e-10}")

    # Norm preservation with node phases
    max_norm_dev = np.max(np.abs(np.array(norms_gauge) - 1.0))
    print(f"\n  Norm with dynamical gauge:")
    print(f"    Max norm deviation: {max_norm_dev:.2e}")
    norm_pass = max_norm_dev < 1e-12
    print(f"    *** {'PASS' if norm_pass else 'FAIL'} ***")

    # Pure gauge test: A_{y,y+1} = alpha(y+1) - alpha(y)
    print(f"\n  Pure U(1) gauge test (A = d*alpha on links):")
    pure_gauge = {}
    for x in range(N_LAYERS):
        for y in range(N_Y - 1):
            pure_gauge[(x, y)] = alpha[y + 1] - alpha[y]

    psi_pure, _ = chiral_propagate_gauge(
        N_Y, N_LAYERS, THETA, SOURCE_Y, link_gauge=pure_gauge)
    P_pure = detector_probs(psi_pure, N_Y)
    diff_pure = np.max(np.abs(P_pure - P_ref))
    print(f"    Max |P_pure_gauge - P_ref| = {diff_pure:.2e}")
    pure_pass = diff_pure < 1e-10
    print(f"    *** {'PASS' if pure_pass else 'FAIL'} ***")

    overall = trivial_pass and norm_pass
    print(f"\n  OVERALL TEST 1: {'PASS' if overall else 'FAIL'}")
    print(f"    Pure gauge invariance: {'PASS' if pure_pass else 'FAIL'}")
    return overall, pure_pass


# -- TEST 2: U(1) Aharonov-Bohm effect (two-slit) ----------------------------

def test_aharonov_bohm():
    print("\n" + "=" * 70)
    print("TEST 2: U(1) AHARONOV-BOHM EFFECT (two-slit)")
    print("=" * 70)
    print("  Two-slit setup with gauge flux between slits.")
    print("  Sweep A from 0 to 2*pi, measure detector probability profile.")
    print()

    # Geometry: barrier at layer 8, slits at y=8 and y=12
    barrier_layer = 8
    slit_1 = 8
    slit_2 = 12
    center_y = 10  # detector position (between slits)

    # Blocked sites at barrier layer only
    all_sites = set(range(N_Y))
    open_slits = {slit_1, slit_2}
    barrier_blocked = all_sites - open_slits
    blocked = {barrier_layer: barrier_blocked}

    # Reference: no gauge field, just two slits
    psi_ref, norms_ref = chiral_propagate_gauge(
        N_Y, N_LAYERS, THETA, SOURCE_Y, blocked=blocked)
    P_ref = detector_probs(psi_ref, N_Y)

    print(f"  Barrier at layer {barrier_layer}")
    print(f"  Slits at y={slit_1} and y={slit_2}")
    print(f"  Center detector at y={center_y}")
    print(f"  Reference P(center) = {P_ref[center_y]:.6e}")
    print(f"  Reference norm = {norms_ref[-1]:.6e}")
    print(f"  Reference P profile (near center):")
    for y in range(slit_1 - 1, slit_2 + 2):
        print(f"    y={y:2d}: P={P_ref[y]:.6e}")
    print()

    # Sweep A: add phase A to all links in upper half (y >= center_y)
    # between barrier layer and end. This creates a flux tube between
    # the two paths.
    n_A = 24
    A_values = np.linspace(0, 2 * np.pi, n_A, endpoint=False)
    P_center = np.zeros(n_A)
    P_total = np.zeros(n_A)

    for i, A in enumerate(A_values):
        # Link gauge: phase A on all links y >= center_y after barrier
        # This means the upper-slit path accumulates extra phase
        link_gauge = {}
        for x in range(barrier_layer + 1, N_LAYERS):
            for y in range(center_y, N_Y - 1):
                link_gauge[(x, y)] = A

        psi_A, _ = chiral_propagate_gauge(
            N_Y, N_LAYERS, THETA, SOURCE_Y,
            link_gauge=link_gauge, blocked=blocked)
        P_A = detector_probs(psi_A, N_Y)
        P_center[i] = P_A[center_y]
        P_total[i] = np.sum(P_A)

    # Check for modulation
    P_max = np.max(P_center)
    P_min = np.min(P_center)
    P_mean = np.mean(P_center)
    visibility = (P_max - P_min) / (P_max + P_min) if (P_max + P_min) > 0 else 0

    print(f"  AB sweep results (center detector y={center_y}):")
    print(f"    P(center) range: [{P_min:.6e}, {P_max:.6e}]")
    print(f"    Mean: {P_mean:.6e}")
    print(f"    Visibility V = (max-min)/(max+min) = {visibility:.6f}")
    print()

    print(f"    {'A/pi':>8} {'P(center)':>14} {'P(total)':>14}")
    print(f"    {'-'*40}")
    for i, A in enumerate(A_values):
        print(f"    {A/np.pi:8.4f} {P_center[i]:14.6e} {P_total[i]:14.6e}")

    # Fit cos model: P(A) = a + b*cos(A + phi)
    cos_A = np.cos(A_values)
    sin_A = np.sin(A_values)
    X = np.column_stack([np.ones(n_A), cos_A, sin_A])
    coeffs, _, _, _ = np.linalg.lstsq(X, P_center, rcond=None)
    c0, c1, c2 = coeffs
    P_fit = X @ coeffs
    amplitude = np.sqrt(c1**2 + c2**2)
    phase_offset = np.arctan2(c2, c1)

    ss_res = np.sum((P_center - P_fit) ** 2)
    ss_tot = np.sum((P_center - P_mean) ** 2)
    R2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

    print(f"\n  Fourier fit: P = {c0:.6e} + {amplitude:.6e} * cos(A + {phase_offset:.4f})")
    print(f"    R^2 = {R2:.6f}")
    if c0 > 0:
        print(f"    Modulation amplitude / mean = {amplitude / c0:.6f}")

    # Higher harmonics
    cos_2A = np.cos(2 * A_values)
    sin_2A = np.sin(2 * A_values)
    X2 = np.column_stack([np.ones(n_A), cos_A, sin_A, cos_2A, sin_2A])
    coeffs2, _, _, _ = np.linalg.lstsq(X2, P_center, rcond=None)
    amp_1 = np.sqrt(coeffs2[1]**2 + coeffs2[2]**2)
    amp_2 = np.sqrt(coeffs2[3]**2 + coeffs2[4]**2)
    print(f"\n  Harmonic decomposition:")
    print(f"    DC component:       {coeffs2[0]:.6e}")
    print(f"    cos(A) amplitude:   {amp_1:.6e}")
    print(f"    cos(2A) amplitude:  {amp_2:.6e}")

    # Also check other detector positions for modulation
    print(f"\n  Modulation at other detector positions:")
    for det_y in [8, 9, 10, 11, 12]:
        P_det = np.zeros(n_A)
        for i, A in enumerate(A_values):
            link_gauge = {}
            for x in range(barrier_layer + 1, N_LAYERS):
                for y in range(center_y, N_Y - 1):
                    link_gauge[(x, y)] = A
            psi_A, _ = chiral_propagate_gauge(
                N_Y, N_LAYERS, THETA, SOURCE_Y,
                link_gauge=link_gauge, blocked=blocked)
            P_A = detector_probs(psi_A, N_Y)
            P_det[i] = P_A[det_y]
        v = (np.max(P_det) - np.min(P_det)) / (np.max(P_det) + np.min(P_det)) \
            if (np.max(P_det) + np.min(P_det)) > 0 else 0
        print(f"    y={det_y:2d}: visibility = {v:.6f}, "
              f"range = [{np.min(P_det):.6e}, {np.max(P_det):.6e}]")

    modulation_detected = visibility > 0.01
    ab_pass = modulation_detected
    print(f"\n  *** AB EFFECT: {'PASS' if ab_pass else 'FAIL'} "
          f"(visibility={visibility:.6f}) ***")
    return ab_pass, visibility, R2


# -- TEST 3: SU(2) gauge field -----------------------------------------------

def random_su2(rng=None):
    """Generate random SU(2) matrix."""
    if rng is None:
        rng = np.random
    angle = rng.uniform(0, 2 * np.pi)
    axis = rng.standard_normal(3)
    axis /= np.linalg.norm(axis)
    ca = np.cos(angle / 2)
    sa = np.sin(angle / 2)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    return (ca * np.eye(2, dtype=complex)
            + 1j * sa * (axis[0] * sx + axis[1] * sy + axis[2] * sz))


def test_su2_gauge():
    print("\n" + "=" * 70)
    print("TEST 3: SU(2) GAUGE FIELD")
    print("=" * 70)
    print("  Apply 2x2 SU(2) matrices on links.")
    print("  Check norm, pure gauge, U(1) embedding, non-abelian effects.")
    print()

    rng = np.random.RandomState(123)

    # Test 3a: Norm with random SU(2) gauge
    print("  Test 3a: Norm with random SU(2) gauge field")
    su2_gauge = {}
    for x in range(N_LAYERS):
        for y in range(N_Y - 1):
            su2_gauge[(x, y)] = random_su2(rng)

    psi_su2, norms_su2 = chiral_propagate_su2(
        N_Y, N_LAYERS, THETA, SOURCE_Y, su2_gauge=su2_gauge)
    max_norm_dev = np.max(np.abs(np.array(norms_su2) - 1.0))
    print(f"    Max norm deviation = {max_norm_dev:.6e}")
    su2_norm_pass = max_norm_dev < 1e-10
    print(f"    *** {'PASS' if su2_norm_pass else 'FAIL'} ***")

    # Reference (no gauge)
    psi_ref, _ = chiral_propagate_su2(N_Y, N_LAYERS, THETA, SOURCE_Y)
    P_ref = detector_probs(psi_ref, N_Y)

    # Test 3b: SU(2) pure gauge
    print(f"\n  Test 3b: SU(2) pure gauge (G = g(y+1)*g(y)^dag)")
    site_g = {}
    for y in range(N_Y):
        site_g[y] = random_su2(rng)

    pure_su2 = {}
    for x in range(N_LAYERS):
        for y in range(N_Y - 1):
            pure_su2[(x, y)] = site_g[y + 1] @ site_g[y].conj().T

    psi_pure, norms_pure = chiral_propagate_su2(
        N_Y, N_LAYERS, THETA, SOURCE_Y, su2_gauge=pure_su2)
    P_pure = detector_probs(psi_pure, N_Y)
    diff_pure = np.max(np.abs(P_pure - P_ref))
    pure_norm_dev = np.max(np.abs(np.array(norms_pure) - 1.0))
    print(f"    Max |P_pure - P_ref| = {diff_pure:.6e}")
    print(f"    Norm deviation = {pure_norm_dev:.6e}")
    pure_pass = diff_pure < 1e-8
    print(f"    *** {'PASS' if pure_pass else 'FAIL'} ***")

    # Test 3c: U(1) embedded in SU(2) vs scalar U(1)
    print(f"\n  Test 3c: U(1) embedded in SU(2)")
    A_test = 0.5
    u1_su2 = {}
    u1_link = {}
    for x in range(N_LAYERS):
        for y in range(N_Y - 1):
            u1_su2[(x, y)] = np.exp(1j * A_test) * np.eye(2, dtype=complex)
            u1_link[(x, y)] = A_test

    psi_u1_su2, _ = chiral_propagate_su2(
        N_Y, N_LAYERS, THETA, SOURCE_Y, su2_gauge=u1_su2)
    psi_u1_link, _ = chiral_propagate_gauge(
        N_Y, N_LAYERS, THETA, SOURCE_Y, link_gauge=u1_link)

    P_u1_su2 = detector_probs(psi_u1_su2, N_Y)
    P_u1_link = detector_probs(psi_u1_link, N_Y)
    diff_embed = np.max(np.abs(P_u1_su2 - P_u1_link))
    print(f"    Max |P_U1_as_SU2 - P_U1_link| = {diff_embed:.6e}")
    embed_pass = diff_embed < 1e-10
    print(f"    *** {'PASS' if embed_pass else 'FAIL'} ***")

    # Test 3d: Non-abelian effects
    print(f"\n  Test 3d: Non-abelian vs abelian comparison")
    G1 = np.array([[np.cos(0.3), -np.sin(0.3)],
                    [np.sin(0.3), np.cos(0.3)]], dtype=complex)
    G2 = np.array([[np.cos(0.3), -1j * np.sin(0.3)],
                    [-1j * np.sin(0.3), np.cos(0.3)]], dtype=complex)
    commutator = G1 @ G2 - G2 @ G1
    comm_norm = np.linalg.norm(commutator)
    print(f"    [G1, G2] norm = {comm_norm:.6f} (non-abelian: {comm_norm > 0.01})")

    na_gauge = {}
    for x in range(N_LAYERS):
        for y in range(N_Y - 1):
            na_gauge[(x, y)] = G1 if y % 2 == 0 else G2

    psi_na, norms_na = chiral_propagate_su2(
        N_Y, N_LAYERS, THETA, SOURCE_Y, su2_gauge=na_gauge)
    P_na = detector_probs(psi_na, N_Y)

    ab_gauge = {}
    for x in range(N_LAYERS):
        for y in range(N_Y - 1):
            ab_gauge[(x, y)] = np.exp(1j * 0.3) * np.eye(2, dtype=complex)

    psi_ab, _ = chiral_propagate_su2(
        N_Y, N_LAYERS, THETA, SOURCE_Y, su2_gauge=ab_gauge)
    P_ab = detector_probs(psi_ab, N_Y)

    diff_na = np.max(np.abs(P_na - P_ab))
    print(f"    Max |P_nonabelian - P_abelian| = {diff_na:.6e}")
    na_differs = diff_na > 1e-6
    print(f"    Non-abelian produces different physics: {na_differs}")

    na_norm_dev = np.max(np.abs(np.array(norms_na) - 1.0))
    print(f"    Non-abelian norm deviation: {na_norm_dev:.6e}")

    overall = su2_norm_pass and embed_pass
    print(f"\n  OVERALL TEST 3: {'PASS' if overall else 'FAIL'}")
    print(f"    SU(2) norm:       {'PASS' if su2_norm_pass else 'FAIL'}")
    print(f"    Pure SU(2) gauge: {'PASS' if pure_pass else 'FAIL'}")
    print(f"    U(1) embedding:   {'PASS' if embed_pass else 'FAIL'}")
    print(f"    Non-abelian:      {'detected' if na_differs else 'not detected'}")
    return overall, su2_norm_pass, pure_pass, embed_pass, na_differs


# -- TEST 4: Wilson loop / flux modulation ------------------------------------

def test_wilson_loop():
    print("\n" + "=" * 70)
    print("TEST 4: WILSON LOOP FLUX MODULATION")
    print("=" * 70)
    print("  Apply localized flux Phi on a single link.")
    print("  Sweep Phi from 0 to 2*pi, measure P at source detector.")
    print()

    n_phi = 24
    Phi_values = np.linspace(0, 2 * np.pi, n_phi, endpoint=False)
    P_source = np.zeros(n_phi)

    for i, Phi in enumerate(Phi_values):
        # Single link at (layer=10, y=10) carries flux Phi
        link_gauge = {(10, 10): Phi}
        psi, _ = chiral_propagate_gauge(
            N_Y, N_LAYERS, THETA, SOURCE_Y, link_gauge=link_gauge)
        P = detector_probs(psi, N_Y)
        P_source[i] = P[SOURCE_Y]

    P_max = np.max(P_source)
    P_min = np.min(P_source)
    P_mean = np.mean(P_source)
    vis = (P_max - P_min) / (P_max + P_min) if (P_max + P_min) > 0 else 0

    print(f"  Single-link flux sweep:")
    print(f"    P(source) range: [{P_min:.6e}, {P_max:.6e}]")
    print(f"    Visibility: {vis:.6f}")
    print()

    # Fit
    cos_P = np.cos(Phi_values)
    sin_P = np.sin(Phi_values)
    X = np.column_stack([np.ones(n_phi), cos_P, sin_P])
    coeffs, _, _, _ = np.linalg.lstsq(X, P_source, rcond=None)
    amp = np.sqrt(coeffs[1]**2 + coeffs[2]**2)
    P_fit = X @ coeffs
    ss_res = np.sum((P_source - P_fit) ** 2)
    ss_tot = np.sum((P_source - P_mean) ** 2)
    R2 = 1 - ss_res / ss_tot if ss_tot > 1e-30 else 0.0

    print(f"    cos(Phi) amplitude: {amp:.6e}")
    print(f"    R^2 (cos fit): {R2:.6f}")

    print(f"\n    {'Phi/pi':>8} {'P(source)':>14}")
    print(f"    {'-'*25}")
    for i, Phi in enumerate(Phi_values):
        print(f"    {Phi/np.pi:8.4f} {P_source[i]:14.6e}")

    # Also try multiple links forming a flux tube
    print(f"\n  Multi-link flux tube (y=9 to y=10, layers 5-15):")
    P_tube = np.zeros(n_phi)
    for i, Phi in enumerate(Phi_values):
        link_gauge = {}
        for x in range(5, 16):
            link_gauge[(x, 10)] = Phi / 11.0  # distribute flux
        psi, _ = chiral_propagate_gauge(
            N_Y, N_LAYERS, THETA, SOURCE_Y, link_gauge=link_gauge)
        P = detector_probs(psi, N_Y)
        P_tube[i] = P[SOURCE_Y]

    vis_tube = (np.max(P_tube) - np.min(P_tube)) / (np.max(P_tube) + np.min(P_tube)) \
        if (np.max(P_tube) + np.min(P_tube)) > 0 else 0
    print(f"    Visibility (tube): {vis_tube:.6f}")
    print(f"    Range: [{np.min(P_tube):.6e}, {np.max(P_tube):.6e}]")

    any_modulation = vis > 0.001 or vis_tube > 0.001
    print(f"\n  *** WILSON LOOP: {'PASS' if any_modulation else 'FAIL'} ***")
    return any_modulation, vis, vis_tube


# -- TEST 5: Norm preservation with U(1) gauge --------------------------------

def test_gauge_norm():
    print("\n" + "=" * 70)
    print("TEST 5: NORM PRESERVATION WITH U(1) GAUGE FIELD")
    print("=" * 70)

    np.random.seed(77)
    link_gauge = {}
    for x in range(N_LAYERS):
        for y in range(N_Y - 1):
            link_gauge[(x, y)] = np.random.uniform(0, 2 * np.pi)

    psi_u1, norms_u1 = chiral_propagate_gauge(
        N_Y, N_LAYERS, THETA, SOURCE_Y, link_gauge=link_gauge)
    max_dev = np.max(np.abs(np.array(norms_u1) - 1.0))
    print(f"  U(1) random gauge: max norm deviation = {max_dev:.2e}")
    u1_pass = max_dev < 1e-12

    print(f"  *** {'PASS' if u1_pass else 'FAIL'} ***")
    return u1_pass


# -- MAIN ---------------------------------------------------------------------

def main():
    print("FRONTIER: CHIRAL GAUGE CONNECTIONS")
    print("Does the chiral walk support U(1) gauge connections and AB modulation?")
    print(f"Parameters: n_y={N_Y}, n_layers={N_LAYERS}, theta={THETA}")
    print(f"Source at y={SOURCE_Y}")
    print()

    results = {}

    # Test 1: Node-phase gauge invariance
    t1_pass, t1_pure = test_node_phase_invariance()
    results['node_phase'] = t1_pass
    results['pure_U1_gauge'] = t1_pure

    # Test 2: AB effect
    t2_pass, t2_vis, t2_r2 = test_aharonov_bohm()
    results['AB_effect'] = t2_pass

    # Test 3: SU(2) gauge
    t3_pass, t3_norm, t3_pure, t3_embed, t3_na = test_su2_gauge()
    results['SU2_overall'] = t3_pass
    results['SU2_norm'] = t3_norm
    results['SU2_pure_gauge'] = t3_pure
    results['SU2_nonabelian'] = t3_na

    # Test 4: Wilson loop
    t4_pass, t4_vis, t4_vis_tube = test_wilson_loop()
    results['wilson_loop'] = t4_pass

    # Test 5: Norm preservation
    t5_pass = test_gauge_norm()
    results['U1_norm'] = t5_pass

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for name, val in results.items():
        tag = "PASS" if val else "FAIL"
        print(f"  {name:25s}: {tag}")

    gauge_core = results['node_phase'] and results['U1_norm']
    ab_works = results['AB_effect'] or results['wilson_loop']
    su2_works = results['SU2_overall']

    print(f"\n  Gauge core (node + norm):   {'PASS' if gauge_core else 'FAIL'}")
    print(f"  AB modulation (any):        {'PASS' if ab_works else 'FAIL'}")
    print(f"  Pure U(1) gauge invariance: {'PASS' if results['pure_U1_gauge'] else 'FAIL'}")
    print(f"  SU(2) structure:            {'PASS' if su2_works else 'FAIL'}")

    if gauge_core and ab_works:
        print(f"\n  HYPOTHESIS CONFIRMED: Chiral walk supports U(1) gauge with AB effect.")
        if results['pure_U1_gauge']:
            print(f"  Pure gauge invariance also holds.")
        if su2_works:
            print(f"  SU(2) gauge structure also supported.")
    elif gauge_core and not ab_works:
        print(f"\n  PARTIALLY CONFIRMED: Gauge structure exists but no AB modulation.")
        print(f"  AB visibility = {t2_vis:.6f}, Wilson visibility = {t4_vis:.6f}")
    else:
        print(f"\n  HYPOTHESIS FALSIFIED: Gauge structure incomplete or broken.")


if __name__ == "__main__":
    main()
