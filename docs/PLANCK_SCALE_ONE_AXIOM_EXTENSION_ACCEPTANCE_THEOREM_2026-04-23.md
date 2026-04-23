# Planck-Scale One-Axiom Extension Acceptance Theorem

**Date:** 2026-04-23
**Status:** branch-local axiom-extension governance note for the Planck-scale packet
**Audit runner:** `scripts/frontier_planck_one_axiom_extension_acceptance_theorem.py`

## Claim

For the Planck-scale branch, the information / Hilbert / locality surface is no
longer only a support note. It is explicitly promoted as the following
Planck-package axiom extension.

## Axiom Extension P1: local information-state semantics

On the physical `Cl(3)` / `Z^3` lattice package:

1. a primitive physical cell has finite local Hilbert/event semantics;
2. primitive cell events are physical event projectors, not regulator artifacts;
3. local information cannot appear in a source-free cell as hidden preparation
   data;
4. a source-free bare cell carries no preferred primitive event unless such a
   preference is supplied by an explicit source, preparation, boundary condition,
   or dynamical embedding;
5. readout operators may be invariantly defined on the physical event frame, but
   they are not themselves hidden state-preparation data.

This extension introduces no new numerical constant, no tunable parameter, and
no observed lattice spacing. It authorizes the state semantics needed to decide
which local state belongs to the bare primitive cell before a prepared or
dynamical state is supplied.

## Relation to the older single-axiom notes

The older single-axiom notes remain reduction/support notes for the broader
paper package:

- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)
- [SINGLE_AXIOM_HILBERT_NOTE.md](./SINGLE_AXIOM_HILBERT_NOTE.md)

This document is the missing governance move for the Planck packet. It says:

> the Planck-scale branch accepts the one-axiom information / Hilbert / locality
> surface as a load-bearing axiom extension for local source-free state
> semantics.

So the final Planck claim should not be worded as:

> the older minimal ledger alone already derived the local state semantics.

The reviewer-safe wording is:

> on the physical `Cl(3)` / `Z^3` package plus Axiom Extension P1, the
> source-free primitive-cell state law is fixed without introducing a scale.

## What P1 authorizes

P1 authorizes exactly the following moves:

1. treating the time-locked `C^16` primitive cell as a finite local event
   carrier;
2. distinguishing a bare source-free state from a prepared state or a dynamical
   reduced vacuum state;
3. imposing no-preferred-primitive-event on the bare source-free cell;
4. evaluating invariantly defined readout projectors against that state.

## What P1 does not authorize

P1 does not:

1. alter the front-door `Cl(3)` / `Z^3` carrier;
2. change the primitive cell dimension;
3. change the worldtube packet projector;
4. set `a = l_P` by assumption;
5. claim that every interacting local reduced state is tracial.

## Consequence

With P1 accepted, the last state-law step is no longer an ambiguous appeal to
"support semantics." It is a declared package extension:

`source-free bare primitive cell`

`-> no preferred primitive event`

`-> rho_cell = I_16 / 16`

`-> Tr(rho_cell P_A) = 4/16 = 1/4`.

The remaining Planck normalization is then a separate area/action matching
theorem, not part of the state-law axiom extension.
