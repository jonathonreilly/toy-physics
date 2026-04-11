# Staggered Geometry Superposition Note — 2026-04-11

**Status:** retained, bounded positive  
**Harness:** [frontier_staggered_geometry_superposition_retained.py](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_geometry_superposition_retained.py)

## What this is

This is a real **staggered-fermion branch-superposition** experiment on a fixed
periodic lattice.

Two classical branches are defined on the same adjacency:

- branch `A`: flat, `phi = 0`
- branch `B`: curved/source branch, `phi = (L + mu^2)^-1 rho_ext`

The same initial staggered wavepacket is evolved on both branches with the
parity/scalar coupling `H_diag = (m + phi) * epsilon(x)`. We then compare:

- detector distinguishability `TV(A,B)`
- detector phase shift `dphi(A,B)`
- coherent-superposition vs classical-mixture detector distance `TVq`
- global branch overlap

This is **not yet** a graph-topology superposition result. The lattice
adjacency is fixed. What is superposed is the effective scalar/geometry branch
on top of the same staggered transport law.

## Retained rerun

Rerun command:

```bash
source /tmp/physics_venv/bin/activate && python scripts/frontier_staggered_geometry_superposition_retained.py
```

Exact rerun output at the retained operating point `G=10`:

| Case | TV | dphi | TVq | overlap | PdetA | PdetB | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| `1D n=41` | `0.0001` | `0.0003` | `0.0000` | `0.9096` | `0.0000` | `0.0000` | `WEAK_OR_NULL` |
| `1D n=61` | `0.0000` | `0.0000` | `0.0000` | `0.9992` | `0.0000` | `0.0000` | `WEAK_OR_NULL` |
| `2D side=8` | `0.5766` | `3.5315` | `0.2237` | `0.0105` | `0.5791` | `0.2399` | `BOUNDED_POSITIVE` |
| `2D side=10` | `0.2493` | `0.3706` | `0.0685` | `0.1623` | `0.6025` | `0.2776` | `BOUNDED_POSITIVE` |
| `2D side=12` | `0.1271` | `0.1596` | `0.0146` | `0.2322` | `0.3937` | `0.2223` | `BOUNDED_POSITIVE` |

Operating point details:

- 2D source branch is placed at `(side/4, side/2)` on the midline
- detector is the right-edge strip `x >= 3*side/4`
- initial packet is a central Gaussian
- `m = 0.30`, `mu^2 = 0.22`, `dt = 0.12`, `N = 30`, `G = 10`

## Interpretation

What survives scrutiny:

- the effect is **null in 1D** under the same protocol
- the effect is **cleanly positive in 2D** at the retained operating point
- the coherent branch superposition differs from the classical mixture:
  - `TVq = 0.2237` at `side=8`
  - `TVq = 0.0685` at `side=10`
  - `TVq = 0.0146` at `side=12`
- the two branch states are globally distinguishable:
  - overlap drops to `0.0105` at `side=8`

What this means:

- the staggered-fermion dynamics is sensitive to a coherent superposition of
  flat vs curved **field branches**
- this is materially stronger than the old path-sum story because the transport
  law is now the retained staggered Hamiltonian, not a different ensemble model

## Limits

This note does **not** establish:

- adjacency/topology superposition
- entanglement generation between two independent matter systems
- a BMV-style witness by itself

So the honest claim is:

> On a fixed periodic 2D staggered lattice, a coherent superposition of flat
> and screened-field branches produces detector-resolved interference that
> differs from the corresponding classical mixture.

That is a bounded positive geometry/field-branch result, not a full graph
geometry superposition claim.
