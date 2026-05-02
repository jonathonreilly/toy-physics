# Neutral Scalar Dynamical Rank-One Closure Attempt

**Status:** exact negative boundary / dynamical rank-one neutral scalar theorem not derived  
**Runner:** `scripts/frontier_yt_neutral_scalar_dynamical_rank_one_closure_attempt.py`  
**Certificate:** `outputs/yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json`

## Purpose

After the commutant no-go, the next possible source-pole purity route is a
dynamical theorem: perhaps the current PR #230 surface forces the neutral
scalar response itself to be rank one, even though symmetry labels do not.
This note tests that stronger route.

## Result

The dynamical rank-one theorem is not derived on the current surface.  A
positive two-pole neutral scalar family keeps the source-created pole mass,
source residue, and source-only readout fixed while a finite orthogonal
neutral pole remains.  Across that family the canonical-Higgs overlap with the
source pole varies, so the same source-pole data do not certify physical
canonical-Higgs purity.

This is a stronger blocker than the symmetry-only commutant no-go.  It says
that the current loaded certificates do not remove the finite orthogonal
neutral pole dynamically either.  A future positive route must supply an
actual rank-one dynamical theorem, same-surface `C_sH` / `C_HH` Gram-purity
data, or an equivalent accepted Higgs-identity certificate.

## Claim Boundary

This is an exact negative boundary, not retained or proposed-retained closure.
It does not set `kappa_s = 1`, `cos(theta)=1`, `c2 = 1`, or `Z_match = 1`, and
does not use `H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`,
plaquette, `u0`, or reduced pilots as proof selectors.

## Verification

```bash
python3 scripts/frontier_yt_neutral_scalar_dynamical_rank_one_closure_attempt.py
# SUMMARY: PASS=17 FAIL=0
```

Next action: measure `C_sH` / `C_HH` Gram purity, derive a genuine dynamical
rank-one theorem, implement W/Z response with identity certificates, or process
seed-controlled FH/LSZ chunks.
