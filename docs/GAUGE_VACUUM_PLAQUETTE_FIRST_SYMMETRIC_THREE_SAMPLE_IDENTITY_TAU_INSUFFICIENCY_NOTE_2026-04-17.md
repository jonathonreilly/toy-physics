# Gauge-Vacuum Plaquette First Symmetric Three-Sample Identity-Tau Insufficiency

**Date:** 2026-04-17  
**Status:** exact PF-only insufficiency theorem on the first symmetric
three-sample seam; even fixing the normalized identity value `Z_hat_6(e)` and
the tail mass `Tau_(>1)` still does **not** determine the first symmetric
retained coefficient pair or the corresponding three-sample triple  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_identity_tau_insufficiency_2026_04_17.py`

## Question

Suppose future work actually evaluates the normalized identity datum

`Z_hat_6(e)`

and also fixes the tail mass

`Tau_(>1)`.

Would that already determine the first symmetric retained coefficient pair

`(rho_(1,0)(6), rho_(1,1)(6))`

or equivalently the first symmetric retained three-sample triple?

## Answer

No.

The current exact first-seam equations show that fixed identity value plus
fixed tail mass still leaves a whole affine fiber of admissible retained
completions.

From the exact identity-mass relation,

`Tau_(>1) = Z_hat_6(e) - 1 - 18 rho_(1,0)(6) - 64 rho_(1,1)(6)`,

so fixing both `Z_hat_6(e)` and `Tau_(>1)` determines only the one linear
combination

`18 rho_(1,0)(6) + 64 rho_(1,1)(6) = C`.

That is one line in the first retained coefficient plane, not one point.

Along that line, the first symmetric retained three-sample triple is

`F [1, rho_(1,0), rho_(1,1)]^T`,

where `F` is the exact radical three-sample matrix. Because the second and
third retained columns of `F` are linearly independent, this triple varies
nontrivially along the line.

So even with fixed `Z_hat_6(e)` and fixed `Tau_(>1)`, the current exact seam
still does **not** determine:

- the retained coefficient pair,
- the retained three-sample triple,
- or the full beta-side vector `v_6`.

The missing input is therefore stricter than “identity-channel closure.”

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md):

- the first symmetric retained sample equations are

  `Z_hat_A = 1 + a rho_(1,0) + R_A^(>1)`,

  `Z_hat_B = 1 + b rho_(1,0) + c rho_(1,1) + R_B^(>1)`,

  `Z_hat_C = 1 + d rho_(1,0) + e rho_(1,1) + R_C^(>1)`,

- and the exact identity-mass relation is

  `Tau_(>1) = Z_hat_6(e) - 1 - 18 rho_(1,0)(6) - 64 rho_(1,1)(6)`.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md):

- the exact retained three-sample operator is the explicit radical matrix

  `F = [[1, a, 0],`
  `     [1, b, c],`
  `     [1, d, e]]`,

- and `det(F) != 0`.

## Theorem 1: fixed identity value plus fixed tail mass leaves an affine retained fiber

Fix any nonnegative `tau_0` and any positive retained identity mass `C > 0`.
Define

`Z_hat_6(e) = 1 + tau_0 + C`.

Then the exact identity-mass relation becomes

`18 rho_(1,0)(6) + 64 rho_(1,1)(6) = C`.

So every parameter value

`lambda in [0, C / 18]`

defines one nonnegative retained coefficient pair

`rho_(1,0)(6) = lambda`,

`rho_(1,1)(6) = (C - 18 lambda) / 64`,

with the same fixed `Z_hat_6(e)` and the same fixed `Tau_(>1) = tau_0`.

If one chooses the exact zero-tail slice

`R_A^(>1) = R_B^(>1) = R_C^(>1) = 0`,

then every such `lambda` gives one exact first-seam retained completion.

So fixed identity value plus fixed tail mass leaves an entire affine line of
retained completions, not one unique retained point.

## Theorem 2: the retained three-sample triple varies nontrivially along that line

Let

`Z_ret(lambda) = F [1, lambda, (C - 18 lambda)/64]^T`.

Then

`d Z_ret / d lambda = F [0, 1, -18/64]^T`.

The first component of this derivative is exactly `a`, and

`a = -3 sqrt(2 - sqrt(2)) != 0`.

Therefore the retained three-sample triple is not constant along the affine
fiber.

So fixed `Z_hat_6(e)` and fixed `Tau_(>1)` still do **not** determine the
retained three-sample data.

## Corollary 1: explicit witness pair at fixed identity and fixed tail mass

Take

`C = 1`,

`Tau_(>1) = tau_0`,

`Z_hat_6(e) = 2 + tau_0`.

Then both coefficient pairs

`P = (rho_(1,0), rho_(1,1)) = (0, 1/64)`,

`Q = (rho_(1,0), rho_(1,1)) = (1/36, 1/128)`

satisfy

`18 rho_(1,0) + 64 rho_(1,1) = 1`,

so they have the same fixed identity value and the same fixed tail mass.

With zero tails, their retained sample triples are

`Z_ret(P) = F [1, 0, 1/64]^T`,

`Z_ret(Q) = F [1, 1/36, 1/128]^T`,

and these are distinct because their `W_A` entries differ by `a / 36 != 0`.

So even one explicit fixed-identity fixed-tail slice already carries multiple
retained three-sample completions.

## What this closes

- exact proof that fixed `Z_hat_6(e)` and fixed `Tau_(>1)` still do **not**
  determine the first symmetric retained coefficient pair
- exact proof that fixed `Z_hat_6(e)` and fixed `Tau_(>1)` still do **not**
  determine the first symmetric retained three-sample triple
- exact clarification that identity-channel closure alone is still not enough
  to close the first retained beta-side seam

## What this does not close

- the true explicit beta-side vector `v_6`
- the true explicit values `Z_6^env(W_A)`, `Z_6^env(W_B)`, `Z_6^env(W_C)`
- the true explicit coefficients `rho_(1,0)(6)`, `rho_(1,1)(6)`
- the full plaquette PF closure
- the global sole-axiom PF selector theorem

## Why this matters

This theorem tightens the work order again.

The branch can no longer say:

- “maybe an identity-channel evaluation or bound will be enough.”

That is now too weak.

What the branch can honestly say is:

- even fixed identity value plus fixed tail mass still leaves nontrivial
  retained underdetermination,
- so the remaining load-bearing input really is beta-side environment data,
  not merely one more scalar summary of that data.
