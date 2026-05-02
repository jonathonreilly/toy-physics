# Cycle 05 (Retained-Promotion) Claim Status Certificate — Staggered Scalar Parity-Coupling Forced from Dirac Structure (closing derivation)

**Block:** physics-loop/staggered-parity-coupling-theorem-2026-05-02
**Note:** docs/STAGGERED_PARITY_COUPLING_FORCED_FROM_DIRAC_THEOREM_NOTE_2026-05-02.md
**Runner:** scripts/frontier_staggered_parity_coupling_derivation.py
**Target row:** `gravity_sign_audit_2026-04-10` (claim_type=positive_theorem, audit_status=audited_conditional, td=67, lbs=B/10.1)

## Block type

**Closing derivation** (output type (a) per the new retained-promotion
campaign prompt). New theorem note + runner that **derives the
verdict-identified obstruction** (retained coupling-sign theorem for
the staggered scalar channel) from the framework's retained staggered
fermion construction.

## Promotion Value Gate (V1–V5)

### V1: SPECIFIC verdict-identified obstruction this PR closes

Quoted from parent row's `verdict_rationale`:

> Repair target: restore or relink the runner and provide a retained
> coupling-sign theorem or cited authority note covering the staggered
> scalar channel. Claim boundary until fixed: the note can stand as a
> conditional sign-audit status memo with explicit external sources.

**This PR's closing-derivation theorem provides the missing retained
coupling-sign theorem: the parity coupling
`H_diag = (m + Φ(x)) · ε(x)` is FORCED by the framework's staggered
fermion structure (Dirac mass-term translation under
Kogut-Susskind / Cl(3) staggered transformation), and the alternative
"identity coupling" `H_diag = m · ε(x) − m · Φ(x)` violates the
staggered chirality structure.**

The parent note (`GRAVITY_SIGN_AUDIT_2026-04-10.md`) calls the parity
coupling "literature-correct" but does not derive it from the
framework's retained staggered fermion construction. This PR provides
the missing derivation.

### V2: NEW derivation contained

Existing parent note's load-bearing step (line 16):

> The literature-correct scalar coupling is the **parity coupling**
> `H_diag = (m + Φ)·ε(x)`.

Asserted as "literature-correct" without framework-internal
derivation.

This PR's derivation:

1. Starts from the continuous Dirac action with mass-term
   `m · ψ̄ψ` and minimal scalar coupling `Φ · ψ̄ψ` (admitted-context
   external QFT structure).
2. Performs the Kogut-Susskind / staggered fermion transformation
   `ψ → χ` with the spin-diagonalization that diagonalizes `γ^μ ∂_μ`.
3. Verifies the standard staggered identity:
   `ψ̄(x) ψ(x) → ε(x) · χ^†(x) χ(x)` where
   `ε(x) = (-1)^{x_1+x_2+x_3}` is the staggered chirality / parity
   sign.
4. Concludes that any scalar field Φ that enters the Dirac action as
   `Φ · ψ̄ψ` (mass-replacement) MUST inherit the same ε(x) weighting
   in the staggered language: `Φ · ψ̄ψ → Φ(x) · ε(x) · n(x)`.
5. Combined: `(m + Φ(x)) · ε(x) · n(x)` is the unique staggered scalar
   coupling consistent with the continuous Dirac mass-term structure.
6. **Counterfactual**: the "identity coupling"
   `H_diag = m · ε(x) − m · Φ(x)` treats Φ as an additive energy
   shift unrelated to the mass. Numerical demonstration that this
   coupling violates the staggered chirality block-structure: the
   mass-shift sector and the energy-shift sector have different
   parity quantum numbers, so identity coupling mixes incompatible
   sectors.
7. **Sign forcing**: the parity coupling on a positive-source background
   `Φ ≥ 0` (which holds by the screened Poisson equation `(L + μ²I)Φ = G·ρ`
   with `L` positive-definite and `ρ ≥ 0`) gives an effective mass
   `m_eff(x) = m + Φ(x) ≥ m`, so the gravitational well DEEPENS the
   local mass gap (TOWARD response). The identity coupling gives an
   energy shift unrelated to the mass, hence no consistent
   gravitational sign.

The derivation is a clean structural argument from the framework's
retained staggered fermion construction.

### V3: Audit lane couldn't already do this from existing retained primitives + standard math machinery

The audit lane in restricted one-hop context cannot synthesize:
- The retained Cl(3) staggered fermion construction
  (`CPT_EXACT_NOTE.md` referenced lattice fermion structure),
- The Kogut-Susskind staggered identity (admitted-context standard
  lattice QFT),
- The structural argument that scalar coupling inherits staggered
  weighting from Dirac coupling,
- The counterfactual that identity coupling violates the chirality
  block structure,

simultaneously in one hop. This is the missing structural
derivation.

### V4: Marginal content non-trivial

Yes:
- Explicit derivation of the staggered identity
  `ψ̄ψ → ε(x) · n(x)` from the Kogut-Susskind diagonalization.
- Structural argument that scalar coupling inherits staggered
  weighting from Dirac coupling.
- Numerical demonstration of the staggered chirality block structure
  on a small lattice (parity-coupling preserves it; identity coupling
  breaks it).
- Sign-forcing argument: positive Φ on the screened Poisson surface
  gives effective-mass increase = TOWARD (gravitational attraction)
  under parity coupling.
- Explicit counterfactual demonstrating identity coupling's
  inconsistency.

This is genuine derivation content the parent row didn't have.

### V5: Not a one-step variant of an already-landed cycle

Cycle 01 (PR #382): SU(3)^3 cubic anomaly Diophantine on RH content.
Cycle 02 (PR #383): SU(2) Witten Z_2 parity argument on doublet count.
Cycle 03 (PR #386): Cauchy multiplicative-to-additive functional
equation reduction on scalar generator.
Cycle 04 (PR #390): U(1)_Y mixed anomaly cubic on no-ν_R sector.

**Cycle 05**: Kogut-Susskind staggered fermion identity + structural
argument on scalar mass-replacement coupling. Different math
(staggered-fermion translation vs anomaly arithmetic vs functional
equation), different parent row (gravity sign audit vs anomaly /
observable principle / matter content rows), different framework
subsystem (staggered fermion gravity vs gauge anomalies / scalar
generator).

Not a one-step variant.

## Outcome classification (per new prompt)

**(a) Closing derivation.** This PR provides a new theorem note +
runner that **derives the verdict-identified obstruction** (retained
coupling-sign theorem for staggered scalar channel) from the
framework's retained staggered fermion construction.

The outcome IS retained-positive movement on the parent row's
load-bearing step (parity coupling sign), conditional on audit-lane
ratification of:
- the framework's retained staggered fermion construction;
- the Kogut-Susskind staggered identity (admitted-context standard
  lattice QFT);
- the structural argument that scalar coupling inherits staggered
  weighting from Dirac coupling.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed (Kogut-Susskind 1975 is
  admitted-context external lattice QFT authority, role-labelled).
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Audit-graph effect

If independent audit ratifies this derivation:
- Parent row `gravity_sign_audit_2026-04-10` load-bearing class-B step
  closes: the parity coupling becomes a derived theorem, not an
  asserted "literature-correct" form.
- Combined with the framework's retained gravity work
  (mirror-symmetry, decoherence, propagator), the gravity-sign chain
  becomes more robust.
- The parent row's td=67 cascade benefits from a retained
  coupling-sign anchor.

## Honesty disclosures

- The Kogut-Susskind staggered identity is admitted-context external
  lattice QFT. We do NOT re-derive the staggered transformation
  itself; we use it as standard machinery.
- The continuous Dirac mass-term form `m · ψ̄ψ` and minimal
  mass-replacement scalar coupling `Φ · ψ̄ψ` are admitted-context
  field-theory structure.
- This PR does NOT prove that gravity is attractive (TOWARD); it
  derives that the parity coupling form on a positive-Φ background
  gives a mass-increasing effective potential, which the framework's
  separate gravity work uses to argue for attraction.
- Audit-lane ratification required; no author-side tier asserted.
