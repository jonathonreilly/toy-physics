# Koide Q Wess-Zumino / Berezinian asymmetric-measure no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_wess_zumino_asymmetric_measure_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Try to turn the strongest exact Q support scalar

```text
T(T+1) - Y^2 = 3/4 - 1/4 = 1/2
```

into the charged-lepton cyclic amplitude law

```text
rho = |b|^2/a^2 = T(T+1) - Y^2,
```

using a Wess-Zumino, anomaly-inflow, or Berezinian measure principle.  If such
a principle supplied the `SU(2)_L - U(1)_Y` sign and unit normalization on the
normalized second-order carrier, then `rho=1/2`, `K_TL=0`, and `Q=2/3` would
follow algebraically.

## Executable result

The retained source class tested by the runner does not force that map.

For a general generator-weighted local measure,

```text
rho(alpha,beta) = alpha C2_SU2 + beta Y^2 = (3 alpha + beta)/4.
```

With `alpha=1`, the closing value needs `beta=-1`.  Retained positive
determinant/radiative measures give the same-sign sum.  A Berezinian/statistics
grading gives one sign to a whole field, not opposite signs to `SU(2)_L` and
`U(1)_Y` generators inside the same field.

The Wess-Zumino anomaly equations also do not supply the missing map.  For one
left-handed SM generation the standard anomaly coefficients cancel exactly:

```text
grav-U1 = 0, U1^3 = 0, SU2^2-U1 = 0, SU3^2-U1 = 0.
```

That zero consistency data cannot be converted into a nonzero
generation-cyclic traceless source without adding an independent physical
identification.

## Residual

```text
RESIDUAL_SCALAR = generator_selective_SU2_minus_U1_grading_alpha1_beta_minus1
RESIDUAL_MAP = generator_selective_SU2_minus_U1_grading_alpha1_beta_minus1
```

Equivalently, the open scalar remains

```text
rho(alpha,beta) - (C2_SU2 - Y^2) = (3 alpha + beta - 2)/4.
```

## Why this is not closure

This packet verifies an obstruction.  It does not derive `K_TL=0`; it shows
that the desired sign pattern is not a consequence of retained Wess-Zumino
consistency or standard Berezinian/statistics grading.

The exact `1/2` Casimir difference remains strong support, but promoting it to
the cyclic amplitude ratio would add precisely the missing physical law.

## Falsifiers

- A retained anomaly-inflow theorem whose descent functional produces a
  nonzero generation-cyclic `K_TL` source with fixed `alpha=1`, `beta=-1`.
- A retained superconnection/Berezinian construction where the internal
  generator grading, not field statistics, flips `U(1)_Y` relative to
  `SU(2)_L` and proves unit normalization.
- A source-class theorem showing all admissible local second-order measures
  collapse uniquely to `C2_SU2 - Y^2`.

## Boundaries

- The runner covers local generator-weighted second-order measures, standard
  field-statistics Berezinians, and the one-generation SM anomaly equations.
- It does not exclude a new topological superconnection principle, a
  nonlocal anomaly inflow law, or a future retained theorem coupling the
  electroweak generators directly to the `C_3` quotient source.

## Hostile reviewer objections answered

- **"The difference is numerically exact; why not accept it?"**  Because the
  map from electroweak Casimirs to `|b|^2/a^2` is still the load-bearing step.
  The runner gives countermaps with identical retained anomaly data and
  different `Q`.
- **"Could a Berezinian sign give the minus?"**  A field-statistics sign
  multiplies all generators of that field together.  It does not flip only
  hypercharge inside a lepton/Higgs doublet.
- **"Could Wess-Zumino consistency fix the sign?"**  The retained anomaly
  coefficients cancel to zero.  They enforce gauge consistency; they do not
  select the nonzero cyclic traceless source.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_wess_zumino_asymmetric_measure_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_Q_WESS_ZUMINO_ASYMMETRIC_MEASURE_NO_GO=TRUE
Q_WESS_ZUMINO_ASYMMETRIC_MEASURE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=generator_selective_SU2_minus_U1_grading_alpha1_beta_minus1
RESIDUAL_MAP=generator_selective_SU2_minus_U1_grading_alpha1_beta_minus1
```
