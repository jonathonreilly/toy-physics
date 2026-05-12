# PR230 Neutral Primitive H3/H4 Aperture Checkpoint

**Status:** bounded-support / neutral primitive H3/H4 aperture checkpoint;
current surface remains open

**Claim type:** open_gate

**Runner:** `scripts/frontier_yt_pr230_neutral_primitive_h3h4_aperture_checkpoint.py`

**Certificate:** `outputs/yt_pr230_neutral_primitive_h3h4_aperture_checkpoint_2026-05-07.json`

```yaml
actual_current_surface_status: bounded-support / neutral primitive H3/H4 aperture checkpoint; H1/H2 support and 63 C_sx/C_xx chunks do not supply physical neutral transfer or source-canonical-Higgs coupling
conditional_surface_status: exact support if a future same-surface primitive neutral transfer or off-diagonal generator certificate supplies H3 and a canonical O_H/source-Higgs or W/Z physical-response packet supplies H4 without forbidden imports
proposal_allowed: false
bare_retained_allowed: false
```

## Purpose

Block09 left the highest-ranked source-Higgs bridge open: the current branch
still has no certified canonical `O_H`, no production `C_sH/C_HH` pole rows,
and no Gram-flat source-Higgs packet.  This block therefore pivots to the next
ranked primitive/rank-one route and asks whether the current Z3 support plus
the completed two-source taste-radial rows can now supply the remaining H3/H4
premises.

They cannot.

## Result

The runner consumes existing certificates and row summaries only.  It does not
touch or relaunch the live chunk worker.

What is genuinely present:

- H1 same-surface Z3 taste-triplet support is loaded.
- H2 positive-cone equal-magnitude support is loaded.
- The two-source taste-radial row combiner now sees the complete contiguous
  `001-063` packet.
- The finite `C_ss/C_sx/C_xx` diagnostics are schema-clean bounded staging
  evidence.

What remains absent:

- H3 physical neutral transfer or off-diagonal generator.
- A strict primitive-cone, irreducibility, or neutral rank-one certificate.
- H4 coupling to the PR230 source/canonical-Higgs sector.
- Certified canonical `O_H`, production `C_sH/C_HH` rows, or source-Higgs Gram
  flatness.
- W/Z physical-response rows with accepted action, sector overlap, matched
  covariance, and strict non-observed `g2`.

The finite `C_sx/C_xx` rows are covariance/correlator evidence, not a transfer
or action matrix.  The current finite-row Gram determinants are positive, so
they also do not give a finite rank-one flatness certificate.  Promoting those
rows to H3 would import the missing transfer theorem.

## Claim Boundary

This block does not claim retained or `proposed_retained` closure.  It does
not treat H1/H2 Z3 support as a physical transfer, does not relabel
`C_sx/C_xx` as `C_sH/C_HH`, does not identify taste-radial `x` as canonical
`O_H`, does not set `kappa_s`, `c2`, `Z_match`, `g2`, or overlaps to one, does
not use `H_unit`, `yt_ward_identity`, `y_t_bare`, observed targets, observed
`g2`, `alpha_LM`, plaquette, or `u0`, and does not touch the live chunk
worker.

## Exact Next Action

Pivot to a real missing artifact:

- W/Z physical-response rows with accepted action, sector overlap, matched
  covariance, and strict non-observed `g2`; or
- a fresh same-surface canonical `O_H` plus production `C_ss/C_sH/C_HH`
  Gram-flat row packet.

Do not reopen the neutral primitive route without a same-surface H3/H4
certificate.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_neutral_primitive_h3h4_aperture_checkpoint.py
python3 scripts/frontier_yt_pr230_neutral_primitive_h3h4_aperture_checkpoint.py
# SUMMARY: PASS=9 FAIL=0
```

Refresh note: the 2026-05-12 runner now accepts the complete current row packet
as support-only.  At this checkpoint it consumes `ready=63/63` with
`combined_rows_written=true` rather than the earlier partial prefixes; the
H3/H4 boundary is unchanged.
