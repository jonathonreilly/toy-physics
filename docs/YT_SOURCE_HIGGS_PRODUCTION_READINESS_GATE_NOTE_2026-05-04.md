# PR #230 Source-Higgs Production Readiness Gate

```yaml
actual_current_surface_status: open / source-Higgs production launch blocked by missing O_H certificate
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_source_higgs_production_readiness_gate.py`  
**Certificate:** `outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json`

## Purpose

The highest-ranked non-MC route for PR #230 remains the source-Higgs
Gram-purity test:

```text
Res(C_sH)^2 = Res(C_ss) Res(C_HH)
```

That route requires a same-surface canonical-Higgs operator `O_H` plus
production `C_sH/C_HH` rows.  The production harness already has a guarded,
default-off source-Higgs row path, but it requires
`--source-higgs-operator-certificate`.  The completed FH/LSZ chunks were not
launched with such a certificate, and the newer two-source taste-radial rows
use the schema fields as explicit `C_sx/C_xx` aliases, not canonical
`C_sH/C_HH` rows.

This gate records that boundary.  It does not launch jobs, modify the live
production harness, write source-Higgs rows, or treat current FH/LSZ or
taste-radial chunks as canonical `C_sH/C_HH` evidence.

## Result

The completed chunk scan now filters for numeric chunk indices only, so the
combined L12 summary is not counted as an extra production chunk.  It scans
the `63` landed FH/LSZ chunks and shows their source-Higgs metadata is marked
`absent_guarded`, with no canonical-Higgs operator certificate, no
source-Higgs modes/noises, and no `C_sH/C_HH` rows.  Therefore the current
chunk wave cannot by itself close the `O_sp/O_H` blocker.

The gate now also scans the completed two-source taste-radial row artifacts.
It currently scans chunks001-014.  Those chunks do contain finite mode rows in
the source-Higgs schema, but the artifact metadata marks them as `C_sx/C_xx`
second-source aliases with
`canonical_higgs_operator_identity_passed=false`, zero pole-residue rows, and
`used_as_physical_yukawa_readout=false`.  They are bounded support for the
two-source route, not canonical source-Higgs production evidence.

The gate also records the future launch surface: after a valid same-surface
`O_H` certificate exists, a separate source-Higgs production chunk can run with
`--source-higgs-cross-modes`, `--source-higgs-cross-noises`, and
`--source-higgs-operator-certificate`, then feed the pole-residue extractor,
source-Higgs builder, Gram-purity postprocessor, retained-route certificate,
and campaign-status certificate.

## Validation

```text
python3 scripts/frontier_yt_source_higgs_production_readiness_gate.py
# SUMMARY: PASS=25 FAIL=0
```

## Boundary

This is launch-readiness bookkeeping only.  It does not define `O_H`, does not
promote `C_sx/C_xx` aliases into canonical `C_sH/C_HH`, does not use `H_unit`
or static EW algebra as a substitute, does not use `yt_ward_identity`,
observed targets, `alpha_LM`, plaquette, or `u0`, and does not authorize
retained or `proposed_retained` wording.

Next action: derive or supply the same-surface canonical-Higgs operator
certificate, then run a separate source-Higgs production chunk and pass the
existing row, pole-residue, Gram-purity, retained-route, and campaign gates.
