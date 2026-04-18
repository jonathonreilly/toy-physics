# Dirac Observable Panel Note

**Date:** 2026-04-10  
**Scope:** one Dirac 3+1D harness, many gravity readouts.

The current Dirac work has reached the point where the main question is not
just whether a sign is `TOWARD` or `AWAY`, but whether the sign survives under
different physically plausible readouts.

This panel is the early bottleneck test for that question.

## What The Panel Measures

On the same `frontier_dirac_walk_3plus1d_v3.py` harness, the panel compares:

- centroid shift
- peak shift
- first-arrival layer for mass-side accumulation
- early mass-side accumulation
- directionally projected current
- mass-side shell imbalance

The point is to separate:

- geometric transport
- packet-shape effects
- recurrence / boundary effects
- readout-specific artifacts

from each other before they become a paper-level claim.

## Why It Matters

The branch already shows that a single gravity readout can be misleading.
Different observables can disagree even when they come from the same lattice,
same coupling, and same propagation law.

The panel is designed to answer three questions:

1. Do all readouts agree on sign in the same basin?
2. Do disagreements appear only near recurrence windows?
3. Is the remaining non-monotonicity geometric, or just a readout artifact?

## Interpretation Rules

- If centroid, peak, current, and shell imbalance agree, the sign is probably
  geometric.
- If peak disagrees but the others agree, the readout is too wave-sensitive.
- If the sign flips only at large `N`, boundary recurrence is still active.
- If first-arrival and early accumulation disagree with the final observables,
  the panel is telling us the transport is not settling before the detector
  window.

## Core-Card Connection

This panel is the concrete implementation target for the historical multi-readout
panel row later absorbed into the audited Dirac-core discussion in
[DIRAC_CORE_CARD_NOTE.md](./DIRAC_CORE_CARD_NOTE.md):

- first-arrival
- peak
- current
- centroid
- torus-aware centroid

If the architecture cannot keep these readouts aligned on a clean operating
point, the gravity story is not yet stable enough for promotion.

## Default Run

The default sweep is intentionally modest:

- `n=21`
- `offset=3`
- `layers=10,12,14,16,18,20`
- `mass=0.3`
- `strength=5e-4`

That is enough to expose the readout split without turning the panel into a
new sprawling campaign.
