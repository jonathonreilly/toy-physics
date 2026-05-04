# YT Schur K-Prime Row Absence Refresh

Date: 2026-05-04

PR: #230

Status: bounded support / refreshed absence guard; no closure proposal is
authorized.

## Purpose

The scalar-denominator / Schur `K'(pole)` route would be a real closure route
if PR #230 had same-surface neutral scalar kernel rows:

- `A(pole)`, `B(pole)`, `C(pole)`
- `A'(pole)`, `B'(pole)`, `C'(pole)`
- or equivalent precontracted Schur rows

The chunked FH/LSZ production campaign has now reached 46 ready L12 chunks, so
the Schur absence guard was rerun against the current larger output surface.

## Result

The refreshed guard scanned `93` current production/certificate files and
found `0` complete Schur row hits.

Verification:

```bash
python3 scripts/frontier_yt_schur_kprime_row_absence_guard.py
# SUMMARY: PASS=14 FAIL=0

python3 scripts/frontier_yt_schur_row_candidate_extraction_attempt.py
# SUMMARY: PASS=13 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=150 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=176 FAIL=0
```

The guard also keeps the finite-source-only counterfamily active: finite
`C_ss(q)`, `dE_top/ds`, and source-slope rows can agree while the Schur kernel
partition and `D_eff'(pole)` differ.  Therefore current FH/LSZ rows cannot be
reclassified as the missing `A/B/C` kernel rows.

## Claim Boundary

This refresh does not derive `K'(pole)`, scalar LSZ normalization,
source-Higgs overlap, `O_sp = O_H`, or physical `y_t`.

Forbidden shortcuts remain unused: `H_unit`, `yt_ward_identity`, observed top
mass or observed `y_t`, `alpha_LM`, plaquette/u0, `kappa_s=1`, `c2=1`,
`Z_match=1`, and `cos(theta)=1`.

Exact next action for this route: produce genuine same-surface Schur kernel
rows from a neutral scalar kernel theorem or measurement.  Otherwise use a
non-source rank-repair route: certified `O_H/C_sH/C_HH` pole rows, same-source
W/Z response rows with identity certificates, or a neutral-sector
irreducibility theorem.
