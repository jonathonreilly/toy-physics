# Irregular Endogenous Sign-Closure Note

**Date:** 2026-04-11  
**Script:** `scripts/frontier_irregular_endogenous_sign_closure.py`  
**Status:** strong new frontier result, not yet retained

## Question

Can the endogenous irregular-graph lane produce one same-surface,
graph-native wavefunction observable that distinguishes attractive from
repulsive parity coupling cleanly, without using cubic exact-force semantics?

This note targets the live blocker directly:

- same graph
- same source
- same initial packet
- same coupling law
- only the sign of `Phi` changes inside the corrected parity channel

## Why a New Surface Was Needed

The earlier endogenous irregular-direction probe asked the wrong question for
the current sign blocker:

- it compared parity to the retired identity coupling
- its observables were short-time wavefunction diagnostics, but the packet was
  not designed to force a clean same-surface `+Phi` vs `-Phi` split
- the result was a blocker (`0/9`, `0/9`, `4/9`)

The weak-coupling retained note already froze a sign-sensitive regime on shell
metrics, but that result still leaned on shell-force-style counts and did not
freeze a same-surface matter-response observable.

This new probe does exactly that.

## Design

### Graphs

Three retained irregular bipartite families:

- random geometric (`side=8`)
- growing (`n_target=64`)
- layered cycle (`8x8`)

Seeds:

- `42..46`

Couplings:

- `G = 5, 10`

Total rows:

- `30`

### Packet

The source is the **graph center** chosen purely from graph structure:

- node with minimum BFS eccentricity
- ties broken by smaller mean BFS depth

The initial packet is also graph-native once the graph is fixed:

```text
psi_0(d) ~ exp(-d^2 / (2 sigma_d^2)) * exp(i k d)
```

with

- `d` = BFS depth from the graph center
- `sigma_d = 1.2`
- `k = 0.7`

So this is a centered shell packet with **outward shell phase**.
It deliberately stresses the sign question:

- attraction should hold the packet closer to the source ball
- repulsion should leak it outward faster

### Observables

Measured over the early-time window `steps 2:11`:

1. `ball1_margin`
   - `P_attr(depth <= 1) - P_rep(depth <= 1)`
2. `ball2_margin`
   - `P_attr(depth <= 2) - P_rep(depth <= 2)`
3. `depth_margin`
   - `<depth>_rep - <depth>_attr`

Positive margins mean attraction keeps the packet closer to the source region
than repulsion on the same surface.

These are all matter-response observables.
None are exact-force imports from the cubic card.

## Result

### Global

| Metric | Positive rows | Mean | Minimum |
|---|---:|---:|---:|
| `ball1_margin` | `30/30` | `+8.35e-02` | `+5.32e-02` |
| `ball2_margin` | `30/30` | `+2.41e-02` | `+5.32e-03` |
| `depth_margin` | `30/30` | `+1.20e-01` | `+6.52e-02` |

Norm drift stayed machine-clean across both signs:

- `max_norm_drift = 9.99e-16`

### By Family

#### Random geometric

- `ball2_margin`: `10/10` positive
- `depth_margin`: `10/10` positive
- means:
  - `ball2_margin ~ +2.91e-02` at `G=5`
  - `ball2_margin ~ +3.86e-02` at `G=10`
  - `depth_margin ~ +8.38e-02` at `G=5`
  - `depth_margin ~ +8.13e-02` at `G=10`

#### Growing

- `ball2_margin`: `10/10` positive
- `depth_margin`: `10/10` positive
- means:
  - `ball2_margin ~ +1.76e-02` at `G=5`
  - `ball2_margin ~ +2.95e-02` at `G=10`
  - `depth_margin ~ +1.25e-01` at `G=5`
  - `depth_margin ~ +2.05e-01` at `G=10`

#### Layered cycle

- `ball2_margin`: `10/10` positive
- `depth_margin`: `10/10` positive
- means:
  - `ball2_margin ~ +1.48e-02` at `G=5`
  - `ball2_margin ~ +1.47e-02` at `G=10`
  - `depth_margin ~ +1.48e-01` at `G=5`
  - `depth_margin ~ +7.73e-02` at `G=10`

## Honest Verdict

This is the strongest same-surface endogenous irregular sign result in the
repo so far.

What it **does** show:

> On a graph-native centered shell-packet surface, attraction keeps more
> probability inside the source ball and at lower mean BFS depth than
> repulsion on all audited irregular family/seed/G rows.

What it **does not** show:

- universal irregular directional gravity for arbitrary initial states
- exact-force closure on irregular graphs
- that every graph-native observable now separates the signs

So the correct interpretation is:

- **endogenous sign selection is now strongly closed on this audited shell-packet surface**
- the broader irregular off-lattice **directional** closure remains a larger
  claim and should stay separate

This is therefore a **strong frontier win**, but not yet a `main` retention
candidate until one of these is added:

- a second packet family with the same `30/30` style separation
- a size-portability sweep on the same shell-packet observable
- an unscreened / low-screening confirmation on the same surface

## Why This Matters

This lane no longer depends on:

- shell-force field-profile positivity
- cubic exact-force semantics
- parity-vs-identity comparisons

It is a direct same-surface wavefunction-response separator between
attractive and repulsive coupling on the retained irregular families.
