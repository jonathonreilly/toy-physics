# Planck-Scale Source-Free Default-Datum Theorem Candidate

**Date:** 2026-04-23  
**Status:** branch-local theorem candidate for the last semantic move  
**Audit runner:** `scripts/frontier_planck_source_free_default_datum_theorem_candidate.py`

## Question

Can the remaining semantic step be stated more natively than either

- "same-object semantics extends to source-free local states", or
- "source-free local state has zero local information defect"?

## Bottom line

Yes.

The cleanest native statement is:

> a **source-free** local state is the **default state datum of the primitive
> cell object when no extra preparation/source datum is supplied**.

That is different from an arbitrary prepared state.

On the accepted one-axiom semantics surface, the physical object is the
graph/locality/unitary structure; additional preparations are additional data
on top of that object. So when no additional local datum is given, the local
state must be determined by the primitive cell object alone.

For the exact primitive cell

`H_cell = C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z ~= C^16`,

the unique normalized default datum determined by the bare cell object alone is

`rho_cell = I_16 / 16`.

Then the already-closed counting theorem gives

`c_cell = Tr((I_16/16) P_A) = 1/4`,

so the direct Planck route closes.

## Why this is cleaner

This formulation says exactly what is being claimed and what is not.

It does **not** say:

- every physical state must be tracial;
- prepared states are forbidden;
- entropy language is fundamental;
- basis language is fundamental.

It says only:

- the package has physical objects;
- prepared states are extra data on top of those objects;
- source-free means no such extra local datum is present;
- therefore the source-free state must be the canonical state attached to the
  bare primitive cell object itself.

That is the sharpest native reading of the lane so far.

## Inputs

- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)
- [SINGLE_AXIOM_HILBERT_NOTE.md](./SINGLE_AXIOM_HILBERT_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- [PLANCK_SCALE_TIMELOCKED_FACTOR_CELL_OBJECT_DERIVATION_2026-04-23.md](./PLANCK_SCALE_TIMELOCKED_FACTOR_CELL_OBJECT_DERIVATION_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_STATE_SAME_OBJECT_DEFENSIBILITY_AUDIT_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_STATE_SAME_OBJECT_DEFENSIBILITY_AUDIT_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_NO_LOCAL_INFORMATION_THEOREM_CANDIDATE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_NO_LOCAL_INFORMATION_THEOREM_CANDIDATE_2026-04-23.md)
- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)

## Theorem 1: source-free state is default local datum, not hidden preparation

Assume:

1. the accepted one-axiom semantics treats the physical substrate/object as
   primary;
2. prepared states are extra physical data supplied on top of that object;
3. "source-free local state" means the state attached to the primitive cell
   when no extra local preparation/source datum is supplied.

Then a source-free local state cannot carry hidden preparation information.
So it must be determined by the primitive cell object alone.

### Reason

If a source-free local state contained extra one-cell weighting or projector
data not fixed by the primitive cell object itself, then that data would be
precisely an unacknowledged local preparation datum.

That contradicts Item 3.

So a source-free local state is the default state datum of the bare cell
object, not an unknown prepared state.

## Corollary 1: default datum on the primitive cell is tracial

On the direct Planck route, the primitive cell object is

`H_cell = C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z ~= C^16`.

The default datum of that bare cell cannot depend on factor-frame presentation
and cannot contain extra local information not supplied by a source.

So by the same-object and no-local-information routes already established on
this branch, the unique normalized default state datum is

`rho_cell = I_16 / 16`.

## Corollary 2: quarter and Planck

Using the already-closed counting theorem

`c_cell(rho) = Tr(rho P_A)`,

one gets

`c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4`.

Therefore the direct route gives

`a^2 = l_P^2`,

hence

`a = l_P`.

## Honest status

This is the strongest native formulation on the branch so far.

But hostile review can still refuse it if they reject the sentence:

> source-free local state = default bare-cell datum when no extra local
> preparation/source is given.

So this note is best read as:

- stronger than the old ad hoc state-selection readings;
- probably the cleanest native candidate;
- still a **candidate** until that last semantic identification is explicitly
  accepted.
