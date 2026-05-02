# Taste-Singlet Ladder Normalization Boundary

**Date:** 2026-05-01
**Status:** exact negative boundary / taste-singlet normalization removes finite ladder crossings
**Runner:** `scripts/frontier_yt_taste_singlet_ladder_normalization_boundary.py`
**Certificate:** `outputs/yt_taste_singlet_ladder_normalization_boundary_2026-05-01.json`

## Purpose

The zero-mode-removed color-singlet ladder search found four finite
`lambda_max >= 1` witnesses, and the taste-corner obstruction showed those
witnesses are dominated by the 16 Brillouin-zone taste corners.  This block
checks the constructive taste-singlet normalization candidate: if the scalar
carrier is a normalized singlet over those corners, each scalar-source vertex
carries `1/sqrt(N_taste)`, so the ladder eigenvalue scales by `1/N_taste`.

## Result

```text
python3 scripts/frontier_yt_taste_singlet_ladder_normalization_boundary.py
# SUMMARY: PASS=6 FAIL=0
```

With `N_taste = 16`, every finite crossing witness drops below threshold:

| Witness | Raw `lambda_max` | Taste-singlet normalized `lambda_max` |
|---|---:|---:|
| `N=4`, `m=0.20`, local | `7.07678273075` | `0.442298920672` |
| `N=6`, `m=0.20`, local | `1.48744308139` | `0.0929651925869` |
| `N=4`, `m=0.30`, local | `1.46336779249` | `0.0914604870307` |
| `N=4`, `m=0.20`, point-split normalized | `2.39129631249` | `0.149456019531` |

The raw crossing range is `[1.46336779249, 7.07678273075]`; the normalized
range is `[0.0914604870307, 0.442298920672]`.  The raw-to-normalized ratio is
exactly `16` for all four rows.

## Claim Boundary

This is not retained or proposed-retained top-Yukawa closure.  It does not
derive the scalar taste/projector normalization, the interacting scalar pole,
or the inverse-propagator derivative.  It shows that the finite ladder
crossings depend on an unfixed taste normalization: the unnormalized taste
multiplicity is load-bearing.

The remaining route is narrower: derive the scalar taste/projector
normalization from the `Cl(3)/Z^3` source functional together with the
interacting color-singlet pole derivative, or measure the same-source pole
residue in production FH/LSZ data.
