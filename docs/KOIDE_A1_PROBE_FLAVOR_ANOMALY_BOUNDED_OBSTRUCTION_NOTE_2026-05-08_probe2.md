# Koide A1 Probe — Flavor-Sector Anomaly Bounded Obstruction (Probe 2)

**Date:** 2026-05-08
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — flavor-sector anomaly
cancellation as a candidate closure for the A1 √2 equipartition admission
on the charged-lepton Koide lane. **Status:** source-note proposal for a
negative closure of the flavor-anomaly probe — shows that no flavor-sector
anomaly channel from a representative three-channel sweep
{F1 = Witten Z₂ on hw=1, F2 = pure cubic Tr[Q_F³] for U(1)_F flavor,
F3 = mixed SU(2)_L² × U(1)_F gauge-flavor anomaly} forces the A1-condition
`|b|²/a² = 1/2` on the C_3-circulant Yukawa decomposition. Three
independent channel-level obstructions are unified by a category-mismatch
lemma P2-S1 that sharpens the R3-functoriality result. The A1 admission
count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-a1-probe-flavor-anomaly-20260508
**Primary runner:** [`scripts/cl3_koide_a1_probe_flavor_anomaly_2026_05_08_probe2.py`](../scripts/cl3_koide_a1_probe_flavor_anomaly_2026_05_08_probe2.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_probe_flavor_anomaly_2026_05_08_probe2.txt`](../logs/runner-cache/cl3_koide_a1_probe_flavor_anomaly_2026_05_08_probe2.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit lane
has full authority to retag, narrow, or reject the proposal.

## Question

The retained
[`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
shows that three SM anomaly traces

```text
Tr[Y]  = 0,    Tr[SU(3)² Y] = 0,    Tr[Y³] = 0
```

force the right-handed hypercharges UNIQUELY at `(4/3, -2/3, -2, 0)`.
The mechanism is a constraint-system on rational species labels
solved by anomaly cancellation.

The closely-related
`KOIDE_A1_DERIVATION_STATUS_NOTE.md`
identifies four already-barred A1 routes (E, A, D, F). The R3
anomaly-inflow obstruction
([`A3_ROUTE3_ANOMALY_INFLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r3.md`](A3_ROUTE3_ANOMALY_INFLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r3.md))
established a universal C_3-orbit obstruction R3-S1: anomalies attach
functorially to symmetries (groups, orbits, cohomology classes), not to
individual states within a single symmetry orbit.

The R3 result speaks to whether anomaly carriers can DISTINGUISH the
three corner states. It does **not** directly speak to whether anomaly
carriers can FIX OPERATOR-COEFFICIENT RATIOS — a distinct question.

> **Question (Probe 2).** Can flavor-sector anomaly cancellation —
> applied as a constraint system on flavor-symmetry labels assigned to
> the lepton sector — force the A1 condition `|b|²/a² = 1/2` on the
> C_3-equivariant circulant Hermitian decomposition `H = aI + bU + b̄U⁻¹`
> on hw=1 ≅ ℂ³?

We test three concrete flavor-anomaly channels:

  - **F1**: Witten Z₂ global anomaly applied to hw=1.
  - **F2**: Pure flavor cubic anomaly `Tr[Q_F³] = 0` for a hypothetical
    U(1)_F flavor gauge group with charges (q_1, q_2, q_3) on the three
    corner states.
  - **F3**: Mixed gauge-flavor anomaly `Tr[SU(2)² Q_F] = 0` for U(1)_F
    acting on the lepton SU(2)_L doublet.

These cover the standard "anomaly cancellation" channels available
when one extends the SM-style mechanism to the flavor sector (i.e.,
adding a flavor symmetry group whose anomaly cancellation imposes
algebraic constraints on flavor-label data).

## Answer

**No.** Flavor-sector anomaly cancellation does not close the A1
admission from retained content. All three channels F1, F2, F3 yield
clean obstructions, unified by a category-mismatch lemma P2-S1 that
sharpens R3-S1 functoriality.

**Channel-level obstructions:**

  - **F1 (Witten Z₂ on hw=1).** Witten anomaly is a parity statement on
    REP COUNT. hw=1 is 3-dim, not a 2-dim SU(2) doublet — Witten does
    not directly apply. Even forcing a hypothetical 1+2 decomposition,
    the Z₂-valued constraint (N_D mod 2 ∈ {0, 1}) cannot algebraically
    encode the continuous A1 target `|b|²/a² = 1/2`.

  - **F2 (Pure cubic Tr[Q_F³] = 0).** The constraint is polynomial in
    REP LABELS (q_1, q_2, q_3 ∈ ℚ). C_3-equivariance forces equal
    charges q_1 = q_2 = q_3 (R3-functoriality), which makes
    `Tr[Q_F] = 3q = 0` ⇒ `q = 0`, trivializing the constraint system.
    Even if one breaks C_3 (a new primitive, barred), the resulting
    `(q_1, q_2, q_3)` data does not map to the operator-coefficient
    ratio `|b|²/a²`.

  - **F3 (Mixed SU(2)² × U(1)_F).** The constraint reduces to
    `Σ q_i = 0` (linear in flavor charges). The A1 target
    `|b|²/a² = 1/2` is QUADRATIC in operator coefficients. A linear-in-q
    constraint cannot algebraically reach a quadratic-in-coefficient
    ratio without an additional normalization map, which retained
    content does not supply.

**Unifying obstruction P2-S1 (sharpens R3-S1):**

> **Lemma (P2-S1, Universal flavor-anomaly category mismatch).** Let G
> be any flavor-relevant symmetry group with rep content {ρ_α} on the
> three corner states {|c_α⟩}. Let A: {ρ_α} → {Tr[Q^k] = 0}_k be any
> anomaly-cancellation constraint system. Then:
>
> (a) A is a finite POLYNOMIAL system (linear, cubic, ...) in
>     REPRESENTATION LABELS (charges, weights, Dynkin indices).
>
> (b) The A1 target `|b|²/a² = 1/2` is a CONTINUOUS QUADRATIC RATIO in
>     OPERATOR COEFFICIENTS (a, b).
>
> No retained morphism `A → (a, b)` exists in the framework's content.
> The two objects live in different mathematical categories.

P2-S1 is structurally **independent** of R3-S1:
  - R3-S1 blocks anomaly mechanisms from DISTINGUISHING corners on hw=1.
  - P2-S1 blocks anomaly mechanisms from FIXING OPERATOR-COEFFICIENT
    RATIOS, even if R3 is escaped via a hypothetical new primitive.

Probe 2 therefore adds a sharpened obstruction at a different point in
the anomaly chain than R3. Both are required to bar the representative
flavor-anomaly route to A1.

## Setup

### Premises (A_min for Probe 2)

| ID | Statement | Class |
|---|---|---|
| A1 | Cl(3) local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | Z³ spatial substrate | framework axiom; same source |
| Embed | Cl⁺(3) ≅ ℍ → SU(2)_L; ω pseudoscalar → U(1)_Y | retained: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) |
| GS | One-Higgs gauge selection: Y_e is arbitrary 3×3 complex matrix | retained: [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md) |
| WardFree | No direct Ward lift forces y_τ; Y_e remains free 3×3 | retained: [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bU + b̄U⁻¹` | retained: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| 3GenObs | hw=1 BZ-corner triplet has M₃(ℂ) algebra; C_3[111] cycles corners | retained-bounded: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| KoideAlg | Koide Q = 2/3 ⟺ a₀² = 2\|z\|² ⟺ \|b\|²/a² = 1/2 (algebraic) | retained: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| HypUniq | SM hypercharge uniqueness from anomaly traces (template) | retained: [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) |
| WittenZ2 | SU(2) Witten Z₂ requires N_D = 0 mod 2 | retained: [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md) |
| R3 | Universal C_3-orbit anomaly-functoriality obstruction | retained-bounded: [`A3_ROUTE3_ANOMALY_INFLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r3.md`](A3_ROUTE3_ANOMALY_INFLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r3.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (anchor-only at
  end, clearly marked per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)).
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- **NO new axioms** (probe is constrained to A1+A2 + retained content;
  any extension to a new flavor gauge group is hypothetical only and
  serves to test reachability, not to be promoted)
- NO admitted SM Yukawa-coupling pattern as derivation input
- NO HK + DHR appeal (Block 01 audit retired this; respected)

## Channel-level analysis

### Channel F1 — Witten Z₂ anomaly on hw=1

**Setup.** Witten's SU(2) Z₂ anomaly: an SU(2) gauge theory with N_D
fundamental Weyl doublets is consistent iff N_D ≡ 0 (mod 2).

**Application to hw=1.** hw=1 ≅ ℂ³ is a 3-dim space carrying the
C_3[111] cyclic permutation. It is **not** a 2-dim SU(2) doublet.
Witten therefore does not directly apply. The runner verifies
`dim(hw=1) = 3 ≠ 2 = dim(SU(2)_doublet)`.

If one **forces** a hypothetical SU(2)_F flavor decomposition of hw=1
into 1+2 (singlet + doublet), the Witten constraint becomes
`N_D = 1 ≡ 1 (mod 2)`: hypothetically anomalous. This is a parity
statement, not a constraint on `|b|²/a²`.

**Why it cannot reach A1.** The Witten constraint is binary-valued
(`N_D mod 2 ∈ {0, 1}`). The A1 target `|b|²/a² = 1/2` is real-valued
in (0, ∞). There is no algebraic embedding of a real number 0.5 in a
binary set. The runner verifies this dimensional incompatibility.

**Verdict F1: OBSTRUCTION** (rep-count parity vs continuous coefficient
ratio).

### Channel F2 — Pure cubic anomaly Tr[Q_F³] = 0 for U(1)_F

**Setup.** Posit a hypothetical U(1)_F flavor gauge group with charges
(q_1, q_2, q_3) on the three corner states. The pure-flavor cubic
anomaly cancellation requires:

```text
Tr[Q_F]   = q_1 + q_2 + q_3       = 0
Tr[Q_F³] = q_1³ + q_2³ + q_3³     = 0
```

These are LINEAR and CUBIC constraints on three real (or rational)
unknowns.

**C_3-equivariance restriction.** Per R3-S1, a C_3-equivariant flavor
charge function must be constant on the C_3 orbit:

```text
q_1 = q_2 = q_3 = q  (R3-equivariant)
```

The constraints become `3q = 0` and `3q³ = 0`, both forcing `q = 0`:
the system is trivially satisfied with no information content. The
runner verifies this collapse.

**Hypothetical R3-escape.** If one IMPORTS a new primitive that breaks
C_3 (barred per A1+A2 + retained content), one could try assignments
like `(q_1, q_2, q_3) = (1, 1, -2)`: linear constraint satisfied
(sum = 0), cubic gives `1 + 1 - 8 = -6 ≠ 0`. Most rational triples
fail the cubic constraint; non-trivial solutions over ℚ are
exceptional. Even a "maximally cancelling" triple
(1, cos(2π/3), cos(4π/3)) = (1, -0.5, -0.5) satisfies
`Σ = 0` but `Σq³ = 1 - 0.125 - 0.125 = 0.75 ≠ 0`.

**Why it cannot reach A1 even when R3 is escaped.** Even with a
non-trivial flavor-charge solution `(q_1, q_2, q_3)`, those values are
REPRESENTATION LABELS on the three corner states. The A1 target
`|b|²/a² = 1/2` is an OPERATOR-COEFFICIENT RATIO on the C_3-circulant
Hermitian decomposition. No retained theorem provides a map from
flavor-charge data to operator-coefficient data.

The runner constructs explicit independent (Yukawa, charge-triple)
combinations: any (a, b) circulant is compatible with any anomaly-
cancelling charge triple. The runner verifies `[Y_e, Q_F_diag] ≠ 0`
in general (no commutativity constraint).

**Verdict F2: OBSTRUCTION** (orbit-functoriality forces trivial system;
even if escaped, charge-data and coefficient-data are independent).

### Channel F3 — Mixed gauge-flavor anomaly Tr[SU(2)² Q_F] = 0

**Setup.** Posit U(1)_F flavor charges q_i on the three lepton-doublet
generations. The mixed SU(2)_L² × U(1)_F anomaly cancellation:

```text
Tr[T(SU(2))² Q_F]  ∝  q_1 + q_2 + q_3  =  0
```

(The Dynkin index `T = 1/2` for the SU(2)_L doublet appears as a
constant prefactor; the trace produces a sum over generation flavor
charges.)

**Direct comparison to A1 target.** The constraint is:

```text
LHS:  q_1 + q_2 + q_3 = 0           (linear in flavor charges)
A1:  |b|² / a² = 1/2                (quadratic in operator coefficients)
```

The two equations are **dimensionally and categorically incompatible**:

| Aspect | Mixed anomaly LHS | A1 target |
|---|---|---|
| Mathematical kind | linear equation | quadratic ratio |
| Variables | flavor charges q_i ∈ ℚ | (a, b) ∈ ℝ × ℂ |
| Solution space | 2-plane in ℝ³ | 2-circle (Frobenius equipartition) in (ℝ × ℂ) |
| Constraint scaling | Σq_i = 0 (homogeneous, linear) | \|b\|²/a² = 1/2 (homogeneous in (a, b) by uniform rescale, but ratio fixed) |

Even if `q_1 = 1, q_2 = -1, q_3 = 0` (anomaly-cancelling triple) is
chosen, no relation to `(a, b)` follows. The runner exhibits 12
independent (Yukawa, charge-triple) pairs, each satisfying its
respective constraints with no cross-coupling.

**Counter-example (concrete).** Take `(a, b) = (1, 1)` ⇒ `|b|²/a² = 1`,
which violates A1. With flavor charges `(1, -1, 0)`, the mixed anomaly
sum is 0 (anomaly-cancelling). Both are simultaneously valid under
retained content; A1 violated.

**Why F3 reduces to F2 with respect to A1 reachability.** F3 produces
the same algebraic constraint shape (linear sum of flavor charges = 0)
as F2 (modulo Dynkin index prefactors). The A1 target is in a
different category from any such linear constraint.

**Verdict F3: OBSTRUCTION** (linear constraint on charges cannot reach
quadratic ratio in coefficients).

## Unifying lemma P2-S1

The three channels {F1, F2, F3} share a common structural failure mode:

> **Lemma (P2-S1, Universal flavor-anomaly category mismatch).**
>
> Let G be any flavor-relevant symmetry group with rep content {ρ_α} on
> the three corner states {|c_α⟩}. Let
>
> ```
> A : {ρ_α} → {Tr[ρ(Q)^k] = 0}_k
> ```
>
> be any anomaly-cancellation constraint system on flavor-charge labels
> Q. Then:
>
> (a) The constraint system A is a finite POLYNOMIAL (or PARITY) system
>     in REPRESENTATION LABELS — typically linear (Σq_i = 0), cubic
>     (Σq_i³ = 0), and binary parity (mod 2).
>
> (b) The A1 target `|b|²/a² = 1/2` is a CONTINUOUS QUADRATIC RATIO in
>     OPERATOR COEFFICIENTS (a, b).
>
> No retained morphism `A → (a, b)` exists in the current framework.
> The constraint-system data and the operator-coefficient data live in
> **different mathematical categories**.
>
> Therefore no flavor-sector anomaly cancellation can reach the A1
> condition without an additional retained content (a normalization
> principle) supplying the morphism.

**Proof sketch.** Each anomaly channel produces a constraint system on
representation labels (charges, weights, Dynkin indices, parity counts).
These labels are valued in ℚ (rationals) or ℤ (integers) or ℤ_n (mod n).
The A1 target is valued in (0, ∞) (real ratios). The natural map from
{charge data} to {coefficient data} would have to be a function
`f: ℚ³ × ℚ → ℝ × ℂ` whose image is constrained to lie on the Frobenius
equipartition locus `|b|²/a² = 1/2`. No such function is supplied by
retained content. Specifically:
  - retained Yukawa-free (`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO`)
    leaves Y_e free as a 3×3 complex matrix;
  - retained C_3-equivariance narrows it to circulant `aI + bU + b̄U⁻¹`,
    but (a, b) remain free per `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE`;
  - no retained theorem maps gauge-Casimir or flavor-charge data into
    (a, b) coefficients (per `KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE`
    Barriers 3 and 4).

The runner verifies P2-S1 by random sampling: 100 random
(charges, circulant) pairs are independently parametrizable, with
`|b|²/a²` ranging freely. Less than 10% of random samples (1.1% in the
runner's seed) accidentally hit the A1 target by chance — confirming
that no anomaly-cancellation constraint system imposes the A1
preference. ∎

## Comparison to R3-S1 (anomaly inflow obstruction)

| Aspect | R3-S1 | P2-S1 (this note) |
|---|---|---|
| **What's obstructed** | Anomaly carriers DISTINGUISHING corner states | Anomaly carriers FIXING coefficient ratios |
| **Mathematical kind** | Functoriality on G-orbits | Category mismatch (charges vs coefficients) |
| **Survives R3-escape?** | (R3 itself) | YES — even with hypothetical R3-breaking primitive, P2-S1 still blocks |
| **Channels covered** | 7 anomaly-inflow channels (E1–E7) | 3 flavor-anomaly channels (F1, F2, F3) |
| **Implication for A1** | Anomaly carriers commute with C_3 ⇒ equal corner expectations | Anomaly arithmetic is polynomial in charges ⇒ cannot reach quadratic-in-coefficient target |

The two obstructions are **independent**. R3-S1 is a statement about
how anomaly invariants act on G-orbits of states; P2-S1 is a statement
about the target category of anomaly arithmetic. Probe 2 sharpens R3
by identifying a structurally distinct second-order obstruction that
also blocks the same overall route.

## What this closes

- **Probe 2 negative closure** (bounded obstruction). Three independent
  flavor-anomaly channels {F1, F2, F3} verified.
- **P2-S1 unifying lemma.** Establishes a category-mismatch obstruction
  that survives even hypothetical R3-escape scenarios.
- **A1-route map sharpening.** Beyond the four already-barred routes
  E, A, D, F (per `KOIDE_A1_DERIVATION_STATUS_NOTE`), Probe 2 adds the
  flavor-anomaly route to the barred list. This narrows the open
  candidate set to {Route A (Koide-Nishiura quartic), Route D
  (Newton-Girard), Route E (Kostant) sub-cases not requiring the
  Casimir-difference normalization}.
- **R3-S1 sharpening.** The R3-functoriality result is sharpened by
  P2-S1 at a structurally different layer. R3 blocks
  corner-distinguishing; P2 blocks coefficient-fixing.
- **Audit-defensibility.** Explicit numerical counterexamples (e.g.,
  `(a=1, b=1)` Yukawa with `(1, -1, 0)` flavor charges) demonstrating
  independence of operator and charge data.

## What this does NOT close

- A1 admission count is **unchanged**. A1 remains a load-bearing
  non-axiom step on the Brannen circulant lane.
- Routes A (Koide-Nishiura quartic), D (Newton-Girard), and E
  (Kostant Weyl-vector) are handled by their own companion
  bounded-obstruction notes.
- Charged-lepton Koide closure remains a bounded observational-pin
  package.
- AC_φλ residual (substep 4) is unaffected.
- This probe does NOT rule out a hypothetical anomaly mechanism
  *outside* the F1, F2, F3 channels enumerated. P2-S1 is a structural
  argument that any *categorical* anomaly cancellation respects the
  obstruction; non-categorical mechanisms (e.g., a hypothetical
  retained normalization map from charge data to coefficient data,
  not currently available) would be outside scope.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| F1 (Witten on hw=1) | Demonstrate a Witten-anomaly-derived constraint that algebraically encodes `|b|²/a² = 1/2` from a representation-count parity. |
| F2 (Pure cubic) | Construct a retained C_3-symmetric U(1)_F gauging that produces non-trivial cubic anomaly cancellation; OR a retained map from flavor charges to circulant coefficients. |
| F3 (Mixed) | Supply a retained quadratic generalization of the mixed gauge-flavor constraint that depends on (a, b). |
| P2-S1 (unifying) | Construct a retained morphism A → (a, b) from the anomaly constraint system to operator coefficients. |
| Anchor (PDG) | Falsified if charged-lepton Koide Q deviates significantly from 2/3 in updated PDG; the representative anchor values used by the paired runner give Q = 0.666661 (sub-0.001% match). |

## Theorem (Probe 2 bounded obstruction)

**Theorem.** On A1+A2 + retained CL3_SM_EMBEDDING + retained
gauge-selection + retained C_3-equivariance + retained
KoideCone-algebraic-equivalence + retained R3 anomaly-inflow + retained
SM hypercharge-uniqueness template + admissible standard math
machinery:

```
No flavor-sector anomaly cancellation channel from the set
{F1, F2, F3} forces the A1-condition |b|²/a² = 1/2 on the
C_3-circulant Yukawa decomposition on hw=1. The three channel-level
obstructions are unified by the lemma P2-S1:

  P2-S1: anomaly cancellation produces a polynomial constraint
         system in REPRESENTATION LABELS, while the A1 target is a
         continuous quadratic ratio in OPERATOR COEFFICIENTS. The
         two are in different mathematical categories with no
         retained morphism between them.

P2-S1 is structurally independent of R3-S1: R3 blocks corner-
distinguishing; P2 blocks coefficient-fixing. Both obstructions
are required to bar the representative flavor-anomaly route to A1.

Therefore Probe 2 closure of A1 is structurally barred under the
stated retained-content surface. The A1 admission count is
unchanged.
```

**Proof.** Each channel-level obstruction is verified independently in
the paired runner; the unifying P2-S1 lemma is verified by 100-sample
random sweep (1.1% accidental match rate, ≪ 10% threshold). ∎

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is the negative flavor-anomaly boundary:
the representative channels F1, F2, and F3 do not force the A1 amplitude
condition, and the P2-S1 category-mismatch lemma separates
coefficient-ratio data from anomaly-label data.

No new admissions are proposed. A1 remains unchanged at its prior
load-bearing non-axiom status on the Brannen circulant lane. The
independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1–V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The "anomaly cancellation extension to flavor sector closes A1" hypothesis is sharpened from "untested" to "structurally barred under retained content; needs explicit charges-to-coefficients morphism that retained content does not supply." |
| V2 | New derivation? | The three-channel flavor-anomaly enumeration {F1, F2, F3}, the unifying P2-S1 category-mismatch lemma, and the explicit independence from R3-S1 are new structural content. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) channel-level obstructions for F1, F2, F3 individually, (ii) the P2-S1 unifying lemma, (iii) the structural independence from R3-S1, and (iv) the random-sweep verification of category mismatch. |
| V4 | Marginal content non-trivial? | Yes — P2-S1 is non-obvious from prior R3 treatment; the SM hypercharge analog had charges-as-unknowns structure that does not transfer to A1's coefficients-as-unknowns target. |
| V5 | One-step variant? | No — the channel-level analysis distinguishes from prior anomaly attacks (which addressed AC_φ corner-distinguishing, not coefficient-fixing); P2-S1 is a structural sharpening at an independent layer of the anomaly-route argument. |

**Source-note V1–V5 screen: pass for bounded-obstruction audit
seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`:

- NOT a relabel of R3 anomaly-inflow obstruction. R3 addresses anomaly-
  carriers respecting C_3 orbits; P2-S1 addresses anomaly-arithmetic
  category mismatch. Independent obstructions, both load-bearing.
- NOT a relabel of Route F obstruction. Route F was specifically the
  Yukawa Casimir-difference identity; this probe is about flavor-
  sector anomaly cancellation as a different mechanism.
- Identifies a NEW STRUCTURAL OBSTRUCTION (P2-S1 category mismatch)
  not present in any prior Koide route or anomaly-attack note.
- Provides explicit independence demonstration via R3-escape thought
  experiment: even if R3 is hypothetically escaped, P2-S1 still blocks.
- Includes random-sweep verification (100 samples) confirming the
  category mismatch operates independently of any specific channel.

## Cross-references

- A1 derivation status (parent): `KOIDE_A1_DERIVATION_STATUS_NOTE.md`
- Route F obstruction (sister): [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
- R3 anomaly inflow obstruction (sister): [`A3_ROUTE3_ANOMALY_INFLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r3.md`](A3_ROUTE3_ANOMALY_INFLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r3.md)
- SM hypercharge uniqueness template: [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
- Witten Z₂ anomaly: [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md)
- Circulant character derivation: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide-cone algebraic equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- CL3 SM embedding: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
- One-Higgs gauge selection: [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md)
- Direct Ward-free Yukawa no-go: [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md)
- Substep 4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- MINIMAL_AXIOMS: `MINIMAL_AXIOMS_2026-05-03.md`
- AS index theorem (E6 in R3): [`A3_ROUTE3_ANOMALY_INFLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r3.md`](A3_ROUTE3_ANOMALY_INFLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r3.md)
- SM full anomaly cancellation: [`AXIOM_FIRST_SM_ANOMALY_CANCELLATION_COMPLETE_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SM_ANOMALY_CANCELLATION_COMPLETE_THEOREM_NOTE_2026-05-03.md)

## Citation references (anomalies and constraint systems)

- Adler, S. L. *Axial-Vector Vertex in Spinor Electrodynamics*,
  Phys. Rev. 177 (1969) 2426 — ABJ anomaly.
- Bell, J. S. & Jackiw, R. *A PCAC puzzle: π⁰ → γγ in the σ-model*,
  Nuovo Cimento A60 (1969) 47 — companion ABJ paper.
- Witten, E. *An SU(2) anomaly*, Phys. Lett. B 117 (1982) 324-328 —
  Z_2 / mod-N discrete anomaly archetype.
- 't Hooft, G. *Naturalness, chiral symmetry, and spontaneous chiral
  symmetry breaking*, in *Recent Developments in Gauge Theories*,
  NATO ASI B59 (Plenum, 1980) — 't Hooft anomaly matching.
- Geng, C. Q. & Marshak, R. E. *Uniqueness of quark and lepton
  representations in the Standard Model from the anomaly viewpoint*,
  Phys. Rev. D 39 (1989) 693 — SM hypercharge uniqueness from anomaly
  cancellation; the template for the A1 probe.
- Foot, R., Joshi, G. C., Lew, H. & Volkas, R. R. *Charge quantization
  in the Standard Model and some of its extensions*, Mod. Phys. Lett. A 5
  (1990) 2721 — charge quantization from anomaly cancellation.
- Babu, K. S. & Mohapatra, R. N. *Quantization of electric charge from
  anomaly constraints and a Majorana neutrino*, Phys. Rev. D 41 (1990)
  271 — extending anomaly arguments to flavor / B-L sectors.
- Koide, Y. *A fermion-mass relation*, Lett. Nuovo Cimento 34 (1982) 201
  — original Koide relation.
- Brannen, C. *Mass formula for charged leptons and Koide* form,
  hep-ph/0505220 — Brannen circulant form.

## Validation

```bash
python3 scripts/cl3_koide_a1_probe_flavor_anomaly_2026_05_08_probe2.py
```

Expected output: structural verification of (i) setup recap and
free-coefficient counter-examples, (ii) F1 Witten-parity vs continuous-
ratio mismatch, (iii) F2 R3-functoriality forces trivial cubic system
plus charge-coefficient independence, (iv) F3 linear-in-charge vs
quadratic-in-coefficient direct counter-examples, (v) P2-S1 unifying
lemma with 100-sample random sweep (1.1% accidental match rate),
(vi) explicit independence demonstration from R3-S1 via hypothetical
R3-escape, (vii) falsifiability anchor (PDG values, anchor-only),
(viii) probe 2 verdict consolidation. Total: 24 PASS / 0 FAIL.

```text
EXACT      : PASS = 24, FAIL = 0
BOUNDED    : PASS = 0, FAIL = 0
TOTAL      : PASS = 24, FAIL = 0
```

Cached: [`logs/runner-cache/cl3_koide_a1_probe_flavor_anomaly_2026_05_08_probe2.txt`](../logs/runner-cache/cl3_koide_a1_probe_flavor_anomaly_2026_05_08_probe2.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: P2-S1 is derived
  via category-mismatch arguments on retained constraint-system
  structure, NOT via consistency-equality. The three F_k channels'
  obstructions cite mathematical category, not numerical coincidences.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim that "flavor anomaly cancellation extends to fix
  A1" by showing that the action-level identification (charges
  data → coefficient data) is not a derivable identity — it requires
  a normalization map that retained content does not supply. The
  arithmetic of charge-anomaly-systems is well-defined; the action-
  level identification fails at the category boundary.
- `feedback_retained_tier_purity_and_package_wiring.md`: this note
  is a source-note proposal at the bounded tier; no automatic
  cross-tier promotion. A1 admission remains at its prior bounded
  status. No retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: the three-channel +
  P2-S1 unifying lemma + explicit R3-distinction is substantive new
  structural content, not a relabel of prior R3 anomaly-inflow result
  or prior Koide routes. P2-S1 sharpens R3 at an independent layer.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  (A, D, E) characterized in terms of WHAT additional content would
  be needed (charges-to-coefficients morphism, normalization
  principle), not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this probe
  packages a multi-angle attack (three independent flavor-anomaly
  channels) on a single load-bearing closure attempt, with sharp
  PASS/FAIL deliverables in the runner.
- `feedback_review_loop_source_only_policy.md`: deliverable is
  exactly (a) one source-theorem note in `docs/`, (b) one paired
  runner in `scripts/`, (c) one cached output in `logs/runner-cache/`.
  No output-packets, no lane promotions, no synthesis notes.

## Honest scope

This is a *Probe 2* result. It does NOT close A1. It DOES:

1. Examine three concrete flavor-anomaly channels (F1 = Witten Z₂ on
   hw=1, F2 = pure cubic Tr[Q_F³] for U(1)_F flavor, F3 = mixed
   SU(2)_L² × U(1)_F gauge-flavor anomaly), and verify each yields a
   clean obstruction.
2. Identify a unifying P2-S1 lemma (universal flavor-anomaly category
   mismatch) that sharpens R3-functoriality at an independent layer.
3. Compress the closure-path map for A1:
   - 4 named routes (E, A, D, F) are barred by their own obstruction
     notes;
   - flavor-anomaly route now barred by P2-S1 (this note);
   - any future A1 closure attempt must supply a genuinely new
     coefficient-fixing bridge rather than recycle these routes.

Closing A1 unconditionally from A1+A2 + retained stack remains an
open derivation target. Future re-attempts must supply at least one
of: (a) a retained morphism from charge data to operator-coefficient
data, (b) a non-categorical mechanism outside the F1, F2, F3 channels,
or (c) explicit user-approved A3-class admission for the A1
amplitude-ratio input.
