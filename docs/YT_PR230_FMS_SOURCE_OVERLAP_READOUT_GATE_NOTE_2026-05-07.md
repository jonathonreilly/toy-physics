# PR230 FMS Source-Overlap Readout Gate

Date: 2026-05-07

Status: exact-support / FMS source-overlap readout gate; no current PR230
closure

Runner:
`scripts/frontier_yt_pr230_fms_source_overlap_readout_gate.py`

Certificate:
`outputs/yt_pr230_fms_source_overlap_readout_gate_2026-05-07.json`

```yaml
actual_current_surface_status: exact-support / FMS source-overlap readout gate; action, canonical O_H, and strict C_ss/C_sH/C_HH pole rows absent on current PR230 surface
conditional_surface_status: readout support if a future accepted same-surface FMS/EW-Higgs action, canonical O_H certificate, and accepted C_ss/C_sH/C_HH pole rows exist
proposal_allowed: false
bare_retained_allowed: false
```

## Readout

Block19 made the FMS `O_H` candidate/action packet explicit.  This gate
connects that packet to the exact residue readout that would fix the remaining
source-to-canonical-Higgs overlap:

```text
kappa_sH = Res(C_sH) / sqrt(Res(C_ss) Res(C_HH))
```

The formula is invariant under scalar-source coordinate rescaling once the
accepted pole rows exist.  It also shows why the current source-only readout is
not enough: a fixed same-source response can be reproduced with different
canonical `y_H` values by changing the orthogonal neutral coupling unless
`Res(C_sH)` and Gram purity are supplied by rows or a theorem.

## Current Boundary

The readout is not executable on the current surface:

- the FMS packet is not an accepted same-surface action;
- canonical `O_H` is absent;
- strict `C_ss/C_sH/C_HH` pole rows are absent;
- the source-Higgs time-kernel manifest is support only and no closure rows
  were launched;
- aggregate retained-route and campaign gates still deny proposal wording.

## Claim Boundary

This block does not claim retained or `proposed_retained` top-Yukawa closure.
It does not set `kappa_s`, `c2`, `Z_match`, or `g2` to one.  It does not infer
`Res(C_sH)` from source-only rows, FMS `C_HH`, taste-radial `C_sx/C_xx` rows,
or literature.  It does not use `H_unit`, `yt_ward_identity`, observed targets,
observed W/Z or `g2`, `alpha_LM`, plaquette, `u0`, reduced pilots, or value
recognition as proof authority.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_fms_source_overlap_readout_gate.py
python3 scripts/frontier_yt_pr230_fms_source_overlap_readout_gate.py
# SUMMARY: PASS=15 FAIL=0
```
