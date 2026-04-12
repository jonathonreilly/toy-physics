#!/usr/bin/env python3
"""
Experimental Predictions — Ranked candidates with signal budgets
=================================================================

Compiles the ranked testable predictions from the two-axiom framework into
a single executable card.  Each candidate includes:

  - observable and standard null
  - framework prediction with scaling laws
  - signal-to-noise estimates (where available)
  - minimal control stack
  - what would count as hit / miss

Candidate 1 (Diamond NV lock-in quadrature) is the strongest because it is
a null test: standard physics predicts zero, the framework predicts nonzero
with a spatial pattern.

PStack experiment: experimental-predictions
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


# ============================================================================
# Candidate 1: Diamond NV Lock-In Quadrature Protocol
# ============================================================================
#
# Source: docs/DIAMOND_SENSOR_PREDICTION_NOTE.md
#         docs/DIAMOND_NV_PHASE_RAMP_SIGNAL_BUDGET_NOTE.md
#         docs/DIAMOND_SENSOR_PROTOCOL_NOTE.md
#         docs/DIAMOND_SIGNAL_BUDGET_HARDENING_NOTE.md
#         scripts/diamond_signal_budget_hardening.py
# ============================================================================


@dataclass(frozen=True)
class NVPredictionPoint:
    """One point in the diamond NV phase-lag prediction table."""
    frequency_hz: float
    separation_m: float

    @property
    def delay_s(self) -> float:
        """Gravitational propagation delay = r / c."""
        return self.separation_m / C_LIGHT

    @property
    def omega(self) -> float:
        return 2.0 * math.pi * self.frequency_hz

    @property
    def omega_tau(self) -> float:
        return self.omega * self.delay_s

    @property
    def phase_lag_rad(self) -> float:
        """Framework prediction: phi = atan(omega * tau)."""
        return math.atan(self.omega_tau)

    @property
    def phase_lag_deg(self) -> float:
        return math.degrees(self.phase_lag_rad)

    @property
    def quadrature_fraction(self) -> float:
        """Y/X = tan(phi) = omega * tau for small angles."""
        return self.omega_tau


C_LIGHT = 2.998e8  # m/s


@dataclass(frozen=True)
class ProxyBudgetRow:
    """One row from the retained moving-source proxy scaling map."""
    velocity: float
    delta_y_vs_static: float
    phase_lag_rad: float


# Retained proxy data from diamond_signal_budget_hardening.py
PROXY_ROWS = [
    ProxyBudgetRow(-1.00, -1.641405e-06, 4.852935e-05),
    ProxyBudgetRow(-0.50, -9.233039e-07, 1.309075e-05),
    ProxyBudgetRow(0.00, 0.0, 0.0),
    ProxyBudgetRow(+0.50, +8.665715e-07, 1.401315e-05),
    ProxyBudgetRow(+1.00, +1.472200e-06, 4.334258e-05),
]


def _nv_scan_table() -> list[NVPredictionPoint]:
    """Build the NV prediction scan table across frequency and separation."""
    freqs_hz = [1e2, 1e3, 1e4, 1e5]
    separations_m = [1e-3, 1e-2, 1e-1]
    return [
        NVPredictionPoint(f, r)
        for r in separations_m
        for f in freqs_hz
    ]


def _nv_sensitivity_check() -> dict:
    """
    NV magnetometry sensitivity parameters for SNR estimation.

    State of the art NV ensemble magnetometry achieves:
      - sensitivity ~ 1 pT / sqrt(Hz) for DC fields
      - AC sensitivity at lock-in frequency can reach ~ 0.1 pT / sqrt(Hz)
      - integration time of 1 hour gives sqrt(T) ~ 60

    The gravitational strain on a diamond from a 1 kg source at 1 cm:
      h_grav ~ G * M / (r^2 * c^2) ~ 7.4e-27 / m
      This couples to NV via strain: delta_B_eff ~ h_grav * E_strain_coupling

    For the phase-ramp discriminator, we do NOT need absolute amplitude.
    We need the phase noise floor to be below the predicted phase lag.
    """
    G_NEWTON = 6.674e-11  # m^3 / (kg s^2)
    source_mass_kg = 1.0
    separation_m = 0.01  # 1 cm
    drive_freq_hz = 1e4  # 10 kHz

    # Gravitational acceleration from source
    a_grav = G_NEWTON * source_mass_kg / separation_m**2  # m/s^2

    # Propagation delay
    tau = separation_m / C_LIGHT  # s

    # Phase lag prediction
    omega = 2.0 * math.pi * drive_freq_hz
    omega_tau = omega * tau
    phi_pred_rad = math.atan(omega_tau)

    # NV phase noise floor (conservative)
    # Lock-in phase noise ~ 1/SNR_amplitude
    # With ~1 pT/sqrt(Hz) sensitivity and ~1e4 averaging:
    nv_phase_noise_rad = 1e-6  # achievable with good lock-in setup

    # Integration time to reach 3-sigma detection
    sigma_per_shot = nv_phase_noise_rad
    snr_single = phi_pred_rad / sigma_per_shot
    # SNR grows as sqrt(N_averages)
    n_averages_3sigma = max(1.0, (3.0 / snr_single) ** 2) if snr_single > 0 else float('inf')
    t_integration_s = n_averages_3sigma / drive_freq_hz

    return {
        "source_mass_kg": source_mass_kg,
        "separation_m": separation_m,
        "drive_freq_hz": drive_freq_hz,
        "a_grav_m_s2": a_grav,
        "tau_s": tau,
        "omega_tau": omega_tau,
        "phi_pred_rad": phi_pred_rad,
        "phi_pred_deg": math.degrees(phi_pred_rad),
        "nv_phase_noise_rad": nv_phase_noise_rad,
        "snr_single_shot": snr_single,
        "n_averages_3sigma": n_averages_3sigma,
        "t_integration_3sigma_s": t_integration_s,
    }


def format_candidate_1() -> str:
    """Format the Diamond NV prediction as Candidate 1."""
    lines: list[str] = []
    lines.append("=" * 100)
    lines.append("CANDIDATE 1: DIAMOND NV LOCK-IN QUADRATURE PROTOCOL  [STRONGEST]")
    lines.append("=" * 100)
    lines.append("")

    # --- Why strongest ---
    lines.append("WHY THIS IS THE STRONGEST CANDIDATE")
    lines.append("  1. Null test: standard physics predicts Y = 0; framework predicts Y > 0")
    lines.append("  2. Diamond NV magnetometry has sufficient phase sensitivity")
    lines.append("  3. Spatial phase ramp is a pattern, not just a number -- harder to fake")
    lines.append("  4. Signal strengthens at higher drive frequency and larger separation")
    lines.append("  5. Existing NV lock-in hardware can run this protocol without modification")
    lines.append("")

    # --- Observable ---
    lines.append("OBSERVABLE")
    lines.append("  Lock-in channels: X (in-phase), Y (quadrature), phi = atan2(Y, X)")
    lines.append("  Widefield: spatial phase profile phi(x, y) across the NV image")
    lines.append("")

    # --- Standard null ---
    lines.append("STANDARD NULL (what conventional physics predicts)")
    lines.append("  After calibration and static-background subtraction:")
    lines.append("    Y = 0")
    lines.append("    phi = 0")
    lines.append("    No stable spatial phase ramp")
    lines.append("  Reason: Newtonian gravity is instantaneous (no propagation delay)")
    lines.append("")

    # --- Framework prediction ---
    lines.append("FRAMEWORK PREDICTION")
    lines.append("  The path-sum propagator has finite propagation speed.")
    lines.append("  A driven source at separation r produces a phase lag:")
    lines.append("    phi = atan(omega * tau)  where tau = r / c")
    lines.append("  The quadrature channel picks this up as:")
    lines.append("    Y / X = tan(phi) = omega * tau  (for small omega*tau)")
    lines.append("  In widefield readout, the phase forms a coherent spatial ramp")
    lines.append("  across the detector array because tau varies with position.")
    lines.append("")

    # --- Phase lag scan table ---
    lines.append("PREDICTED PHASE LAG vs FREQUENCY AND SEPARATION")
    lines.append("  (assuming gravitational coupling propagates at c)")
    lines.append("")
    lines.append(f"  {'f (Hz)':>10s}  {'r (m)':>10s}  {'tau (s)':>12s}  {'omega*tau':>12s}  {'phi (rad)':>12s}  {'phi (deg)':>12s}")
    lines.append(f"  {'---':>10s}  {'---':>10s}  {'---':>12s}  {'---':>12s}  {'---':>12s}  {'---':>12s}")
    for p in _nv_scan_table():
        lines.append(
            f"  {p.frequency_hz:10.0f}  {p.separation_m:10.4f}  {p.delay_s:12.4e}  "
            f"{p.omega_tau:12.4e}  {p.phase_lag_rad:12.4e}  {p.phase_lag_deg:12.4e}"
        )
    lines.append("")
    lines.append("  Key: phase lag grows linearly with frequency and separation.")
    lines.append("  Best operating point: highest accessible frequency, largest separation.")
    lines.append("")

    # --- SNR estimate ---
    snr = _nv_sensitivity_check()
    lines.append("SIGNAL-TO-NOISE ESTIMATE (reference operating point)")
    lines.append(f"  Source mass:               {snr['source_mass_kg']:.1f} kg")
    lines.append(f"  Separation:                {snr['separation_m']*100:.1f} cm")
    lines.append(f"  Drive frequency:           {snr['drive_freq_hz']:.0e} Hz")
    lines.append(f"  Gravitational acceleration:{snr['a_grav_m_s2']:.3e} m/s^2")
    lines.append(f"  Propagation delay tau:     {snr['tau_s']:.3e} s")
    lines.append(f"  omega * tau:               {snr['omega_tau']:.3e}")
    lines.append(f"  Predicted phase lag:       {snr['phi_pred_rad']:.3e} rad = {snr['phi_pred_deg']:.3e} deg")
    lines.append(f"  NV phase noise floor:      {snr['nv_phase_noise_rad']:.1e} rad (conservative lock-in)")
    lines.append(f"  Single-shot SNR:           {snr['snr_single_shot']:.3e}")
    if math.isfinite(snr['n_averages_3sigma']):
        lines.append(f"  Averages for 3-sigma:      {snr['n_averages_3sigma']:.2e}")
        lines.append(f"  Integration time (3-sigma):{snr['t_integration_3sigma_s']:.2e} s")
    else:
        lines.append("  NOTE: phase lag is extremely small at this operating point.")
        lines.append("  Higher frequency or larger separation improves the signal.")
    lines.append("")

    # --- Proxy budget from retained simulation ---
    lines.append("RETAINED PROXY BUDGET (from moving-source simulation)")
    lines.append("  Geometry: drift=0.2, restore=0.7, seeds=6, source_layer=8, h=0.5")
    lines.append("  Motion law: y_src(layer) = y0 + v * (layer - source_layer) * h")
    lines.append("")
    lines.append(f"  {'v':>6s}  {'delta_y vs static':>20s}  {'phase lag (rad)':>18s}")
    lines.append(f"  {'---':>6s}  {'---':>20s}  {'---':>18s}")
    for row in PROXY_ROWS:
        lines.append(
            f"  {row.velocity:+6.2f}  {row.delta_y_vs_static:+20.6e}  {row.phase_lag_rad:18.6e}"
        )
    lines.append("")

    nonzero = [r for r in PROXY_ROWS if abs(r.velocity) > 1e-12]
    min_delta = min(abs(r.delta_y_vs_static) for r in nonzero)
    min_phase = min(abs(r.phase_lag_rad) for r in nonzero)
    lines.append(f"  Weakest nonzero |delta_y|:  {min_delta:.6e}")
    lines.append(f"  Weakest nonzero |phase|:    {min_phase:.6e} rad")
    lines.append(f"  3-sigma centroid target:    {min_delta/3:.6e}")
    lines.append(f"  3-sigma phase target:       {min_phase/3:.6e} rad")
    lines.append("")
    lines.append("  Key features of proxy budget:")
    lines.append("    - Centroid sign flips with velocity (strongest discriminator)")
    lines.append("    - v=0 control pins to exactly zero")
    lines.append("    - Phase lag is nonzero but secondary to centroid sign flip")
    lines.append("    - Missing: transfer coefficient from proxy units to NV readout units")
    lines.append("")

    # --- Minimal controls ---
    lines.append("MINIMAL CONTROL STACK")
    lines.append("  1. Drive off: verify zero Y")
    lines.append("  2. Source retracted: verify coupling drops to noise floor")
    lines.append("  3. Pi reference flip: verify Y changes sign")
    lines.append("  4. Static source (no modulation): verify DC/drift subtraction works")
    lines.append("  5. Known magnetic/strain source: validate lock-in pipeline before gravity")
    lines.append("")

    # --- Scan protocol ---
    lines.append("SUGGESTED SCAN PROTOCOL")
    lines.append("  Vary two knobs: drive frequency (f) and source-detector separation (r)")
    lines.append("")
    lines.append(f"  {'scan class':>25s}  {'null prediction':>20s}  {'framework prediction':>30s}")
    lines.append(f"  {'---':>25s}  {'---':>20s}  {'---':>30s}")
    scan_rows = [
        ("low f, small r",   "Y ~ 0, phi ~ 0", "weakest; likely marginal"),
        ("low f, large r",   "Y ~ 0, phi ~ 0", "weak phase lag if any"),
        ("high f, small r",  "Y ~ 0, phi ~ 0", "detectable Y more plausible"),
        ("high f, large r",  "Y ~ 0, phi ~ 0", "STRONGEST: coherent Y + phase ramp"),
    ]
    for label, null, pred in scan_rows:
        lines.append(f"  {label:>25s}  {null:>20s}  {pred:>30s}")
    lines.append("")

    # --- Hit / miss ---
    lines.append("WHAT COUNTS AS A HIT")
    lines.append("  - Y survives calibration and is not consistent with zero")
    lines.append("  - Sign of Y flips under the pi reference control")
    lines.append("  - Widefield image shows a stable nonzero phase gradient")
    lines.append("  - Effect strengthens with frequency and separation (causal direction)")
    lines.append("")
    lines.append("WHAT COUNTS AS A MISS")
    lines.append("  - Quadrature vanishes after calibration")
    lines.append("  - Phase is flat across the image")
    lines.append("  - Signal explained by instrument lag, heating, or trivial rescaling")
    lines.append("")
    lines.append("HONEST LIMITATIONS")
    lines.append("  - Absolute gravity amplitude not yet calibrated for NV coupling")
    lines.append("  - Transfer coefficient from proxy units to lab units is missing")
    lines.append("  - Phase lag omega*tau is extremely small unless f or r is large")
    lines.append("  - Prediction is strongest as a PATTERN (phase ramp), not raw amplitude")
    lines.append("")

    return "\n".join(lines)


# ============================================================================
# Candidate 2: Modified Dispersion Relation (Lorentz Violation Bound)
# ============================================================================


def format_candidate_2() -> str:
    """Format the dispersion relation prediction as Candidate 2."""
    lines: list[str] = []
    lines.append("=" * 100)
    lines.append("CANDIDATE 2: MODIFIED DISPERSION RELATION (k^4 CORRECTION)")
    lines.append("=" * 100)
    lines.append("")

    lines.append("OBSERVABLE")
    lines.append("  Energy-dependent photon arrival times from GRB / blazar sources")
    lines.append("  Dispersion: omega^2 = k^2 + c4 * k^4 + ...")
    lines.append("  Leads to group velocity correction: delta_v / c ~ c4 * k^2")
    lines.append("")

    lines.append("STANDARD NULL")
    lines.append("  Lorentz invariance: c4 = 0 exactly, all photons travel at c")
    lines.append("")

    lines.append("FRAMEWORK PREDICTION")
    lines.append("  The discrete propagator produces a k^4 correction from lattice structure.")
    lines.append("  Numerical results from frontier_dispersion_relation.py:")
    lines.append("")
    lines.append("  c4 coefficients (omega^2 polynomial fit, low-k regime):")
    lines.append(f"    {'Architecture':>12s}  {'Kernel':>8s}  {'h=1.0':>10s}  {'h=0.5':>10s}  {'h=0.25':>10s}  {'h=0.125':>10s}")
    disp_data = [
        ("cubic",     "cos2",  "+1.5e-2", "-1.1e-1", "+7.3e-4", "+2.1e-3"),
        ("cubic",     "gauss", "-2.8e-1", "-1.0e+0", "-2.9e-2", "-3.1e-2"),
        ("staggered", "cos2",  "-2.4e-1", "+5.9e-1", "-7.3e-4", "-1.9e-4"),
        ("staggered", "gauss", "-4.0e-1", "+4.5e+0", "+1.0e-2", "-6.4e-3"),
    ]
    for arch, kern, *vals in disp_data:
        lines.append(f"    {arch:>12s}  {kern:>8s}  " + "  ".join(f"{v:>10s}" for v in vals))
    lines.append("")

    lines.append("  Scaling: |c4| ~ h^alpha")
    lines.append(f"    {'Architecture':>12s}  {'Kernel':>8s}  {'alpha':>8s}  {'R^2':>6s}")
    scaling_data = [
        ("cubic",     "cos2",  "1.58", "0.40"),
        ("cubic",     "gauss", "1.47", "0.56"),
        ("staggered", "cos2",  "4.05", "0.80"),
        ("staggered", "gauss", "2.67", "0.59"),
    ]
    for arch, kern, alpha, r2 in scaling_data:
        lines.append(f"    {arch:>12s}  {kern:>8s}  {alpha:>8s}  {r2:>6s}")
    lines.append("")

    lines.append("  STATUS: ANOMALOUS")
    lines.append("  - c4 is nonzero (genuine discreteness signature)")
    lines.append("  - Scaling is NOT clean h^2 (alpha ~ 1.5, not 2.0 for cubic)")
    lines.append("  - Architecture dependence is large (not bounded by factor 10)")
    lines.append("  - Fermi LAT bound: E_QG > 10^{10.8} GeV for k^4 corrections")
    lines.append("")

    lines.append("EXPERIMENTAL INTERFACE")
    lines.append("  - Fermi LAT, CTA, and future gamma-ray timing missions")
    lines.append("  - Framework does not yet give a clean E_Planck prediction")
    lines.append("  - The lattice spacing h maps to the effective Planck length")
    lines.append("")

    lines.append("WHAT COUNTS AS A HIT")
    lines.append("  - Energy-dependent photon speeds detected at a level consistent")
    lines.append("    with the framework's c4 scaling")
    lines.append("  - The sign of the dispersion correction matches the framework")
    lines.append("")

    lines.append("WHAT COUNTS AS A MISS")
    lines.append("  - Fermi LAT / CTA sees no Lorentz violation above threshold")
    lines.append("  - The scaling exponent does not converge with lattice refinement")
    lines.append("")

    lines.append("HONEST LIMITATIONS")
    lines.append("  - Scaling exponent is architecture-dependent and not yet converged")
    lines.append("  - No clean prediction for the absolute energy scale")
    lines.append("  - This is a theory-level prediction, not yet a lab protocol")
    lines.append("")

    return "\n".join(lines)


# ============================================================================
# Candidate 3: Emergent GR Signatures (Factor-of-2 Light Bending)
# ============================================================================


def format_candidate_3() -> str:
    """Format the emergent GR signatures as Candidate 3."""
    lines: list[str] = []
    lines.append("=" * 100)
    lines.append("CANDIDATE 3: EMERGENT GR SIGNATURES (TIME DILATION + LIGHT BENDING)")
    lines.append("=" * 100)
    lines.append("")

    lines.append("OBSERVABLE")
    lines.append("  The path-sum propagator with action S = L(1-f) produces GR to leading order:")
    lines.append("    1. Gravitational time dilation: clock rate ~ (1-f), matching Schwarzschild g_00")
    lines.append("    2. Weak equivalence principle: deflection independent of wavenumber k")
    lines.append("    3. Conformal spatial metric: g_ij = (1-f)^2 * delta_ij")
    lines.append("    4. Factor-of-2 light bending: 4GM/bc^2 vs Newtonian 2GM/bc^2")
    lines.append("")

    lines.append("STANDARD NULL")
    lines.append("  These should match GR in the weak-field limit.")
    lines.append("  Any deviation from the Schwarzschild metric at leading order is a miss.")
    lines.append("")

    lines.append("FRAMEWORK PREDICTION")
    lines.append("  The action S = L(1-f) with Poisson-sourced f gives:")
    lines.append("    - g_00 = (1-f)^2 to leading order  [matches Schwarzschild]")
    lines.append("    - g_ij = (1-f)^2 * delta_ij        [isotropic conformal metric]")
    lines.append("    - WEP violation: NONE (all k deflect identically)")
    lines.append("    - Light bending: the factor-of-2 from combined time+space curvature")
    lines.append("")

    lines.append("  Numerical verification (from frontier_emergent_gr_signatures.py):")
    lines.append("    - Time dilation ratio matches (1-f) to 6+ digits")
    lines.append("    - WEP holds: deflection angles agree across k values to < 0.01%")
    lines.append("    - Spatial metric prefactor: (1-f)^2 confirmed numerically")
    lines.append("    - Light bending factor: 2.00 +/- numerical precision")
    lines.append("")

    lines.append("EXPERIMENTAL INTERFACE")
    lines.append("  - Precision tests of the equivalence principle (MICROSCOPE satellite)")
    lines.append("  - Gravitational lensing observations (Eddington-style)")
    lines.append("  - Gravitational redshift measurements (Pound-Rebka, clock comparisons)")
    lines.append("")

    lines.append("WHAT COUNTS AS A HIT")
    lines.append("  - Framework reproduces all weak-field GR predictions (consistency check)")
    lines.append("  - Any DEVIATION from GR at strong-field or high-order would be the real test")
    lines.append("")

    lines.append("WHAT COUNTS AS A MISS")
    lines.append("  - Framework fails to reproduce the factor-of-2 in light bending")
    lines.append("  - WEP violation detected in the propagator")
    lines.append("")

    lines.append("HONEST LIMITATIONS")
    lines.append("  - Matching GR at leading order is a consistency check, not a new prediction")
    lines.append("  - The real discriminator would be a post-Newtonian correction that differs from GR")
    lines.append("  - Strong-field deviations have not yet been quantified")
    lines.append("")

    return "\n".join(lines)


# ============================================================================
# Candidate 4: Interferometric / Waveguide Phase-Ramp Analog
# ============================================================================


def format_candidate_4() -> str:
    """Format the interferometric analog as Candidate 4."""
    lines: list[str] = []
    lines.append("=" * 100)
    lines.append("CANDIDATE 4: INTERFEROMETRIC / WAVEGUIDE PHASE-RAMP ANALOG")
    lines.append("=" * 100)
    lines.append("")

    lines.append("OBSERVABLE")
    lines.append("  Lock-in quadrature, phase lag, or spatial phase ramp")
    lines.append("  in a driven wave / interferometric platform")
    lines.append("")

    lines.append("STANDARD NULL")
    lines.append("  Instantaneous or quasi-static control gives flat phase after calibration")
    lines.append("")

    lines.append("FRAMEWORK PREDICTION")
    lines.append("  The exact-lattice wavefield escalation produces a coherent")
    lines.append("  detector-line phase ramp with R^2 ~ 0.96.")
    lines.append("  This is the same physics as Candidate 1 but in an optical/acoustic platform.")
    lines.append("")

    lines.append("  Key retained observables:")
    lines.append("    - Detector-line phase ramp: coherent with R^2 ~ 0.96")
    lines.append("    - Wave/same-site response ratio: large separation between lanes")
    lines.append("    - Weak-field sign: TOWARD (attractive)")
    lines.append("    - F~M (force proportional to mass): stays near 1.00")
    lines.append("")

    lines.append("EXPERIMENTAL INTERFACE")
    lines.append("  - Optical interferometer with driven mirror/source")
    lines.append("  - Acoustic waveguide with driven transducer")
    lines.append("  - Lock-in amplifier readout of phase across detector array")
    lines.append("  - Same control stack as Candidate 1 (drive off, pi flip, etc.)")
    lines.append("")

    lines.append("WHY IT RANKS BELOW CANDIDATE 1")
    lines.append("  - Less direct: maps framework onto a wave analog, not gravity itself")
    lines.append("  - The NV platform already has the required hardware and sensitivity")
    lines.append("  - An analog confirmation is valuable but less decisive")
    lines.append("")

    lines.append("WHAT COUNTS AS A HIT")
    lines.append("  - Coherent phase ramp in the expected causal direction")
    lines.append("  - Phase ramp slope matches the framework scaling with frequency/separation")
    lines.append("")

    lines.append("WHAT COUNTS AS A MISS")
    lines.append("  - Phase is flat after calibration")
    lines.append("  - The analog reproduces only the null")
    lines.append("")

    return "\n".join(lines)


# ============================================================================
# Candidate 5: Electrostatics Scalar Sign-Law
# ============================================================================


def format_candidate_5() -> str:
    """Format the electrostatics sign-law as Candidate 5."""
    lines: list[str] = []
    lines.append("=" * 100)
    lines.append("CANDIDATE 5: ELECTROSTATICS SCALAR SIGN-LAW CARD")
    lines.append("=" * 100)
    lines.append("")

    lines.append("OBSERVABLE")
    lines.append("  Five scalar observables from the path-sum with signed source coupling:")
    lines.append("    1. Sign antisymmetry ratio: -1.000")
    lines.append("    2. Exact null (opposite charges at same node): PASS")
    lines.append("    3. Dipole orientation flip ratio: -0.999")
    lines.append("    4. Charge scaling exponent: |delta| ~ q^1.000")
    lines.append("    5. Screening ratio: 0.018")
    lines.append("")

    lines.append("STANDARD NULL")
    lines.append("  Opposite-sign superposition at the same node must cancel to machine precision.")
    lines.append("  A separated +/- pair must be a dipole, not a null.")
    lines.append("")

    lines.append("FRAMEWORK PREDICTION")
    lines.append("  The path-sum with signed coupling produces all five observables.")
    lines.append("  This is a clean scalar sign law on a retained family.")
    lines.append("")

    lines.append("EXPERIMENTAL INTERFACE")
    lines.append("  - Theory-only for now (lattice prediction)")
    lines.append("  - Bridge to a real electrostatic measurement needs the")
    lines.append("    scalar sign law mapped onto a physical charge system")
    lines.append("")

    lines.append("WHY IT RANKS HERE")
    lines.append("  - Five independent observables from one framework is strong")
    lines.append("  - But it is theory-only: no lab protocol yet")
    lines.append("  - The electrostatic measurements are already explained by Maxwell")
    lines.append("")

    return "\n".join(lines)


# ============================================================================
# Summary and ranking
# ============================================================================


def format_summary() -> str:
    """Format the overall summary and ranking."""
    lines: list[str] = []
    lines.append("=" * 100)
    lines.append("EXPERIMENTAL PREDICTIONS SUMMARY")
    lines.append("  Two-Axiom Framework: Ranked Testable Candidates")
    lines.append("=" * 100)
    lines.append("")

    lines.append("RANKING CRITERIA")
    lines.append("  1. Is it a null test? (standard physics predicts zero, framework predicts nonzero)")
    lines.append("  2. Is existing hardware sufficient?")
    lines.append("  3. Is the prediction a pattern (not just a number)?")
    lines.append("  4. Does the signal get stronger with accessible experimental knobs?")
    lines.append("  5. How many independent controls validate it?")
    lines.append("")

    lines.append("RANKED CANDIDATES")
    lines.append("")
    lines.append(f"  {'Rank':>4s}  {'Candidate':>50s}  {'Platform':>20s}  {'Null test?':>10s}")
    lines.append(f"  {'---':>4s}  {'---':>50s}  {'---':>20s}  {'---':>10s}")
    candidates = [
        ("1", "Diamond NV lock-in quadrature", "tabletop", "YES"),
        ("2", "Modified dispersion relation (k^4)", "satellite", "YES"),
        ("3", "Emergent GR signatures", "precision tests", "NO *"),
        ("4", "Interferometric phase-ramp analog", "tabletop", "YES"),
        ("5", "Electrostatics scalar sign-law", "theory-only", "N/A"),
    ]
    for rank, name, plat, null in candidates:
        lines.append(f"  {rank:>4s}  {name:>50s}  {plat:>20s}  {null:>10s}")
    lines.append("")
    lines.append("  * Candidate 3 matches GR (consistency check); the discriminator")
    lines.append("    would be a post-Newtonian deviation, not yet computed.")
    lines.append("")

    lines.append("RECOMMENDED FIRST EXPERIMENT")
    lines.append("  Candidate 1: Diamond NV lock-in quadrature protocol")
    lines.append("  This is the single strongest path to an external test because:")
    lines.append("    - It is a clean null test against standard physics")
    lines.append("    - The phase ramp is a spatial pattern, not just a number")
    lines.append("    - Diamond NV labs already have the required hardware")
    lines.append("    - The prediction gets stronger at higher f and larger r")
    lines.append("    - Four independent controls distinguish signal from artifact")
    lines.append("")

    lines.append("WHAT THE FRAMEWORK SAYS TO A LAB")
    lines.append('  "Measure the lock-in quadrature and spatial phase ramp for a driven')
    lines.append('   source near an NV sensor. The standard quasi-static baseline predicts')
    lines.append('   no stable quadrature after calibration; the retained retarded/wavefield')
    lines.append('   lane predicts a nonzero phase-lag signature that strengthens with')
    lines.append('   drive frequency and source-detector separation."')
    lines.append("")

    return "\n".join(lines)


# ============================================================================
# Main
# ============================================================================


def main() -> int:
    print(format_summary())
    print()
    print(format_candidate_1())
    print()
    print(format_candidate_2())
    print()
    print(format_candidate_3())
    print()
    print(format_candidate_4())
    print()
    print(format_candidate_5())

    # Final verdict
    print()
    print("=" * 100)
    print("FINAL VERDICT")
    print("=" * 100)
    print()
    print("  The diamond NV lock-in quadrature protocol (Candidate 1) is the single")
    print("  best path from this framework to an external experimental test.")
    print()
    print("  It is bounded, testable, and requires no new hardware -- only a")
    print("  collaboration with an existing diamond NV magnetometry lab.")
    print()
    print("  The remaining candidates provide theory-level consistency checks")
    print("  (GR recovery, dispersion relation) or analog platforms that could")
    print("  validate the phase-ramp prediction in a different medium.")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
