# Sanity Check: Off-Center Fringe Visibility

## Date
2026-03-30

## Target
The finding that off-center fringe visibility V(y≠0) depends on network geometry with two monotonic trends (increases with width, decreases with slit separation) and a sharp threshold below which visibility drops to exactly zero.

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| Model Consistency | CLEAN | Uses only events, links, causal DAG path-sum, and record sectors. All grid geometry parameters are properties of the network structure. No external concepts imported. |
| Scale Reasonableness | CLEAN | Visibility is a ratio (0 to 1), scale-invariant. Values span the full range from 0.000 to 1.000 in sensible patterns. No extreme magnitudes in the final observable. |
| Symmetry Compliance | CLEAN | V(y) profiles are symmetric around y=0 in every case, as required by the slit setup's reflection symmetry. Off-center positions have no additional symmetry protection, so V(y≠0) < 1 is expected and observed. |
| Limit Behavior | CLEAN | At width→small (8): only center has visibility (narrow path diversity). At slit_sep→0 (=4, smallest): broad visibility (paths nearly coincide, similar phase). At slit_sep→large (=16): visibility concentrates at center (paths diverge maximally). All sensible. |
| Numerical Artifacts | CLEAN | Visibility zeros are EXACT zeros, not precision artifacts — they occur where only one path reaches the detector position (through one slit), so there IS no second path to interfere with. This is a topological property of the grid, not a numerical one. The nonzero values (0.001 to 0.997) are smooth and monotonic, no noise or jitter. |
| Bug Likelihood | CLEAN | Script imports the parameterized function from the first sweep (which was baseline-validated against the existing `center_detector_phase_scan()`). The off-center logic is identical — just evaluating at y≠0 instead of y=0. No new code paths to harbor bugs. |

## Deeper Analysis

### Why does the sharp visibility threshold exist?

When width/slit_sep is too small, the grid geometry means paths from source→slit→off-center-detector only have viable routes through ONE slit (the closer one). With only one contributing path, there's no second amplitude to interfere with, so V=0 exactly. This isn't a bug or precision issue — it's a TOPOLOGICAL property of the discrete grid. As width/slit_sep increases, paths through BOTH slits can reach the off-center detector, and interference appears.

This is actually interesting: the model has a discrete geometry where the number of interfering paths changes discontinuously with geometry parameters. This is a distinctly network-like feature that has no direct analogue in continuous space.

### Is the monotonicity trivially guaranteed?

No. In a continuous-space double slit, fringe visibility at a fixed off-axis angle does NOT monotonically increase with screen distance — it oscillates (fringe maxima and minima alternate). The monotonic increase we see here is a property of the DISCRETE grid, not of interference in general. More paths contributing at larger width smoothly increases contrast rather than creating oscillation.

### Could this be an artifact of the grid's regular structure?

Worth investigating. A rectangular grid with unit spacing creates a very regular path structure. An irregular or random network might show different behavior. But for the regular grid, the result appears genuine.

## Skeptical Reviewer's Best Objection

"Your monotonic trends might be an artifact of the rectangular grid's extreme regularity. In a less symmetric network, the clean monotonicity could break down. You've characterized a property of rectangular grids, not a general property of discrete event networks."

## Response

Fair point. The result IS specific to rectangular grids so far. However:
1. The model's axioms don't require a rectangular grid — any network topology is valid.
2. The finding still establishes that geometry-dependent interference IS a property of the model.
3. Whether it persists on irregular networks is a testable follow-up, not an invalidation of this result.
4. The sharp visibility threshold (topological origin) should be robust to grid irregularity since it depends on path EXISTENCE, not path regularity.

## Verdict
**CLEAN** — All six checks pass. The result is genuine, not a symmetry artifact or numerical issue. The two monotonic trends and the sharp threshold are dynamical properties of the model's path-sum on discrete grids. The reviewer's concern about grid regularity is valid but is a scope limitation, not an invalidation.
