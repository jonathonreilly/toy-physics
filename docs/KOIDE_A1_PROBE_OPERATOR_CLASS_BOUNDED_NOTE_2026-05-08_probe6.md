# Koide A1 Probe 6 — Operator-Class Expansion Bounded Obstruction

**Date:** 2026-05-08
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Probe 6 closure attempt for
the A1 √2 equipartition admission on the charged-lepton Koide lane.
Tests whether the Brannen ansatz has been formulated on the wrong
operator class (Hermitian C_3-equivariant), and whether expanding to
complex circulants, squared-mass matrices, or operator-on-operator
actions opens a closure path.
**Status:** source-note proposal for a negative Probe 6 closure —
shows that none of the three operator-class expansions (Hypothesis A:
complex circulant; Hypothesis B: M = Y† Y squared mass; Hypothesis C:
operator-on-operator action on M_3(ℂ)) opens a closure path for A1.
Each hypothesis lands either back in the prior Hermitian sub-class
(B, C) or in a strictly larger moduli where A1 is even less forced
(A). The A1 admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-a1-probe-operator-class-20260508
**Primary runner:** [`scripts/cl3_koide_a1_probe_operator_class_2026_05_08_probe6.py`](../scripts/cl3_koide_a1_probe_operator_class_2026_05_08_probe6.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_probe_operator_class_2026_05_08_probe6.txt`](../logs/runner-cache/cl3_koide_a1_probe_operator_class_2026_05_08_probe6.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Question

Eight prior attacks on the A1 √2-equipartition admission have all
closed negatively:

  - Routes A (Koide-Nishiura U(3) quartic), D (Newton-Girard polynomial),
    E (Kostant-Weyl-vector coincidence), F (Yukawa Casimir-difference)
  - Round-2 Probes 1-4 (each documented in their respective notes)

ALL EIGHT assumed the **Brannen ansatz**: a Hermitian C_3-equivariant
operator on hw=1 ≅ ℂ³ of the circulant form

```
H = a·I + b·C + b̄·C²,    a ∈ ℝ,  b ∈ ℂ    (3 real DOF)
```

Hypothesis under test (Probe 6): **the Brannen ansatz might be the
wrong operator class.** The 8 attack failures might be artifacts of
working in a too-restrictive sub-class. Specifically:

1. Yukawa coupling matrices `Y_e` are generally NOT Hermitian in
   standard QFT; the squared mass matrix `M = Y_e† Y_e` is the
   Hermitian object.

2. A general C_3-equivariant complex circulant `H = a·I + b·C + c·C²`
   with `a, b, c ∈ ℂ` has 6 real DOF (5 after overall scale removal),
   not 3. The Hermitian sub-class `c = b̄` is a strict 3-DOF
   restriction.

3. The relevant operator might live on a different space — not on
   hw=1 directly but on `M_3(ℂ)` operators (Yukawa matrices
   themselves), or via operator-on-operator action.

4. A1-condition might be derivable in the larger operator class —
   e.g., from a positivity constraint on the bilinear `Y_e† Y_e`, or
   from a structural property of complex circulants that the
   Hermitian sub-class loses.

**Question:** Does dropping the Hermitian assumption (or expanding
to operator-on-operator action) give a path to A1 closure that the
8 prior attacks couldn't access?

## Answer

**No.** None of the three operator-class expansions opens a closure
path. Five independent structural observations each block the proposed
expansions:

1. **Hypothesis B collapse.** The squared mass matrix `M = Y† Y`
   built from a complex circulant `Y = aI + bU + cU²` is
   automatically Hermitian and circulant. Specifically,
   ```
   M = α·I + β·U + β̄·U²    where
     α = |a|² + |b|² + |c|²    (real, positive)
     β = āb + c̄a + b̄c       (complex)
   ```
   So Hypothesis B does NOT escape the prior 3-DOF Hermitian sub-class.
   The squared-mass matrix lives in EXACTLY THE SAME operator class
   the 8 prior attacks already worked on.

2. **Hypothesis A "more DOF" trap.** The 6-DOF complex circulant
   gives MORE compatibility with A1, not LESS. A1 is a codimension-1
   constraint in either 3-DOF or 6-DOF moduli — the larger class
   admits A1 on a strictly higher-dimensional surface (5D in 6D vs
   2D in 3D). More DOF means more freedom, not more force. This is
   the "more DOF doesn't help" trap explicitly flagged in the task.

3. **Hypothesis C identity.** C_3 acting on M_3(ℂ) by conjugation
   `A → U A U†` has invariant subspace = circulants, exactly the
   same class as R1 of the existing
   `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE` (Hermitian: 3 DOF;
   non-Hermitian: 6 DOF). No new structure.

4. **Positivity is not a forcing principle.** Positivity of M is
   COMPATIBLE with A1 for some δ (`δ = 0`: all eigenvalues > 0) and
   INCOMPATIBLE for others (`δ = π/3`: one eigenvalue < 0). Positivity
   thus carves out only a sub-region; it does NOT force A1 to be
   `|β|²/α² = 1/2`.

5. **Brannen ansatz is the correct operator class for stating A1.**
   The Hermitian sub-class is exactly the one in which Brannen's
   `1 + √2 cos(δ + 2πk/3)` form arises. Expanding the operator class
   either (a) lands back in the same class (B, C), or (b) generalizes
   to a larger class where A1 is even less constrained (A). The
   8 prior attack failures are NOT artifacts of the operator class —
   they reflect a structural absence of forcing principle.

The combined picture: **all three operator-class expansions
(Hypotheses A, B, C) are structurally barred from closing A1 within
retained content.** The A1 admission count is unchanged.

## Setup

### Premises (A_min for Probe 6 closure attempt)

| ID | Statement | Class |
|---|---|---|
| A1 | Cl(3) local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | Z³ spatial substrate | framework axiom; same source |
| Embed | Cl⁺(3) ≅ ℍ → SU(2)_L; ω pseudoscalar → U(1)_Y | retained: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) |
| GS | One-Higgs gauge selection: Y_e is arbitrary 3×3 complex matrix | retained: [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md) |
| WardFree | Y_e remains free 3×3 under direct top-Ward lift | retained: [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md) |
| Circulant | C_3-equivariant on hw=1 lies in span{I, U, U²}; Hermitian sub-class is `aI + bU + b̄U²` | retained: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| Equiv | Any derived operator from C_3-symmetric primitives is C_3-equivariant | retained: [`A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md`](A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md) Step 2 |
| KoideAlg | Koide Q = 2/3 ⟺ a₀² = 2|z|² ⟺ |b|²/a² = 1/2 (algebraic) | retained: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| PosParent | Any positive C_3-covariant parent is circulant; nontrivial parents live in eigenvalue/Fourier channel | retained: [`KOIDE_POSITIVE_PARENT_AXIS_OBSTRUCTION_NOTE_2026-04-18.md`](KOIDE_POSITIVE_PARENT_AXIS_OBSTRUCTION_NOTE_2026-04-18.md) |
| SchurInh | Reduction-class theorem: enlarging the carrier preserves the obstruction under C_3-equivariant Schur reduction | retained: [`KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18.md`](KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18.md) |
| SQRTM | √m amplitude principle: positive parent M has principal square root M^(1/2) carrying √m amplitudes | retained: [`KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md`](KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md) |
| Substep4 | AC_φλ remains the explicit identification residual on hw=1 | retained-bounded: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md) |
| RouteF | Yukawa Casimir-difference lemma blocked by 4 barriers (one of the 8 prior attacks) | retained: [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (anchor-only at
  end, clearly marked).
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- **NO new axioms** (Probe 6's promise was to test whether expanding
  the operator class derives A1 without new axioms; any new
  primitive would require explicit user approval and is not proposed
  here)
- **NO new admitted_context_inputs introduced.** This probe operates
  strictly within the existing retained-content surface.

## The structural lemmas at issue (Hypotheses A, B, C)

**Hypothesis A:** drop Hermiticity. C_3-equivariant complex circulant:
```
Y = a·I + b·C + c·C²,    a, b, c ∈ ℂ    (6 real DOF)
```

**Hypothesis B:** squared mass matrix:
```
M = Y† Y    where Y is a complex circulant
```

**Hypothesis C:** operator-on-operator action: `C_3` acts on M_3(ℂ) by
conjugation `A → U A U†`; A1-condition emerges in the full operator
algebra.

**Question:** Does any of these expansions FORCE the A1 condition
`|b|²/a² = 1/2` (or its 6-DOF analog) from retained content alone?

## Theorem (Probe 6 bounded obstruction)

**Theorem.** On A1+A2 + retained CL3_SM_EMBEDDING + retained
gauge-selection + retained C_3-equivariance + retained
KoideCone-algebraic-equivalence + retained positive-parent-axis
+ retained SchurInheritance + admissible standard linear-algebra:

```
None of Hypotheses A, B, C closes A1 from retained content alone.
Five independent structural observations each verified
numerically in the paired runner.

  (B-collapse) M = Y† Y collapses 6 DOF (Y) → 3 DOF (M); lands
               back in the prior Hermitian sub-class.
  (A-trap)     6-DOF complex circulant makes A1 MORE compatible
               (codim-1 in 6D vs codim-1 in 3D), not MORE forced.
  (C-identity) M_3(ℂ) C_3-conjugation-invariant subspace =
               circulants; no new structure beyond R1.
  (Positivity) Positivity of M COMPATIBLE with A1 only for
               some δ (not all); not a forcing principle.
  (Anstaz-fit) The Hermitian sub-class is the correct operator
               class for stating A1 — expanding does not help.

Therefore the "wrong-operator-class" hypothesis fails as a closure
path for A1. The A1 admission count is UNCHANGED.
```

**Proof.** Each observation is verified independently in the paired
runner; combining them establishes that no derivation chain from
retained content reaches A1 via any of the three operator-class
expansions.

### Observation 1 (Hypothesis B collapse)

For Y = a·I + b·U + c·U² with `a, b, c ∈ ℂ`, compute
M = Y† Y. Using `U† = U⁻¹ = U²` (since U is the cyclic 3×3 permutation,
U³ = I), expand:
```
M = (āI + b̄U² + c̄U)(aI + bU + cU²)
  = (|a|² + |b|² + |c|²)·I
  + (āb + c̄a + b̄c)·U
  + (āc + b̄a + c̄b)·U²
```

Setting α = |a|² + |b|² + |c|² (real), β = āb + c̄a + b̄c (complex), one
sees the U² coefficient is exactly β̄. So:
```
M = α·I + β·U + β̄·U²
```
which is **Hermitian circulant** (3 real DOF: α, Re(β), Im(β)).

The 6 real DOF in Y collapse to 3 real DOF in M. The squared-mass
matrix lands in EXACTLY the 3-DOF Hermitian sub-class the 8 prior
attacks already worked on. Hypothesis B does NOT escape that class.

The runner verifies this collapse with explicit numerical
constructions and decomposition checks.

### Observation 2 (Hypothesis A "more DOF" trap)

The general 6-DOF complex circulant Y has a moduli space ℂ³ (with
overall scale, ℂ×CP² ≅ ℝ × ℝ⁵). Imposing the A1-analog condition
`|b|²/|a|² = 1/2` (or the more natural `|β|²/α² = 1/2` after passing
to M = Y†Y) is a SINGLE real equation. So the A1-condition surface
has codimension 1 in 6 real DOF — i.e., dimension 5.

In the 3-DOF Hermitian sub-class, the same A1 condition has
codimension 1 — dimension 2.

Both are codim-1. Neither is FORCED. But the 6-DOF case has
**strictly more freedom**, hence A1 is even more compatible with
arbitrary configurations (and even less forced) than in the 3-DOF
case. Random parametric scans (5000 samples in the runner) confirm
that A1 ratios span a wide range with `mean ≈ 0.25`, `std ≈ 0.20`,
and only ~0.7% of samples land within 1% of A1.

This is the "more DOF doesn't help" trap explicitly flagged in the
task: expanding from 3 to 6 real DOF gives MORE freedom, not LESS.
A1 needs to be FORCED by structure, not just COMPATIBLE with it.

### Observation 3 (Hypothesis C identity)

C_3 acts on M_3(ℂ) (9-dim complex algebra) by conjugation
A → U A U†. Standard character decomposition:
```
M_3(ℂ) ≅ 3·trivial ⊕ 3·ω ⊕ 3·ω̄
```
The trivial isotypic (C_3-conjugation-invariant) subspace is
3-dimensional over ℂ, equivalently 6-dim over ℝ — exactly the
complex circulants `span{I, U, U²}`. The Hermitian sub-block of this
is the 3-real-dim Hermitian circulants — exactly the Brannen ansatz
target.

So Hypothesis C reduces to the **same circulant class** already
captured in R1 of `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE`. No
new structure emerges.

The runner verifies the dimension count via explicit C_3-projection
of the 9 standard basis matrices E_{ij}: rank(P) = 3, matching
dim(span{I, U, U²}) = 3.

### Observation 4 (Positivity not a forcing principle)

For Hermitian circulant H = a·I + b·U + b̄·U² with `a ∈ ℝ`, `b ∈ ℂ`,
let `δ = arg(b)`. Eigenvalues:
```
λ_k = a + 2|b|·cos(δ + 2πk/3),    k = 0, 1, 2
```

A1 condition: `|b|/a = 1/√2` (i.e., `|b|²/a² = 1/2`).

For `δ = 0`: cosines = (1, -1/2, -1/2). λ_min = a - |b| = a(1 - 1/√2) > 0
(positive definite).

For `δ = π/3`: cosines = (1/2, 1/2, -1). λ_min = a - 2|b| = a(1 - √2) < 0
(NOT positive definite).

For `δ = π/12` (Brannen neutrino phase): one eigenvalue ≈ 0
(critical / massless boundary).

So A1 is COMPATIBLE with positivity for some δ but INCOMPATIBLE for
others. Positivity does NOT force A1. The A1 ratio sits at the
positivity-boundary for some δ — a "near-critical" structural fact
already noted in the existing positive-parent obstruction note —
but this critical structure is not a positive forcing principle.

The runner verifies all three δ regimes numerically.

### Observation 5 (Brannen ansatz is the correct class for A1)

The Brannen / Rivero ansatz `√m_k = v_0(1 + √2·cos(δ + 2πk/3))` is
the spectral form of the **Hermitian sub-class** at the A1 ratio.
The 3-DOF Hermitian-circulant family is exactly the class in which
this spectral form is naturally stated.

Expanding to:
- Hypothesis A (6-DOF complex): introduces complex eigenvalues that
  are NOT physical masses (must be real positive).
- Hypothesis B (M = Y†Y): collapses back to 3-DOF Hermitian (Obs 1).
- Hypothesis C (operator-on-operator): same 3- or 6-DOF circulant
  class (Obs 3).

Therefore the tested operator-class expansions do not rescue A1; the
failures of the 8 prior attacks (Routes A, D, E, F + Probes 1-4)
cannot be attributed to these natural wrong-operator-class criticisms.
They reflect a genuine structural absence of forcing principle for A1
across the checked C_3-equivariant operator classes on retained content.

### Combined verdict

The five observations combine to: **no operator-class expansion
opens a closure path for A1.** The 8 prior attack failures are
structural, not artifacts. A1 remains a load-bearing non-axiom step
on the Brannen circulant lane.

## Why this is a sharpened obstruction, not just a negative result

Probe 6 is informative because:

1. It **rules out** a specific class of "wrong assumption" criticisms
   ("the Brannen ansatz might be too restrictive"). Future re-attempts
   on A1 cannot appeal to "wider operator class" without first
   addressing Observations 1-5.

2. It **establishes** that the squared-mass-matrix structure (which
   IS the standard QFT framing for Yukawa observables) automatically
   lives in the prior 3-DOF Hermitian sub-class. So routes through
   `M = Y†Y` add no new structural freedom.

3. It **clarifies** that positivity, while structurally interesting
   (A1 sits at the criticality boundary), is not a forcing principle
   for A1.

4. It **confirms** that the 8 prior attack failures (Routes A, D, E,
   F + Probes 1-4) are not class-restriction artifacts. The negative
   result is intrinsic to the C_3-equivariant operator landscape on
   retained content.

5. It **sharpens the open frontier**: any future positive A1 closure
   must supply EITHER (a) a new retained primitive that breaks
   C_3-equivariance with controlled / charged-lepton-specific
   covariance, OR (b) a structurally new bridge across sectors
   (gauge ↔ flavor) not present in retained content, OR (c) explicit
   user-approved A3-class admission. The "wider operator class"
   route is now closed.

## What this closes

- **Probe 6 negative closure** (bounded obstruction). Three
  operator-class hypotheses (complex circulant, M = Y†Y,
  operator-on-operator) all blocked by five independent structural
  observations.
- **Sharpens the "Brannen ansatz wrong class?" question**: prior
  status was "untested speculative criticism." This note demonstrates
  that none of the three natural class expansions opens a closure path;
  the tested class criticism does not explain the A1 obstruction.
- **Sister-route implications**: confirms the Route A, D, E, F and
  Round-2 obstruction pattern is not a class-restriction artifact; the
  "wider class" criticism is now formally answered.
- **Squared-mass-matrix framing audited**: even the standard QFT
  framing M = Y†Y collapses to the same 3-DOF Hermitian class. No
  hidden structural freedom in that framing.

## What this does NOT close

- A1 admission count is unchanged. A1 remains a load-bearing
  non-axiom step on the Brannen circulant lane.
- Routes A (Koide-Nishiura quartic), D (Newton-Girard), E
  (Kostant Weyl-vector), and the other Round-2 probes are handled by
  their own companion obstruction notes; this note only closes the
  operator-class expansion criticism.
- Charged-lepton Koide closure remains a bounded observational-pin
  package (status from
  [`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
  unchanged).
- AC_φλ residual (substep 4) is unaffected.
- L3a trace-surface bounded obstruction status unchanged.
- Existing positive-parent / square-root amplitude / full-lattice
  Schur inheritance theorems retain their content; this probe
  complements rather than supersedes them.
- This note does NOT propose any new axiom, primitive, or
  admitted_context_inputs. It operates strictly within the existing
  retained-content surface.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| Hypothesis B collapse | Construct (a, b, c) ∈ ℂ³ with Y = aI+bU+cU² such that Y†Y is NOT in the Hermitian-circulant subspace — refutes Obs 1. |
| Hypothesis A "more DOF" trap | Identify a structural principle (from retained content alone) that forces A1 in 6-DOF complex circulants but not in 3-DOF Hermitian circulants — refutes Obs 2. |
| Hypothesis C identity | Construct a M_3(ℂ) C_3-conjugation-invariant subspace not equal to span{I, U, U²} — refutes Obs 3. |
| Positivity not forcing | Demonstrate that positivity of M = Y†Y FORCES |β|²/α² = 1/2 in retained content — refutes Obs 4. |
| Numerical anchor | Falsified if charged-lepton Koide Q deviates significantly from 2/3 in updated PDG; representative anchor values give Q = 0.666661 (sub-0.001% match). |

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is the negative Probe 6 boundary:
expanding the operator class beyond Hermitian C_3-equivariant
circulants does not open a closure path for A1, blocked by the five
observations above unless a new C_3-breaking primitive or new
cross-sector bridge is supplied.

No new admissions are proposed. A1 remains unchanged at its prior
load-bearing non-axiom status on the Brannen circulant lane. The
independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The "Brannen ansatz might be wrong operator class" hypothesis is answered: NO — three natural class expansions all fail. |
| V2 | New derivation? | The "Hypothesis B collapse" lemma (M = Y†Y of complex circulant is automatically Hermitian circulant) is new structural content with explicit algebraic proof and numerical verification. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) Hypothesis B collapse, (ii) Hypothesis A "more DOF" trap, (iii) Hypothesis C identity, (iv) positivity not-forcing, (v) Brannen-class fit. |
| V4 | Marginal content non-trivial? | Yes — the explicit α = |a|² + |b|² + |c|² and β = āb + c̄a + b̄c formulas (via Y†Y expansion), plus the parametric scan showing A1 is measure-zero in 6D, are new computational content not present in prior Routes/Probes. |
| V5 | One-step variant? | No — the operator-class question is structurally distinct from the convention/category mismatch arguments of Routes A-F. Probe 6 attacks a different angle: whether the working operator class has been wrongly chosen. |

**Source-note V1-V5 screen: pass for bounded-obstruction audit
seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of Routes A-F or Probes 1-4. The operator-class
  question (whether the Hermitian sub-class is wrongly chosen) is
  structurally distinct from the convention/category/cancellation
  arguments of those prior attacks.
- Identifies NEW STRUCTURAL CONTENT: the explicit M = Y†Y collapse
  formula (Obs 1), the dimension count in 6-DOF moduli (Obs 2), the
  M_3(ℂ) C_3-conjugation projection rank (Obs 3), and the
  positivity-vs-A1 phase analysis (Obs 4).
- Sharpens the "wider operator class" criticism from open speculation
  to closed-negatively, with a clear list of what would be required
  to reopen it.
- Provides explicit numerical counterexamples and parametric scans
  that demonstrate the free-parameter status of the 6-DOF (a, b, c)
  in C_3-equivariant complex circulants.

## Cross-references

- A1 derivation status (parent): `KOIDE_A1_DERIVATION_STATUS_NOTE.md`
- Existing Brannen ansatz / Hermitian-class derivation: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Route F bounded obstruction (sister): [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
- A3 Route 1 (C_3-breaking dynamics): [`A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md`](A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md)
- Positive-parent axis obstruction: [`KOIDE_POSITIVE_PARENT_AXIS_OBSTRUCTION_NOTE_2026-04-18.md`](KOIDE_POSITIVE_PARENT_AXIS_OBSTRUCTION_NOTE_2026-04-18.md)
- Full-lattice Schur inheritance: [`KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18.md`](KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18.md)
- √m amplitude principle: [`KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md`](KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md)
- Charged-lepton Koide-cone algebraic equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- One-Higgs gauge selection: [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md)
- Direct Ward-free Yukawa no-go: [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md)
- Substep 4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- CL3 SM embedding: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Higher-order structural theorems: [`HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)
- MINIMAL_AXIOMS: `MINIMAL_AXIOMS_2026-05-03.md`

## Validation

```bash
python3 scripts/cl3_koide_a1_probe_operator_class_2026_05_08_probe6.py
```

Expected output: structural verification of (i) Hermitian sub-class
sanity, (ii) Hypothesis A complex-circulant 6-DOF non-forcing,
(iii) Hypothesis B M = Y†Y collapse to Hermitian circulant,
(iv) Hypothesis C operator-on-operator identity with R1 class,
(v) positivity not a forcing principle, (vi) parametric scan
A1 measure zero in 6D, (vii) falsifiability anchor (PDG values,
anchor-only), (viii) bounded-obstruction theorem statement.

Total: 40 PASS / 0 FAIL.

Cached: [`logs/runner-cache/cl3_koide_a1_probe_operator_class_2026_05_08_probe6.txt`](../logs/runner-cache/cl3_koide_a1_probe_operator_class_2026_05_08_probe6.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  specifically applies the "consistency equality is not derivation"
  rule. The 1/2 = 1/2 numerical coincidence between A1 and various
  group-theoretic targets is not loaded in this note; the focus is
  whether wider operator-class structure FORCES A1 from retained
  content, and the answer is NO across all three hypotheses.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim that "the Brannen ansatz is the wrong operator
  class" by examining the action-level identification of the operator
  class itself, not just algebra. The answer is that the squared-mass
  matrix M = Y†Y, which is the standard QFT framing for fermion
  observables, AUTOMATICALLY lands in the Brannen sub-class — so the
  Brannen ansatz IS the right class.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction; the
  parent A1 admission remains at its prior bounded status. No
  retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: the operator-class
  question is structurally distinct from prior Routes/Probes. The
  five observations (B-collapse, A-trap, C-identity, positivity,
  Brannen-class fit) are substantive new structural content with
  explicit algebraic and numerical verifications.
- `feedback_compute_speed_not_human_timelines.md`: the note
  characterizes what new content WOULD be needed to reopen the
  hypothesis (new C_3-breaking primitive, cross-sector bridge, or
  user-approved A3 admission), not how-long-it-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  a multi-angle attack (five independent structural observations)
  on a single load-bearing structural hypothesis (operator-class
  expansion), with sharp PASS/FAIL deliverables in the runner.
- `feedback_review_loop_source_only_policy.md`: deliverable matches
  the review-loop source-only pattern: (a) source theorem note in
  docs/, (b) paired runner in scripts/, (c) cached output in
  logs/runner-cache/. No output-packets, lane promotions, synthesis
  notes, or working "Block" notes.
