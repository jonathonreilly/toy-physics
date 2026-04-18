# PMNS Graph-First Fixed-Slice Minimal Production Certificate

**Date:** 2026-04-18  
**Status:** exact certificate packaging of the PMNS-native production frontier;
the whole remaining native lane is one minimal fixed-slice two-holonomy
production certificate, and the current bank still does not realize it  
**Script:** `scripts/frontier_pmns_graph_first_fixed_slice_minimal_production_certificate_2026_04_18.py`

## Question

After the fixed-slice two-holonomy collapse theorem and the production-boundary
reduction, can the PMNS-native frontier be stated as one minimal reviewer-safe
certificate rather than a looser “source law”?

## Answer

Yes.

The whole remaining PMNS-native sole-axiom frontier is exactly one minimal
production certificate:

1. fix one slice `w = w0`,
2. produce any two independent native holonomies
   `(h_(phi1), h_(phi2))`,
3. require that the pair is nontrivial:
   `(h_(phi1), h_(phi2)) != (w0, w0)`.

That certificate is equivalent to production of nonzero

`J_chi = chi`.

So the PMNS-native lane is no longer a route-search problem. It is one minimal
fixed-slice two-holonomy production certificate.

The current bank still does **not** realize that certificate.

## Setup

From
[PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_COLLAPSE_NOTE_2026-04-17.md](./PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_COLLAPSE_NOTE_2026-04-17.md):

- once `w` is fixed, any two independent native holonomies reconstruct `chi`
  exactly on the readout side.

From
[PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_PRODUCTION_BOUNDARY_NOTE_2026-04-17.md](./PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_PRODUCTION_BOUNDARY_NOTE_2026-04-17.md):

- the remaining production blocker is exactly one nontrivial fixed-slice
  holonomy-pair source law,
- equivalently production of nonzero `chi = J_chi`.

## Theorem 1: exact minimal production-certificate form of the PMNS-native lane

The whole remaining PMNS-native sole-axiom lane is exactly one minimal
fixed-slice two-holonomy production certificate.

Indeed, the collapse theorem shows that on a fixed slice any independent
holonomy pair reconstructs `chi` exactly, while the production-boundary theorem
shows that the only remaining content is to produce a **nontrivial** such pair.

Therefore the remaining PMNS-native lane is exactly:

- one fixed slice,
- one independent two-holonomy pair,
- one nontriviality condition.

## Corollary 1: the current bank still does not realize the certificate

The current retained sole-axiom PMNS-native bank still forces `J_chi = 0`.

Therefore it still does **not** produce a nontrivial fixed-slice holonomy
pair, and so does not realize the minimal production certificate.

## What this closes

- one minimal certificate packaging of the PMNS-native production frontier
- exact clarification that the remaining PMNS-native science is no longer
  readout but one two-holonomy production certificate

## What this does not close

- a sole-axiom nonzero-current production theorem
- a Wilson-to-PMNS descendant theorem
- the global sole-axiom PF selector theorem

## Why this matters

This puts the PMNS-native front in the same hard-review-safe style as the
Wilson and plaquette fronts.

The branch can now say:

- Wilson positive reopening is one local `2-edge + 3` certificate,
- PMNS-native production is one minimal fixed-slice two-holonomy certificate,
- plaquette non-Wilson closure is one minimal `moment + K` certificate.

## Command

```bash
python3 scripts/frontier_pmns_graph_first_fixed_slice_minimal_production_certificate_2026_04_18.py
```
