# PMNS Scalar Bridge Nonrealization

**Date:** 2026-04-15
**Status:** exact current-bank theorem on nonrealization of the PMNS selector
inside the present additive scalar observable grammar
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_pmns_scalar_bridge_nonrealization.py`

## Question

After the support-side bank fails to force the residual one-sided PMNS
orientation bit, could the current scalar observable principle still generate
the missing sector-sensitive inter-sector bridge?

## Bottom line

No.

The retained scalar observable generator is

`W[J] = log|det(D+J)| - log|det D|`.

For independent lepton blocks

`D = D_nu ⊕ D_e`,

this generator is exactly additive and its mixed local-source curvature
vanishes across the blocks.

So the present scalar observable grammar is block-local on the lepton surface.
It does not generate a mixed scalar bridge selecting whether the active
two-Higgs lane sits on `Y_nu` or on `Y_e`.

## Atlas and axiom inputs

This theorem reuses:

- `Observable principle`
- `PMNS sector-exchange nonforcing`

## Why this matters

The support-side nonforcing theorem closed one loophole:

- the current branch/support classifier bank cannot force the orientation bit

This note closes the next obvious loophole:

- the current additive scalar observable bank cannot force it either

So the remaining selector science is now outside both of those exact banks.

## Theorem-level statement

**Theorem (Current-bank nonrealization of a PMNS scalar selector bridge).**
Assume the retained additive scalar observable generator

`W[J] = log|det(D+J)| - log|det D|`

and the exact PMNS sector-exchange nonforcing theorem. Then on independent
lepton blocks:

1. `W` is exactly additive on `D_nu ⊕ D_e`
2. mixed local-source curvature vanishes across the two blocks
3. the current scalar observable grammar therefore remains block-local on the
   lepton surface

Therefore the present scalar observable bank does not realize the missing PMNS
sector-selector bridge.

## What this closes

This closes the last obvious scalar-observable loophole in the current exact
bank.

It is now exact that the remaining PMNS selector science is not:

- another support theorem
- another atlas selector audit
- another scalar source-response theorem inside the present additive
  `log|det|` grammar

It must instead come from something genuinely new:

- a sector-sensitive inter-sector bridge
- a non-additive or non-scalar observable grammar
- or a universality theorem killing the one-sided class

## What this does not close

This note does **not** prove:

- that no future scalar observable could ever work
- that universality is true
- that universality failure is impossible
- any positive coefficient derivation on a surviving branch

It is a theorem only about the **current** retained scalar observable bank.

## Command

```bash
python3 scripts/frontier_pmns_scalar_bridge_nonrealization.py
```
