# Derivation: Visibility Threshold R_c(y)

## Date
2026-03-30

## Target Behavior
Off-center fringe visibility V(y) = 0 exactly when width/slit_sep < R_c(y), with R_c(y) ≈ 0.25|y| + 1.0 for slit_half=4. The transition is discontinuous.

## Axioms Used
- Events are nodes on a rectangular grid: (x, y) for x in [0, width], y in [-height, height]
- Links connect adjacent nodes (including diagonals based on the DAG construction)
- The causal DAG is built from arrival times: a link from A to B exists only if arrival_time(B) > arrival_time(A)
- Blocked nodes at the barrier (x = width/2) except at slit positions

## Minimal Example

Consider the simplest case: source at (1, 0), barrier at x = w/2, slits at y = ±s, detector at x = w, screen position y_d > 0.

A path from source to detector through slit y = -s (the far slit) must:
1. Travel from (1, 0) to (w/2, -s) — moving rightward and downward
2. Pass through the slit at (w/2, -s)
3. Travel from (w/2, -s) to (w, y_d) — moving rightward and upward

The post-barrier leg (step 3) travels from y = -s to y = y_d, a vertical distance of s + y_d, over a horizontal distance of w/2.

On the rectangular grid with the causal DAG, the maximum upward displacement per horizontal step is bounded. Each step advances x by 1 and y by at most +1 (diagonal move). Therefore:

**Maximum vertical displacement in w/2 steps = w/2**

For the far-slit path to reach (w, y_d), we need:

s + y_d ≤ w/2

Rearranging:

**w ≥ 2(s + y_d)**

Or in terms of ratio R = w/(2s):

**R ≥ 1 + y_d/s**

## Derivation

### Step 1: Grid connectivity constrains maximum path deflection

On the rectangular grid, the causal DAG admits links to neighbors at (dx, dy) where dx > 0 (forward in time) or dx = 0 with specific ordering. The maximum vertical step per horizontal step is |dy/dx| = 1 (diagonal links).

### Step 2: The far slit requires maximum deflection

A path through the far slit (y = -s for y_d > 0) must cover vertical distance (s + y_d) in the post-barrier region of width w/2. At maximum deflection of 1 unit vertical per horizontal step:

Required: s + y_d ≤ w/2

### Step 3: The near slit is always reachable (for small y_d)

A path through the near slit (y = +s) must cover vertical distance |s - y_d| in the post-barrier region. For y_d < s, this is s - y_d < s < w/2 (always satisfiable for w ≥ 2s, which is the minimum for a barrier to exist).

### Step 4: The threshold occurs when the far slit first becomes reachable

V(y_d) = 0 when only the near slit contributes (far slit unreachable).
V(y_d) > 0 when both slits contribute.

The transition occurs at:

**w/2 = s + y_d**
**R_c = w/(2s) = 1 + y_d/s**

### Step 5: Verify against data

For slit_half = s = 4:

| y_d | R_c predicted = 1 + y_d/4 | R_c observed |
|-----|---------------------------|-------------|
| 1 | 1.25 | 1.25 (w=10) |
| 2 | 1.50 | 1.50 (w=12) |
| 3 | 1.75 | 1.75 (w=14) |
| 5 | 2.25 | 2.25 (w=18) |

**Exact match at all four data points.**

## Novel Prediction

The derivation predicts:

1. **R_c(y) = 1 + |y|/s exactly** (not approximately). The ≈ in the empirical fit was unnecessary — the relationship is exact.

2. **For y_d = s (screen position at the slit): R_c = 2.** This means V(y=s) > 0 requires w ≥ 4s. Testable.

3. **For y_d = 0 (center): R_c = 1.** The center always has two-slit reachability as long as the grid is wider than the slit separation. This explains why V(y=0) = 1 at all geometries in the original sweep — both slits are always reachable at center.

4. **The pre-barrier leg imposes no additional constraint** for a centered source, because the source-to-slit distance (horizontal w/2, vertical s) has the same geometry as the slit-to-detector leg for y_d = 0.

5. **On a non-rectangular grid with maximum diagonal slope m** (instead of 1), the threshold would generalize to: R_c(y) = 1 + |y|/(m × s). This is testable on grids with different connectivity.

## Weakest Link

Step 1 assumes the maximum deflection per step is exactly 1 (diagonal links). This depends on how `build_causal_dag` constructs the DAG. If the DAG admits longer-range links (e.g., knight's-move connections), the threshold would be lower. The derivation is exact for the standard rectangular grid with nearest-neighbor + diagonal links.

## Status
CONFIRMED — exact match at all 4 data points. The law R_c(y) = 1 + |y|/s is derived from the grid's causal DAG connectivity constraint, not fit from data.
