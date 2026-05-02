# Orthogonal Neutral Decoupling No-Go

**Status:** exact negative boundary / orthogonal neutral decoupling shortcut not derived  
**Runner:** `scripts/frontier_yt_orthogonal_neutral_decoupling_no_go.py`  
**Certificate:** `outputs/yt_orthogonal_neutral_decoupling_no_go_2026-05-02.json`

## Purpose

After the dynamical rank-one attempt failed, the next shortcut is to dismiss a
finite or heavy orthogonal neutral pole as harmless.  This note tests whether
the current PR #230 surface contains such a decoupling theorem.

## Result

It does not.  The runner constructs a same-source counterfamily in which the
source-created pole mass and source residue are fixed, the orthogonal neutral
mass is raised, and the canonical-Higgs overlap remains below one.  A finite
mass gap alone does not set `cos(theta)=1`, set the orthogonal top coupling to
zero, or identify the source pole with the canonical Higgs radial mode.

Decoupling would require a derived scaling theorem tying the overlap or
orthogonal top coupling to the heavy mass limit, same-surface `C_sH` / `C_HH`
Gram-purity data, or an accepted Higgs-identity certificate.

## Claim Boundary

This is an exact negative boundary, not retained or proposed-retained closure.
It does not set `kappa_s = 1`, does not use finite mass gaps as source-pole
purity, and does not use `H_unit`, `yt_ward_identity`, observed masses,
`alpha_LM`, plaquette, `u0`, or reduced pilots as proof selectors.

## Verification

```bash
python3 scripts/frontier_yt_orthogonal_neutral_decoupling_no_go.py
# SUMMARY: PASS=14 FAIL=0
```

Next action: derive a real decoupling-scaling theorem, measure `C_sH` /
`C_HH` Gram purity, derive a stronger source-Higgs identity theorem, implement
W/Z response with identity certificates, or process FH/LSZ chunks.
