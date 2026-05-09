# DM Neutrino Triplet Even-Response Theorem

**Date:** 2026-04-15  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_dm_neutrino_triplet_even_response_theorem.py`

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/frontier_dm_neutrino_triplet_even_response_theorem.py` exits 0 with PASS in the current cache; the prior audit verdict citing a nonzero exit was generated against a stale cache and is invalidated by this source-note hash drift. The runner output and pass/fail semantics are otherwise unchanged.

## Question

Once the CP-odd source `gamma` is isolated, what exactly is the even sector it
couples to in the DM CP tensor?

## Bottom line

Exactly two even response channels:

- `E1 = delta + rho`
- `E2 = A + b - c - d`

and the intrinsic tensor factorizes as

- `cp1 = -2 gamma E1 / 3`
- `cp2 =  2 gamma E2 / 3`.

Under character conjugation `phi -> -phi`:

- `gamma` is odd
- `E1` and `E2` are even
- `cp1` and `cp2` flip sign

So the last-mile denominator law is no longer a vague seven-variable problem.
It is:

- one odd source
- two even response channels

## What this closes

This closes the **form** of the response law.

The branch no longer has to say only “derive the triplet somehow.” It can now
say exactly:

- source leg: `gamma`
- response legs: `E1`, `E2`
- leptogenesis tensor: odd times even

## What this does not close

This note does **not** derive the actual values of `gamma`, `E1`, or `E2`.

It only fixes the exact response structure they must satisfy.

## Command

```bash
python3 scripts/frontier_dm_neutrino_triplet_even_response_theorem.py
```
