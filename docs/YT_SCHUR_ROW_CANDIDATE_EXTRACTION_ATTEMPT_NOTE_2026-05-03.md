# YT Schur Row Candidate Extraction Attempt

```yaml
actual_current_surface_status: exact negative boundary / Schur row candidate extraction from finite ladder support
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_schur_row_candidate_extraction_attempt.py`
**Certificate:** `outputs/yt_schur_row_candidate_extraction_attempt_2026-05-03.json`

## Purpose

The Schur row contract gate names the future row file needed by the
`K'(pole)` route:

```text
outputs/yt_schur_scalar_kernel_rows_2026-05-03.json
```

This block checks whether the nearest current support artifacts already supply
those rows: the finite scalar-ladder scan, the eigen-derivative gate, the
total-momentum derivative scout, and the Feshbach response boundary.

## Result

They do not.  The eigen-derivative gate has a finite toy `M0_at_pole` matrix
and derivative examples, but no certified source/orthogonal neutral kernel
partition and no `A_prime/B_prime/C_prime` block rows.  The derivative scout
has finite `d lambda_max / d p_hat^2` proxies, but those are
prescription-sensitive finite scouts, not Schur rows.  The ladder scan gives
lambda crossings under simplified projector/IR choices.  Feshbach response
preservation is exact support for already defined operators, not a microscopic
scalar kernel partition.

```bash
python3 scripts/frontier_yt_schur_row_candidate_extraction_attempt.py
# SUMMARY: PASS=13 FAIL=0
```

## Boundary

This block does not write
`outputs/yt_schur_scalar_kernel_rows_2026-05-03.json`, does not claim retained
or `proposed_retained` closure, and does not turn source-only or finite-ladder
support into physical `y_t`.

The next positive action remains genuine same-surface Schur kernel rows with
partition, pole-control, and firewall certificates, or a pivot to certified
`O_H/C_sH/C_HH` pole rows or same-source W/Z response rows.
