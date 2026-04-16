# PMNS Direct Closure Attempt Note

**Date:** 2026-04-15  
**Status:** exact direct-underdetermination theorem for the current retained
PMNS bank  
**Script:** `scripts/frontier_pmns_direct_closure_attempt.py`

## Question

Can the current exact bank directly derive or solve the missing objects
themselves?

The missing objects are:

- the branch Hermitian-data package itself
- the breaking-triplet values `(delta, rho, gamma)`
- the restricted Higgs-offset selector on the canonical `(0,1)` seed pair

## Bottom line

No. The current exact bank is not a point-law for these objects. It is an
exact coordinate chart plus a binary sheet cover.

More precisely:

1. the global active Hermitian law is an exact `2 + 2 + 3` chart
2. the breaking triplet is an exact `3`-real source complement inside that
   chart
3. the weak-axis seed patch is an exact two-sheet cover
4. the remaining seed selector is exactly the binary monomial-edge /
   Higgs-offset bit

So the strongest direct theorem is not a positive solve. It is a sharp
underdetermination theorem: the current retained bank fixes the form of the
objects, but not their axiom-side values.

## Exact equations from the current bank

On the canonical active branch,

`H = Y Y^dag`

with

`Y = diag(x_1, x_2, x_3) + diag(y_1, y_2, y_3 e^{i phi}) C`.

The exact global Hermitian decomposition is

`H = H_core + B(delta, rho, gamma)`,

where

`H_core = [[a, b, b], [b, c, d], [b, d, c]]`

and

`B(delta, rho, gamma) = [[0, rho, -rho - i gamma], [rho, delta, 0], [-rho + i gamma, 0, -delta]]`.

The exact coordinate relations are

- `a = H_11`
- `b = (r_12 + r_31 cos phi) / 2`
- `c = (H_22 + H_33) / 2`
- `d = r_23`
- `delta = (H_22 - H_33) / 2`
- `rho = (r_12 - r_31 cos phi) / 2`
- `gamma = r_31 sin phi`

On the compatible weak-axis seed patch `A <= 4 B`,

`diag(A, B, B)` lifts to

`H_seed = mu I + nu (C + C^2)`,

and the exact compatible sheets are

`Y_+ = x_+ I + y_+ C`, `Y_- = y_+ I + x_+ C`.

At the monomial edge `A = B`,

`Y_+ = sqrt(A) I`, `Y_- = sqrt(A) C`.

## Direct underdetermination

The current bank does not derive the branch Hermitian values, because the
global law is a full-rank chart.

The current bank does not derive `(delta, rho, gamma)`, because those are the
three independent coordinates spanning the exact breaking complement.

The current bank does not fix the restricted Higgs-offset selector, because
the seed patch admits two exact exchange sheets with identical Hermitian data
and identical right-Gram data.

So the direct closure attempt stops here:

- branch Hermitian data are not solved
- breaking-triplet values are not solved
- the restricted Higgs-offset selector is not solved

## Strongest exact theorem

**Theorem (Direct PMNS underdetermination on the current retained bank).**
Assume the exact current bank equations listed above.

1. The generic active Hermitian law is an exact real chart of dimension `7`.
2. The breaking triplet is an exact real source space of dimension `3`.
3. The compatible weak-axis seed patch has exactly two canonical exchange
   sheets.
4. On the monomial edge `A = B`, those two sheets become the two one-Higgs
   endpoints `sqrt(A) I` and `sqrt(A) C`.
5. Therefore the current bank does not determine the branch Hermitian-data
   values, the breaking-triplet values, or the restricted Higgs-offset
   selector.

So the current exact bank is a coordinate system, not a closure law.

## What would be needed for positive closure

Any positive direct solve would require one new axiom-side selector law that
collapses the current chart. In the current bank, no such law exists.

## Command

```bash
python3 scripts/frontier_pmns_direct_closure_attempt.py
```
