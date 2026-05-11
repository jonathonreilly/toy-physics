# Koide A1 Route A — Koide-Nishiura U(3) Quartic Bounded Obstruction

**Date:** 2026-05-08
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Route A closure attempt for
the A1 √2 equipartition admission on the charged-lepton Koide lane
via the Koide-Nishiura U(3) quartic variational principle.
**Status:** source-note proposal for a negative Route A closure —
shows that the candidate Koide-Nishiura quartic
`V(Φ) = [2(tr Φ)² − 3 tr(Φ²)]²` cannot be derived from retained
Cl(3)/Z³ content. Four independent structural barriers each
independently block the proposed identification. The A1 admission
count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-a1-route-a-koide-nishiura-20260508
**Primary runner:** [`scripts/cl3_koide_a1_route_a_koide_nishiura_2026_05_08_routea.py`](../scripts/cl3_koide_a1_route_a_koide_nishiura_2026_05_08_routea.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_route_a_koide_nishiura_2026_05_08_routea.txt`](../logs/runner-cache/cl3_koide_a1_route_a_koide_nishiura_2026_05_08_routea.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit lane
has full authority to retag, narrow, or reject the proposal.

## Question

`KOIDE_A1_DERIVATION_STATUS_NOTE.md`
identifies "Route A" (Koide-Nishiura U(3) quartic potential) as one
of three remaining open candidates for closing the A1 √2 equipartition
admission. The proposed closure is:

> The U(3)-invariant quartic potential
>
>   `V(Φ) = [2(tr Φ)² − 3 tr(Φ²)]² = 81 (a² − 2|b|²)²`
>
> on the C_3-equivariant circulant Hermitian Φ = aI + bC + b̄C² has
> its UNIQUE global minimum (V = 0) at A1, i.e., at `|b|²/a² = 1/2`.
>
> If V(Φ) is part of the retained Cl(3)/Z³ effective charged-lepton
> action, A1 is forced as the ground state.

The existing runner
[`scripts/frontier_koide_a1_quartic_potential_derivation.py`](../scripts/frontier_koide_a1_quartic_potential_derivation.py)
verifies the *internal arithmetic*: V is U(3)-invariant on M_3(C),
V ≥ 0 always, V = 0 ⟺ |b|²/a² = 1/2. But it does NOT establish
that V emerges structurally from retained Cl(3)/Z³ content.

The status note classifies Route A as "outside Theorem 6's
cancellation" because V is *trace-based* (built from tr Φ and
tr Φ²), not *Clifford-generator-based*. This places Route A
**outside** the bar of Theorem 6, but does NOT by itself close A1.

**Question:** Can the structural identification "V(Φ) appears in
the retained Cl(3)/Z³ effective charged-lepton action with the
specific coefficients (2, −3)" be **derived** from retained
content alone — no empirical loading, no new axioms?

## Answer

**No.** The Koide-Nishiura quartic V(Φ) cannot close A1 from retained
content alone. Four independent structural barriers each block the
proposed derivation. The internal arithmetic 81(a² − 2|b|²)² ≥ 0
holding is a tautology of how V was constructed (squaring the Koide
condition), not evidence of an axiom-native derivation.

The four barriers (each verified numerically in the paired runner):

1. **(B1) Wilson-coefficient circularity.** The specific coefficient
   ratio (α : β) = (2 : −3) in V₀ = α(tr Φ)² + β tr(Φ²) is the
   polynomial encoding of Q = tr(Φ²)/(tr Φ)² = 2/3 — the empirical
   Koide value. Other Wilson coefficient ratios (α : β) give different
   equilibrium |b|²/a² ratios and different Q values. The framework's
   retained content does NOT supply a structural argument fixing
   (α : β) = (2 : −3) other than "this is what reproduces Q = 2/3."

2. **(B2) U(3)-invariance import.** The retained framework has
   *C_3-equivariance* on hw=1 (
   [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1),
   not full U(3)-flavor symmetry. The Koide-Nishiura quartic's
   construction principle ("U(3)-invariant quartic depending only on
   tr(Φ) and tr(Φ²)") is a stronger symmetry than retained content
   provides. Importing U(3) flavor symmetry is a non-retained
   structural assumption.

3. **(B3) Trace-only restriction.** Even granting U(3)-invariance,
   the ring of U(3)-invariant quartics on Hermitian Φ is generated
   by {(tr Φ)⁴, (tr Φ)² tr(Φ²), tr(Φ²)², tr(Φ) tr(Φ³), tr(Φ⁴)} —
   five independent quartics (which on circulant span a 4-dim
   subspace of polynomials in (a, |b|)). The Koide form V₀² uses
   ONLY {(tr Φ)⁴, (tr Φ)² tr(Φ²), tr(Φ²)²} — a 3-dim subspace
   inside the 5-dim quartic invariant ring. Generic Wilson
   expansion includes the other two invariants too; perturbing
   V₀² by such terms shifts the minimum away from A1.

4. **(B4) Empirical-target circularity (squaring trap).** The
   "variational principle" V(Φ) = V₀(Φ)² is constructed by:
   (i) starting from the residual `V₀ = 2(tr Φ)² − 3 tr(Φ²)`
       which is the Koide ratio condition rewritten as zero,
   (ii) squaring it to get a non-negative functional whose
       zero locus is the Koide cone.
   This is logically equivalent to: "set V = (Q − 2/3)²·(tr Φ)⁴
   times a positive constant; minimize V." The 2/3 in this
   construction is the *empirical target value*, not a derivation
   output. The proposed "variational principle" is therefore
   structurally circular: it *defines* a functional whose
   minimum is the empirical answer.

The combined picture: **Route A is structurally barred** at the
"axiom-native" level. The internal arithmetic (V(Φ) = 81(a² − 2|b|²)²
has minimum on Koide cone) is a tautology. Closing A1 via this route
would require either: (a) a new retained primitive supplying the
specific Wilson coefficient ratio (2 : −3) without empirical loading,
(b) explicit user-approved A3-class admission of U(3) flavor symmetry
plus trace-only restriction plus the (2 : −3) coefficient ratio as a
package, or (c) an alternative structural mechanism not based on the
quartic-potential numerology.

## Comparison with Routes E and F

This obstruction is **structurally analogous to but logically distinct from**
the obstructions documented for Routes E (Kostant Weyl-vector) and
F (Yukawa Casimir-difference). All three routes share the meta-pattern:

| Route | Trap class | Specific trap |
|---|---|---|
| **E** (Kostant) | Norm-convention dependence | `\|ρ_{A_1}\|² ∈ {1/4, 1/2, 1}` depending on Cartan-Killing normalization `\|α\|² ∈ {1, 2, 4}` |
| **F** (Casimir-diff) | Charge-convention dependence | `T(T+1) − Y² ∈ {-1/4, 1/2}` depending on PDG vs SU(5) Y-convention |
| **A** (this note) | Wilson-coefficient circularity | `(α : β) = (2 : -3)` directly encodes Q = 2/3 as input |

Routes E and F failed via *external* convention dependencies in
Lie-algebraic norm calculations (`\|·\|²`, `T(T+1) − Y²`). Route A
fails via a *different* mechanism: not a norm convention but a
**Wilson-coefficient choice** in the effective-action expansion. The
"1/2" emerges from the *empirically chosen* coefficient ratio
(2 : -3) — and that ratio is precisely the polynomial encoding of
Q = 2/3.

Routes E and F's underlying problem: a Lie-algebraic scalar happens to
equal the target value `1/2` under one specific normalization
convention, but the same scalar takes other values under equally valid
conventions (so the "match" is convention-dependent).

Route A's underlying problem: the *empirical target value* Q = 2/3 is
written into the *coefficient ratio* of the proposed potential, then
recovered as the potential's minimum. The "1/2" ≡ `|b|²/a²` is the
algebraic consequence of a coefficient choice that *itself* is the
empirical input.

Routes E, F, A are **three different convention/circularity traps**
that all reduce to: the framework's retained content provides no
mechanism to derive the specific number `1/2` (= |b|²/a², or
equivalently Q = 2/3) without empirically loading it into a chosen
normalization, charge convention, or Wilson coefficient ratio.

This is the most general meta-conclusion that emerges from Routes E,
F, A together. The "structurally different approach" hypothesis
of Route A — variational extremum vs Lie-algebraic norm — does NOT
escape the meta-pattern; it is a different specific instantiation of
the same circular-derivation trap.

## Setup

### Premises (A_min for Route A closure attempt)

| ID | Statement | Class |
|---|---|---|
| A1 | Cl(3) local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | Z³ spatial substrate | framework axiom; same source |
| Embed | Cl⁺(3) ≅ ℍ → SU(2)_L; ω pseudoscalar → U(1)_Y; Y_L, Y_H fixed | retained: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | retained: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| Equiv | Any derived operator from C_3-symmetric primitives is C_3-equivariant | retained: [`A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md`](A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md) Step 2 (when present); see also [`HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md) Theorem 5 |
| 3GenObs | hw=1 BZ-corner triplet has M_3(C) algebra; C_3[111] cycles corners | retained-bounded: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| KoideAlg | Koide Q = 2/3 ⟺ a₀² = 2|z|² ⟺ |b|²/a² = 1/2 (algebraic) | retained: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| Substep4 | AC_φλ remains the explicit identification residual on hw=1 | retained-bounded: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md) |
| RouteA_Math | V(Φ) = [2(tr Φ)² − 3 tr(Φ²)]² has minimum on Koide cone (algebraic identity) | tautology; verified by [`scripts/frontier_koide_a1_quartic_potential_derivation.py`](../scripts/frontier_koide_a1_quartic_potential_derivation.py) |
| Theorem5 | No retained C_3-invariant variational principle selects the Koide cone *as a unique point* | retained: [`HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md) Theorem 5 |
| Theorem6 | Fourth-order signed Clifford ordering cancellation rules out 4th-order retained spatial-Clifford + EWSB-Higgs family | retained: [`HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md) Theorem 6 |

### Forbidden imports

- NO PDG observed mass values used as derivation input (anchor-only at
  end, clearly marked per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)).
- NO PDG-extracted Q value (the empirical Q ≈ 2/3 to high precision is
  what makes Route A interesting but cannot be loaded as a derivation
  input).
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- **NO new axioms** (Route A's promise was axiom-native; any A3-class
  admission of U(3) flavor symmetry, trace-only restriction, or
  specific Wilson coefficient ratio requires explicit user approval
  and is not proposed here).

## The structural lemma at issue

**Proposed lemma (Route A — Koide-Nishiura U(3) quartic):**

```
The retained Cl(3)/Z³ effective action contains, on the circulant
hw=1 sector, the U(3)-invariant quartic potential

  V(Φ) = α [2(tr Φ)² − 3 tr(Φ²)]²    for some α > 0

(equivalently: V(Φ) = 81 α (a² − 2|b|²)² on circulant Φ = aI + bC + b̄C²).

By V ≥ 0 with equality on the locus a² = 2|b|², the ground-state
manifold is the Koide cone, forcing |b|²/a² = 1/2 = A1.
```

The runner [`scripts/frontier_koide_a1_quartic_potential_derivation.py`](../scripts/frontier_koide_a1_quartic_potential_derivation.py)
verifies the algebraic identity and the existence of the unique
minimum (5/5 PASS), but does **not** establish that this specific V
appears in any retained effective action. This note investigates
whether such an identification is derivable from retained content.

## Theorem (Route A bounded obstruction)

**Theorem.** On A1+A2 + retained CL3_SM_EMBEDDING + retained
C_3-equivariance + retained KoideCone-algebraic-equivalence +
retained Theorem 5 (no C_3-invariant variational principle) +
retained Theorem 6 (4th-order Clifford cancellation) + admissible
standard math machinery:

```
The structural identification

  "V(Φ) = [2(tr Φ)² − 3 tr(Φ²)]² appears in the retained Cl(3)/Z³
   effective charged-lepton action with the specific coefficient
   ratio (α : β) = (2 : −3)"

cannot be derived from retained Cl(3)/Z³ content alone. Four
independent structural barriers each block the lemma:

  (B1) Wilson-coefficient circularity: (α : β) = (2 : −3) directly
       encodes Q = 2/3 as input.
  (B2) U(3)-invariance import: framework has C_3, not U(3).
  (B3) Trace-only restriction: generic U(3)-quartics span a larger
       space than {(tr Φ)⁴, (tr Φ)² tr(Φ²), tr(Φ²)²}.
  (B4) Empirical-target circularity: V is constructed by squaring
       the Koide condition, making "minimization → A1" tautological.

Therefore Route A closure of A1 is structurally barred under the
stated retained-content surface. The A1 admission count is unchanged.
```

**Proof.** Each barrier is verified independently in the paired runner;
combining them establishes that no derivation chain from retained
content reaches the proposed Wilson-coefficient identification.

### Barrier 1: Wilson-coefficient circularity

Consider the family of U(3)-invariant quadratic-in-Hermitian-traces
residual functionals:

```
V₀^{(α,β)}(Φ) = α (tr Φ)² + β tr(Φ²)
```

with `α, β ∈ ℝ`. On circulant `Φ = aI + bC + b̄C²`:

```
V₀^{(α,β)} = (9α + 3β) a² + 6β |b|²
```

The zero locus `V₀^{(α,β)} = 0` (when `9α + 3β` and `β` have opposite
signs, giving a real locus) corresponds to:

```
|b|²/a² = -(9α + 3β)/(6β) = (-3α/2β) - (1/2)
```

The runner tabulates several `(α, β)` choices:

| (α : β) | `|b|²/a²` at zero | Q value at zero |
|---|---|---|
| (2 : −3) **[Koide]** | 1/2 | 2/3 |
| (1 : −1) | 1 | 1 |
| (3 : −4) | 5/8 | 3/4 |
| (1 : −2) | 1/4 | 1/2 |
| (4 : −5) | 7/10 | 4/5 |

Each `(α : β)` choice corresponds to a different Q value at the
minimum of V = (V₀^{(α,β)})². The choice (2 : −3) is the **only**
ratio that gives `Q = 2/3` (the empirical Koide value).

No retained Cl(3)/Z³ theorem fixes (α : β) at (2 : −3). The framework
provides no constraint on this Wilson coefficient ratio. Choosing it
empirically to match observed Q is **circular** — it makes Q an
input, not a derivation output.

**This is the analog of Routes E/F's convention dependence**, in a
different category. Routes E/F have *normalization-conventions* that
take different values under different conventions; Route A has
*Wilson-coefficient choices* that take different values under different
EFT expansion truncations. Both are external choices, neither derivable
from retained content.

### Barrier 2: U(3)-invariance import

The retained framework's symmetry on hw=1 is **C_3-equivariance**
([`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1):

```
H is C_3-equivariant ⟺ [H, C] = 0 where C = cyclic shift on three corners
⟺ H = aI + bC + b̄C² with a ∈ ℝ, b ∈ ℂ
```

The framework also has retained S_2-breaking obstruction (
[`HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)
Theorem 6 companion): no retained sole-axiom S_2-breaking primitive
exists on hw=1. So the framework has at most C_3-symmetric content.

The Koide-Nishiura construction assumes **U(3)-flavor symmetry** —
a continuous SU(3) action on Hermitian Φ ∈ M_3(ℂ). U(3)-invariant
quartics (built from `(tr Φ)`, `(tr Φ²)`, `(tr Φ³)`, `(tr Φ⁴)`) are
much more restrictive than C_3-invariant quartics.

When restricted to circulant Φ = aI + bC + b̄C², many polynomials
in entries of Φ that are NOT U(3)-invariants reduce to functions of
(a, |b|) — including C_3-invariants that are not U(3)-invariants.
A generic C_3-invariant quartic is NOT a U(3)-invariant quartic, so
generic Wilson expansion in C_3-invariant terms produces additional
quartic operators not captured by the U(3)-invariant V_0².

**Importing U(3)-flavor symmetry as a structural assumption beyond
retained C_3** is non-derivable from Cl(3)/Z³ axioms. The standard
SM has no U(3)-flavor symmetry — Yukawa couplings explicitly break
flavor U(3) — and the framework has not derived an emergent U(3)
flavor symmetry on hw=1.

### Barrier 3: Trace-only restriction

Even granting U(3)-invariance, the ring of U(3)-invariant
quartic polynomial functions on M_3(ℂ)_Herm is generated (via
power-sum / Newton-Girard) by:

```
I_1 = (tr Φ)⁴
I_2 = (tr Φ)² · tr(Φ²)
I_3 = tr(Φ²)²
I_4 = tr(Φ) · tr(Φ³)
I_5 = tr(Φ⁴)
```

— five independent quartic invariants. On circulant Φ = aI + bC + b̄C²
(real b for explicit calculation), these reduce to:

```
I_1 = 81 a⁴
I_2 = 27 a⁴ + 54 a² b²
I_3 = 9 a⁴ + 36 a² b² + 36 b⁴
I_4 = 9 a⁴ + 54 a² b² + 18 a b³
I_5 = 3 a⁴ + 36 a² b² + 24 a b³ + 18 b⁴
```

These five invariants have rank 4 on circulant (one linear dependence,
because the circulant subspace is only 2-real-parameter and the monomials
are {a⁴, a²b², ab³, b⁴} — 4 independent monomials, so 5 invariants
necessarily have rank ≤ 4).

The Koide quartic in this basis is:

```
V(Φ) = (V_0)² = [2 (tr Φ)² − 3 tr(Φ²)]²
     = 4 (tr Φ)⁴ − 12 (tr Φ)² tr(Φ²) + 9 tr(Φ²)²
     = 4 I_1 − 12 I_2 + 9 I_3
     + (0) I_4 + (0) I_5
```

So V uses ONLY I_1, I_2, I_3 — the {(tr Φ), (tr Φ²)}-pure traces.
The other two invariants (I_4 = tr(Φ) tr(Φ³); I_5 = tr(Φ⁴)) appear
with zero coefficient.

A generic U(3)-invariant quartic Wilson expansion would include all
five invariants:

```
V_gen = c_1 I_1 + c_2 I_2 + c_3 I_3 + c_4 I_4 + c_5 I_5
```

with `c_4 ≠ 0` and `c_5 ≠ 0` generically. Such generic expansions
have minima that depend on the (c_4, c_5) values and shift away from
the Koide cone:

| Perturbation | Minimum at |b|/a |
|---|---|
| V_0² alone | 0.7071 (= 1/√2 ✓ A1) |
| V_0² + 0.01 (tr Φ)⁴ | 0.7089 (shifted) |
| V_0² + 1.0 (tr Φ)⁴ | 0.8660 (significantly shifted) |
| V_0² + 0.01 tr(Φ⁴) | 0.7069 (slightly shifted) |
| V_0² + 1.0 tr(Φ⁴) | 0.6941 (shifted) |
| V_0² + 10.0 tr(Φ⁴) | 0.5212 (significantly shifted) |
| V_0² + 100.0 tr(Φ⁴) | 0.0000 (collapsed) |

(All numerical values on minimization with the constraint
`tr(Φ²) = 1` to fix scale; runner verifies.)

The runner shows that adding `(tr Φ)⁴` or `tr(Φ⁴)` perturbations
shifts the minimum continuously away from A1, with no special role
for the Koide value. Restricting to {(tr Φ), (tr Φ²)}-pure traces
is a **convention** that picks out the Koide quartic among generic
U(3)-quartic expansions; it is not forced by retained content.

(Note: the (tr Φ²)² perturbation does NOT shift the minimum because
`tr(Φ²) = N` is held constant by the variational constraint —
verified in runner. This is a degenerate case, not a structural
support.)

### Barrier 4: Empirical-target circularity (squaring trap)

The proposed potential is constructed as:

```
Step 1: Define V_0 = 2(tr Φ)² − 3 tr(Φ²) — the Koide condition residual
Step 2: V := V_0² — square to get a non-negative functional
Step 3: Argue "V has unique minimum on V_0 = 0 = Koide cone"
Step 4: Conclude "minimum forces A1 = Koide cone"
```

This construction is **circular at the action-level identification**:

The Koide ratio is defined as `Q = tr(Φ²)/(tr Φ)²` (algebraic identity
on Hermitian Φ). The empirical observation is `Q ≈ 2/3` to PDG
precision. Setting Q = 2/3 gives `3 tr(Φ²) = 2 (tr Φ)²`, i.e.,
`V_0 = 0`.

So `V_0` is **defined** as the algebraic residual when Q = 2/3 is
imposed. Squaring gives `V` with minimum at the imposed condition.
This is logically equivalent to:

```
Define V := (Q − 2/3)² · 9 (tr Φ)⁴
Minimize V → Q = 2/3
```

The "minimum" is the *empirical input* recovered as *output*. This is
the standard form of a circular derivation: the answer is encoded into
the construction.

For comparison, a *genuine* derivation would proceed:

```
Step 1: From retained primitives, derive an effective action with
        explicit gauge/Yukawa coefficients.
Step 2: Compute the action's quartic terms on hw=1 in the basis
        {I_1, I_2, I_3, I_4, I_5}, getting specific (c_1, ..., c_5).
Step 3: Show the (c_1, ..., c_5) values are forced by retained content
        AND happen to factor as (c_1, c_2, c_3, c_4, c_5) = (4, -12, 9, 0, 0)
        without any circular reference to Q = 2/3 or |b|²/a² = 1/2.
Step 4: Then the minimum at Koide cone is a derivation output.
```

The framework provides Steps 1 and 2 in principle (CL3 SM embedding,
admitted Higgs/Yukawa coefficients), but Step 3 — fixing the specific
factorization (4, -12, 9, 0, 0) without circularity — has not been
demonstrated. Indeed, **Theorem 5** of
[`HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)
already established that no retained C_3-invariant variational
principle on the current surface selects the Koide cone *as a unique
point*. Theorem 5 does not directly bar Route A's Koide-cone-as-locus
form, but it does flag the broader context: no retained variational
mechanism on hw=1 forces the Koide answer.

The runner verifies the squaring construction's circularity by
showing that:
- `V := (Q − q*)² · 9 (tr Φ)⁴` is a valid quartic for ANY value `q*`,
  with V ≥ 0 and V = 0 ⟺ Q = q*.
- For `q* = 2/3`, V coincides (up to overall scale) with the Koide
  quartic V_0².
- For `q* = 1/3` (uniform spectrum), V coincides with a different
  quartic that has its minimum at Q = 1/3.
- For `q* = 1` (degenerate triple), V coincides with yet another
  quartic.

The choice of `q* = 2/3` is the empirical input. The framework's
retained content does not pick it out structurally.

## Why the V(Φ) algebraic identity is a tautology

The runner verifies the identity:

```
For circulant Φ = aI + bC + b̄C²:
  V(Φ) = [2(tr Φ)² − 3 tr(Φ²)]² = 81 (a² − 2|b|²)²
```

This is a *purely algebraic* identity on the 2-real-parameter
circulant subspace. It says: "If you compute V_0 = 2(tr Φ)² − 3 tr(Φ²)
on circulant Φ, it equals 9(a² − 2|b|²); squaring gives 81(a² − 2|b|²)²."

This identity holds for ANY circulant Φ regardless of any axiom set
or framework. It is true in pure algebra. The 5/5 PASS in the
existing runner
[`scripts/frontier_koide_a1_quartic_potential_derivation.py`](../scripts/frontier_koide_a1_quartic_potential_derivation.py)
verifies this algebraic tautology, NOT a structural derivation.

The structural question is NOT "does V have its minimum at Koide cone"
(yes, by V's construction). The structural question is "does retained
content put V in the effective action with specific coefficients
(2, -3)?" — and the answer, per B1-B4, is no.

This is a **Type-I admission** per
`feedback_consistency_vs_derivation_below_w2.md`:
"consistency equality is not derivation." The arithmetic correctness
of V_0² = 81(a² − 2|b|²)² is consistency; the structural identification
of V with retained effective action is derivation, and it does not
hold under retained content alone.

## Counterfactual: alternative quartic potentials

The runner constructs alternative U(3)-invariant quartics that:
- Share the same algebraic structure (positive square form)
- Have minima on different loci than the Koide cone
- Pick out different Q values (Q = 1/3, Q = 1, Q = 1/2, etc.)

Examples (with circulant variables a, b real, b ≥ 0):

| Quartic | (α, β) for V_0 = α(tr Φ)² + β tr(Φ²) | Min at Q | Min at \|b\|²/a² |
|---|---|---|---|
| V₀² (Koide) | (2, -3) | 2/3 | 1/2 |
| Alt₁ | (1, -3) | 1 | 1 (degenerate) |
| Alt₂ | (1, -1) | 1 | 1 |
| Alt₃ | (3, -4) | 3/4 | 5/8 |
| Alt₄ | (1, -2) | 1/2 | 1/4 |
| Alt₅ | (4, -5) | 4/5 | 7/10 |

If the Koide quartic V₀² were structurally forced from Cl(3)/Z³,
the framework would have to explain why V₀² is preferred over the
alternatives. The framework does NOT supply such a discriminator at
retained-content tier.

## Authoritative comparison to prior work

| Prior closure attempt | Status | Comment |
|---|---|---|
| Route A (Koide-Nishiura U(3) quartic) | **THIS NOTE: bounded obstruction** | **four-barrier negative closure: Wilson coeff circularity, U(3) import, trace-only restriction, squaring trap** |
| Route B (Clifford torus on S³) | does not match Koide cone | 45° latitude vs equator |
| Route C (AS Lefschetz cot²) | parallel numeric identity | 2/3 = 2/3 coincidence |
| Route D (Newton-Girard) | open; trace-poly form | 6 = n(n+1)/2 coefficient unforced |
| Route E (A_1 Weyl-vector / Kostant) | bounded obstruction (norm-convention dependence) | per the prompt's referenced Route E note (parallel to this Route A obstruction) |
| Route F (Yukawa Casimir-difference) | bounded obstruction (charge-convention dependence) | [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md) |
| Numerical match runner (Apr 2026, 5/5 PASS) | establishes V's algebraic identity | does NOT establish structural identification of V with retained effective action |

This note **complements** the existing Route A numerical-match runner
([`scripts/frontier_koide_a1_quartic_potential_derivation.py`](../scripts/frontier_koide_a1_quartic_potential_derivation.py))
by establishing that the structural identification cannot be derived
from retained content, even though the numerical match (algebraic
identity) holds.

## Three-route closure

With the present note, three of Route A, E, F have been brought to
explicit bounded-obstruction status. The recurrence pattern is:

> Each "axiom-native A1 candidate route" provides a CONVENTION-DEPENDENT
> or COEFFICIENT-CIRCULAR mechanism for arriving at the value `1/2`
> (= |b|²/a², equivalently Q = 2/3). Each is structurally barred from
> derivation under retained Cl(3)/Z³ content alone; each requires
> an external normalization, charge convention, or Wilson coefficient
> ratio that itself encodes the empirical answer.

This three-route pattern strongly suggests that **A1 is not closable
within retained Cl(3)/Z³ + textbook math alone**. Closing A1 axiom-
natively appears to require either:

- A new retained primitive (e.g., real-irrep-block democracy as named
  in [`HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)
  Theorem 5's candidate primitive list)
- Explicit user-approved A3-class admission (with named scope and
  audit-tier classification)
- An entirely different structural mechanism not yet identified

Future re-attempts on A1 closure should account for the three-route
meta-pattern documented across Routes E, F, A.

## What this closes

- **Route A negative closure** (bounded obstruction). Four
  independent structural barriers verified:
  - (B1) Wilson-coefficient circularity
  - (B2) U(3)-invariance import
  - (B3) Trace-only restriction
  - (B4) Empirical-target circularity (squaring trap)

- **Sharpens the "candidate" status**: prior status was "open
  candidate route — would close A1 if V(Φ) is derived from Cl(3)/Z³."
  This note demonstrates that the structural identification cannot
  be derived from retained content. Future re-attempts must supply
  at least one of: (a) a non-circular structural argument fixing
  Wilson coefficients (α : β) = (2 : −3), (b) a derivation of
  emergent U(3)-flavor symmetry on hw=1 from retained primitives,
  (c) a structural argument restricting Wilson expansion to {(tr Φ),
  (tr Φ²)}-only generators, (d) a non-empirical-target derivation of
  the specific value Q = 2/3 from independent retained primitives.

- **Three-route meta-pattern documented**: Routes E (norm-convention),
  F (charge-convention), A (Wilson-coefficient circularity) all
  obstruct closure via distinct convention/coefficient-dependence
  traps. The meta-pattern itself is an audit-defensible result.

- **Sister-route implications**: Routes B, C, D remain in their prior
  bounded statuses; none have been newly closed by this note.

- **Audit-defensibility**: explicit tabulated alternative quartic
  potentials demonstrate the Wilson-coefficient choice's
  non-uniqueness, removing the "structurally different mechanism"
  reading from the axiom-native candidate list at retained-grade.

## What this does NOT close

- A1 admission count is unchanged. A1 remains a load-bearing
  non-axiom step on the Brannen circulant lane.
- Routes B and C remain in their prior statuses; Route D is handled by
  its own Newton-Girard bounded-obstruction companion note.
- The "real-irrep-block democracy" candidate primitive (Theorem 5
  of [`HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md))
  is not closed or barred by this note — it remains an open candidate.
- Charged-lepton Koide closure remains a bounded observational-pin
  package (status from
  [`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
  unchanged).
- The numerical-match runner
  [`scripts/frontier_koide_a1_quartic_potential_derivation.py`](../scripts/frontier_koide_a1_quartic_potential_derivation.py)
  retains its 5/5 PASS for the *algebraic* identity. This note does
  NOT retract that — it adds a structural-derivation analysis that
  the algebraic check by itself does not provide.
- AC_φλ residual (substep 4) is unaffected.
- L3a trace-surface bounded obstruction status unchanged.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| Wilson-coefficient circularity (B1) | Demonstrate a retained constraint that fixes (α : β) = (2 : −3) without empirical loading — refutes B1. |
| U(3)-invariance import (B2) | Derive an emergent U(3)-flavor symmetry on hw=1 from retained Cl(3)/Z³ primitives — refutes B2. |
| Trace-only restriction (B3) | Derive a retained restriction excluding `tr(Φ) tr(Φ³)` and `tr(Φ⁴)` invariants from the effective action — refutes B3. |
| Empirical-target circularity (B4) | Derive Q = 2/3 from independent retained primitives without recourse to Brannen-circulant trace structure or empirical observation — refutes B4. |
| Algebraic identity (anchor) | Falsified if `V₀² ≠ 81 (a² − 2|b|²)²` on circulant Φ; numerical check holds to machine precision (5/5 PASS in existing runner). |

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is the negative Route A boundary:
the Koide-Nishiura U(3) quartic structural identification is blocked
by Wilson-coefficient circularity, U(3)-invariance import, trace-only
restriction, and empirical-target circularity unless a new retained
primitive supplies the (2 : −3) coefficient ratio without empirical
loading.

No new admissions are proposed. A1 remains unchanged at its prior
load-bearing non-axiom status on the Brannen circulant lane. The
independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The "Route A is the strongest non-Theorem-6 candidate (outside Clifford cancellation)" claim is sharpened from "open candidate route" to "structurally barred under retained content; needs explicit Wilson-coefficient fix or U(3) import." |
| V2 | New derivation? | The four-barrier obstruction argument applied to Route A is new structural content. Prior status note enumerated Route A as an open candidate; this note proves the structural identification cannot close. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) Wilson-coefficient circularity tabulation, (ii) U(3)-vs-C_3 invariance import comparison, (iii) trace-only restriction perturbation analysis, (iv) squaring-trap empirical-target circularity, and (v) the four-barrier conjunction. |
| V4 | Marginal content non-trivial? | Yes — the explicit tabulation of alternative `(α : β)` Wilson coefficient choices and their corresponding Q values, plus the U(3)-quartic perturbation analysis (showing minimum shifts), is non-obvious from prior notes. |
| V5 | One-step variant? | No — the four-barrier argument is structural across multiple categories (Wilson coefficient, U(3) symmetry import, generic invariant ring, squaring construction circularity), not a relabel of any prior Koide route. |

**Source-note V1-V5 screen: pass for bounded-obstruction audit
seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of prior Koide routes (E, F). The four-barrier
  obstruction argument applied to Route A is new structural content
  with explicit tabulated counterexamples and Wilson-coefficient
  perturbation analysis.
- Identifies a NEW STRUCTURAL TRAP (Barrier 1 = Wilson-coefficient
  circularity, distinct from Routes E/F's normalization-convention
  dependence; Barrier 4 = empirical-target circularity / squaring
  trap, distinct from E/F's "norm equals 1/2" coincidence).
- Sharpens the "outside Theorem 6 candidate" claim from open to
  closed-negatively, with explicit list of what would be required to
  reopen it.
- Provides explicit numerical perturbation analysis demonstrating
  the trace-only restriction's non-uniqueness — a calculation not
  performed in prior Route A discussions.

## Cross-references

- A1 derivation status (parent): `KOIDE_A1_DERIVATION_STATUS_NOTE.md`
- Existing Route A numerical runner: [`scripts/frontier_koide_a1_quartic_potential_derivation.py`](../scripts/frontier_koide_a1_quartic_potential_derivation.py)
- Route F bounded obstruction (sibling): [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
- Circulant character derivation: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide-cone algebraic equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- CL3 SM embedding: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
- Higher-order structural theorems (Theorems 5, 6): [`HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)
- Substep 4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Physical lattice baseline: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- C_3 symmetry preserved interpretation: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
- A1 physical bridge attempt summary: [`KOIDE_A1_PHYSICAL_BRIDGE_ATTEMPT_2026-04-22.md`](KOIDE_A1_PHYSICAL_BRIDGE_ATTEMPT_2026-04-22.md)
- A1 loop final status: [`KOIDE_A1_LOOP_FINAL_STATUS_2026-04-22.md`](KOIDE_A1_LOOP_FINAL_STATUS_2026-04-22.md)
- MINIMAL_AXIOMS: `MINIMAL_AXIOMS_2026-05-03.md`

## Validation

```bash
python3 scripts/cl3_koide_a1_route_a_koide_nishiura_2026_05_08_routea.py
```

Expected output: structural verification of (i) algebraic identity for
V₀² on circulant (reproduces the existing 5/5 from
`frontier_koide_a1_quartic_potential_derivation.py`), (ii) Barrier 1
Wilson-coefficient circularity with tabulated alternatives, (iii)
Barrier 2 U(3)-vs-C_3 invariance comparison, (iv) Barrier 3 trace-only
restriction with perturbation analysis, (v) Barrier 4 empirical-target
circularity / squaring trap analysis, (vi) alternative quartic
potentials demonstrating non-uniqueness, (vii) three-route meta-pattern
verification (Routes E, F, A all suffer convention/coefficient
dependence), (viii) bounded-obstruction theorem statement.

Cached: [`logs/runner-cache/cl3_koide_a1_route_a_koide_nishiura_2026_05_08_routea.txt`](../logs/runner-cache/cl3_koide_a1_route_a_koide_nishiura_2026_05_08_routea.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  specifically applies the "consistency equality is not derivation"
  rule. The algebraic identity `V₀² = 81(a² − 2|b|²)²` is a
  consistency equality (built into V's construction), not a structural
  identity that admits derivation under retained content. The
  proposed lemma cannot load-bear A1 closure on this basis.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim that "V(Φ) is the unique U(3)-quartic vanishing on
  the Koide cone" by showing that the action-level identification
  (V appears in retained effective action with specific Wilson
  coefficients) requires multiple non-derived structural assumptions.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction; the
  parent A1 admission remains at its prior bounded status. No
  retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: the four-barrier
  argument with explicit Wilson-coefficient tabulation, U(3)
  perturbation analysis, and squaring-trap analysis is substantive
  new structural content, not a relabel of prior Koide routes E or F.
- `feedback_compute_speed_not_human_timelines.md`: alternative
  closure paths characterized in terms of WHAT additional content
  would be needed (Wilson coefficient fix, U(3) emergent symmetry,
  trace-only restriction, non-empirical Q derivation), not how-long-
  they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  a multi-angle attack (four independent barriers) on a single
  load-bearing structural identification, with sharp PASS/FAIL
  deliverables in the runner.
- `feedback_bridge_gap_fragmentation_2026_05_07`: this note
  fragments Route A's "single closure attempt" into four independent
  barriers with separable evidence, in line with the bridge-gap
  fragmentation pattern.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links for
the audit citation graph. It does not promote this note or change
the audited claim scope.

- [koide_a1_derivation_status_note](KOIDE_A1_DERIVATION_STATUS_NOTE.md)
- [koide_a1_route_f_casimir_difference_bounded_obstruction_note_2026-05-08_routef](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
- [koide_circulant_character_derivation_note_2026-04-18](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- [charged_lepton_koide_cone_algebraic_equivalence_note](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- [cl3_sm_embedding_theorem](CL3_SM_EMBEDDING_THEOREM.md)
- [higher_order_structural_theorems_note](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)
- [staggered_dirac_substep4_ac_narrow_bounded_note_2026-05-07_substep4ac](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- [three_generation_observable_theorem_note](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- [physical_lattice_foundational_interpretation_note_2026-05-08](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- [c3_symmetry_preserved_interpretation_note_2026-05-08](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
- [koide_a1_physical_bridge_attempt_2026-04-22](KOIDE_A1_PHYSICAL_BRIDGE_ATTEMPT_2026-04-22.md)
- [koide_a1_loop_final_status_2026-04-22](KOIDE_A1_LOOP_FINAL_STATUS_2026-04-22.md)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
