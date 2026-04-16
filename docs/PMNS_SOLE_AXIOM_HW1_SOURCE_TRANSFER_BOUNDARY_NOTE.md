# PMNS Sole-Axiom `hw=1` Source/Transfer Boundary

**Date:** 2026-04-16  
**Script:** `scripts/frontier_pmns_sole_axiom_hw1_source_transfer_boundary.py`

## Question

If we derive the canonical `hw=1` source/transfer pack itself from the sole
axiom `Cl(3)` on `Z^3`, do native source insertion and graph-first forward
transport generate a nontrivial retained PMNS pack?

## Answer

No.

The strongest canonical sole-axiom `hw=1` source/transfer construction stays
trivial:

- the sole-axiom active resolvent is the identity on the retained triplet
- the sole-axiom passive resolvent is only a scalar multiple of the identity
- source insertion through the native site projectors therefore gives only the
  basis columns `e1,e2,e3`, up to the passive scalar weight
- graph-first forward transport fixes the ordered frame `E12,E23,E31`
- but that transport contributes only support/frame information, not nontrivial
  PMNS value data

So even this source-inserted transfer attack does not evade the free-profile
boundary.

## Exact content

On the retained `hw=1` triplet:

1. the native source projectors are exactly `E11,E22,E33`
2. forward cycle transport sends them to the graph-first ordered frame
   `E12,E23,E31`
3. the derived active source columns are exactly the basis columns
4. the derived passive source columns are exactly a scalar multiple of the
   basis columns
5. the derived active/passive blocks are therefore exactly `(I3, I3)`

The retained PMNS closure stack rejects that canonical pack, because it does
not realize a one-sided minimal PMNS class.

## Consequence

This strengthens the sole-axiom retained PMNS boundary:

- not only do the sole-axiom lower-level response profiles stay trivial
- even the strongest canonical source-inserted / graph-first-transferred
  `hw=1` pack stays trivial

So the remaining blocker is not “we forgot to insert sources” or “we forgot to
use the graph-first transfer frame.” Those routes are now closed on the current
exact bank as well.

## Verification

```bash
python3 scripts/frontier_pmns_sole_axiom_hw1_source_transfer_boundary.py
```
