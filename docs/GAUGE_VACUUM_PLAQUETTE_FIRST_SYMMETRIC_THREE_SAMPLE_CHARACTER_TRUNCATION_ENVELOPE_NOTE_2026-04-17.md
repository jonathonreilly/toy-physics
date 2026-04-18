# Gauge-Vacuum Plaquette First Symmetric Three-Sample Character-Truncation Envelope

**Date:** 2026-04-17  
**Status:** exact retained-expansion theorem on the plaquette PF lane; the
current exact stack supports a theorem-grade first-symmetric truncation law and
an exact tail envelope for the three named `beta = 6` samples, but it still
does not close those sample values themselves  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_character_truncation_envelope_2026_04_17.py`

## Question

After the exact radical three-sample reconstruction theorem, the character
measure theorem, and the explicit local four-link Wilson factor, can the
current repo support any honest theorem-grade partial evaluation or bound on

`Z_6^env(W_A)`,

`Z_6^env(W_B)`,

`Z_6^env(W_C)`?

## Answer

Yes.

The current stack supports an exact first-symmetric retained truncation law and
an exact universal tail envelope.

Write the normalized boundary class function as

`Z_hat_6(W) = Z_6^env(W) / z_(0,0)^env(6)`.

Then the character-measure theorem gives

`Z_hat_6(W) = sum_(p,q) d_(p,q) rho_(p,q)(6) chi_(p,q)(W)`,

with

- `rho_(p,q)(6) >= 0`,
- `rho_(p,q)(6) = rho_(q,p)(6)`,
- `rho_(0,0)(6) = 1`.

On the first symmetric retained witness sector, the three named samples satisfy
the exact decomposition

`Z_hat_A = 1 + a rho_(1,0) + R_A^(>1)`,

`Z_hat_B = 1 + b rho_(1,0) + c rho_(1,1) + R_B^(>1)`,

`Z_hat_C = 1 + d rho_(1,0) + e rho_(1,1) + R_C^(>1)`,

where

`Z_hat_i = Z_hat_6(W_i)`,

`a = -3 sqrt(2 - sqrt(2))`,

`b = -3 sqrt(2) + 3 sqrt(2 - sqrt(2 + sqrt(2))) + 3 sqrt(2 - sqrt(2 - sqrt(2)))`,

`c = 16 + 8 sqrt(2 + sqrt(2)) - 8 sqrt(2 + sqrt(2 + sqrt(2))) - 8 sqrt(2 + sqrt(2 - sqrt(2)))`,

`d =  3 sqrt(2) + 3 sqrt(2 - sqrt(2 + sqrt(2))) - 3 sqrt(2 - sqrt(2 - sqrt(2)))`,

`e = 16 - 8 sqrt(2 + sqrt(2)) - 8 sqrt(2 + sqrt(2 + sqrt(2))) + 8 sqrt(2 + sqrt(2 - sqrt(2)))`,

and `R_i^(>1)` is the contribution of all conjugation-symmetric orbits beyond
`(0,0)`, `(1,0)/(0,1)`, and `(1,1)`.

Because `rho_(p,q)(6) >= 0` and `|chi_(p,q)(W)| <= d_(p,q)`, those tail terms
obey the exact envelope

`|R_i^(>1)| <= Tau_(>1)`,

with

`Tau_(>1) = sum_((p,q) notin {(0,0),(1,0),(0,1),(1,1)}) d_(p,q)^2 rho_(p,q)(6)`.

Equivalently,

`Tau_(>1) = Z_hat_6(e) - 1 - 18 rho_(1,0)(6) - 64 rho_(1,1)(6)`.

So the current repo already supports:

- one exact first-symmetric partial evaluation law,
- one exact universal tail bound,
- and therefore one honest controlled first-retained approximation framework
  once any future theorem or computation supplies `rho_(1,0)(6)`,
  `rho_(1,1)(6)`, and either `Tau_(>1)` or `Z_hat_6(e)`.

What it still does **not** support is explicit closure of those quantities.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md):

- the normalized boundary coefficients `rho_(p,q)(6)` are nonnegative and
  conjugation-symmetric,
- the full marked-holonomy dependence is already carried by the character
  expansion.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md):

- the first retained symmetric orbit-evaluation matrix on
  `W_A, W_B, W_C` is explicit in radicals,
- `W_A` kills the `chi_(1,1)` orbit exactly.

From
[GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md):

- the local four-link Wilson factor `a_(p,q)(6)^4` is explicit at `beta = 6`.

That local sequence does **not** identify the actual environment coefficients
`rho_(p,q)(6)`, but it does provide one exact same-surface beta-side retained
witness sequence that can be evaluated immediately.

## Theorem 1: exact first-symmetric retained decomposition of the three named samples

Let

`Z_hat_i = Z_6^env(W_i) / z_(0,0)^env(6)`,

for `i in {A,B,C}`.

Split the character expansion into the retained first symmetric orbit set

`R_1 = {(0,0),(1,0),(0,1),(1,1)}`

and the complement `R_(>1)`.

Then

`Z_hat_A = 1 + a rho_(1,0)(6) + R_A^(>1)`,

`Z_hat_B = 1 + b rho_(1,0)(6) + c rho_(1,1)(6) + R_B^(>1)`,

`Z_hat_C = 1 + d rho_(1,0)(6) + e rho_(1,1)(6) + R_C^(>1)`,

with the radical coefficients `a,b,c,d,e` listed above.

In particular:

- the first retained contribution to `W_A` depends only on `rho_(1,0)(6)`,
- the `rho_(1,1)(6)` orbit enters only through `W_B` and `W_C`,
- and those two entries retain opposite exact sign.

So the exact three-sample radical map already yields a genuine first-retained
partial evaluation law on the live `beta = 6` seam.

## Theorem 2: exact universal tail envelope

For every marked holonomy `W in SU(3)`,

`|chi_(p,q)(W)| <= d_(p,q)`.

Because every omitted coefficient in `R_(>1)` is nonnegative,

`|R_i^(>1)|
 <= sum_((p,q) in R_(>1)) d_(p,q) rho_(p,q)(6) |chi_(p,q)(W_i)|
 <= sum_((p,q) in R_(>1)) d_(p,q)^2 rho_(p,q)(6)
 = Tau_(>1)`.

So the same exact tail mass `Tau_(>1)` bounds the retained-truncation error at
all three named sample points.

## Corollary 1: exact sample intervals from any future first-retained coefficient solve

If future work supplies

- `rho_(1,0)(6)`,
- `rho_(1,1)(6)`,
- and `Tau_(>1)` or `Z_hat_6(e)`,

then the three named samples lie in the explicit intervals

`Z_hat_A in [1 + a rho_(1,0) - Tau_(>1), 1 + a rho_(1,0) + Tau_(>1)]`,

`Z_hat_B in [1 + b rho_(1,0) + c rho_(1,1) - Tau_(>1), 1 + b rho_(1,0) + c rho_(1,1) + Tau_(>1)]`,

`Z_hat_C in [1 + d rho_(1,0) + e rho_(1,1) - Tau_(>1), 1 + d rho_(1,0) + e rho_(1,1) + Tau_(>1)]`.

So the current repo already supports a controlled first-retained approximation
template. What remains open is the coefficient and tail solve itself.

## Corollary 2: exact beta=6 local retained witness

From the explicit local four-link Wilson factor at `beta = 6`,

`a_(1,0)(6)^4 = 0.03187405744484778...`,

`a_(1,1)(6)^4 = 0.0006931763545747348...`.

Substituting these explicit local coefficients into the first-retained radical
sample law gives the concrete local retained witness

`Z_hat_A^(loc,1) = 0.9268139577616217...`,

`Z_hat_B^(loc,1) = 1.0095674219120703...`,

`Z_hat_C^(loc,1) = 1.0654786337155373...`.

This is **not** the actual environment sample triple. It is the strongest
same-surface beta-side retained witness the current local source data support
without overclaiming the residual environment solve.

## What this closes

- exact first-symmetric retained partial evaluation law for the three named
  `beta = 6` samples
- exact universal tail envelope for the retained truncation error
- exact clarification that the current repo already supports a controlled
  first-retained approximation template once first retained coefficients and
  identity-tail mass are supplied
- one explicit beta=6 local retained witness triple from the exact local
  four-link Wilson factor

## What this does not close

- explicit values `rho_(1,0)(6)` or `rho_(1,1)(6)`
- explicit tail mass `Tau_(>1)` or explicit `Z_hat_6(e)`
- explicit values `Z_6^env(W_A)`, `Z_6^env(W_B)`, `Z_6^env(W_C)`
- explicit closed-form class-sector matrix elements of `K_6^env` or `B_6(W)`
- the global sole-axiom PF selector theorem

## Why this matters

This is the strongest honest character-side sharpening I found without
pretending the three same-surface samples are already solved.

The branch can now say something materially stronger than:

- the first retained matrix is explicit,
- but the three samples are unknown.

It can now say:

- the first retained contribution to each of the three samples is explicit,
- the retained error is bounded by one exact positive tail mass,
- the local Wilson data already produce one explicit same-surface retained
  witness triple,
- and the remaining work is exactly the residual environment coefficient/tail
  solve.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_character_truncation_envelope_2026_04_17.py
```

Expected summary:

- `THEOREM PASS=4 SUPPORT=4 FAIL=0`
