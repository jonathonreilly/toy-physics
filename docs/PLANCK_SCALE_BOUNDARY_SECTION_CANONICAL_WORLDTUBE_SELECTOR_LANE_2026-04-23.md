# Planck-Scale Boundary Section-Canonical Worldtube Selector Lane

**Date:** 2026-04-23  
**Status:** science-only theorem plus sharp residual obstruction  
**Audit runner:** `scripts/frontier_planck_boundary_section_canonical_worldtube_selector_lane.py`

## Question

The last serious boundary bridge was reduced to the statement

`p_phys = m_axis`,

where

`m_axis = Tr(rho_cell P_A) = 1/4`

is the coarse `C^16` `hw=1` axis-sector mass.

The immediate objection was:

> why should the physical selector live on the four-axis `hw=1` worldtube
> channel at all?

Equivalently:

- does exact time-lock plus exact `3+1` axis structure canonically select the
  coarse four-axis worldtube sector;
- or is the route still only orbit-canonical, with no section theorem;
- and if a canonical sector *is* forced, what ambiguity actually remains?

## Bottom line

The strongest honest result is better than the earlier endpoint no-go.

The current boundary/spacetime structure does force the **coarse** selector
carrier:

1. on the minimal time-locked `3+1` taste cell, the residual symmetry fixes one
   temporal bit and permutes the three spatial bits;
2. on the minimal nonzero shell adjacent to the vacuum cell, the only
   residual-invariant projectors are

   `0`, `P_t`, `P_s`, `P_A = P_t + P_s`,

   where

   - `P_t` projects onto the unique temporal one-hot cell,
   - `P_s` projects onto the three spatial one-hot cells,
   - `P_A` projects onto the full four-axis `hw=1` channel;

3. if the physical boundary/worldtube selector is required to be

   - local on one minimal time-locked cell,
   - supported on the minimal shell adjacent to the vacuum,
   - time-complete,
   - and spatially isotropic,

   then the projector is uniquely forced to be

   `P_A = sum_(|eta|=1) P_eta`;

4. therefore the coarse four-axis worldtube channel is **section-canonical**
   on the current boundary/spacetime stack;
5. what remains non-canonical is any **finer section inside the spatial
   triplet**: the residual spatial permutation symmetry still forbids a
   canonical individual spatial ray.

So the honest verdict is:

> the boundary/spacetime stack is no longer merely orbit-canonical at the
> coarse worldtube level. It canonically selects the `C^16` `hw=1` axis sector.
> The remaining obstruction is finer: no canonical spatial ray inside that
> sector is forced.

Equivalently:

> the coarse worldtube sector is **section-canonical**, while no finer spatial
> ray inside that sector is canonically selected.

In plain terms: no finer spatial ray inside that sector is canonically
selected.

This does **not** yet prove

`p_phys = m_axis`

as a scalar observable law.

What it does prove is the previously missing carrier step:

> the physical selector can be forced onto the coarse `C^16` `hw=1`
> worldtube sector from current time-lock plus `3+1` boundary structure.

## Inputs

This lane uses only already-opened branch-local structures:

- [PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md](./PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md)
- [PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md](./PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md](./PLANCK_SCALE_C16_TASTE_CELL_ONE_SIXTEENTH_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md](./PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md)
- [PLANCK_SCALE_C16_AXIS_MASS_PHYSICAL_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md](./PLANCK_SCALE_C16_AXIS_MASS_PHYSICAL_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md)

What those lanes already fix exactly:

1. exact time-lock gives one temporal direction and three spatial directions;
2. the minimal `3+1` taste-cell carrier is the four-bit cube

   `H_cell = span{|eta> : eta in {0,1}^4}`;

3. the exact coarse candidate for the boundary quarter is the `hw=1` axis
   projector

   `P_A = sum_(eta in {1000,0100,0010,0001}) P_eta`;

4. the surviving open bridge was the physical identification of the boundary
   pressure with the scalar readout on that sector.

This note attacks the carrier-selection step directly.

## Setup

Work on the exact four-bit cell basis

`eta = (eta_t, eta_x, eta_y, eta_z) in {0,1}^4`.

Let

`P_eta = |eta><eta|`.

The vacuum/empty cell is

`0 := (0,0,0,0)`.

The exact time-lock note removes any separate temporal calibration freedom and
distinguishes one time axis from the three spatial axes. The residual discrete
symmetry on the bit labels is therefore the spatial permutation group

`G_res = S_3`

acting on `(eta_x, eta_y, eta_z)` while fixing `eta_t`.

For each state define:

- temporal occupancy `t(eta) := eta_t`,
- spatial weight `w_s(eta) := eta_x + eta_y + eta_z`,
- total Hamming weight `|eta| := t(eta) + w_s(eta)`.

Under `G_res`, the exact orbit of a state is determined by the pair

`(t(eta), w_s(eta))`.

So there are exactly eight residual orbit classes:

- `(0,0)`, `(0,1)`, `(0,2)`, `(0,3)`,
- `(1,0)`, `(1,1)`, `(1,2)`, `(1,3)`.

The minimal nonzero shell adjacent to the vacuum is

`S_1 := {eta : |eta| = 1}`

and it splits into the disjoint residual orbits

- temporal one-hot orbit

  `T := {(1,0,0,0)}`,

- spatial one-hot orbit

  `S := {(0,1,0,0),(0,0,1,0),(0,0,0,1)}`.

Define the corresponding projectors

`P_t := P_(1000)`,

`P_s := P_(0100) + P_(0010) + P_(0001)`,

`P_A := P_t + P_s`.

Then `P_A` is exactly the `hw=1` axis-sector projector already isolated on the
`C^16` bridge lane.

## Theorem 1: minimal-shell invariant selector classification

On the minimal shell `S_1`, the residual-invariant projectors are exactly:

- `0`,
- `P_t`,
- `P_s`,
- `P_A = P_t + P_s`.

### Proof

Any residual-invariant projector supported on `S_1` must be constant on
`G_res`-orbits. But `S_1 = T disjoint union S`, and `T`, `S` are the only two
orbits on that shell.

Therefore any invariant support is a union of those orbits, hence one of:

- empty support,
- `T` only,
- `S` only,
- `T union S`.

Passing from supports to orthogonal projectors gives exactly the four projectors
listed above.

So the minimal-shell selector problem is already much smaller than it first
looked: the residual ambiguity is not an arbitrary 4-state family but only the
choice among these four invariant projector supports.

## Theorem 2: axis-complete worldtube selectors force `P_A`

Assume the physical boundary/worldtube selector is required to satisfy:

1. **minimality**: it is supported on the minimal nonzero shell `S_1`;
2. **time-completeness**: it contains the unique temporal unit-step state
   `(1,0,0,0)`;
3. **spatial isotropy**: it contains all spatial unit-step states as one
   residual orbit;
4. **residual invariance**: it is `G_res`-invariant.

Then the unique admissible projector is

`P_A = P_t + P_s = sum_(|eta|=1) P_eta`.

### Proof

By Theorem 1, every residual-invariant minimal-shell projector is one of

`0`, `P_t`, `P_s`, `P_A`.

Time-completeness excludes `0` and `P_s`.
Spatial isotropy excludes `0` and `P_t`.

So the only projector satisfying both requirements is

`P_A`.

This proves that once one asks for a selector that really sees the full
time-locked `3+1` one-step worldtube channel, the coarse `hw=1` axis-sector
projector is not a choice any more. It is forced.

## Why the assumptions are the right ones

The two substantive inputs above are not fitted to the number `1/4`.

They encode the current boundary/spacetime meaning of a *worldtube selector*:

- **time-completeness** is forced because the boundary carrier is one-clock and
  therefore cannot represent a physical spacetime worldtube channel while
  omitting the unique temporal one-step direction;
- **spatial isotropy** is forced because the exact `3+1` stack distinguishes
  one time axis from the spatial triplet, but does not distinguish one spatial
  axis from another on the boundary scalar route.

So the assumptions are not an import of the target value. They are the natural
carrier-side reading of the exact time-lock plus `3+1` boundary structure.

## Theorem 3: the remaining obstruction is finer section selection, not sector selection

Although `P_A` is now forced, no individual spatial ray inside `P_s` is
canonically selected by the current boundary/spacetime structure.

More precisely:

- `P_t` is canonical because the temporal direction is fixed by time-lock;
- `P_s` is canonical as the full spatial orbit projector;
- but for any individual spatial ray projector

  `P_x`, `P_y`, `P_z`,

  there exists a permutation `sigma in S_3` such that

  `sigma P_x sigma^(-1) = P_y != P_x`,

  and similarly for the other pairs.

Therefore no nonzero proper subprojector of `P_s` is residual-invariant.

So the exact remaining ambiguity is:

> not which coarse four-axis worldtube sector is physical,
> but whether one needs a finer spatial section inside that already-selected
> sector.

This is the precise analogue of the older distinction between an
orbit-canonical object and a section-canonical one. Here the coarse sector is
canonical, while the fine spatial rays are still only orbit-related.

## Corollary: the `C^16` carrier step is now closed at the coarse sector level

Let

`rho_cell = I_16 / 16`

be the canonical democratic full-cell state.

Because Theorem 2 forces the worldtube selector onto `P_A`, the corresponding
same-carrier coarse scalar is forced to be

`m_axis = Tr(rho_cell P_A) = 4/16 = 1/4`.

So the old carrier objection is narrowed decisively:

- before this note, the axis-sector projector looked like one candidate
  selector support among several;
- after this note, the coarse `hw=1` axis-sector support is forced by the
  current boundary/spacetime carrier assumptions.

What remains open is not sector choice. It is the scalar identification law:

- why the physical boundary pressure is exactly the scalar readout on that
  selected sector.

## What is proved

This lane proves three exact things.

### Theorem A - minimal-shell residual classification

On the minimal nonzero shell of the time-locked four-bit cell, the invariant
selector supports are exactly:

`empty, temporal, spatial, full axis`.

### Theorem B - section-canonical coarse worldtube selector

Time-complete plus spatially isotropic minimal-shell selectors are uniquely
forced onto the coarse `hw=1` four-axis worldtube channel:

`P_A = sum_(|eta|=1) P_eta`.

### Theorem C - sharp residual obstruction

No finer spatial ray inside that sector is canonically selected by the current
stack; the residual spatial symmetry still prevents a canonical rank-1 spatial
section.

## What this does not prove

This note does **not** prove:

- the full Planck boundary lane is closed;
- the current scalar observable-principle law already equals the coarse
  sector mass;
- an individual spatial ray is physically distinguished inside the spatial
  triplet;
- any new numerical value beyond the already-isolated `1/4`.

It only proves the sharper carrier theorem:

> the physical selector can be forced onto the coarse `C^16` `hw=1` axis
> sector from current boundary and spacetime structure.

## Best honest verdict

This lane improves the boundary program in a meaningful way.

The sector-support objection is no longer the real blocker.

The current state is:

- **coarse worldtube sector selection:** closed
- **fine spatial section selection:** still obstructed
- **scalar identification `p_phys = m_axis`:** still open

So the remaining Planck boundary problem is now genuinely a scalar observable
law on a canonically selected sector, not a lingering ambiguity about which
`C^16` worldtube channel should be used at all.
