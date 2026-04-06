# Claude Complex-Action Carryover Note

**Date:** 2026-04-05  
**Status:** retained narrow exact-lattice carryover

## Artifact chain

- [`scripts/exact_lattice_complex_action_carryover.py`](/Users/jonreilly/Projects/Physics/scripts/exact_lattice_complex_action_carryover.py)
- [`logs/2026-04-05-exact-lattice-complex-action-carryover.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-exact-lattice-complex-action-carryover.txt)

## Question

Can the branch exact-lattice complex-action harness be replayed on current
`main` as a narrow carryover, while keeping the claim surface exact-lattice
only?

This note stays deliberately narrow:

- one exact 3D lattice family
- one complex action
  - `S = L(1-f) + i*gamma*L*f`
- one exact `gamma = 0` reduction check
- one frozen-field Born test
- one `gamma` sweep for the TOWARD -> AWAY crossover

## Frozen result

The replay on `main` succeeds on the retained exact family:

- exact reduction:
  - standard propagator delta: `+9.339748e-02`
  - complex(`gamma = 0`) delta: `+9.339748e-02`
  - match: exact within machine precision
- Born test:
  - `gamma = 0.0`: `|I3|/P = 2.409e-15`
  - `gamma = 0.5`: `|I3|/P = 3.941e-16`
  - `gamma = 1.0`: `|I3|/P = 1.236e-16`
- gamma sweep:
  - `gamma = 0.00`: `TOWARD`, escape `2.7311`
  - `gamma = 0.05`: `TOWARD`, escape `2.0970`
  - `gamma = 0.10`: `AWAY`, escape `1.6119`
  - `gamma = 0.20`: `AWAY`, escape `0.9558`
  - `gamma = 0.50`: `AWAY`, escape `0.2056`
  - `gamma = 1.00`: `AWAY`, escape `0.0177`

## Safe read

The narrow, review-safe statement is:

- on the retained exact lattice family, the complex-action replay preserves
  the exact `gamma = 0` reduction
- the Born test is machine clean on the frozen field
- the `gamma` sweep retains the branch-like `TOWARD -> AWAY` crossover
- the escape ratio decreases smoothly as `gamma` increases

## What this is not

This note does **not** promote the result beyond the exact lattice family.

It is not:

- geometry-independent
- a continuum theorem
- a grown-geometry transfer claim
- a self-gravity mechanism claim

## Branch implication

The branch complex-action harness is now carryable onto `main` only in this
narrow form:

- exact-lattice only
- exact reduction retained
- Born retained
- crossover retained
- no broader complex-action theory claim implied

That is the strongest defensible carryover on current `main`.
