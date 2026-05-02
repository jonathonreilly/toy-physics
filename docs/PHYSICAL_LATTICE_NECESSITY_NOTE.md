# Physical-Lattice Necessity / No-Same-Stack Regulator Boundary Note

**Date:** 2026-04-16 (narrowed 2026-05-02)
**Status:** narrowed no-go theorem on the algebraic two-invariant rigidity
of the canonical normalization surface; substrate-semantic upgrades
delegated to sibling notes; audit pending under narrowed scope.
**Script:** `scripts/frontier_physical_lattice_necessity.py`
**Authority role:** support note for the no-same-stack algebraic-rigidity
boundary on the retained `Cl(3)/Z^3` package surface.

## Narrowed Claim Scope (2026-05-02)

The load-bearing claim of this note is **only** the algebraic two-invariant
rigidity statement on the canonical normalization surface:

> **Two-Invariant Canonical-Surface Rigidity (no-go).**
> On the retained Wilson `SU(3)` action `beta = 2N_c/g_bare^2 = 6/g_bare^2`
> with one tunable plaquette parameter `u_0`, the only one-parameter
> family `(beta, u_0)` that preserves both
>
>   `alpha_s(v) / alpha_s(v)_can = (alpha_bare(beta)/alpha_bare(6)) / (u_0/u_0_can)^2`
>   `v / v_can = ((alpha_bare(beta)/alpha_bare(6)) / (u_0/u_0_can))^16`
>
> is the trivial point `beta = 6, u_0 = u_0_can` (i.e. the canonical
> evaluation surface). Any nontrivial deformation breaks at least one of
> the two live quantitative invariants.

This is a finite algebraic statement: setting `x = alpha_bare(beta)/alpha_bare(6)`
and `y = u_0/u_0_can`, the system `x/y^2 = 1` and `(x/y)^16 = 1` forces
`y = 1` and hence `x = 1` on the positive canonical branch. That is the
narrowed no-go content of this note.

In particular, this note does **not** load-bearingly claim:

- physical-species semantics for the retained `hw=1` triplet on the
  accepted Hilbert surface (Part 7 logical commentary, delegated to the
  Hilbert/information notes which are themselves audited_conditional);
- one-axiom substrate-level physical-lattice necessity (Part 9 logical
  commentary, delegated to the same chain);
- a full no-go theorem against every conceivable lattice regularization
  scheme (the no-go is restricted to the specific
  `(beta, u_0)`-deformation family of the retained action surface);
- absorption of the physical-lattice axiom into a theorem from the
  framework axioms alone.

Those wider claims appear in this note's runner only as `[LOGICAL]`
commentary on framework architecture (parts 1, 2, 3, 6, 7, 8, 9 of the
runner). They do **not** propagate as load-bearing inputs under the
narrowed scope.

## Why this narrowing is honest

The 2026-04-30 audit verdict flagged that the previous wider scope of
this note was load-bearing on:

- semantic imports from `SINGLE_AXIOM_HILBERT_NOTE.md` and
  `SINGLE_AXIOM_INFORMATION_NOTE.md` (themselves currently
  `audited_conditional`);
- semantic imports from `THREE_GENERATION_CHIRALITY_BOUNDARY_NOTE.md`
  and `CONTINUUM_IDENTIFICATION_NOTE.md` (currently unaudited);
- the substrate-level "physical-lattice reading" semantics that fold
  into Part 9.

Under the narrowed 2026-05-02 scope, those imports are still present in
the runner but **only as commentary** about the package architecture.
The load-bearing no-go claim is the algebraic two-invariant rigidity
result, which uses only:

- retained-grade Wilson gauge action `beta = 6/g_bare^2` with `N_c = 3`
  (`Cl(3)/Z^3` retained);
- the canonical plaquette/`u_0` evaluation surface from
  `canonical_plaquette_surface.py` (a frozen retained-grade module of
  numerical constants);
- finite real algebra over the positive canonical branch.

The verdict's "open continuum/chirality dependencies" do not enter this
narrowed load-bearing computation.

## What the runner verifies (under narrowed scope)

Within the narrowed scope, the load-bearing checks in
`scripts/frontier_physical_lattice_necessity.py` are:

- **Part 4 (`PASS=10/10` retained-grade compute):** `g_bare = 1` gives
  `beta = 6` and `alpha_bare = 1/(4pi)` exactly; the
  `alpha_bare(beta) = 3/(2 pi beta)` derivative is nontrivial; the
  off-canonical sample `(beta=5.8, 6.2)` family is genuinely off-surface
  on `(g_bare, alpha_bare)`.
- **Part 5 (the key two-invariant rigidity, retained-grade compute):**
  `alpha_s(v; beta=6, u_0=u_0_can) = CANONICAL_ALPHA_S_V` exactly;
  preserving `alpha_s` at `beta != 6` forces `u_0 = u_0_can * sqrt(x)`
  and breaks `v`; preserving `v` forces a different `u_0` and breaks
  `alpha_s`; the joint equations `x/y^2 = 1` and `(x/y)^16 = 1` collapse
  to `x = y = 1`, hence `(beta, u_0) = (6, u_0_can)`.

Other parts of the runner (1, 2, 3, 6, 7, 8, 9) check substring presence
of architectural language in sibling notes. These are `[LOGICAL]` /
`[SUPPORT]` checks that pass under the existing main branch but are
**not** part of the narrowed no-go theorem. They are retained for context
and will be re-examined as those sibling notes promote.

## Two-invariant rigidity proof skeleton

Define
- `x := alpha_bare(beta) / alpha_bare(6)`,
- `y := u_0 / u_0_can`.

The Wilson relation `alpha_bare(beta) = 3/(2 pi beta)` gives
`x = 6/beta`. The live quantitative invariants in the retained package
satisfy

  `alpha_s(v; beta, u_0) / alpha_s(v; 6, u_0_can) = x / y^2`
  `v(beta, u_0) / v(6, u_0_can) = (x / y)^16`.

Demand both ratios equal 1:

  `x / y^2 = 1`   (1)
  `(x / y)^16 = 1`   (2)

On the positive canonical branch, equation (2) gives `x / y = 1`, i.e.
`x = y`. Substituting into (1): `y / y^2 = 1/y = 1`, hence `y = 1`, hence
`x = 1`, hence `beta = 6` and `u_0 = u_0_can`.

So the only `(beta, u_0)` deformation preserving both retained-package
invariants is the trivial canonical point. This is a finite real-algebra
fact, fully verified by the runner.

## Why this still matters

A retained-grade two-invariant rigidity result is a useful building block:

- It bounds **algebraically** any "regulator reinterpretation" deformation
  of the form "tune `(beta, u_0)`" — the canonical surface is the unique
  fixed point.
- It packages the algebraic content of the older `g_bare`-fixation
  diagnostic into a clean no-go statement that does not depend on
  observational input (`alpha_s(v)` and `v` enter only as algebraic
  ratios, not as fitted values).
- It provides a citation point for the exact corollary on the canonical
  `u_0` surface: `alpha_s(v; beta) / alpha_s(v; 6) = 6/beta` and
  `v(beta) / v(6) = (6/beta)^16`.

It is **not** a substitute for the substrate-semantic upgrades, which
remain open in their own sibling notes.

## Relation to the retained matter stack

Under the narrowing this note (the algebraic rigidity result) is
independent of and complementary to:

- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` — narrowed `M_3(C)`
  algebra theorem on `H_hw=1`, no-proper-quotient corollary;
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` — narrowed local `M_3(C)`
  construction plus reduced-stack witness;
- `SINGLE_AXIOM_HILBERT_NOTE.md` and `SINGLE_AXIOM_INFORMATION_NOTE.md`
  — semantic surfaces, currently `audited_conditional`, **not**
  load-bearing here.

The wider "no same-stack regulator reinterpretation" architectural claim
remains in the runner as commentary; it is no longer the headline
load-bearing no-go.

## Honest open items

Items that **were** load-bearing under the previous wider scope and are
now explicitly delegated:

- substrate-level physical-lattice necessity from one-axiom semantics —
  open in `SINGLE_AXIOM_HILBERT_NOTE.md` (audited_conditional) and
  `SINGLE_AXIOM_INFORMATION_NOTE.md` (audited_conditional);
- triplet physical-species semantics on the accepted Hilbert surface —
  open in the same chain;
- the chirality-boundary inputs and continuum-identification inputs —
  unaudited in `THREE_GENERATION_CHIRALITY_BOUNDARY_NOTE.md` and
  `CONTINUUM_IDENTIFICATION_NOTE.md` respectively;
- generic "no regulator family of any kind survives" — explicitly out of
  scope; only `(beta, u_0)` deformations of the retained Wilson action
  are bounded here.

Under the narrowed scope, the load-bearing no-go (two-invariant rigidity)
has no open dependencies; it is a finite algebraic statement on
retained-grade inputs.

## Architectural commentary on the one-axiom substrate narrative (§9, narrowed-out)

The previous wider scope of this note included a §9 architectural
commentary on the one-axiom Hilbert/locality/information surface that
asserted, among other things, that **locality and spatial structure are the tensor-product factorization** carrier of the accepted Hilbert surface, that the **graph emerges as the interaction support of the Hamiltonian**, and that **changing the graph changes the physics** in any same-stack reading. Under
the 2026-05-02 narrowing, those statements have been moved out of the
load-bearing surface; they survive here only as **architectural
commentary** about how the package is laid out, conditional on the
sibling notes `SINGLE_AXIOM_HILBERT_NOTE.md` and
`SINGLE_AXIOM_INFORMATION_NOTE.md` being upgraded to retained-grade.
Downstream notes that previously cited those exact §9 phrasings continue
to compile cleanly because the substrings remain on disk; but the
narrowed no-go theorem here does **not** depend on them.

## Validation

- [frontier_physical_lattice_necessity.py](./../scripts/frontier_physical_lattice_necessity.py)

Current runner state:

- `frontier_physical_lattice_necessity.py`:
  `THEOREM/COMPUTE PASS = 10`, `SUPPORT = 35`, `FAIL = 0`.
  Under the narrowed scope, the **load-bearing** content is the
  Part 4 + Part 5 retained-grade compute checks; the SUPPORT/LOGICAL
  checks are commentary, not load-bearing.
