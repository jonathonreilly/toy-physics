# Dimension Emergence -- Bounded Companion Note

**Date:** 2026-04-12
**Status:** bounded companion to `DIMENSION_EMERGENCE_NOTE.md`
**Branch:** `claude/youthful-neumann`
**Script:** `scripts/frontier_dimension_emergence.py`

## Scope

This note narrows the dimension-emergence claim to what the numerical
evidence actually supports, following the codex review audit of
2026-04-12.

## Bounded Claim

On regular d-dimensional cubic lattices, the Poisson Green's function
determines the force-law exponent:

| Lattice | d_s (measured) | Force exponent | Continuum prediction |
|---------|---------------|----------------|----------------------|
| 2D      | 2.01          | alpha ~ -0.19  | 0 (log potential)    |
| 3D      | 2.84          | alpha ~ -1.06  | -1 (1/r potential)   |

The dimensional progression is retained: increasing lattice dimension
produces monotonically steeper Green's function decay, and d=3 yields
the inverse-square force law via the 1/r potential.

## What Is NOT Claimed

1. **No universality beyond tested lattice families.** The result is a
   bounded regular-lattice Poisson proxy. It does not establish that
   spectral dimension alone determines the force law on arbitrary graph
   topologies (small-world, scale-free, grown graphs, etc.).

2. **No quantitative Green's function match on irregular graphs.**
   Screened-Poisson on small-world/tree graphs shows the qualitative
   trend but not quantitative agreement with beta = -(d_s - 2).
3. **No dynamic dimension emergence.** Whether a growing graph can
   dynamically reach d_s = 3 is not addressed.

## What IS Retained

- Heat-kernel spectral dimension correctly recovers d_s = 1, 2, 3 on
  regular lattices (3D reads 2.84 due to finite size at 12^3 nodes).
- On these lattices, the Poisson field equation reproduces the expected
  continuum force law: F ~ 1/r^(d-1).
- d_s = 3 is the lowest integer dimension where the Green's function
  decays as a power law (1/r), producing inverse-square force.

## Caveats

- 3D d_s = 2.84 (target 3.0): finite-size effect at N = 1728.
- 2D alpha = -0.19 (target 0): log convergence slow at side = 56.

## References

- Script: `scripts/frontier_dimension_emergence.py`
- Parent note: `docs/DIMENSION_EMERGENCE_NOTE.md`
- Codex review: `docs/OVERNIGHT_CLAUDE_AUDIT_2026-04-12.md`
