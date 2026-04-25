# Koide Q Gaussian/equipartition covariance no-go

## Theorem attempt

Maybe the missing `K_TL = 0` source law is forced by a retained Gaussian
maximum-entropy, covariance-whitening, or equipartition principle on the
first-live `C_3` carrier.  If so, the covariance law would derive equal total
singlet and doublet block powers and the usual chain would close:

```text
K_TL = 0 -> Y = I_2 -> E_+ = E_perp -> kappa = 2 -> Q = 2/3.
```

## Brainstorm/ranking

1. Microdegree Gaussian equipartition: strongest retained authority, because it
   uses the ordinary covariance entropy of the three real modes.
2. Trace/determinant normalized covariance: fastest exact check; tests whether
   normalization alone removes the anisotropy.
3. Equal block-temperature equipartition: positive-looking, but likely imports
   the equal-block law as a measure choice.
4. Covariance whitening: strong if a retained metric fixes the whitening trace,
   but weak against metric-choice objections.
5. Weighted block entropy: useful hostile-review parameterization of hidden
   assumptions.

The runner implements the first, second, and fifth variants exactly.

## Exact reduction

On the retained `C_3` carrier, every positive invariant Gaussian covariance has
the form

```text
Sigma = x P_+ + y P_perp,
```

with

```text
E_+ = tr(P_+ Sigma) = x,
E_perp = tr(P_perp Sigma) = 2y,
R = E_perp / E_+ = 2y/x.
```

The source-neutral Koide leaf is therefore the special anisotropy

```text
R = 1 <=> x = 2y.
```

## Result

Trace normalization gives `x + 2y = n`, leaving `y` free.  Determinant
normalization gives `det(Sigma) = x y^2`, again leaving a one-parameter
positive family.  Standard Gaussian entropy is

```text
S = log det(Sigma) = log x + 2 log y + constant.
```

Under fixed trace budget, its stationary point is

```text
x = y = n/3,
R = 2,
Q = 1,
K_TL = 3/8.
```

Thus ordinary microdegree equipartition is not Koide.  The equal-block point is
obtained only by replacing the microdegree weight with a block-label weight.
For weighted block entropy

```text
S_alpha = log(E_+) + alpha log(E_perp),
```

the extremum has

```text
E_perp / E_+ = alpha.
```

The Koide leaf is `alpha = 1`; retained real microdimension counting gives
`alpha = 2`.

## Residual

```text
RESIDUAL_SCALAR = block_entropy_weight_alpha_minus_1_equiv_K_TL
RESIDUAL_WEIGHT = block_entropy_weight_alpha_minus_1_equiv_K_TL
```

## Hostile review

- **Circularity:** claiming equal block-temperature is exactly choosing
  `alpha = 1`; that is the missing block-source law in entropy language.
- **Target import:** no PDG masses, observational pins, `Q = 2/3`, or
  `K_TL = 0` are used in the audit.
- **Retained-authority gap:** the standard retained Gaussian entropy counts
  microdegrees and selects rank weights, not equal block totals.
- **Overbroad claim avoided:** this no-go covers covariance/equipartition laws
  on the finite first-live `C_3` carrier; it does not exclude a new retained
  physical law that changes the entropy measure.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_gaussian_equipartition_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_GAUSSIAN_EQUIPARTITION_NO_GO=TRUE
Q_GAUSSIAN_EQUIPARTITION_CLOSES_Q=FALSE
RESIDUAL_SCALAR=block_entropy_weight_alpha_minus_1_equiv_K_TL
RESIDUAL_WEIGHT=block_entropy_weight_alpha_minus_1_equiv_K_TL
```
