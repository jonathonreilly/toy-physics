# Analysis: Gravity Scaling + Self-Maintenance Viability

## Date
2026-03-30

## Key Findings

### 1. Decay rate α DOES decrease with grid size, but NOT as 1/L

| Grid | L_eff | α | α×L | π/L |
|------|-------|---|-----|-----|
| 20×16 | 16 | 0.230 | 3.67 | 0.196 |
| 30×24 | 24 | 0.156 | 3.74 | 0.131 |
| 40×32 | 32 | 0.122 | 3.92 | 0.098 |
| 60×48 | 48 | 0.101 | 4.85 | 0.065 |
| 80×64 | 64 | 0.104 | 6.65 | 0.049 |
| 100×80 | 80 | 0.114 | 9.14 | 0.039 |

α decreases from 0.23 to ~0.10 as grid size grows from 16 to 80, but then appears to plateau around α≈0.10-0.11 for the largest grids. This is NOT 1/L scaling (α×L is not constant). The gravity range grows with grid size but saturates — it doesn't become infinitely long-range.

The plateau at α≈0.10 suggests the field mode's relaxation has a characteristic decay length that becomes grid-independent at large scales. This could be related to the `(1-support) × avg(neighbors)` update rule in `derive_node_field` — the (1-support) factor introduces a local damping that prevents the field from reaching true harmonic behavior.

### 2. Self-maintenance viability boundary

| Config | Support? | Rule |
|--------|----------|------|
| 1 isolated node | NO | No persistent neighbors |
| 2 adjacent | YES (0.125) | Each is 1 of 8 neighbors of the other |
| 2 separated by 1 gap | NO | Not neighbors on grid |
| 2 separated by 2 | NO | Not neighbors |
| 3 L-shape | YES (0.250) | Corner node has 2/8 persistent neighbors |
| 4 square | YES (0.375) | Each has 3/8 persistent neighbors |
| 5 cross | YES (0.500) | Center has 4/8 persistent neighbors |
| Corner nodes | Higher support (0.333) | Fewer total neighbors at corner |
| Edge nodes | Higher support (0.200) | Fewer total neighbors at edge |

**The viability rule is: nodes must be ADJACENT (within 1 step including diagonals) to have nonzero mutual support. No gaps allowed.** Support = (# persistent neighbors) / (total neighbors). Corner/edge nodes get higher support per persistent neighbor because they have fewer total neighbors (3 or 5 vs 8 in interior).

### 3. Support scales with local density, not total count

Max support for configurations of different sizes:
- 2 nodes: 0.125 (1/8)
- 3 nodes: 0.250 (2/8)
- 4 square: 0.375 (3/8)
- 5 cross: 0.500 (4/8)

Max support = (n_persistent_neighbors) / 8 = (# of the node's 8 grid neighbors that are persistent). It saturates at 1.0 when all 8 neighbors are persistent (requires 9+ nodes in a filled 3×3 block).

## Significance

The gravity range does NOT scale to infinity — it saturates around α≈0.10, giving a characteristic decay length of ~10 grid units. This is a MODEL PREDICTION: the discrete toy model's gravity has finite range, unlike the 1/r² or ln(r) behavior of continuum gravity. Whether this is a feature (discrete gravity is naturally short-range) or a limitation (the field relaxation rule introduces artificial damping) is an open interpretive question.

The self-maintenance boundary confirms Axiom 2 at the mechanistic level: persistence requires adjacent patterns, with support scaling as local density fraction.
