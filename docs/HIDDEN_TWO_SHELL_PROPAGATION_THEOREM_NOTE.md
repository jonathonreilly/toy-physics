# Exact Propagated Two-Shell Theorem on the `3+1` Plaquette Surface

**Date:** 2026-04-16  
**Status:** exact constructive propagated hidden-sector theorem  
**Script:** `scripts/frontier_hidden_two_shell_theorem.py`

## Question

Does the first hidden quotient alphabet actually close one more rooted layer, or
does a new hidden geometry appear immediately?

## Exact answer

A new hidden geometry appears immediately, but it is still finite and local.

The exact `n = 5` hidden quotient sector from
`docs/HIDDEN_SHELL_CHANNEL_THEOREM_NOTE.md` is a one-cube / one-shell defect:

- one unit `4`-cube boundary
- one shared exterior `3`-cell

Its one-step rooted image at `n = 6` is still a one-cube defect, but now with

- one unit `4`-cube boundary
- two shared exterior `3`-cells

So the hidden sector remains local under propagation, but the bare `12`-state
one-shell alphabet is **not** closed as a final rooted transfer state.

The exact next refinement is now in
`docs/HIDDEN_TWO_SHELL_CHANNEL_THEOREM_NOTE.md`, which proves that this
propagated two-shell sector also collapses to a finite local alphabet under
unit `4`-cube symmetry, but not a tiny one: `226` ordered local orbits and
`121` unordered pair-orbits.

## Theorem 1: exact one-step image of the first hidden sector

Take every representative in the exact `n = 5` duplicate quotient sector and
extend it by one admissible root-preserving `3`-cell.

Group the resulting `n = 6` fillings by quotient surface key.

Then the exact one-step image has:

- `140224` quotient classes
- multiplicity histogram `{1: 58944, 2: 81280}`

So every duplicate quotient class in this image is again a simple pair.

## Theorem 2: every propagated duplicate pair is still one unit `4`-cube

For every duplicate quotient class in that one-step image:

- the symmetric difference of the two representatives has size `8`
- that symmetric difference is exactly one unit `4`-cube boundary

So the propagated hidden sector has not escaped the same basic cubical defect
type.

## Theorem 3: the hidden shell has grown from one cell to two

Fix the witness `4`-cube from Theorem 2.

For every propagated duplicate pair, the two representatives agree on exactly
two `3`-cells outside that witness cube.

Equivalently, every propagated duplicate class is:

`one unit 4-cube boundary + two shared exterior 3-cells`.

This is an exact two-shell sector.

## Why this matters

This corrects the over-strong closure phrasing around the prior hidden-shell
theorem.

The exact first hidden alphabet is real and useful, but its correct propagated
statement is:

1. the first hidden layer reduces to a finite local one-shell alphabet
2. its one-step image remains local
3. that image is an exact two-shell sector, not a closed `12`-state final
   Markov alphabet

So the rooted route now points toward an exact finite local **shell hierarchy**,
not a single hidden-shell summary.

The next note strengthens that claim from qualitative to exact:

> the propagated two-shell sector has `226` ordered local orbits and `121`
> unordered pair-orbits, with `184` distinct exact one-step quotient transfer
> histograms on the ordered sector.

## Honest status

This note still does **not** derive analytic `P(6)`.

It does something important and exact:

1. it proves the first propagated hidden layer is still local
2. it proves the local hidden sector grows in a controlled way
3. it replaces the earlier “one more layer closes” wording with the stronger
   and more honest theorem: the hidden sector lifts to a two-shell defect class

That is a real theorem step toward either:

- a rooted finite-shell hierarchy, or
- a direct finite-`beta` activity theorem on the quotient-surface gas

## Commands run

```bash
python3 scripts/frontier_hidden_two_shell_theorem.py
```

Output summary:

- exact one-step image quotient class count: `140224`
- exact one-step image multiplicity histogram: `{1: 58944, 2: 81280}`
- exact duplicate child class count: `81280`
- every duplicate child pair has symmetric-difference size `8`
- every duplicate child pair is one unit `4`-cube boundary plus `2` shared
  exterior `3`-cells
