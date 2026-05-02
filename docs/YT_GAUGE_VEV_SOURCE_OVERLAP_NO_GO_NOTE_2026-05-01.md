# PR #230 Gauge-VEV Source-Overlap No-Go

**Status:** exact negative boundary / gauge-VEV source-overlap no-go  
**Runner:** `scripts/frontier_yt_gauge_vev_source_overlap_no_go.py`  
**Certificate:** `outputs/yt_gauge_vev_source_overlap_no_go_2026-05-01.json`

## Question

Can the canonical electroweak VEV or gauge-boson mass normalization fix the
overlap between the Cl(3)/Z3 scalar source `s` and the canonical Higgs field
`h`?

## Result

No.  The gauge sector fixes the metric of an already-identified canonical
Higgs field.  It does not identify the additive lattice scalar source with
that field.

The runner constructs countermodels with identical:

```text
v_canonical
g_ew
m_W
canonical y_h
```

but different source overlap:

```text
h = kappa_s s
```

Changing `kappa_s` changes `dE/ds` and changes the physical `dE/dh` that would
be inferred if `kappa_s` were set to one.  The VEV/gauge-mass surface therefore
cannot replace scalar LSZ residue or same-source production pole data.

## Claim Boundary

```text
proposal_allowed: false
```

This blocks a shortcut only.  It does not derive `kappa_s`, does not use
`H_unit`, and does not supply production evidence.

## Exact Next Action

Fix `kappa_s` through a same-source scalar pole residue measurement/theorem, or
continue the production FH/LSZ route.  Do not identify the substrate source
with the canonical Higgs field from `v` alone.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_gauge_vev_source_overlap_no_go.py
python3 scripts/frontier_yt_gauge_vev_source_overlap_no_go.py
# SUMMARY: PASS=8 FAIL=0
```
