# First Nonlocal Connected Plaquette Correction on the Exact `3+1` Lattice

**Date:** 2026-04-15  
**Status:** exact finite-order gauge theorem beyond the one-plaquette block  
**Script:** `scripts/frontier_plaquette_first_nonlocal_connected_correction.py`

## Question

After the constant-lift no-go, what is the first exact constructive correction
to the local `SU(3)` plaquette block on the full `3 spatial + 1 time` lattice?

## Exact answer

The correct object is the first **nonlocal connected** correction relative to
the exact one-plaquette block.

The exact result is:

`P_full(beta) = P_1plaq(beta) + beta^5 / 472392 + O_nonlocal(beta^6)`.

Equivalently, through `beta^5`:

`P_full(beta) = beta/18 + beta^2/216 - 5 beta^4/93312 - 49 beta^5/15116544 + O(beta^6)`.

The local block and the full lattice agree through `O(beta^4)`. The first
distinct `3+1` lattice correction is the area-`5` cube-complement term at
`O(beta^5)`.

## Important correction to the naive stage plan

The raw finite-order numerator/denominator story is subtler than the first
draft.

Local same-plaquette repeats and disconnected plaquette-antiplaquette bubbles
already occur below area `5`. So it is false that the denominator literally
starts only at area `6`.

What is true, and what is proved here, is narrower:

> after resumming the exact local one-plaquette block, the first **nonlocal
> connected** correction from distinct plaquettes occurs at `beta^5`.

That is the right finite-order theorem surface.

In particular, lower-order distinct-plaquette terms can still appear as raw
plaquette-antiplaquette bubbles. Those do not contradict the theorem, because
they factor out as exact unit bubbles and therefore do not contribute to the
connected difference relative to `P_1plaq`.

## Theorem 1: exact local block through `beta^5`

Using the exact Toeplitz/Bessel one-plaquette partition function and expanding
it in exact rational arithmetic gives:

`P_1plaq(beta) = beta/18 + beta^2/216 - 5 beta^4/93312 - beta^5/186624 + O(beta^6)`.

There is no `beta^3` term in the local block.

## Theorem 2: the first distinct connected geometry is the area-`5` cube complement

The exact open-surface hierarchy note already proves:

- the tagged plaquette is the unique area-`1` same-boundary surface
- the first nonlocal same-boundary surfaces have area `5`
- on the exact `3+1` lattice there are exactly `4` such minimal completions

So any genuinely distinct connected correction must wait until `5` inserted
plaquettes, i.e. `O(beta^5)`.

Local repeats and vacuum-bubble factors may occur earlier, but they are
already absorbed by the exact local block or canceled in the connected
comparison.

### Bubble lemma

For any plaquette `p`, the pair `W_p W_p^dag` is an exact unit bubble after
integrating over the three nonshared links of `p`:

`integral dA |Tr(M A)|^2 = 1`

for any fixed `M in SU(3)`, by Haar invariance and the two-point identity.

So lower-order distinct-plaquette terms built only by attaching such
plaquette-antiplaquette bubbles do not generate a connected correction beyond
the exact local block.

## Theorem 3: exact oriented cube-boundary moment

Take one elementary cube containing the tagged plaquette. The corresponding
area-`5` complement together with the tagged plaquette forms the full oriented
cube boundary.

For one global orientation of that cube boundary, every link appears exactly
once as `U` and once as `U^dag`, so the expectation is computed using only the
two-point identity

`integral dU U_ij U^dag_kl = delta_il delta_jk / 3`.

Counting the induced color-index loops gives:

- `12` link integrals
- `8` free color loops

therefore

`< product_(faces of cube) Tr U_face > = 3^(8-12) = 1/81`.

There are exactly `2` surviving global orientations in the `Re Tr` expansion:
outward and inward.

## Theorem 4: exact first nonlocal connected coefficient

For one fixed area-`5` cube complement:

- each plaquette contributes a factor `1/6` from `P_p = (Tr U_p + Tr U_p^dag)/6`
- the `1/5!` from the action expansion cancels the `5!` orderings of the five
  distinct inserted plaquettes
- the oriented cube-boundary moment is `1/81`
- the orientation count is `2`

On the exact `3+1` lattice there are `4` such cube complements.

Therefore

`C_5^nonlocal = 4 * 2 * (1/6^6) * (1/81) = 1/472392`.

So

`P_full(beta) = P_1plaq(beta) + beta^5 / 472392 + O_nonlocal(beta^6)`.

## Why this is the right next theorem

This is the first constructive result after the constant-lift failure:

- the local block remains exact
- the first full-lattice correction is now explicit
- the correction is tied to the exact `3+1` cube geometry, not to a guessed
  coupling lift

So the project now has both halves of the story:

1. the old dressed one-plaquette closure is dead
2. the real analytic route begins with an exact connected open-surface
   correction

## Honest status

This still does **not** close full analytic `P(beta = 6)`.

It closes the next real theorem gate:

> the first nonlocal connected departure from the exact one-plaquette block is
> known exactly, and it is the area-`5` cube-complement contribution with
> coefficient `1/472392`.

The next gate is the exact higher-surface layer beyond the elementary cube
complements.

That next gate is now partially closed by
`docs/ROOTED_3CHAIN_COEFFICIENT_ENGINE_NOTE.md`, which tabulates the exact
rooted same-boundary `3`-chain coefficients through five `3`-cells, corrects
the earlier boundary-shellable undercount, and proves that a directed-cell
face-factorized closure is already false at `n = 3`.

The exact local closure / obstruction surface beyond that is now:

- `docs/DIRECTED_CELL_BOUNDARY_CLUSTER_THEOREM_NOTE.md`
- `docs/ROOT_FACE_LAUNCH_THEOREM_NOTE.md`
- `docs/DIRECTED_CELL_BOUNDARY_STATE_TRANSFER_NOTE.md`
- `docs/LOCAL_FACE_CLOSURE_REJECTION_NOTE.md`

## Commands run

```bash
python3 scripts/frontier_plaquette_first_nonlocal_connected_correction.py
```

Output summary:

- exact checks: `10 pass / 0 fail`
- exact first nonlocal connected coefficient: `1/472392`
- exact full-vs-local difference first appears at `beta^5`
