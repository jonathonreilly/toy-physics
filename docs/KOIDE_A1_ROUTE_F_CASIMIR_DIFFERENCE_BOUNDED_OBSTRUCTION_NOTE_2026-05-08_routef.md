# Koide A1 Route F — Yukawa Casimir-Difference Bounded Obstruction

**Date:** 2026-05-08
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Route F closure attempt for
the A1 √2 equipartition admission on the charged-lepton Koide lane.
**Status:** source-note proposal for a negative Route F closure —
shows that the candidate structural lemma `|b|²/a² = T(T+1) − Y²`
cannot be derived from retained Cl(3)/Z³ content. Four independent
structural barriers each block the proposed identity. The A1
admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-a1-route-f-casimir-difference-20260508
**Primary runner:** [`scripts/cl3_koide_a1_route_f_casimir_difference_2026_05_08_routef.py`](../scripts/cl3_koide_a1_route_f_casimir_difference_2026_05_08_routef.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_route_f_casimir_difference_2026_05_08_routef.txt`](../logs/runner-cache/cl3_koide_a1_route_f_casimir_difference_2026_05_08_routef.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit lane
has full authority to retag, narrow, or reject the proposal.

## Question

`KOIDE_A1_DERIVATION_STATUS_NOTE.md`
identifies "Route F" (Yukawa Casimir-difference identity) as the
**strongest axiom-native candidate** for closing the A1 √2
equipartition admission. The proposed structural lemma is:

> `|b|² / a²  =  T(T+1) − Y²` for Yukawa-doublet participants

If proven, this would give axiom-native A1 from:
  - Cl⁺(3) ≅ ℍ ⟹ T(T+1) = 3/4 (retained CL3_SM_EMBEDDING_THEOREM)
  - ω pseudoscalar ⟹ Y² = 1/4 (retained, L hypercharge in PDG conv)
  - Casimir-difference lemma ⟹ |b|²/a² = 1/2 (proposed)
  - ⟹ A1 (Frobenius equipartition) is forced

Existing runner `scripts/frontier_koide_a1_yukawa_casimir_identity.py`
verifies the **numerical match** 1/2 = 3/4 − 1/4 with 9/9 PASS,
confirming that L doublet and Higgs UNIQUELY satisfy the identity
within the SM.

**Question:** Can the structural lemma `|b|²/a² = T(T+1) − Y²` be
**derived** from retained Cl(3)/Z³ content alone — no empirical
loading, no new axioms?

## Answer

**No.** The lemma cannot close from retained content alone. Four
independent structural barriers each independently block the proposed
derivation. The 1/2 = 1/2 numerical match between the two sides is a
coincidence between quantities defined in independent sectors of the
framework, not a structural identity that admits derivation.

The four barriers (each verified numerically in the paired runner):

1. **Convention dependence.** The identity `T(T+1) − Y² = 1/2` holds
   only in the modern PDG convention `Q = T_3 + Y` (with Y_L = -1/2).
   In the SU(5)-style convention used by the framework's retained
   `CL3_SM_EMBEDDING_THEOREM` (Y_L = -1, Y_H = +1), the same
   computation gives `T(T+1) − Y² = 3/4 − 1 = -1/4`, NOT 1/2. A
   genuine structural identity must be convention-invariant; this one
   is not.

2. **Free Yukawa coefficients.** Per retained
   `CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`,
   one-Higgs gauge selection determines that `Y_e` is an arbitrary
   3×3 complex matrix. C_3-equivariance (Route 1 obstruction) further
   narrows it to the circulant form `Y = aI + bU + b̄U^{-1}`, but
   `a` and `b` remain FREE parameters. No retained gauge or group
   constraint fixes their ratio. Counterexamples (`a=1, b=1`,
   `a=1, b=0`, etc.) all satisfy the retained constraints while
   violating A1.

3. **Sector orthogonality.** The SU(2)_L doublet (where `T(T+1) = 3/4`
   lives) is a 2-dim representation. The hw=1 sector (where the
   C_3-circulant `aI + bU + b̄U^{-1}` lives) is a 3-dim space carrying
   the C_3[111] cycle on the three generations. These are
   ORTHOGONAL sectors in the framework: the SU(2)_L Casimir scalar
   acts trivially on generation indices (gauge symmetry commutes with
   flavor). No retained theorem provides a structural map linking the
   gauge-Casimir to the generation-space flavor-coefficient ratio.

4. **Category mismatch.** LHS `|b|²/a²` is a ratio of *operator
   coefficients* in a Hermitian decomposition; it is invariant under
   uniform rescaling `(a,b) → (λa, λb)` but not under independent
   rescaling. RHS `T(T+1) − Y²` is a *group-theoretic scalar*
   independent of any operator structure. Equating two objects from
   different mathematical categories requires a structural map (a
   normalization principle that fixes how operator coefficients
   inherit gauge-Casimir values). No retained theorem supplies such a
   map.

The combined picture: **Route F is structurally barred**. The 1/2 = 1/2
match is a numerical coincidence of independently-defined values, not
a derivation. Closing A1 via this route would require either (a) a new
retained primitive supplying the gauge-to-flavor normalization map,
(b) explicit user-approved A3-class admission, or (c) an alternative
structural lemma not based on the Casimir-difference numerology.

## Setup

### Premises (A_min for Route F closure attempt)

| ID | Statement | Class |
|---|---|---|
| A1 | Cl(3) local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | Z³ spatial substrate | framework axiom; same source |
| Embed | Cl⁺(3) ≅ ℍ → SU(2)_L; ω pseudoscalar → U(1)_Y; Y_L, Y_H fixed | retained: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) |
| GS | One-Higgs gauge selection: Y_e is arbitrary 3×3 complex matrix | retained: [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md) |
| WardFree | No direct Ward lift forces y_τ; Y_e remains free 3×3 | retained: [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bU + b̄U^{-1}` | retained: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| Equiv | Any derived operator from C_3-symmetric primitives is C_3-equivariant | retained: [`A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md`](A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md) Step 2 |
| 3GenObs | hw=1 BZ-corner triplet has M_3(C) algebra; C_3[111] cycles corners | retained-bounded: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Substep4 | AC_φλ remains the explicit identification residual on hw=1 | retained-bounded: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md) |
| KoideAlg | Koide Q = 2/3 ⟺ a₀² = 2|z|² ⟺ |b|²/a² = 1/2 (algebraic) | retained: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| RouteF_RHS | `T(T+1) − Y² = 1/2` numerically holds for L, H in PDG conv | retained: existing 9/9 runner [`scripts/frontier_koide_a1_yukawa_casimir_identity.py`](../scripts/frontier_koide_a1_yukawa_casimir_identity.py) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (anchor-only at
  end, clearly marked per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)).
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- **NO new axioms** (Route F's promise was axiom-native; any A3-class
  admission requires explicit user approval and is not proposed here)
- NO admitted SM Yukawa-coupling pattern as derivation input

## The structural lemma at issue

**Proposed lemma (Route F):**
```
|b|² / a²  =  T(T+1) − Y²    on circulant Hermitian on hw=1 ≅ ℂ³
```
where:
- `(a, b)` are the coefficients of the circulant decomposition
  `H = aI + bU + b̄U^{-1}` (a real, b complex), forced on hw=1 by
  C_3-equivariance.
- `T = 1/2`, `Y = -1/2` (PDG conv) are the SU(2)_L isospin and
  U(1)_Y hypercharge labels of the lepton-doublet L (also of the
  Higgs H with Y = +1/2).
- `T(T+1) − Y²` evaluates to `3/4 − 1/4 = 1/2` in PDG conv; this
  matches the A1 target value `|b|²/a² = 1/2`.

**The runner [`scripts/frontier_koide_a1_yukawa_casimir_identity.py`](../scripts/frontier_koide_a1_yukawa_casimir_identity.py) verifies the NUMERICAL VALUE of the RHS (9/9 PASS), but does NOT prove the structural identity LHS = RHS.** The proposed lemma is an
identification claim, not yet derived. This note investigates whether
that derivation is possible from retained content.

## Theorem (Route F bounded obstruction)

**Theorem.** On A1+A2 + retained CL3_SM_EMBEDDING + retained
gauge-selection + retained C_3-equivariance + retained
KoideCone-algebraic-equivalence + admissible standard math machinery:

```
The structural lemma

  |b|² / a²  =  T(T+1) − Y²

cannot be derived from retained Cl(3)/Z³ content alone. Four
independent structural barriers each block the lemma:

  (B1) Convention dependence: 1/2 vs -1/4 under different Y conventions.
  (B2) Free Yukawa coefficients: a, b are free parameters.
  (B3) Sector orthogonality: SU(2)_L doublet (2-dim) and hw=1
       generation triple (3-dim) are orthogonal sectors.
  (B4) Category mismatch: operator-coefficient ratio vs
       group-theoretic scalar require a normalization map not
       supplied by retained content.

Therefore Route F closure of A1 is structurally barred under the
stated retained-content surface. The A1 admission count is unchanged.
```

**Proof.** Each barrier is verified independently in the paired runner;
combining them establishes that no derivation chain from retained
content reaches `|b|²/a² = T(T+1) − Y²`.

### Barrier 1: Convention dependence

The retained `CL3_SM_EMBEDDING_THEOREM.md` Section E uses the
SU(5)-style convention `Q = T_3 + Y/2`, with `Y_L = -1`, `Y_H = +1`,
`Y_q = +1/3`, `Y_{eR} = -2`, etc. In this convention:

```
T(T+1) − Y²  =  3/4 − 1²  =  -1/4    (lepton doublet, framework conv)
```

The same physical particle has `Y = -1/2` in the PDG convention
`Q = T_3 + Y`, where the identity gives `+1/2`. These are NOT
inconsistent statements about physics — they are DIFFERENT conventions
for labeling the same quantum number. But a *structural identity*
must be invariant under such relabeling.

The fact that the proposed lemma's RHS `T(T+1) − Y²` takes different
*numerical values* under different (equivalent) conventions
demonstrates that the equation `|b|²/a² = T(T+1) − Y²` is not
convention-invariant in the form proposed.

To make the identity convention-invariant, one would need to express
the RHS in terms of physical quantities (e.g., electric charge `Q`,
or weak isospin third component `T_3`, or the ratio `g_Y²/g_2²` of
gauge couplings) — and then derive `|b|²/a²` from those. The Route F
proposal as stated does not do this; it asserts the convention-
dependent value `1/2`.

The runner verifies `T(T+1) − Y² ∈ {-1/4, 1/2}` under the two
conventions while the same physical quantum numbers underlie both.

### Barrier 2: Free Yukawa coefficients

The retained `CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`
establishes that the gauge-allowed charged-lepton Yukawa is

```
- Y_e_{αβ} L̄_L^α H e_R^β + h.c.
```

with `Y_e` an **arbitrary 3×3 complex matrix in flavor space**.
Gauge selection alone does not determine any matrix entry.

C_3-equivariance (Route 1 obstruction
[`A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md`](A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md))
narrows `Y_e` to the circulant form `Y = aI + bU + b̄U^{-1}` on the
hw=1 generation sector, but `a` and `b` REMAIN FREE PARAMETERS.

The runner constructs explicit counterexamples that satisfy all
retained constraints but violate A1:

| (a, b) | `|b|²/a²` | Hermitian | C_3-equivariant | A1? |
|---|---|---|---|---|
| `(1.0, 0.3+0j)` | 0.09 | ✓ | ✓ | ✗ |
| `(1.0, 0.7+0.4j)` | 0.65 | ✓ | ✓ | ✗ |
| `(1.0, 1.0)` | 1.00 | ✓ | ✓ | ✗ |
| `(1.0, 0.0)` | 0.00 | ✓ | ✓ | ✗ (degenerate) |

Since `T(T+1) − Y²` has a single fixed value (1/2 in PDG conv) but
`|b|²/a²` ranges freely over the moduli space of retained-compatible
circulants, no derivation chain can force the equality from retained
content.

### Barrier 3: Sector orthogonality

The SU(2)_L doublet representation is 2-dim: `L = (ν_L, e_L)^T`
carrying `T = 1/2`, `T_3 = ±1/2`. The Casimir `T(T+1) = 3/4` is a
SCALAR on this 2-dim space.

The hw=1 generation triple is 3-dim: it carries the C_3[111] cycle
on three corner states `(c_1, c_2, c_3)`, and the C_3-equivariant
Hermitian operators are circulants on this 3-dim space.

These are **orthogonal mathematical sectors** in the framework:

- SU(2)_L acts trivially on generation indices (gauge symmetry
  commutes with flavor).
- The C_3 cycle acts trivially on doublet indices.
- Tensor product structure: full state space = doublet ⊗ generation,
  but operators that preserve gauge symmetry are diagonal on doublet
  index (acting as scalars there), and operators that respect the
  C_3 cycle are circulants on generation index.

The Casimir `T(T+1)` lives entirely in the doublet sector (a scalar
multiplier on the 2-dim space). The circulant coefficients `(a, b)`
live entirely in the generation sector. There is no retained theorem
that maps the doublet-sector scalar to the generation-sector
operator-coefficient ratio.

The runner verifies the dimensional mismatch (`dim(doublet) = 2 ≠ 3 =
dim(hw=1)`) and the action-triviality (`T(T+1)` acts as a scalar
multiplier on flavor sector, leaving `(a, b)` free).

### Barrier 4: Category mismatch

The two sides of the proposed lemma are mathematical objects of
different categories:

- **LHS** `|b|²/a²`: a ratio of operator coefficients in the
  decomposition `H = aI + bU + b̄U^{-1}`. It is dimensionless and
  invariant under uniform rescaling `(a,b) → (λa, λb)`, but it is
  NOT invariant under independent rescaling of `a` alone or `b`
  alone. The value depends on the *operator content* of `H` (and
  thus on its physical interpretation).

- **RHS** `T(T+1) − Y²`: a group-theoretic scalar derived from
  representation labels. It depends only on the SU(2)_L × U(1)_Y
  representation `(T, Y)`, not on any operator structure. It is
  state-independent.

To equate LHS and RHS, one needs a **normalization principle**: a
rule that fixes how the operator-coefficient ratio inherits a value
from gauge-Casimir labels. The Route F proposal does not supply such
a principle.

For comparison, the retained `C_τ = T(T+1) + Y² = 1` theorem
([`KOIDE_EXPLICIT_CALCULATIONS_NOTE.md`](KOIDE_EXPLICIT_CALCULATIONS_NOTE.md)
Section "Deliverable 2") DOES have such a normalization: the Casimir
sum `C_τ` is the coefficient of a specific 1-loop self-energy
diagram, where the `T(T+1)` and `Y²` pieces correspond to
gauge-boson exchange diagrams (`W±`, `W_3`, `B`) with explicit
Feynman-rule coefficients. The Casimir SUM is normalized by the
diagrammatic computation.

For the Casimir DIFFERENCE, no analogous diagrammatic principle
exists. The "difference" appears in chiral anomaly cancellation
relations, but those produce CONSISTENCY CONDITIONS (sum-vanishing
constraints), not amplitude-coefficient values.

The runner verifies the rescaling-invariance asymmetry of LHS and
notes the absence of a retained normalization principle for the
Casimir difference.

## Why the 1/2 = 1/2 numerical match is a coincidence

Within the SM, the values `T(T+1) − Y² = 1/2` (PDG conv, for L and H)
are tightly constrained by SM gauge structure. The value `1/2` is an
arithmetic consequence of `T = 1/2` and `Y² = 1/4` for the lepton
doublet — fixed by SM phenomenology, not by the retained framework
axioms.

The value `|b|²/a² = 1/2` (Brannen equipartition) is required to
algebraically force Koide `Q = 2/3`, which is observed in PDG
charged-lepton masses to high precision. This is a CONSEQUENCE of
the observed mass pattern, not a derivable structural identity.

So both sides equal 1/2 because:
- LHS = 1/2 is required to fit observed Koide Q = 2/3 (empirical)
- RHS = 1/2 is fixed by SM gauge structure of lepton doublet
  (textbook/empirical SM content)

Neither side is derived from Cl(3)/Z³ axioms. They match because they
both encode information about SM structure — but that information was
input, not derived. The numerical match is therefore evidence that
the framework is consistent with SM phenomenology, not evidence of an
axiom-native derivation.

This is a Type-I admission per
`feedback_consistency_vs_derivation_below_w2.md`: "consistency
equality is not derivation."

## Counterfactual: alternative SM extensions

The runner constructs alternative hypothetical multiplets that ALSO
satisfy `T(T+1) − Y² = 1/2`:

- Hypothetical exotic `T=1/2, Y=+1/2` multiplet (matches Higgs,
  re-derivative within SM; same value)
- Hypothetical BSM `T=1, Y² = 3/2` multiplet (different
  representation, same identity value)

If `1/2 = T(T+1) − Y²` were a structural Cl(3)/Z³ output, exactly
one SM particle (or a tightly-controlled family) would have this
value. Instead, the value `1/2` is achieved by an INFINITE family
of group-theoretic representations (any `(T, Y)` with `T(T+1) - Y² =
1/2`). The "uniqueness within SM" of Route F's RHS is an artifact of
SM particle content, not a structural prediction.

## Comparison to prior work

| Prior closure attempt | Status | Comment |
|---|---|---|
| Route A (Koide-Nishiura U(3) quartic) | companion bounded obstruction | trace-based 4th-order; Wilson-coefficient ratio unforced |
| Route B (Clifford torus on S³) | does not match Koide cone | 45° latitude vs equator |
| Route C (AS Lefschetz cot²) | parallel numeric identity | 2/3 = 2/3 coincidence |
| Route D (Newton-Girard) | companion bounded obstruction | trace-poly form; 6 = n(n+1)/2 coefficient unforced |
| Route E (A_1 Weyl-vector / Kostant) | companion bounded obstruction | `|ρ_{A_1}|² = 1/2` matches but no structural map |
| Route F (Yukawa Casimir-difference) | **THIS NOTE: bounded obstruction** | **four-barrier negative closure** |
| Numerical match runner (Apr 2026, 9/9 PASS) | establishes RHS arithmetic | does NOT establish structural lemma |

This note **complements** the existing Route F numerical-match runner
by establishing that the structural lemma cannot be derived even
though the numerical match holds.

## What this closes

- **Route F negative closure** (bounded obstruction). Four
  independent structural barriers verified.
- **Sharpens the "candidate" status**: prior status was "open
  candidate lemma — would close A1 if proved." This note demonstrates
  the lemma cannot close from retained content. Future re-attempts
  must supply at least one of: (a) gauge-to-flavor normalization
  principle, (b) cross-sector bridge theorem, (c) convention-
  invariant reformulation.
- **Sister-route implications**: Route F should not be cited as an
  axiom-native closure path going forward; companion Route A, D, and E
  notes close their own candidate mechanisms negatively.
- **Audit-defensibility**: explicit numerical counterexamples to the
  proposed lemma, removing it from the "axiom-native A1" candidate
  list at retained-grade.

## What this does NOT close

- A1 admission count is unchanged. A1 remains a load-bearing
  non-axiom step on the Brannen circulant lane.
- Routes A (Koide-Nishiura quartic), D (Newton-Girard), and E
  (Kostant Weyl-vector) are handled by their own companion
  bounded-obstruction notes.
- Charged-lepton Koide closure remains a bounded observational-pin
  package (status from
  [`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
  unchanged).
- The numerical-match runner
  [`scripts/frontier_koide_a1_yukawa_casimir_identity.py`](../scripts/frontier_koide_a1_yukawa_casimir_identity.py)
  retains its 9/9 PASS for the *numerical* check. This note does NOT
  retract that — it adds a structural-derivation analysis that the
  numerical check by itself does not provide.
- AC_φλ residual (substep 4) is unaffected.
- L3a trace-surface bounded obstruction status unchanged.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| Convention dependence (B1) | Demonstrate a convention-invariant reformulation that gives 1/2 in all gauge conventions — refutes B1. |
| Free Yukawa coefficients (B2) | Derive a retained constraint that fixes `|b|²/a² = 1/2` from gauge-only data — refutes B2. |
| Sector orthogonality (B3) | Construct a retained operator that maps SU(2)_L Casimir-difference to hw=1 circulant coefficient ratio — refutes B3. |
| Category mismatch (B4) | Supply a retained normalization principle that fixes operator-coefficient inheritance from group-theoretic scalars — refutes B4. |
| Numerical match (anchor) | Falsified if charged-lepton Koide Q deviates significantly from 2/3 in updated PDG; the representative anchor values used by the paired runner give Q = 0.666661 (sub-0.001% match). |

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is the negative Route F boundary: the
Yukawa Casimir-difference structural lemma is blocked by convention
dependence, free Yukawa coefficients, sector orthogonality, and category
mismatch unless a new gauge-to-flavor normalization map or cross-sector
bridge theorem is supplied.

No new admissions are proposed. A1 remains unchanged at its prior
load-bearing non-axiom status on the Brannen circulant lane. The
independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The "Route F is the strongest axiom-native A1 candidate" claim is sharpened from "open candidate lemma" to "structurally barred under retained content; needs explicit gauge-to-flavor bridge." |
| V2 | New derivation? | The four-barrier obstruction argument applied to Route F is new structural content. Prior status note enumerated the candidate but did not prove the obstruction. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) convention-dependence, (ii) free Yukawa, (iii) sector orthogonality, (iv) category mismatch, and (v) the four-barrier conjunction. |
| V4 | Marginal content non-trivial? | Yes — the convention-dependence finding (1/2 vs -1/4 under SU(5) vs PDG conventions) is non-obvious from prior notes and directly challenges Route F. |
| V5 | One-step variant? | No — the four-barrier argument is structural across multiple sectors (gauge, flavor, convention, normalization), not a relabel of any prior Koide route. |

**Source-note V1-V5 screen: pass for bounded-obstruction audit
seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of prior Koide routes. The four-barrier obstruction
  argument applied to Route F is new structural content with explicit
  numerical counterexamples and convention-dependence analysis.
- Identifies a NEW STRUCTURAL OBSTRUCTION (Barrier 1 = convention
  dependence) not present in the prior `KOIDE_A1_DERIVATION_STATUS_NOTE`
  treatment of Route F.
- Sharpens the "strongest axiom-native candidate" claim from open to
  closed-negatively, with a clear list of what would be required to
  reopen it.
- Provides explicit numerical counterexamples that demonstrate the
  free-parameter status of `(a, b)` — these were not present in prior
  Route F discussions.

## Cross-references

- A1 derivation status (parent): `KOIDE_A1_DERIVATION_STATUS_NOTE.md`
- Existing Route F numerical runner: [`scripts/frontier_koide_a1_yukawa_casimir_identity.py`](../scripts/frontier_koide_a1_yukawa_casimir_identity.py)
- Circulant character derivation: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide-cone algebraic equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- CL3 SM embedding: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
- Koide explicit calculations (C_τ = 1): [`KOIDE_EXPLICIT_CALCULATIONS_NOTE.md`](KOIDE_EXPLICIT_CALCULATIONS_NOTE.md)
- One-Higgs gauge selection: [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md)
- Direct Ward-free Yukawa no-go: [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md)
- A3 Route 1 (sister route): [`A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md`](A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md)
- Substep 4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Physical lattice baseline: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Higher-order structural theorems: [`HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)
- MINIMAL_AXIOMS: `MINIMAL_AXIOMS_2026-05-03.md`

## Validation

```bash
python3 scripts/cl3_koide_a1_route_f_casimir_difference_2026_05_08_routef.py
```

Expected output: structural verification of (i) numerical match
(reproduces 9/9 from existing Route F runner, restricted to the
identity arithmetic itself), (ii) Barrier 1 convention dependence,
(iii) Barrier 2 free Yukawa coefficients with counterexamples,
(iv) Barrier 3 sector orthogonality, (v) Barrier 4 category mismatch,
(vi) alternative-multiplet counterexamples to uniqueness, (vii)
falsifiability anchor (PDG values, anchor-only), (viii)
bounded-obstruction theorem statement. Total: 25 PASS / 0 FAIL.

Cached: [`logs/runner-cache/cl3_koide_a1_route_f_casimir_difference_2026_05_08_routef.txt`](../logs/runner-cache/cl3_koide_a1_route_f_casimir_difference_2026_05_08_routef.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  specifically applies the "consistency equality is not derivation"
  rule. The numerical match `1/2 = 1/2` is a consistency equality,
  not a structural Casimir-difference identity, and the proposed
  lemma cannot load-bear A1 closure on this basis.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim that "T(T+1) − Y² is the Casimir difference"
  by showing that the action-level identification (operator
  coefficient ratio = group-theoretic scalar) is not a derivable
  identity — it requires a normalization map that retained content
  does not supply.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction; the
  parent A1 admission remains at its prior bounded status. No
  retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: the four-barrier
  argument with explicit counterexamples and convention analysis is
  substantive new structural content, not a relabel of prior Koide
  routes.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  (A, D, E) characterized in terms of WHAT additional content would
  be needed (gauge-to-flavor bridge, normalization principle,
  cross-sector theorem), not how-long-they-would-take.
- `feedback_hostile_review_semantics.md`: trace-ratio derivations
  (proposed `|b|²/a² = T(T+1) − Y²`) are stress-tested at the
  action-level identification, not just algebra. The arithmetic
  works; the action-level identification fails the four-barrier
  semantic challenge.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  a multi-angle attack (four independent barriers) on a single
  load-bearing structural lemma, with sharp PASS/FAIL deliverables in
  the runner.
- `feedback_physics_loop_corollary_churn.md`: this is not corollary
  churn — it is a closure attempt on a previously-open candidate
  identified as "strongest axiom-native" and its proper structural
  evaluation. The negative result is informative.
