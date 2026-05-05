# Gauge-Vacuum Plaquette First Three-Sample Local-Wilson Retained Positive-Cone Obstruction

**Date:** 2026-04-17  
**Status:** exact PF-only impossibility boundary on the named-sample
evaluation route; the exact local Wilson one-plaquette triple on
`W_A, W_B, W_C` cannot itself be the first symmetric positive-type retained
environment answer, so the nonlocal `K_6^env / B_6(W)` completion is not an
optional refinement  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_three_sample_local_wilson_retained_positive_cone_obstruction_2026_04_17.py`

## Question

After the exact local Wilson partial evaluation, the exact three-sample radical
map, and the exact positive-cone theorem on the first symmetric retained
sector, does the current repo support any stronger theorem on the live
`K_6^env / B_6(W_i)` seam than:

- the local sample-side Wilson values are known, but
- the full environment amplitudes are still open?

## Answer

Yes.

The current stack supports one exact obstruction theorem:

the normalized local Wilson one-plaquette sample triple

`Z^loc = [w_6(W_A), w_6(W_B), w_6(W_C)] / Z_(1plaq)(6)`

does **not** lie in the exact first symmetric retained positive cone.

Equivalently, when that local triple is reconstructed through the exact radical
three-sample inverse map, its unique retained coefficient vector is

`a^loc = F^(-1) Z^loc`

with

`a^loc_(0,0) =  0.34960695245840506...`,

`a^loc_(1,0) =  0.09339384931083796...`,

`a^loc_(1,1) = -0.03190961277002443...`.

So the local Wilson triple would require a **negative** adjoint-orbit retained
coefficient.

That is incompatible with the positive-type character-measure structure already
proved for the environment class function.

Therefore the exact local Wilson block cannot itself be the first symmetric
retained positive-type environment evaluator on `W_A, W_B, W_C`. Any honest
closure of the named-sample seam must include a genuinely nonlocal completion
through `K_6^env / B_6(W)` before or at the retained-sector stage.

This is stronger than merely saying the full environment samples are open. It
proves the current exact local evaluator is already on the wrong side of the
retained positive cone.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_PARTIAL_EVALUATION_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_LOCAL_WILSON_PARTIAL_EVALUATION_NOTE_2026-04-17.md):

- the exact local Wilson one-plaquette sample triple on the named seam is

`Z^loc_A = w_6(W_A) / Z_(1plaq)(6) = 0.1351652795620484...`,

`Z^loc_B = w_6(W_B) / Z_(1plaq)(6) = 0.3170224955005415...`,

`Z^loc_C = w_6(W_C) / Z_(1plaq)(6) = 0.5812139466746337...`.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md):

- the first symmetric retained exact sample matrix is

`F = [[1, a, 0],`
`     [1, b, c],`
`     [1, d, e]]`,

with radical entries

`a = -3 sqrt(2 - sqrt(2))`,

`b = -3 sqrt(2) + 3 sqrt(2 - sqrt(2 + sqrt(2))) + 3 sqrt(2 - sqrt(2 - sqrt(2)))`,

`c = 16 + 8 sqrt(2 + sqrt(2)) - 8 sqrt(2 + sqrt(2 + sqrt(2))) - 8 sqrt(2 + sqrt(2 - sqrt(2)))`,

`d =  3 sqrt(2) + 3 sqrt(2 - sqrt(2 + sqrt(2))) - 3 sqrt(2 - sqrt(2 - sqrt(2)))`,

`e = 16 - 8 sqrt(2 + sqrt(2)) - 8 sqrt(2 + sqrt(2 + sqrt(2))) + 8 sqrt(2 + sqrt(2 - sqrt(2)))`,

- and `F` is exactly invertible.

From
[GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_POSITIVE_CONE_ORDER_WITNESS_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_POSITIVE_CONE_ORDER_WITNESS_NOTE_2026-04-17.md):

- the first symmetric retained positive cone is

`C = Cone(r_0, r_1, r_2)`,

where the columns of `F` are the generating rays,

- and cone membership is equivalent to

`F^(-1) Z >= 0`

componentwise.

## Theorem 1: the exact local Wilson sample triple reconstructs with a negative adjoint coefficient

Let

`Z^loc = [Z^loc_A, Z^loc_B, Z^loc_C]^T`.

Apply the exact inverse radical map:

`a^loc = F^(-1) Z^loc`.

Then

`a^loc_(0,0) =  0.34960695245840506...`,

`a^loc_(1,0) =  0.09339384931083796...`,

`a^loc_(1,1) = -0.03190961277002443...`.

In particular:

- the trivial and fundamental-orbit retained coordinates are positive,
- but the adjoint-orbit retained coordinate is strictly negative.

So the exact local Wilson triple lies outside the first symmetric retained
positive cone.

## Corollary 1: the local Wilson evaluator cannot itself be the first symmetric positive-type environment evaluator

The environment character-measure theorem requires nonnegative retained
character coefficients on the positive-type class-function side.

Because `a^loc_(1,1) < 0`, the exact local Wilson triple cannot itself equal
any first symmetric retained positive-type environment sample triple.

So the current exact local evaluator is not merely incomplete; it is already
incompatible with the retained positive-type environment geometry.

## Corollary 2: the obstruction is not the coarse sample ordering

The local Wilson triple still obeys the coarse ordering

`Z^loc_B > Z^loc_A`.

So the failure is not the simple order witness proved earlier.

The actual obstruction is sharper: the local triple violates the third exact
half-space face of the retained positive cone, equivalently the adjoint-orbit
coordinate is negative after exact reconstruction.

## Corollary 3: any retained positive-type repair needs at least one positive adjoint-channel correction

Within the first symmetric retained reconstruction map, the local Wilson triple
already carries an adjoint-orbit deficit of

`0.03190961277002443...`.

Therefore any first symmetric retained positive-type repair must add at least
that amount in the `chi_(1,1)` channel coordinate before the reconstructed
coefficient vector can become nonnegative.

This does **not** yet evaluate the true environment triple. It states the
minimal retained-channel sign repair forced by the current exact local data.

## What this closes

- one exact incompatibility theorem between the exact local Wilson sample triple
  and the first symmetric retained positive cone
- one exact statement that the local Wilson evaluator cannot itself be the
  first symmetric positive-type environment evaluator on the named seam
- one exact identification of the obstruction: negative reconstructed
  adjoint-orbit coefficient
- one exact clarification that nonlocal `K_6^env / B_6(W)` completion is
  mathematically necessary before or at retained-sector closure

## What this does not close

- explicit values `Z_6^env(W_A)`, `Z_6^env(W_B)`, `Z_6^env(W_C)`
- explicit class-sector matrix elements of `K_6^env`
- explicit class-sector matrix elements of `B_6(W)`
- explicit values `rho_(1,0)(6)`, `rho_(1,1)(6)`, or `Tau_(>1)`
- the full plaquette PF closure
- the global sole-axiom PF selector theorem

## Why this matters

This sharpens the evaluation route in the honest direction.

The branch can now say not only:

- the local Wilson values are explicit, and
- the full environment amplitudes are still open.

It can also say:

- the local Wilson triple cannot itself be the retained positive-type answer,
- the obstruction occurs already at the first explicit retained seam,
- and any real evaluator has to do genuinely nonlocal work through the open
  `K_6^env / B_6(W)` objects rather than merely polishing the local block.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_first_three_sample_local_wilson_retained_positive_cone_obstruction_2026_04_17.py
```

Expected summary:

- `THEOREM PASS=5 SUPPORT=4 FAIL=0`
