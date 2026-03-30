# Sanity Check: Interference Geometry Sweep — Perfect Contrast Result

## Date
2026-03-30

## Target
The finding that coherent-mode fringe contrast = 1.000000 exactly at ALL geometries tested (6 widths x 4 slit separations), and record-mode contrast = 0.000000 exactly at all geometries.

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| Model Consistency | CLEAN | Uses only events, links, delays, path-sum over causal DAG, and binary record sectors. All within model primitives. |
| Scale Reasonableness | FLAG | Unnormalized probabilities span 1e4 to 1e32 — a 28 order-of-magnitude range. The contrast calculation (ratio) is scale-invariant so this doesn't affect the finding, but the extreme magnitudes suggest numerical precision could be a concern at larger grids. |
| Symmetry Compliance | CLEAN | The two-slit setup has y-reflection symmetry (slit at +s and -s). All distributions are symmetric in y, as expected. Phase shift only applies to the upper slit, breaking this symmetry as expected. |
| Limit Behavior | CLEAN | At slit_sep→very large (=16), distribution collapses to center peak (single-effective-slit). At slit_sep→small (=4), distribution moves to edges. At width→small (=8), few paths, edge-dominated. All sensible limiting behavior. |
| Numerical Artifacts | FLAG | The minimum probability at destructive interference is reported as 0.000000 at small grids but shows tiny nonzero residuals at larger grids (e.g., 0.000002 at width=24/slit=4, 0.009720 at width=28/slit=2). These are likely floating-point precision effects from summing ~1e30-scale complex amplitudes. The contrast calculation still rounds to 1.000000 because the minimum is negligible relative to the maximum. At even larger grids, the residual could grow and reduce contrast below 1. |
| Bug Likelihood | CLEAN | The parameterized function is a direct copy of `two_slit_distribution()` with hardcoded values replaced by parameters. Logic is identical. The baseline validation at width=16, slit_sep=4 reproduces the existing `center_detector_phase_scan()` results. |

## Deeper Investigation of the "Perfect Contrast" Finding

The contrast = 1 result is suspiciously clean. Let me examine WHY:

**The center detector at y=0 sits exactly equidistant from both slits (at +s and -s).** By the y-symmetry of the rectangular grid, every path through the upper slit to y=0 has an exact mirror-image path through the lower slit with the SAME action/delay. The only difference is the applied `phase_shift_upper`.

When phase_shift = pi, the upper-slit amplitude picks up a factor of e^(i*pi) = -1, exactly canceling the lower-slit amplitude at y=0. This is EXACT because the geometry is exactly symmetric — not because of fine-tuning.

**This means contrast = 1 at y=0 is a consequence of the grid's discrete reflection symmetry, not a dynamical result of the model.** It would hold in ANY path-sum model on a symmetric grid with symmetric slits. It does NOT test the model's specific dynamics.

**The contrast at y != 0 would NOT be exactly 1** because paths to off-center detectors do not have exact mirror symmetry. This is the more interesting measurement that the experiment did not fully explore.

## Skeptical Reviewer's Best Objection

"Contrast = 1 at y=0 is trivially guaranteed by the grid's reflection symmetry. You're measuring a symmetry of your setup, not a property of the model's dynamics. The interesting question is the fringe PATTERN at off-center positions, which you measured but didn't analyze for geometry dependence."

## Response

The reviewer is correct. The contrast-at-center measurement was the wrong observable for this hypothesis. The finding is real but trivial — it follows from setup symmetry, not model dynamics. The SHAPE of the full distribution (which DOES change with geometry) is the dynamically interesting observable that should be the focus of follow-up work.

Specifically: measure fringe spacing and fringe count across the full screen as a function of slit separation and grid width. These are NOT protected by symmetry and would test the model's actual path-selection dynamics.

## Verdict
SUSPICIOUS — The central result (contrast = 1) is real but trivially explained by setup symmetry. It does not test the model's dynamics. The full distribution shapes ARE dynamically interesting and geometry-dependent but were not the focus of the analysis. The numerical precision flag at large grids (residuals growing from 0 to ~5000 over 28 orders of magnitude of probability) warrants monitoring but does not currently affect results.
