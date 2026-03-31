# Hypothesis: Interference Pattern Geometry Sensitivity

## Date
2026-03-30

## Statement
The interference pattern's visibility (fringe contrast) in the two-slit setup depends quantitatively on network geometry parameters (grid width, slit separation), and this dependence reveals a continuous transition between interference-dominated and record-dominated regimes even within the model's existing binary record mechanism.

## Prediction
When `record_created=False` (coherent regime):
- The interference fringe contrast at the center detector (y=0) varies as a function of `phase_shift_upper`, tracing a sinusoidal-like response curve.
- The AMPLITUDE of this response curve (peak-to-trough) should depend on the ratio of path-length difference to total path length, which is controlled by slit separation and grid width.
- Specifically: wider grids (longer paths from source to detector) should show SHARPER interference fringes because the two paths have more opportunity to accumulate distinct phases.
- Narrower slit separation should REDUCE fringe contrast because the two paths become more similar.

When `record_created=True` (record regime):
- The center detector response should be FLAT as a function of `phase_shift_upper` (no interference).
- This should hold regardless of geometry parameters.

The RATIO of coherent-regime contrast to record-regime contrast as a function of geometry gives a quantitative "interference suppression strength."

## Falsification Criteria
- If the center detector response is already flat (no fringes) in the coherent regime at the default geometry, the setup is not actually producing interference and the claim needs re-examination.
- If the fringe contrast does NOT depend on geometry (same contrast at all grid widths and slit separations), the hypothesis is falsified — geometry doesn't matter and the binary record toggle is the whole story.
- If the record regime shows ANY phase-dependent variation, the record mechanism is leaking.

## Null Hypothesis
The interference pattern is entirely determined by the binary `record_created` flag and is insensitive to network geometry. The phase response curve has the same shape at all grid sizes and slit separations.

## Relevant Prior Work
- `two_slit_distribution()` in `toy_event_physics.py` (line 23141) — existing implementation with binary record toggle.
- `center_detector_phase_scan()` in `toy_event_physics.py` (line 23240) — scans phase but only at default geometry.
- No scripts or logs sweep geometry parameters for the two-slit setup.

## Proposed Experiments
1. Phase scan at default geometry (baseline): sweep `phase_shift_upper` from 0 to 2*pi, measure center detector probability, both with and without record.
2. Grid width sweep: repeat phase scan at widths 8, 12, 16, 20, 24. Measure fringe contrast at each.
3. Slit separation sweep: repeat phase scan at slit separations 2, 4, 6, 8. Measure fringe contrast at each.
4. Combined geometry map: 2D sweep of width x slit_separation, measuring fringe contrast. Identify the contour where contrast drops below 50% of maximum.

## Status
PROPOSED
