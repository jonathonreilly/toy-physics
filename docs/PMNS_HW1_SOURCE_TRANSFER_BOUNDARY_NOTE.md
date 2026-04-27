# PMNS HW1 Source-Transfer Boundary

**Date:** 2026-04-16
**Status:** theorem-grade boundary for the proposed_retained `hw=1` source/transfer attack on the PMNS blocker
**Script:** `scripts/frontier_pmns_hw1_source_transfer_boundary.py`

## Question

Can a genuinely axiom-first `hw=1` source/transfer law on the retained lepton
triplet do better than the current sole-axiom free-profile boundary?

## Bottom line

Yes, at the retained interface level.

The `hw=1` source-transfer package closes the active/passive retained lane
cleanly:

1. the active transfer shadow fixes the weak-axis seed pair
   `(xbar, ybar)`
2. the direct corner transport asymmetry fixes the branch bit
3. the active source-response columns fix the active kernel exactly
4. the passive source-response columns fix `q` and `a_i`
5. the combined source/transfer pack reconstructs the retained PMNS pair and
   the downstream Hermitian / PMNS data exactly

So the retained PMNS lane is no longer blocked by an intrinsic ambiguity in
the `hw=1` source/transfer observables themselves.

## Exact boundary

The current exact bank still does **not** derive that source/transfer pack
from `Cl(3)` on `Z^3` alone.

In particular:

- transfer summaries alone are blind to the full 5-real active corner source
- two distinct off-seed active microscopic blocks can share the same transfer
  shadow while differing in the corner-breaking source
- the source-response columns are exactly what repair that blindness and fix
  the active kernel

So the remaining sole-axiom blocker is now sharply isolated:

- not a hidden PMNS-side value ambiguity
- not a branch-selection ambiguity on the retained pack
- not a passive monomial ambiguity

It is the derivation of the actual lower-level source/transfer observables
from `Cl(3)` on `Z^3` alone.

## Consequence

This boundary is the right one for review:

- if the `hw=1` source/transfer pack is supplied, the retained PMNS lane
  closes exactly
- if only the sole axiom is supplied, the current exact bank still does not
  select the nontrivial source/transfer pack

That is the sharpest honest state of the retained source/transfer attack.

## Verification

```bash
python3 scripts/frontier_pmns_hw1_source_transfer_boundary.py
```

