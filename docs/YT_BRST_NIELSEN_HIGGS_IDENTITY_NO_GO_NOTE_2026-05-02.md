# PR #230 BRST/Nielsen Higgs-Identity No-Go

**Status:** exact negative boundary / BRST-Nielsen identities not Higgs-pole identity  
**Runner:** `scripts/frontier_yt_brst_nielsen_higgs_identity_no_go.py`  
**Certificate:** `outputs/yt_brst_nielsen_higgs_identity_no_go_2026-05-02.json`

## Result

BRST, Slavnov-Taylor, and Nielsen-style gauge identities do not close the PR
#230 source-to-canonical-Higgs bridge.

The runner constructs a neutral-scalar witness family where the gauge identity
surface is held fixed:

- BRST/ST residuals are zero;
- physical pole gauge-parameter derivative is zero;
- W/Z mass algebra and Goldstone gauge-parameter bookkeeping are fixed;
- the scalar pole spectrum is fixed.

Across that same gauge-identity surface, the PR #230 source operator rotates as

```text
O_s(theta) = cos(theta) h + sin(theta) chi
```

where `h` is the canonical Higgs radial mode and `chi` is an orthogonal neutral
scalar.  The source overlap, same-source top response, and same-source gauge
response vary while the gauge identities remain unchanged.

## Verification

```bash
python3 scripts/frontier_yt_brst_nielsen_higgs_identity_no_go.py
# SUMMARY: PASS=9 FAIL=0
```

## Claim Boundary

This is not retained or proposed-retained `y_t` closure.  It forbids using
BRST/ST/Nielsen identities as a substitute for:

- a microscopic scalar source-pole identity;
- a same-source pole-residue measurement;
- a source-pole purity theorem;
- a certificate that the measured source pole is the canonical Higgs radial
  mode used by `v`.

It also does not license `kappa_s = 1`, `Z_match = 1`, `c2 = 1`, an `H_unit`
readout, `yt_ward_identity` authority, observed top mass/yukawa proof
selection, or alpha/plaquette/u0 proof input.

