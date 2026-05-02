# PR #230 FH/LSZ Finite-Volume Pole-Saturation Obstruction

**Status:** exact negative boundary / FH-LSZ finite-volume pole-saturation obstruction
**Runner:** `scripts/frontier_yt_fh_lsz_finite_volume_pole_saturation_obstruction.py`
**Certificate:** `outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json`

## Claim

Finite-volume discreteness is not scalar pole saturation.  The runner builds
positive finite-shell models at `L=12,16,24` with near-pole continuum levels
whose gap closes like `1/L^2`.  The pole-residue lower bound remains zero.

## Boundary

This blocks using a finite-L pole witness as the missing scalar LSZ theorem.
A retained route still needs a uniform spectral gap, pole-saturation theorem,
continuum-threshold certificate, production acceptance certificate, or
microscopic scalar denominator theorem.

## Verification

```bash
python3 scripts/frontier_yt_fh_lsz_finite_volume_pole_saturation_obstruction.py
# SUMMARY: PASS=7 FAIL=0
```
