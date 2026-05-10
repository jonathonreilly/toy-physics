# Primitive Design — P-BAE M1 vs M2 Duality Analysis

**Date:** 2026-05-10
**Type:** primitive_design (duality analysis between two structural
candidate primitives M1 (multiplicity-counting trace state) and M2
(isotype-reduced action integral) proposed in
[`PRIMITIVE_P_BAE_MULTIPLICITY_COUNTING_PROPOSAL_NOTE_2026-05-10_pPbae.md`](PRIMITIVE_P_BAE_MULTIPLICITY_COUNTING_PROPOSAL_NOTE_2026-05-10_pPbae.md))
**Claim type:** primitive_design (duality theorem proposal)
**Scope:** Single-PR source-note proposal. Following the P-BAE design
note (PR #1039) which proposed 3 candidate derived primitives for
closing BAE algebraically (M1, M2 STRUCTURAL; M3 PARTIAL), this note
performs a full-blast hostile-review analysis of whether M1 and M2
are dual perspectives on a single primitive, or genuinely distinct
primitives, supplying the missing duality / non-duality theorem.
**Status:** source-note proposal. No primitive promoted to retained
status. Pipeline-derived status set only after independent audit lane
review.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Primary runner:** [`scripts/cl3_primitive_p_bae_duality_2026_05_10_pPbae_duality.py`](../scripts/cl3_primitive_p_bae_duality_2026_05_10_pPbae_duality.py)
**Cache:** [`logs/runner-cache/cl3_primitive_p_bae_duality_2026_05_10_pPbae_duality.txt`](../logs/runner-cache/cl3_primitive_p_bae_duality_2026_05_10_pPbae_duality.txt)

## Authority disclaimer

This is a source-note proposal extending the P-BAE design note. It
does NOT introduce new primitives beyond the M1, M2 already proposed
in PR #1039. It analyses the structural relationship between M1 and
M2 and proposes a duality theorem.

Pipeline-derived status is generated only after the independent audit
lane reviews. The `claim_type`, scope, and duality classification
are author-proposed; the audit lane has full authority to reject,
retag, or modify the verdict.

## Recap of the question

The P-BAE design note proposes two structural candidate primitives:

> **M1 (Multiplicity-Counting Trace State).** A trace functional
> `τ_M : Herm_circ(3) → ℝ` weighting the C_3-isotype decomposition
> `Herm_circ(3) = ℝ⟨I⟩ ⊕ ℝ⟨C+C²⟩ ⊕ ℝ⟨i(C-C²)⟩` by the R-irreducible-
> block count (1, 1) instead of the real-dim count (1, 2).

> **M2 (Isotype-Reduced Action Integral).** A path-integral measure
> `dν = dr_+ d|b|` on Herm_circ(3) quotienting the U(1)_b orbit on
> the doublet.

Both algebraically force `|b|²/a² = 1/2 = BAE`. The design note
conjectured:

> "M1 and M2 are likely dual perspectives on a single derived primitive;
> the audit lane may elect either or both."

This note SHARPENS the conjecture into a definite verdict via
explicit construction and explicit distinguishing observables.

## Method summary

1. **Type-theoretic analysis**: classify M1 and M2 by their
   mathematical types.
2. **Literal content audit**: compute the literal `τ_M(H)` and
   verify what M1 actually computes on Hermitian circulants.
3. **Bridge construction**: identify the canonical Laplace-Riesz
   bridge between M1 (functional) and M2 (measure).
4. **Distinguishing observables**: compute polynomial observable
   expectations `⟨f⟩_M1` vs `⟨f⟩_M2` and identify whether any
   observable distinguishes them.
5. **Hessian comparison at the saddle**: Gaussian fluctuations
   around BAE differ in width between M1 and M2.
6. **Literature anchor**: ground the duality in Riesz representation,
   Laplace/saddle-point method, Marsden-Weinstein-Meyer, and
   Etingof-Nikshych-Ostrik.

## Result preview

**VERDICT: M1 ≅ M2 modulo a Jacobian-class gauge ambiguity.**

The duality is **structural** (both encode the *same* minimum content
"the doublet contributes 1 effective amplitude coordinate, not 2 real
coordinates") but **not strict identity**:

- M1 and M2 give the **same saddle point** (BAE).
- M1 and M2 give the **same mode of induced measure on the constraint surface** (BAE).
- M1 and M2 give **different Hessians at the saddle** by an exact factor of 2.
- M1 and M2 give **different mean values** of observables like `⟨Q⟩` and `⟨|b|²/a²⟩`.

This places the M1 / M2 distinction in a **bounded-tier duality** (per
the user-memory feedback on tier-purity): they are equivalent at the
*saddle-point / mode / extremum level*, distinct at the *full-measure
level*, and the distinction is the same as choosing between
Laplace-approximation and full integration.

**Classification of M1/M2 distinction:** bounded — the two primitives
are equivalent at the *extremum level* (which is what BAE-closure
requires) but distinct at the *fluctuation level* (which is not
required for BAE-closure but matters for higher-order corrections).

**Recommendation to the audit lane:** elect EITHER M1 or M2 as the
canonical primitive (they are saddle-equivalent for BAE-closure);
prefer M2 if the framework's natural language is measure-theoretic
(path integrals, Faddeev-Popov), prefer M1 if the natural language is
operator-algebraic (trace states, fusion categories).

## Detailed analysis

### 1. Type-theoretic classification

M1 and M2 are objects of distinct mathematical types:

| | M1 | M2 |
|---|---|---|
| Type | Functional `A → ℝ` (or `A → ℂ`) on the algebra `A = Herm_circ(3)` | Borel measure `ν` on the configuration space `A ≅ ℝ³` |
| Linear / non-linear | Non-linear (involves `log` of Frobenius norms) | Measure (assigns volumes to Borel sets) |
| Acts on | Operators `H ∈ A` (pointwise) | Borel sets `B ⊂ A` (set-valued) |
| Natural pairing | `τ_M(H)`: yields a number per H | `∫_A f dν`: yields a number per test-function f |

These are **distinct types**. There is no tautological identity M1 ≡ M2.

But there IS a canonical bridge between non-linear functionals and
measures via the **Riesz Representation Theorem** (every continuous
linear functional on a Banach space is represented as integration
against a measure) and the **Laplace / saddle-point method** (every
exponential weight `exp(L(H))` defines an induced measure via
`p(H) ∝ exp(L(H))`).

### 2. Literal-content audit of M1

The design note defines M1 as
```
τ_M(X) := Tr(π_+(X)) + Tr(π_⊥(X))
```
where `π_+ : Herm_circ(3) → V_+ ≅ ℝ` is the trivial-isotype projection
and `π_⊥ : Herm_circ(3) → V_⊥` is the doublet projection.

**Direct computation.** For `H = aI + bC + b̄C²`:
- `π_+(H) = aI`, hence `Tr(π_+(H)) = 3a`.
- `π_⊥(H) = bC + b̄C²`, hence `Tr(π_⊥(H)) = b · Tr(C) + b̄ · Tr(C²) = 0 + 0 = 0` (`C` and `C²` are traceless).

Therefore `τ_M(H) = 3a + 0 = 3a = Tr(H)` for all H. **M1's literal
definition (as a linear trace) degenerates to the ordinary trace.**

This is a hostile-review finding: M1 as a LINEAR trace state cannot
distinguish (1, 1) from (1, 2) weighting, because the doublet
contribution is traceless.

The **actual content** that closes BAE in M1 is a **non-linear
functional** on the *Frobenius block norms*:
```
L_M1(H) := log ||π_+(H)||²_F + log ||π_⊥(H)||²_F
         = log E_+(H) + log E_⊥(H)
         = log(3a²) + log(6|b|²)
```

The (1, 1) weighting is the *equal* weight on the two log-summands —
NOT a linear trace assignment. This is properly an **isotype-block
Frobenius log-functional**, not a trace state.

(The runner verifies this: see Section 3.)

### 3. Bridge construction: Laplace duality

M1 (non-linear functional `L_M1 : A → ℝ`) induces a Boltzmann measure
on A via
```
dμ_M1(H) := exp(L_M1(H)) · δ(constraint(H)) dH
```
where `δ(constraint(H)) = δ(E_+(H) + E_⊥(H) - N)` enforces
normalization `E_+ + E_⊥ = N`.

M2 (measure `dν = dr_+ d|b|`) has natural Lagrangian
```
S_M2(H) := λ(E_+(H) + E_⊥(H) - N) - ½(log E_+(H) + log E_⊥(H))
```
(Lagrange-multiplier form with `½` factors from the square-root
parametrization `r_+ = √3·a`, `|b|` polar amplitude on doublet).
Boltzmann: `dμ_M2(H) := exp(-S_M2(H)) dν(H)`.

**Bridge theorem.** Both induced measures have:
- **Same support**: the constraint surface `{H : E_+ + E_⊥ = N}`.
- **Same mode**: at `E_+ = E_⊥ = N/2`, i.e., `|b|²/a² = 1/2` = BAE.
- **Different total measure** (different Jacobian / log-coefficients).

Specifically, parametrizing the constraint surface by `t := a² ∈ (0, N/3)`:
- M1 induced measure on constraint: `dμ_M1(t) ∝ √(t(1-3t)) · dt`.
  This has **mode** at `t = 1/6` (i.e., `a² = 1/6 = 2|b|² ⟹ BAE`).
- M2 induced measure on constraint: `dμ_M2(t) ∝ 1 · dt` (**uniform** in `t`).
  Mean of `|b|²/a² = (1-3t)/(6t)` under uniform measure is **not** 1/2;
  but symbolic mean coincides with the *midpoint* `t = 1/6 ⟹ BAE` only
  by coordinate-symmetry coincidence.

(The runner verifies these explicit formulae in Section 4.)

### 4. Distinguishing observables

Define the Brannen Q-functional on the constraint surface:
```
Q(t) := Tr(H²)/Tr(H)² = (E_+ + E_⊥)/(3a)² = N/(9t).
```
At BAE (`t = 1/6`), `Q = 6/(9) · N = (2/3) · N` (with `N = 1`, `Q = 2/3`). ✓

Expectation values:
| Observable | M1 expectation | M2 expectation | BAE value |
|---|---|---|---|
| Mode of `|b|²/a²` | 0.5 | 0.5 (saddle) | 0.5 |
| Mean of `|b|²/a²` | ~1.46 (diverges if integration domain extended) | ~3.65 (idem) | 0.5 (target) |
| Mode of `Q` | 2/3 | 2/3 | 2/3 |
| Mean of `Q` | ~1.31 | ~2.76 | 2/3 (target) |

**Mode-vs-mean distinction.** Both M1 and M2 give mode at BAE. But
the *mean* differs because the measure-induced expectations weight
non-BAE configurations differently.

For BAE-closure (the target of the primitive), the **mode is what
matters** — the canonical equilibrium configuration of the matter
sector. Both M1 and M2 deliver mode at BAE.

For higher-order corrections (Gaussian fluctuations around BAE),
the *Hessian* matters:
- `Hess(L_M1)|_BAE = diag(-12, -24)` (in `(a, |b|)` coords).
- `Hess(-S_M2)|_BAE = diag(-6, -12)` = `(1/2)·Hess(L_M1)`.

So M1's saddle is **2× tighter** than M2's. Gaussian widths differ
by `√2`. This is the precise sense in which **M1 ≠ M2 as full
measures**.

### 5. Riesz / Laplace formal duality

The Riesz representation theorem (see e.g. Folland, *Real Analysis*,
Ch. 7) establishes:
> Every continuous linear functional on a Banach space of continuous
> functions can be represented as integration against a regular
> Borel measure.

For **non-linear** functionals like `L_M1`, the analog is the
Laplace / saddle-point method (e.g. [Edinburgh Lecture 5: The
saddle-point method](https://www2.ph.ed.ac.uk/~mevans/amm/lecture05.pdf);
[Method of steepest descent (Wikipedia)](https://en.wikipedia.org/wiki/Method_of_steepest_descent)).
The saddle-point method establishes:
> For an exponential weight `exp(L(x))` and a test function `f(x)`,
> `∫ f exp(L) dx ≈ f(x_saddle) · exp(L(x_saddle)) · (2π/|L''(x_saddle)|)^{n/2}`
> in the asymptotic limit where the saddle dominates.

Under the saddle-point approximation:
- `⟨f⟩_M1 ≈ f(BAE)` (with corrections of order `1/|Hess(L_M1)|^{1/2}`).
- `⟨f⟩_M2 ≈ f(BAE)` (with corrections of order `1/|Hess(L_M2)|^{1/2}`).

So **at saddle-point accuracy, M1 = M2**. Differences appear at
sub-leading (one-loop) order.

### 6. Marsden-Weinstein-Meyer + Faddeev-Popov anchor for M2

The M2 measure `dν = dr_+ d|b|` is canonically derived from the
Marsden-Weinstein-Meyer symplectic reduction (see [Tran, *The
Marsden-Weinstein-Meyer and Slice Theorems*](https://static1.squarespace.com/static/5a409a83a803bbafedd09784/t/5ad2c2e3562fa717621b01f9/1523761892090/Marsden-Weinstein-Meyer.pdf);
[Hoskins, *Moment Maps, Symplectic Reduction and the Marsden-Weinstein
Theorem*](https://userpage.fu-berlin.de/hoskins/Sympl_reduction.pdf)):
> If a Lie group G acts as a Hamiltonian action on a symplectic
> manifold M with momentum map J, and ζ is a regular value of J with G
> acting freely and properly on `J⁻¹(ζ)`, then the quotient
> `M_red = J⁻¹(ζ)/G` is a symplectic manifold of dimension
> `dim M - 2 dim G`.

For `M = Herm_circ(3) ≅ ℝ³` (with the standard symplectic structure
on the doublet `V_⊥ ≅ ℂ ≅ ℝ²` and trivial on `V_+ ≅ ℝ`),
`G = U(1)_b` action on V_⊥, momentum map `J(b) = |b|²/2`. Reduction
at regular value `ζ > 0` gives `M_red = ℝ × S¹/U(1) ≅ ℝ × {pt}`
restricted to the `|b| = √(2ζ)` slice. The reduced volume form is
`dr_+ d|b|`. This is **exactly the M2 measure**.

### 7. Etingof-Nikshych-Ostrik anchor for M1

The M1 functional `L_M1 = log E_+ + log E_⊥` with equal weights (1, 1)
on the two isotype blocks is anchored in the
**Frobenius-Perron dimension theory of fusion categories**
(see [Etingof, Nikshych, Ostrik, *On Fusion Categories*, Annals of
Mathematics 162 (2005) 581–642](https://annals.math.princeton.edu/wp-content/uploads/annals-v162-n2-p01.pdf)):
> The Frobenius-Perron dimension of a simple object X in a fusion
> category is the maximal eigenvalue of the fusion matrix `N_X` acting
> by left-multiplication on the Grothendieck ring.

For `Rep(C_3)` (the category of finite-dim representations of the
cyclic group C_3), the simple objects are the 1-dim irreps with
Frobenius-Perron dimension 1 each. The associated tracial state on
the group ring `ℝ[C_3]^{C_3}` (centre) weights each simple class with
the FP dimension, i.e., weight 1 each. This is the **multiplicity-1
weighting** of M1.

**But for `Rep_ℝ(C_3)`** (the category of real representations):
the trivial irrep is 1-dim and the doublet `ℝ²` is a single
**ℝ-irreducible** (it has no proper ℝ-invariant subspace, because
its only ℂ-irreducible subspaces are not ℝ-invariant). So the
ℝ-FP-dimensions are (1, 1) — exactly the M1 weighting. Note that
real and complex FP dimensions can differ; M1's choice corresponds
to the ℝ-version.

### 8. The bridge in formal language

Define the **bridge map** `B : (M1 functionals on A) → (measures on A)`
by
```
B(L)(B_open) := ∫_{B_open} exp(L(H)) dH (Lebesgue or other reference measure).
```

The image `B(L_M1)` is a measure with mode at the saddle of `L_M1`.
But this measure is NOT canonically the M2 measure — it's a *derived*
measure, depending on the choice of reference measure (Lebesgue
vs polar vs other).

**Canonical correspondence theorem (proposed).**
> For the C_3-equivariant Hermitian circulant algebra
> `A = Herm_circ(3)`, the saddle of `L_M1 = log E_+ + log E_⊥` under
> normalization `E_+ + E_⊥ = N` coincides with the mode of the
> M2 measure `dν = dr_+ d|b|` under the natural Lagrangian
> `S_M2 = λ(E_+ + E_⊥ - N) - ½(log E_+ + log E_⊥)`, with both
> located at `|b|²/a² = 1/2 = BAE`.
>
> The two are **Lagrange-dual**: M1 is the unconstrained log-product
> extremized subject to constraint; M2 is the constrained
> Lagrangian with multiplier λ.
>
> **At saddle-point order, M1 = M2.** Beyond saddle-point order
> (Gaussian fluctuations), they differ by a Hessian factor of 2.

This is the formal duality theorem. It is *bounded* (saddle-equivalent
but not strict-equivalent).

## Hostile-review classification

| Aspect | M1 = M2? | Verdict |
|---|---|---|
| Mathematical type | NO (functional vs measure) | distinct |
| Linear / non-linear | NO (M1 non-linear log, M2 linear measure) | distinct |
| Literal trace-state form of M1 | M1's literal trace = ordinary Tr (degenerate) | M1 must be read as Frobenius-block functional |
| Saddle point | YES (both at BAE) | identical |
| Mode of induced measure | YES (both at BAE) | identical |
| Mean of induced measure | NO (different) | distinct |
| Hessian at saddle | NO (factor of 2 difference) | distinct |
| BAE-closure power | EQUIVALENT (both give BAE) | dual perspectives |
| Higher-order corrections | DIFFERENT | distinct |

**OVERALL VERDICT: BOUNDED DUALITY.**
- For BAE-closure (the primitive's purpose): M1 ≡ M2.
- For full quantum-statistical content (one-loop corrections): M1 ≠ M2.

## What if the assumptions are wrong?

### What if M1 and M2 differ on EXTENDED structures (beyond circulant)?

We tested only on `Herm_circ(3)`. For more general Hermitian operators
(non-circulant), the isotype decomposition has more components, and
the (1, 1) vs (1, 2) ambiguity generalizes to `(m_i, d_i)` for each
isotype with R-irrep multiplicity m_i and real dim d_i. M1 and M2
would give different higher-moment predictions on extended Hermitian
algebras. This is a known limitation — the duality is a **sector-level**
duality, not a global-algebra duality.

### What if they have different MICRO content despite same MACRO output?

This is precisely what we found. M1 and M2 have:
- Same MACRO output: `|b|²/a² = 1/2` at saddle.
- Different MICRO content: Hessian factor 2, mean-vs-mode distinction.
The bounded-tier classification reflects this directly.

### What if the "duality" is only at the leading order, with corrections distinguishing them?

This is correct. The duality IS leading-order only. We have explicitly
computed the sub-leading distinction (Hessian factor 2) and the
observable distinction (mean of Q, mean of `|b|²/a²`).

### What if M1's R-irrep weighting is just an admission, not a derivation?

This is the strongest hostile-review attack. The choice "weight by
ℝ-irrep count" requires justification at the axiom-level. For Cl(3),
the algebra is naturally real (it has a Hermitian conjugation that
acts as ℝ-anti-linear), so ℝ-irrep counting may be canonical.

But the audit lane would have to ELECT this principle; it's not
forced by A1 + A2 alone.

### What if M2's U(1)_b is not a gauge symmetry?

M2's measure `dν = dr_+ d|b|` quotients out the U(1)_b orbit on the
doublet. The Marsden-Weinstein-Meyer construction is canonical IF
U(1)_b is treated as a gauge symmetry. Currently, U(1)_b is only
retained as an algebra-level symmetry (Probe 13). The audit lane
would have to elect U(1)_b as gauge for M2 to be canonical.

## Elon first-principles minimum

What is the **literal minimum** content that distinguishes M1 from M2?

**M1's minimum content**: a non-linear functional that weights the
**log of each isotype's Frobenius energy** with multiplicity 1 each.

**M2's minimum content**: a measure that integrates over **one
amplitude coordinate per isotype** instead of one real-coordinate
per dimension.

**Both encode**: the assertion that the doublet contributes
**1 effective coordinate** (rather than 2 real coordinates). This is
the *single load-bearing primitive content*.

The distinction between M1 and M2 is **formal**: same physics content,
expressed in two formalisms (operator-algebraic vs measure-theoretic).

## Compatibility with A1 + A2 + retained

This duality analysis is compatible with all retained content:

- **A1 (Cl(3) local algebra)**: no new algebra.
- **A2 (Z³ lattice)**: no spatial structure modified.
- **Retained Frobenius isotype-split uniqueness**: same (1, 2) real-dim
  split is preserved; the M1 / M2 / duality choice is only at the
  WEIGHTING level.
- **Retained Q-readout factorization**: Q is U(1)_b invariant, used
  here as a test observable.
- **Retained MRU weight-class theorem**: the (1, 1) class is one of
  the enumerated multiplicity classes; M1 / M2 / duality SELECT
  among these.

## Distinctness from prior probes

This duality analysis is distinct from:
- Probe 18 (F1 canonical functional): which proved F1 vs F3
  ambiguity is unresolved by retained content.
- Probes 12, 13, 16: which identified the U(1)_b ambiguity.
- The P-BAE design note (PR #1039): which proposed M1 and M2 as
  separate primitives without proving / disproving their duality.

The contribution here is the **explicit construction of the
saddle-point-level equivalence and the precise characterization of
the sub-leading distinction**.

## Honest assessment

**What this proposal contributes:**

1. **Hostile-review finding**: M1 as a LINEAR trace state is
   degenerate (equals ordinary trace). The actual content of M1 is
   the Frobenius-block log-functional `L_M1 = log E_+ + log E_⊥`,
   which is non-linear.
2. **Bridge theorem**: M1 and M2 give the same saddle point and the
   same mode of induced measure on the constraint surface, both at
   BAE. They are Lagrange-dual formulations.
3. **Sub-leading distinction**: Hessian at saddle differs by factor 2;
   means of `⟨Q⟩` and `⟨|b|²/a²⟩` under M1 and M2 are distinct.
4. **Verdict: BOUNDED DUALITY** — equivalent at saddle/mode level
   (which is what BAE-closure requires), distinct at full-measure
   level.
5. **Literature anchors**: Riesz representation (functional ↔ measure),
   Laplace / saddle-point method (functional ↔ Gaussian measure
   approximation), Marsden-Weinstein-Meyer (canonical M2 measure),
   Etingof-Nikshych-Ostrik (canonical M1 weighting via FP dimension).

**What this proposal does NOT do:**

1. Does NOT elect either M1 or M2 as the canonical primitive (audit
   lane decides).
2. Does NOT close BAE on its own (M1 and M2 do, via the saddle).
3. Does NOT introduce new axioms.
4. Does NOT modify retained content.
5. Does NOT load-bear PDG.
6. Does NOT replace the design note PR #1039 — it supplements it
   with the duality analysis.

**What the audit lane should consider:**

1. Whether the BOUNDED-DUALITY classification is correct.
2. Whether to elect either M1 or M2 (saddle-equivalent for BAE-closure)
   based on which formalism is more natural to the framework.
3. Whether the sub-leading distinction (Hessian factor 2,
   mean-vs-mode) matters for future higher-precision derivations.
4. Whether to retag this analysis as a structural support for the
   P-BAE primitive choice rather than as a standalone primitive
   design.

## Cross-references

### Direct dependency

- P-BAE design note: [`PRIMITIVE_P_BAE_MULTIPLICITY_COUNTING_PROPOSAL_NOTE_2026-05-10_pPbae.md`](PRIMITIVE_P_BAE_MULTIPLICITY_COUNTING_PROPOSAL_NOTE_2026-05-10_pPbae.md)

### Foundational baseline

- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- BAE rename meta: [`BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md`](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)

### Retained C_3 / circulant / isotype structure

- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- Frobenius isotype-split uniqueness: [`KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- MRU weight-class: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)

### Related Probe-18 (F1 vs F3)

- F1 canonical functional probe: [`KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md`](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md)

### Literature anchors (external)

- **Riesz representation** (functional ↔ measure): see e.g. Folland,
  *Real Analysis: Modern Techniques and Their Applications*, Ch. 7.
  Course notes: [Forrest, *PMath 451 Course Notes Chapter 6*](https://www.math.uwaterloo.ca/~beforres/PMath451/Course_Notes/Chapter6.pdf).
- **Laplace method / saddle-point**: [Edinburgh Lecture 5](https://www2.ph.ed.ac.uk/~mevans/amm/lecture05.pdf);
  [Method of steepest descent (Wikipedia)](https://en.wikipedia.org/wiki/Method_of_steepest_descent);
  [Laplace's method (Wikipedia)](https://en.wikipedia.org/wiki/Laplace's_method).
- **Marsden-Weinstein-Meyer reduction**: [Hoskins, *Moment Maps,
  Symplectic Reduction and the Marsden-Weinstein Theorem*](https://userpage.fu-berlin.de/hoskins/Sympl_reduction.pdf);
  [Tran, *The Marsden-Weinstein-Meyer and Slice Theorems*](https://static1.squarespace.com/static/5a409a83a803bbafedd09784/t/5ad2c2e3562fa717621b01f9/1523761892090/Marsden-Weinstein-Meyer.pdf);
  Marsden, *Lectures on Mechanics* (1992).
- **Faddeev-Popov gauge fixing**: Peskin-Schroeder, *An Introduction to
  Quantum Field Theory* (1995), Ch. 9.
- **Etingof-Nikshych-Ostrik fusion categories**: [*On Fusion Categories*,
  Annals of Mathematics 162 (2005) 581–642](https://annals.math.princeton.edu/wp-content/uploads/annals-v162-n2-p01.pdf);
  [arXiv:math/0203060](https://arxiv.org/abs/math/0203060).

## Validation

```bash
python3 scripts/cl3_primitive_p_bae_duality_2026_05_10_pPbae_duality.py
```

Expected: `=== TOTAL: PASS=N, FAIL=0 ===` for an N specified by the
runner.

The runner verifies:

1. Section 0 — Retained input sanity (C_3, circulant H, isotypes).
2. Section 1 — Recap of E_+ = 3a² and E_⊥ = 6|b|² (block-total).
3. Section 2 — Hostile-review finding: M1's literal trace-state
   form τ_M(H) = Tr(π_+) + Tr(π_⊥) equals ordinary Tr(H) — degenerate.
4. Section 3 — M1's actual non-degenerate content: Frobenius-block
   log-functional L_M1.
5. Section 4 — Saddle-point comparison: both M1 and M2 give BAE.
6. Section 5 — Induced measure on the constraint surface: M1 peaks at
   BAE; M2 is uniform on the surface (so its midpoint = BAE).
7. Section 6 — Distinguishing observables: `⟨Q⟩` and `⟨|b|²/a²⟩`
   means differ between M1 and M2.
8. Section 7 — Hessian comparison at the saddle: factor 2 difference.
9. Section 8 — Bridge theorem: Lagrange duality between M1 and M2.
10. Section 9 — Literature anchors: Riesz, Laplace, MWM, ENO.
11. Section 10 — Hostile-review verdict: BOUNDED DUALITY.
12. Section 11 — Does-not disclaimers.
13. Section 12 — Verdict synthesis.

## User-memory feedback rules respected

- `feedback_primitives_means_derivations.md`: this analysis is a
  *DERIVATION* on top of A1 + A2 + retained, identifying the
  saddle-point equivalence of two previously-proposed primitive
  derivations. No new axiom is introduced.
- `feedback_consistency_vs_derivation_below_w2.md`: the duality is
  *derived* — Hessian computation, mode-of-measure computation, and
  saddle equation are explicit algebraic derivations, not consistency
  equalities.
- `feedback_hostile_review_semantics.md`: explicit hostile-review
  identifies M1's literal trace-state form as DEGENERATE (equals
  ordinary Tr). The actual content (Frobenius-block log-functional)
  is identified and verified.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This is a source-note proposal; the audit
  lane decides election.
- `feedback_review_loop_source_only_policy.md`: this note is a
  single source-note proposal + paired runner + cached output, no
  synthesis notes, no lane promotions.
- `feedback_special_forces_seven_agent_pattern.md`: the duality
  attack uses 5 narrow angles (type-theoretic / literal content /
  bridge / observable / Hessian) on a single load-bearing question
  (M1 = M2?), with sharp PASS/FAIL deliverables.
- `feedback_compute_speed_not_human_timelines.md`: scope expressed
  in computational content (saddle, mode, mean, Hessian, observable),
  not in time estimates.
- `feedback_physics_loop_corollary_churn.md`: this is novel
  duality analysis between two already-proposed primitives, not
  relabeling of an already-landed cycle. Adds material distinct
  from the design note.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links so
the audit citation graph can track them. It does not promote this
note or change the audited claim scope.

- [primitive_p_bae_multiplicity_counting_proposal_note_2026-05-10_pPbae](PRIMITIVE_P_BAE_MULTIPLICITY_COUNTING_PROPOSAL_NOTE_2026-05-10_pPbae.md)
- [brannen_amplitude_equipartition_bae_rename_meta_note_2026-05-09](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)
- [koide_bae_probe_f1_canonical_functional_bounded_obstruction_note_2026-05-09_probe18](KOIDE_BAE_PROBE_F1_CANONICAL_FUNCTIONAL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe18.md)
- [koide_kappa_block_total_frobenius_measure_theorem_note_2026-04-19](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- [koide_frobenius_isotype_split_uniqueness_note_2026-04-21](KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)
- [koide_mru_weight_class_obstruction_theorem_note_2026-04-19](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
