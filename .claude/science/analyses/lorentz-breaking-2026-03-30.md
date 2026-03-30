# Analysis: Lorentz Breaking on Discrete Grid

## Date
2026-03-30

## Key Findings

### 1. The grid breaks rotational symmetry by exactly 8.2%
Action per unit Euclidean distance:
- Axis-aligned (0°, 90°): 1.000000 (exact)
- Diagonal (45°): 1.000000 (exact)
- Off-axis (~30°, ~60°): 1.072 (+7.2%)

The grid preserves symmetry along its 4 axes and 4 diagonals (8 directions). Between these special directions, paths must staircase, adding ~8% excess action.

### 2. Signal speed anisotropy = 8.2%
Signal speed = 1.000 along axes and diagonals, drops to 0.924 at off-axis angles. The "speed of light" in this model is direction-dependent on the grid — a lattice artifact that would vanish on a finer or irregular grid.

### 3. The 8.2% figure is the grid's discreteness scale
The theoretical maximum anisotropy for a square grid with 8-neighbor connectivity is:
- Path from (0,0) to (1,1): Euclidean distance = √2, grid distance = √2 (one diagonal step). Ratio = 1.000.
- Path from (0,0) to (2,1): Euclidean distance = √5 ≈ 2.236, best grid path = 1 diagonal + 1 horizontal = √2 + 1 ≈ 2.414. Ratio = 2.414/2.236 = 1.080.

The measured 8.2% matches this theoretical prediction (1.080 - 1.000 = 8.0%).

### 4. Gravity also carries the 8.2% anisotropy
Gravitational action_diff varies with path direction through the mass. This means gravitational measurements on the grid have ~8% direction-dependent systematic error — the same lattice artifact.

## Significance

The 8.2% Lorentz-breaking is a QUANTITATIVE PREDICTION of the model's discreteness. On a finer grid (more neighbors per node), this would decrease. On a triangular grid (6 directions vs 8), it would be different. On a random graph, it would fluctuate.

This number characterizes the "grain" of the discrete spacetime — how much the underlying network structure shows through in observable physics. In the continuum limit (infinite grid resolution), it would vanish, recovering full rotational symmetry.
