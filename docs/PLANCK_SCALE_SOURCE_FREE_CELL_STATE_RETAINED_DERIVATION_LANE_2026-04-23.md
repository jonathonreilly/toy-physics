# Planck-Scale Source-Free Cell-State Retained Derivation Lane

**Date:** 2026-04-23  
**Status:** science-only exact reduction / no-go on the source-free-state step  
**Audit runner:** `scripts/frontier_planck_source_free_cell_state_retained_derivation_lane.py`

## Question

Can the direct Planck route derive the source-free full-cell state

`rho_cell = I_16 / 16`

from already-accepted retained structure only, without adding a new stronger
symmetry principle by hand?

The intended starting point is the direct worldtube route:

- exact local time-locked cell `H_cell = C^16`,
- exact one-step worldtube packet `P_A`,
- exact packet coefficient candidate
  `c_wt = Tr(rho_cell P_A)`,

together with the non-Schur occupation classification on the same cell.

## Bottom line

No.

The strongest honest result is an exact **reduction / underdetermination
theorem**.

1. On the direct worldtube route, the already-accepted retained structure
   fixes the cell carrier, fixes the packet `P_A`, and fixes the residual
   exact symmetry after time-lock.
2. On that retained surface, every diagonal source-free candidate state is
   classified by the eight orbit weights

   `a_(t,w)`, with `(t,w) in {0,1} x {0,1,2,3}`,

   together with one normalization equation.
3. So the current retained structure leaves an exact **7-parameter family** of
   source-free candidate states on the full `C^16` cell.
4. The already-accepted scalar observable principle does not reduce this
   family, because it is an observable-generator theorem, not a state-selector
   theorem.
5. The already-accepted Hilbert/Born event grammar does not reduce this
   family either, because `mu_rho(P) = Tr(rho P)` is conditional on a chosen
   state `rho`; it does not choose `rho`.
6. Therefore the democratic state

   `rho_cell = I_16 / 16`

   is **not derivable** from the currently accepted retained stack alone.

So closure is **not** achieved on this lane.

The sharpest exact remaining need is:

> a retained **source-free local traciality theorem** on the full time-locked
> cell algebra.

This is stronger than the old reduction to residual `S_3`, but weaker and
cleaner than simply inserting full four-bit flip invariance as a new symmetry
postulate. The stronger flip-invariance route is still a sufficient witness,
but the real missing content is a state-selection theorem:

> why source-free local occupancy should be the tracial/no-preferred-projector
> state on the full primitive cell.

## Inputs

This lane uses only already-opened branch-local and accepted support surfaces:

- [PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md](./PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md)
- [PLANCK_SCALE_NON_SCHUR_AXIS_OCCUPATION_LAW_LANE_2026-04-23.md](./PLANCK_SCALE_NON_SCHUR_AXIS_OCCUPATION_LAW_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_PROJECTOR_VALUED_OBSERVABLE_PRINCIPLE_LANE_2026-04-23.md](./PLANCK_SCALE_PROJECTOR_VALUED_OBSERVABLE_PRINCIPLE_LANE_2026-04-23.md)
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [SINGLE_AXIOM_HILBERT_NOTE.md](./SINGLE_AXIOM_HILBERT_NOTE.md)
- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)

What those notes already fix:

1. the local carrier is the exact four-bit cell
   `H_cell = span{|eta> : eta in {0,1}^4}`;
2. time-lock distinguishes one temporal bit and leaves residual spatial
   permutation symmetry `S_3`;
3. the physical coarse packet is the exact Hamming-weight-one packet
   `P_A = sum_(|eta|=1) P_eta`;
4. the factor-of-two packet lift is already closed on the readout side;
5. the scalar observable principle fixes scalar generators from partition
   factorization;
6. the Hilbert/Born side fixes event readouts on a chosen state.

This note asks whether any of those already-retained ingredients also force the
source-free state on the full cell.

## Setup

Work on the exact time-locked four-bit basis

`eta = (eta_t, eta_x, eta_y, eta_z) in {0,1}^4`.

Let

- `P_eta = |eta><eta|`,
- `w_s(eta) = eta_x + eta_y + eta_z`,
- `Pi_(t,w)` be the projector onto the orbit
  `{eta : eta_t = t, w_s(eta) = w}`.

After time-lock, the temporal bit is distinguished while the three spatial bits
are permuted. So the exact residual label symmetry on the primitive cell is

`G_res = S_3`,

acting on `(eta_x, eta_y, eta_z)` and fixing `eta_t`.

Its orbits are classified exactly by the pair

`(t,w) = (eta_t, w_s(eta)) in {0,1} x {0,1,2,3}`.

So there are exactly eight orbit classes.

## Definition: retained-direct source-free candidate state

Call `rho` a **retained-direct source-free candidate state** if:

1. `rho` is diagonal on the primitive cell projectors `P_eta`;
2. `rho` is positive and normalized;
3. `rho` is invariant under the retained exact residual symmetry `G_res = S_3`.

This is exactly the state grammar already admitted by the direct worldtube
route plus the non-Schur occupation classification. It does **not** add a new
full-cell transitivity theorem.

## Theorem 1: exact classification of retained-direct source-free candidates

Every retained-direct source-free candidate state has the form

`rho = sum_(t=0)^1 sum_(w=0)^3 a_(t,w) Pi_(t,w)`,

with

- `a_(t,w) >= 0`,
- normalization
  `sum_(t,w) binom(3,w) a_(t,w) = 1`.

### Proof

Diagonality gives

`rho = sum_eta p(eta) P_eta`.

Residual `S_3` invariance means

`p(eta) = p(sigma eta)`

for every spatial permutation `sigma`.

Therefore `p(eta)` can depend only on the residual orbit data
`(eta_t, w_s(eta))`. These are exactly the eight pairs
`(t,w) in {0,1} x {0,1,2,3}`.

Each orbit `(t,w)` has multiplicity `binom(3,w)`. So positivity and
normalization are exactly the conditions written above.

That is the complete classification.

## Corollary 1: current retained structure leaves a 7-parameter family

There are eight orbit weights `a_(t,w)` and one normalization equation.
So the retained-direct source-free family has exact affine dimension `7`.

In particular, the democratic state

`rho_tr := I_16 / 16`

is only one point in this family, not the unique point forced by current
retained structure.

## Two explicit admissible witness states

The underdetermination is not abstract.

### Witness A: democratic/tracial state

Take

`rho_tr = I_16 / 16`.

This is diagonal, positive, normalized, and `S_3`-invariant.

It gives

`Tr(rho_tr P_A) = 4 / 16 = 1/4`.

### Witness B: packet-light residual state

Let the four one-hot states each carry weight `1/32`, and let every remaining
state carry weight `7/96`.

Equivalently,

`rho_lt = (1/32) P_A + (7/96) (I_16 - P_A)`.

This state is also diagonal, positive, normalized, and `S_3`-invariant.

But now

`Tr(rho_lt P_A) = 4 * (1/32) = 1/8`,

not `1/4`.

So the current retained-direct grammar admits at least two distinct source-free
candidate states with different worldtube-packet coefficients.

That is already enough to rule out a retained derivation of
`rho_cell = I_16 / 16` from the current accepted stack alone.

## Theorem 2: the accepted scalar observable principle does not select the state

The accepted scalar observable principle fixes a scalar generator

`W[J] = log |det(D+J)| - log |det D|`

from exact partition factorization and additivity.

But this is an **observable-generator theorem**, not a theorem selecting a
density matrix on the primitive cell event algebra.

So the scalar observable principle does not collapse the 7-parameter family of
retained-direct source-free candidate states.

### Reason

The scalar principle tells us how scalar observables depend on sources once the
microscopic source-response engine is fixed. It does not supply a separate law
of the form

`rho_source-free = ...`

on the full primitive cell event algebra.

This is exactly why the old scalar Schur route produced a scalar boundary
observable, not a source-free full-cell state.

## Theorem 3: the accepted Hilbert/Born event grammar does not select the state

The accepted Hilbert/Born event grammar says that for a chosen state `rho` and
projector `P`, the event readout is

`mu_rho(P) = Tr(rho P)`.

But this is conditional on `rho`. It is not a theorem selecting `rho`.

Therefore the Hilbert/Born side also does not collapse the 7-parameter
retained-direct family.

### Reason

Both witness states above define perfectly good Born/event readouts on the same
projector algebra:

- `mu_tr(P) = Tr(rho_tr P)`,
- `mu_lt(P) = Tr(rho_lt P)`.

They obey the same normalization and exclusive-event additivity rules, but they
give different values on the same physical packet `P_A`.

So the accepted event grammar distinguishes probabilities **given a state**; it
does not identify the source-free state itself.

## Corollary 2: exact no-go for retained derivation from the current accepted stack

From Theorems 1-3:

- the current retained-direct stack admits a 7-parameter family of
  source-free candidate states;
- the currently accepted scalar observable principle does not select one point
  in that family;
- the currently accepted Hilbert/Born event grammar does not select one point
  either.

Therefore:

> `rho_cell = I_16 / 16` is **not derivable** from the already-accepted
> retained structure alone.

This is the sharpest exact no-go available on the current lane.

## What additional retained theorem would still be needed

The smallest honest missing theorem is:

> **Source-Free Local Traciality Theorem.**
> On the exact time-locked primitive cell algebra `M_16(C)`, the source-free
> local state is the unique normalized state assigning equal weight to every
> primitive one-cell projector.

On the diagonal event algebra this is exactly

`rho_cell = I_16 / 16`.

This is the real missing content.

### Why this is sharper than "just add full flip symmetry"

The older sufficient witness was:

`source-free state is invariant under the full local flip group G_4 ~= (Z_2)^4`.

That indeed forces the democratic state because the action is transitive on the
16 primitive cells.

But that is stronger than the minimal missing idea. The real missing theorem is
not "there is a new symmetry postulate"; it is:

> source-free local occupancy has no preferred primitive projector on the full
> cell.

That can be realized in several equivalent ways:

1. full local flip transitivity (strong operational witness);
2. local traciality / no-preferred-projector theorem on `M_16(C)`;
3. an exact source-free cell-counting theorem from the boundary/action side
   that bypasses explicit state language and lands the same uniform weights.

Any one of those would be enough. None is yet retained.

## Consequence for the direct Planck route

The direct route is now reduced even more cleanly:

- `P_A` is already fixed;
- the packet coefficient `c_wt = Tr(rho_cell P_A)` is already the right direct
  object;
- the missing source-free content is not packet combinatorics anymore;
- it is the local state-selection theorem.

So the source-free-state route does **not** close Planck here.

What it does achieve is the sharpest exact reduction:

> the current retained stack leaves a 7-parameter source-free family, and the
> exact missing upgrade is a source-free local traciality theorem on the full
> `C^16` primitive cell.

## Safe wording

**Can claim**

- the current retained direct route does not yet derive
  `rho_cell = I_16 / 16`;
- the current retained direct route leaves an exact 7-parameter family of
  source-free candidate states on the full cell;
- neither the accepted scalar observable principle nor the accepted Born/event
  grammar selects one unique source-free state;
- the exact remaining need is a source-free local traciality theorem (or an
  equivalent retained theorem with the same diagonal consequence).

**Cannot claim**

- that the source-free state is already retained-derived on the current lane;
- that the existing one-axiom Hilbert/locality/information notes already force
  the tracial state on the full primitive cell;
- that Planck is retained-closed from the direct route on the basis of the
  current state law.

## Command

```bash
python3 scripts/frontier_planck_source_free_cell_state_retained_derivation_lane.py
```
