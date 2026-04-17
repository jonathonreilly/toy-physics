# Analysis: Interference Geometry Sensitivity

## Date
2026-03-30

## Source
- Log: `logs/2026-03-30-interference-geometry-sweep.txt`
- Script: `scripts/interference_geometry_sweep.py`
- Hypothesis: `.claude/science/hypotheses/interference-geometry-sensitivity.md`

## Data Summary
- 48 geometry x record combinations tested (6 widths x 4 slit separations x 2 record modes)
- 24 phase steps per combination = 1,152 total probability evaluations
- 5 full screen distributions at selected geometries
- All runs completed successfully, no NaN or degenerate cases

## Key Findings

### Finding 1: PERFECT fringe contrast in coherent mode — geometry independent
**Every single coherent-mode geometry point shows contrast = 1.000000.**

This means the center detector probability sweeps from exactly 0 to some maximum as phase varies from 0 to 2*pi, regardless of grid width (8 to 28) or slit separation (4 to 16). The interference is COMPLETE at every geometry tested.

This **falsifies the hypothesis** that fringe contrast depends on network geometry. The null hypothesis holds: contrast is entirely determined by the binary record toggle, not by geometry.

### Finding 2: PERFECT suppression in record mode — geometry independent
**Every single record-mode geometry point shows contrast = 0.000000.**

The center detector probability is exactly flat (constant) as a function of phase shift when records are created. The record mechanism completely destroys phase sensitivity at all geometries.

### Finding 3: Absolute probability scales enormously with geometry
While contrast is geometry-independent, the ABSOLUTE unnormalized probability at the center detector varies by 30+ orders of magnitude across geometries:
- width=8, slit_sep=4: max ~ 1.66e4
- width=16, slit_sep=8: max ~ 1.43e7
- width=28, slit_sep=16: max ~ 1.63e32

This reflects the combinatorial explosion of paths on larger grids. But this scaling affects both the max and min of the phase curve proportionally, preserving contrast = 1.

### Finding 4: Distribution SHAPE changes dramatically with geometry
The full screen distributions reveal rich structure:

- **slit_sep=4 (narrow slits)**: Probability concentrates at screen EDGES (y=+-10: ~0.34), almost nothing at center (y=0: 0.0016). The two paths mostly "miss" the center.
- **slit_sep=16 (wide slits, close together)**: Probability concentrates at CENTER (y=0: 0.82). Nearly single-slit behavior since slits are close.
- **slit_sep=8 (moderate)**: Classic two-peaked structure near slit positions (y=+-9: ~0.15) with secondary peaks at center region. Clear interference fringe pattern.
- **width=8 (short grid)**: Edge-dominated, most probability at y=+-10.
- **width=28 (long grid)**: Smoother, more developed fringe pattern with clear secondary maxima.

So geometry DOES matter for the distribution shape — just not for the phase sensitivity at y=0.

### Finding 5: The model's interference is mathematically exact
The contrast = 1.000 result is not approximate — it's exact to floating-point precision. This means the model's path-sum produces PERFECT destructive interference at the center detector when the phase shift is pi, regardless of geometry. This is a structural property of the causal DAG, not a finite-size approximation.

## Statistical Summary
| Quantity | Value | Notes |
|----------|-------|-------|
| Coherent contrast (all geometries) | 1.000000 | Exact across all 24 parameter points |
| Record contrast (all geometries) | 0.000000 | Exact across all 24 parameter points |
| Contrast variance across geometries | 0.0 | No geometry dependence whatsoever |
| Probability scale range | ~1e4 to ~1e32 | Grows exponentially with grid size |

## Hypothesis Verdict
**REFUTED** — The hypothesis predicted that fringe contrast depends on geometry. It does not. The null hypothesis (geometry independence of contrast) is confirmed with exact precision across all 24 geometry points tested.

However, the experiment revealed something the hypothesis did not predict: the distribution SHAPE (which screen positions receive probability) depends strongly on geometry, even though the phase sensitivity at the center is always perfect. This is a new observation worth investigating.

## Follow-Up Recommendations

1. **Why is contrast exactly 1?** — Derive from model axioms why the path-sum always produces perfect destructive/constructive interference at the center, regardless of geometry. This is a structural property of the causal DAG that deserves a `/first-principles` derivation.

2. **Distribution shape as a function of geometry** — The shape changes (edge-peaked vs center-peaked vs multi-fringed) deserve their own sweep. What controls the number of fringe peaks? How does fringe spacing depend on slit separation?

3. **Partial record mechanisms** — Since the binary record toggle produces all-or-nothing suppression, explore PARTIAL record formation: what if only a fraction of paths create records? This would require a code modification to `two_slit_distribution()` to allow probabilistic record creation.

4. **Attenuation effects** — The `attenuation_power` parameter could create partial decoherence-like effects even without records. Sweep it.
