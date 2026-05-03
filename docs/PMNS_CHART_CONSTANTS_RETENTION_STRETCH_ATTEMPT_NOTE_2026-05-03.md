# PMNS Chart Constants γ, E₁, E₂ Retention — Stretch Attempt with Named Obstructions

**Date:** 2026-05-03
**Type:** stretch_attempt (output type c)
**Claim scope:** documents a worked stretch attempt at retiring
the three PMNS chart constants γ = 1/2, E₁ = √(8/3),
E₂ = √(8)/3 = 2√2/3 from support-grade to retained, where these
constants enter cycle 12's Path B leptogenesis ε_1 prediction
through cp1 = -2γE₁/3 = -2√6/9 and cp2 = +2γE₂/3 = 2√2/9.
Outcome: partial structural identification for γ via sharp
selector projector + c_odd, partial structural identification
for E₁ and E₂ via Frobenius dual + spectral match, but absolute
retention blocked by the audited_conditional status of the
upstream c_odd, v_even, and weak-even-swap-reduction theorems.

**Status:** stretch attempt, audit-lane ratification required for
any retained-grade interpretation. This is not a closing
derivation.

**Runner:** [`scripts/frontier_pmns_chart_constants_retention.py`](./../scripts/frontier_pmns_chart_constants_retention.py)

**Authority role:** sharpens cycle 12's Obstruction O1 (PMNS
chart constants γ, E₁, E₂ are support-grade) into three named
sub-obstructions A, B, C with specific load-bearing premises.

## A_min (minimal allowed premise set)

- (P1, retained) `DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16`:
  γ = 1/2, E₁ = √(8/3), E₂ = √(8)/3 are exact constants on a
  nonempty H-side source surface, with explicit positive-Hermitian
  witness. **Retained** (audited_clean, td=35).
- (P2, audited_conditional) `DM_NEUTRINO_CODD_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15`:
  c_odd = +1 from sharp selector projector + bosonic normalization
  on additive CPT-even scalar generator W[J].
- (P3, audited_conditional) `DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15`:
  v_even = (√(8/3), √(8)/3) from Frobenius dual representatives
  F₁ = (1/2)T_δ + (1/4)T_ρ and F₂ = A_op + (1/4)b_op - (1/2)c_op
  - (1/2)d_op, with spec(F₁) = ±√(3/8) and spec(F₂) = ±3/√8
  isospectral to scaled copies of Z_row = diag(1,-1) on the
  exact 2-row weak source factor.
- (P4, audited_conditional) `DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15`:
  τ_+ = τ_E + τ_T = 1 from swap-even projector P_+ = (1/2)(I +
  P_swap) on 2-row weak source factor.
- (P5, retained-bounded prior cycle) Cycle 12's
  `EPSILON1_FROM_CP_CHAIN_STRETCH_ATTEMPT_NOTE_2026-05-03`:
  cp1/cp2 = -√3 is exact and forbidden-import-clean from chart
  constants (γ, E₁, E₂) = (1/2, √(8/3), √(8)/3).
- (P6, framework-internal) Cl(3) Dynkin index for spin-1/2 rep =
  1/2 (admitted Lie-algebra fact, role-labeled).
- (P7, framework-internal) SU(2) fundamental representation
  Casimir = 3/4 (admitted Lie-algebra fact, role-labeled).

## Forbidden imports

- **PDG values for neutrino masses, PMNS angles**: NOT consumed.
- **m_top, sin²θ_W, η_obs**: NOT consumed.
- **Literature numerical comparators**: NOT consumed (Lie-algebra
  facts are admitted-context structural facts, role-labeled).
- **y_0 (G_weak)**: NOT consumed (cycle 12's O2).
- **α_LM (plaquette MC)**: NOT consumed (cycle 12's O3).
- **Cycle 12's cp1/cp2 = -√3 ratio**: ADMITTED AS PRIOR-CYCLE
  INPUT (retained-bounded from cycle 12 Path B).
- **PMNS support-grade infrastructure**: ADMITTED AS BOUNDED INPUT.
- **No fitted selectors**.
- **No same-surface family arguments**.

## Background: where γ, E₁, E₂ enter

From cycle 12's Path B (`DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15`):

```text
ε_1 = |(1/(8π)) y_0² (cp1 · f_23 + cp2 · f_3) / K_00|
```

with `cp1 = -2γE₁/3` and `cp2 = +2γE₂/3` exact heavy-basis CP
tensor channels. Substituting (γ, E₁, E₂) = (1/2, √(8/3),
√(8)/3) gives cp1 = -2√6/9 and cp2 = 2√2/9 with structural
ratio cp1/cp2 = -√3 (cycle 12 verified).

The structural origin of each chart constant traces upstream to:

```text
γ      = c_odd · a_sel
E₁     = √(8/3) · τ_+
E₂     = (√8/3) · τ_+
```

with c_odd, a_sel, v_even = (√(8/3), √8/3), τ_+ all derived in
audited_conditional theorems P2-P4 above. The retained
source-surface theorem P1 proves these constants pull back to a
nonempty H-side surface with explicit positive Hermitian witness.

## Worked attempt

### Sub-attempt A: γ = 1/2

#### Trivial-origin candidates (each numerically matches but is structurally falsified)

**Candidate A1: SU(2) Dynkin index for fundamental rep = 1/2.**
Numerical: T(1/2) = 1/2 ✓. But γ does NOT appear in any retained
SU(2) gauge sector identity; it appears in the `c_odd a_sel`
neutrino-sector decomposition, which is a Cl(3) (not SU(2))
sector. So the numerical match is coincidental — γ is not the
SU(2) Dynkin index in any structurally-identified role.

**Candidate A2: Cl(3) staggered chirality projection (1 - γ_5)/2
= 1/2 trace.** Numerical: 1/2 ✓. But the Cl(3) chirality
projection enters the framework via cycle 06's Majorana
null-space and cycle 04's hypercharge structure, NOT via the
neutrino source-amplitude decomposition. The (1-γ_5)/2 trace =
1/2 emerges as a generic projector trace, not specifically as γ
in the neutrino sector.

**Candidate A3: Casimir of SU(2) fundamental = 3/4.** Numerical
3/4 ≠ 1/2 ✗. Falsified.

**Candidate A4: Cl(3) Pauli matrix amplitude in σ_3/2 = 1/2.**
Same as Candidate A1 trivially.

#### Genuine structural origin (audited_conditional)

From P2 `DM_NEUTRINO_CODD_BOSONIC_NORMALIZATION_THEOREM`:

```text
S_cls = diag(0, 0, 1, -1)        (reduced selector generator)
T_gamma = [[0,0,-i],[0,0,0],[i,0,0]]  (DM odd triplet generator)
spec(S_cls) = {0, 0, +1, -1}
spec(T_gamma) = {0, +1, -1}
```

These differ only by null multiplicity. Under the unique additive
CPT-even bosonic source-response generator W[J] = log|det(D+J)| -
log|det D|, the null multiplicity drops out after subtracting the
zero-source baseline. Both sources satisfy W = log|1 - j²/m²| on
scalar baseline m·I, hence:

```text
|c_odd| = 1, c_odd = +1 (source-oriented branch convention)
```

From P5 (cycle 12) cp1/cp2 = -√3 forces the relative sign and
magnitude of γ, E₁, E₂ as a coupled system: alternative γ values
would only preserve cp1/cp2 = -√3 if E₁, E₂ are scaled
proportionally. So γ = 1/2 is fixed via two routes:
- (a) Sharp selector projector P_nu = diag(1,0) centered against
  (P_nu + P_e)/2 gives a_sel = 1/2 (P3 in cycle 12 lineage).
- (b) c_odd = +1 from spectral isospectrality (above).

Hence γ = c_odd · a_sel = (+1) · (1/2) = 1/2.

#### Sub-A outcome: PARTIAL CLOSING DERIVATION

The structural origin of γ = 1/2 is identified as the sharp
selector projector centering amplitude. The closing-derivation
gap is:
- The "sharp resolved branch projector vs soft weighted mixture"
  choice is the load-bearing premise. P_nu = diag(1,0) is
  motivated by the source-oriented branch but has no single-axiom
  derivation from minimal primitives without the bosonic-bilinear
  selector principle.
- Trivial Lie-algebra candidates (SU(2) Dynkin = 1/2) numerically
  match by coincidence; the structural identification is sharp
  selector centering, not gauge-sector Dynkin.

### Sub-attempt B: E₁ = √(8/3) ≈ 1.633

#### Trivial-origin candidates

**Candidate B1: Casimir of some retained representation.**
For SU(2) fundamental Casimir = 3/4, SU(3) fundamental = 4/3,
SU(2) adjoint = 2. None equals 8/3 = 2.667. Numerical mismatch.
However, 8/3 appears in cycle 04's `Tr[Y³] = -16/9` with
16/9 / 6 = 8/27 (not 8/3). So the 8/3 numerator is NOT directly
from cycle 04's hypercharge cubic.

**Candidate B2: 2 × (4/3) = 8/3 from twice the SU(3) fundamental
Casimir.** Numerical match. But the framework's neutrino sector
does NOT involve SU(3) color, so this is structurally
inappropriate.

**Candidate B3: Reciprocal of SU(2) fundamental Casimir × const:
1/(3/4) = 4/3, not 8/3.** Falsified.

#### Genuine structural origin (audited_conditional)

From P3 `DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM`:

The active Hermitian basis {A_op, b_op, c_op, d_op, T_δ, T_ρ}
is Frobenius-orthogonal. The Riesz/Frobenius dual of E₁ = δ + ρ
on this basis is

```text
F₁ = (1/2) T_δ + (1/4) T_ρ
```

with `<H, F₁>_F = δ + ρ = E₁` (Frobenius inner product).

Eigenvalue spectrum:

```text
spec(F₁) = {-√(3/8), 0, +√(3/8)}
```

so F₁ is isospectral to √(3/8) Z_row (where Z_row = diag(1,-1)
is the unique traceless Hermitian on the exact 2-row weak source
factor).

Under the bosonic normalization W[J], on scalar baselines this
gives:

```text
√(3/8) E₁ = τ_+
```

Hence E₁ = √(8/3) τ_+. With τ_+ = 1 from P4 (sharp swap-even
projector P_+ = (1/2)(I + P_swap) on 2-row factor with
(τ_E, τ_T) = (1/2, 1/2)):

```text
E₁ = √(8/3)
```

#### Sub-B outcome: STRETCH ATTEMPT WITH PARTIAL

The structural origin of E₁ = √(8/3) is identified as the
Frobenius dual eigenvalue magnitude √(3/8) reciprocal, with
τ_+ = 1 from sharp swap-even projector. The closing-derivation
gap is:
- Frobenius orthogonality of basis {A_op, b_op, c_op, d_op,
  T_δ, T_ρ} is load-bearing; this is an audited_conditional
  framework claim, not retained.
- τ_+ = 1 inherits from `DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM`
  (audited_conditional).
- The Frobenius dual coefficient pattern (1/2, 1/4) for F₁ in
  terms of (T_δ, T_ρ) is exact algebra given the basis
  orthogonality, but the choice of basis is the upstream
  obstruction.

### Sub-attempt C: E₂ = √(8)/3 = 2√2/3 ≈ 0.943

#### Magnitude analysis

Note E₁ ≈ 1.633 and E₂ ≈ 0.943 have **different** magnitudes.
The prompt's mention of E₂² - E₁² = 0 is incorrect arithmetic:
E₁² = 8/3 ≈ 2.667 and E₂² = 8/9 ≈ 0.889, so E₂² - E₁² = 8/9 -
8/3 = 8/9 - 24/9 = -16/9 ≈ -1.778. Each constant has its own
structural origin via different Frobenius dual representative.

#### Trivial-origin candidates

**Candidate C1: 2/√(something).** 2√2/3 = 2 × √2/3 = √(8)/3.
Numerical: ≈ 0.9428. No standard Casimir equals 8/9.

**Candidate C2: 1 - 1/9 = 8/9 = E₂².** Numerical match for E₂²
but structurally arbitrary (no retained primitive yields 1/9 in
this role).

**Candidate C3: SU(2) fundamental dim²/9 = 4/9 ≠ 8/9.** Falsified.

#### Genuine structural origin (audited_conditional)

From P3 `DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM`:

The Frobenius dual of E₂ = A + b - c - d on the orthogonal basis
is

```text
F₂ = A_op + (1/4) b_op - (1/2) c_op - (1/2) d_op
```

with `<H, F₂>_F = A + b - c - d = E₂` (note: the coefficient
arithmetic on the basis Frobenius norms gives the (1, 1/4, -1/2,
-1/2) coefficient pattern; see P3 for derivation details).

Eigenvalue spectrum:

```text
spec(F₂) = {-3/√8, 0, +3/√8}
```

so F₂ is isospectral to (3/√8) Z_row.

Under the bosonic normalization W[J]:

```text
(3/√8) E₂ = τ_+
```

Hence E₂ = √8/3 · τ_+ = √8/3 (with τ_+ = 1 again).

Numerically: E₂ = √8/3 = 2√2/3 ≈ 0.9428 ✓.

#### Sub-C outcome: STRETCH ATTEMPT WITH PARTIAL

Same load-bearing premises as Sub-B: Frobenius orthogonality of
the active Hermitian basis + τ_+ = 1 from sharp swap-even
projector. The closing-derivation gap is identical: both
audited_conditional, not retained.

### Cross-constraint via cycle 12's cp1/cp2 = -√3 ratio

Substituting (γ, E₁, E₂):

```text
cp1/cp2 = (-2γE₁/3) / (+2γE₂/3) = -E₁/E₂ = -√(8/3) / (√8/3)
        = -√(8/3) · 3/√8 = -3/√3 = -√3
```

So cp1/cp2 = -E₁/E₂ depends ONLY on the ratio E₁/E₂ = √3 (γ
factors out!). Counterfactually:

- **Doubling γ → 1**: cp1/cp2 unchanged (γ cancels). Falsifies
  the structural origin "γ from a_sel = 1/2 specifically" via
  the cp1/cp2 ratio alone, BUT the absolute scale of cp1 (via
  Path B's ε_1 formula) is sensitive to γ.
- **E₁ → 1, E₂ → 1**: cp1/cp2 → -1, breaking cycle 12's verified
  -√3 ratio.
- **E₁ → √(8/3), E₂ → 1**: cp1/cp2 → -√(8/3) ≈ -1.633, breaking
  the verified ratio.
- **E₁ → 1, E₂ → √(8)/3**: cp1/cp2 → -3/√8 ≈ -1.061, breaking
  the verified ratio.
- **(E₁, E₂) → (k·√(8/3), k·√(8)/3) for any k**: cp1/cp2
  preserved at -√3. So the cp1/cp2 = -√3 ratio FORCES E₁/E₂ =
  √3 but does NOT fix the absolute magnitudes.

The absolute magnitudes are fixed by τ_+ = 1 from P4
(audited_conditional), giving the Sub-B and Sub-C closing
arguments above.

### Synthesis: three sub-attempts, three named obstructions

Sub-A: γ = 1/2 has PARTIAL closing derivation via sharp selector
projector P_nu = diag(1,0) → a_sel = 1/2 + c_odd = +1 → γ = 1/2.
Trivial Lie-algebra candidates (SU(2) Dynkin = 1/2) match
numerically by coincidence; the structural identification is
sharp selector centering. Load-bearing premise: bosonic-bilinear
selector principle (audited_conditional via c_odd theorem).

Sub-B: E₁ = √(8/3) has STRETCH ATTEMPT WITH PARTIAL via
Frobenius dual F₁ = (1/2)T_δ + (1/4)T_ρ → spec ±√(3/8) →
isospectral to √(3/8) Z_row → E₁ = √(8/3) τ_+ = √(8/3). Trivial
Casimir candidates fail to match 8/3 in any retained sector.
Load-bearing premise: Frobenius orthogonality of active
Hermitian basis (audited_conditional via v_even theorem) + τ_+ =
1 (audited_conditional via swap-reduction theorem).

Sub-C: E₂ = √(8)/3 has STRETCH ATTEMPT WITH PARTIAL via
Frobenius dual F₂ = A_op + (1/4)b_op - (1/2)c_op - (1/2)d_op →
spec ±3/√8 → isospectral to (3/√8) Z_row → E₂ = √(8)/3 τ_+ =
√(8)/3. Same load-bearing premises as Sub-B.

## Named Obstructions

### Obstruction A: γ from sharp selector projector (audited_conditional → retained)

The sharp resolved branch projector P_nu = diag(1,0) (vs soft
weighted mixture) is the load-bearing premise for a_sel = 1/2.
The c_odd theorem (`DM_NEUTRINO_CODD_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15`)
is **audited_conditional**, not retained.

**Specific repair target**: derive the sharp resolved branch
projector choice from minimal Cl(3) on Z³ axiom + the
bosonic-bilinear selector principle as a retained framework
output. Connects to retained Koide γ-orbit infrastructure
(`Q_Koide = 2/3`, `SELECTOR² = 2/3`) but the bridge from Koide
character to the specific sharp projector is currently bounded.

### Obstruction B: E₁ from Frobenius dual (audited_conditional → retained)

The Frobenius orthogonality of basis {A_op, b_op, c_op, d_op,
T_δ, T_ρ} is the load-bearing premise for F₁ = (1/2)T_δ +
(1/4)T_ρ. The v_even theorem (`DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15`)
is **audited_conditional**, not retained. Additionally, τ_+ = 1
inherits from `DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15`
(audited_conditional).

**Specific repair target**: derive Frobenius orthogonality of
the active Hermitian basis from minimal primitives (Cl(3) on Z³)
and promote v_even to retained. This is a substantial multi-step
algebraic chain in the framework's neutrino-sector Hermitian
chart.

### Obstruction C: E₂ from Frobenius dual (audited_conditional → retained)

Same as Obstruction B (shared upstream theorems).

**Specific repair target**: same as B (single repair retires both
B and C since they share the v_even + swap-reduction upstream).

## What this claims

- (P1) The three chart constants γ = 1/2, E₁ = √(8/3),
  E₂ = √(8)/3 have identified structural origins via sharp
  selector projector + Frobenius dual + bosonic normalization,
  with the upstream theorems (c_odd, v_even, swap-reduction) all
  audited_conditional.
- (P2) The chart constants pull back to a nonempty H-side
  source surface with explicit positive-Hermitian witness via
  the **retained** `DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16`.
- (P3) Cross-constraint with cycle 12's cp1/cp2 = -√3 retained-
  bounded ratio forces E₁/E₂ = √3 but does NOT alone fix
  absolute magnitudes; absolute magnitudes are fixed by τ_+ = 1
  from audited_conditional swap-reduction.
- (P4) Three named sub-obstructions A, B, C with specific
  load-bearing premises and concrete repair targets.

## What this does NOT claim

- Does NOT close cycle 12's Obstruction O1 (PMNS chart
  constants support-grade) — sharpens it into three sub-
  obstructions.
- Does NOT promote γ, E₁, E₂ from support to retained on the
  current authority surface.
- Does NOT promote any author-side tier; audit-lane ratification
  required.
- Does NOT consume any PDG observed value as derivation input.
- Does NOT derive c_odd, v_even, or swap-reduction theorems from
  primitives — these remain audited_conditional upstream.

## Cited dependencies

- (P1, retained) `DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16`.
- (P2, audited_conditional) `DM_NEUTRINO_CODD_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15`.
- (P3, audited_conditional) `DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15`.
- (P4, audited_conditional) `DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15`.
- (P5, retained-bounded prior cycle)
  `EPSILON1_FROM_CP_CHAIN_STRETCH_ATTEMPT_NOTE_2026-05-03`
  (cycle 12: cp1/cp2 = -√3 ratio).
- (P6, audited_conditional) `DM_NEUTRINO_SOURCE_AMPLITUDE_THEOREM_NOTE_2026-04-15`
  (a_sel = 1/2, τ_E = τ_T = 1/2, τ_+ = 1).
- (Obstruction context)
  `PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21`
  (support, not retained — proposed selector laws delta·q_+ =
  Q_Koide and det(H) = E_2).
- (Cycle 12 parent)
  `EPSILON1_FROM_CP_CHAIN_STRETCH_ATTEMPT_NOTE_2026-05-03`
  (sharpens its Obstruction O1).
- (Lie-algebra context, admitted role-labeled) SU(2) Dynkin
  index for fundamental rep = 1/2; Casimir of SU(2) fundamental
  = 3/4; Cl(3) chirality projection trace = 1/2.

## Forbidden imports check

- η_obs not consumed.
- m_top not consumed.
- sin²θ_W not consumed.
- PDG neutrino mass values not consumed.
- PMNS angle observed values not consumed.
- y_0 (G_weak) not consumed (cycle 12 O2).
- α_LM (plaquette) not consumed (cycle 12 O3).
- cp1/cp2 = -√3 ratio: ADMITTED AS CYCLE-12 PRIOR-CYCLE INPUT.
- PMNS support-grade infrastructure: ADMITTED AS BOUNDED INPUT.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_pmns_chart_constants_retention.py`](./../scripts/frontier_pmns_chart_constants_retention.py)
verifies:

1. Numerical match: γ = 1/2, E₁ = √(8/3) ≈ 1.633,
   E₂ = √(8)/3 = 2√2/3 ≈ 0.943 to 14 digits.
2. **Sub-A (γ = 1/2) trivial-origin tests**: SU(2) Dynkin index =
   1/2 (matches numerically), Cl(3) chirality projection trace =
   1/2 (matches numerically), Casimir of SU(2) fundamental = 3/4
   (does NOT match — falsified).
3. **Sub-A genuine structural origin**: γ = c_odd · a_sel =
   (+1)(1/2) = 1/2 from sharp selector projector P_nu =
   diag(1,0) centered against (P_nu + P_e)/2.
4. **Sub-B (E₁ = √(8/3)) trivial-origin tests**: SU(2)
   fundamental Casimir = 3/4 (mismatch — falsified), SU(3)
   fundamental Casimir = 4/3 (mismatch — falsified), 2 × SU(3)
   Casimir = 8/3 (matches numerically but structurally
   inappropriate since neutrino sector has no SU(3) color).
5. **Sub-B genuine structural origin**: E₁ = √(8/3) τ_+ from
   Frobenius dual F₁ = (1/2)T_δ + (1/4)T_ρ with spec ±√(3/8),
   isospectral to √(3/8) Z_row, with τ_+ = 1.
6. **Sub-C (E₂ = √8/3) trivial-origin tests**: 1 - 1/9 = 8/9 =
   E₂² (matches numerically but no retained 1/9), no Casimir
   match.
7. **Sub-C genuine structural origin**: E₂ = √(8)/3 · τ_+ from
   Frobenius dual F₂ = A_op + (1/4)b_op - (1/2)c_op - (1/2)d_op
   with spec ±3/√8, isospectral to (3/√8) Z_row.
8. **Cross-constraint via cycle 12's cp1/cp2 = -√3**:
   - Verify cp1/cp2 = -E₁/E₂ = -√3 with current values.
   - Counterfactuals: E₁=E₂=1 → ratio = -1 (broken);
     E₁=√(8/3), E₂=1 → ratio = -√(8/3) (broken);
     E₁=1, E₂=√(8)/3 → ratio = -3/√8 (broken).
   - Uniform scaling (k·√(8/3), k·√(8)/3) preserves -√3.
9. **Eigenvalue verification**: spec(F₁) = ±√(3/8) and spec(F₂)
   = ±3/√8 verified numerically via 6×6 matrix eigendecomposition
   on Frobenius dual basis (with hermitian construction).
10. **τ_+ = 1 from sharp swap-even projector**: P_+ = (1/2)(I +
    P_swap) on 2-row factor → (τ_E, τ_T) = (1/2, 1/2) → τ_+ = 1.
11. **c_odd = +1 from spectral isospectrality**: spec(S_cls) =
    {0, 0, +1, -1} and spec(T_gamma) = {0, +1, -1} differ only
    by null multiplicity; bosonic normalization W[J] absorbs the
    null multiplicity.
12. **Counterfactual c_odd**: If c_odd = -1, then γ = -1/2,
    cp1 = +√6/9, cp2 = -2√2/9, ratio still = -√3 (sign flip).
    But the source-oriented branch convention fixes c_odd = +1.
13. **Counterfactual a_sel = 1**: If a_sel = 1 (full projector
    instead of centered), γ = 1, breaking cycle 12's Path B
    formula structure but preserving cp1/cp2 ratio.
14. **Counterfactual a_sel = 1/3**: Numerical mismatch, breaks
    sharp projector centering algebra.
15. **Three named obstructions** explicitly recorded with
    repair targets.
16. **Forbidden-import audit**: γ, E₁, E₂ structural origins
    traced to audited_conditional upstream theorems; PDG values
    NOT consumed; no fitted selectors.

## Cross-references

- [`EPSILON1_FROM_CP_CHAIN_STRETCH_ATTEMPT_NOTE_2026-05-03.md`](EPSILON1_FROM_CP_CHAIN_STRETCH_ATTEMPT_NOTE_2026-05-03.md) —
  cycle 12 parent; Obstruction O1 is sharpened by this PR.
- [`DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16.md`](DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16.md) —
  retained source-surface theorem (γ, E₁, E₂ on nonempty surface).
- [`DM_NEUTRINO_CODD_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_CODD_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md) —
  audited_conditional c_odd = +1 theorem.
- [`DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md) —
  audited_conditional v_even = (√(8/3), √(8)/3) theorem.
- [`DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md) —
  audited_conditional swap-reduction τ_+ = 1.
- [`DM_NEUTRINO_SOURCE_AMPLITUDE_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_SOURCE_AMPLITUDE_THEOREM_NOTE_2026-04-15.md) —
  audited_conditional source amplitude (a_sel = 1/2, τ_+ = 1).
- [`PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md`](PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md) —
  PMNS chart-constant support context (Obstruction O1 origin).
- [`KOIDE_GAMMA_ORBIT_SELECTOR_BRIDGE_NOTE_2026-04-18.md`](KOIDE_GAMMA_ORBIT_SELECTOR_BRIDGE_NOTE_2026-04-18.md) —
  Koide γ-orbit selector bridge (potential connection for Sub-A).
