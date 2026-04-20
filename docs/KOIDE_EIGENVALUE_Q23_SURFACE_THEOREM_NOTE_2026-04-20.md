# Koide Eigenvalue `Q = 2/3` Surface Theorem

**Date:** 2026-04-20  
**Status:** exact support / assumption-escape closeout on the charged-lepton Koide lane  
**Primary runner:** `scripts/frontier_koide_eigenvalue_q23_surface_theorem.py`

## Scope

This note formalizes the strongest `M2`-style escape hatch from the current
selected-line Koide lane:

- keep the retained selected slice `H_sel(m) = H(m, sqrt(6)/3, sqrt(6)/3)`,
- replace the current slot-diagonal readout by the eigenvalues of
  `exp(beta H_sel(m))`,
- impose Koide directly on that eigenvalue triple.

The question is whether this removes the imported selected-line scalar witness
and closes `Q = 2/3` natively.

It does not.

## The theorem

Let `lambda_i(m)` be the eigenvalues of `H_sel(m)` and define

```text
Q_eig(m, beta)
  = [sum_i exp(2 beta lambda_i(m))] / [sum_i exp(beta lambda_i(m))]^2.
```

Then:

1. For any fixed non-scalar three-eigenvalue spectrum,

   ```text
   dQ_eig/dbeta
     = 2 / Z^3 * sum_{i<j} (lambda_j-lambda_i) a_i a_j (a_j-a_i),
   ```

   where `a_i = exp(beta lambda_i)` and `Z = sum_i a_i`.

2. Because `a_i` inherits the eigenvalue ordering, every summand is
   nonnegative and at least one is positive whenever the spectrum is not
   scalar. So `beta -> Q_eig(m,beta)` is strictly increasing.

3. On the charged-lepton selected line, the largest eigenvalue stays simple on
   the physical branch, so for each tested `m` there is one unique
   `beta_q23(m) > 0` with `Q_eig(m, beta_q23(m)) = 2/3`.

So the eigenvalue route produces an exact one-real surface
`beta = beta_q23(m)`. It does **not** isolate a distinguished `m`.

## Numerical branch consequences

On the physical selected line, the runner verifies:

- the top eigenvalue gap stays strictly positive on the branch,
- `Q_eig(m, beta)` is strictly increasing on the tested `beta` window,
- the `Q_eig = 2/3` surface covers a genuine interval
  `beta_q23(m) in [0.545443, 0.673462]`,
- at the current physical selected point
  `m_* = -1.160469470087`, the eigenvalue-surface beta is
  `beta_q23(m_*) = 0.5679143989`,
- this differs from the current slot-route witness
  `beta_* = 0.6335713585` by `0.065657`.

Tested framework-native beta constants do not close the route either. The best
tested hit is `beta = 1/sqrt(3)`, which lands at

```text
m = -1.10394029,
|m - m_*| = 5.6529e-02,
```

still far from the physical point.

## Meaning

This route is not a hidden native derivation of Koide. It is a clean
reparameterized support surface:

- `Q_eig = 2/3` gives one exact beta for each selected-line `m`,
- but an independent beta-law is still required to choose the physical point.

So the `M2` escape hatch is no longer a live closure candidate by itself. The
remaining charged-lepton gap stays where the current branch already located it:
one microscopic selector law on the selected line.
