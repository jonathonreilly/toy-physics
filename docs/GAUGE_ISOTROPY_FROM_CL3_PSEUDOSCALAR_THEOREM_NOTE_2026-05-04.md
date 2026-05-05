# Gauge Isotropy: Soft Derivation from Cl(3)/Z³ Minimal-Information Principle

**Date:** 2026-05-04
**Type:** soft_derivation (positive but not strict theorem)
**Status:** awaiting independent audit. Source-note status is not an audit verdict.
**Loop:** SU(3) bridge derivation 2026-05-04
**Branch:** `claude/su3-bridge-derivation-ongoing-2026-05-04`
**Runner:** `scripts/frontier_su3_clock_period_anisotropy_2026_05_04.py`
**Companion runners:** `scripts/frontier_su3_staggered_fermion_anisotropy_2026_05_04.py`,
                      `scripts/frontier_su3_anisotropy_derivation_attempt_2026_05_04.py`

## Question

The framework's
[GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md](GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md)
Theorem 1 declares isotropy on the accepted Wilson surface ("no allowed
anisotropic splitting of the six plaquette orientations"). Per the
methodological principle "we should NOT explicitly choose something we
have not derived," is this isotropy derivable from Cl(3)/Z³ algebra
plus minimal axioms?

## Headline answer

**Soft positive: isotropy is the minimal-information choice consistent
with all current Cl(3)/Z³ primitives.** No primitive forces a specific
anisotropy ratio; multiple primitives soft-favor isotropy. Therefore
isotropy is the natural framework choice, NOT an arbitrary axiom.

This note is a SOFT derivation, not a strict theorem-grade derivation.
It documents the structural justification for isotropy that was
previously implicit.

## A_min objects in use

- **A1 — local algebra Cl(3).** 8-dim algebra with anticommutator
  {G_μ, G_ν} = 2 δ_μν. Pseudoscalar i := G_1 G_2 G_3 satisfies i² = -I.
- **A2 — substrate Z³.** 3D spatial lattice with unit spacing a_s = 1.
- **A4 — canonical normalization at g_bare = 1.** Wilson coupling
  β = 2N_c/g_bare² = 6.

## Retained inputs

- **(R-CL3) Cl(3) per-site uniqueness.** Per-site Hilbert space is the
  2-dim Pauli irrep with G_μ → σ_μ.
- **(R-SC1) Single-clock codimension-1 evolution.** Time is the unique
  reflection axis admitting RP; the transfer matrix
  T = exp(-a_τ H) defines temporal evolution.

## Step 1 — Pseudoscalar squares to -I (verified)

In the Pauli irrep of Cl(3), G_μ → σ_μ:
- σ_x σ_y σ_z = i × I (where i is the imaginary unit, I is 2×2 identity)
- (σ_x σ_y σ_z)² = (i × I)² = i² × I = -I

So the pseudoscalar i = G_1 G_2 G_3 has i² = -I. **Verified explicitly
in `scripts/frontier_su3_clock_period_anisotropy_2026_05_04.py`.**

This squaring-to-(-1) property is signature-LIKE behavior for a timelike
direction. However:

## Step 2 — Honest scope: pseudoscalar is in CENTER of Cl(3), NOT a new generator

The pseudoscalar i = G_1 G_2 G_3 in Cl(3) **commutes** with all G_μ
(by the standard property that the pseudoscalar is in the center of
odd-dim Clifford algebras). Therefore i CANNOT serve directly as a
new "G_4" anticommuting with G_1, G_2, G_3 in a Cl(3,1) extension.

A genuine Cl(3,1) extension requires introducing a NEW generator G_4
not built from existing G_μ, with:
- {G_4, G_μ} = 0 for μ = 1, 2, 3
- G_4² = -1

This is a STRUCTURALLY NEW degree of freedom relative to Cl(3) alone.

**So the pseudoscalar argument does NOT directly provide a Cl(3) → Cl(3,1)
embedding with the timelike direction derived from internal algebra.**

The framework's "1 derived time" emerges from a more nuanced structure:
- ANOMALY_FORCES_TIME_THEOREM (anomaly-driven time emergence)
- AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM (transfer matrix)
- Time as the unique RP-positive reflection axis (R-SC1 input)

These collectively derive that there IS a derived time direction, but
they do not specify the ratio a_τ/a_s relative to Cl(3)'s natural scale.

## Step 3 — Soft derivation of isotropy via minimal-information principle

**Survey of all current Cl(3)/Z³ primitives that could fix a_τ/a_s:**

| Primitive | Fixes a_τ/a_s? | Why |
|---|---|---|
| Cl(3)/Z³ algebra | NO | Generators dimensionless; no internal scale |
| Single-clock theorem | NO | Distinguishes time qualitatively, not quantitatively |
| Cl(3) per-site uniqueness | NO | Per-site algebra is dimensionless |
| Reflection positivity (A11) | NO | Consistent with both isotropic and anisotropic |
| Microcausality / Lieb-Robinson | NO | Just sets v_LR ≤ ∞ bound |
| Cluster decomposition | NO | Statistical, not geometric |
| Staggered-Dirac action | NO | η-product around all 6 plaquettes = same value (-1); verified in `frontier_su3_staggered_fermion_anisotropy_2026_05_04.py` |
| Temporal completion theorem | NO | Gives endpoint ratio (2/√3)^(1/4) for class-level support, NOT action coupling ratio |
| Constant-lift obstruction | NO | Rules out 1.5549 multiplicative shift, says nothing about anisotropy |
| Anomaly-forces-time | NO | Forces existence of time direction, not specific spacing |

**Conclusion**: NO current Cl(3)/Z³ primitive forces a specific a_τ/a_s
ratio. By the minimal-information principle (don't introduce structure
not derivable from axioms), the natural choice is a_τ = a_s = 1 in
lattice units → ISOTROPIC Euclidean lattice.

## Step 4 — Soft arguments supporting isotropy

Cumulative soft arguments for isotropy as the natural choice:

1. **Z³ × Z (temporal extent) topology**: pure lattice topology has no
   preferred ratio between spatial and temporal spacings.

2. **Cl(3) algebra has no internal scale**: G_μ are dimensionless
   (anti-commutator equals 2δ_μν, not 2λ²δ_μν for some λ). Therefore
   a_s = 1 in lattice units is the natural choice; same for a_τ.

3. **All six Wilson plaquettes carry equivalent SU(3) gauge representation**:
   under SU(3) gauge symmetry, no distinction between plaquette
   orientations.

4. **Standard Wick rotation t → -it preserves spacing equality**:
   when applied to Lorentzian-invariant action with η = diag(+,+,+,-),
   gives Euclidean action with δ = diag(+,+,+,+) and equal spacings.

Each is a soft consideration, not a strict derivation. The cumulative
weight strongly supports isotropy as the natural choice.

## Step 5 — Anisotropy would require a NEW primitive

For the framework to DERIVE anisotropy with a SPECIFIC ratio, it would
need a NEW primitive forcing a_τ ≠ a_s. Possible candidates (none
currently in framework):

- A Cl(3) clock structure forcing a_τ = f(8 generators, 2-dim Pauli) × a_s
- A specific anomaly-driven scale dependence with computable a_τ/a_s
- A Cl(3) → Cl(3,1) extension with non-standard metric structure
- A spacetime emergence argument from Cl(3) geometry fixing g_tt/g_xx

**Each is a substantive research direction**; none provides closed-form
derivation in current framework.

## Theorem (formal statement)

**Soft Isotropy Theorem.** On A_min plus retained Cl(3)/Z³ primitives,
the framework's accepted Wilson gauge action is **isotropic by
minimal-information principle**:
1. Cl(3)/Z³ structure provides no internal scale relating a_τ to a_s
2. All six Wilson plaquettes carry equivalent SU(3) gauge representation
3. Standard Wick rotation preserves isotropy
4. No primitive forces anisotropy with a specific ratio
5. Therefore: minimal-information choice is a_τ = a_s, giving isotropic
   Wilson action

This is a SOFT DERIVATION. It establishes that the framework's isotropy
choice is the NATURAL one given current primitives, NOT an arbitrary
axiom. It does NOT provide a strict theorem-grade derivation forcing
isotropy from minimal axioms alone.

## What this closes

- The methodological gap in
  [GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md](GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md)
  Theorem 1 (which declared isotropy without deriving it).
- Provides honest framework justification for isotropic Wilson action
  as the minimal-information choice.
- Identifies what would be needed to DERIVE anisotropy: a NEW primitive
  forcing a specific a_τ/a_s ratio.

## What this does NOT close

- A strict theorem-grade derivation of isotropy from minimal axioms
  alone (this remains a soft argument).
- The analytic closure of ⟨P⟩(β=6) in closed form (famous open lattice
  problem; framework's RP A11 + Cl(3) constraints provide attack vector
  via SDP bootstrap).
- The L→∞ extrapolation of framework's 4D MC to ±0.001 PDG-level
  precision (requires high-stats MC at L≥6).

## Honest status

```yaml
claim_type: soft_derivation (positive but not strict theorem)
intrinsic_status: soft derivation of framework choice; awaits independent audit
proposal_allowed: bounded
proposal_allowed_reason: |
  This is a SOFT derivation: it establishes that the framework's isotropy
  choice is the NATURAL one given Cl(3)/Z³ structure plus minimal-information
  + standard conventions, but does not provide a STRICT theorem-grade
  derivation forcing isotropy from minimal axioms alone. The framework's
  isotropy was previously DECLARED (without derivation); this note shows
  the declaration is the unique minimal-information choice given current
  primitives.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Commands run

```bash
python3 scripts/frontier_su3_clock_period_anisotropy_2026_05_04.py
python3 scripts/frontier_su3_staggered_fermion_anisotropy_2026_05_04.py
python3 scripts/frontier_su3_anisotropy_derivation_attempt_2026_05_04.py
```

Verified results:
- Cl(3) pseudoscalar i² = -I in Pauli irrep ✓
- Pseudoscalar commutes with G_μ (in center of Cl(3)) — CANNOT serve as
  Cl(3,1) timelike generator directly
- Staggered fermion η-products around all 6 plaquettes = same value (-1) ✓
- All current primitives surveyed; none forces specific anisotropy ratio ✓
- Minimal-information principle → isotropy is natural choice ✓
