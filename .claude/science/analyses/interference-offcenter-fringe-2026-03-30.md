# Analysis: Off-Center Fringe Visibility

## Date
2026-03-30

## Source
- Log: `logs/2026-03-30-interference-offcenter-fringe-sweep.txt`
- Script: `scripts/interference_offcenter_fringe_sweep.py`

## Data Summary
- 20 geometry points (5 widths x 4 slit separations) x 2 record modes = 40 configurations
- 21 screen positions per configuration (-10 to +10)
- 24 phase steps per screen position
- Total: 40 x 21 x 24 = 20,160 probability evaluations
- All completed, no failures.

## Key Findings

### Finding 1: Off-center visibility IS geometry-dependent (hypothesis now SUPPORTED)

Unlike center visibility (always 1.0), off-center visibility varies dramatically with geometry. The KEY TEST table shows this clearly at y=1:

| width | slit_sep=4 | slit_sep=8 | slit_sep=12 | slit_sep=16 |
|-------|-----------|-----------|------------|------------|
| 8 | 0.929 | 0.000 | 0.000 | 0.000 |
| 12 | 0.980 | 0.927 | 0.000 | 0.000 |
| 16 | 0.991 | 0.963 | 0.926 | 0.000 |
| 20 | 0.995 | 0.978 | 0.955 | 0.925 |
| 24 | 0.997 | 0.986 | 0.971 | 0.952 |

**The geometry dependence is NOT a symmetry artifact.** These off-center positions have no reflection-symmetry protection.

### Finding 2: Two independent monotonic trends

**Trend A — Width effect:** At fixed slit separation, visibility at any off-center position INCREASES with grid width. Example at y=1, slit_sep=8: 0.000 → 0.927 → 0.963 → 0.978 → 0.986 as width goes 8→12→16→20→24.

**Trend B — Slit separation effect:** At fixed width, visibility at any off-center position DECREASES with slit separation. Example at y=3, width=24: 0.674 → 0.458 → 0.239 → 0.110 as slit_sep goes 4→8→12→16.

Both trends are monotonic across the entire tested range with zero exceptions.

### Finding 3: Visibility has a characteristic spatial profile — bell-shaped around center

For every geometry, V(y) forms a bell-shaped envelope centered on y=0 that decays toward the screen edges. The HALF-WIDTH of this bell depends on geometry:

- Narrow slits (sep=4), wide grid (width=24): bell extends to screen edges (V(y=10)=0.337)
- Wide slits (sep=16), narrow grid (width=8): only y=0 has any visibility (delta function)
- The transition from "delta" to "broad bell" is controlled by the ratio width/slit_sep

### Finding 4: There appears to be a visibility threshold — a critical width/slit_sep ratio

Below a certain width/slit_sep ratio, off-center visibility drops to EXACTLY zero (not just small — zero). The boundary is sharp:

| slit_sep | First width with V(y=1) > 0 | Ratio |
|----------|----------------------------|-------|
| 4 | 8 | 2.0 |
| 8 | 12 | 1.5 |
| 12 | 16 | 1.33 |
| 16 | 20 | 1.25 |

This suggests a critical ratio around width/slit_sep ≈ 1.25-2.0 below which off-center interference visibility vanishes entirely. This is a quantitative, falsifiable, geometry-dependent result that is NOT protected by symmetry.

### Finding 5: Record mode remains perfectly suppressive

Record mode gives V = 0.0000000000 at ALL screen positions, ALL geometries. The record mechanism doesn't just kill center interference — it kills interference everywhere, at every position, with no leakage at the 10-digit level.

### Finding 6: Mean visibility grows monotonically with width

| width | slit_sep=4 | slit_sep=8 | slit_sep=12 | slit_sep=16 |
|-------|-----------|-----------|------------|------------|
| 8 | 0.153 | 0.048 | 0.048 | 0.048 |
| 12 | 0.253 | 0.159 | 0.048 | 0.048 |
| 16 | 0.372 | 0.205 | 0.158 | 0.048 |
| 20 | 0.482 | 0.246 | 0.195 | 0.158 |
| 24 | 0.572 | 0.288 | 0.228 | 0.191 |

Every column increases monotonically downward. Wider grids = more screen positions participate in interference = higher mean visibility. The model's path-sum spreads phase sensitivity over more of the detector screen as the network grows.

## Hypothesis Verdict
**SUPPORTED** — Off-center fringe visibility depends quantitatively on network geometry, with two clean monotonic trends (width and slit separation) and a sharp visibility threshold. This is a genuine dynamical property of the model's path-selection rules, not a symmetry artifact.

## Follow-Up Recommendations
1. **Pin down the critical ratio** — Finer sweep around width/slit_sep ≈ 1.0-2.5 to determine the exact threshold.
2. **Functional form** — Does V(y) follow a known envelope (Gaussian, Lorentzian, sinc²)? Fit it.
3. **Derive from axioms** — Use `/first-principles` to derive why wider grids spread visibility. The mechanism should involve path count or path-length diversity.
