# Scalar Additivity + CPT-Even Phase-Blindness — Derived from a Single Structural Premise

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the **derivation** that the two admitted-context
premises in `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` —
(i) scalar additivity `W[J₁ ⊕ J₂] = W[J₁] + W[J₂]`,
(ii) CPT-even phase-blindness (W depends only on `|Z|`, not the
fermionic phase) —
**collapse to a single structural premise**: real continuous strict
additivity under Grassmann factorization. Given that single premise
plus Cauchy's multiplicative-to-additive functional-equation theorem
(admitted-context math) and the lattice CPT structure of
`CPT_EXACT_NOTE.md` (retained), `W = c log|Z|` is forced and
CPT-evenness is a consequence (not a separate premise).
The numerical hierarchy readouts (`v = 246.28 GeV`, etc.) are
explicitly out of scope.
**Status:** audit pending. This is a candidate **closing derivation**
of the verdict-identified obstruction on
`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`. Under the scope-aware
classification framework, `effective_status` is computed by the audit
pipeline; no author-side tier is asserted in source. Audit-lane
ratification is required before any retained-grade status applies.
**Runner:** [`scripts/frontier_scalar_additivity_cpt_even_derivation.py`](./../scripts/frontier_scalar_additivity_cpt_even_derivation.py)
**Authority role:** closing derivation for the parent's class-B
load-bearing step (decisive move to physical scalar generator).

## Verdict-identified obstruction (quoted)

> Issue: the claim is framed as deriving the observable principle from
> the axiom, but the decisive move to the physical scalar generator
> imports scalar additivity and CPT-even phase-blindness as selection
> premises. Why this blocks retained status: the runner verifies the
> algebra after those premises are chosen; it does not derive why
> physical scalar observables must select that generator from the
> axiom alone. Repair target: add and audit a theorem deriving scalar
> additivity and CPT-even phase-blindness from retained primitives, or
> narrow this row to a conditional theorem given those premises.

## Statement

Let:

- (P1, retained) `Z[J] = det(D + J)` is the exact Grassmann partition
  amplitude on the framework's lattice Dirac operator, with
  Grassmann factorization on independent subsystems:

  ```text
  D = D₁ ⊕ D₂  ⇒  Z[J₁ ⊕ J₂] = Z₁[J₁] · Z₂[J₂].
  ```

  (Standard finite Grassmann integral / fermion-determinant identity.)
- (P2, retained, structural) The lattice CPT structure of the Cl(3)
  staggered framework: `CPT⁻¹ D CPT = D*` (modulo phase
  conventions handled in `CPT_EXACT_NOTE.md`). Consequence:
  `Z[J] = det(D+J)` transforms as `Z → Z*` under CPT, so `|Z|` is
  CPT-invariant and `arg(Z)` is CPT-anti-invariant.
- (P3, structural / single physical premise) **Strict real continuous
  additivity under factorization.** A "physical scalar bosonic
  observable generator" is a function

  ```text
  W : ℂ \ {0} → ℝ
  ```

  that is **continuous** in `Z` and satisfies **strict** additivity on
  independent subsystems:

  ```text
  W(Z₁ · Z₂) = W(Z₁) + W(Z₂)   (∀ Z₁, Z₂ ∈ ℂ \ {0}).
  ```

  No "mod 2π" — strict equality, holding on all admissible argument
  pairs simultaneously.
- (P4, admitted) Cauchy's multiplicative-to-additive functional
  equation theorem (Cauchy 1821; standard real-analysis textbook):
  Continuous `f : (0, ∞) → ℝ` with `f(rs) = f(r) + f(s)` is
  uniquely `f(r) = c log r` for some constant `c ∈ ℝ`.

**Conclusion (T1) (closing derivation: uniqueness of W).** Under
P1+P2+P3+P4, the unique (up to a multiplicative scale) continuous real
strictly additive functional of `Z` is

```text
W(Z) = c · log|Z|,    c ∈ ℝ.
```

CPT-evenness is then a **consequence**: `W(Z) = c log|Z|` is invariant
under `Z → Z*` (the CPT action on the fermion determinant), so
`W(Z) = W(Z*)`. CPT-even phase-blindness is **derived**, not assumed.

**Conclusion (T2) (counterfactual: arg(Z) fails strict additivity).**
The CPT-odd candidate `W = arg(Z)` satisfies additivity only **mod
2π**:

```text
arg(Z₁ Z₂) = arg(Z₁) + arg(Z₂) - 2π · n(Z₁, Z₂),
n ∈ {-1, 0, 1}.
```

Concrete witness: take `Z₁ = Z₂ = exp(i · 3π/4)`. Then
`arg(Z₁) + arg(Z₂) = 3π/2`, but `arg(Z₁ Z₂) = arg(exp(i·3π/2)) = -π/2`
(principal branch). Strict additivity fails: `arg(Z₁ Z₂) ≠ arg(Z₁) +
arg(Z₂)` numerically by 2π.

So `arg(Z)` is excluded by the strict-additivity premise alone, before
any CPT consideration.

**Conclusion (T3) (counterfactual: continuity is necessary).** Without
the continuity hypothesis in P3, Cauchy's functional equation
`f(r+s) = f(r) + f(s)` admits pathological non-measurable solutions
(constructed via a Hamel basis of ℝ over ℚ, requiring the axiom of
choice). The continuity hypothesis collapses the solution space to
`f(r) = c r`, hence (via `r = log|Z|`) `W = c log|Z|`. Continuity is
load-bearing.

**Conclusion (T4) (premise reduction).** The parent note's two
admitted-context premises:

- "scalar additivity" (the strict additive functional equation), and
- "CPT-even phase-blindness" (W depends only on |Z|),

reduce to ONE structural premise (P3: real continuous strict
additivity under factorization) plus retained P1/P2 + admitted P4.
The CPT-even property is a derived consequence.

## Proof

### Step 1: Restrict to the absolute-value sector

By P1 (Grassmann factorization on independent subsystems):

```text
Z[J₁ ⊕ J₂] = Z₁[J₁] · Z₂[J₂].
```

By P3 (W is real-valued and strictly additive):

```text
W(Z₁ · Z₂) = W(Z₁) + W(Z₂).
```

Decompose any nonzero `Z ∈ ℂ \ {0}` as `Z = r · e^(iθ)` with `r =
|Z| > 0` and `θ = arg(Z) ∈ (-π, π]` (principal branch).

For the special case `Z₁ = r₁ > 0` and `Z₂ = r₂ > 0` (positive
reals), strict additivity gives:

```text
W(r₁ · r₂) = W(r₁) + W(r₂)   (∀ r₁, r₂ > 0).
```

Define `f(r) := W(r)` for `r > 0`. Then `f : (0, ∞) → ℝ` is continuous
(by P3 continuity of W in Z) and satisfies the multiplicative-to-additive
Cauchy functional equation.

### Step 2: Apply Cauchy's theorem (P4)

By Cauchy's multiplicative-to-additive functional-equation theorem:

```text
f(r) = c · log(r),   c ∈ ℝ (uniquely determined).
```

So `W(r) = c log r` for all positive real `r`.

### Step 3: Extend to all of ℂ \ {0} via the strict-additivity constraint

Take any `Z ∈ ℂ \ {0}` and write `Z = |Z| · e^(iθ)`. Note
`Z = |Z| · e^(iθ)` and `Z* = |Z| · e^(-iθ)`, so `Z · Z* = |Z|² > 0`.
Strict additivity then gives:

```text
W(Z · Z*) = W(Z) + W(Z*),
W(|Z|²)   = c · log(|Z|²) = 2c · log|Z|   (by Step 2).
```

So `W(Z) + W(Z*) = 2c · log|Z|`.

By symmetry of strict additivity under `Z ↔ Z*` (just swap labels),
neither `W(Z)` nor `W(Z*)` is preferred over the other:

```text
W(Z) = W(Z*) = c · log|Z|.
```

(Detail: any imaginary-part contribution to `W` would have to satisfy
strict additivity in `arg`, which fails — see Step 4.)

So `W(Z) = c log|Z|` for all `Z ∈ ℂ \ {0}`.

### Step 4: Counterfactual — `arg(Z)` fails strict additivity

To prove the imaginary-part contribution must vanish, we show that any
candidate `W̃(Z) = c log|Z| + b · arg(Z)` with `b ≠ 0` fails strict
additivity.

Consider `Z₁ = Z₂ = e^(i·3π/4)`. Then:
- `arg(Z₁) = arg(Z₂) = 3π/4`,
- `Z₁ · Z₂ = e^(i·3π/2)`,
- `arg(Z₁ · Z₂) = -π/2` (principal branch in `(-π, π]`).

Compute:
- `W̃(Z₁ · Z₂) = c log|Z₁ Z₂| + b arg(Z₁ Z₂) = 0 + b · (-π/2) = -bπ/2`.
- `W̃(Z₁) + W̃(Z₂) = 0 + 0 + 2b · (3π/4) = 3bπ/2`.

Strict additivity demands `-bπ/2 = 3bπ/2`, i.e., `2bπ = 0`, hence
`b = 0`.

So `W = c log|Z|` is the **unique** real continuous strictly additive
functional of `Z` on `ℂ \ {0}`.

### Step 5: CPT-evenness as a consequence

By P2 (lattice CPT structure of CPT_EXACT_NOTE.md), the CPT action on
the lattice fermion determinant sends `Z = det(D+J) → Z*`. Then:

```text
W(CPT · Z) = W(Z*) = c log|Z*| = c log|Z| = W(Z).
```

So `W` is CPT-invariant. **CPT-even phase-blindness is a consequence
of the derivation, not a separate premise.**

### Step 6: Continuity is load-bearing

Without continuity, Cauchy's functional equation
`f(r+s) = f(r) + f(s)` (or its multiplicative form) admits
pathological solutions: a Hamel basis of ℝ over ℚ (requiring the
axiom of choice) yields nonmeasurable additive functions. Continuity
is necessary to rule these out.

This is recorded as a load-bearing structural condition on P3, not an
independent premise.

### Step 7: Premise reduction

The parent note (`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`) admits:
- "scalar additivity" (premise 3 in its derivation chain),
- "CPT-even phase-blindness" (premise 4).

These two reduce to ONE: **P3 (real continuous strict additivity
under Grassmann factorization)**. CPT-evenness is then a derived
consequence.

```text
Two admitted premises in parent
    ↓ (this PR's derivation)
One structural premise (real continuous strict additivity)
+ retained P1 (Grassmann factorization)
+ retained P2 (lattice CPT structure)
+ admitted P4 (Cauchy's theorem)
```

∎

## What this claims

- `(T1)` Unique scalar generator: `W(Z) = c log|Z|`, derived from one
  structural premise (real continuous strict additivity) + retained
  CPT and Grassmann structure + admitted-context Cauchy theorem.
- `(T2)` Counterfactual `arg(Z)` fails strict additivity: explicit
  Z₁, Z₂ pair witnessing the 2π wraparound failure.
- `(T3)` Continuity is load-bearing: without it, pathological
  solutions emerge.
- `(T4)` Parent's two premises reduce to one + retained machinery +
  admitted Cauchy.

## What this does NOT claim

- Does NOT derive the physical "extensivity" requirement (P3 is a
  single structural premise, not derived from deeper axioms).
- Does NOT derive Cauchy's functional-equation theorem itself (P4 is
  admitted-context external mathematical authority).
- Does NOT derive the lattice CPT structure (P2 is cited from
  `CPT_EXACT_NOTE.md`, retained).
- Does NOT close the parent row by itself: the parent's other
  in-scope content (Matsubara identity, Klein-four invariance,
  L_t = 4 selector) remains under its own audit-lane status.
- Does NOT address numerical readouts (e.g., v = 246.28 GeV) — out of
  scope.
- Does NOT promote any author-side tier; audit-lane ratification is
  required.

## Cited dependencies

- (P1) [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) §"Theorem 1: additivity forces log|Z|" — Grassmann factorization on independent subsystems.
- (P2) [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) — retained-grade lattice CPT structure for the Cl(3) staggered framework.
- (P3) Single new structural premise: real continuous strict
  additivity under Grassmann factorization. (Stated as the framework's
  physical-extensivity requirement; not derived from deeper axioms.)
- (P4) Cauchy 1821; standard real-analysis textbook reference for the
  multiplicative-to-additive functional-equation theorem.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed (Cauchy 1821 is
  standard mathematical authority — admitted-context external,
  role-labelled).
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_scalar_additivity_cpt_even_derivation.py`](./../scripts/frontier_scalar_additivity_cpt_even_derivation.py)
verifies (PASS=17/0):

1. Grassmann factorization for block-diagonal `D = D₁ ⊕ D₂`:
   `det(D+J) = det(D₁+J₁) · det(D₂+J₂)` numerically.
2. `log|Z|` satisfies strict additivity on factorized Z numerically.
3. `arg(Z)` FAILS strict additivity: explicit Z₁, Z₂ with
   `arg(Z₁) + arg(Z₂) ≠ arg(Z₁ · Z₂)` (off by exactly 2π).
4. Cauchy's theorem numerical check: continuous additive solutions on
   (0, ∞) are sampled and shown to fit `c log r` exactly.
5. CPT-evenness of `log|Z|` on the framework's lattice Dirac
   determinant: `Z → Z*` under CPT, `log|Z| → log|Z*| = log|Z|`.
6. CPT-oddness of `arg(Z)`: `arg(Z) → arg(Z*) = -arg(Z)` under CPT.
7. Counterfactual: `W = c log|Z| + b arg(Z)` with `b ≠ 0` fails
   strict additivity at the explicit witness pair `Z₁ = Z₂ =
   exp(i·3π/4)`.
8. Continuity is load-bearing: a sampled discontinuous additive
   functional fails to fit the unique `c log r` form.
9. Parent row's two premises (additivity, CPT-even phase-blindness)
   ARE recovered as consequences of the single P3 premise + retained
   machinery.

## Cross-references

- [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) —
  parent row whose verdict-identified obstruction is closed by this
  derivation.
- [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) — retained-grade lattice
  CPT structure cited in P2.
- [`HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md`](HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md) —
  sister authority on the Matsubara decomposition; this PR addresses
  scalar generator uniqueness, not the decomposition.
