# Gauge-Vacuum Plaquette First Symmetric Three-Sample Minimal Positive Completion

**Date:** 2026-04-19  
**Status:** exact constructive first-sector upgrade on the named `beta = 6`
three-sample seam; the local Wilson triple still fails the retained positive
cone, but there is one unique smallest adjoint-only positive completion  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_minimal_positive_completion_2026_04_19.py`

## Question

Given the exact local Wilson three-sample triple on `W_A, W_B, W_C`, the exact
radical reconstruction map, and the exact first symmetric retained positive
cone, is there any constructive theorem stronger than “the current local triple
fails positivity”?

## Answer

Yes.

There is one exact constructive upgrade beyond the current no-go:

1. reconstruct the explicit local Wilson sample triple
   `Z^loc = [Z^loc_A, Z^loc_B, Z^loc_C]^T`
   through the exact inverse radical map
   `a^loc = F^(-1) Z^loc`;
2. observe that only the adjoint retained coordinate fails positivity:
   `a^loc_(1,1) < 0`, while `a^loc_(0,0) > 0` and `a^loc_(1,0) > 0`;
3. add exactly the minimal adjoint repair `-a^loc_(1,1)` and leave the other
   retained coordinates unchanged.

This produces the unique **explicit first-sector positive completion candidate**

`a^min = (a^loc_(0,0), a^loc_(1,0), 0)`

and the corresponding exact **completed sample triple**

`Z^min = F a^min`.

So the branch is no longer only a no-go at the first symmetric retained seam.
It now has one explicit constructive first-sector positive completion
candidate.

## Exact data

From the local-Wilson obstruction theorem:

`a^loc_(0,0) =  0.34960695245840506...`,

`a^loc_(1,0) =  0.09339384931083795...`,

`a^loc_(1,1) = -0.03190961277002444...`.

Therefore the unique minimal adjoint repair is

`r_min = -a^loc_(1,1) = 0.03190961277002444...`.

So

`a^min = (0.34960695245840506..., 0.09339384931083795..., 0)`.

Evaluating `Z^min = F a^min` gives the exact completed sample triple

`Z^min(W_A) = 0.1351652795620484...`,

`Z^min(W_B) = 0.3740128800091385...`,

`Z^min(W_C) = 0.5438438585441973...`.

The completion changes only the adjoint sample ray:

- `W_A` stays fixed because the adjoint orbit vanishes exactly there,
- `W_B` increases,
- `W_C` decreases.

## Theorem 1: unique adjoint-only minimal positive completion

Let `C = Cone(r_0, r_1, r_2)` be the exact first symmetric retained positive
cone with coordinates `a = F^(-1) Z`.

For the explicit local Wilson triple `Z^loc`, the first two coordinates of
`a^loc = F^(-1) Z^loc` are already nonnegative and the third is strictly
negative.

Hence among all adjoint-only repairs of the form

`a = (a^loc_(0,0), a^loc_(1,0), a^loc_(1,1) + t)`,

cone membership is equivalent to `t >= -a^loc_(1,1)`.

Therefore the unique minimal adjoint-only positive repair is

`t = -a^loc_(1,1)`,

equivalently `a = a^min`.

## What this closes

- one exact constructive upgrade beyond the local-Wilson positive-cone no-go
- one exact explicit first-sector positive completion candidate
- one exact completed sample triple on the named `W_A, W_B, W_C` seam
- one exact statement that the smallest positive repair is purely adjoint and
  unique along the adjoint-only route

## What this does not close

- the true full `beta = 6` spatial-environment transfer / boundary realization
- the actual framework-point Perron/Jacobi packet
- the full plaquette PF closure
- the global sole-axiom PF selector theorem

## Meaning

This is the first genuinely constructive reopening on the plaquette branch
after the current-bank no-go theorems.

The branch can now say:

- the local Wilson triple is not itself the retained positive answer,
- but it canonically generates one explicit first-sector positive completion
  candidate,
- so the remaining seam is no longer “find any positive first-sector object,”
  but “realize or extend this candidate inside the true `beta = 6`
  spatial-environment packet.”

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_minimal_positive_completion_2026_04_19.py
```
