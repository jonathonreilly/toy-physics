# Gauge-Vacuum Plaquette First Symmetric Three-Sample Tau-Bound Route

**Date:** 2026-04-17  
**Status:** exact PF-only boundary theorem on the `Tau_(>1)` repair route for
the first symmetric three-sample seam; the current branch still does **not**
upper-bound the true environment `Tau_(>1)`, but it now proves one sharp lower
barrier for any route that tries to repair the exact local Wilson sample triple
using only the first-seam retained ansatz plus a uniform tail box  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_tau_bound_route_2026_04_17.py`

## Question

Beyond the exact `Tau`-controlled outer wedge and the theorem that the current
stack does not imply a finite upper bound on the true environment
`Tau_(>1)`, is there one stronger honest theorem on the `Tau_(>1)` route for
the first symmetric three-sample seam?

## Answer

Yes.

The strongest honest new theorem I found is a **sharp route boundary theorem**
for the explicit local Wilson completion path.

Let

`z_A^loc = w_6(W_A) / Z_(1plaq)(6) = 0.1351652795620484...`,

`z_B^loc = w_6(W_B) / Z_(1plaq)(6) = 0.3170224955005416...`,

`z_C^loc = w_6(W_C) / Z_(1plaq)(6) = 0.5812139466746343...`

be the exact normalized local Wilson sample triple on the named seam.

Ask whether this explicit triple can be represented in the first-seam
truncation-envelope form

`z_A^loc = 1 + a rho_(1,0) + R_A^(>1)`,

`z_B^loc = 1 + b rho_(1,0) + c rho_(1,1) + R_B^(>1)`,

`z_C^loc = 1 + d rho_(1,0) + e rho_(1,1) + R_C^(>1)`,

with

`rho_(1,0) >= 0`,

`rho_(1,1) >= 0`,

`|R_i^(>1)| <= tau`.

Then every such route completion must satisfy the sharp lower bound

`tau >= tau_*`,

where

`rho_(1,0)^* = (z_B^loc - z_A^loc) / (b - a) = 0.07110955014685417...`,

`tau_* = 1 - z_B^loc + b rho_(1,0)^*`

`      = 1 - z_A^loc - (-a) rho_(1,0)^*`

`      = 0.7015600400931378...`.

This bound is **sharp**.

It is attained by the explicit witness

`rho_(1,0) = rho_(1,0)^*`,

`rho_(1,1) = 0`,

`R_A^(>1) = z_A^loc - (1 + a rho_(1,0)^*) = -tau_*`,

`R_B^(>1) = z_B^loc - (1 + b rho_(1,0)^*) = -tau_*`,

`R_C^(>1) = z_C^loc - (1 + d rho_(1,0)^*) = -0.5666769381705485...`,

so `|R_C^(>1)| < tau_*`.

Therefore the exact local Wilson triple lies at exact `L^infty` distance
`tau_*` from the normalized first-retained positive wedge.

Equivalently:

- no route with `tau < 0.7015600400931378...` can repair the exact local
  Wilson triple on the first seam,
- the sharp obstruction is already exhausted by the `W_A / W_B` competition,
- and the `W_C` row is strictly slack at the optimizer.

This is a theorem about the **local-Wilson `Tau` route**.
It is **not** an upper or lower bound on the true environment `Tau_(>1)`.
The existing nonderivation theorem still says the current seam constraints
alone do not imply any finite upper bound on the actual environment tail mass.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_PARTIAL_EVALUATION_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_PARTIAL_EVALUATION_NOTE_2026-04-17.md):

- the exact normalized local Wilson one-plaquette sample triple on
  `W_A, W_B, W_C` is explicit.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_CHARACTER_TRUNCATION_ENVELOPE_NOTE_2026-04-17.md):

- the first-seam truncation-envelope model is

`Z_hat_A = 1 + a rho_(1,0) + R_A^(>1)`,

`Z_hat_B = 1 + b rho_(1,0) + c rho_(1,1) + R_B^(>1)`,

`Z_hat_C = 1 + d rho_(1,0) + e rho_(1,1) + R_C^(>1)`,

- with the uniform tail box
  `|R_i^(>1)| <= Tau_(>1)`.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_RETAINED_POSITIVE_CONE_OBSTRUCTION_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_RETAINED_POSITIVE_CONE_OBSTRUCTION_NOTE_2026-04-17.md):

- the exact local Wilson triple already lies outside the first retained
  positive cone.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_TAU_UPPER_BOUND_NONDERIVATION_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_TAU_UPPER_BOUND_NONDERIVATION_NOTE_2026-04-17.md):

- the current exact seam constraints still do **not** imply a finite upper
  bound on the true environment `Tau_(>1)`.

So the honest next question is no longer:

- “does the current stack force the true `Tau_(>1)` to be finite?”

That is already answered negatively.

The right route question is:

- “if one starts from the exact local Wilson triple and asks the tail box to
  repair it into a first-seam positive-type completion, how large must the
  tail box already be?”

## Theorem 1: sharp local-Wilson `Tau` barrier

Let

`alpha = -a > 0`.

Suppose the exact local Wilson triple is represented in first-seam form with

`rho_(1,0) >= 0`,

`rho_(1,1) >= 0`,

`|R_i^(>1)| <= tau`.

Then:

1. From the `W_A` row,

   `tau >= |z_A^loc - (1 + a rho_(1,0))|`

   `    >= 1 - z_A^loc - alpha rho_(1,0)`.

2. From the `W_B` row, because `z_B^loc < 1` and `b, c > 0`,

   `tau >= |z_B^loc - (1 + b rho_(1,0) + c rho_(1,1))|`

   `    = 1 - z_B^loc + b rho_(1,0) + c rho_(1,1)`

   `    >= 1 - z_B^loc + b rho_(1,0)`.

Therefore every admissible route completion obeys

`tau >= max(1 - z_A^loc - alpha rho_(1,0), 1 - z_B^loc + b rho_(1,0))`.

The first line is strictly decreasing in `rho_(1,0)` and the second is
strictly increasing.
So the minimum of their maximum occurs at the unique crossing point

`1 - z_A^loc - alpha rho_(1,0)^* = 1 - z_B^loc + b rho_(1,0)^*`,

hence

`rho_(1,0)^* = (z_B^loc - z_A^loc) / (b - a)`.

Substituting back gives the sharp lower bound

`tau >= tau_* = 1 - z_B^loc + b rho_(1,0)^*`.

## Corollary 1: the bound is sharp

Take

`rho_(1,0) = rho_(1,0)^*`,

`rho_(1,1) = 0`,

and define the residuals by the three exact sample equations.

Then

`R_A^(>1) = -tau_*`,

`R_B^(>1) = -tau_*`,

`R_C^(>1) = -0.5666769381705485...`,

so all three rows satisfy `|R_i^(>1)| <= tau_*`.

Hence `tau_*` is not only necessary; it is attained.

Therefore the local-Wilson completion route has exact sharp threshold

`tau_min^route = tau_* = 0.7015600400931378...`.

## Corollary 2: the sharp obstruction is already two-sample

At the optimizer,

`|R_C^(>1)| = 0.5666769381705485... < tau_*`,

with slack

`tau_* - |R_C^(>1)| = 0.1348831019225893...`.

So the sharp barrier is already generated by the competition between:

- lowering `W_A` far enough below the trivial baseline, and
- simultaneously lowering `W_B`, even though the first retained `W_B` row is
  forced upward by `b, c > 0`.

The `W_C` row is not load-bearing at the sharp boundary.

## Corollary 3: this route is quantitatively non-small-tail

Because

`tau_* = 0.7015600400931378... > 0.7`,

no small-tail repair exists for the exact local Wilson triple on this route.

So the current branch can now say something materially sharper than:

- the local Wilson triple is outside the retained positive cone.

It can say:

- the exact local Wilson triple is outside the normalized first-retained wedge
  by a **sharp quantitative amount**, and
- any route that tries to fix it only by invoking the first-seam
  `Tau_(>1)` tail box already needs uniform tail size greater than `0.7`.

## What this closes

- one exact sharp lower bound on the `Tau` repair route for the explicit local
  Wilson three-sample triple
- one exact optimizer
  `rho_(1,0)^* = (z_B^loc - z_A^loc) / (b - a)`, `rho_(1,1)^* = 0`
- one exact statement that the route barrier is already exhausted by the
  `W_A / W_B` rows
- one exact `L^infty` distance interpretation of the local-Wilson triple to
  the normalized first-retained positive wedge

## What this does not close

- the true environment value of `Tau_(>1)`
- any finite upper bound on the true environment `Tau_(>1)`
- explicit values `rho_(1,0)(6)` or `rho_(1,1)(6)` for the true environment
- explicit values `Z_6^env(W_A)`, `Z_6^env(W_B)`, `Z_6^env(W_C)`
- explicit class-sector matrix elements of `K_6^env` or `B_6(W)`
- the global sole-axiom PF selector theorem

## Why this matters

This is the clean quantitative boundary that was still missing on the `Tau`
side.

Before this note, the branch could say:

- the seam has one exact `Tau`-controlled outer wedge,
- and the current exact constraints do not imply a finite upper bound on the
  true `Tau_(>1)`.

Now it can also say:

- the obvious local-Wilson route is not merely incomplete,
- it is separated from the first-seam positive-type completion region by one
  exact sharp `Tau` barrier,
- and that barrier is already numerically large.

So the next honest progress on the `Tau` route cannot be “small local repair.”
It must add genuinely new nonlocal input.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_first_symmetric_three_sample_tau_bound_route_2026_04_17.py
```

Expected summary:

- `THEOREM PASS=6 SUPPORT=4 FAIL=0`
