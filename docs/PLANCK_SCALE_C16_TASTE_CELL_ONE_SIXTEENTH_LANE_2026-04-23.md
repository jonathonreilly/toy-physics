# Planck-Scale `C^16` Taste-Cell One-Sixteenth Lane

**Date:** 2026-04-23  
**Status:** exact reduction theorem on the structural `16`; not yet a closure theorem  
**Audit runner:** `scripts/frontier_planck_c16_taste_cell_one_sixteenth_lane.py`

## Question

Can the Planck-lane target

`q_* = 1/16`

be derived from a genuine `C^16` / taste-cell theorem, rather than from a
post-hoc coefficient match?

Equivalently:

- is the Planck `1/16` the same structural `16` as the hierarchy/taste
  `2^4 = 16`,
- or is it a different `16` coming only from the cubical-defect normalization
  `a^2 / l_P^2 = 16 q_*`,
- and if the structural `16` is real, what exactly is still missing?

## Bottom line

Yes, there is a genuine same-structure reduction, but it is not yet the final
physical closure.

The important structural fact is:

- the meaningful non-hierarchy `16` across the repo is the full four-bit
  staggered/taste-cell carrier `eta in {0,1}^4`, i.e. the exact `2^4 = 16`
  minimal 4D hypercube corners;
- the canonical democratic state on that carrier is
  `rho_cell = I_16 / 16`;
- every primitive taste cell therefore carries exact weight `1/16`;
- the four axis states in the `hw=1` sector,
  `{1000, 0100, 0010, 0001}`,
  inherit the exact conditioned state `I_4 / 4`, hence exactly `2` bits;
- therefore the existing Planck-lane target
  `kappa_info^(bit) = 1/32`
  is exactly
  `1/(2 * 16)`
  on the same underlying carrier:
  one primitive four-bit taste cell has share `1/16`, while the induced
  axis-sector information carrier has `2` bits.

So the branch now has a sharp reduction theorem:

> the Planck-lane `1/16` can be realized as the canonical primitive-cell share
> of the same `2^4` structural carrier that underlies the hierarchy/taste
> lane.

What is **not** yet derived is the final physical identification

`q_* = primitive C^16 taste-cell share`.

So this lane lands outcome (2), not outcome (1):

- **same structural `16`: YES**
- **exact canonical `1/16` on the `C^16` taste-cell carrier: YES**
- **physical closure `q_* = 1/16` without an extra identification step: NOT YET**

## Where the structural `16` really appears

The useful non-hierarchy appearances of `16` are not the many incidental
`16 pi^2`, card labels, or parameter defaults. The meaningful ones are:

1. the full four-dimensional staggered carrier `C^16`, with `2^4 = 16`
   corners / cell states on the minimal 4D cube;
2. the `Cl(4)` / chirality extension that splits the 4D carrier into the
   accepted `C^16` surfaces used elsewhere in the repo;
3. the full-space `C^16` normalization surfaces, where exact averaging over
   the entire 16-state carrier already appears as a physical bookkeeping move.

So the right scientific comparison is:

- **hierarchy lane:** `16 = 2^4` from the four-dimensional staggered
  taste/corner count;
- **this Planck lane:** the same `2^4 = 16` gives the canonical primitive
  taste-cell share `1/16`.

This is **not** the same as the separate defect-normalization `16` coming from

`a^2 / l_P^2 = 8 pi q_* / eps_*`

at the minimal cubical defect

`eps_* = pi/2`,

which yields

`a^2 / l_P^2 = 16 q_*`.

Those are conceptually different `16`s:

- one is the **full 4D cell count**,
- the other is the **Einstein/Regge defect coefficient**.

Exact Planck would identify them numerically on the same lane. They are not
automatically the same theorem.

## The full `C^16` taste-cell carrier

Work on the exact four-bit minimal hypercube basis

`H_cell = span{|eta> : eta in {0,1}^4}`.

This is the cleanest first-principles carrier for the structural `16`: the
four coordinates are the four minimal 4D lattice bits, and the full cell basis
has cardinality

`|{0,1}^4| = 16`.

On this carrier define the canonical democratic state

`rho_cell = I_16 / 16`.

For each primitive taste cell `eta`, let

`P_eta = |eta><eta|`.

Then exactly

`Tr(rho_cell P_eta) = 1/16`

for every `eta`.

This is the precise same-structure `1/16`: it is not fitted, and it does not
use the Planck coefficient formula at all. It is the canonical primitive-cell
share of the exact `2^4` taste-cell carrier.

## The axis `hw=1` sector and the exact `2` bits

Inside the full 4D cube, the Hamming-weight-one sector is

`A = {1000, 0100, 0010, 0001}`.

These are the four canonical axis cells. They form the exact four-state axis
carrier that matches the abstract `3+1` time-locked carrier up to basis
relabeling:

- three spatial axis states,
- one temporal axis state.

Let

`P_A = sum_(eta in A) P_eta`.

Under the full democratic state,

`Tr(rho_cell P_A) = 4/16 = 1/4`.

Condition on the axis sector:

`rho_A = P_A rho_cell P_A / Tr(rho_cell P_A) = I_4 / 4`.

Therefore the induced axis-sector carrier is exactly the democratic four-state
carrier

`(1/4, 1/4, 1/4, 1/4)`,

whose Shannon/von Neumann information is

`I_A = log 4 = 2 bits`.

This is the clean bridge to the already-landed time-locked lane:

- the full `C^16` taste-cell carrier gives the fine-cell share `1/16`;
- the induced `hw=1` axis carrier gives the coarse information `2` bits.

## Exact `1/32` per bit from the same carrier

If the elementary action phase `q_*` is identified with the primitive-cell
share of the full `C^16` taste-cell carrier, then

`q_* = 1/16`.

On the induced axis carrier,

`I_* = 2 bits`.

So the converted information/action constant becomes

`kappa_info^(bit) = q_* / I_* = (1/16) / 2 = 1/32`.

This is the cleanest meaning of the user-observed pattern

`1/32 = 1/(2 * 16)`:

- the `16` is the full `2^4` taste-cell count;
- the `2` is the exact information content of the induced democratic four-axis
  carrier.

So on this lane the relation is not numerology. It is an exact carrier-level
identity once the primitive-cell-share reading is adopted.

## What is actually proved

This lane proves three exact statements.

### Theorem A — Same structural `16`

The relevant Planck-lane `16` can be realized on the same `2^4` four-bit
taste-cell carrier as the hierarchy/taste `16`.

### Theorem B — Canonical primitive-cell one-sixteenth

On the democratic full `C^16` cell state, every primitive cell has exact share
`1/16`.

### Theorem C — Exact coarse/fine relation

Conditioning the same democratic full-cell state to the `hw=1` axis sector
produces the exact democratic four-state carrier with information `2` bits, so

`(primitive cell share) / (axis-carrier information) = (1/16) / 2 = 1/32`.

## What is still open

The remaining scientific gap is now very specific:

> prove that the physical elementary action phase `q_*` is the primitive-cell
> share on the full `C^16` taste-cell carrier.

Without that, the lane is not fully closed. What is closed is the structural
reduction:

- the Planck `1/16` can come from the same `2^4` carrier as the hierarchy
  `16`;
- the matching is exact and canonical;
- the final missing step is the physical selector law that reads `q_*` from
  that primitive-cell share.

## Best honest verdict

This lane is stronger than a coefficient echo and weaker than a full closure.

It shows:

- the structural `16` really does recur beyond the hierarchy lane;
- the recurrence is meaningful and exact on the same `2^4` carrier;
- the Planck `1/16` is not forced by the defect coefficient alone;
- the remaining burden is one sharp physical-identification theorem, not an
  unexplained numerical coincidence.

## Reviewer-safe wording

> On the exact four-bit staggered/taste-cell carrier `eta in {0,1}^4`, the
> canonical democratic state assigns weight `1/16` to each primitive cell.
> Conditioning to the axis/Hamming-weight-one sector
> `{1000,0100,0010,0001}` gives the exact democratic four-state carrier with
> information `2` bits. Thus the Planck-lane target `1/32` per bit can be
> realized exactly as `(1/16)/2` on the same structural `2^4` carrier that
> underlies the hierarchy/taste `16`. The remaining open step is the physical
> identification of the elementary action phase with that primitive-cell share.
