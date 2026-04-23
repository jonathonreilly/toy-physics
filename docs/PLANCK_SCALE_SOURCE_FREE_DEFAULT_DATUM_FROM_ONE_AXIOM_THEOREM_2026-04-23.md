# Planck-Scale Source-Free Default Datum from One Axiom Theorem

**Date:** 2026-04-23  
**Status:** branch-local theorem on the explicit Axiom Extension P1 information / Hilbert / locality surface
**Audit runner:** `scripts/frontier_planck_source_free_default_datum_from_one_axiom_theorem.py`

## Question

Can the last semantic move on the direct Planck lane be derived more natively
from first principles:

> a source-free primitive-cell state is the default datum of the bare physical
> cell, not an arbitrary hidden preparation?

The goal here is not to prove that every local reduced vacuum state in the
interacting theory is tracial. The target is narrower:

> on the accepted one-axiom information / Hilbert / locality surface, what is
> the state attached to the **bare primitive physical cell itself** when no
> extra local preparation or source datum has been supplied?

## Bottom line

Yes, on the explicit Axiom Extension P1 surface.

On the accepted one-axiom surface, the primitive physical substrate is a real
local object and information is conserved and local. A nontrivial local state
on that object carries retrievable local information: unequal event weights,
proper spectral projectors, or other local biases. If no extra local source or
preparation datum is supplied, that information cannot be attributed to hidden
preparation without contradicting the source-free premise.

So on that surface:

> a source-free primitive-cell state is the default datum of the bare physical
> cell object, not an arbitrary unknown prepared state.

For the exact time-locked primitive event frame

`E = {P_eta : eta in {0,1}^4}`,

default-datum status plus no-preferred-primitive-event forces

`rho_cell = I_16 / 16`.

Then the already-closed kinematic counting law

`c_cell(rho) = Tr(rho P_A)`

gives

`c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4`,

so the direct route yields

`a^2 = l_P^2`,

hence

`a = l_P`.

## Scope and exact claim

This note works on **Axiom Extension P1**, the explicitly promoted one-axiom
information / Hilbert / locality surface for the Planck packet, not on the
smaller front-door minimal input ledger by itself. The older reduction notes are
supporting background; the governance promotion is recorded in:

- [PLANCK_SCALE_ONE_AXIOM_EXTENSION_ACCEPTANCE_THEOREM_2026-04-23.md](./PLANCK_SCALE_ONE_AXIOM_EXTENSION_ACCEPTANCE_THEOREM_2026-04-23.md)
- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)
- [SINGLE_AXIOM_HILBERT_NOTE.md](./SINGLE_AXIOM_HILBERT_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)

The theorem here does **not** claim:

- every local reduced vacuum state of an interacting global theory is tracial;
- every physical state on the cell is default;
- Hamiltonian-selected or entangled reduced states are impossible.

It claims only:

- the **Planck primitive-cell coefficient** is a kinematic primitive-cell datum,
  not a dynamical vacuum observable;
- therefore the relevant state on the cell is the **source-free default datum**
  of the bare cell;
- on the exact primitive cell, that default datum is tracial.

## Inputs

- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)
- [SINGLE_AXIOM_HILBERT_NOTE.md](./SINGLE_AXIOM_HILBERT_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- [PLANCK_SCALE_TIMELOCKED_FACTOR_CELL_OBJECT_DERIVATION_2026-04-23.md](./PLANCK_SCALE_TIMELOCKED_FACTOR_CELL_OBJECT_DERIVATION_2026-04-23.md)
- [PLANCK_SCALE_KINEMATIC_CELL_COEFFICIENT_THEOREM_CANDIDATE_2026-04-23.md](./PLANCK_SCALE_KINEMATIC_CELL_COEFFICIENT_THEOREM_CANDIDATE_2026-04-23.md)
- [PLANCK_SCALE_EVENT_FRAME_NO_INFORMATION_STATE_THEOREM_2026-04-23.md](./PLANCK_SCALE_EVENT_FRAME_NO_INFORMATION_STATE_THEOREM_2026-04-23.md)

## Three distinct notions

Hostile review gets cleaner once these are separated.

### 1. Prepared local state

A prepared local state carries extra local datum. The physical object is really

`(primitive cell, preparation datum)`.

There is no reason for such a state to be tracial.

### 2. Dynamical local reduced state

A local reduced state of a globally prepared or interacting vacuum can also be
nontracial. The physical object there is really

`(global state, primitive cell embedding)`.

Again, there is no reason for such a state to be tracial.

### 3. Source-free primitive-cell default datum

This is the target here. It means:

> the local state attached to the bare primitive cell itself when no extra
> local preparation/source datum is specified.

That is a different object from 1 and 2. The theorem concerns only 3.

## Theorem 1: source-free primitive-cell state is not arbitrary hidden preparation

Assume the accepted one-axiom surface:

1. there are distinguishable local things;
2. information flows between them without being created or destroyed;
3. the local substrate is physical, not a disposable regulator;
4. the direct Planck coefficient is a kinematic primitive-cell counting datum
   on that substrate.

Let `X` be the bare primitive cell object. Call `rho_sf(X)` the
**source-free primitive-cell state** if no extra local preparation/source datum
has been supplied to `X`.

Then `rho_sf(X)` cannot be an arbitrary hidden prepared state.

### Reason

An arbitrary hidden prepared state would contain extra local information not
fixed by `X` itself: unequal primitive event weights, proper spectral
projectors, or another local bias retrievable by the Born/event semantics on
the finite Hilbert carrier.

But on the one-axiom information reading, local information cannot appear
without a source or incoming flow. By locality, such information must come
from:

- the object `X` itself,
- an explicit preparation datum,
- or incoming dynamical coupling to the wider system.

For a source-free primitive-cell state, the second and third are absent by
definition. So any remaining local information must be part of the bare object
itself.

If the local state is not fixed by the bare object, then it is hidden
preparation data in disguise.

Therefore:

> on the accepted one-axiom surface, a source-free primitive-cell state is the
> default datum of the bare physical cell object, not an arbitrary hidden
> preparation.

## Theorem 2: default datum on the exact primitive event frame is tracial

On the direct Planck lane, the exact primitive cell has physical event frame

`E = {P_eta : eta in {0,1}^4}`.

The older argument appealed to arbitrary factor-local `U(2)^4` presentation
changes. This hardened version does not. The physical event frame is retained.

Define

`N_evt = sum_eta |eta| P_eta`.

The packet is invariantly defined as

`P_A = 1_{N_evt = 1}`.

So `P_A` is a physical readout projector on the event frame, not an arbitrary
basis choice.

Now apply Axiom Extension P1: a source-free bare primitive cell has no preferred
primitive event unless such a preference is supplied by a source, preparation,
boundary condition, or dynamical embedding. For the bare source-free cell no such
datum is supplied.

Therefore all primitive event weights are equal:

`rho_sf = sum_eta p P_eta`.

Normalization gives

`16 p = 1`,

so

`p = 1/16`.

Hence

`rho_sf = I_16 / 16`.

Packet-preserving symmetry alone would not be enough: it would allow
`rho = alpha P_A + beta (I - P_A)`. The state law is instead no preferred
primitive event for the bare source-free cell, while `P_A` remains the fixed
worldtube readout evaluated afterward.

## Corollary 1: quarter and Planck

From the already-closed kinematic counting law

`c_cell(rho) = Tr(rho P_A)`,

one gets

`c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4`.

The area/action normalization theorem then gives

`a^2 = l_P^2`,

hence

`a = l_P`.

## What this does and does not settle

### What it does settle

On the accepted one-axiom information / Hilbert / locality surface, if the
Planck coefficient is a kinematic primitive-cell counting datum, then the
relevant source-free local state is the default datum of the bare primitive
cell and that datum is tracial.

### What it does not settle

If a reviewer insists that the relevant quantity is instead a **dynamical local
reduced vacuum state observable**, this theorem does not apply. But that is no
longer a disagreement about the state law itself. It is a disagreement about
the observable class of the Planck coefficient.

That is exactly why
[PLANCK_SCALE_KINEMATIC_CELL_COEFFICIENT_THEOREM_CANDIDATE_2026-04-23.md](./PLANCK_SCALE_KINEMATIC_CELL_COEFFICIENT_THEOREM_CANDIDATE_2026-04-23.md)
matters.

## Honest status

This is the hardened one-axiom route on the branch.

My honest read is:

- on Axiom Extension P1, this is a theorem-level state-law close;
- on the smaller front-door minimal input ledger alone, it remains an explicit
  axiom-extension move rather than a derivation.

So the exact remaining hostile-review escape hatch is now explicit:

> deny Axiom Extension P1's no-preferred-primitive-event state law, or
> reclassify the elementary Planck coefficient as a dynamical reduced-state
> observable rather than kinematic primitive-cell counting data.

If those denials are rejected, the one-axiom default-datum route closes cleanly.
