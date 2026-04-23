# Planck-Scale Worldtube-to-Boundary Cell-Counting Theorem Lane

**Date:** 2026-04-23  
**Status:** science-only direct-counting theorem plus sharp retained residual  
**Audit runner:** `scripts/frontier_planck_worldtube_to_boundary_cell_counting_theorem_lane.py`

## Question

The direct Planck chain was reduced to one final bridge:

`c_cell = Tr(rho_cell P_A)`,

where:

- `P_A` is the forced minimal one-step worldtube packet on the time-locked
  four-bit cell;
- `rho_cell` is the source-free full-cell state;
- `Tr(rho_cell P_A)` is the exact worldtube-packet coefficient.

Can that bridge be closed directly, without reusing the older scalar
"boundary pressure" grammar?

More concretely:

> why should an elementary codimension-1 gravitational boundary cell count the
> minimal one-step worldtube packet?

## Bottom line

Yes, at the level of the **cell-counting law** itself.

If one asks for an **elementary boundary cell coefficient** in the direct
physical-lattice sense, then the right object is not a Schur free-energy scalar.
It is the expectation value of an integer-valued local count observable on the
exact one-cell event algebra.

On that direct counting grammar, the operator is forced:

1. the exact physical minimal shell is the forced one-step packet

   `P_A = P_t + P_s = sum_(|eta|=1) P_eta`;

2. every elementary codimension-1 cell count observable that is

   - local on one time-locked cell,
   - supported on the minimal shell adjacent to the vacuum,
   - additive on exclusive atomic one-step events,
   - residual-invariant under the exact spatial `S_3`,
   - and integer-valued as a genuine count,

   has the form

   `N_(u_t,u_s) = u_t P_t + u_s P_s`,

   with nonnegative integers `u_t`, `u_s`;

3. if the cell coefficient counts **minimal one-step incidences**, then the
   unique temporal one-hot event and each spatial one-hot event each carry one
   unit count;
4. time-lock removes any independent temporal unit rescaling, so there is no
   remaining same-surface distinction between a temporal unit incidence and a
   spatial unit incidence at the level of the count itself;
5. therefore

   `u_t = u_s = 1`,

   hence the exact boundary-cell count operator is

   `N_cell = P_A`;

6. for every state `rho`,

   `c_cell(rho) = Tr(rho N_cell) = Tr(rho P_A)`;

7. on the strongest current source-free close candidate

   `rho_cell = I_16 / 16`,

   this gives

   `c_cell = Tr(rho_cell P_A) = 4/16 = 1/4`.

So the direct bridge

`c_cell = Tr(rho_cell P_A)`

is closed as a same-surface **cell-counting theorem**.

What remains for retained Planck is now narrower:

> not the cell-counting law, but whether the democratic source-free state
> `rho_cell = I_16 / 16` is itself retained on the accepted stack.

## Inputs

This direct lane uses only already-opened branch-local structures:

- [PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md](./PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_NON_SCHUR_AXIS_OCCUPATION_LAW_LANE_2026-04-23.md](./PLANCK_SCALE_NON_SCHUR_AXIS_OCCUPATION_LAW_LANE_2026-04-23.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)

What those lanes already fix exactly:

1. the local primitive carrier is the time-locked four-bit cell

   `H_cell = span{|eta> : eta in {0,1}^4}`;

2. the physical minimal shell adjacent to the vacuum is the Hamming-weight-1
   packet

   `A = {eta : |eta| = 1}`,

   with exact projector

   `P_A = sum_(eta in A) P_eta`;

3. the full packet is physical, not merely the visible quotient:

   `P_A = P_q + P_E`,

   with the hidden `E` block exact and non-discardable on the retained
   physical-lattice semantics;

4. on the strongest current source-free close candidate,

   `rho_cell = I_16 / 16`,

   so

   `Tr(rho_cell P_A) = 1/4`.

This note attacks only the missing cell-counting identification itself.

## Setup

Work on the exact one-cell basis

`eta = (eta_t, eta_x, eta_y, eta_z) in {0,1}^4`.

Let

`P_eta = |eta><eta|`.

Define the vacuum cell

`0 := (0,0,0,0)`.

The minimal shell adjacent to the vacuum is

`S_1 := {eta : |eta| = 1}`.

It splits into:

- the unique temporal one-hot state

  `T := {(1,0,0,0)}`;

- the spatial one-hot orbit

  `S := {(0,1,0,0),(0,0,1,0),(0,0,0,1)}`.

Define the corresponding projectors

`P_t := P_(1000)`,

`P_s := P_(0100) + P_(0010) + P_(0001)`,

`P_A := P_t + P_s`.

By the section-canonical selector theorem, `P_A` is already the forced coarse
worldtube packet. By the multiplicity-lift theorem, passing to the quotient
block `P_q` would throw away exact physical multiplicity.

## Definition: elementary boundary cell count observable

Call `N` an **elementary boundary cell count observable** if it satisfies:

1. **one-cell locality**: `N` acts on the exact one-cell event algebra;
2. **minimal-shell support**: `N` vanishes off `S_1`;
3. **atomic diagonality**: `N` is diagonal in the atomic physical-lattice
   basis `{|eta>}`;
4. **exclusive-event additivity**: on a disjoint union of atomic one-step
   events, the count is the sum of the atomic counts;
5. **residual invariance**: the three spatial one-hot atoms are counted
   equally under the exact residual `S_3`;
6. **integer count semantics**: atomic eigenvalues are nonnegative integers,
   because `N` counts incidences rather than energies or amplitudes.

This is deliberately narrower than the old scalar observable grammar: the point
is to model a direct **cell count**, not a free-energy density.

## Theorem 1: exact classification of local minimal-shell cell counters

Every elementary boundary cell count observable has the form

`N_(u_t,u_s) = u_t P_t + u_s P_s`,

with nonnegative integers `u_t`, `u_s`.

### Proof

By one-cell locality, minimal-shell support, and atomic diagonality, `N` is a
diagonal combination of atomic projectors on the four one-hot atoms only.

Residual `S_3` invariance identifies the three spatial coefficients, so the
three spatial one-hot atoms share one common coefficient `u_s`, while the
unique temporal one-hot atom has coefficient `u_t`.

Exclusive-event additivity means the observable on a disjoint packet is the sum
of those atomic contributions, and integer count semantics force

`u_t, u_s in Z_(>=0)`.

Therefore every such counter is exactly

`N_(u_t,u_s) = u_t P_t + u_s P_s`.

So the direct cell-counting bridge is now only a two-integer problem.

## Theorem 2: minimal one-step incidence counting forces `N_cell = P_A`

Assume the elementary codimension-1 gravitational boundary cell coefficient is
the count of **minimal one-step incidences** of the physical worldtube packet.

Then the unique local minimal-shell count observable is

`N_cell = P_A`.

### Proof

Each atomic state in `S_1` represents exactly one minimal one-step incidence of
the time-locked cell:

- `(1,0,0,0)` is the unique temporal one-step incidence;
- `(0,1,0,0)`, `(0,0,1,0)`, `(0,0,0,1)` are the three spatial one-step
  incidences.

Because `N_cell` is a genuine count, each such minimal atomic incidence carries
unit count `1`, not an arbitrary fitted weight.

So on the classification of Theorem 1,

`u_t = 1`,
`u_s = 1`.

Therefore

`N_cell = P_t + P_s = P_A`.

This is the direct same-surface cell-counting closure of the previously open
bridge.

## Why time-lock matters here

Without time-lock, one might still try to assign distinct unit conventions to
temporal and spatial one-step incidences.

But the time-lock lane already removes any independent temporal rescaling:

`a_s = c a_t`.

So once one is counting **incidences** rather than energies, amplitudes, or
free-energy contributions, there is no same-surface room left for a separate
temporal count unit. A one-step temporal incidence and a one-step spatial
incidence are both unit incidences of the same elementary time-locked cell.

That is exactly why the count operator lands on `P_A`, not on

`u_t P_t + u_s P_s`

with unequal coefficients.

## Theorem 3: quotient-only counting is physically inadmissible

The quotient-visible block `P_q` is not an admissible elementary boundary cell
count observable on the current lane.

### Reason

There are two independent obstructions.

First, `P_q` is not atomic-diagonal on the physical-lattice cell basis, so it
is not a count of atomic one-step incidences at all.

Second, even as a coarse packet surrogate it would discard the exact hidden
doublet block `P_E`, and the current physical-lattice / no-proper-quotient
surface already forbids replacing an exact retained physical packet by a proper
quotient that throws away exact observable multiplicity.

So the direct count object must live on the full packet `P_A`, not the Schur
quotient `P_q`.

## Corollary 1: exact cell-counting law

For every state `rho` on the exact one-cell carrier,

`c_cell(rho) = Tr(rho N_cell) = Tr(rho P_A)`.

So the old open direct bridge

`c_cell = Tr(rho_cell P_A)`

is no longer open at the level of the counting law. It is the exact counting
theorem on the direct route.

## Corollary 2: quarter on the strongest current source-free close candidate

If the source-free full-cell state is

`rho_cell = I_16 / 16`,

then

`c_cell = Tr(rho_cell P_A) = rank(P_A)/16 = 4/16 = 1/4`.

So once the source-free state theorem is in hand, Planck closes on the direct
cell-counting route with no extra coefficient freedom.

## What this does and does not close

### Closed here

- the remaining direct bridge `c_cell = Tr(rho P_A)` as a same-surface
  cell-counting theorem;
- the rejection of quotient-only counting on `P_q`;
- the replacement of the old scalar "boundary pressure" wording by a direct
  elementary boundary-cell counting law.

### Historical residual after this note

This note does **not** prove that the democratic source-free full-cell state

`rho_cell = I_16 / 16`

is already retained on the accepted stack.

The current non-Schur lane still says that exact democraticity follows only
after the stronger full flip-transitivity principle on the time-locked four-bit
cell.

So the sharp retained residual is now:

> not the cell-counting law, but the source-free full-cell occupation law.

Equivalently:

- if the stronger full-cell flip-invariance law is accepted, the direct Planck
  route closes cleanly;
- if not, the direct route remains conditional on that source-free state step.

### Current residual after later notes

That state step is now closed after the later one-axiom bridge, on the
authorized one-axiom semantic surface:

- [PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_ONE_AXIOM_CONSERVATIVE_SEMANTICS_BRIDGE_THEOREM_2026-04-23.md](./PLANCK_SCALE_ONE_AXIOM_CONSERVATIVE_SEMANTICS_BRIDGE_THEOREM_2026-04-23.md)

So the current package-boundary caveat is no longer the counting law and no
longer the state computation itself. It is whether the one-axiom semantic
surface is authorized as load-bearing local state semantics for this lane.

## Safe wording

**Can claim**

- the direct Planck bridge
  `c_cell = Tr(rho P_A)`
  is closed as an elementary cell-counting theorem;
- the correct direct object is a local boundary-cell count observable, not a
  scalar free-energy density;
- after the later one-axiom default-datum theorem, the direct route closes on
  the authorized one-axiom semantic surface.

**Cannot claim**

- that Planck is an unqualified theorem of the older minimal ledger alone;
- that the older scalar Schur/free-energy route gives the Planck quarter.

## Command

```bash
python3 scripts/frontier_planck_worldtube_to_boundary_cell_counting_theorem_lane.py
```
