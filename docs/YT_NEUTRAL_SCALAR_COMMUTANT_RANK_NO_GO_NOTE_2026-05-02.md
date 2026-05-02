# Neutral Scalar Commutant Rank No-Go

**Status:** exact negative boundary / neutral scalar commutant does not force rank-one purity  
**Runner:** `scripts/frontier_yt_neutral_scalar_commutant_rank_no_go.py`  
**Certificate:** `outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json`

## Purpose

The rank-one route would close the source-pole purity problem if current
symmetry and D17 data forced the neutral scalar response space to be
one-dimensional.  This note tests that symmetry-only route.

## Result

The rank-one theorem is not derived.  Two neutral scalar directions can carry
the same listed substrate/gauge labels, so the symmetry commutant still admits
a rank-two positive response family.  The runner keeps source-only `C_ss`
residue fixed while the canonical-Higgs overlap is not certified by symmetry
alone.

This strengthens the existing rank-one gate: D17/carrier support is useful,
but it is not a dynamical theorem that sets the orthogonal neutral scalar
response to zero.

## Claim Boundary

This is an exact negative boundary, not retained or proposed-retained closure.
It does not set `cos(theta)=1` or `kappa_s = 1`, does not treat D17 as
rank-one dynamics, and does not use `H_unit`, `yt_ward_identity`, observed
targets, `alpha_LM`, plaquette, or `u0`.

## Verification

```bash
python3 scripts/frontier_yt_neutral_scalar_commutant_rank_no_go.py
# SUMMARY: PASS=14 FAIL=0
```

Next action: derive a dynamical rank-one neutral scalar theorem, measure
`C_sH` / `C_HH` Gram purity, implement W/Z response with identity certificates,
or process seed-controlled FH/LSZ chunks.
