# Analysis: Self-Maintenance Rule Sweep

## Date
2026-03-30

## Key Findings

### 1. The model default (S={3,4} B={3,4}) produces NO stable fixed points
All 5 tested seed patterns either die or oscillate:
- 3×3 block → period-3 (9↔8↔5)
- 5-cross → period-3 (5↔9↔8)
- Line of 5 → DEAD by step 4
- 2×3 rectangle → DEAD by step 2
- Glider attempt → period-2

The model's "persistent patterns" under the default rule are OSCILLATORS, not static structures. This means the delay field sourced by these patterns also oscillates — the gravitational potential is time-varying on the scale of the pattern's period.

### 2. The most stability-productive rule is S={2,3,4,5} B={4}
4 out of 5 seeds produce stable fixed points:
- 3×3 block → stable at 8 nodes
- 5-cross → stable at 5 nodes
- 2×3 rectangle → stable at 6 nodes
- Glider attempt → stable at 3 nodes

This rule has broad survival (2-5 neighbors) but strict birth (exactly 4). It's the most conservative — easy to survive, hard to be born. The resulting patterns are compact (3-8 nodes).

### 3. Rule space bifurcation: narrow birth → stability, broad birth → explosion or death

| Birth breadth | Typical outcome |
|--------------|-----------------|
| {4} only | Stable fixed points (compact) |
| {3} only | Stable but larger (24 nodes) |
| {3,4} | Oscillating |
| {2,3} | Growing (fills grid) |
| {2} | Growing (fills grid) |

The birth threshold acts as a selection pressure: strict birth → few new nodes → stability. Permissive birth → many new nodes → explosive growth or chaotic dynamics.

### 4. Pattern size depends on rule, not seed
Under S={2,3,4,5} B={3}: three different seeds all converge to 24 nodes. Under S={2,3,4,5} B={4}: different seeds converge to different sizes (3-8). The rule determines the attractor size; the seed selects which attractor.

## Significance
The default rule produces oscillators, not fixed points. This means:
- The model's "persistent patterns" are dynamic structures that maintain their identity through periodic oscillation
- The delay field they source is time-varying (oscillates with the pattern's period)
- The gravity mechanism acts through a PULSATING potential, not a static one
- This is consistent with Axiom 2's wording ("self-maintaining patterns"), which doesn't require stationarity

The stability boundary in rule space is sharp: birth={4} vs birth={3,4} is the difference between fixed points and oscillators. This is a phase transition in the rule space.
