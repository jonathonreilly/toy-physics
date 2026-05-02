# Observable Principle From Axiom Note

**Date:** 2026-04-13 (narrowed 2026-05-02)
**Status:** narrowed bounded theorem on the finite-block scalar
observable generator; hierarchy/`v` consequence boxed as a corollary
that depends on the (unaudited) canonical plaquette surface.
**Script:** `scripts/frontier_hierarchy_observable_principle_from_axiom.py`

## Narrowed Claim Scope (2026-05-02)

The load-bearing claim of this note is:

> **Finite-Block Scalar Generator Theorem (bounded under explicit
> selection premises).**
> Fix a finite Grassmann block with lattice Dirac operator `D` and a
> source-deformed operator `D[J] = D + J`. Assume that the physical
> scalar-observable generator `W[J]` satisfies the two **explicit
> selection premises**:
>
>   (P1) **Additivity on independent subsystems:** for `D = D_1 ⊕ D_2`
>        and `J = J_1 ⊕ J_2`, `W[J_1 ⊕ J_2] = W[J_1] + W[J_2]`;
>   (P2) **CPT-even phase blindness:** `W` depends only on `|Z[J]|` and
>        not on the fermionic phase of `Z[J]`.
>
> Then the unique continuous solution is
>
>   `W[J] = c log|det(D + J)| - c log|det D|`
>
> for some real constant `c`. Fixing `c = 1` and subtracting the
> zero-source baseline gives
>
>   `W[J] = log |det(D+J)| - log |det D|`.
>
> Local scalar observables are then exactly the source derivatives of
> `W`:
>
>   `∂W/∂j_x = Re Tr[(D+J)^(-1) P_x]`,
>   `∂^2 W / ∂j_x ∂j_y = - Re Tr[(D+J)^(-1) P_x (D+J)^(-1) P_y]`.

This is an algebraic / functional-equation theorem **bounded under the
two explicit selection premises (P1) and (P2)**. The premises themselves
are stated as axioms of the scalar-observable principle, not derived
from the lattice axiom alone.

Claim type: **`bounded_theorem`** (was previously `positive_theorem`).
The theorem closes cleanly conditional on (P1) + (P2); the premises are
explicit selection assumptions about what counts as a physical scalar
generator.

In particular, this note does **not** load-bearingly claim:

- a derivation of (P1) and (P2) from the lattice axiom alone (they are
  imported here as explicit physical-observable selection premises);
- the canonical hierarchy chain (depends on the unaudited
  `PLAQUETTE_SELF_CONSISTENCY_NOTE.md` and the
  `canonical_plaquette_surface.py` constants);
- the `v` prediction at `0.025513%` of measurement (corollary of the
  above; bounded by the plaquette chain's audit grade).

## Why the narrowing is honest

The previous wider scope of the original note had two issues:

1. The hierarchy/`v` prediction imports canonical constants from
   `PLAQUETTE_SELF_CONSISTENCY_NOTE.md`, which is currently unaudited.
2. The "scalar additivity / CPT-even phase blindness" premises are
   themselves selection assumptions, not deductions from the lattice
   axiom.

The 2026-05-02 narrowing addresses both:

1. The hierarchy/`v` prediction is moved out of the load-bearing
   theorem and explicitly boxed as a corollary that depends on the
   plaquette chain. The corollary is still computed by the runner
   (Part 5), but it is no longer the main claim.
2. The two selection premises (P1, P2) are stated **explicitly** as
   axioms of the scalar-observable principle. The note no longer
   claims that the lattice axiom alone forces them; it claims the
   weaker, honest statement that **given (P1) + (P2)**, the unique
   continuous additive CPT-even scalar generator is the log-abs-det.

## What the runner verifies (narrowed)

`scripts/frontier_hierarchy_observable_principle_from_axiom.py`
(`PASS=13`, `FAIL=0`).

Under the narrowed scope, the **load-bearing** retained-grade
computational checks are:

- **Part 1 (additivity on independent subsystems):** `|Z|` is exactly
  multiplicative on `D_1 ⊕ D_2`, hence `log|Z|` is exactly additive;
  raw `|Z|` is not. (Premise P1 is then non-vacuous: the log-abs-det
  is the additive functional, while the bare amplitude is not.)
- **Part 2 (block locality of source response):** mixed local-source curvature vanishes across independent blocks (i.e. mixed derivatives vanish on independent blocks, the connectedness/extensivity hallmark); first-block local curvature is inherited exactly by the block-diagonal full system.
- **Part 3 (uniform-source generator matches Matsubara formula):**
  `log|det(D + jI)| - log|det D|` matches the exact Matsubara
  closed-form `4 sum_omega log(1 + j^2 / [u_0^2 (3 + sin^2 omega)])`;
  the small-`j` quadratic coefficient matches the analytic
  `A(L_t) = (1/(2 L_t u_0^2)) sum_omega 1/(3 + sin^2 omega)`.
- **Part 4 (selector kernel is sign/conjugation closed):** the
  curvature kernel depends only on `sin^2 omega`; `L_t = 4` is the
  unique minimal resolved Klein-four orbit.

The **bounded corollary** in Part 5 (hierarchy `v = 246.282...` GeV
within `0.026%` of measurement) uses canonical constants from
`canonical_plaquette_surface.py` and is presented here as an example
of how the narrowed theorem connects to the live quantitative chain
**conditional on the plaquette note's audit grade**. It is not the
load-bearing content of this note.

## Selection premises stated as axioms

Under the narrowed scope, the two selection premises are listed as
explicit axioms of the scalar-observable principle:

- **(P1) Scalar additivity on independent subsystems.** For independent
  finite Grassmann subsystems `D_1, D_2`, the physical scalar generator
  satisfies `W[J_1 ⊕ J_2] = W[J_1] + W[J_2]`. This is the standard
  scalar-extensivity requirement for thermodynamic-style observables;
  it is not derived here from the lattice axiom but stated as an
  axiom of what we call a *physical scalar generator*.
- **(P2) CPT-even phase blindness.** The physical scalar generator
  depends only on `|Z[J]| = |det(D + J)|`, not on the fermionic phase
  of `Z[J]`. This is the standard scalar-bosonic-observable
  requirement; it is not derived here but stated as an axiom of what
  we call a *physical scalar generator*.

These two premises are then sufficient: by the multiplicative-to-additive functional equation `W(r_1 r_2) = W(r_1) + W(r_2)` for `r_i > 0` and the standard continuous-solution theorem, `W = c log|Z| + const`. Normalization fixes `c = 1` and the baseline subtraction; the result is the log-abs-det generator (the unique additive CPT-even scalar generator).

Once the scalar generator is fixed, local scalar observables are source derivatives of `W` (this is the original Theorem 2 statement, preserved here under the narrowed scope as a corollary): for the local source-projector basis `J = sum_x j_x P_x`, the first-order derivative is `∂W/∂j_x = Re Tr[(D+J)^(-1) P_x]`.

## What this still buys (under narrowed scope)

- A clean **finite-block uniqueness** result: under (P1) + (P2), the
  log-abs-det generator is **the** physical scalar generator on
  finite Grassmann blocks (no free functional choices remain).
- A clean **block-locality** result: source derivatives of the
  log-abs-det generator are connected, bilinear, and local in the
  source projectors `P_x`.
- A **Matsubara closed form** for the uniform-source generator on the
  exact `L_s = 2` APBC block.
- A **bounded hierarchy corollary** (Part 5) for the `v` prediction
  conditional on the canonical plaquette chain.

## What this does not buy (under narrowed scope)

- Derivation of (P1) + (P2) from the lattice axiom alone. Those remain
  explicit selection axioms.
- A retained-grade hierarchy `v` derivation. The Part 5 corollary
  inherits the audit grade of the plaquette chain.

## Honest open items

- **(P1) + (P2) as theorems from the lattice axiom alone.** Currently
  stated as explicit selection premises. A future strengthening could
  derive them from a structural property of finite Grassmann
  partition functions plus a scalar-observable selection theorem.
- **`PLAQUETTE_SELF_CONSISTENCY_NOTE.md` audit grade.** The hierarchy
  corollary inherits this grade; promoting that note to retained-grade
  would promote the corollary too.
- **`canonical_plaquette_surface.py` constants.** Currently a frozen
  module; if the plaquette note is re-derived, those constants flow
  through.

Under the narrowed scope, the **load-bearing** content (the finite-block
log-abs-det uniqueness theorem under explicit (P1) + (P2)) has no open
dependencies; it is a finite linear-algebra + functional-equation
statement.

## Relation to the retained matter stack

The narrowed theorem provides a clean retained-grade building block:

- For any future hierarchy / Higgs lane that wants to use the
  log-abs-det as the physical scalar generator on finite blocks, this
  note supplies the under-(P1)+(P2) uniqueness and the explicit
  source-response algebra.
- The hierarchy/`v` corollary (Part 5) is shipped as a bounded
  consequence rather than an independent theorem, with its audit grade
  explicitly tied to the plaquette chain.
