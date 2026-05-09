# Matched 2D vs 4D Decoherence Note

**Status:** support - structural or confirmatory support note
**Date:** 2026-04-03
**Purpose:** Test whether the current 4D decoherence claim survives a degree-matched comparison against the 2D modular family.
**Primary runner:** `scripts/matched_2d_4d_decoherence.py`


## Setup

- Same modular family on both sides
- Same slit/barrier and mass-selection rule
- Same `pur_min` metric
- Same `k`-band `[3, 5, 7]`
- 2D radius fixed at `3.0`
- 4D radius chosen per `N` to match the 2D mean degree as closely as possible on the same seed set
- `npl = 25`, `gap = 3.0`
- `N = [25, 40, 60, 80, 100]`
- `8` seeds

## Result

The matched comparison does **not** support a clean “4D flattens the ceiling” claim.

Measured mean `pur_min`:

| N | 2D `pur_min` | 2D `<k>` | 4D `pur_min` | 4D `<k>` | matched 4D `r` |
|---|---|---|---|---|---|
| 25 | 0.9341 | 9.76 | 0.9647 | 9.52 | 4.75 |
| 40 | 0.9577 | 9.98 | 0.9559 | 9.69 | 4.75 |
| 60 | 0.9555 | 10.11 | 0.9378 | 9.78 | 4.75 |
| 80 | 0.9667 | 10.24 | 0.9812 | 9.89 | 4.75 |
| 100 | 0.9428 | 10.25 | 0.9991 | 9.89 | 4.75 |

Per-seed exponent fit on `(1 - pur_min)`:

- 2D matched: `alpha = -0.158 ± 1.024`
- 4D matched: `alpha = -2.704 ± 0.620`
- `delta alpha (4D - 2D) = -2.546`

## Interpretation

- The current 4D claim is **not apples-to-apples** with the 2D baseline when we force a shared modular family and approximate degree matching.
- Dimension alone is **not** rescuing the ceiling in this matched pocket.
- The 4D large-`N` lane remains a real bounded regime, but its earlier “escape” framing should stay provisional unless it survives a broader matched sweep.

## Recommendation

- Keep the 4D modular lane as a bounded large-`N` candidate.
- Do not promote the current 4D exponent-flattening wording as a dimensional theorem.
- If we want a stronger dimensional claim, rerun with a wider matched radius grid and a larger seed count, or collapse the claim to the bounded-window statement only.
