# Neutral Scalar Rank-One Purity Gate

**Status:** open / neutral scalar rank-one purity gate not passed  
**Runner:** `scripts/frontier_yt_neutral_scalar_rank_one_purity_gate.py`  
**Certificate:** `outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json`

## Purpose

A direct positive route to source-pole purity would be a retained theorem that
the neutral scalar response space is rank one.  In that case the source-created
neutral scalar pole could not mix with an orthogonal top-coupled scalar, and
the source-pole readout would be the canonical Higgs readout.

## Result

The gate is not passed.  Current D17/carrier support is not a dynamical
rank-one theorem for the neutral scalar response Hilbert space.  The current
surface still has the exact blockers already exposed by the PR #230 loop:

- no selection rule forbids an orthogonal neutral scalar with top coupling;
- source-pole mixing remains a live countermodel;
- source-only pole data do not determine source-Higgs overlap;
- `C_sH` / `C_HH` Gram purity is not measured;
- the same-source W/Z response certificate gate is not passed.

The runner records a rank-two witness in which the same listed charges and D17
carrier label can be preserved while the source pole mixes with an orthogonal
neutral scalar and changes the source-pole readout.

## Claim Boundary

This is an open purity gate, not retained or proposed-retained closure.  It
does not treat D17 carrier support as source-pole purity, does not set
`cos(theta)=1`, does not set the orthogonal top coupling to zero, and does not
set `kappa_s = 1`.

## Verification

```bash
python3 scripts/frontier_yt_neutral_scalar_rank_one_purity_gate.py
# SUMMARY: PASS=12 FAIL=0
```

Next action: derive the rank-one neutral-scalar response theorem, measure
`C_sH` / `C_HH` Gram purity, implement the W/Z response certificate route, or
continue seed-controlled FH/LSZ production.
