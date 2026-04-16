# Exact Two-Shell Channel Theorem on the `3+1` Plaquette Surface

**Date:** 2026-04-16  
**Status:** exact constructive local two-shell theorem  
**Script:** `scripts/frontier_hidden_two_shell_channel_theorem.py`

## Question

Once the first hidden quotient sector propagates to the exact two-shell sector,
does that second layer also collapse to a finite local alphabet, or does it
immediately become a large uncontrolled memory term?

## Exact answer

It also collapses to a finite local alphabet.

The one-step image of the `n = 5` hidden quotient sector is the exact two-shell
sector proved in `docs/HIDDEN_TWO_SHELL_PROPAGATION_THEOREM_NOTE.md`:

- one unit `4`-cube boundary
- two shared exterior `3`-cells

Under the full symmetry group of the unit `4`-cube, that propagated two-shell
sector reduces to:

- `226` exact ordered local two-shell orbits
- `121` exact unordered pair-orbits of complementary representatives

So the rooted hidden sector is not just “still local.” It has a finite exact
second-shell alphabet, but that alphabet is already much richer than the first
hidden-shell layer.

## Theorem 1: exact raw-to-orbit collapse

The exact propagated duplicate sector contains:

- `81280` duplicate quotient classes
- `49840` distinct raw ordered local two-shell states
- `24920` distinct raw unordered local two-shell pairs

After unit `4`-cube symmetry reduction, these collapse to:

- `226` ordered local two-shell orbits
- `121` unordered pair-orbits

This is a strong finiteness statement, but it also shows that the shell
hierarchy is growing quickly rather than collapsing to a tiny kernel.

## Theorem 2: exact ordered two-shell multiplicities

The `226` ordered two-shell orbits occur with exact multiplicity histogram

`{176:2, 192:6, 272:6, 304:6, 320:4, 352:19, 368:1, 384:9, 400:1, 480:6, 544:48, 576:2, 608:10, 640:7, 672:1, 704:23, 736:3, 768:6, 960:10, 1088:20, 1280:9, 1408:26, 1536:1}`.

## Theorem 3: exact one-step transfer kernel on the two-shell alphabet

For each of the `226` ordered two-shell orbits, compute the exact one-step
quotient continuation histogram.

The resulting next quotient counts range from `54` to `67`, with exact orbit
histogram

`{54:2, 55:1, 56:12, 57:8, 58:24, 59:39, 60:28, 61:42, 62:23, 63:23, 64:9, 65:12, 66:2, 67:1}`.

The full one-step quotient histograms are not all distinct, but there are
still `184` distinct exact transfer histograms on this `226`-orbit alphabet.

So the exact ordered two-shell alphabet remains finite, but it is already much
richer than the first-shell kernel.

## Theorem 4: exact unordered channel histogram

At the unordered pair level, the exact continuation-channel histogram has
`41` distinct count channels spread across `121` unordered pair-orbits.

The full exact channel histogram is checked by the runner; some large channels
are:

- `(59, 63)`: `5104`
- `(60, 61)`: `5184`
- `(61, 65)`: `3552`
- `(62, 62)`: `3808`

## Why this matters

This is the strongest rooted-side constructive result on the branch so far.

We now have:

1. exact first hidden sector = finite one-shell alphabet
2. exact propagated image = exact two-shell sector
3. exact two-shell sector = finite `226`-orbit ordered alphabet with `184`
   distinct exact one-step transfer histograms

So the rooted hidden sector is no longer just “some extra local memory.” It is
beginning to look like a genuine finite local shell hierarchy, but one whose
state space is growing quickly.

That does **not** yet derive analytic `P(6)`, but it narrows the remaining live
rooted route to a sharp question:

> does this exact local shell hierarchy continue to close at higher shell depth,
> or does a later layer force a qualitatively new nonlocal state variable?

## Honest status

This note still does **not** close the plaquette.

It does prove something stronger than the prior propagation note:

- the propagated hidden sector is finite
- its finite alphabet is explicit
- its exact one-step rooted transfer law is explicit
- the second shell does **not** compress to a tiny closed kernel

That is a real theorem step toward a rooted closure theorem, if one exists.

## Commands run

```bash
python3 scripts/frontier_hidden_two_shell_channel_theorem.py
```

Output summary:

- exact duplicate propagated classes: `81280`
- exact raw ordered two-shell states: `49840`
- exact ordered two-shell orbits: `226`
- exact unordered pair-orbits: `121`
- exact ordered next-count histogram:
  - `54:2`, `55:1`, `56:12`, `57:8`, `58:24`, `59:39`, `60:28`, `61:42`,
    `62:23`, `63:23`, `64:9`, `65:12`, `66:2`, `67:1`
- exact distinct ordered transfer histograms: `184`
