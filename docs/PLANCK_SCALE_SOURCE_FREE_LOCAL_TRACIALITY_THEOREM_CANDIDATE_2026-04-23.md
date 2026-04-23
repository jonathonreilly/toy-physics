# Planck-Scale Source-Free Local Traciality Theorem Candidate

**Date:** 2026-04-23  
**Status:** science-only new-theory candidate on the last open Planck blocker  
**Audit runner:** `scripts/frontier_planck_source_free_local_traciality_theorem_candidate.py`

## Question

After closing the direct counting law

`c_cell(rho) = Tr(rho P_A)`,

can the remaining Planck blocker be attacked directly by a cleaner new theorem
than the older full-bit-flip witness?

The remaining blocker is:

`rho_cell = I_16 / 16`.

The current accepted stack does not derive that state. The direct question is:

> what is the smallest clean new source-free state law on the primitive
> time-locked `C^16` cell that would close Planck without leaning on the older
> scalar Schur/free-energy route?

## Bottom line

Yes.

The clean new candidate is:

> **Source-Free Local Traciality Theorem.**
> On the exact primitive time-locked cell algebra, the source-free local state
> is the unique normalized state with no preferred primitive projector.

On a finite primitive cell, that theorem is equivalent to the tracial state

`rho_cell = I_16 / 16`.

Then the already-closed counting theorem gives

`c_cell = Tr(rho_cell P_A) = 1/4`,

and the direct Planck route closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

So the branch is now reduced to one very clean new-theory question:

> should source-free local occupancy on the primitive `C^16` cell be tracial?

This is cleaner than the older full-bit-flip witness because it names the real
missing content directly instead of packaging it as a stronger symmetry trick.

## Why this is cleaner than the old flip witness

The old exact sufficient witness was:

`source-free local occupation is invariant under the full local flip group`.

That works, but it is stronger than the real content we need.

The real content is not “bit flips” as such. It is:

- no primitive cell event is preferred in the source-free local state;
- therefore the primitive-cell state is tracial.

The flip witness is just one way to realize that.

So the cleaner new theory is:

- **physical statement:** source-free local occupancy has no preferred primitive
  projector;
- **mathematical consequence:** the state is tracial;
- **Planck consequence:** quarter follows from the counting theorem.

## Setup

Work on the exact time-locked primitive cell

`H_cell = span{|eta> : eta in {0,1}^4}`,

with atomic projectors

`P_eta = |eta><eta|`.

So the primitive event frame has `16` atoms.

The section-canonical one-step worldtube packet is

`P_A = sum_(|eta|=1) P_eta`,

with exactly four atomic events.

The already-closed counting theorem says:

`c_cell(rho) = Tr(rho P_A)`.

So the only missing state content is `rho`.

## Three equivalent formulations of the new candidate

On the finite primitive cell, the following three formulations point to the
same state.

### Form A: no-preferred-projector state

The source-free local state assigns equal weight to every primitive atomic
projector `P_eta`.

Then automatically

`rho_cell = I_16 / 16`.

### Form B: primitive-cell automorphism invariance

The source-free local state is invariant under a transitive automorphism group
of the primitive cell event frame.

Any such transitive invariance forces equal atomic weights, hence again

`rho_cell = I_16 / 16`.

### Form C: maximum source-free local entropy

In the absence of any local source datum or expectation constraint, the
primitive-cell source-free state is the entropy-maximizing state on the full
16-atom frame.

On a finite `16`-state frame, the unique entropy maximizer is the uniform
state, hence

`rho_cell = I_16 / 16`.

These are not yet retained theorems of the current package. But they are clean,
exact new-theory candidates for the last blocker.

## Theorem 1: no-preferred-projector implies traciality

Assume:

1. the source-free local state is diagonal on the primitive projectors
   `P_eta`;
2. every primitive projector carries the same source-free weight.

Then the state is uniquely

`rho_cell = I_16 / 16`.

### Proof

If every atomic projector has equal weight `c`, then normalization gives

`16 c = 1`,

so

`c = 1/16`.

Therefore

`rho_cell = sum_eta (1/16) P_eta = I_16 / 16`.

## Theorem 2: transitive event-frame invariance implies traciality

Assume the source-free local state is invariant under any transitive symmetry
group acting on the `16` primitive projectors.

Then every atomic projector lies in one orbit, so all atomic weights are equal.
By Theorem 1,

`rho_cell = I_16 / 16`.

This makes explicit that the older full-flip witness is not the theorem itself;
it is just one transitive symmetry realization of the deeper traciality claim.

## Theorem 3: source-free max-entropy implies traciality

Among diagonal states on a finite `16`-atom event frame, the unique maximizer
of Shannon/von Neumann entropy is the uniform state.

Therefore the unique source-free maximum-entropy state is

`rho_cell = I_16 / 16`.

This is the information-theoretic form of the same candidate theorem.

## Corollary: direct Planck closure under local traciality

Assume the Source-Free Local Traciality Theorem.

Then

`rho_cell = I_16 / 16`.

The already-closed direct counting law gives

`c_cell = Tr(rho_cell P_A)`.

Because `P_A` has rank `4`,

`c_cell = Tr((I_16 / 16) P_A) = 4 / 16 = 1/4`.

So the elementary boundary cell coefficient is exactly quarter, and the direct
Planck route closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

## Honest status

This is **not** yet a retained theorem.

It is a new science candidate.

The honest claim is:

- the branch has already closed the counting law;
- the branch has already shown current accepted structure does not select the
  source-free state;
- the cleanest remaining new theory is source-free local traciality on the
  primitive cell.

So the lane is now:

- no longer coefficient hunting;
- no longer packet selection;
- no longer counting-law selection;
- exactly one new state theorem candidate.

## Why this may be the right axiom-native move

If Planck is really native, it is more plausible that it should come from a
local source-free state law on the primitive finite cell than from a patched
continuum free-energy scalar.

That is why this candidate is stronger conceptually than the older
"boundary pressure" language:

- it lives directly on the primitive cell;
- it talks directly about source-free local state;
- it closes directly through the already-earned counting theorem.

So even if this candidate is new, it is at least pointed at the right object.

## Safe wording

**Can claim**

- the remaining Planck blocker can be reformulated as a source-free local
  traciality question;
- local traciality is a cleaner new candidate than the older full-flip witness;
- if local traciality holds, Planck closes immediately through the counting
  theorem.

**Cannot claim**

- that local traciality is already retained on the current package surface;
- that Planck is already retained-derived by this note alone.

## Command

```bash
python3 scripts/frontier_planck_source_free_local_traciality_theorem_candidate.py
```
