# Framework-Specific Closure Candidate Search

**Date:** 2026-05-05
**PR:** [#528](https://github.com/jonathonreilly/cl3-lattice-framework/pull/528)
**Goal:** Identify Cl(3)/Z³ structural constraints that could yield CLOSED-FORM
analytic ⟨P⟩(β=6), beyond what standard Anderson-Kruczenski/Kazakov-Zheng
bootstrap achieves (which gives bounds, not closure)

## The Distinguishing Question

**Standard SDP bootstrap** uses:
- Reflection positivity (assumed for SU(3) Wilson)
- Migdal-Makeenko equations (algebraic identities)
- Result: 1-3% bracketing of ⟨P⟩(β=6)

**Framework's potential addition**:
- Cl(3)/Z³-specific algebraic constraints not present in standard SU(3)
- If these zero out portions of the SDP feasible region, could close
- This is THE Nobel-quality frontier

## Candidate Search Methodology

For each Cl(3)/Z³ structural feature, ask:
1. Does this feature restrict Wilson loop relations BEYOND standard SU(3)?
2. Can the restriction be expressed as a linear/algebraic constraint?
3. When added to SDP, does it tighten beyond [0.59, 0.605] toward exact 0.5934?

## Candidate Catalog

### CANDIDATE 1: Cl(3) Z₂ Even/Odd Grading

**Structure**: Cl(3) has Z_2 grading:
- Even: scalar (1) + bivectors (3) = 4-dim
- Odd: vectors (3) + pseudoscalar (1) = 4-dim

**SU(3) embedding**: SU(3) generators T_a (8 traceless Hermitian) decompose
into: 3 in vector subspace, 5 in bivector? Need explicit check.

**Search**: do Wilson loops have specific behavior under this grading?
- Wilson plaquette χ_(1,0)(U) for fundamental rep (1,0)
- Does (1,0) decompose into Z_2-even or Z_2-odd parts?
- If grading restricts allowed Wilson loop products, gives constraint

**STATUS**: speculative, requires explicit Cl(3)→SU(3) decomposition check

### CANDIDATE 2: Z₃ Center Symmetry

**Structure**: SU(3) center is Z_3 = {1, ω, ω²}, ω = e^{2πi/3}

**SU(3) Wilson plaquette**: invariant under center transformation U → ωU
because closed loop with no fundamental matter

**Cl(3)/Z³ specific**: framework's per-site Cl(3) algebra has specific
center transformation structure

**Constraint**: irrep (p,q) transforms under center as ω^(p-q). For all
contributions to ⟨P⟩, must have net Z_3 charge zero.

**Standard already enforces this**: pure gauge SU(3) bootstrap automatically
Z_3 invariant (no fundamental matter to break it)

**Framework addition**: ?
- If Cl(3) per-site structure couples to center in specific way,
  could enforce ADDITIONAL selection rules

**STATUS**: doesn't obviously add beyond standard SU(3) bootstrap

### CANDIDATE 3: Per-Site Cl(3) Uniqueness

**Structure**: AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM proves per-site
Hilbert space is 2-dim Pauli irrep

**SU(3) Wilson lattice**: link variables U_l ∈ SU(3) (continuous group),
Hilbert space is L²(SU(3))^N_links per spatial slice

**Framework**: per-site Cl(3) acts on 2-dim Pauli — but this is the FERMION
sector (matter), not the gauge sector

**Search**: does per-site fermion Hilbert space constrain gauge Wilson loops?
- Fermion-gauge coupling via staggered-Dirac
- Effective action after fermion integration adds Wilson loop terms
- Could give specific Wilson loop relations

**STATUS**: requires dynamical fermion calculation; quenched gauge sector
unaffected at leading order

### CANDIDATE 4: Pseudoscalar i² = -I Algebraic Structure

**Structure**: Cl(3) pseudoscalar i = G_1 G_2 G_3 satisfies i² = -I
(verified in Pauli irrep)

**Search**: does i² = -I impose specific Wilson loop matrix element relation?
- For Wilson loops involving i factor, U_p × i has specific Hermiticity
- Could give Wilson loop ↔ adjoint-Wilson-loop relations

**STATUS**: speculative; requires explicit Wilson loop computation in
Cl(3)-graded variables

### CANDIDATE 5: Reduction-Law Determinacy

**Framework theorem**: P_full(β) = P_1plaq(β_eff(β)) UNIQUELY
(REDUCTION_EXISTENCE_THEOREM)

**Susceptibility flow**: β_eff'(β) = χ_L(β) / χ_1plaq(β_eff(β))

**Search**: if χ_L(β) can be UNIQUELY determined from framework primitives
(no freedom), then β_eff(6) is unique, giving closed-form ⟨P⟩(6)

**Current state**:
- Framework has χ_L onset (β^4 term)
- Higher orders require shell enumeration (mixed-cumulant theorem at higher
  shells)
- Framework's INFINITE_HIERARCHY_OBSTRUCTION says no FINITE truncation closes
- BUT framework's spectral-measure theorem says the full χ_L IS uniquely
  determined by the partition function

**KEY INSIGHT**: if framework can express χ_L(β) as a CONVERGENT expansion
with framework-derivable terms at each order, the integral closes.

**STATUS**: most concrete framework-specific path; needs higher-order
mixed-cumulant computation (β^9, β^13 terms)

### CANDIDATE 6: Connected-Hierarchy Borel Resummation

**Framework theorem**: connected hierarchy of cumulants
**INFINITE_HIERARCHY_OBSTRUCTION**: no finite truncation closes

**Search**: does framework's hierarchy structure allow Borel resummation?
- For Borel-resummable series Σ a_n β^n with a_n ~ n!, the integral
  ∫dτ e^{-τ} A(βτ) gives closed form
- Standard QCD perturbation series is BOREL NON-SUMMABLE due to
  renormalons (instantons)
- Framework's mixed-cumulant series might have specific structure
  allowing Borel summation IF framework constraints kill the renormalons

**STATUS**: speculative; would need to compute framework's series to
see if renormalons appear

### CANDIDATE 7: Anomaly-Forces-Time

**Framework theorem**: ANOMALY_FORCES_TIME — anomaly cancellation forces
specific time-direction structure

**Search**: does anomaly impose Wilson loop relations?
- Anomalies typically constrain low-energy effective actions
- Could enforce specific gauge sector identities

**STATUS**: speculative; relation to Wilson loop bootstrap unclear

### CANDIDATE 8: V-Invariant Tensor-Network Convergence

**Framework**: V-invariant L_s=2 APBC SPATIAL cube via tensor-network
contraction gives specific value
- Verified via MC: 0.4225 (V-invariant Schur)
- Verified via direct MC at L=2: 0.4360

**Search**: if framework can show V-invariant block ALSO determines
3+1D L→∞ value via specific theorem, closes
- Currently V-invariance is shown to be FINITE-VOLUME (L=2 block)
- Full 3+1D requires temporal direction (which gives 0.5934 at L→∞)

**STATUS**: doesn't directly close ⟨P⟩(β=6) since V-invariant is L=2-only

## Most Promising Path: Candidate 5 + 6

**Combined framework-specific approach**:

1. Compute mixed-cumulant terms beyond β^5:
   - Use distinct-shell theorem to enumerate 8-plaquette, 12-plaquette
     shells contributing at β^9, β^13
   - Each shell gives specific SU(3) Haar integral coefficient
   - Pattern: 4 cube shells → β^5; how many shells at β^9, β^13?

2. Examine series structure for framework-specific patterns:
   - If coefficients follow Cl(3)-specific suppression, could be Borel-resummable
   - If pattern matches known closed forms (theta functions, modular forms), could close

3. Borel-Padé extrapolation:
   - With multiple framework-derived coefficients, attempt Borel resummation
   - If successful, gives closed-form analytic ⟨P⟩(β)

**Estimated effort to test Candidate 5+6**: 2-4 weeks
- Most rigorous and concrete framework-specific path
- IF series Borel-resums to known closed form: ★ NOBEL CLOSURE ★
- IF not: still gives tightest analytic bound + extends framework's
  exact perturbative knowledge

## Recommended Next Concrete Step

**Compute the β^9 mixed-cumulant term explicitly** for the framework's
Wilson plaquette. This:

1. Extends framework's exact perturbative knowledge (β^5 → β^9)
2. Provides one more data point for Borel-resummation analysis
3. Reveals whether the series has framework-specific structure
4. Could surface a pattern suggesting closure

Implementation:
- Catalog 8-plaquette closed shells via lattice combinatorics
- For each shell, compute SU(3) Haar integral with explicit signs
- Sum contributions to get β^9 coefficient
- Cross-check against known QCD perturbation theory

Estimated effort: 5-7 days for β^9 computation.

## Search Discipline

For each candidate explored:
- ✅ State the constraint precisely
- ✅ Verify framework-derivability from minimal axioms
- ✅ Add to SDP/ODE and check tightening
- ✅ Document result (closure / no closure / tightening only)

This systematic search across 8 candidates is the framework-specific
closure attempt. Realistic outcome: 1-3 candidates yield additional
constraints; 0-1 might close. The Nobel shot is in the closure-yielding
candidate IF found.
