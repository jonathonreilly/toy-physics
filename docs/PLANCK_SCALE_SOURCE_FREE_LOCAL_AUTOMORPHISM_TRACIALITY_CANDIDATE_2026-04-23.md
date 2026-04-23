# Planck-Scale Source-Free Local Automorphism Traciality Candidate

**Date:** 2026-04-23  
**Status:** science-only direct theorem candidate for the last Planck blocker  
**Audit runner:** `scripts/frontier_planck_source_free_local_automorphism_traciality_candidate.py`

## Question

Now that the direct cell-counting bridge is closed,

`c_cell(rho) = Tr(rho P_A)`,

can the last remaining blocker

`rho_cell = I_16 / 16`

be attacked more directly than the older bit-flip or boundary-pressure
packaging?

## Bottom line

Yes.

The cleanest direct target is no longer a worldtube-specific combinatorics
statement. It is a **primitive-cell state theorem**:

> **Source-Free Local Automorphism Traciality Theorem (candidate).**
> On the primitive one-cell algebra `A_cell = M_16(C)`, the source-free local
> state is invariant under exact no-datum relabelings of primitive one-cell
> events. Therefore the unique normalized source-free state is the tracial
> state
>
> `rho_cell = I_16 / 16`.

This is the right direct attack because:

1. the worldtube-to-boundary cell-counting law is already closed;
2. the old retained-direct underdetermination theorem shows the remaining
   freedom is entirely a local state-selection problem on the primitive cell;
3. invariance of a state under exact primitive-cell automorphisms is the
   cleanest "no preferred primitive projector" formulation of source-free local
   data;
4. on a full matrix algebra that invariance forces the normalized trace
   immediately.

So the remaining Planck route is best read as:

`primitive source-free traciality`  
`-> rho_cell = I_16 / 16`  
`-> c_cell = Tr(rho_cell P_A) = 1/4`  
`-> a^2 = l_P^2`  
`-> a = l_P`.

## What this improves

The older sufficient witness was:

`source-free local occupancy is invariant under the full bit-flip group G_4`.

That is mathematically fine, but it is stronger than the real missing content
and it hides the general point.

The actual missing theorem is not "there is one more special symmetry on the
worldtube packet." It is:

> source-free local data on the primitive finite cell carry no preferred
> primitive projector.

That is more naturally stated at the level of the full primitive cell algebra
than at the level of the already-derived packet `P_A`.

## Inputs

This note uses only current branch-local exact surfaces:

- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md](./PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md)
- [SINGLE_AXIOM_HILBERT_NOTE.md](./SINGLE_AXIOM_HILBERT_NOTE.md)
- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)

What those already fix:

1. the primitive local carrier is a finite 16-state one-cell Hilbert carrier;
2. the direct Planck route is already reduced to a local state-selection
   problem;
3. the counting law itself is already closed:
   `c_cell(rho) = Tr(rho P_A)`;
4. the remaining live issue is exactly source-free local traciality / no
   preferred primitive projector on the full cell.

## Setup

Work on the primitive one-cell basis

`eta in {0,1}^4`,

with rank-1 projectors

`P_eta = |eta><eta|`.

Let the full primitive cell algebra be

`A_cell = M_16(C)`.

Call a local state `rho` **source-free / no-datum** if:

1. `rho` is positive and normalized;
2. `rho` lives on the primitive one-cell algebra itself, with no extra
   same-cell weighting datum;
3. `rho` is invariant under exact no-datum relabelings of primitive one-cell
   events.

The third line is the real candidate upgrade. Algebraically, the cleanest
version is:

`U rho U^dagger = rho`

for every exact local relabeling unitary `U` on the primitive one-cell event
algebra.

## Theorem 1: local relabeling invariance forces the tracial state

Assume `rho` is a normalized state on `M_16(C)` invariant under the exact
primitive-cell relabeling automorphisms.

Then

`rho = I_16 / 16`.

### Proof

It is enough to impose invariance under two finite classes of relabelings:

1. **primitive sign-flip unitaries**

   `D_i = I - 2 P_i`,

   one for each primitive atom `P_i`;

2. **primitive swap unitaries**

   `S_(ij)`,

   exchanging primitive basis states `i` and `j`.

These already generate enough exact relabelings to fix the state.

Write `rho_(ij)` for the matrix entries of `rho` in the primitive basis.

### Step 1: sign-flip invariance kills off-diagonal entries

For `i != j`, invariance under `D_i` gives

`rho = D_i rho D_i`.

But the `(i,j)` entry transforms as

`(D_i rho D_i)_(ij) = - rho_(ij)`.

So

`rho_(ij) = - rho_(ij)`,

hence

`rho_(ij) = 0`

for every `i != j`.

Therefore `rho` is diagonal in the primitive projector basis.

### Step 2: swap invariance equalizes all diagonal entries

Now let `d_i = rho_(ii)`.

Invariance under the swap `S_(ij)` gives

`rho = S_(ij) rho S_(ij)^dagger`,

so the diagonal entries satisfy

`d_i = d_j`

for every pair `i,j`.

Therefore all sixteen diagonal entries are equal:

`d_i = d`

for all `i`.

### Step 3: normalization fixes the value

Since `Tr(rho) = 1`,

`16 d = 1`,

so

`d = 1/16`.

Hence

`rho = I_16 / 16`.

This is the unique normalized relabeling-invariant state on the primitive
cell.

## Corollary 1: quarter follows immediately once the state theorem is accepted

The direct counting theorem already closes

`c_cell(rho) = Tr(rho P_A)`.

So with

`rho_cell = I_16 / 16`

and `rank(P_A) = 4`, one gets

`c_cell = Tr((I_16 / 16) P_A) = 4/16 = 1/4`.

Then the direct Planck chain closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

## Why this is cleaner than the old bit-flip witness

The previous sufficient witness was full local `G_4` bit-flip invariance.

That is one concrete transitive subgroup on the primitive basis, but it is not
the conceptual core. The conceptual core is:

> source-free local data have no preferred primitive event.

The automorphism/traciality formulation states that principle directly.

So if this route closes, the strongest theorem wording should be about
primitive-cell relabeling invariance or local traciality, not about a special
Planck-only flip trick.

## Honest status

This note does **not** claim that the theorem above is already retained.

The exact mathematics is straightforward:

- relabeling-invariant state on `M_16(C)` implies `I_16 / 16`.

But the physical premise

`source-free local state = no-datum relabeling-invariant state on the full primitive cell`

is still new relative to the currently accepted retained stack.

So the honest current status is:

- **strong direct theorem candidate**
- **cleaner than the old bit-flip packaging**
- **not yet retained**
- **if promoted, it would close the last Planck blocker directly**

## Safe wording

**Can claim**

- the counting law is already closed, so the last live issue is a primitive
  local state theorem;
- the cleanest direct candidate is source-free local traciality on `M_16(C)`;
- relabeling invariance on the primitive cell forces `rho_cell = I_16 / 16`
  exactly;
- if that physical premise is accepted, quarter and `a = l_P` follow
  immediately.

**Cannot claim**

- that the current accepted retained package already proves the relabeling
  invariance premise;
- that Planck is now retained-derived on this branch;
- that the old underdetermination theorem is gone without this new state law.

## Command

```bash
python3 scripts/frontier_planck_source_free_local_automorphism_traciality_candidate.py
```
