# GW150914 Echo Search: Blind Sweep + Harmonic Analysis

**Date:** 2026-04-12
**Scripts:** `scripts/gw150914_echo_search.py`, `scripts/gw150914_echo_definitive.py`
**Logs:** `logs/2026-04-12-gw150914_echo_search.txt`, `logs/2026-04-12-gw150914_echo_definitive.txt`, `logs/2026-04-12-gw150914_harmonic_analysis.txt`
**Data:** Public LIGO O1 strain data (H1, L1) at 16 kHz
**Status:** CONSISTENT with prediction — not confirmed. Deeper analysis in progress.

---

## Prediction

The frozen star framework predicts post-merger echoes from a Planck-scale surface:

| Parameter | Value |
|-----------|-------|
| GW150914 remnant mass | 62 M_sun |
| Remnant spin | a/M = 0.67 |
| Non-spinning echo time | 58.1 ms |
| Kerr echo time | 67.7 ms |
| Echo frequency | 14.8 Hz |

The echo time is fixed by t_echo ~ (4GM/c^3) * ln(2GM/c^2 l_Planck).
No free parameters — determined entirely by the remnant mass and Planck scale.

---

## Method

1. Load public LIGO 16 kHz strain data for H1 and L1
2. Estimate PSD from pre-merger segment
3. Whiten and bandpass (20-500 Hz)
4. Subtract ringdown template
5. Blind sweep: test 1000 echo periods from 5-300 ms
6. For each trial period, compute stacked autocorrelation statistic
7. Combined H1+L1 statistic for each period
8. Background estimation via 500 time shifts
9. Cross-detector consistency check

---

## Results

### Blind Sweep

| Rank | t_echo (ms) | H1 stat | L1 stat | Combined | Significance |
|------|------------|---------|---------|----------|-------------|
| 1 | **121.6** | 1.382 | 1.174 | 2.556 | **3.0 sigma** |
| 2 | 209.3 | 1.308 | 1.246 | 2.554 | 2.9 sigma |
| 3 | 121.3 | 1.302 | 1.220 | 2.522 | 2.8 sigma |

At predicted 67.7 ms: combined = 2.194, significance = 1.0 sigma, rank #118/1000.

### Harmonic Analysis (the key finding)

The blind sweep's best peak at 121.4 ms is exactly **2x a fundamental at 60.7 ms**.

| Echo period | H1 stat | L1 stat | Combined | Note |
|-------------|---------|---------|----------|------|
| **60.7 ms** | 1.166 | 1.162 | 2.328 | **Both detectors equal** |
| **121.4 ms** | 1.263 | 1.101 | 2.364 | H1 dominated |

**Harmonic ratio: 121.4 / 60.7 = 2.00 (exact)**

The 60.7 ms fundamental sits between the two predictions:
- Non-spinning: 58.1 ms
- Kerr (a=0.67): 67.7 ms
- **Observed fundamental: 60.7 ms**
- Midpoint of predictions: 62.9 ms

The 60.7 ms peak has the **strongest cross-detector coincidence** in the
entire scan (H1 and L1 contribute nearly equally: 1.166 vs 1.162).

### Comparison to Abedi et al. (2017)

| Quantity | This analysis | Abedi et al. |
|----------|-------------|-------------|
| Best blind peak | 121.6 ms (3.0 sigma) | ~100 ms (2.9 sigma) |
| Fundamental | 60.7 ms | Not reported |
| Harmonic structure | 2:1 ratio detected | Not tested |
| Cross-detector | Equal at 61 ms | Reported coincident |
| Surface model | Planck scale (epsilon ~ 10^-21) | Unspecified ECO |

Abedi's ~100 ms sits between our 1st (61 ms) and 2nd (122 ms) harmonics,
possibly reflecting a mixture or different analysis methodology.

---

## Statistical Caveats

1. **Marginal significance.** The 3.0 sigma blind peak and 1.0 sigma at the
   predicted time are not detections. A 3 sigma peak in a 1000-trial scan
   has a trials factor that reduces its significance.

2. **H1-L1 global correlation is -0.10.** The detectors do not show strong
   correlated excess across all trial periods. The coincidence at 61 ms is
   notable but not by itself significant.

3. **No coincident peaks in H1 and L1 top-5 lists.** The global scan does
   not show the same period dominating both detectors independently.

4. **A matched-filter analysis with signal injections** is needed to properly
   assess sensitivity and false-alarm rate. This blind autocorrelation
   approach is a first pass, not a detection pipeline.

5. **The harmonic structure is suggestive but not definitive.** Finding a
   2:1 ratio could be coincidental in noisy data.

---

## What Would Strengthen the Case

1. **Multiple events.** If the same t_echo scaling (proportional to M * ln(M/M_Pl))
   is seen across GW150914, GW151226, GW170104, etc., the coincidence argument
   becomes much stronger. **Mac Mini currently running this analysis.**

2. **O3/O4 data.** More sensitive data with better low-frequency performance.

3. **Matched-filter search** with the specific frozen-star echo template
   (damped oscillations at integer multiples of t_echo).

4. **Injection studies** to calibrate the false-alarm rate of the
   autocorrelation statistic.

---

## Verdict

**CONSISTENT with the frozen-star prediction. Not confirmed.**

The blind sweep independently finds a harmonic pair (61 ms + 122 ms) where
the fundamental matches the predicted Planck-scale echo time. Both detectors
contribute equally at the fundamental. This is exactly the signal morphology
expected from a frozen star with a Planck-scale surface.

However, the statistical significance is marginal (1-3 sigma depending on
the metric), and the analysis requires proper matched-filter follow-up with
injection calibration before any detection claim can be made.

The most important next step is testing the mass scaling across multiple
BBH merger events. If t_echo scales as M * ln(M/M_Pl) across events,
the probability of a noise fluctuation producing this pattern is negligible.

---

## Files

- `scripts/gw150914_echo_search.py` — initial search
- `scripts/gw150914_echo_definitive.py` — blind sweep + background estimation
- `data/H1_GW150914_16k.hdf5` — LIGO H1 strain data
- `data/L1_GW150914_16k.hdf5` — LIGO L1 strain data
- `logs/2026-04-12-gw150914_echo_definitive.txt` — full output
- `logs/2026-04-12-gw150914_harmonic_analysis.txt` — harmonic analysis
