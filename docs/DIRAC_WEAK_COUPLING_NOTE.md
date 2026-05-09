# Dirac Weak Coupling Note

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/frontier_dirac_walk_3plus1d_weak_coupling_scan.py` exits 0 with PASS in the current cache; the prior audit verdict citing an unregistered artifact was generated against an earlier cache state and is invalidated by this source-note hash drift.

**Date:** 2026-04-10
**Scope:** periodic 3+1D Dirac v4 scan with weaker coupling and longer propagation at fixed dimensionless geometry.

This note records the results from
[`scripts/frontier_dirac_walk_3plus1d_weak_coupling_scan.py`](../scripts/frontier_dirac_walk_3plus1d_weak_coupling_scan.py).
The scan keeps the periodic v4 sign convention fixed, varies the coupling
downward, and lengthens propagation by increasing `N` while holding the
dimensionless controls `delta = d / n` and `lambda = L / n` fixed.

## Scan Grid

- mass: `m0 = 0.30`
- strengths: `5.0e-04`, `2.0e-04`, `1.0e-04`, `5.0e-05`
- sizes: `n = 17, 21, 25, 29`
- lambda targets: `0.40`, `0.55`, `0.70`
- delta targets: `0.10`, `0.14`, `0.18`, `0.22`

## Exact Measured Outcomes

The cross-strength totals were identical across the full sweep:

- stable delta rows: `6/12`
- positive-stable rows: `2/12`
- best signed delta-law fit: not available in any block
- best `|bias|` fit: `alpha = 4.413..4.414`, `R^2 = 0.8537`

Per lambda block, the sign-stable rows were:

- `lambda = 0.40`: `2/4`
- `lambda = 0.55`: `1/4`
- `lambda = 0.70`: `3/4`

The best `|bias|` fits by lambda were:

- `lambda = 0.40`: `alpha = 1.086..1.088`, `R^2 = 0.1290..0.1292`
- `lambda = 0.55`: `alpha = 2.810..2.811`, `R^2 = 0.5099..0.5100`
- `lambda = 0.70`: `alpha = 4.413..4.414`, `R^2 = 0.8537`

The baseline-to-weakest comparison from the scan was:

- baseline `strength = 5.0e-04`, `lambda = 0.40`: stable delta rows `2/4`, positive-stable rows `2/4`, `|bias|` fit `alpha = 1.088`, `R^2 = 0.1292`
- weakest `strength = 5.0e-05`, `lambda = 0.70`: stable delta rows `3/4`, positive-stable rows `0/4`, `|bias|` fit `alpha = 4.414`, `R^2 = 0.8537`

## Interpretation

The weaker-coupling sweep does **not** show a strength-driven rescue of the
remaining periodic Dirac gravity failures. The cross-strength sign-stability
counts are unchanged across all four couplings, and the signed delta-law fit
never becomes available because the rows still mix signs.

What *does* improve is the offset magnitude law at larger `lambda`. The
`|bias|` fit becomes much cleaner as propagation length increases, but that
looks like a geometry / recurrence effect rather than a coupling effect, since
the same fit family is essentially unchanged across the four strengths.

## Carry-Forward

- Keep the periodic v4 harness as the baseline comparison point.
- Treat larger `lambda` as the more useful knob for cleaning up the magnitude
  law.
- Do not promote weaker coupling as a general fix for the remaining sign
  failures without a separate geometry change.
