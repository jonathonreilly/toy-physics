# Planck-Scale Source-Free Local State Law Conditional Audit

**Date:** 2026-04-23  
**Status:** branch-local hostile-review audit for the direct Planck lane  
**Audit runner:** `scripts/frontier_planck_source_free_local_state_law_retained_audit.py`

## Question

After deriving the source-free local state law on the primitive `C^2` factors
and lifting it by exact tensor-product locality, do we now have a retained
axiom-native Planck close?

## Verdict

No.

The previous blocker was:

`rho_cell = I_16 / 16`.

That state law is derived in the branch-local theorem candidate
[PLANCK_SCALE_SOURCE_FREE_LOCAL_STATE_LAW_THEOREM_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_LOCAL_STATE_LAW_THEOREM_2026-04-23.md):

- source-free bare local `C^2` factor
  `-> I_2 / 2`
- exact tensor-product locality
  `-> rho_cell = (I_2/2)^⊗4 = I_16/16`

The direct counting law was already closed in
[PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md):

`c_cell(rho) = Tr(rho P_A)`.

So on the branch-local conditional package,

`c_cell = Tr((I_16/16) P_A) = 1/4`

and the direct Planck chain closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

## Why this is not retained

The old retained-direct no-go note was correct about the previously accepted
stack: without a source-free local state law, the full-cell state was
underdetermined.

The new theorem closes that gap only after adding two fresh branch-local
state-law premises:

1. bare-factor unitary invariance on `C^2`;
2. no cross-factor datum on the exact local tensor product.

Those are clean candidate promotions, but they are not present in the accepted
minimal framework input stack. The single-axiom Hilbert note used for
motivation is explicitly a reduction/support note, not the accepted
load-bearing package boundary.

## Honest status

This is a **branch-local conditional close candidate**.

It is **not** woven through `main`, **not** reviewer-ratified, and **not** yet
an axiom-native retained close. What is closed is narrower:

- the counting side is closed;
- the branch now has a clean conditional state-law theorem;
- the exact remaining burden is to derive or justify those two state-law
  premises from the accepted `Cl(3)`/`Z^3` package itself.

Until then, the right label is:

- **conditional close candidate**
- not **retained native derivation**

## What would count as a retained close

Any one of the following would be enough:

1. derive bare-factor unitary no-datum invariance from accepted package
   structure;
2. derive no-cross-factor-datum tensor composition from accepted package
   structure;
3. derive an equivalent source-free primitive-cell traciality theorem directly
   from the accepted stack without introducing either premise as a fresh law.

Without one of those, hostile review should reject any claim that Planck is
already fully derived from native accepted axioms.
