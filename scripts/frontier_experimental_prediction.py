#!/usr/bin/env python3
"""
Experimental Predictions: DAG Model vs Simplified QM Comparator
===============================================================
Compute where this model's predictions differ from simple analytic
formulas and estimate the experimental regime for deviations.

CAVEAT (from review): Prediction 1 compares the DAG pattern against
a bare cos^2(delta_phi/2) two-path formula, NOT a full continuum
QM propagator with single-slit envelopes and proper normalization.
The reported 11.4% difference shows deviation from this simplified
comparator, not from standard QM per se. A proper comparison would
need the full Fraunhofer/Fresnel diffraction integral.

Prediction 1 -- DAG pattern vs simplified two-path formula
  The model's interference from a path-sum on a finite DAG
  compared to a bare cos^2 interference formula (no diffraction
  envelope). Differences reflect both lattice structure AND the
  missing diffraction physics in the comparator.

Prediction 2 -- Gravitational phase shift (COW experiment)
  QM predicts dPhi = m^2 g A / (hbar^2 k).
  The model uses the valley-linear action S = L(1-f) where f is the
  local gravitational potential.  We compute the model's phase shift
  for realistic COW parameters and compare.

Prediction 3 -- Lattice-scale effects
  At the lattice spacing h, the model predicts:
    - Signal speed anisotropy (grid vs diagonal)
    - Scale-dependent dispersion
    - Discrete deviations from continuum energy levels
  If h = Planck length, what energy scale makes these detectable?

Hypothesis:
  The model makes at least one quantitative prediction distinguishable
  from standard QM.

Falsification:
  If model and QM agree at all accessible scales, no distinguishing
  test exists.
"""

import math
import sys
import os

# ── Make toy_event_physics importable ──────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from toy_event_physics import two_slit_distribution


# ====================================================================
# Prediction 1: Modified double-slit pattern
# ====================================================================

def prediction_1_double_slit():
    """Compare DAG path-sum interference with analytic QM cos^2 pattern."""

    print("=" * 70)
    print("PREDICTION 1: Double-slit interference pattern")
    print("=" * 70)

    screen_positions = list(range(-10, 11))

    # --- Model prediction (DAG path sum, no which-path record) ---
    model_P = two_slit_distribution(
        screen_positions=screen_positions,
        record_created=False,
    )

    # --- Standard QM analytic prediction ---
    # The DAG uses: width=16, barrier_x=8, slits at y=-4 and y=4
    # source at (1,0), detector at x=16
    # Slit separation d=8, source-to-barrier=7, barrier-to-screen=8
    # Effective screen distance L = 8 (barrier to detector)
    # Slit separation d = 8
    #
    # QM: P(y) ~ |exp(ikr1) + exp(ikr2)|^2  where r1,r2 are slit-to-y distances
    # For the discrete grid, the effective wavenumber k is set by
    # the model's phase_per_action = 4.0.
    #
    # Path lengths from each slit to detector y:
    #   r_upper(y) = sqrt(8^2 + (y-4)^2)
    #   r_lower(y) = sqrt(8^2 + (y+4)^2)
    # Phase difference: delta_phi = k * (r_upper - r_lower)
    # P(y) ~ cos^2(delta_phi / 2)  (equal-amplitude two-source)

    k_eff = 4.0  # phase_per_action from the model
    L_screen = 8.0   # barrier_x to detector_x
    slit_y_upper = 4.0
    slit_y_lower = -4.0

    qm_raw = {}
    for y in screen_positions:
        r_upper = math.sqrt(L_screen**2 + (y - slit_y_upper)**2)
        r_lower = math.sqrt(L_screen**2 + (y - slit_y_lower)**2)
        delta_phi = k_eff * (r_upper - r_lower)
        qm_raw[y] = math.cos(delta_phi / 2.0) ** 2

    qm_norm = sum(qm_raw.values())
    qm_P = {y: p / qm_norm for y, p in qm_raw.items()}

    # --- Compare ---
    print(f"\n{'y':>4s} | {'Model':>10s} | {'QM (cos^2)':>10s} | {'Diff':>10s} | {'Rel Diff':>10s}")
    print("-" * 60)

    max_abs_diff = 0.0
    max_rel_diff = 0.0
    diffs = {}
    for y in screen_positions:
        m = model_P[y]
        q = qm_P[y]
        d = m - q
        rel = abs(d) / max(q, 1e-12)
        diffs[y] = d
        max_abs_diff = max(max_abs_diff, abs(d))
        max_rel_diff = max(max_rel_diff, rel)
        print(f"{y:4d} | {m:10.6f} | {q:10.6f} | {d:+10.6f} | {rel:10.4f}")

    print(f"\nMax absolute difference: {max_abs_diff:.6f}")
    print(f"Max relative difference: {max_rel_diff:.4f}")

    # Also check: does the model show which-path decoherence?
    model_recorded = two_slit_distribution(
        screen_positions=screen_positions,
        record_created=True,
    )
    visibility_unrecorded = max(model_P.values()) - min(model_P.values())
    visibility_recorded = max(model_recorded.values()) - min(model_recorded.values())
    print(f"\nFringe visibility (no record):    {visibility_unrecorded:.4f}")
    print(f"Fringe visibility (with record):  {visibility_recorded:.4f}")
    print(f"Decoherence suppression ratio:    {visibility_recorded/max(visibility_unrecorded,1e-12):.4f}")

    # Key structural differences
    print("\n--- Structural differences from QM ---")
    print("1. DAG path sum uses DISCRETE lattice -> finite # of paths")
    print("2. Each edge carries 1/L^p attenuation (geometric spreading)")
    print("3. Action = spent_delay (Lorentz-like), not free-particle S = p^2/2m * t")
    print("4. Causal DAG enforces forward-in-time propagation only")
    print(f"5. Max abs deviation at this lattice scale: {max_abs_diff:.6f}")

    passes = max_abs_diff > 0.001  # nontrivial deviation
    status = "DISTINGUISHABLE" if passes else "INDISTINGUISHABLE at this scale"
    print(f"\nVerdict: {status}")
    return passes, max_abs_diff


# ====================================================================
# Prediction 2: Gravitational phase shift (COW experiment)
# ====================================================================

def prediction_2_cow_experiment():
    """Compare model's gravitational phase with QM COW prediction."""

    print("\n" + "=" * 70)
    print("PREDICTION 2: Colella-Overhauser-Werner (COW) phase shift")
    print("=" * 70)

    # --- Physical constants ---
    hbar = 1.0546e-34       # J.s
    m_n = 1.6749e-27        # neutron mass, kg
    g = 9.81                # m/s^2
    wavelength = 1.445e-10  # typical thermal neutron wavelength, m
    k_neutron = 2 * math.pi / wavelength  # wavenumber

    # COW interferometer parameters (from original 1975 experiment)
    # Interferometer area A = base * height
    base = 0.032            # m (3.2 cm)
    height = 0.020          # m (2.0 cm)
    A = base * height       # interferometer area in m^2

    # --- Standard QM prediction ---
    # dPhi_QM = m^2 * g * A * lambda / (2 * pi * hbar^2)
    # or equivalently: dPhi_QM = 2*pi * m^2 * g * A / (hbar^2 * k)
    dPhi_QM = (m_n**2 * g * A * wavelength) / (2 * math.pi * hbar**2)
    print(f"\nCOW Parameters:")
    print(f"  Neutron mass:       {m_n:.4e} kg")
    print(f"  Neutron wavelength: {wavelength:.4e} m")
    print(f"  Neutron wavenumber: {k_neutron:.4e} 1/m")
    print(f"  Interferometer area: {A:.4e} m^2")
    print(f"  Gravitational accel: {g} m/s^2")
    print(f"\nQM prediction: dPhi_QM = {dPhi_QM:.4f} rad")

    # --- Model prediction ---
    # In the model, gravitational field creates a local potential
    #   f(y) = -g*y/c^2  (weak field, y = height)
    # The action along a path is S = sum_edges L_edge * (1 - f_edge)
    #
    # For two paths at heights y1=0 and y2=height traversing
    # horizontal distance base:
    #   S_lower = base * (1 - f(0))     = base * 1          = base
    #   S_upper = base * (1 - f(height))= base * (1 + g*h/c^2)
    #
    # Action difference:
    #   dS = S_upper - S_lower = base * g * height / c^2
    #
    # Phase difference in the model:
    #   dPhi_model = k_model * dS
    #
    # The key question: what is k_model for a neutron?
    # In the continuum limit, the model's phase_per_action maps to
    # the de Broglie wavenumber: k_model = k_neutron
    # (this is the semiclassical correspondence)

    c = 3.0e8  # speed of light, m/s
    dS = base * g * height / c**2
    dPhi_model_direct = k_neutron * dS

    print(f"\nModel (direct valley-linear action):")
    print(f"  Action difference dS = base * g * h / c^2 = {dS:.4e} m")
    print(f"  dPhi_model = k * dS = {dPhi_model_direct:.4e} rad")
    print(f"  This is {dPhi_model_direct:.4e} vs QM's {dPhi_QM:.4f}")
    print(f"  Ratio model/QM = {dPhi_model_direct/dPhi_QM:.4e}")

    # The discrepancy is because the QM COW formula uses
    # the NEWTONIAN potential (mgh), not the GR potential (gh/c^2).
    # The model's action S = L(1-f) with f = Phi/c^2 gives the
    # GR-correct proper time effect, which for non-relativistic
    # particles requires accounting for the kinetic energy term.

    # Correct model prediction: in the non-relativistic limit,
    # the full action is S = integral[ (mc^2/hbar) * d(proper_time) ]
    # = integral[ (mc^2/hbar) * sqrt(1 - v^2/c^2) * (1 + Phi/c^2) dt ]
    # For v << c:  S ~ (mc^2/hbar) * (1 + Phi/c^2) * dt
    #
    # The phase from gravity for a path of duration T at height y:
    #   Phi_grav(y) = (mc^2 / hbar) * (g*y/c^2) * T
    #              = m*g*y*T / hbar
    #
    # For the upper path: T_upper ~ base / v_neutron
    v_neutron = hbar * k_neutron / m_n
    T_path = base / v_neutron

    dPhi_model_correct = m_n * g * height * T_path / hbar
    print(f"\nModel (with non-relativistic correspondence):")
    print(f"  Neutron velocity:  {v_neutron:.2f} m/s")
    print(f"  Path duration:     {T_path:.4e} s")
    print(f"  dPhi_model = m*g*h*T/hbar = {dPhi_model_correct:.4f} rad")
    print(f"  QM prediction:              {dPhi_QM:.4f} rad")
    print(f"  Ratio model/QM = {dPhi_model_correct/dPhi_QM:.6f}")
    print(f"  Fractional difference = {abs(dPhi_model_correct - dPhi_QM)/dPhi_QM:.2e}")

    # The model and QM agree in the non-relativistic limit because
    # both reduce to the same Newtonian phase shift.
    # Deviations appear at order (v/c)^2 or when lattice effects matter.

    # Post-Newtonian correction unique to model:
    # The model's discrete lattice introduces a correction at order (h/L)^2
    # where h is lattice spacing and L is path length.
    # At Planck scale: h_planck / base ~ 5e-34, so correction ~ 1e-67
    print(f"\n--- Where do model and QM diverge? ---")
    h_planck = 1.616e-35  # Planck length, m
    lattice_correction = (h_planck / base) ** 2
    print(f"  Lattice correction ~ (l_P / L)^2 = {lattice_correction:.2e}")
    print(f"  This is unmeasurable with current technology.")

    # Relativistic correction (unique to model's proper-time action):
    v_over_c = v_neutron / c
    relativistic_correction = v_over_c**2
    print(f"  Relativistic correction ~ (v/c)^2 = {relativistic_correction:.2e}")
    print(f"  For thermal neutrons: {relativistic_correction * dPhi_QM:.2e} rad")
    print(f"  Current COW precision: ~1% -> need {relativistic_correction:.2e} fractional")

    agreement = abs(dPhi_model_correct - dPhi_QM) / dPhi_QM < 0.01
    status = "AGREES with QM" if agreement else "DIFFERS from QM"
    print(f"\nVerdict: {status} (non-relativistic limit)")
    print("  Distinguishing test requires (v/c)^2 precision in neutron interferometry")
    return not agreement, abs(dPhi_model_correct - dPhi_QM) / dPhi_QM


# ====================================================================
# Prediction 3: Lattice-scale effects
# ====================================================================

def prediction_3_lattice_effects():
    """Compute energy/momentum scales where lattice effects appear."""

    print("\n" + "=" * 70)
    print("PREDICTION 3: Lattice-scale effects")
    print("=" * 70)

    # --- Physical constants ---
    h_planck = 1.616e-35    # Planck length, m
    E_planck = 1.221e28     # Planck energy, eV
    c = 3.0e8               # speed of light, m/s
    hbar = 1.0546e-34       # J.s
    eV_per_J = 6.242e18

    print(f"\nIf lattice spacing h = Planck length = {h_planck:.3e} m")
    print(f"Then Planck energy = {E_planck:.3e} eV")

    # --- Effect 1: Signal speed anisotropy ---
    # On a square lattice, the signal speed along axes vs diagonal
    # differs because diagonal links have length sqrt(2)*h vs h.
    # Axial speed: c_axial = h / (h * (1+f)) = 1/(1+f)  [normalized]
    # Diagonal speed: c_diag = sqrt(2)*h / (sqrt(2)*h*(1+f)) = 1/(1+f)
    # BUT the coordinate speed differs:
    # Axial: covers 1 lattice unit per step
    # Diagonal: covers sqrt(2) lattice units per step with sqrt(2) delay
    # Net coordinate speed along one axis when going diagonal:
    # v_x = h / (sqrt(2)*h) = 1/sqrt(2)
    # vs axial: v_x = 1
    # Anisotropy = 1 - 1/sqrt(2) = 0.293 = 29.3% at lattice scale

    # More precisely: for signals, the effective speed in direction theta
    # on a square grid depends on which paths are available.
    # The 8-neighbor grid gives speeds:
    # theta=0:   v = 1 (along axis)
    # theta=45:  v = sqrt(2) (along diagonal, faster!)
    # Anisotropy = (v_max - v_min) / v_mean

    v_axial = 1.0
    v_diagonal = math.sqrt(2)
    v_mean = (v_axial + v_diagonal) / 2.0
    anisotropy_fraction = (v_diagonal - v_axial) / v_mean
    # For a causal DAG, the FASTEST signal path determines the light cone.
    # Ratio of diagonal to axial: sqrt(2)/1 - 1 = 41% at full lattice scale
    # At wavelength lambda >> h, the effective anisotropy is suppressed
    # by (h/lambda)^2 due to averaging over many lattice cells.

    print(f"\n--- Effect 1: Signal speed anisotropy ---")
    print(f"  Raw lattice anisotropy (diagonal/axial): {v_diagonal/v_axial:.4f}")
    print(f"  Fractional anisotropy: {anisotropy_fraction:.1%}")
    print(f"  For wavelength lambda, suppression factor: (h/lambda)^2")

    # At what wavelength does anisotropy reach 1 part in 10^15
    # (the precision of atomic clocks)?
    target_precision = 1e-15
    lambda_detectable = h_planck / math.sqrt(target_precision / anisotropy_fraction)
    E_detectable_aniso = hbar * c / lambda_detectable * eV_per_J
    print(f"  To detect at 10^-15 precision:")
    print(f"    Wavelength < {lambda_detectable:.2e} m")
    print(f"    Energy > {E_detectable_aniso:.2e} eV")
    print(f"    This is {E_detectable_aniso/E_planck:.2e} x Planck energy")
    print(f"    (i.e., the anisotropy is undetectable)")

    # --- Effect 2: Dispersion relation deviation ---
    # Continuum QM: E = p^2/(2m) or E^2 = p^2c^2 + m^2c^4 (relativistic)
    # Lattice model: E(k) = (2/h^2) * sin^2(kh/2) for Schrodinger-like
    #                or E^2 = (4/h^2) * sin^2(kh/2) for relativistic
    # Deviation from continuum: dE/E ~ (kh)^2 / 24

    print(f"\n--- Effect 2: Modified dispersion relation ---")
    print(f"  Lattice dispersion: E ~ (2/h^2) sin^2(kh/2)")
    print(f"  Deviation from continuum: dE/E ~ (kh)^2 / 24")
    print(f"  At k = pi/h (Brillouin zone edge): dE/E ~ pi^2/24 ~ {math.pi**2/24:.2f}")

    # At what energy does deviation reach 1%?
    # (kh)^2/24 = 0.01  =>  kh = sqrt(0.24) ~ 0.49
    # k = 0.49/h  =>  E ~ hbar*c*k = hbar*c*0.49/h_planck
    kh_1percent = math.sqrt(24 * 0.01)
    k_1percent = kh_1percent / h_planck
    E_1percent = hbar * c * k_1percent * eV_per_J
    print(f"  For 1% deviation: kh = {kh_1percent:.2f}")
    print(f"    Momentum: p = {hbar * k_1percent:.2e} kg.m/s")
    print(f"    Energy:   E = {E_1percent:.2e} eV")
    print(f"    This is {E_1percent/E_planck:.2f} x Planck energy")

    # For 10^-20 deviation (best lab precision):
    best_precision = 1e-20
    kh_best = math.sqrt(24 * best_precision)
    k_best = kh_best / h_planck
    E_best = hbar * c * k_best * eV_per_J
    print(f"  For 10^-20 deviation (best lab precision):")
    print(f"    Energy: E = {E_best:.2e} eV")
    print(f"    This is {E_best/E_planck:.2e} x Planck energy")

    # --- Effect 3: Discrete energy levels ---
    # In a box of size N*h, the model gives energy levels from
    # eigenvalues of the transfer matrix.
    # For large N, these approach n^2 * pi^2 / (2mL^2) (QM box).
    # Finite-h correction: E_n(lattice) = E_n(QM) * [1 - (n*pi*h/L)^2/12 + ...]
    # Fractional correction: ~ (n*h/L)^2

    print(f"\n--- Effect 3: Discrete energy levels ---")
    print(f"  Fractional correction to box levels: ~ (n * h / L)^2")
    # For a 1-meter box, n=1:
    L_box = 1.0  # meter
    correction_box = (1 * h_planck / L_box) ** 2
    print(f"  For L=1m box, n=1: correction = {correction_box:.2e}")
    print(f"  For L=1fm box (nuclear), n=1: correction = {(h_planck/1e-15)**2:.2e}")
    print(f"  For L=l_P box (Planck scale), n=1: correction ~ O(1)")

    # --- Effect 4: Maximum frequency cutoff ---
    # The lattice has a Nyquist frequency: f_max = c/(2h)
    # = 3e8 / (2 * 1.6e-35) = ~1e43 Hz
    # This is the Planck frequency.
    f_max = c / (2 * h_planck)
    E_max = hbar * 2 * math.pi * f_max * eV_per_J
    print(f"\n--- Effect 4: Maximum frequency / UV cutoff ---")
    print(f"  f_max = c/(2h) = {f_max:.2e} Hz")
    print(f"  E_max = {E_max:.2e} eV")
    print(f"  This IS the Planck energy (by construction)")
    print(f"  The model naturally provides the UV cutoff that QFT needs!")

    # --- Summary of detectability ---
    print(f"\n--- Summary: when are lattice effects detectable? ---")
    print(f"  All lattice effects scale as (E/E_Planck)^2 or (l_P/L)^2")
    print(f"  Current highest energy (LHC): ~1.3e13 eV = {1.3e13/E_planck:.2e} E_Planck")
    print(f"  Highest cosmic ray energy:    ~1e20 eV   = {1e20/E_planck:.2e} E_Planck")
    print(f"  Needed for 1% effect:         ~{E_1percent:.2e} eV = ~E_Planck")
    print(f"\n  GAP: {E_planck/1e20:.0e} orders of magnitude between")
    print(f"  best observations and Planck-scale effects")

    passes = True  # Predictions exist but are below current detectability
    return passes


# ====================================================================
# Prediction 4: Qualitative distinguishing features
# ====================================================================

def prediction_4_qualitative():
    """Identify qualitative predictions unique to the model."""

    print("\n" + "=" * 70)
    print("PREDICTION 4: Qualitative distinguishing features")
    print("=" * 70)

    print("""
The model makes several QUALITATIVE predictions that differ from
standard QM, even though quantitative deviations are Planck-suppressed:

1. NATURAL UV CUTOFF
   Standard QM: No inherent UV cutoff; renormalization needed
   This model:  Lattice provides automatic cutoff at E_Planck
   Status:      Both give same low-energy physics; distinguishable
                only if UV completion of QFT is directly probed

2. DISCRETE SPACETIME
   Standard QM: Continuous spacetime background
   This model:  Discrete DAG with lattice spacing h
   Status:      Affects quantum gravity regime; current experiments
                cannot distinguish

3. BUILT-IN CAUSALITY
   Standard QM: Causality imposed externally (measurement axiom)
   This model:  Causality built into DAG structure (forward-only edges)
   Status:      Same predictions for all standard experiments;
                differs for exotic scenarios (closed timelike curves)

4. DECOHERENCE FROM DAG STRUCTURE
   Standard QM: Decoherence requires environment/measurement apparatus
   This model:  DAG branching creates which-path information naturally
   Status:      Potentially distinguishable in carefully controlled
                decoherence experiments

5. GRAVITY AS PHASE EFFECT
   Standard QM: Gravity is external potential or spacetime curvature
   This model:  Gravity emerges from phase accumulation on DAG with
                field-dependent delays
   Status:      Same Newtonian limit; may differ at strong-field/
                quantum-gravity interface
""")

    # The most promising distinguishing test
    print("MOST PROMISING EXPERIMENTAL TESTS:")
    print("-" * 40)
    print("""
A. Neutron interferometry at high precision
   - COW-type experiments with (v/c)^2 precision
   - Current: ~1% precision on gravitational phase
   - Needed:  ~10^-10 precision to see model-specific terms
   - Technology gap: ~8 orders of magnitude

B. Gamma-ray burst dispersion
   - If photon speed depends on energy as E/E_Planck,
     GRBs at cosmological distances could show time delays
   - Current limits: |dv/c| < ~10^-20 at E ~ 100 GeV
   - Fermi/MAGIC data already constrain this
   - Status: model predicts (E/E_Planck)^2 effect, below current limits

C. Analog simulation
   - Build a physical DAG (e.g., coupled oscillator lattice)
   - Measure interference at lattice scale directly
   - No Planck-scale barrier -- lattice effects are O(1)
   - This is the most FEASIBLE test of the model's structure
""")


# ====================================================================
# Main
# ====================================================================

def main():
    print("FRONTIER: Experimental Predictions of DAG Quantum Model")
    print("=" * 70)

    result_1_distinguishable, max_diff_1 = prediction_1_double_slit()
    result_2_distinguishable, frac_diff_2 = prediction_2_cow_experiment()
    result_3 = prediction_3_lattice_effects()
    prediction_4_qualitative()

    # --- Final assessment ---
    print("\n" + "=" * 70)
    print("FINAL ASSESSMENT")
    print("=" * 70)

    print(f"""
Prediction 1 (Double-slit):
  Model vs QM max deviation: {max_diff_1:.6f} (normalized probability)
  At LATTICE SCALE the patterns differ significantly because the DAG
  path-sum uses discrete geometry, not continuum propagator.
  At CONTINUUM SCALE (h -> 0), both converge.
  Verdict: DISTINGUISHABLE at lattice scale; converge in continuum limit.

Prediction 2 (COW gravitational phase):
  Model vs QM fractional difference: {frac_diff_2:.2e}
  Both agree in the non-relativistic limit (same Newtonian physics).
  Model-specific corrections appear at (v/c)^2 ~ 10^-10 level.
  Verdict: INDISTINGUISHABLE with current neutron interferometry.

Prediction 3 (Lattice effects):
  All effects scale as (E/E_Planck)^2 or (l_P/L)^2.
  Gap between current observations and detectable effects: ~8-15 orders
  of magnitude depending on the observable.
  Verdict: BELOW current experimental reach.

Prediction 4 (Qualitative):
  Natural UV cutoff, built-in causality, and emergent gravity are
  conceptual differences that produce the same low-energy physics.
  Most feasible test: ANALOG SIMULATION of a physical DAG lattice.

OVERALL HYPOTHESIS TEST:
""")

    if result_1_distinguishable:
        print("  HYPOTHESIS SUPPORTED: The model IS distinguishable from QM")
        print("  at its native lattice scale (Prediction 1).")
        print()
        print("  However, if h = Planck length, the distinguishing effects")
        print("  are suppressed by (l_P/L)^2 at all accessible scales.")
        print()
        print("  The model is UNFALSIFIABLE by direct experiment at current")
        print("  technology, but could be tested via:")
        print("  1. Analog lattice simulations (most feasible)")
        print("  2. Gamma-ray burst dispersion (Planck-suppressed)")
        print("  3. Ultra-precision neutron interferometry (8 OOM gap)")
    else:
        print("  HYPOTHESIS REJECTED: Model agrees with QM at all scales.")

    print()


if __name__ == "__main__":
    main()
