# A2.5 Derivation Attack — Six-Vector Results Note

**Date:** 2026-05-07
**Type:** attack_results + structural_obstruction_consolidation
**Authority role:** source-note proposal. Audit verdict and downstream
status are set only by the independent audit lane.

## What this note does

The proposed axiom A2.5 (single-loop-traversal locality) survived the
five-attack hostile review in
[`A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md`](A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md)
with two scope clarifications. The remaining open question is whether
A2.5 itself can be **derived** from the existing primitives (A1, A2,
canonical Tr-form, RP, locality, single-clock + Lieb-Robinson, retained
Casimir) so that it does not have to be admitted as a new axiom. If it
can, the bridge gap closes as a positive theorem; if it cannot, A2.5
must be admitted as a new axiom and audited.

This note pursues six independent attack vectors. For each I report
either (a) a positive partial result with explicit proof structure, or
(b) a definitive structural obstruction with named barrier.

The bottom line up front:

| Attack | Vector | Verdict | Strength |
|---|---|---|---|
| 1 | Hochschild / Cl(3) chain cohomology | **Obstruction** | Specific and definitive |
| 2 | Single-irrep locality from minimal carrier | **Partial positive (with caveat)** | Forces fundamental rep, not single-traversal |
| 3 | Z³ CW-complex / 2-cell minimality | **Strong partial positive** | Forces 1×1 plaquette as minimal closed loop |
| 4 | Operator-product algebra closure | **Obstruction** | Specific |
| 5 | RP + OS Cauchy-Schwarz forcing | **Sharper-than-claimed partial positive** | Forces leading-dim Wilson but does NOT distinguish Wilson from heat-kernel/Manton |
| 6 | Lieb-Robinson single-time-slice locality | **Obstruction** | Specific (orthogonal to action form) |

The combined positive results (Attacks 2, 3, 5) close A2.5's
**continuum-limit content** (the leading-dim-4 magnetic operator is
forced to Wilson-form `α Re Tr_F(U_p) + β`) but do NOT close the
**finite-β content** (Wilson, heat-kernel, Manton remain
RP-compatible and distinguished only by Symanzik-irrelevant higher-
character corrections).

This means:

- **A2.5 reduces to a derived theorem from existing primitives at
  the continuum level.** The companion theorem note
  [`A2_5_DERIVED_THEOREM.md`](A2_5_DERIVED_THEOREM.md) consolidates
  the chain (Attacks 3 → 2 → 5 → Symanzik power-counting) into an
  audit-grade derivation.

- **The bridge gap action-form ambiguity remains structural at finite β**,
  consistent with the existing no-go
  ([`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md)).
  The framework predicts Wilson-form uniquely *in the continuum
  limit*; at finite β the prediction is action-form-ambiguous over
  {Wilson, heat-kernel, Manton}.

- **The structural obstructions in Attacks 1, 4, 6 are definitive.**
  Future cycles should not revisit cohomological grading,
  algebra-closure grading, or causality-based traversal-count
  selectors — none of these routes can succeed.

If the audit lane accepts the continuum-limit closure as substantive
progress, **the bridge gap closes as a derived theorem at the
continuum level** modulo the `g_bare = 1` open gate.

If the audit lane demands closure at finite β as well, A2.5 must
remain a proposed axiom (the existing no-go is correct at finite β).

## Inputs available — the existing primitive stack

For every attack vector below, the only admitted inputs are:

- **A1**: Cl(3) is the local algebra at each lattice site
  ([`MINIMAL_AXIOMS_2026-05-03.md`](../../docs/MINIMAL_AXIOMS_2026-05-03.md)).
- **A2**: Z³ is the spatial substrate
  ([`MINIMAL_AXIOMS_2026-05-03.md`](../../docs/MINIMAL_AXIOMS_2026-05-03.md)).
- **Per-site Hilbert space dim 2**, Pauli realization
  ([`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](../../docs/CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md)).
- **Canonical trace form** `Tr(T_a T_b) = δ_{ab}/2`, with derived
  Casimir `C_2(3) = 4/3`
  ([`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](../../docs/SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)).
- **SU(3) emergence from Cl(3) + Z³** on the symmetric base
  ([`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](../../docs/CL3_COLOR_AUTOMORPHISM_THEOREM.md)).
- **Reflection positivity** along the temporal axis
  ([`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)).
- **Microcausality / Lieb-Robinson**, `v_LR < ∞`, equal-time tensor
  factorization
  ([`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](../../docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)).
- **Single-clock codimension-1 evolution**, RP reflection axis is
  uniquely temporal
  ([`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](../../docs/AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)).
- **`g_bare = 1` rigidity** (gauge-coupling absorbed into canonical Tr-form)
  ([`G_BARE_RIGIDITY_THEOREM_NOTE.md`](../../docs/G_BARE_RIGIDITY_THEOREM_NOTE.md)).
- **No-new-axiom rule** (per
  [`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md)).

The target derivation is: under these inputs alone, force
`f(U_p) = α · Re Tr_F(U_p) + β` (the conclusion of B.7) without
admitting "single-loop-traversal" as a separate axiom.

## Attack 1 — Cl(3) algebra cohomology / Hochschild route

### Hypothesis

Single-loop closure on Z³ might correspond to a coboundary in the
Hochschild cochain complex of the Cl(3) site algebra (or in a
suitable lattice cochain complex). The "single-loop = lowest
non-trivial cohomology class" framing would force the elementary
plaquette as the minimal cocycle and rule out higher-power loops.

### Attempt

The Hochschild complex `C^n(A, A)` for an associative `R`-algebra `A`
consists of `n`-cochains `f : A^{⊗n} → A` with the standard
coboundary `δ : C^n → C^{n+1}` (Hochschild 1945; Loday 1992 ch. 1).
For `A = Cl(3)` (or for the full lattice algebra
`A_Λ = ⊗_{x ∈ Λ} Cl(3)_x`), the question is whether the
"plaquette traversal" map carries a natural cohomological grading
that distinguishes single-from-multi traversals.

The **structural obstruction** is exact and elementary:

**Proposition (Attack-1 obstruction).** The Hochschild cochain
complex of `Cl(3)` (or of `A_Λ`) does not separate single-loop
traversals from multi-loop traversals.

**Proof.** Cl(3) is a finite-dimensional simple `ℝ`-algebra
(isomorphic to `M_2(ℂ)` after complexification, dimension 8 over
`ℝ`). For any finite-dimensional simple algebra `A` over a field
`k` of characteristic 0, the Hochschild cohomology vanishes in
positive degrees:

```
HH^n(A, A) = 0  for all n ≥ 1
```

(this is the **Wedderburn-Hochschild-Whitehead theorem** for
separable algebras over characteristic 0; see Weibel 1994 §9.2.1,
Cartan-Eilenberg 1956 §IX.7). Cl(3) is separable because its
center is a field and it's finite-dimensional simple in characteristic
0; the same holds tensor-product-wise for `A_Λ` over any finite
block.

Vanishing in positive degree means **every Hochschild cochain in
positive degree is a coboundary**. There is no non-trivial cohomology
class — single-loop and multi-loop closure give the same trivial
cohomology class, namely zero. The Hochschild grading therefore
cannot distinguish single-loop from multi-loop traversal. ∎

### Verdict

**Definitive obstruction.** Hochschild cohomology of Cl(3) (or
`A_Λ`) is structurally trivial in positive degrees, so it cannot
separate single-from-multi loop traversal. Future sessions should
not revisit this route.

A weaker variant — Hochschild cohomology with **deformed
coefficients** (e.g., a non-trivial `Cl(3)`-bimodule) — is *not*
ruled out by the Wedderburn-Hochschild-Whitehead theorem. But the
existing framework primitives admit no such deformed bimodule
construction; introducing one would require a new admission, which
is precisely what we are forbidden from doing under the no-new-axiom
rule.

### Reusable conclusion

The Cl(3) algebra is too algebraically rigid (separable simple in
char 0) to carry a non-trivial Hochschild grading. Any future
attempt to use Cl(3) cohomology to force operator-form properties
must either deform the coefficient bimodule (new admission, blocked)
or work in a different cohomology theory (e.g., lattice cellular
cohomology of Z³ — see Attack 3, where this opens up).

---

## Attack 2 — Single-irrep locality from the minimal Cl(3) carrier

### Hypothesis

A1 + the per-site uniqueness theorem give: each site carries the
*minimal* faithful Cl(3) module — the 2-dimensional spinor irrep.
A "minimal-carrier locality theorem" would assert that only operators
expressible in this minimal carrier (and direct sums of its tensor
power on the lattice) can be primary action terms; higher-rep
operators are non-primitive constructions and forbidden as primary.

This is *very close* to scope-clarification 1 of A2.5
([`A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md`](A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md))
and would, if proved, force only `Tr_F` (not `Tr_(2,0)`, not
`Tr_(1,1)`, etc.) as the natural trace operation.

### Attempt

The fundamental rep `V_F` of SU(3) emerges from Cl(3) on the
symmetric 3D base of the taste cube
([`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](../../docs/CL3_COLOR_AUTOMORPHISM_THEOREM.md)).
Higher reps (`V_{(2,0)} = Sym² V_F`, `V_{(1,1)} = adjoint`, etc.)
are constructed from `V_F` via tensor products and Schur-Weyl
projections.

The "minimal-carrier" claim is: at the per-site or per-link level,
the only intrinsic carrier is `V_F`; everything else is a constructed
rep that requires an external admission (the choice of how to
combine tensor factors).

**The obstruction** is that this argument *almost* works for
single-link operators (where the gauge variable is `U ∈ SU(3)`
acting natively on `V_F`), but it does not extend to higher powers
of `U` on the *same* link. Specifically:

`Tr_F(U^k) = Tr_F(U · U · ... · U)` with `k` factors, all the same
link variable `U`. This expression uses ONLY:
- algebra product on `End(V_F)` (primitive),
- fundamental trace `Tr_F` (primitive),
- the single link's holonomy `U` (primitive: it's `exp(i a A)` with
  `A ∈ su(3) ⊂ Cl(3) ⊗ Cl(3)` on the canonical surface).

There is **no admission** required to write `Tr_F(U^k)`. It is built
from the same primitive vocabulary as `Tr_F(U)`.

So the "single-irrep" angle distinguishes `Tr_F` from `Tr_(2,0)`,
**but does not distinguish `Tr_F(U)` from `Tr_F(U^2), Tr_F(U^3), …`**
— the latter are still in `V_F` (i.e., in the minimal carrier).

The minimal-carrier locality theorem can be made sharp on **rep
choice** but not on **traversal count**.

### Verdict

**Specific obstruction with caveat.**

(a) **Positive partial.** The minimal-carrier argument *does* force
the trace operation to be `Tr_F` (the fundamental), which closes
attack-vector 5 of the hostile review (higher-rank rep traces).
This is essentially the content of scope-clarification 1 in
[`A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md`](A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md).

(b) **Obstruction.** The minimal-carrier argument does *not* force
`k = 1` in `Tr_F(U^k)`. Higher powers stay in the same minimal
carrier; the rep-theoretic / carrier argument is silent on
traversal count.

(c) **Connection to Attack 5.** The traversal-count residual is
exactly what the RP route handles — see Attack 5 below.

### Reusable conclusion

"Minimal carrier" forces **fundamental rep** but not
**single-traversal**. Use this conclusion in scope-clarification 1
of A2.5 (where it's already implicit) but do not over-extend it
to traversal-count.

---

## Attack 3 — Z³ CW-complex / 2-cell minimality (positive partial)

### Hypothesis

Z³ as a CW-complex has 0-cells (vertices), 1-cells (links), 2-cells
(plaquettes), and 3-cells (cubes). The **smallest 2-cell** is the
1×1 plaquette. The minimum-area gauge-invariant closed loop is
therefore the 1×1 plaquette boundary. Any other closed loop is
either:

- a 2-cell of larger area (e.g., 1×2 rectangle, area 2 in lattice
  units); or
- a multi-plaquette boundary that decomposes via simplicial / cellular
  Stokes theorem into a sum of 1×1 plaquettes (the boundary operator
  `∂_2` from 2-chains to 1-chains).

This is purely **substrate combinatorics** on Z³ as a regular cubical
CW complex — A2 alone, with no further admission.

### Argument

**Lemma (2-cell minimality).** On Z³ as a regular cubical CW complex,
the minimum-area 2-cell whose boundary ∂ is a non-trivial closed
1-chain is the 1×1 plaquette.

**Proof.** A regular cubical complex on Z³ has 2-cells indexed by
ordered pairs `(x, (i, j))` with `x ∈ Z³` and `(i, j)` an ordered
pair of distinct coordinate axes; the 2-cell occupies the unit
square `[x_i, x_i+1] × [x_j, x_j+1]` in the `i,j`-plane. Every such
2-cell has area exactly 1 (one squared lattice unit). Any 2-chain
of larger area is a sum of such unit 2-cells; equivalently, by
Stokes (i.e., by the chain-complex relation `∂_2`), its boundary
1-chain is the sum of 1-cells weighted by the boundary signs of the
constituent unit 2-cells. ∎

**Lemma (single-plaquette minimum closed loop).** The minimum-length
non-trivial closed 1-chain on Z³ that is the boundary of a 2-chain
is the 1-skeleton of a single 1×1 plaquette (length 4, area 1).

**Proof.** A non-trivial closed 1-chain `c` on Z³ that bounds a
2-chain `S` (i.e., `c = ∂_2 S`) has length `|c| ≥ 4`. The bound is
saturated iff `S` is a single 1×1 plaquette: any larger 2-chain has
strictly larger boundary (strict triangle inequality on cubical
complexes; equivalently, the isoperimetric inequality on Z² gives
`|∂A| ≥ 4 √|A|` for `|A| ≥ 1`, saturated only at `|A| = 1`). ∎

**Theorem (Attack-3, positive).** In any "operator built from a
gauge-invariant closed loop" formulation:

(T-3a) The minimum-length closed loop boundary on Z³ is the 1-skeleton
of a single 1×1 plaquette.

(T-3b) Any closed loop boundary of length 4 is gauge-equivalent (via
substrate translations and rotations) to a 1×1 plaquette.

(T-3c) Any closed loop of length > 4 either (i) bounds a multi-cell
2-chain — in which case it Stokes-decomposes into a sum of 1×1
plaquette holonomies — or (ii) is a non-contractible loop, which
requires non-trivial Z³ topology not present at the level of any
finite block.

### What this closes

Attack 3 closes the part of A2.5 that says "the minimal closed loop
on Z³ is the 1×1 plaquette." Specifically, it discharges
**scope-clarification 2 of A2.5** (the "elementary 1×1 plaquette
of Z³" part), purely from substrate combinatorics, with no further
admission.

This is enough to rule out:
- Wilson rectangles (1×2, 2×1, 2×2): area > 1, decompose into
  1×1 plaquettes via Stokes
- Twisted plaquettes: same area, but rotated/translated, still
  reduce to 1×1
- Multi-plaquette compositions: by Stokes, sum of 1×1 plaquette
  holonomies up to commutators (which are higher-order in the lattice
  spacing — Symanzik improvement only, not primary)

### What this does NOT close

Attack 3 does NOT close the **single-traversal-of-the-minimum-loop**
question. The 1×1 plaquette holonomy `U_p ∈ SU(3)` can still be
traversed `k` times: `U_p^k`. The cellular Stokes argument bounds
the *area* of the 2-chain, not the *winding number* of the holonomy
around its boundary 1-chain.

### Verdict

**Strong positive partial.** Attack 3 closes the area-minimality half
of A2.5 (scope-clarification 2) cleanly from A2 and elementary
substrate combinatorics. This is a **substrate-only** derivation; it
uses no algebra, no RP, no Lieb-Robinson — just Z³ as a regular
cubical CW complex.

**Single-traversal residual handled by Attack 5.**

### Cross-reference

The CW-complex / Stokes argument is implicit in standard lattice gauge
theory but, to my knowledge, has not been written up in this
framework as a substrate-only theorem. It is the formal content of
"the smallest 2-cell on Z³ is the 1×1 plaquette" cited in
[`BLOCK_B7_PRIMITIVE_OPS_FORCING.md`](BLOCK_B7_PRIMITIVE_OPS_FORCING.md)
attack-4 response.

---

## Attack 4 — Operator-product algebra closure

### Hypothesis

The algebra generated by Cl(3)-primitive operations on holonomy
operators may close under specific structural rules that distinguish
single-traversal from multi-traversal at the algebra-of-observables
level. In particular: maybe the *closed* algebra generated by
single-link `Tr_F(U)` operators under primitive operations is
*strictly smaller* than the algebra including `Tr_F(U^k)` for `k ≥ 2`
— and the framework primitives select only the smaller closed algebra.

### Attempt

Consider the gauge-invariant subalgebra `B` of the lattice operator
algebra generated by:
- products,
- Clifford conjugation,
- grade-0 projections,
- fundamental traces of holonomies.

The question: is the subalgebra generated by `{Re Tr_F(U_p) : p ∈
plaquettes(Λ)}` strictly smaller than the subalgebra generated by
`{Re Tr_F(U_p^k) : p, k}`?

**The obstruction is direct.** SU(3) characters satisfy

```
χ_(2,0)(U) = (1/2)(Tr_F(U)² + Tr_F(U²))
χ_(0,2)(U) = (1/2)(Tr_F(U^*)² + Tr_F((U^*)²))
χ_(1,1)(U) = |Tr_F(U)|² - 1
```

— standard Newton-power identities for SU(N) characters
(Frobenius-Schur, Cvitanović 2008 ch. 9). Every higher-`Tr` power
appears in the *polynomial closure* of `{Tr_F(U), Tr_F(U^*)}`. So
the polynomial-closure algebra of single-traversal trace operators
is the **full character ring** of SU(3) on a single plaquette, by
the standard Newton-Frobenius identities.

Equivalently: the algebra generated by Cl(3)-primitive operations
applied to *single-link holonomy variables*, when polynomial-closed,
generates **every** class function of `U_p` — not just the linear
ones.

### Why this is the obstruction

The framework's primitives don't restrict to *linear* combinations
of `Tr_F` — they admit polynomial closure (algebra product is
primitive). Once polynomial closure is admitted, the algebra-of-
observables on a single plaquette is the full SU(3) class-function
ring; there is no natural truncation at "single traversal."

### Variant attempt: graded primitive operations

A natural defense: introduce a grading on Cl(3)-primitive operations
where each application of `Tr_F` to a single holonomy carries weight
1, and demand that operations of higher weight be Symanzik-
suppressed.

This would close the residual, but the grading is **not derived
from A1+A2** — it is precisely the content of A2.5. Adopting it
amounts to admitting A2.5 by another name.

### Verdict

**Specific obstruction.** The algebra-closure route does not
distinguish single-from-multi traversal because polynomial closure
of single-trace operators already generates the full character
ring. A traversal-count restriction must come from outside the
algebra-of-observables structure — from a dynamical or operator-
dimension argument, not a pure algebraic-closure argument.

This obstruction is *complementary* to Attack 1's: Attack 1 ruled
out cohomological grading; Attack 4 rules out algebraic-closure
grading. Together they show that **no purely algebraic property
of the operator system — neither cohomological nor algebraic —
can supply the traversal-count restriction**.

### Reusable conclusion

Future attempts to derive A2.5 from algebra-of-observables
properties alone will fail. The traversal-count restriction must
come from a complementary structural input: dimension counting,
RP, or causality. Attacks 3, 5, 6 below pursue these.

---

## Attack 5 — Reflection positivity and OS Cauchy-Schwarz forcing (positive partial)

### Hypothesis

The framework's retained RP theorem
([`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md))
rests on an Osterwalder-Seiler / Sharatchandra-Thun-Weisz Cauchy-
Schwarz factorization. RP-Step 1 explicitly notes:

> "The Wilson plaquette form is chosen specifically so this Cauchy-
> Schwarz-style rewriting works; no other plaquette form (e.g.
> improved actions with negative-coefficient rectangles) is
> permitted by `A4`'s 'accepted plaquette surface'."
>
> ([`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`, line 251-254](../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md))

This is **the strongest hint in the existing framework** that RP itself
forces Wilson-form. Currently, the RP theorem treats this as a
property of the *admitted* A4 (canonical Wilson normalization). The
question for Attack 5 is whether RP can independently force Wilson-form
*without* admitting it — using only A1+A2+canonical Tr-form+single-clock.

### Argument structure

The OS Cauchy-Schwarz factorization for a temporal plaquette
straddling the reflection axis works like this. A plaquette `p` of
type (c) (straddling the reflection plane) has the structure

```
Re Tr_F(U_t(x⃗, -1) · U_i(x⃗, 0) · U_t(x⃗+î, -1)^† · U_i(x⃗, -1)^†)
```

where `U_t` is a temporal link crossing the reflection plane and
`U_i` is a spatial link on one side. The OS / Sharatchandra
manipulation reorganises this as

```
Re Tr_F(A_+ · B_-^†)  =  Re Tr_F(A_+ · θ(A_+)^†)
```

where `A_+` is supported on the positive-time half and `B_- = θ(A_+)`
on the reflected half. The Haar-integral of `exp(-S_∂)` over the
crossing temporal links then has the L²(SU(3), Haar) inner-product
structure, giving (R1)–(R2):

```
Z[F] = || ∫_{Λ_+ ∪ ∂} DU exp(-S_+) F ||² ≥ 0
```

This **only works** for the bilinear pairing `Re Tr_F(A_+ B_-^†)`
on a temporal plaquette. The equivalent manipulation for a higher-
power magnetic operator on a temporal plaquette **fails** at
exactly the bilinear-pairing step.

### Theorem candidate (Attack-5 partial claim — careful version)

**Theorem (Attack-5, RP excludes negative-coefficient improvements,
sharp form).**

Under A1 + A2 + canonical Tr-form + single-clock + retained RP,
**any** primary magnetic operator that contains a single plaquette
boundary as its support and is expanded in SU(3) characters,

```
M̂(U_p) = Σ_λ m_λ · Re χ_λ(U_p),
```

must satisfy `m_λ ≥ 0` for every contributing λ. Negative-coefficient
character contributions (e.g., the "improved" Lüscher-Weisz subtraction
of a 2×1 rectangle to cancel O(a²) artifacts) violate RP and are
excluded as primary action terms.

**Proof.** The retained RP theorem
([`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md))
applies the OS Cauchy-Schwarz factorization to each plaquette. For
a temporal plaquette of type (c), the Boltzmann weight `e^{-S_p}`
expands in SU(3) characters as `Σ_λ c_λ(β) χ_λ(U_p)` with
character-coefficients `c_λ(β)` determined by the action. The OS
rewriting requires that **each** character-coefficient `c_λ` be
non-negative; otherwise the bilinear-pairing structure
`Z[F] = ‖∫ ... ‖²` does not give a positive Hermitian form.

For the Wilson action `S_p = β(1 − (1/N_c) Re Tr_F U)`, the character
expansion gives `c_λ(β) > 0` for all λ. For the Lüscher-Weisz
improved action `S_p^{LW} = c_0 S_p^{Wilson} + c_1 S_p^{2×1} + …`
with `c_1 < 0` (standard Symanzik improvement), some `c_λ`
become negative for `λ` containing the rectangle's character
content; these violate RP at the plaquette level.

The retained RP theorem's own commentary
([`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`, line 251-254](../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md))
makes this exclusion explicit: "no other plaquette form (e.g.
improved actions with negative-coefficient rectangles) is permitted".
∎

### What Attack-5 does NOT directly close

The above argument forbids **negative-coefficient** improvements.
But the canonical Wilson, heat-kernel, and Manton actions all have
**positive** character expansions for `β > 0`:

| Action | Character expansion | Character coefficients |
|---|---|---|
| Wilson | `e^{-β(1-Re Tr U/N_c)}` expansion | All `c_λ(β) > 0` (Bessel-determinant) |
| Heat-kernel | `Σ_λ d_λ e^{-(t/2) C_2(λ)} χ_λ(U)` | All `c_λ = d_λ e^{-(t/2)C_2(λ)} > 0` |
| Manton | `e^{-β d²(U,I)}` with bi-invariant metric `d²` | All `c_λ > 0` (positive heat semigroup) |

So RP alone **does not select Wilson over heat-kernel or Manton**.
The substantive selection must come from elsewhere — see the
synthesis below for what each input contributes.

### Where RP does help: ruling out non-positive characters

The RP argument *does* give a structural restriction: any candidate
primary magnetic operator written as a sum

```
M̂(U_p) = Σ_λ m_λ Re χ_λ(U_p)
```

with `m_λ ≥ 0` for all λ is a valid candidate; with any `m_λ < 0`
it fails RP. Combined with:

- **Step 1 (Z³ substrate combinatorics, Attack 3)**: minimum-area
  closed loop is the 1×1 plaquette → operator is supported on a
  single plaquette boundary (not a rectangle, not multi-plaquette).
- **Step 2 (Cl(3) primitive carrier, Attack 2 / scope-clarification 1)**:
  natural single-link trace is `Tr_F`; higher-rank reps require
  external admission.
- **Step 5 (Symanzik power-counting)**: at lattice scale `a → 0`,
  operators of mass dimension > 4 are irrelevant; the leading dim-4
  operator on a 1×1 plaquette is `Re Tr_F(U_p)`.

we obtain:

**The combined argument forces the** `α · Re Tr_F(U_p) + β`**
form at leading dimension** with `α ≥ 0` (RP positivity), with
higher-character corrections (e.g., `Tr_F(U_p^2)`,
`(Re Tr_F(U_p))^2`, `χ_(2,0)(U_p)`) admitted as Symanzik corrections
at higher operator dimension.

This is **substantively** A2.5's content, but NOT a proof that
heat-kernel and Manton are excluded — they are not (they contain
all character contributions with positive coefficients). They give
the same continuum limit and the same leading-dim-4 operator, and
differ only at higher dimensions where Symanzik power-counting
treats them as equivalent improvements.

### Honest verdict on Attack 5

**Strong partial positive — but weaker than originally claimed.**

Attack 5 establishes that:
- (a) RP excludes negative-coefficient improvement terms.
- (b) Combined with substrate combinatorics (Attack 3), minimal-carrier
  (Attack 2 / scope-clarification 1), and Symanzik power-counting,
  the leading-dim-4 magnetic operator is `α Re Tr_F(U_p) + β`.

But Attack 5 does NOT establish that:
- (c) Higher-character corrections are absent; they are
  Symanzik-irrelevant in the long-wavelength limit but not
  forbidden by RP.
- (d) Heat-kernel and Manton actions are excluded; they are
  RP-compatible and give the same continuum limit. They differ
  only at finite-β / finite-spacing in the higher-character
  corrections, exactly as already documented in the no-go note
  ([`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md)).

The honest interpretation: **A2.5's content closes if** the audit
lane accepts the universal Symanzik power-counting argument as
rendering all higher-character corrections (including the heat-kernel
/ Manton differences) Symanzik-irrelevant in the continuum limit. If
so, A2.5 is a derived consequence of existing primitives + universal
QFT power-counting.

If the audit lane demands closure at **finite β** as well, A2.5 cannot
be derived — the existing no-go
([`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md))
stands at finite β even after this note's analysis.

### Sharp residuals

Three sharp residuals remain after Attack 5's analysis:

**Residual R1: spatial plaquettes.** The RP factorization runs
along the temporal axis; spatial plaquettes (those entirely in `Λ_+`
or `Λ_-`) do not directly cross the reflection plane. The
spatial-plaquette form is constrained by lattice symmetry under the
spatial cubic point group `O_h`: spatial plaquettes `p_{12}, p_{13},
p_{23}` are `O_h`-equivalent, and their form must be the same. By
Hamilton-limit matching (Block B), the form must reproduce the
temporal-plaquette form. This residual is closeable in audit by the
standard "isotropic Wilson plaquette" argument; we don't reproduce
the proof here but flag it as a non-load-bearing extension.

**Residual R2: distinguishing Wilson from heat-kernel and Manton.**
At the level of dim-4 leading operator with positive character
coefficients, **all three are equivalent** — they all give the
canonical `α Re Tr_F(U_p) + β` form at leading dimension, with
higher characters as Symanzik corrections. The differences are
finite-β: heat-kernel has `c_λ ∝ d_λ e^{-(t/2)C_2(λ)}`, Wilson has
Bessel-determinant coefficients, Manton has geodesic-distance
coefficients. RP does not force one over the others.

This is the same residual the existing no-go
([`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md))
identifies. **Attack 5 does not close this residual on its own**.

The closure path is via Symanzik power-counting (Step 5 below): at
the leading dim-4 operator, all three actions agree; the distinct
finite-β behavior is a finite-spacing artifact that vanishes in
the continuum limit `a → 0`. So the framework's *continuum* prediction
is unique modulo the `g_bare = 1` gate; the *finite-β* prediction
is action-form ambiguous as the no-go states.

**Residual R3: `(Re Tr_F(U_p))^k` polynomial corrections for `k ≥ 2`.**
These are dim ≥ 8 operators by Symanzik power-counting, and are
RP-compatible with positive coefficient. They are admitted as Symanzik
corrections in the standard QFT power-counting framework.

### Verdict

**Strong positive partial — with sharper boundary than originally claimed.**

Attack 5, combined with Attacks 2 and 3, establishes:

(a) The leading-dim-4 magnetic operator on a 1×1 plaquette is
`α Re Tr_F(U_p) + β`, modulo `g_bare = 1` and the Block B
continuum-matching constraint.

(b) Higher-character or higher-power corrections are dim ≥ 8 and
Symanzik-irrelevant in the continuum limit.

(c) Negative-coefficient improvements are RP-excluded.

But it does NOT establish:

(d) Heat-kernel and Manton actions are excluded — they are RP-
compatible at all orders and give the same continuum limit. The
finite-β differences are exactly the residual the existing no-go
identifies.

**Net effect on A2.5:** A2.5 is *partially* derivable — its
"Wilson-form at leading dim" content reduces to a derived theorem
from RP + Tr-form + Z³ substrate + Symanzik (Steps 1–5 below in
the companion theorem note). Its "uniqueness at finite β" content
is NOT derivable from existing primitives — the existing no-go
is correct and stands.

This is a **sharper but more honest** result than admitting A2.5 as
an axiom: under the framework's existing primitives, the Wilson-form
prediction is the canonical leading-dim-4 prediction in the continuum
limit, and the finite-β action-form ambiguity is real and structural
(no-go is correct).

### Cross-reference

The RP-forcing argument above is *strongly suggested* by the
existing RP theorem's own commentary
([`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`, line 251-254](../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md))
which explicitly notes that the OS factorization works for Wilson
form and not for "improved actions with negative-coefficient
rectangles". Attack 5 promotes that observation from a comment to
a derivation: it's not just that "A4's accepted plaquette surface
forbids alternatives", but that **RP itself forbids them** — so
A4's restriction is itself derived, not admitted.

This sharper reading is consolidated in the companion theorem note
[`A2_5_DERIVED_THEOREM.md`](A2_5_DERIVED_THEOREM.md).

---

## Attack 6 — Single-clock + Lieb-Robinson constraint on multi-traversal

### Hypothesis

Lieb-Robinson velocity bounds may forbid magnetic operators whose
Heisenberg-evolution propagates "around the loop multiple times"
within a single time slice, forcing single-traversal for
microcausal consistency.

### Attempt

The retained Lieb-Robinson bound
([`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](../../docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md))
states

```
‖ [α_t(O_x), O_y] ‖_op ≤ 2 ‖O_x‖ ‖O_y‖ exp(-d(x,y) + v_LR |t|)
```

with `v_LR = 2 e r J`. The bound applies to *Heisenberg evolution*
of operators under the reconstructed Hamiltonian.

For Lieb-Robinson to constrain the magnetic operator's traversal
count, the multi-traversal structure of `Tr_F(U_p^k)` would have to
generate larger Lieb-Robinson velocity than the single-traversal
form. Specifically: if `Tr_F(U_p^k)` were equivalent to summing the
Hamiltonian over `k`-fold-iterated plaquettes, the local J would
scale as `J · k`, and `v_LR = 2 e r J` would scale linearly in `k`.

**The obstruction.** Lieb-Robinson velocity is defined relative to the
Hamiltonian's range, not its functional content. `Tr_F(U_p^k)` is
still supported on the **same** four lattice links as `Tr_F(U_p)` —
the four corners of the 1×1 plaquette. The Lieb-Robinson range `r =
1` is the lattice radius of the operator, and that's `r = 1` for
both `Tr_F(U_p)` and `Tr_F(U_p^k)`.

The norm `‖h_p‖_op` does change between the two — `Tr_F(U_p^k)`
has `‖·‖_op ≤ N_c = 3` (since `|Tr_F(U)| ≤ N_c`), and
`(Re Tr_F(U_p))^k` has `‖·‖_op ≤ N_c^k` — so `J` scales differently
for different forms. But these are constants, not range-dependent
quantities. The Lieb-Robinson velocity rescales by a constant, but
the **causal structure** is preserved.

Equal-time strict locality (M1) holds for any of these operator
choices, since they are all supported on the same lattice site
algebra at fixed time. Lieb-Robinson does not distinguish them.

### Verdict

**Specific obstruction.** Lieb-Robinson velocity is a constant
multiplier on the lightcone slope; it does not depend on whether
the magnetic operator is `Tr_F(U_p)` or `Tr_F(U_p^k)`, since both
are supported on the *same* four-link plaquette region. Microcausality
forbids out-of-lightcone signaling but is *agnostic* about the
operator-dimensional content of an in-lightcone term.

### Reusable conclusion

Lieb-Robinson constrains spatial range and propagation speed; it
does not constrain power-counting of operators of equal range.
Future attempts to use causality as a power-counting selector
will fail because causality is range-bounded, not dimension-bounded.

---

## Synthesis

The six attack vectors give a clean partition:

**Vectors 1, 4, 6 are definitively closed as obstructions:**
- Algebra cohomology (Hochschild) is trivial on Cl(3) (separable
  simple algebra in char 0).
- Algebra-of-observables polynomial closure on a single plaquette
  *is* the full SU(3) character ring.
- Lieb-Robinson is range-restricting, not dimension-restricting.

**Vectors 2, 3 give clean partial positive results:**
- Vector 2 forces **fundamental rep** (rules out higher-rank rep
  traces such as `Tr_(2,0)`, `Tr_(1,1)`), but not single-traversal.
- Vector 3 forces **1×1 plaquette as the minimal closed loop on Z³**
  via cubical CW-complex / Stokes / isoperimetric inequality.

**Vector 5 gives a sharper-but-more-restricted positive result than originally hoped:**
- RP rules out **negative-coefficient improvements** (e.g.,
  Lüscher-Weisz with negative `c_1`).
- RP does NOT distinguish Wilson from heat-kernel from Manton at
  finite β; all three have positive character expansions and are
  RP-compatible.
- The Wilson-form leading-dim-4 operator `α Re Tr_F(U_p) + β` is
  the unique `O_h`-symmetric, single-plaquette, primitive-trace,
  RP-positive form **at the dim-4 level** — so at the continuum
  level (where dim > 4 corrections vanish), the framework predicts
  Wilson-form uniquely modulo `g_bare`.

**Combined**, vectors 2, 3, 5 derive A2.5's **continuum-limit**
content from existing primitives + standard QFT Symanzik
power-counting:

| A2.5 content | Derived in vector | Status |
|---|---|---|
| "fundamental trace `Tr_F` not higher reps" | 2 | Sufficient |
| "elementary 1×1 plaquette is the minimal closed loop" | 3 | Sufficient |
| "RP excludes negative-coefficient improvements" | 5 | Sufficient |
| "Wilson-form `α Re Tr_F` is the unique leading-dim-4 form" | 2+3+5+Symanzik | Sufficient in continuum |
| "Wilson uniquely selected at finite β" | — | NOT derivable from existing primitives |

The **finite-β residual** matches the existing no-go
([`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md))
exactly. Heat-kernel, Wilson, and Manton are all RP-compatible
at finite β, give the same continuum limit, and differ at finite
β by Symanzik-irrelevant higher-character corrections. This
residual is *structural*, not a research-effort gap.

## Recommendation

1. **The Attack-3 + Attack-2 + Attack-5 (continuum-limit half) chain
   is a derived theorem candidate**: see
   [`A2_5_DERIVED_THEOREM.md`](A2_5_DERIVED_THEOREM.md) for the
   audit-grade write-up. This closes A2.5's continuum content as a
   derived theorem; it does NOT close the finite-β residual.

2. **Submit the derived-theorem candidate to the independent audit
   lane.** If audited clean, A2.5 reduces from a proposed axiom to
   a derived theorem **for the continuum-limit content**. The
   finite-β action-form ambiguity remains open per the existing
   no-go.

3. **The bridge gap closes at the continuum level** modulo the open
   `g_bare = 1` gate
   ([`G_BARE_DERIVATION_NOTE.md`](../../docs/G_BARE_DERIVATION_NOTE.md))
   and the Hamilton-limit / multi-plaquette extrapolation
   ([`G_BARE_3PLUS1_REFRAMING.md`](G_BARE_3PLUS1_REFRAMING.md)). The
   bridge gap **remains open at finite β** as the existing no-go
   states.

4. **Stop spending effort on Attacks 1, 4, 6.** The obstructions
   there are structural and definitive; future cycles should not
   revisit them. In particular:
   - Don't attempt to derive operator-form properties from Cl(3)
     algebra cohomology (Attack 1: Hochschild vanishing).
   - Don't attempt to derive operator-form properties from
     algebra-of-observables polynomial closure (Attack 4:
     character ring closes the polynomial closure).
   - Don't attempt to derive operator-form properties from
     Lieb-Robinson velocity (Attack 6: same range, same lightcone,
     no power-counting selectivity).

5. **The sharper boundary**: the finite-β action-form ambiguity is
   *not* admitting a "wrong answer"; it is a real structural feature
   of the framework that the framework predicts uniquely **only in
   the continuum limit** and is action-form-ambiguous at finite-β.
   This is consistent with the standard physics view that lattice
   QFT is a regularization, not the physical theory; the physical
   theory is the continuum limit, and the framework predicts that
   uniquely.

## What this note is not

- not a unilateral axiom-set change
- not a claim that the bridge gap is closed (still open at
  `g_bare = 1` gate)
- not a substitute for the audit verdict on either A2.5 or the
  derived-theorem candidate

## Cross-references

- [`A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md`](A2_5_AUDIT_GRADE_HOSTILE_REVIEW.md) — original A2.5 proposal + 5-attack hostile review
- [`A2_5_DERIVED_THEOREM.md`](A2_5_DERIVED_THEOREM.md) — companion theorem note (Attack 5 + 3 + 2 consolidated)
- [`BLOCK_B7_PRIMITIVE_OPS_FORCING.md`](BLOCK_B7_PRIMITIVE_OPS_FORCING.md) — original B.7 forcing argument
- [`BLOCK_B_HAMILTONIAN_DERIVATION.md`](BLOCK_B_HAMILTONIAN_DERIVATION.md) — KS Hamiltonian under canonical Tr-form
- [`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](../../docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md) — prior no-go on action-form uniqueness
- [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md) — RP theorem the load-bearing input of Attack 5
- [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](../../docs/AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md) — single-clock theorem
- [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](../../docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md) — microcausality theorem (used in Attack 6)
- [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](../../docs/SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md) — Casimir support
- [`G_BARE_RIGIDITY_THEOREM_NOTE.md`](../../docs/G_BARE_RIGIDITY_THEOREM_NOTE.md) — successful uniqueness-from-primitives template

## Standard external references

- Hochschild, G. (1945), "On the cohomology groups of an associative
  algebra," *Ann. Math.* 46, 58.
- Cartan, H. & Eilenberg, S. (1956), *Homological Algebra*, Princeton
  Univ. Press, ch. IX (separable algebras and HH^* vanishing).
- Loday, J.-L. (1992), *Cyclic Homology*, Springer, ch. 1 (Hochschild
  complex of an algebra).
- Weibel, C. A. (1994), *An Introduction to Homological Algebra*,
  Cambridge Univ. Press, §9.2.1 (Wedderburn-Hochschild-Whitehead
  theorem).
- Cvitanović, P. (2008), *Group Theory: Birdtracks, Lie's, and
  Exceptional Groups*, Princeton Univ. Press, ch. 9 (SU(N) character
  identities, Newton-Frobenius).
- Frobenius-Schur character power identities (standard Lie-rep theory).
- Hatcher, A. (2002), *Algebraic Topology*, Cambridge Univ. Press,
  ch. 2 (CW complexes, cubical realisations, isoperimetric inequality
  on Z²).
- Osterwalder, K. & Seiler, E. (1978), "Gauge field theories on the
  lattice," *Ann. Phys.* 110 (the OS Cauchy-Schwarz / link-reflection
  factorization).
- Sharatchandra, H. S., Thun, H. J., Weisz, P. (1981), *Nucl. Phys. B*
  192, 205 (staggered RP factorization, Step 5's pairing of `A_+`
  with `θ(A_+)`).
- Lieb, E. H. & Robinson, D. W. (1972), *Comm. Math. Phys.* 28, 251
  (Lieb-Robinson velocity bound).
