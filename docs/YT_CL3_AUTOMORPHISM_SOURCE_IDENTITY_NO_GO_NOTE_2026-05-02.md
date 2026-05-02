# PR #230 Cl(3)/Z3 Automorphism Source-Identity No-Go

**Status:** exact negative boundary / Cl3 automorphism data not source-Higgs identity  
**Runner:** `scripts/frontier_yt_cl3_automorphism_source_identity_no_go.py`  
**Certificate:** `outputs/yt_cl3_automorphism_source_identity_no_go_2026-05-02.json`

## Result

Finite Cl(3)/Z3 source-orbit and automorphism data do not derive the missing
PR #230 source-to-canonical-Higgs / LSZ normalization.

The runner keeps the finite substrate data fixed:

- Cl(3) generator norms;
- Z3 translation orbit size;
- signed-permutation orbit size;
- D17 single scalar carrier count;
- source-coordinate unit;
- neutral scalar-source quantum numbers.

Across that same finite-orbit surface, the continuous pole data still vary:

- source overlap `Z_s`;
- inverse-propagator derivative `D'(pole)`;
- same-source pole residue;
- canonical response factor.

## Verification

```bash
python3 scripts/frontier_yt_cl3_automorphism_source_identity_no_go.py
# SUMMARY: PASS=10 FAIL=0
```

## Claim Boundary

This is not retained or proposed-retained `y_t` closure.  It says finite
substrate orbit data are structural support only.  They cannot replace:

- a microscopic scalar denominator theorem;
- a source-pole purity theorem;
- a same-source pole-residue measurement;
- a canonical-Higgs identity certificate.

It also does not license `kappa_s = 1`, `Z_match = 1`, `c2 = 1`, an `H_unit`
readout, `yt_ward_identity` authority, observed top mass/yukawa proof
selection, or alpha/plaquette/u0 proof input.

