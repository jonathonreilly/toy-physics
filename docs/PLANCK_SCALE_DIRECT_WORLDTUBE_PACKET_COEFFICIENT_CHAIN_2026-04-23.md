# Planck-Scale Direct Worldtube-Packet Coefficient Chain

**Date:** 2026-04-23  
**Status:** science-only canonical direct-chain reformulation of the surviving Planck route  
**Audit runner:** `scripts/frontier_planck_direct_worldtube_packet_coefficient_chain.py`

## Question

Can the surviving Planck lane be stated directly, without leaning on the older
Schur / transfer / "boundary pressure" language?

## Bottom line

Yes.

The strongest surviving route is no longer best described as a scalar boundary
free-energy problem. It is best described as a direct coefficient chain on the
minimal time-locked cell:

1. the exact local primitive is the time-locked four-bit cell `C^16`;
2. the exact minimal one-step worldtube packet on that cell is the four-atom
   projector

   `P_A = sum_(|eta|=1) P_eta`;

3. if the source-free primitive-cell state is the default bare-cell datum of
   the physical local cell, then the exact full-cell state is the democratic
   state

   `rho_cell = I_16 / 16`;

4. the exact worldtube-packet coefficient is therefore

   `c_wt := Tr(rho_cell P_A) = 4 / 16 = 1/4`;

5. the elementary codimension-1 gravitational boundary law is now closed on
   the branch as exact packet counting, so the elementary boundary cell
   coefficient is

   `c_cell = c_wt = 1/4`;

6. with the geometric action/area reduction already isolated elsewhere on the
   branch, `c_cell = 1/4` is exactly the coefficient needed for

   `a^2 = l_P^2`,

   hence

   `a = l_P`.

So the current direct route is not:

> "find the right boundary pressure."

It is:

> derive the source-free primitive-cell default datum on the physical local
> cell, because the counting side is already closed.

That is now the whole remaining bridge.

## Why the old "boundary pressure" term is no longer central

The old phrase came from an earlier scalar route, where the boundary was
packaged through Schur reduction, Gaussian partition data, and additive
free-energy or growth-rate scalars.

That route remains useful as a negative control:

- it isolates the exact scalar Schur observable

  `p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`;

- and it proves that this scalar does **not** land quarter.

But the strongest surviving route no longer depends on that scalar grammar.
Its load-bearing object is the full one-step worldtube packet `P_A`, not the
Schur scalar.

So on the current branch:

- **historical scalar-route language**
  "boundary pressure" = Schur/free-energy/growth-rate exploratory grammar;
- **current direct-route language**
  `c_wt = Tr(rho_cell P_A)` = worldtube-packet coefficient / boundary-cell
  coefficient candidate.

For the direct route, "boundary pressure" is now mostly historical wording and
is no longer the cleanest name for the object under study.

## Minimal direct science chain

This is the direct chain stripped of the older scalar packaging.

### Step 1: exact local cell after time-lock

After time-lock, the minimal local carrier is the exact four-bit cell

`eta = (eta_t, eta_x, eta_y, eta_z) in {0,1}^4`.

So the primitive finite carrier has dimension

`2^4 = 16`.

Call the atomic projectors

`P_eta = |eta><eta|`.

### Step 2: exact minimal one-step worldtube packet

The section-canonical minimal one-step worldtube packet is the Hamming-weight-1
packet

`A = {eta : |eta| = 1}`,

with projector

`P_A = sum_(eta in A) P_eta`.

This packet has exactly four atoms:

- one temporal one-hot state,
- three spatial one-hot states.

So

`rank(P_A) = 4`.

### Step 3: the packet is physical as a full packet, not just a quotient

The current branch-local packet analysis already fixes:

- the visible Schur quotient block `P_q`,
- the hidden exact `E`-doublet complement `P_E`,
- and the full packet decomposition

  `P_A = P_q + P_E`.

The missing factor `2` is therefore not a normalization accident but exact
carrier multiplicity.

More importantly, the current physical-lattice surface already treats proper
quotienting of retained exact observable sectors as inadmissible. So the direct
physical object is the full packet `P_A`, not merely the quotient `P_q`.

### Step 4: source-free default datum on the physical primitive cell

Once the lattice is taken as physical, the exact time-locked `C^16` cell is a
real primitive local object, not a disposable regulator block.

So the state question is no longer:

> "what arbitrary state might happen to live on this Hilbert space?"

It is:

> "what is the default state datum of this physical primitive cell when no
> extra local preparation/source datum is supplied?"

The strongest current native candidate is precisely:

`rho_cell = I_16 / 16`.

This is supported on the branch by:

- source-free `Cl(3)` factor-state traciality;
- same-object / different-presentation semantics on the primitive cell;
- no-created-local-information / zero local-information-defect semantics;
- and the cleaner default-datum reading of source-free local state.

If that source-free default-datum law is accepted, every primitive cell atom
carries equal source-free weight `1/16`.

### Step 5: exact worldtube-packet coefficient

Define the direct worldtube-packet coefficient by

`c_wt := Tr(rho_cell P_A)`.

Because `P_A` is the sum of exactly four orthogonal atomic projectors and
`rho_cell = I_16 / 16`,

`c_wt = 4 * (1/16) = 1/4`.

This is the exact quarter now isolated on the branch.

### Step 6: boundary counting is closed

The direct worldtube-to-boundary counting theorem already closes the physical
counting bridge:

`c_cell(rho) = Tr(rho P_A)`.

So once the source-free default datum is fixed, the elementary boundary cell
coefficient is automatically exactly `1/4`.

### Step 7: Planck identification

Once the elementary boundary cell coefficient is `1/4`, the geometric
boundary/action reduction gives the standard Planck area coefficient, hence

`a^2 = l_P^2`,

and therefore

`a = l_P`.

## Direct route versus scalar route

These are now two distinct routes, and they should not be blurred together.

### Scalar route

Object:

`p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`.

Interpretation:

- scalar boundary free-energy density;
- lives on the reduced Schur carrier;
- mathematically exact;
- lands the wrong coefficient for Planck.

### Direct route

Object:

`c_wt = Tr(rho_cell P_A)`.

Interpretation:

- occupancy / measure of the exact minimal worldtube packet;
- lives on the full time-locked `C^16` cell;
- uses the full retained packet, not the quotient;
- lands the exact quarter coefficient.

So the live scientific choice is not between two ways of writing the same
quantity. It is between two different observable grammars:

- scalar free-energy on a reduced carrier;
- packet measure on the full primitive cell.

## Exact remaining open statement

The counting side is no longer open.

The direct worldtube-to-boundary theorem already closes

`c_cell(rho) = Tr(rho P_A)`.

The classification fight is also now sharply reduced:

- the universal elementary coefficient is attached to the primitive physical
  cell,
- the exact count operator is already fixed kinematically,
- a reduced-vacuum expectation belongs to the larger datum class
  `(H_cell, iota, Omega)`,
- so a fundamental reclassification as reduced-vacuum observable changes the
  object rather than explaining the same coefficient.

So the direct route is now reduced to one remaining package-boundary question:

> is the source-free primitive-cell state on the physical `C^16` cell the
> default datum of that bare cell?

What is already closed:

- the local carrier size `16`;
- the packet size `4`;
- the exact packet `P_A`;
- the physical need to keep the full packet rather than its quotient;
- the exact cell-counting law `c_cell(rho) = Tr(rho P_A)`;
- the object-class reduction ruling out a fundamental generic
  reduced-vacuum reclassification;
- the exact source-free direct state `rho_cell = I_16 / 16` on the strongest
  one-axiom default-datum route;
- the exact coefficient `c_wt = 1/4`.

What is not yet closed:

- whether the package accepts that source-free primitive-cell default-datum
  principle as native enough for this lane.

## Safe wording

**Can claim**

- the surviving Planck route can be stated directly without the older
  "boundary pressure" packaging;
- the canonical direct quantity is the worldtube-packet coefficient
  `c_wt = Tr(rho_cell P_A)`;
- the cell-counting bridge is already closed:
  `c_cell(rho) = Tr(rho P_A)`;
- on the current one-axiom default-datum route this coefficient is exactly
  `1/4`;
- the reduced-vacuum reclassification is no longer the live scientific issue;
  the remaining issue is the source-free default-datum principle.

**Cannot claim**

- that the older scalar Schur observable already implies `c_cell = c_wt`;
- that front-door minimal-stack retained Planck closure is finished without
  accepting the source-free default-datum move.

## Inputs

This direct reformulation uses only:

- [PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md](./PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_SECTION_CANONICAL_WORLDTUBE_SELECTOR_LANE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_MULTIPLICITY_LIFT_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_NON_SCHUR_AXIS_OCCUPATION_LAW_LANE_2026-04-23.md](./PLANCK_SCALE_NON_SCHUR_AXIS_OCCUPATION_LAW_LANE_2026-04-23.md)
- [PLANCK_SCALE_PROJECTOR_VALUED_OBSERVABLE_PRINCIPLE_LANE_2026-04-23.md](./PLANCK_SCALE_PROJECTOR_VALUED_OBSERVABLE_PRINCIPLE_LANE_2026-04-23.md)
- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_PRIMITIVE_COEFFICIENT_OBJECT_CLASS_THEOREM_2026-04-23.md](./PLANCK_SCALE_PRIMITIVE_COEFFICIENT_OBJECT_CLASS_THEOREM_2026-04-23.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)

The older scalar boundary-observable notes remain historically useful as
negative controls, but they are no longer the cleanest canonical entrypoint for
the surviving direct route.

## Command

```bash
python3 scripts/frontier_planck_direct_worldtube_packet_coefficient_chain.py
```
