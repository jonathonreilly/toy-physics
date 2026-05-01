# DM Leptogenesis PMNS Minimal A13 Sheet-Selector Theorem

**Date:** 2026-04-16  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_dm_leptogenesis_pmns_minimal_a13_sheet_selector_theorem.py`

## Question

After quotienting by the current exact even PMNS data, what is the smallest
remaining selector object that distinguishes the constructive projected-source
witness from its CP-flipped partner on the current branch?

## Bottom line

It is exactly the sign of the single odd projected-source slot `A13`,
equivalently the sign of `gamma = A13 / 2`.

The current exact even data already agree on the constructive witness and its
CP-flipped partner:

- `E1`
- `E2`
- flavored transport
- the current exact even selector objectives

What still differs is only the sign of the odd source slot:

- `A13 > 0` on the constructive witness
- `A13 < 0` on its CP-flipped partner

So the residual PMNS selector object is one-bit:

- `sign(A13)`

## Exact microscopic meaning

This is already a legitimate microscopic target.

The charged source law factors exactly through

- `dW_e^H = Schur_{E_e}(D_-)`

and on that projected Hermitian source pack:

- `gamma = A13 / 2`

So the minimal theorem-grade sheet selector is equivalently:

- a microscopic law forcing `A13 > 0` on `dW_e^H`

## Consequence

The PMNS comparator no longer needs to ask for a vague full-`D` selector.

The smallest exact unresolved selector object is now:

- the sign of `A13` on the projected source pack

with the even data already closed.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_minimal_a13_sheet_selector_theorem.py
```
