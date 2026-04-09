# Derivation: Tapered lattice unifies attraction and distance law

## Date
2026-04-04

## Target Behavior
Simultaneously achieve:
(a) Gravity TOWARD mass (centroid shift positive toward mass)
(b) Distance-dependent deflection (|delta| decreases with b)

Currently achieved separately:
- Random mirror DAGs: (a) yes, (b) no
- NN lattice: (a) no, (b) yes (b^(-1.82) on 3D)

## Axioms Used
- Events are nodes with positions
- Links connect events with continuation weights
- Continuation weights include a directional measure (forward preference)

## Minimal Example

Consider a 1D beam propagating through a layered network:

```
Layer 0: [source at y=0]
Layer 1: [y=-2, y=-1, y=0, y=+1, y=+2]
Layer 2: [y=-2, y=-1, y=0, y=+1, y=+2]
```

Standard NN: each node connects to y-1, y, y+1 in next layer.
All nodes have multiplicity 3. Beam spreads uniformly.

Tapered NN: connectivity depends on |y|:
- y=0: connects to y=-1, y=0, y+1 (3 edges)
- y=±1: connects to y=0, y=±1 (2 edges, toward center + straight)
- y=±2: connects to y=±2 (1 edge, straight only)

Now the multiplicity from source (y=0) after 2 layers:
- y=0: 3×3 = 9 paths (through high-connectivity center)
- y=±1: 3×2 = 6 paths
- y=±2: 3×2×1 = 6 paths... hmm, still similar.

The REAL difference: at y=±2 with only straight edges, the path
from source must have taken 2 sideways steps to get there. With
the taper, those sideways steps are suppressed because the
y=±1 nodes only have 2 edges (not 3). The amplitude reaching
y=±2 is smaller not because of fewer edges FROM y=±2, but because
of fewer edges TO y=±2 from central nodes.

Actually, the key mechanism is different. Let me re-derive.

## Derivation

### Step 1: Beam depletion occurs when the mass-free amplitude at a
node is LARGER than the mass-present amplitude at the same node.

On the standard lattice, the mass field changes the phase of ALL
paths equally (deterministic geometry). The phase change causes
destructive interference at the beam center, reducing the peak
amplitude. The centroid shifts AWAY from the depletion zone.

### Step 2: Attraction occurs when the mass-present amplitude at
mass-side nodes is LARGER than the mass-free amplitude.

On random DAGs, different paths to the same node have different
geometric lengths. The phase change from the mass field affects
each path differently. Some paths get MORE constructive (phases
align better) while others get less. On average, paths TOWARD
mass tend to align (shorter paths, similar field exposure), while
paths AWAY tend to cancel (longer paths, varied field exposure).

### Step 3: The lattice fails because path geometry is deterministic.

All paths from source to a given detector node pass through the
SAME sequence of y-positions. The phase change from the field is
the same for all paths to that node. There's no opportunity for
selective constructive interference.

### Step 4: To get attraction on a lattice, paths to the same
detector node must have DIFFERENT accumulated phases.

This requires: paths with different TOTAL LENGTHS reaching the
same endpoint. On the standard NN lattice, all paths from (0,0)
to (N,y) have the same x-displacement (N) but different y-paths.
The total length depends on how many diagonal steps were taken.

A path with k diagonal steps has length:
  L = (N-k) × h + k × √2 × h = h × (N + k(√2 - 1))

So paths with MORE diagonal steps are LONGER. The phase from the
mass field at each edge depends on the field VALUE at that edge,
which depends on the y-position of the edge. Different paths pass
through different y-positions, so they accumulate different
field-dependent phases.

### Step 5: The problem is that the field-FREE phases also differ.

Even without mass, paths with different numbers of diagonal steps
have different total lengths → different phases. The interference
pattern is set by BOTH the field-free phase and the field-dependent
phase. The mass field perturbs this pattern, and the perturbation
creates beam depletion rather than attraction because the field
is POSITIVE everywhere (it always increases the phase).

### Step 6: To get attraction, the field perturbation must create
CONSTRUCTIVE interference on the mass side and DESTRUCTIVE on
the opposite side.

This happens when:
  (a) Paths to mass-side nodes sample LOWER field (less phase added)
  (b) Paths to opposite-side nodes sample HIGHER field (more phase added)
  (c) The LOWER phase addition aligns better with the field-free phase pattern

Condition (a) is backwards! The mass creates higher field on the
mass side, not lower. The spent-delay action S = dl - √(dl²-L²)
DECREASES with field (mass creates a phase VALLEY). So paths
through the mass region accumulate LESS phase.

### Step 7: On the lattice, the spent-delay action creates a
phase valley at the mass position. But the valley affects ALL
paths that pass near the mass equally (deterministic geometry).

The net effect: paths on the mass side ALL get reduced phase.
The reduction is the same for all of them (same y-positions).
The amplitude at mass-side detector nodes DECREASES because the
reduced phase changes the interference pattern → depletion.

### Step 8: To get attraction, different paths to the SAME
mass-side node must respond DIFFERENTLY to the phase valley.

This requires: some paths pass through the valley (reduced phase)
while others don't (normal phase). The paths that pass through
the valley contribute amplitude with a different phase than the
paths that don't. If the valley-phase paths CONSTRUCTIVELY
INTERFERE with the no-valley paths, the total amplitude at that
node INCREASES → attraction.

### Step 9: This requires LONG-RANGE transverse edges.

On the NN lattice, all paths to a given node pass through
similar y-positions (random walk with step ±1). There's no path
that BYPASSES the mass region to reach a mass-side detector node.

With LONG-RANGE edges (connecting to y±2 or y±3), a path can
jump OVER the mass region and reach the mass-side detector from
the other side. This "bypass" path doesn't pass through the
valley and has a different phase. The interference between
"through-valley" and "bypass" paths creates the constructive
interference that produces attraction.

### Step 10: But long-range edges destroy beam confinement.

If nodes connect to y±3, the beam spreads 3× faster → no distance law.

### Step 11: THE RESOLUTION: long-range edges ONLY near the beam center.

A tapered lattice where:
- Near y=0: full connectivity (y±1, y±2, y±3) → high multiplicity,
  path diversity, constructive interference
- Far from y=0: NN only (y±1) → low multiplicity, beam confined

This gives BOTH:
(a) Attraction: paths through and around the valley interfere
    constructively at mass-side nodes (from long-range edges near center)
(b) Distance law: beam confined by NN connectivity at edges
    (amplitude can't spread beyond the taper zone)

## Novel Prediction

**A tapered lattice with connectivity decreasing as |y| increases
should show BOTH gravity toward mass AND distance-dependent
deflection on the SAME graph.**

Specific prediction: on a 3D tapered NN lattice with:
- |y|<2: max_dy=3 (7 edges in y-direction)
- 2<|y|<4: max_dy=2 (5 edges)
- |y|>4: max_dy=1 (3 edges, standard NN)

At field strength 0.0001, mass at z=3:
- Gravity should be TOWARD mass (positive delta_z)
- |delta_z| should DECREASE with z_mass (distance law)

## Weakest Link

Step 9: the assumption that bypass paths create constructive
interference is not guaranteed. The bypass path has a very
different total length, which might make its phase completely
uncorrelated with the through-valley paths. If the phases are
random relative to each other, the interference averages to
zero (no effect), not constructive.

Test: measure the PHASE DISTRIBUTION of paths reaching a single
mass-side detector node on the tapered lattice, with and without
the mass field. If the field narrows the phase distribution
(aligns phases), that's constructive interference.

## Status
PROPOSED — test the tapered lattice prediction.
