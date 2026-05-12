# PR230 Source-Higgs Bridge Aperture Checkpoint

**Status:** bounded-support / source-Higgs bridge aperture checkpoint; current
surface remains open

**Runner:** `scripts/frontier_yt_pr230_source_higgs_bridge_aperture_checkpoint.py`

**Certificate:** `outputs/yt_pr230_source_higgs_bridge_aperture_checkpoint_2026-05-07.json`

```yaml
actual_current_surface_status: bounded-support / source-Higgs bridge aperture checkpoint; 63 completed C_sx/C_xx chunks do not close canonical O_H or C_sH/C_HH Gram flatness
conditional_surface_status: exact support if a future same-surface canonical O_H certificate, production C_ss/C_sH/C_HH pole rows, complete row/FV/IR authority, and Gram flatness land without forbidden imports
proposal_allowed: false
bare_retained_allowed: false
```

## Purpose

Block08 closed the current W/Z accepted-action shortcut.  This checkpoint asks
whether the highest-ranked source-Higgs route has become a real aperture using
the row evidence already present on disk.

The answer is no.  The current surface has useful two-source taste-radial row
staging, but it still lacks the non-shortcut source-Higgs bridge:

```text
certified O_H + production C_ss/C_sH/C_HH pole rows + Gram flatness.
```

## Result

The runner consumes existing certificates only and does not touch the live chunk
worker.

- The canonical `O_H` hard-residual gate remains open.
- The direct source-Higgs pole-row contract is exact support, but current
  production `C_sH/C_HH` rows are absent.
- The completed two-source taste-radial packet is now the complete contiguous
  `001-063` manifest packet.
- Those rows are still `C_sx/C_xx` second-source rows.  The row metadata marks
  them as not canonical `C_sH/C_HH`, with
  `canonical_higgs_operator_identity_passed=false` and
  `used_as_physical_yukawa_readout=false`.
- The combined measurement-row file is written, but it is finite
  `C_sx/C_xx` support only and not canonical `C_sH/C_HH` pole evidence.
- The time-kernel/GEVP and strict scalar-LSZ/FV gates remain support/boundary
  surfaces, not physical pole authority.
- The source-Higgs builder and Gram-purity postprocessor still have no
  production row certificate.

The current source-Higgs bridge therefore remains bounded support plus an exact
open boundary.  The 63 chunks are real staging evidence, but they do not close
canonical `O_H`, source-Higgs pole rows, or Gram flatness.

## Claim Boundary

This block does not claim retained or `proposed_retained` top-Yukawa closure.
It does not relabel `C_sx/C_xx` as `C_sH/C_HH` before `x=canonical O_H`, does
not set `kappa_s`, `c2`, `Z_match`, or any overlap to one, does not use
`yt_ward_identity`, `H_unit`, `y_t_bare`, observed targets, observed `g2`,
`alpha_LM`, plaquette, or `u0`, and does not treat W/Z response as closed after
block08.

## Exact Next Action

Continue only through a real missing artifact:

- same-surface canonical `O_H` plus production `C_ss/C_sH/C_HH` pole rows with
  Gram flatness;
- same-surface neutral primitive/rank-one authority; or
- W/Z physical-response rows with accepted action, sector-overlap, matched
  covariance, and strict non-observed `g2`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_source_higgs_bridge_aperture_checkpoint.py
python3 scripts/frontier_yt_pr230_source_higgs_bridge_aperture_checkpoint.py
# SUMMARY: PASS=19 FAIL=0
```
