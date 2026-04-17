# Analysis: Barrier-Free Interference on Generated DAGs

## Date
2026-03-30

## Key Finding: The barrier is NOT essential scaffold

Strong interference (V > 0.5) appears on generated DAGs with NO blocked nodes and NO amplitude zeroing. The only hand-imposed element is a regional phase shift (upper vs lower y-half of crossing edges at one vertical cut). 18/20 seeds show V(y=0) > 0.06, with 12/20 showing V > 0.5.

## What was removed vs what remains

### Removed (no longer needed):
- Barrier blocking (amplitude zeroing at non-slit nodes)
- Slit positions (no specific slit y-coordinates)
- Slit width parameter
- Any node removal or topology modification

### Still imposed:
- Regional phase shift (upper vs lower y-region boundary)
- Position of the vertical cut (which layer to shift at)
- The phase_shift_upper value itself

### Endogenous:
- Graph topology (random DAG from local spawn rules)
- Path structure (which paths exist, how they contribute)
- Amplitude balance (determined by graph structure)
- Interference visibility (determined by amplitude balance)

## What determines interference strength (TEST 2)

The phase boundary position controls V by determining the amplitude balance. V is maximized when ~50% of crossing edges get the phase shift (balanced split). This is exactly the amp_ratio predictor from the earlier 30-seed study (r=0.93).

The boundary at y=-2 (129/219 upper crossings = 59%) gives V=0.945.
The boundary at y=+4 (44/219 upper crossings = 20%) gives V=0.070.

## Bottleneck is NOT essential (TEST 3)

V_bottleneck ≈ V_midpoint across 10 seeds. The natural sparse point adds no interference advantage over an arbitrary vertical cut. The graph is dense enough that every vertical cut has enough crossings for interference.

## Remaining scaffold: the regional phase shift

The phase shift is still hand-imposed. It represents the "which-path" information — analogous to a phase plate in optics. Removing it entirely would mean no phase-dependent observable, and visibility would trivially be zero (no phase to sweep).

The honest question: is the regional phase shift a reasonable model of how path-distinguishability could arise from graph dynamics? In the model's language, the phase shift is `e^(i*k*action)` where the action depends on the local delay field. If the delay field were asymmetric (e.g., from a persistent pattern above the path), paths through the upper region would naturally accumulate different phase than paths through the lower region — endogenous regional phase from gravity.

This connects to the GRAVITY result: persistent patterns create delay-field distortions that change the action along paths. This action change IS a natural phase shift. So the "hand-imposed phase shift" could be replaced by a persistent pattern's gravitational field, making the phase shift endogenous.

## Significance
The barrier has been eliminated. The remaining scaffold (regional phase shift) maps onto a known model mechanism (gravitational delay-field distortion from persistent patterns). The next step is to test whether a persistent pattern's delay field, applied to a generated DAG, produces interference-like phase sensitivity without ANY hand-imposed phase parameter.
