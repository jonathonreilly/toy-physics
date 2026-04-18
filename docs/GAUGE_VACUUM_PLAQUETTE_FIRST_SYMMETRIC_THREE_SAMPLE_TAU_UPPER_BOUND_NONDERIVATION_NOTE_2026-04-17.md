# Gauge-Vacuum Plaquette First Symmetric Three-Sample Tau Upper-Bound Nonderivation

**Date:** 2026-04-17  
**Status:** exact PF-only current-stack insufficiency theorem on the first
explicit `beta = 6` three-sample seam; the current exact branch now gives one
clean reason no theorem-grade finite upper bound on `Tau_(>1)` follows yet from
the landed seam constraints alone  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_tau_upper_bound_nonderivation_2026_04_17.py`

## Question

Using only the current exact PF seam already landed on branch:

- the character-measure theorem,
- the first symmetric three-sample truncation envelope,
- the first symmetric positive-cone/order witness,
- the `Tau`-controlled retained-coefficient wedge,
- the scalar-value insufficiency theorem,
- and the exact first-retained identity-mass relation,

does the repo now force any finite theorem-grade upper bound on

`Tau_(>1)`?

## Answer

No.

The current branch supports a stronger negative theorem:

> no finite upper bound on `Tau_(>1)` is derivable from the presently landed
> first-seam equalities and inequalities alone.

The reason is explicit.

For every nonnegative parameter `T`, the tuple

`rho_(1,0)(6) = 0`,

`rho_(1,1)(6) = 0`,

`R_A^(>1) = R_B^(>1) = R_C^(>1) = 0`,

`Z_hat_A = Z_hat_B = Z_hat_C = 1`,

`Z_hat_6(e) = 1 + T`,

`Tau_(>1) = T`

satisfies every theorem-level seam constraint currently available on this lane:

- the exact three-sample truncation-envelope equalities,
- the exact tail bounds `|R_i^(>1)| <= Tau_(>1)`,
- the retained positive-cone geometry,
- the exact order witness,
- the exact `Tau`-controlled wedge inequalities,
- and the exact identity-value relation
  `Tau_(>1) = Z_hat_6(e) - 1 - 18 rho_(1,0)(6) - 64 rho_(1,1)(6)`.

So the current exact seam constraints admit a one-parameter family with
arbitrarily large `Tau_(>1)`.

Therefore no finite theorem-grade upper bound on `Tau_(>1)` follows yet from
the current exact stack itself.

This is a **current-stack nonderivation theorem**, not a claim that the true
environment necessarily has arbitrarily large tail mass. It says only that the
present theorem bank does not yet exclude it.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md):

- `Z_6^env(W) / z_(0,0)^env(6)` is a real nonnegative class function,
- the normalized character coefficients are nonnegative and conjugation
  symmetric,
- and the trivial coefficient is normalized to `rho_(0,0)(6) = 1`.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md):

`Z_hat_A = 1 + a rho_(1,0)(6) + R_A^(>1)`,

`Z_hat_B = 1 + b rho_(1,0)(6) + c rho_(1,1)(6) + R_B^(>1)`,

`Z_hat_C = 1 + d rho_(1,0)(6) + e rho_(1,1)(6) + R_C^(>1)`,

with

`|R_i^(>1)| <= Tau_(>1)`,

and

`Tau_(>1) = Z_hat_6(e) - 1 - 18 rho_(1,0)(6) - 64 rho_(1,1)(6)`.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_POSITIVE_CONE_ORDER_WITNESS_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_POSITIVE_CONE_ORDER_WITNESS_NOTE_2026-04-17.md):

- the retained three-sample vector lies in the exact positive cone
  `Cone((1,1,1), (a,b,d), (0,c,e))`,
- and in particular `(1,1,1)` itself is an allowed retained positive-cone
  point.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_TAU_CONTROLLED_RETAINED_COEFFICIENT_WEDGE_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_TAU_CONTROLLED_RETAINED_COEFFICIENT_WEDGE_NOTE_2026-04-17.md):

`0 <= rho_(1,0)(6) <= k10 (1 + Tau_(>1))`,

`0 <= rho_(1,1)(6) <= k11 (1 + Tau_(>1))`,

with explicit positive constants `k10`, `k11`.

From
[GAUGE_VACUUM_PLAQUETTE_BETA6_SCALAR_VALUE_INSUFFICIENCY_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_BETA6_SCALAR_VALUE_INSUFFICIENCY_NOTE_2026-04-17.md):

- one scalar same-surface observable does not determine the full class-sector
  boundary vector.

So to derive a finite theorem-grade upper bound on `Tau_(>1)`, the current
stack would need one additional exact input that is not already among these
constraints.

## Theorem 1: one exact current-stack-compatible family carries arbitrary `Tau_(>1)`

Let `T >= 0` be arbitrary.

Define

`rho_(1,0)(6) = 0`,

`rho_(1,1)(6) = 0`,

`R_A^(>1) = R_B^(>1) = R_C^(>1) = 0`,

`Z_hat_A = Z_hat_B = Z_hat_C = 1`,

`Z_hat_6(e) = 1 + T`,

`Tau_(>1) = T`.

Then:

1. The exact three-sample envelope equalities hold:

   `Z_hat_A = 1 + a * 0 + 0 = 1`,

   `Z_hat_B = 1 + b * 0 + c * 0 + 0 = 1`,

   `Z_hat_C = 1 + d * 0 + e * 0 + 0 = 1`.

2. The exact tail bounds hold:

   `|R_i^(>1)| = 0 <= T = Tau_(>1)`.

3. The retained positive-cone constraint holds:

   the retained three-sample vector is exactly `(1,1,1)`,
   which is the trivial ray of the cone.

4. The exact order witness holds:

   `Z_hat_B - Z_hat_A = 0`.

5. The exact wedge inequalities hold:

   `0 <= 0 <= k10 (1 + T)`,

   `0 <= 0 <= k11 (1 + T)`.

6. The exact identity-value relation holds:

   `Tau_(>1) = (1 + T) - 1 - 18 * 0 - 64 * 0 = T`.

So for **every** nonnegative `T`, the current exact seam constraints admit this
constraint-compatible tuple.

## Corollary 1: no finite current-stack upper bound on `Tau_(>1)` follows

Assume there were a finite theorem-grade bound

`Tau_(>1) <= T_*`

derivable from the current exact seam constraints alone.

Pick `T > T_*`.

By Theorem 1, the current exact seam constraints still admit the tuple above
with `Tau_(>1) = T`, contradicting the supposed derivation.

Therefore no finite theorem-grade upper bound on `Tau_(>1)` follows yet from
the current exact seam bank itself.

## Corollary 2: one fixed same-surface scalar observable still does not repair this

The scalar-value insufficiency theorem already proves that one fixed same-surface
observable does not determine the full class-sector vector.

So adding a single accepted framework-point scalar value does not convert the
current seam constraints into a finite upper bound on `Tau_(>1)`.

The missing load-bearing input remains either:

- an actual upper bound or evaluation of `Z_hat_6(e)`,
- an actual upper bound on the higher character mass,
- or explicit `K_6^env / B_6(W)` matrix-element evaluation.

## What this closes

- one exact theorem that the **current** PF seam constraints do not yet imply a
  finite upper bound on `Tau_(>1)`
- one explicit one-parameter constraint-compatible family with arbitrary
  `Tau_(>1)`
- one exact clarification that the present branch is missing a new load-bearing
  input, not just algebraic rearrangement of existing seam data

## What this does not close

- the actual value of `Tau_(>1)`
- an actual upper bound on `Tau_(>1)` for the true Wilson environment
- explicit values of `rho_(1,0)(6)` or `rho_(1,1)(6)`
- explicit values `Z_6^env(W_A)`, `Z_6^env(W_B)`, `Z_6^env(W_C)`
- explicit `beta = 6` matrix elements of `K_6^env` or `B_6(W)`
- the global sole-axiom PF selector theorem

## Why this matters

This prevents the next wrong shortcut.

The branch can now say something sharper than:

- “`Tau_(>1)` is still open,” or
- “the current seam gives only a wedge.”

It can now say:

- the current seam constraints admit arbitrarily large `Tau_(>1)` as a
  theorem-level possibility,
- so no finite `Tau_(>1)` cap follows yet from the present theorem bank,
- and the next real PF work must add a genuinely new exact input rather than
  more rearrangement of the current three-sample geometry.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_tau_upper_bound_nonderivation_2026_04_17.py
```

Expected summary:

- `THEOREM PASS=5 SUPPORT=5 FAIL=0`
