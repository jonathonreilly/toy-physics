# Gauge-Vacuum Plaquette First Symmetric Three-Sample Tau-Controlled Retained-Coefficient Wedge

**Date:** 2026-04-17  
**Status:** exact PF-only coefficient-side outer-bound theorem on the first
explicit `beta = 6` retained seam; the current stack does not yet solve
`rho_(1,0)(6)`, `rho_(1,1)(6)`, or `Tau_(>1)`, but it does force them into one
exact `Tau`-controlled outer wedge and yields explicit linear upper bounds  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_tau_controlled_retained_coefficient_wedge_2026_04_17.py`

## Question

Using only the current exact stack already on the PF lane:

- the `beta = 6` boundary character-measure theorem,
- the first symmetric three-sample truncation envelope,
- the positive-cone/order witness,
- and the exact local Wilson partial evaluation,

is there one honest theorem directly on

`rho_(1,0)(6)`,

`rho_(1,1)(6)`,

`Tau_(>1)`?

## Answer

Yes.

The current stack supports one exact coefficient-side **outer wedge theorem**.

Let

`tau = Tau_(>1)`,

`rho10 = rho_(1,0)(6)`,

`rho11 = rho_(1,1)(6)`,

and define

`alpha = -a = 3 sqrt(2 - sqrt(2))`,

`beta = -e`,

where `a < 0` and `e < 0` are the exact first-sector radical coefficients from
the named three-sample map, and `d > 0` is the corresponding `W_C` coefficient.

Then every admissible coefficient/tail triple on the current exact stack must
satisfy

`tau >= 0`,

`rho10 >= 0`,

`rho11 >= 0`,

`rho10 <= (1 + tau) / alpha`,

`rho11 <= (1 + d rho10 + tau) / beta`.

Equivalently, the admissible set is contained in one exact outer wedge in
`(rho10, rho11, tau)`-space.

Therefore the current stack already yields explicit `Tau`-controlled linear
upper bounds:

`rho10 <= k10 (1 + tau)`,

`rho11 <= k11 (1 + tau)`,

with

`k10 = 1 / alpha = 0.4355209882921255...`,

`k11 = (1 + d / alpha) / beta = 1.6273092758221751...`.

Hence the first-retained identity mass also obeys

`18 rho10 + 64 rho11 <= M (1 + tau)`,

where

`M = 18 / alpha + 64 (1 + d / alpha) / beta = 111.98717144187746...`.

This does **not** solve `rho10`, `rho11`, or `tau`.
It is still an outer bound, because the current stack does not yet upper-bound
`tau` itself or evaluate the three full environment samples.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md):

- `Z_6^env(W)` is a real nonnegative class function,
- `rho_(p,q)(6) >= 0`,
- `rho_(p,q)(6) = rho_(q,p)(6)`,
- `rho_(0,0)(6) = 1`.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md):

`Z_hat_A = 1 + a rho10 + R_A^(>1)`,

`Z_hat_B = 1 + b rho10 + c rho11 + R_B^(>1)`,

`Z_hat_C = 1 + d rho10 + e rho11 + R_C^(>1)`,

with

`|R_i^(>1)| <= tau`.

The same note also already supplies the exact same-surface local first retained
witness point

`rho10^(loc) = a_(1,0)(6)^4 = 0.03187405744484778...`,

`rho11^(loc) = a_(1,1)(6)^4 = 0.0006931763545747348...`.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_POSITIVE_CONE_ORDER_WITNESS_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_POSITIVE_CONE_ORDER_WITNESS_NOTE_2026-04-17.md):

- the exact sign pattern is
  `a < 0`, `b > 0`, `c > 0`, `d > 0`, `e < 0`.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_PARTIAL_EVALUATION_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_PARTIAL_EVALUATION_NOTE_2026-04-17.md):

- the exact same-surface local Wilson sample values on the named seam are
  already explicit.

## Theorem 1: exact tau-controlled outer wedge

Because `Z_6^env(W)` is nonnegative and `z_(0,0)^env(6) > 0`, the normalized
sample values satisfy

`Z_hat_A >= 0`,

`Z_hat_B >= 0`,

`Z_hat_C >= 0`.

Apply this to the exact truncation-envelope intervals.

For `W_A`,

`Z_hat_A in [1 + a rho10 - tau, 1 + a rho10 + tau]`.

For this interval to intersect `[0, infinity)`, it is necessary that its upper
endpoint be nonnegative:

`1 + a rho10 + tau >= 0`.

Since `alpha = -a > 0`, this is equivalent to

`rho10 <= (1 + tau) / alpha`.

For `W_C`,

`Z_hat_C in [1 + d rho10 + e rho11 - tau, 1 + d rho10 + e rho11 + tau]`.

Again, interval intersection with `[0, infinity)` requires

`1 + d rho10 + e rho11 + tau >= 0`.

Since `beta = -e > 0`, this is equivalent to

`rho11 <= (1 + d rho10 + tau) / beta`.

Together with nonnegativity of `rho10`, `rho11`, and `tau`, this proves the
exact outer wedge

`0 <= rho10 <= (1 + tau) / alpha`,

`0 <= rho11 <= (1 + d rho10 + tau) / beta`,

`tau >= 0`.

The `W_B` row gives no stronger upper bound here because its first-retained
coefficients are already positive.

## Corollary 1: explicit individual tau-controlled coefficient bounds

Because the `rho11` upper bound is increasing in `rho10` and

`rho10 <= 1 / alpha * (1 + tau)`,

one gets

`rho11 <= (1 + d / alpha) / beta * (1 + tau) = k11 (1 + tau)`.

So the exact coefficient-side linear bounds are

`rho10 <= k10 (1 + tau)`,

`rho11 <= k11 (1 + tau)`,

with

`k10 = 0.4355209882921255...`,

`k11 = 1.6273092758221751...`.

## Corollary 2: explicit first-retained identity-mass bound

Using the exact identity-channel retained coefficient

`Z_hat_6(e) = 1 + 18 rho10 + 64 rho11 + tau`,

the wedge bounds imply

`18 rho10 + 64 rho11 <= M (1 + tau)`,

with

`M = 18 k10 + 64 k11 = 111.98717144187746...`.

So the current stack already linearly controls the first retained identity mass
in terms of the one open tail parameter.

## Corollary 3: same-surface local Wilson witness lies strictly inside the `tau = 0` slice

The exact local Wilson first-retained point satisfies

`rho10^(loc) = 0.03187405744484778... < 1 / alpha`,

`rho11^(loc) = 0.0006931763545747348... < (1 + d rho10^(loc)) / beta`.

Equivalently,

`1 + a rho10^(loc) = 0.9268139577616217... > 0`,

`1 + d rho10^(loc) + e rho11^(loc) = 1.0654786337155373... > 0`.

So the exact same-surface local first retained coefficients give one explicit
interior witness for the `tau = 0` cross-section of the outer wedge.

This is a support witness only. It does **not** identify the true environment
coefficients.

## What this closes

- one exact coefficient-side outer wedge for
  `(rho_(1,0)(6), rho_(1,1)(6), Tau_(>1))`
- one explicit `Tau`-controlled individual upper bound on `rho_(1,0)(6)`
- one explicit `Tau`-controlled individual upper bound on `rho_(1,1)(6)`
- one explicit `Tau`-controlled first-retained identity-mass bound
- one exact same-surface local Wilson interior witness for the `tau = 0`
  slice

## What this does not close

- an upper bound on `Tau_(>1)` itself
- explicit values of `rho_(1,0)(6)` or `rho_(1,1)(6)`
- explicit values `Z_6^env(W_A)`, `Z_6^env(W_B)`, `Z_6^env(W_C)`
- explicit class-sector matrix elements of `K_6^env` or `B_6(W)`
- the global sole-axiom PF selector theorem

## Why this matters

This is the strongest honest next coefficient theorem I found on the current
PF lane.

The branch no longer says only:

- the first retained coefficients are open, and
- the three-sample seam is evaluative.

It can now say:

- the open first retained coefficients already live in one exact
  `Tau`-controlled outer wedge,
- their first retained identity mass already has one explicit linear upper
  bound in terms of `Tau_(>1)`,
- and the exact same-surface local Wilson point already sits strictly inside
  the `tau = 0` slice.

That is real coefficient-side structure, even though the actual environment
solve is still open.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_tau_controlled_retained_coefficient_wedge_2026_04_17.py
```
