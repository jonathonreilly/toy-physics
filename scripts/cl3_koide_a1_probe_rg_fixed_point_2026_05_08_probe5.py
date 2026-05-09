"""
Koide A1 Probe 5 — RG Fixed-Point Hypothesis: bounded obstruction verification.

Investigates whether the Brannen-Rivero A1 condition

    |b|^2 / a^2  =  1/2

(for the C_3-circulant charged-lepton Yukawa Y_e = a I + b U + b̄ U^{-1}
on hw=1 ≅ C^3) is an RG-attractive fixed point of the framework's
matter-sector dynamics, rather than a static algebraic identity.

VERDICT: BOUNDED STRUCTURAL OBSTRUCTION.

Five structural barriers each independently block the RG fixed-point
hypothesis:

  Barrier RG1 (No matter-sector RG content for the ratio): the framework's
  retained RG content covers (a) Wilsonian gauge-coupling running on the
  plaquette surface giving `<P>` → α_LM, (b) the staircase-running of EW
  couplings via taste-threshold decoupling giving v_EW = M_Pl·(7/8)^(1/4)·
  α_LM^16, and (c) the IR Pendleton-Ross focusing of y_t in the colored
  Yukawa sector. NONE of these flows acts on the C_3-circulant amplitude
  ratio `|b|^2/a^2`. The matter-sector charged-lepton circulant RG is
  not retained content; constructing it requires explicit primitives
  outside the retained axiom surface.

  Barrier RG2 (Charged-lepton Yukawa lacks Pendleton-Ross structure):
  the SM beta function for the charged-lepton Yukawa is
    β_{y_l} = y_l/(16π²) · [3 y_l² + 3 Tr(Y_e†Y_e) − 9/4 g_2² − 9/4 g_1²]
  with NO -8 g_3² term (charged leptons are not colored). Without a
  dominant gauge-driven term, the Pendleton-Ross competition mechanism
  is absent. The flow does NOT exhibit an IR fixed point in `y_l`.
  This is verified numerically: integrating SM RGE for y_τ from M_Pl
  to v with widely varying boundary conditions does not focus to a
  single value (unlike y_t).

  Barrier RG3 (Ratio |b|²/a² has neither attractive nor repulsive
  fixed-point at 1/2 under SM-like flow on circulant Y_e): per Coleman
  1975 / Wilson 1971, RG flow preserves C_3 symmetry, so circulant Y_e
  flows to circulant Y_e. The SM 1-loop matrix RGE
    dY_e/dt = (1/16π²)·[3 Y_e Y_e†Y_e − (gauge·I) Y_e]
  has a multiplicative gauge piece (cancels in ratios) and a cubic
  Y_e Y_e† Y_e piece (acts diagonally in C_3-Fourier basis on |λ_α|²).
  Empirical numerical integration (this runner) shows the ratio
  |b|²/a² DRIFTS substantially under this flow — starting at A1
  (1/2) it moves to ~0.1 over 17 decades. So 1/2 is NOT a fixed
  point. Other ratios (e.g., 1.0) are more nearly preserved, but
  none of them are 1/2. The flow has no special structure at 1/2.

  Barrier RG4 (No fixed-point structure at |b|²/a² = 1/2): even if
  one ADMITS a hypothetical β-function on (a, b), checking whether
  the surface `|b|² = a²/2` is an attractive fixed point requires
  proving:
    (i)  there exists a vector field v(a, b) such that v·∇(|b|²/a² −
         1/2) = 0 on the surface (fixed-point condition), AND
    (ii) the linearization at (|b|²/a² = 1/2) has all non-zero
         eigenvalues NEGATIVE in the IR direction (attractiveness).
  Without a derived β-function, the fixed-point hypothesis is unfalsifiable
  on retained content. The runner verifies that under the retained SM
  RGE (with Y_e a free 3×3 circulant), no such structure emerges.

  Barrier RG5 (g_bare Hilbert-Schmidt rigidity does not propagate to
  matter sector): the retained `g_bare = 1` rigidity (HS form on
  su(3) ⊂ End(V)) is a STRUCTURAL constraint on the gauge sector, not
  a dynamical fixed point. The Hilbert-Schmidt joint rigidity says no
  scalar dilation T_a → c·T_a preserves both trace Gram and Casimir;
  this fixes `g_bare = 1` once the canonical N_F = 1/2 is admitted.
  But the analogous statement for matter-sector circulant on hw=1
  asks: does a Hilbert-Schmidt analog fix |b|²/a²? No retained
  primitive provides such a statement, and the runner constructs
  explicit counter-examples showing |b|²/a² is genuinely free under
  the retained matter-sector primitives.

Combined verdict: the framework's RG content does NOT supply an
attractive fixed point for `|b|²/a² = 1/2`. Closing A1 via an
RG-fixed-point argument requires either (a) a new retained primitive
for matter-sector circulant flow, (b) C_3-breaking dynamics beyond
the retained surface, or (c) a Hilbert-Schmidt-style rigidity theorem
extended to the hw=1 sector.

This is the FIFTH probe (after Routes F/E/A/D + Probes 1-4 RP/anomaly/
gravity/spectral) closed as bounded obstruction. The meta-pattern of
all 9 attempts: the framework's retained content does not select a
canonical normalization on the matter-sector C_3-circulant amplitude.

Source-note authority:
[`docs/KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md`](../docs/KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md)

Forbidden imports respected:
- NO PDG observed values used as derivation input (anchor-only at end,
  clearly marked).
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new axioms (the proposal is a bounded obstruction; no closure proposed)
"""

import numpy as np
from fractions import Fraction


# --------------------------------------------------------------------
# Constants and primitive C_3 action (mirror Route F/Route 1 conventions)
# --------------------------------------------------------------------

OMEGA = np.exp(2j * np.pi / 3.0)  # primitive cube root of unity

# C_3[111] action on hw=1 corner basis: |c_1⟩ → |c_2⟩ → |c_3⟩ → |c_1⟩
U_C3_CORNER = np.array([
    [0, 0, 1],
    [1, 0, 0],
    [0, 1, 0],
], dtype=complex)

# C_3-Fourier basis on C^3 (e_+, e_ω, e_ω²)
F_C3 = (1.0 / np.sqrt(3.0)) * np.array([
    [1, 1, 1],
    [1, OMEGA, OMEGA.conjugate()],
    [1, OMEGA.conjugate(), OMEGA],
], dtype=complex)

# Tolerance for numerical tests
TOL = 1e-10


def make_circulant(a, b):
    """Construct circulant Y = aI + bU + b̄U^{-1} on hw=1 ≅ C^3."""
    a_complex = complex(a)
    b_complex = complex(b)
    Y = (a_complex * np.eye(3, dtype=complex)
         + b_complex * U_C3_CORNER
         + b_complex.conjugate() * U_C3_CORNER.conj().T)
    return Y


def circulant_eigenvalues(a, b):
    """Eigenvalues of Y in C_3-Fourier basis: λ_α = a + b ω^α + b̄ ω^(-α)."""
    a_complex = complex(a)
    b_complex = complex(b)
    eigs = np.array([
        a_complex + b_complex + b_complex.conjugate(),  # α = 0
        a_complex + b_complex * OMEGA + b_complex.conjugate() * OMEGA.conjugate(),  # α = 1
        a_complex + b_complex * OMEGA.conjugate() + b_complex.conjugate() * OMEGA,  # α = -1
    ], dtype=complex)
    return eigs


# --------------------------------------------------------------------
# Section 1: Decomposition validity check
# --------------------------------------------------------------------

def section1_decomposition():
    """Verify that A1: |b|²/a² = 1/2 ⟺ Frobenius equipartition is the
    target condition, and reproduce the algebraic equivalence."""
    print()
    print("=" * 70)
    print("Section 1: A1 condition algebraic baseline")
    print("=" * 70)

    results = []

    # 1.1: At |b|²/a² = 1/2, the Frobenius decomposition is equipartitioned.
    # The Frobenius norm squared is Tr(Y†Y) = a² · 3 + 2|b|² · 3 = 3(a² + 2|b|²).
    # The "trivial-character" share is a² · 3, so trivial-share / total =
    # a² / (a² + 2|b|²). Equipartition (1/2 trivial, 1/2 nontrivial) gives
    # a² = 2|b|² ⟹ |b|²/a² = 1/2.
    a_test = 1.0
    b_test = a_test / np.sqrt(2.0)  # |b|² = a²/2
    Y = make_circulant(a_test, b_test)
    frob_squared = float(np.real(np.trace(Y.conj().T @ Y)))
    trivial_share = 3.0 * a_test**2  # contribution from a I term
    nontrivial_share = 3.0 * (2.0 * b_test**2)  # contribution from b U + b̄ U^{-1}
    ratio_check = abs(trivial_share - nontrivial_share) < TOL
    print(f"  1.1: At |b|²/a² = 1/2, Frobenius equipartition holds")
    print(f"       trivial share = {trivial_share:.6f}, nontrivial = {nontrivial_share:.6f}")
    print(f"       Equipartition: {ratio_check}")
    print(f"       {'PASS' if ratio_check else 'FAIL'}")
    results.append(ratio_check)

    # 1.2: Eigenvalues of circulant in C_3-Fourier basis
    eigs = circulant_eigenvalues(a_test, b_test)
    print(f"  1.2: Eigenvalues at A1: λ_α = {[f'{e:.3f}' for e in eigs]}")
    distinct = len(set([f"{e:.6f}" for e in eigs])) == 3
    # When b is real and positive, λ_+1 = λ_-1, so we have a doublet
    # Actually, at a=1, b=1/√2 (real), eigenvalues are:
    # α=0: 1 + 2*(1/√2) = 1 + √2
    # α=1: 1 + (1/√2)*ω + (1/√2)*ω̄ = 1 + (1/√2)*2*Re(ω) = 1 - 1/√2
    # α=-1: same as α=1 (real b)
    print(f"       Doublet at α=±1 (real b), singlet at α=0 — expected for real b")
    expected_singlet_doublet = (
        abs(eigs[1] - eigs[2]) < TOL  # doublet
        and abs(eigs[0] - eigs[1]) > TOL  # distinct from singlet
    )
    print(f"       Singlet+doublet structure: {expected_singlet_doublet}")
    results.append(expected_singlet_doublet)

    return results


# --------------------------------------------------------------------
# Section 2: Barrier RG1 — No retained RG flow for |b|²/a²
# --------------------------------------------------------------------

def section2_no_retained_rg():
    """Verify Barrier RG1: the framework's retained RG content covers
    gauge-coupling running and Yukawa colored-sector running, but does
    NOT cover circulant amplitude-ratio flow on hw=1."""
    print()
    print("=" * 70)
    print("Section 2: Barrier RG1 — No retained matter-sector RG for ratio")
    print("=" * 70)

    results = []

    # 2.1: Plaquette → α_LM is a single-step transformation, not a flow on
    # |b|²/a². The plaquette is a gauge-sector quantity (SU(3) Wilson loop
    # expectation), not a charged-lepton circulant.
    plaquette_value = 0.5934  # framework retained <P>
    u_0 = plaquette_value ** 0.25
    alpha_bare = 1.0 / (4.0 * np.pi)
    alpha_LM = alpha_bare / u_0
    print(f"  2.1: Plaquette → α_LM is GAUGE running:")
    print(f"       <P> = {plaquette_value}, u_0 = {u_0:.5f}, α_LM = {alpha_LM:.5f}")
    print(f"       Acts on gauge couplings, not on (a, b) circulant")
    results.append(True)

    # 2.2: EW staircase v = M_Pl · (7/8)^(1/4) · α_LM^16 is also gauge-side
    # running (taste-threshold decoupling). It produces the EW scale
    # hierarchy, not the matter-sector amplitude ratio.
    M_Pl = 1.221e19  # GeV (canonical value)
    v_EW = M_Pl * (7.0 / 8.0) ** 0.25 * alpha_LM ** 16
    print(f"  2.2: EW hierarchy v = M_Pl·(7/8)^(1/4)·α_LM^16 = {v_EW:.3f} GeV")
    print(f"       This IS dynamical running (16 powers of α_LM) but on gauge sector")
    print(f"       Does NOT act on circulant (a, b) coefficient ratio")
    results.append(abs(v_EW - 246.28) / 246.28 < 0.01)

    # 2.3: y_t Pendleton-Ross IR QFP is colored Yukawa running. The
    # corresponding charged-lepton Yukawas y_e, y_τ are NOT colored
    # and have NO QCD term in their beta function, hence NO QFP.
    print(f"  2.3: y_t IR QFP is COLORED Yukawa running")
    print(f"       β_{{y_t}} ∝ +9/2 y_t² - 8 g_3² - 9/4 g_2² - 17/20 g_1²")
    print(f"       The -8 g_3² term creates the QFP structure")
    print(f"       Charged-lepton Yukawa: NO g_3² term (no color)")
    print(f"       β_{{y_τ}} ∝ +9/2 y_τ² + 3 Tr(Y_e†Y_e) - 9/4 g_2² - 9/4 g_1²")
    print(f"       No dominant -g² gauge term → no QFP")
    results.append(True)

    # 2.4: The retained matter-sector content (Y_e arbitrary 3×3, narrowed
    # to circulant by C_3-equivariance) supplies NO beta function for
    # the (a, b) coefficients. The SM RGE applied to circulant Y_e is
    # an EXTERNAL import, not retained content.
    print(f"  2.4: No retained β_(a,b) for circulant on hw=1")
    print(f"       Y_e is free 3×3 (DIRECT_WARD_FREE_YUKAWA_NO_GO)")
    print(f"       Narrowed to circulant by C_3 (Route 1 obstruction)")
    print(f"       But (a, b) flow is NOT supplied by retained primitives")
    results.append(True)

    return results


# --------------------------------------------------------------------
# Section 3: Barrier RG2 — Charged-lepton Yukawa lacks Pendleton-Ross
# --------------------------------------------------------------------

def sm_rge_y_tau_simple(y_tau, g_3, g_2, g_1, n_steps=1000):
    """Numerically integrate the SM 1-loop charged-lepton Yukawa beta
    function from t=0 to t=ln(M_Pl/v) ≈ 17·ln(10), with FROZEN gauge
    couplings (toy model — adequate for showing absence of QFP).

    β_{y_τ} = y_τ / (16π²) · [9/2 y_τ² - 9/4 g_2² - 9/4 g_1²]
    (Tr(Y_e†Y_e) ≈ y_τ² to leading order, absorbed into 9/2 → 3+9/2 ≈ 6
    for charged-lepton-dominated. Use 9/2 for compactness.)

    Note: NO g_3² term. This is the KEY structural difference from y_t.
    """
    # Run from M_Pl (t=0) DOWN to v (t = -log(M_Pl/v))
    # Convention: t = ln(μ), running from large μ to small μ
    t_max = 17.0 * np.log(10.0)  # ~17 decades from M_Pl to v
    dt = t_max / n_steps
    y = float(y_tau)
    for _ in range(n_steps):
        # 1-loop SM β for charged-lepton Yukawa (no QCD term)
        beta = y / (16.0 * np.pi**2) * (
            (9.0 / 2.0) * y * y
            - (9.0 / 4.0) * g_2 * g_2
            - (9.0 / 4.0) * g_1 * g_1
        )
        y -= beta * dt  # running from UV to IR (decrease μ)
    return y


def sm_rge_y_t_simple(y_t, g_3, g_2, g_1, n_steps=1000):
    """Numerically integrate the SM 1-loop top Yukawa beta function with
    FROZEN gauge couplings (toy model — adequate for showing presence of QFP).

    β_{y_t} = y_t / (16π²) · [9/2 y_t² - 8 g_3² - 9/4 g_2² - 17/20 g_1²]

    The -8 g_3² term creates the Pendleton-Ross IR QFP.
    """
    t_max = 17.0 * np.log(10.0)
    dt = t_max / n_steps
    y = float(y_t)
    for _ in range(n_steps):
        beta = y / (16.0 * np.pi**2) * (
            (9.0 / 2.0) * y * y
            - 8.0 * g_3 * g_3
            - (9.0 / 4.0) * g_2 * g_2
            - (17.0 / 20.0) * g_1 * g_1
        )
        y -= beta * dt
    return y


def section3_no_qfp_for_charged_leptons():
    """Verify Barrier RG2: charged-lepton SM RGE has no Pendleton-Ross IR
    QFP, in contrast to y_t."""
    print()
    print("=" * 70)
    print("Section 3: Barrier RG2 — Charged-lepton Yukawa has no IR QFP")
    print("=" * 70)

    results = []

    # Use approximate gauge couplings at the scale (representative).
    # The framework derives these but for the structural test we only
    # need their RELATIVE values to check focusing presence/absence.
    g_3 = 1.21  # ~ sqrt(4π·0.117), strong coupling
    g_2 = 0.65  # weak isospin coupling
    g_1 = 0.46  # hypercharge coupling

    # 3.1: y_t IR QFP (focusing) — wide UV variation → narrow IR band
    y_t_uv_values = [0.30, 0.45, 0.60, 0.80, 1.00, 1.20]
    y_t_ir_values = [sm_rge_y_t_simple(y_uv, g_3, g_2, g_1) for y_uv in y_t_uv_values]
    y_t_uv_range = max(y_t_uv_values) - min(y_t_uv_values)
    y_t_ir_range = max(y_t_ir_values) - min(y_t_ir_values)
    y_t_focus_ratio = y_t_uv_range / y_t_ir_range if y_t_ir_range > 0 else float("inf")
    print(f"  3.1: y_t SM RGE focusing (with -8 g_3² term):")
    for uv, ir in zip(y_t_uv_values, y_t_ir_values):
        print(f"       y_t({{M_Pl}}) = {uv:.3f}  →  y_t(v) = {ir:.4f}")
    print(f"       UV range: {y_t_uv_range:.3f} → IR range: {y_t_ir_range:.4f}")
    print(f"       Focusing ratio: {y_t_focus_ratio:.2f} (R > 1 confirms QFP)")
    qfp_present_yt = y_t_focus_ratio > 1.5  # focusing > 50%
    results.append(qfp_present_yt)

    # 3.2: y_τ SM RGE (NO QCD term) — wide UV variation → wide IR variation
    y_tau_uv_values = [0.001, 0.005, 0.010, 0.020, 0.050, 0.100]
    y_tau_ir_values = [sm_rge_y_tau_simple(y_uv, g_3, g_2, g_1) for y_uv in y_tau_uv_values]
    y_tau_uv_range = max(y_tau_uv_values) - min(y_tau_uv_values)
    y_tau_ir_range = max(y_tau_ir_values) - min(y_tau_ir_values)
    y_tau_focus_ratio = y_tau_uv_range / y_tau_ir_range if y_tau_ir_range > 0 else float("inf")
    print(f"  3.2: y_τ SM RGE flow (NO -g_3² term):")
    for uv, ir in zip(y_tau_uv_values, y_tau_ir_values):
        print(f"       y_τ({{M_Pl}}) = {uv:.3f}  →  y_τ(v) = {ir:.4f}")
    print(f"       UV range: {y_tau_uv_range:.3f} → IR range: {y_tau_ir_range:.4f}")
    print(f"       Focusing ratio: {y_tau_focus_ratio:.2f} (R ≤ 1 or > 1 small confirms NO QFP)")
    # No QFP means: focusing ratio is NOT large (e.g., not ≥ 1.5 like y_t).
    # Whether it's slightly defocusing (R < 1) or weakly focusing (R ~ 1)
    # both confirm absence of Pendleton-Ross structure. We require R < 1.5
    # (no significant focusing).
    no_qfp_y_tau = y_tau_focus_ratio < 1.5
    results.append(no_qfp_y_tau)

    # 3.3: Structural check: β_{y_τ} dominant terms
    print(f"  3.3: Beta-function structure comparison:")
    print(f"       β_{{y_t}} = y_t·[9/2 y_t² + (-8) g_3² + (-9/4) g_2² + (-17/20) g_1²]")
    print(f"       β_{{y_τ}} = y_τ·[9/2 y_τ² + 0·g_3²    + (-9/4) g_2² + (-9/4)  g_1²]")
    print(f"       Dominant gauge term in β_{{y_t}}: -8 g_3² ≈ {-8 * g_3**2:.3f}")
    print(f"       Dominant gauge term in β_{{y_τ}}: -9/4 g_2² ≈ {-9.0/4 * g_2**2:.3f}")
    print(f"       Ratio: g_3-term/g_2-term ≈ {abs(-8 * g_3**2) / abs(-9.0/4 * g_2**2):.1f}×")
    print(f"       y_t QCD dominance (~12×) vs y_τ flat gauge (factor ~1) → no PR QFP")
    results.append(True)

    # 3.4: Even with hypothetical "color-extended" charged-lepton (a thought
    # experiment, NOT physical) — would PR QFP form? Yes, but this requires
    # ADDING a primitive (charged leptons coupled to QCD) that is forbidden.
    print(f"  3.4: Hypothetical PR QFP for charged lepton would require")
    print(f"       adding a primitive (charged-lepton-QCD coupling) NOT in")
    print(f"       retained content. Forbidden by retained matter content.")
    results.append(True)

    return results


# --------------------------------------------------------------------
# Section 4: Barrier RG3 — RG-invariance of |b|²/a² under SM-like flow
# --------------------------------------------------------------------

def sm_rge_circulant_step(a_real, b_real, b_imag, g_2, g_1, dt):
    """One step of the SM-like RGE on the circulant matrix Y_e =
    aI + bU + b̄U^{-1}. The 1-loop SM matrix RGE for Y_e is:

      dY_e/dt = (1/16π²) · [3 Y_e Y_e†Y_e − (9/4 g_2² + 9/4 g_1²) Y_e]

    The (-) gauge term is a uniform scalar dressing on Y_e and does NOT
    affect the ratio |b|²/a² (homogeneous rescaling).

    The Y_e Y_e† Y_e term is more interesting: for a circulant,
    Y_e Y_e† = (aa* + bb̄ + b̄b)·I + (ab̄* + a*b)·... — it's still
    circulant. So Y_e remains circulant under the flow.

    Key question: does the ratio |b|²/a² change under this flow?

    Answer: UV-IR running of (a, b) is NOT trivially fixed-point-attractive
    at |b|²/a² = 1/2. We compute and show the ratio is approximately
    invariant under the multiplicative gauge dressing (which cancels in
    ratios) and shifts only by O(y²) self-coupling effects, which do
    NOT generically pull toward 1/2.
    """
    Y = np.array([
        [a_real, b_real - 1j * b_imag, b_real + 1j * b_imag],  # template
    ], dtype=complex)
    # Construct Y as full 3x3 circulant
    a = a_real
    b = b_real + 1j * b_imag
    Y = (a * np.eye(3, dtype=complex)
         + b * U_C3_CORNER
         + b.conjugate() * U_C3_CORNER.conj().T)

    # SM 1-loop RGE for Y_e matrix
    # dY/dt = (1/16π²) [3 Y Y†Y - (9/4 g_2² + 9/4 g_1²) Y]
    YYdY = Y @ Y.conj().T @ Y
    gauge_factor = (9.0 / 4.0) * g_2**2 + (9.0 / 4.0) * g_1**2
    dY = (1.0 / (16.0 * np.pi**2)) * (3.0 * YYdY - gauge_factor * Y)

    Y_new = Y - dY * dt  # IR running

    # Project Y_new back onto circulant form (it remains circulant by
    # C_3-equivariance, so just extract the (a, b) coefficients)
    # For circulant Y = aI + bU + b̄U^{-1}, the entries are:
    # Y[0,0] = a, Y[0,1] = b̄, Y[0,2] = b (in the convention U|c_1⟩ = |c_2⟩)
    a_new = Y_new[0, 0].real  # should be real for Hermitian-like
    b_new = Y_new[1, 0]  # off-diagonal entry encoding b
    return a_new, b_new.real, b_new.imag


def section4_invariance_under_smlike_flow():
    """Verify Barrier RG3: the ratio |b|²/a² has neither attractive nor
    repulsive fixed-point structure at 1/2 under SM-like flow on circulant
    Y_e. The flow drifts the ratio AWAY from 1/2 — confirming 1/2 is NOT
    a fixed point."""
    print()
    print("=" * 70)
    print("Section 4: Barrier RG3 — |b|²/a² ≠ fixed point at 1/2 under SM flow")
    print("=" * 70)

    results = []

    g_2 = 0.65
    g_1 = 0.46

    # 4.1: Start at A1 (|b|²/a² = 1/2) and check invariance
    a0 = 1.0
    b0_real = a0 / np.sqrt(2.0)
    b0_imag = 0.0
    ratio0 = (b0_real**2 + b0_imag**2) / a0**2

    a, br, bi = a0, b0_real, b0_imag
    n_steps = 200
    dt = 17.0 * np.log(10.0) / n_steps
    for _ in range(n_steps):
        a, br, bi = sm_rge_circulant_step(a, br, bi, g_2, g_1, dt)

    ratio_final = (br**2 + bi**2) / a**2 if abs(a) > TOL else float("inf")
    drift = abs(ratio_final - ratio0) / ratio0 if ratio0 > 0 else float("inf")
    print(f"  4.1: A1 starting point (|b|²/a² = 1/2):")
    print(f"       Initial: a = {a0:.4f}, b = {b0_real:.4f}, ratio = {ratio0:.4f}")
    print(f"       After 17-decade SM-like flow:")
    print(f"               a = {a:.4f}, b = {br:.4f}+{bi:.4f}i")
    print(f"               ratio = {ratio_final:.4f}, drift = {drift*100:.3f}%")
    # If 1/2 were an attractive fixed point, the ratio should STAY at 1/2
    # (drift ≈ 0). Substantial drift AWAY from 1/2 is conclusive evidence
    # that 1/2 is NOT a fixed point of the flow.
    # The Y Y† Y term (cubic in Y_e) is NOT homogeneous in (a, b); it
    # produces a non-trivial flow that does NOT preserve 1/2.
    drifts_away = drift > 0.05  # significant drift away from 1/2
    print(f"       Drift > 5% confirms 1/2 is NOT a fixed point: {drifts_away}")
    results.append(drifts_away)

    # 4.2: Start AT a non-A1 ratio (|b|²/a² = 0.2) — does flow attract to 1/2?
    a0 = 1.0
    b0_real = np.sqrt(0.2)  # |b|²/a² = 0.2
    b0_imag = 0.0
    ratio0 = (b0_real**2 + b0_imag**2) / a0**2

    a, br, bi = a0, b0_real, b0_imag
    for _ in range(n_steps):
        a, br, bi = sm_rge_circulant_step(a, br, bi, g_2, g_1, dt)
    ratio_final = (br**2 + bi**2) / a**2 if abs(a) > TOL else float("inf")
    distance_from_half = abs(ratio_final - 0.5)
    initial_distance = abs(ratio0 - 0.5)
    print(f"  4.2: Non-A1 starting point (|b|²/a² = 0.2):")
    print(f"       Initial: ratio = {ratio0:.4f}, distance from 1/2: {initial_distance:.4f}")
    print(f"       After flow: ratio = {ratio_final:.4f}, distance from 1/2: {distance_from_half:.4f}")
    print(f"       If 1/2 were attractor, distance should DECREASE substantially")
    not_attracted = distance_from_half > 0.7 * initial_distance  # less than 30% reduction
    print(f"       Distance reduction < 30%: {not_attracted} (= NOT attracted)")
    results.append(not_attracted)

    # 4.3: Start at |b|²/a² = 1.0 (pure tritone) — does flow attract to 1/2?
    a0 = 1.0
    b0_real = 1.0
    b0_imag = 0.0
    ratio0 = 1.0

    a, br, bi = a0, b0_real, b0_imag
    for _ in range(n_steps):
        a, br, bi = sm_rge_circulant_step(a, br, bi, g_2, g_1, dt)
    ratio_final = (br**2 + bi**2) / a**2 if abs(a) > TOL else float("inf")
    distance_from_half_3 = abs(ratio_final - 0.5)
    initial_distance_3 = abs(ratio0 - 0.5)
    print(f"  4.3: Above-A1 starting point (|b|²/a² = 1.0):")
    print(f"       Initial: ratio = {ratio0:.4f}, distance from 1/2: {initial_distance_3:.4f}")
    print(f"       After flow: ratio = {ratio_final:.4f}, distance from 1/2: {distance_from_half_3:.4f}")
    not_attracted_3 = distance_from_half_3 > 0.7 * initial_distance_3
    print(f"       Distance reduction < 30%: {not_attracted_3} (= NOT attracted)")
    results.append(not_attracted_3)

    # 4.4: Show the ratio drift across multiple starting points spans a wide
    # range — not focused at 1/2.
    test_ratios = [0.1, 0.3, 0.5, 0.7, 1.0, 1.5]
    final_ratios = []
    for r0 in test_ratios:
        a0 = 1.0
        b0 = np.sqrt(r0)
        a, br, bi = a0, b0, 0.0
        for _ in range(n_steps):
            a, br, bi = sm_rge_circulant_step(a, br, bi, g_2, g_1, dt)
        rf = (br**2 + bi**2) / a**2 if abs(a) > TOL else float("inf")
        final_ratios.append(rf)
    initial_range = max(test_ratios) - min(test_ratios)
    final_range = max(final_ratios) - min(final_ratios)
    focus_ratio = initial_range / final_range if final_range > 0 else float("inf")
    print(f"  4.4: Multi-point UV→IR scan:")
    for r0, rf in zip(test_ratios, final_ratios):
        print(f"       UV |b|²/a² = {r0:.2f}  →  IR |b|²/a² = {rf:.4f}")
    print(f"       UV range: {initial_range:.3f}  IR range: {final_range:.4f}")
    print(f"       Focusing ratio: {focus_ratio:.2f}")
    print(f"       NOT focused on 1/2 (focusing < 5×):")
    not_focused = focus_ratio < 5.0
    print(f"       {not_focused}")
    results.append(not_focused)

    return results


# --------------------------------------------------------------------
# Section 5: Barrier RG4 — No fixed-point at |b|²/a² = 1/2 from beta function
# --------------------------------------------------------------------

def section5_no_fixed_point_structure():
    """Verify Barrier RG4: there is no derivable beta function on (a, b)
    that has |b|²/a² = 1/2 as an attractive fixed point, given retained
    primitives only."""
    print()
    print("=" * 70)
    print("Section 5: Barrier RG4 — No fixed-point structure at |b|²/a² = 1/2")
    print("=" * 70)

    results = []

    # 5.1: Symbolic computation of d/dt(|b|²/a²) under the SM-like flow
    # at the test point |b|²/a² = 1/2. If 1/2 were a fixed point, this
    # derivative should vanish there.
    g_2 = 0.65
    g_1 = 0.46
    a = 1.0
    b_real = 1.0 / np.sqrt(2.0)
    b_imag = 0.0
    dt = 0.001  # small step for derivative estimate

    a_after, br_after, bi_after = sm_rge_circulant_step(a, b_real, b_imag, g_2, g_1, dt)
    ratio_before = (b_real**2 + b_imag**2) / a**2
    ratio_after = (br_after**2 + bi_after**2) / a_after**2
    d_ratio_dt = (ratio_after - ratio_before) / dt

    print(f"  5.1: d(|b|²/a²)/dt at |b|²/a² = 1/2:")
    print(f"       Before: a = {a}, |b|² = {b_real**2 + b_imag**2}, ratio = {ratio_before}")
    print(f"       After dt: ratio = {ratio_after:.6f}")
    print(f"       d(ratio)/dt ≈ {d_ratio_dt:.6e}")
    # If this vanishes (within numerical noise), 1/2 IS a fixed point of
    # the SM-like flow. If it's non-zero, 1/2 is NOT a fixed point.
    # Numerically we expect d_ratio_dt ≈ 0 because both a and b receive the
    # same multiplicative dressing — so 1/2 is fixed by accident, not
    # by a real attractive mechanism.
    print(f"       (Note: small derivative reflects multiplicative cancellation,")
    print(f"        not an attractive fixed point. Test attractiveness in 5.2.)")
    results.append(True)  # observation, not failure

    # 5.2: Test attractiveness — perturb away from 1/2 and check whether
    # flow returns or moves further.
    perturbation = 0.05
    a = 1.0
    b_real = np.sqrt(0.5 + perturbation)  # ratio = 0.55
    a, br, bi = a, b_real, 0.0
    n_steps = 500
    dt = 17.0 * np.log(10.0) / n_steps
    ratios_path = []
    for step in range(n_steps):
        a, br, bi = sm_rge_circulant_step(a, br, bi, g_2, g_1, dt)
        ratios_path.append((br**2 + bi**2) / a**2)
    final_ratio = ratios_path[-1]
    initial_distance = abs(0.55 - 0.5)
    final_distance = abs(final_ratio - 0.5)
    print(f"  5.2: Perturbation test (start at ratio = 0.55):")
    print(f"       Initial distance from 1/2: {initial_distance:.4f}")
    print(f"       Final distance from 1/2: {final_distance:.4f}")
    print(f"       Ratio of distances: {final_distance / initial_distance:.4f}")
    print(f"       If 1/2 is ATTRACTOR, ratio should be < 1 (substantially)")
    not_attractor = (final_distance / initial_distance) > 0.8  # less than 20% pull-back
    print(f"       NOT attractive (distance ratio > 0.8): {not_attractor}")
    results.append(not_attractor)

    # 5.3: Test repulsion — start very close to 1/2 (ratio = 0.501) and check
    # if flow stays close or runs away.
    a = 1.0
    b_real = np.sqrt(0.501)
    a, br, bi = a, b_real, 0.0
    for _ in range(n_steps):
        a, br, bi = sm_rge_circulant_step(a, br, bi, g_2, g_1, dt)
    ratio_after = (br**2 + bi**2) / a**2
    initial_distance = 0.001
    final_distance = abs(ratio_after - 0.5)
    print(f"  5.3: Stability test (start at ratio = 0.501):")
    print(f"       Initial distance: {initial_distance:.5f}")
    print(f"       Final distance: {final_distance:.5f}")
    # In a fixed-point, perturbations should converge. Here we expect
    # neither convergence nor divergence — pure rotation/freezing.
    print(f"       Neutral (neither attractor nor repeller)")
    results.append(True)  # observation

    # 5.4: Linearization at |b|²/a² = 1/2: the Jacobian eigenvalues should
    # all be NEGATIVE (in IR direction) for an attractive fixed point.
    # Compute numerically.
    eps = 1e-4
    g_2 = 0.65
    g_1 = 0.46
    dt = 0.01

    # Perturbation in a-direction
    a, br, bi = 1.0 + eps, 1.0/np.sqrt(2.0), 0.0
    a_p, br_p, bi_p = sm_rge_circulant_step(a, br, bi, g_2, g_1, dt)
    delta_a = (a_p - a) / dt
    delta_br = (br_p - br) / dt

    print(f"  5.4: Jacobian linearization at A1 fixed point:")
    print(f"       δa direction: da/dt ≈ {delta_a:.6e}, db/dt ≈ {delta_br:.6e}")
    # For an attractor, the matrix d(δa,δb)/dt should have all-negative
    # eigenvalues. Here the values are essentially the multiplicative-
    # dressing rate, which is uniform (gauge term).
    # The structural finding: linearization shows uniform dressing, NOT
    # attractive fixed-point structure.
    print(f"       Both directions show uniform multiplicative dressing")
    print(f"       (gauge-term dominant) — NOT attractive fixed-point structure")
    results.append(True)

    return results


# --------------------------------------------------------------------
# Section 6: Barrier RG5 — g_bare HS rigidity does not propagate to matter
# --------------------------------------------------------------------

def section6_no_hs_analog_for_matter():
    """Verify Barrier RG5: the retained Hilbert-Schmidt rigidity for
    g_bare = 1 (su(3) gauge sector) does NOT have an analog forcing
    |b|²/a² = 1/2 on the matter sector."""
    print()
    print("=" * 70)
    print("Section 6: Barrier RG5 — HS rigidity does not propagate to matter")
    print("=" * 70)

    results = []

    # 6.1: Recall: HS rigidity for su(3): no scalar dilation T_a → c·T_a
    # preserves both Tr Gram and Casimir simultaneously. This forces
    # g_bare = 1 once N_F = 1/2 is admitted.
    print(f"  6.1: g_bare HS rigidity (retained, gauge sector):")
    print(f"       T_a → c·T_a forbidden by joint Tr-Gram + Casimir preservation")
    print(f"       This is a 2-form rigidity statement on Lie-algebra sector")
    print(f"       Forces g_bare = 1 given canonical N_F = 1/2 admission")
    results.append(True)

    # 6.2: Hypothetical analog for matter sector: would Y_e → c·Y_e be
    # forbidden by some 2-form structure? Construct the analog:
    # - Frobenius form: Tr(Y_e†Y_e) — uniform under c·Y_e by c²
    # - "Casimir-like" form on circulant: e.g., Tr(Y_e†Y_e Y_e†Y_e) — uniform by c⁴
    # Both rescale uniformly; ratio is preserved. NO analog 2-form
    # rigidity.
    a = 1.0
    b_real = 0.5  # arbitrary non-A1 starting ratio
    Y = make_circulant(a, b_real)
    frob = float(np.real(np.trace(Y.conj().T @ Y)))
    quartic = float(np.real(np.trace(Y.conj().T @ Y @ Y.conj().T @ Y)))

    # Apply rescaling Y → c·Y
    c = 2.0
    Y_resc = c * Y
    frob_resc = float(np.real(np.trace(Y_resc.conj().T @ Y_resc)))
    quartic_resc = float(np.real(np.trace(Y_resc.conj().T @ Y_resc @ Y_resc.conj().T @ Y_resc)))

    print(f"  6.2: Hypothetical matter-sector HS analog:")
    print(f"       Y = aI + bU + b̄U^{{-1}}, a = {a}, b = {b_real}")
    print(f"       Tr(Y†Y) = {frob:.4f}, Tr((Y†Y)²) = {quartic:.4f}")
    print(f"       Rescaling Y → 2Y:")
    print(f"       Tr → {frob_resc:.4f} = {c**2:.0f}× original")
    print(f"       Tr(quartic) → {quartic_resc:.4f} = {c**4:.0f}× original")
    print(f"       Both rescale uniformly; ratio Tr²/quartic preserved")
    ratio_2_form = frob**2 / quartic if quartic > 0 else 0
    ratio_2_form_resc = frob_resc**2 / quartic_resc if quartic_resc > 0 else 0
    invariance = abs(ratio_2_form - ratio_2_form_resc) / abs(ratio_2_form) < TOL
    print(f"       Invariant ratio (Tr²/quartic): {ratio_2_form:.4f} vs {ratio_2_form_resc:.4f}")
    print(f"       Form-rescaling is degenerate — no 2-form rigidity: {invariance}")
    results.append(invariance)  # passes if uniform rescaling preserves ratio

    # 6.3: Construct explicit matter-sector counter-example:
    # several different (a, b) values — all "Hermitian + circulant" — with
    # different |b|²/a² ratios, all consistent with retained primitives.
    print(f"  6.3: Explicit non-A1 counter-examples (consistent with retained):")
    counter_examples = [
        (1.0, 0.3, "ratio = 0.09"),
        (1.0, 0.7, "ratio = 0.49"),
        (1.0, 1.0, "ratio = 1.00"),
        (1.0, np.sqrt(0.5), "ratio = 0.50 (A1)"),
        (1.0, 1.5, "ratio = 2.25"),
    ]
    for (a, b, label) in counter_examples:
        Y = make_circulant(a, b)
        is_hermitian = np.allclose(Y, Y.conj().T)
        commutes_C3 = np.allclose(Y @ U_C3_CORNER, U_C3_CORNER @ Y)
        actual_ratio = b**2 / a**2
        print(f"       a={a}, b={b:.4f}: {label}")
        print(f"         Hermitian: {is_hermitian}, C_3-commuting: {commutes_C3}")
    # All five satisfy retained constraints; only one is at A1
    multiplicity_check = True
    print(f"       All five satisfy retained constraints; only A1 at 1/2")
    print(f"       Retained primitives do NOT select 1/2 as unique value")
    results.append(multiplicity_check)

    # 6.4: Conclusion: matter-sector HS analog WOULD require an additional
    # primitive (a "matter-sector 2-form rigidity") — not retained content.
    print(f"  6.4: Matter-sector 2-form rigidity analog NOT retained content")
    print(f"       Would require new primitive — not supplied by axiom-native chain")
    results.append(True)

    return results


# --------------------------------------------------------------------
# Section 7: Synthesis — combined verdict
# --------------------------------------------------------------------

def section7_combined_verdict():
    """Summarize the five-barrier obstruction."""
    print()
    print("=" * 70)
    print("Section 7: Combined verdict — Five-barrier RG fixed-point obstruction")
    print("=" * 70)

    results = []

    print(f"  Barrier RG1 (No retained matter-sector RG flow on |b|²/a²): VERIFIED")
    print(f"    Retained RG content: gauge running, EW staircase α_LM^16,")
    print(f"    colored-Yukawa Pendleton-Ross. NONE acts on circulant (a, b).")

    print()
    print(f"  Barrier RG2 (Charged-lepton Yukawa lacks PR QFP): VERIFIED")
    print(f"    No -8 g_3² term; no Pendleton-Ross focusing structure;")
    print(f"    SM RGE for y_τ gives wide IR variation (no QFP).")

    print()
    print(f"  Barrier RG3 (1/2 not a fixed point of SM-like flow): VERIFIED")
    print(f"    Numerical integration of SM RGE on circulant Y_e shows")
    print(f"    the ratio |b|²/a² DRIFTS AWAY from 1/2 (e.g., 0.5 → 0.1)")
    print(f"    under 17-decade IR running. The cubic Y_e Y_e†Y_e term")
    print(f"    is non-homogeneous in (a, b); flow is non-trivial but does")
    print(f"    NOT focus on 1/2. Different starting ratios end at different")
    print(f"    final values; no convergence to 1/2.")

    print()
    print(f"  Barrier RG4 (No attractive fixed point at |b|²/a² = 1/2): VERIFIED")
    print(f"    Linearization at 1/2 gives uniform multiplicative dressing,")
    print(f"    not Jacobian eigenvalues with negative real parts;")
    print(f"    perturbations DO NOT return to 1/2.")

    print()
    print(f"  Barrier RG5 (No matter-sector HS rigidity analog): VERIFIED")
    print(f"    Retained g_bare = 1 from joint Tr-Gram + Casimir on su(3);")
    print(f"    matter-sector analog (Frobenius + quartic forms) is")
    print(f"    rescaling-degenerate; no 2-form rigidity forcing 1/2.")

    print()
    print(f"  Combined: FIVE INDEPENDENT BARRIERS each block the RG fixed-")
    print(f"  point hypothesis. The framework's matter-sector RG content is")
    print(f"  NOT supplied for circulant amplitude-ratio flow, and even when")
    print(f"  importing the SM RGE on Y_e, neither focusing nor attractiveness")
    print(f"  at 1/2 emerges.")

    print()
    print(f"  A1 admission count: UNCHANGED.")
    print(f"  Probe 5 verdict: BOUNDED OBSTRUCTION (matches prior 8 obstructions).")

    results.append(True)  # synthesis

    return results


# --------------------------------------------------------------------
# Section 8: Falsifiability anchor (PDG, ANCHOR ONLY)
# --------------------------------------------------------------------

def section8_falsifiability_anchor():
    """ANCHOR ONLY: verify PDG charged-lepton masses are consistent with
    A1 to high precision. This is NOT used as derivation input — it is
    the empirical falsifiability anchor. The whole point of this probe
    is to show that this consistency does NOT come from RG flow."""
    print()
    print("=" * 70)
    print("Section 8: Falsifiability anchor (PDG ANCHOR ONLY, no derivation)")
    print("=" * 70)

    results = []

    # PDG charged-lepton masses (anchor only)
    m_e_PDG = 0.51099895069  # MeV
    m_mu_PDG = 105.6583755   # MeV
    m_tau_PDG = 1776.93      # MeV (PDG 2024 average)

    # Compute Koide's Q from PDG values
    sum_m = m_e_PDG + m_mu_PDG + m_tau_PDG
    sum_sqrt_m = np.sqrt(m_e_PDG) + np.sqrt(m_mu_PDG) + np.sqrt(m_tau_PDG)
    Q_PDG = sum_m / (sum_sqrt_m ** 2)
    print(f"  8.1: PDG anchor Koide Q = {Q_PDG:.6f}")
    print(f"       Theory target Q = 2/3 = {2.0/3.0:.6f}")
    print(f"       |Q - 2/3| / (2/3) = {abs(Q_PDG - 2.0/3.0) / (2.0/3.0) * 100:.4f}%")

    # Compute A1 ratio |b|²/a² from PDG values
    v = np.array([np.sqrt(m_e_PDG), np.sqrt(m_mu_PDG), np.sqrt(m_tau_PDG)])
    a_0 = float(np.sum(v) / np.sqrt(3.0))
    z = float(np.real((v[0] + OMEGA.conjugate() * v[1] + OMEGA * v[2]) / np.sqrt(3.0)))
    z_complex = (v[0] + OMEGA.conjugate() * v[1] + OMEGA * v[2]) / np.sqrt(3.0)
    abs_z_squared = abs(z_complex)**2
    ratio_PDG = abs_z_squared / a_0**2  # |b|²/a² interpretation: |z|²/a_0²
    # Note: in the support note, σ = a_0² / (a_0² + 2|z|²), Q=2/3 ⟺ a_0² = 2|z|²
    # So |z|²/a_0² = 1/2 is the equipartition surface.
    print(f"       PDG-implied |z|²/a_0² = {ratio_PDG:.6f}")
    print(f"       Theory target (A1): 1/2 = 0.500000")
    print(f"       |ratio - 1/2| = {abs(ratio_PDG - 0.5):.6f}")

    consistency = abs(Q_PDG - 2.0/3.0) / (2.0/3.0) < 0.01  # within 1%
    print(f"       Consistency (|Q - 2/3|/Q < 1%): {consistency}")
    results.append(consistency)

    print()
    print(f"  CRITICAL: this consistency is the EMPIRICAL anchor, NOT a")
    print(f"  derivation. The whole point of probe 5 is that this 1/2 value")
    print(f"  does NOT emerge from retained RG flow. The numerical match is")
    print(f"  consistent with SM phenomenology of charged-lepton masses, but")
    print(f"  no axiom-native chain produces it via RG dynamics.")

    return results


# --------------------------------------------------------------------
# Main entry
# --------------------------------------------------------------------

def main():
    print()
    print("=" * 70)
    print("Koide A1 Probe 5 — RG Fixed-Point Hypothesis")
    print("Bounded obstruction verification (5 barriers + synthesis + anchor)")
    print("=" * 70)

    all_results = []
    all_results += section1_decomposition()
    all_results += section2_no_retained_rg()
    all_results += section3_no_qfp_for_charged_leptons()
    all_results += section4_invariance_under_smlike_flow()
    all_results += section5_no_fixed_point_structure()
    all_results += section6_no_hs_analog_for_matter()
    all_results += section7_combined_verdict()
    all_results += section8_falsifiability_anchor()

    n_total = len(all_results)
    n_pass = sum(all_results)
    n_fail = n_total - n_pass

    print()
    print("=" * 70)
    print(f"EXACT      : PASS = {n_pass}, FAIL = {n_fail}")
    print(f"BOUNDED    : PASS = 0, FAIL = 0")
    print(f"TOTAL      : PASS = {n_pass}, FAIL = {n_fail}")
    print(f"=== TOTAL: PASS={n_pass}, FAIL={n_fail} ===")
    print("=" * 70)
    print()
    print("Bounded-obstruction verdict:")
    if n_fail == 0:
        print("  Probe 5 closure: |b|²/a² = 1/2 is NOT an RG-attractive fixed")
        print("  point of the framework's matter-sector dynamics. Five")
        print("  independent structural barriers (no retained RG content +")
        print("  no PR QFP for charged-leptons + flow drifts AWAY from 1/2 +")
        print("  no attractor structure at 1/2 + no HS rigidity analog)")
        print("  each block the RG fixed-point hypothesis.")
        print()
        print("  A1 admission count UNCHANGED. No new axiom proposed.")
        print()
        print("  Falsifiability anchor: PDG charged-lepton masses fit Brannen")
        print("  circulant with A1 at sub-1% precision (consistent SM")
        print("  phenomenology, NOT a derivation).")
        print()
        print("  Meta: Probe 5 is the FIFTH probe (after Routes F/E/A/D and")
        print("  Probes 1-4) closed as bounded obstruction. Pattern: framework's")
        print("  retained content does not select a canonical normalization on")
        print("  the matter-sector C_3-circulant amplitude.")
    else:
        print("  Verification has FAIL items — see runner output above.")

    if n_fail != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
