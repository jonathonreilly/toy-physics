# Analysis: Continuum Limit

## Date
2026-03-30

## Key Findings

### 1. The grid anisotropy is SCALE-INVARIANT — no continuum limit by distance alone
Signal speed anisotropy = 8.23% at ALL measurement distances (5 to 70 grid units). Action excess for off-axis paths = 7.06-7.25% at all path lengths. The discrete grid structure is visible at every scale.

**To achieve a continuum limit, you must change the grid itself** (finer resolution, more neighbors, or random graph). Going to larger distances on the same grid does not help.

### 2. Interference physics DOES converge despite grid anisotropy
V(y=1) stabilizes at 0.978-0.985 for widths ≥ 12. The interference predictions are robust to grid size even though the underlying grid anisotropy doesn't vanish. Interference is a TOPOLOGICAL property that doesn't depend on precise edge lengths — it depends on path existence, which is grid-size-independent once the threshold R_c is met.

### 3. Gravity dilutes with scale (ad_normalized → 0)
Action-diff per unit path length decreases from -0.345 (width=20) to -0.160 (width=80). The gravitational effect weakens as the grid grows, consistent with the field being a discrete Green's function on a finite domain.

### 4. The model does NOT have a naive continuum limit
On a fixed rectangular grid:
- Grid anisotropy: fixed at 8.2% (does not vanish)
- Interference: converges (topological, grid-insensitive)
- Gravity: weakens (dilutes with scale)

A true continuum limit would require:
- Finer grid spacing (more nodes per physical unit)
- Or: irregular/random graphs (no preferred directions)
- Or: extended neighbor connectivity (more directions per node)

## Significance
The model's discreteness is irreducible on a fixed grid. The 8.2% anisotropy is a permanent feature of the 8-neighbor rectangular lattice, not a finite-size artifact that vanishes at scale. This is actually physically interesting: it defines a "Planck scale" for the model — the grid spacing below which rotational symmetry breaks down.

For the model to have a continuum limit, the graph structure itself must become finer. This connects to the evolving-network prototype: if the graph GROWS (adding nodes), the effective resolution increases and the anisotropy should decrease in physical units even if it stays at 8.2% in grid units.
