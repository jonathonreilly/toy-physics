# Generation Axiom Boundary Note

**Date:** 2026-04-16 (narrowed 2026-05-02)
**Status:** narrowed bounded theorem on the retained `hw=1` operator-algebra
surface plus reduced-stack witness; audit pending under the narrowed scope.
**Script:** `scripts/frontier_generation_axiom_boundary.py`
**Authority role:** local-construction support note for the
retained-generation operator algebra; species/substrate semantics live in
sibling notes and are not load-bearing here.

## Narrowed Claim Scope (2026-05-02)

The load-bearing claim of this note is **only** the local operator-algebra
construction on `H_hw=1` plus the reduced-stack witness that the older
five-item memo had listed substrate physicality as an explicit input.

In particular, this note does **not** load-bearingly claim:

- physical-species semantics for the retained `hw=1` triplet on the accepted
  Hilbert surface (delegated to `PHYSICAL_LATTICE_NECESSITY_NOTE.md` Part 7);
- one-axiom substrate-level physical-lattice necessity (delegated to
  `PHYSICAL_LATTICE_NECESSITY_NOTE.md` Part 9);
- no-proper-quotient as a global theorem on the full taste space (delegated
  to `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` and the rooting-undefined
  runner).

Those three semantic upgrades were previously folded into the boundary
statement here; the 2026-05-02 narrowing scopes them out so the
load-bearing surface of this note depends only on retained-grade inputs
(translations on `Z^3`, the induced `C3[111]` map on `H_hw=1`, and finite
linear algebra over `C^3`).

## Safe statement (narrowed)

On the retained `hw=1` triplet `H_hw=1 = span{X1, X2, X3}` carried by the
exact `Z^3` translation characters:

1. The three lattice translations `Tx, Ty, Tz` act as
   `diag(-1,+1,+1), diag(+1,-1,+1), diag(+1,+1,-1)` and pairwise distinguish
   the three sectors.
2. The induced `C3[111]` map (obtained by restricting the exact full
   taste-space `C3[111]` to the three retained `hw=1` eigenspaces) cycles
   `X1 -> X2 -> X3 -> X1`.
3. The set `{Tx, Ty, Tz, C3[111]}` generates the full matrix algebra
   `M_3(C)` on `H_hw=1`, with commutant of dimension 1.

This is an exact local construction at the level of `3 x 3` complex
matrices. It is reusable as a building block by sibling notes that wish to
upgrade it to species or substrate semantics, but it does not itself perform
that upgrade.

## What the runner verifies

`scripts/frontier_generation_axiom_boundary.py` (`PASS=35`, `FAIL=0`)
performs the following retained-grade computational checks:

- Clifford `Cl(3)` algebra, 8-state taste basis, KS gamma matrices
  (numerical, A1 only).
- Eight Brillouin-zone corners; Wilson-mass equivalence at all corners
  (numerical).
- Three `hw=1` Fermi points each give `|E_min| = 1` (numerical).
- Commutant of `Cl(3)` on `C^8` is 8-dimensional (numerical).
- Projected commutant at each `hw=1` corner is `M(2,C)` with identical
  Casimir (numerical).
- `C3[111]` on `C^8` is unitary, order 3, and maps the three retained
  eigenspaces cyclically (numerical).
- The retained operator algebra `<Tx, Ty, Tz, C3[111]>` on `H_hw=1` has
  dimension 9, and its commutant has dimension 1 (numerical).

These are all retained-grade computational checks that depend only on
finite numpy linear algebra applied to the retained-grade `Cl(3)/Z^3` input
surface.

The remaining checks in the runner that talk about "Hilbert surface
semantics", "regulator escape route", "ontological commitment", or
"physical-species semantics" are **labelled `[LOGICAL]`** in the runner
output. These are commentary on the package architecture, not load-bearing
operator-algebra claims, and are explicitly **not part of this note's
narrowed bounded theorem**. They are retained in the runner only as the
reduced-stack witness for the older five-item memo.

## Why the narrowing is honest

The previous statement of this note conflated two things:

- **A retained-grade local construction.** That `Tx, Ty, Tz, C3[111]`
  generate `M_3(C)` on `H_hw=1` is a finite-dimensional matrix-algebra
  fact, fully verified by the runner.
- **A semantic upgrade to physical-species / substrate ontology.** That
  upgrade requires accepted Hilbert semantics, the no-proper-quotient
  closure, and the substrate-level physical-lattice reading. Those are
  load-bearing imports from sibling notes whose audit grade is not under
  this note's control.

The audit verdict (2026-04) flagged the second item as a load-bearing
import that this note's runner does not derive internally. The narrowing
removes that import from this note's load-bearing surface; the upgrade
still happens, but it is now explicitly delegated to
`PHYSICAL_LATTICE_NECESSITY_NOTE.md` and
`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`, which carry that load.

## Why this still matters

A retained-grade local construction note is a useful building block:

- It exhibits the explicit `3 x 3` matrix-algebra structure used by every
  sibling note that wants to talk about the retained generation surface.
- It packages the witness that the older five-item memo had listed
  substrate physicality as an explicit input — useful for diff-tracking
  the historical reduction in framework axioms.
- It provides a single citation point for "the retained operator algebra
  on the three `hw=1` sectors is exactly `M_3(C)`."

It is no longer a load-bearing input for any `physical species` or
`substrate physicality` claim downstream; downstream notes that need those
upgrades cite the sibling notes directly.

## Relation to the retained matter stack

This note (after narrowing) supports but does not replace:

- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` (no-proper-quotient on the
  retained surface);
- `PHYSICAL_LATTICE_NECESSITY_NOTE.md` (no-same-stack regulator
  reinterpretation; species semantics; substrate necessity);
- the various rooting-undefined / mass-matrix support notes.

The clean current division of labor is:

- **this note** (narrowed):
  exact local `M_3(C)` construction on `H_hw=1` plus reduced-stack witness
  for the older substrate premise;
- **`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`**:
  irreducibility / no-proper-quotient consequence on `H_hw=1`;
- **`PHYSICAL_LATTICE_NECESSITY_NOTE.md`**:
  no-same-stack regulator nonequivalence + species semantics + substrate
  necessity on the accepted one-axiom surface.

## Validation

- primary runner:
  [frontier_generation_axiom_boundary.py](./../scripts/frontier_generation_axiom_boundary.py)

Current branch runner state:

- `frontier_generation_axiom_boundary.py`: `PASS=35`, `FAIL=0`;
  retained-grade computational checks plus reduced-stack `[LOGICAL]`
  witness commentary (not load-bearing under the narrowed scope).

## Honest open items

Under the narrowed scope, no open items remain inside this note. Items
that **were** open under the previous wider scope have been redirected:

- "physical-species semantics on the accepted Hilbert surface" — open in
  `PHYSICAL_LATTICE_NECESSITY_NOTE.md` Part 7; not load-bearing here.
- "substrate-level physical-lattice necessity" — open in
  `PHYSICAL_LATTICE_NECESSITY_NOTE.md` Part 9; not load-bearing here.
- "no-proper-quotient on the retained surface" — open in
  `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`; not load-bearing here.

This narrowing trades global force for retained-grade chain closure on the
local fragment.
