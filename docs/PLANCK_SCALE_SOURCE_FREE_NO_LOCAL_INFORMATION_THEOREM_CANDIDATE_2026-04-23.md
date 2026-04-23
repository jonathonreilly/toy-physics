# Planck-Scale Source-Free No-Local-Information Theorem Candidate

**Date:** 2026-04-23  
**Status:** branch-local theorem candidate / defensibility support note  
**Audit runner:** `scripts/frontier_planck_source_free_no_local_information_theorem_candidate.py`

## Question

Can the source-free primitive-cell state be forced more natively from the
framework's **conserved information** reading, rather than only from
presentation/basis arguments?

## Bottom line

This gives a second clean route to the same endpoint.

If the primitive one-cell state is genuinely **source-free**, then it may not
carry any extra local information beyond the cell object itself.

On a finite `16`-state cell, the unique normalized state with **zero local
information defect** relative to the full cell is the tracial state

`rho_cell = I_16 / 16`.

So if the one-axiom information-flow reading is taken seriously at the local
state level, source-free local traciality follows.

## Why this is different

The same-object semantics bridge says:

> source-free state cannot depend on how the same primitive object is
> presented.

This note says something slightly different:

> source-free state cannot carry extra local information that was never
> supplied by a source/preparation datum.

That argument is closer to the one-axiom information note:

- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)

and it avoids relying entirely on basis-language intuition.

## Inputs

- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)
- [SINGLE_AXIOM_HILBERT_NOTE.md](./SINGLE_AXIOM_HILBERT_NOTE.md)
- [PLANCK_SCALE_TIMELOCKED_FACTOR_CELL_OBJECT_DERIVATION_2026-04-23.md](./PLANCK_SCALE_TIMELOCKED_FACTOR_CELL_OBJECT_DERIVATION_2026-04-23.md)
- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)

## Definition: local information defect

On the primitive cell `H_cell ~= C^16`, define the local information defect of
a normalized state `rho` by

`I_loc(rho) = log 16 - S(rho)`,

where

`S(rho) = -Tr(rho log rho)`

is the von Neumann entropy.

This quantity is:

- nonnegative;
- zero exactly for the tracial state `I_16/16`;
- basis-independent.

So `I_loc(rho)` measures how much extra local information / negentropy is
stored in the cell beyond the fully undifferentiated source-free baseline.

## Candidate principle: source-free means no extra local information

Interpret source-free local state assignment as:

> no additional local preparation datum has been supplied to the primitive
> cell.

On the one-axiom information-flow reading, information is not created from
nothing. Therefore a source-free primitive cell should not carry positive local
information defect on its own:

`I_loc(rho_sf) = 0`.

This is the finite-cell information-theoretic form of "no extra local datum."

## Theorem 1: zero local information defect forces traciality

If `rho` is a normalized state on `C^16` with

`I_loc(rho) = 0`,

then

`rho = I_16 / 16`.

### Proof

By definition,

`I_loc(rho) = log 16 - S(rho)`.

So `I_loc(rho) = 0` iff `S(rho) = log 16`.

The unique entropy maximizer on a finite `d`-dimensional Hilbert space is the
tracial state `I_d/d`. Therefore on `d = 16`,

`rho = I_16 / 16`.

## Corollary 1: quarter and Planck

Using the already-closed counting law

`c_cell(rho) = Tr(rho P_A)`,

one gets

`c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4`.

So the direct Planck route closes:

`a^2 = l_P^2`,

hence

`a = l_P`.

## Strength and weakness

### Strength

This route is basis-independent and uses a quantity with direct information
meaning:

`I_loc(rho)`.

So it avoids the weaker-looking rhetorical form
"don't choose a preferred basis."

### Weakness

The real promoted content is now:

> source-free local state has zero local information defect.

That is cleaner than raw max-entropy language, but hostile review can still ask
whether the one-axiom information note already compels that step on the
primitive cell, or whether this is still a promoted local-state theorem.

So this note is best read as a **second independent support route**, not yet as
automatic retained closure.

## Honest status

This theorem candidate does not by itself upgrade the branch to a front-door
retained native Planck close.

What it does do is materially strengthen the last step:

- the source-free tracial state is now supported both by
  same-object semantics
  and by
  no-created-local-information semantics;
- both routes land on the same state
  `I_16/16`;
- the remaining objection is now narrower:

  > does the accepted one-axiom "information is conserved" reading really force
  > zero local information defect on a source-free primitive cell?

That is a cleaner objection than the older complaint that the lane was just
guessing a uniform state.
