# Matched 2D vs 4D Decoherence Note

**Status:** support — bounded comparison note. Honest narrowing 2026-05-10:
the claim is the bounded numerical-replay statement on the explicitly
named generator definitions below. No upstream "modular family"
abstraction is being imported as an audited authority.
**Date:** 2026-04-03 (note); 2026-05-10 (rigorization sync)
**Purpose:** Test whether the current 4D decoherence claim survives a degree-matched comparison against the 2D modular family **as defined by the generator routines below**.
**Primary runner:** `scripts/matched_2d_4d_decoherence.py`

## One-hop generator dependencies (explicit)

The runner imports two graph generators directly:

- `generate_modular_dag` from `scripts/topology_families.py` — 2D
  hierarchical/modular DAG generator. The exact 2D family used here is
  the one defined by that function at the runner's pinned arguments
  (`radius=3.0`, `gap=3.0`, `npl=25`, seed range as enumerated in the runner).
- `generate_4d_modular_dag` from `scripts/four_d_decoherence_large_n.py`
  — 4D modular DAG generator. The exact 4D family used here is the one
  defined by that function at the per-`N` matched radius `r = 4.75`
  (selected from a sweep grid against the 2D mean degree).

These two source files are the bounded definitions of the "modular
family" referenced in the comparison. The note's claim is **not** an
abstract universality statement about modular DAGs; it is a bounded
numerical statement about the specific output of these two generator
routines on this harness, with the same slit/barrier convention,
mass-selection rule, `pur_min` metric, and `k`-band on both sides.


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
