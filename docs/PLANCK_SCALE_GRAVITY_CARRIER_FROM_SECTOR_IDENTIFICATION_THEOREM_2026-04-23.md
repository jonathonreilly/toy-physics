# Planck-Scale Gravity Carrier From Sector Identification Theorem

**Date:** 2026-04-23
**Status:** branch-local theorem-grade carrier note for remaining issue #2
**Audit runner:** `scripts/frontier_planck_gravity_carrier_from_sector_identification_theorem.py`

## Question

Why should the primitive worldtube count be the microscopic carrier of
gravitational area/action, rather than merely a count that happens to give the
right coefficient after a later match?

## Bottom line

On the retained physical `Cl(3)` / `Z^3` Planck packet, the correct statement
is conditional but sharp:

> If the semiclassical gravitational boundary/action sector is identified with
> the local source-free codimension-1 worldtube-incidence sector of the
> time-locked primitive cell, then the microscopic carrier is uniquely
> `N_grav = P_A = 1_(|eta| = 1)`.

This is stronger than a numerical fit. The matching premise selects an object
class: local additive one-step worldtube incidence counts on the same physical
boundary surface. Inside that object class, residual symmetry, time-completeness,
spatial isotropy, primitive unit-count semantics, and no-quotient physical
multiplicity force the full primitive worldtube packet `P_A`.

This note does **not** derive semiclassical gravity from the cell algebra alone.
It honestly scopes the remaining physical input as a sector-identification
input, not as a hidden value of the coefficient.

## Relation to existing notes

This file links the already retained pieces rather than editing them:

- [PLANCK_SCALE_GRAVITATIONAL_AREA_ACTION_CARRIER_IDENTIFICATION_THEOREM_2026-04-23.md](./PLANCK_SCALE_GRAVITATIONAL_AREA_ACTION_CARRIER_IDENTIFICATION_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_AREA_ACTION_NORMALIZATION_THEOREM_2026-04-23.md](./PLANCK_SCALE_AREA_ACTION_NORMALIZATION_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md](./PLANCK_SCALE_NATIVE_DERIVATION_THEOREM_PACKET_2026-04-23.md)
- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md)
- [PLANCK_SCALE_UNIVERSAL_PRIMITIVE_COUNTING_TRACE_THEOREM_2026-04-23.md](./PLANCK_SCALE_UNIVERSAL_PRIMITIVE_COUNTING_TRACE_THEOREM_2026-04-23.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)

The earlier carrier-identification theorem says the remaining denial is narrow:
deny that the primitive boundary count is the microscopic carrier of
gravitational area/action. This note makes that denial maximally explicit.

## Setup

The primitive time-locked cell is

`H_cell = span{|eta> : eta in {0,1}^4}`,

with

`eta = (eta_t, eta_x, eta_y, eta_z)`.

Let `P_eta = |eta><eta|`. The vacuum atom is `0000`. The minimal nonzero shell
adjacent to the vacuum is

`S_1 := {eta : |eta| = 1}`.

It splits under the residual spatial permutation group `S_3` into:

- the temporal orbit `T = {1000}`;
- the spatial orbit `S = {0100, 0010, 0001}`.

Define

`P_t := P_1000`,

`P_s := P_0100 + P_0010 + P_0001`,

`P_A := P_t + P_s = sum_(|eta| = 1) P_eta`.

The section-canonical worldtube-selector theorem already forces `P_A` as the
coarse time-complete and spatially isotropic one-step worldtube sector. The
worldtube-to-boundary counting theorem already proves that a primitive
one-step incidence counter is `N_cell = P_A`.

## Matching premise: Gravity-Sector Identification (GSI)

The remaining physical premise is:

**GSI.** The continuum gravitational boundary/action sector of the accepted
physical `Cl(3)` / `Z^3` package is the long-distance realization of the local,
source-free, time-locked codimension-1 worldtube-incidence sector. Therefore
the microscopic object matched to

`S_grav / k_B = A c_light^3 / (4 G hbar) = A / (4 l_P^2)`

must be a local additive count of primitive one-step worldtube incidences on
the same physical boundary surface.

GSI is not a numerical input. It does not say `c_cell = 1/4`. It does not say
`a = l_P`. It does not choose a coefficient. It chooses which microscopic
sector is being called the gravitational area/action sector.

GSI is also not proven by this note from bare cell algebra. If a reviewer
denies GSI, the branch still has the exact primitive counting coefficient
`Tr((I_16 / 16) P_A) = 1/4`, but the physical conclusion
`a^2 = l_P^2` is not obtained from these notes.

## Definition: admissible microscopic gravitational area/action carrier

Given GSI, an admissible one-cell microscopic carrier `N` for the leading
gravitational boundary/action density must satisfy:

1. **same-surface locality:** `N` acts on the retained one-cell physical event
   algebra at a boundary section;
2. **codimension-1 worldtube support:** `N` is supported on primitive one-step
   incidences adjacent to the vacuum cell, hence on `S_1`;
3. **atomic count semantics:** `N` counts physical lattice atoms and is
   diagonal in the `|eta>` basis;
4. **exclusive additivity:** counts on disjoint one-step atoms add;
5. **source-free universality:** no source, prepared state, curvature scalar,
   or exterior environment datum is needed to define the operator;
6. **residual spatial invariance:** the three spatial one-step atoms are
   counted equally under the exact residual `S_3`;
7. **time-completeness:** the carrier contains the unique temporal unit step;
8. **spatial isotropy:** the carrier contains the whole spatial one-step orbit;
9. **primitive unit incidence:** each admitted one-step incidence contributes
   one unit of count;
10. **no proper quotient:** the full retained physical packet is counted; a
    quotient that discards exact multiplicity is not the same physical carrier.

These conditions are deliberately about the carrier object, not about the
target number. None contains `1/4`, `l_P`, or Newton's constant.

## Theorem 1: GSI reduces the gravity carrier to a primitive incidence counter

Assume GSI. Then the leading local microscopic gravitational area/action carrier
is an admissible primitive one-step incidence counter in the sense above.

### Proof

The gravitational boundary/action law is a leading local area density:

`S_grav / k_B = A / (4 l_P^2)`.

It is codimension-1, extensive in boundary area, and source-free at the level
of the universal density. Under GSI, the microscopic representative must live
on the same boundary surface and in the same local codimension-1 sector.

On the retained time-locked physical cell, the only primitive codimension-1
incidences adjacent to the vacuum are the four Hamming-weight-one atoms in
`S_1`. Higher Hamming-weight atoms are not primitive one-step boundary
incidences; they add extra local occupation data. Local curvature scalars,
free-energy scalars, reduced-vacuum expectations, and prepared-state
observables are different object classes because they require non-count
weights or additional data beyond the primitive incidence sector.

Therefore GSI does not permit an arbitrary local scalar. It reduces the
microscopic gravity-carrier problem to the primitive one-step incidence-counter
problem on `S_1`.

## Theorem 2: local one-step incidence counters have only two weights

Every local, additive, atomic, residual-invariant, minimal-shell count operator
has the form

`N_(u_t,u_s) = u_t P_t + u_s P_s`,

where `u_t` and `u_s` are nonnegative integers.

### Proof

Minimal-shell support restricts the operator to the four atoms of `S_1`.
Atomic count semantics and exclusive additivity make the operator diagonal with
nonnegative integer atomic eigenvalues. Residual `S_3` invariance forces the
three spatial atomic eigenvalues to agree. The temporal one-step atom is its
own residual orbit. Hence exactly two integer weights remain: `u_t` on `P_t`
and `u_s` on `P_s`.

## Theorem 3: GSI forces `N_grav = P_A`

Under GSI, the unique admissible microscopic gravitational area/action carrier
is

`N_grav = P_A`.

### Proof

By Theorem 1, the carrier is a primitive one-step incidence counter. By
Theorem 2, it is `N_(u_t,u_s)`.

Time-completeness excludes `u_t = 0`: a spacetime worldtube carrier cannot
omit the unique temporal one-step incidence.

Spatial isotropy excludes dropping the spatial orbit: the retained `3+1`
boundary structure distinguishes time from space but does not distinguish one
spatial axis from another.

Primitive unit-incidence semantics excludes arbitrary fitted weights. A
primitive one-step incidence contributes one count unit. Thus

`u_t = 1`,

`u_s = 1`.

Therefore

`N_grav = N_(1,1) = P_t + P_s = P_A`.

No numerical coefficient has been inserted. The coefficient appears only after
applying the source-free cell state to the forced carrier:

`c_cell = Tr(rho_cell P_A)`.

On the one-axiom source-free state surface,

`rho_cell = I_16 / 16`,

so

`c_cell = Tr((I_16 / 16) P_A) = 4/16 = 1/4`.

## Alternative carriers and why they are not the same object

The theorem rules out the following alternatives inside the GSI object class:

- `0` is not a nonzero gravitational area/action carrier.
- `P_t` is time-only and omits the spatial boundary orbit.
- `P_s` is space-only and omits the clock step needed for a spacetime
  worldtube.
- `u_t P_t + u_s P_s` with `u_t != u_s` imports a non-count anisotropic
  weighting not present in the time-locked unit-incidence sector.
- `k P_A` with integer `k > 1` counts `k` copies of each incidence and is not
  the primitive carrier.
- A quotient-visible sector such as `P_q` is not an atomic physical-lattice
  count and discards retained multiplicity.
- A scalar Schur/free-energy observable is a different object class.
- A generic reduced-vacuum expectation depends on additional data such as an
  embedding and a state.
- A local curvature or field-strength density belongs to the geometric-scalar
  class, not the primitive worldtube-incidence class.

These exclusions do not say those objects are meaningless. They say they are
not the microscopic carrier selected by GSI for the leading gravitational
area/action density.

## Consequence for normalization

Once `N_grav = P_A` is identified as the microscopic carrier and the source-free
state theorem gives `c_cell = 1/4`, the standalone normalization theorem applies:

`S_cell / k_B = c_cell A / a^2`,

`S_grav / k_B = A / (4 l_P^2)`.

Equating densities gives

`a^2 = 4 c_cell l_P^2`.

Substituting `c_cell = 1/4` gives

`a^2 = l_P^2`.

This final step imports the standard gravitational area/action law and GSI. It
does not import the lattice spacing.

## What is forced versus still physical input

Forced inside the retained Planck packet plus GSI:

- the carrier object is a count observable, not a scalar energy functional;
- the carrier support is the primitive Hamming-weight-one worldtube sector;
- residual symmetry and time-lock reduce the count to `u_t P_t + u_s P_s`;
- primitive unit-incidence semantics forces `u_t = u_s = 1`;
- therefore `N_grav = P_A`;
- with the source-free default state, the coefficient is `1/4`.

Still physical input:

> the continuum gravitational boundary/action sector is the long-distance
> realization of this primitive worldtube-incidence sector.

That is the sector-identification input. A fully stronger result would derive
the gravitational continuum action directly from the microscopic dynamics and
show that its boundary term is exactly the continuum limit of `P_A`. This note
does not claim that stronger result.

## Hostile-review safe formulation

Safe claim:

> Conditional on GSI, the primitive worldtube count `P_A` is the unique local
> microscopic carrier of gravitational area/action available on the retained
> Planck packet, and the later `a = l_P` normalization follows without fitting a
> coefficient.

Unsafe claim:

> The bare cell algebra alone proves that gravity must exist and must be the
> `P_A` sector.

The second sentence is not established here. The first sentence is the theorem.

## Command

```bash
python3 scripts/frontier_planck_gravity_carrier_from_sector_identification_theorem.py
```
