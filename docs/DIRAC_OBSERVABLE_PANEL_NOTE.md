# Dirac Observable Panel Note

**Status:** bounded - bounded or caveated result note
**Claim type:** bounded_theorem
**Date:** 2026-04-10  
**Scope:** one Dirac 3+1D harness, many gravity readouts.

**Audit-conditional perimeter (2026-05-03):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
bounded_theorem`. The audit chain-closure explanation is exact: "The
dependency now closes for retained bounded core results, including
multi-observable gravity under primary readouts, but the supplied
runner output does not report the observable-panel-specific readouts
listed in this note. The missing step is a panel run or retained
summary tying centroid, peak, first-arrival, early accumulation,
current, and shell imbalance to the stated default sweep and sign-
alignment questions." This rigorization edit only sharpens the
boundary of the conditional perimeter; nothing here promotes audit
status. The supported content of this note is the bounded
methodological framing: the panel of readouts, the interpretation
rules, and the default sweep are all auditable framings, not
numerical claims. A future panel-runner deposit producing the six
listed readouts on the default `n=21, layers=10..20, mass=0.3,
strength=5e-4` sweep would close the conditional perimeter; this note
remains a methodological card until that runner output is registered.

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
