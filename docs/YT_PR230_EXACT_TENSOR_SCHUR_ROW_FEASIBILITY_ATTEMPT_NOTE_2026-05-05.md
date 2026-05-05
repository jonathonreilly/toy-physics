# PR230 Exact Tensor Schur Row Feasibility Attempt

```yaml
actual_current_surface_status: exact negative boundary / exact tensor Schur A/B/C row feasibility blocked on current PR230 surface
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_pr230_exact_tensor_schur_row_feasibility_attempt.py`
**Certificate:** `outputs/yt_pr230_exact_tensor_schur_row_feasibility_attempt_2026-05-05.json`

## Purpose

This block tests the exact tensor/PEPS version of the Schur route.  The
question is not whether exact tensor contraction is useful in principle.  It
is whether the current PR230 surface already defines enough structure for an
exact contraction to emit genuine same-surface Schur `A/B/C` kernel rows.

## Result

The attempt does not close.  Exact tensor contraction can evaluate a defined
finite tensor network, but it cannot define the missing row labels.  The
current surface still lacks:

- a neutral scalar kernel basis containing source and orthogonal directions;
- a source/orthogonal projector and normalization;
- definitions of `A(q)`, `B(q)`, and `C(q)`, or equivalent precontracted matrix
  Schur rows;
- contact/subtraction, threshold, finite-volume/IR, and limiting-order
  conventions for using those rows at the pole;
- a canonical bridge or neutral-sector irreducibility authority making the
  rows physical;
- a certified exact tensor/PEPS contraction of that defined row network.

The runner records a row-definition counterfamily: two finite Schur row
families match the same source-only tensor marginal on the sampled grid while
carrying different `A/B/C` rows.  This is the exact-tensor form of the current
blocker: without the row network and partition as same-surface input, the
method name does not supply row authority.

## Boundary

No retained or `proposed_retained` PR230 closure is claimed.  This block does
not write a Schur row file, does not use exact tensor/PEPS as a proof selector,
and does not import `H_unit`, Ward authority, observed targets,
`alpha_LM`/plaquette/`u0`, reduced pilots, unit `c2/Z_match/kappa_s`, or
PSLQ/value recognition.

## Next Positive Action

To make exact tensor/PEPS a positive Schur route, first define a same-surface
neutral scalar kernel basis and source/orthogonal projector, then emit
`A/B/C` or precontracted matrix Schur rows from a certified exact contraction.
If that cannot be supplied, the cleaner positive routes remain
`O_H/C_sH/C_HH` pole rows, same-source W/Z response rows with `g2` and identity
authority, strict scalar-LSZ moment/threshold/FV authority, or a
neutral-sector irreducibility certificate.

## Verification

```bash
python3 scripts/frontier_yt_pr230_exact_tensor_schur_row_feasibility_attempt.py
# SUMMARY: PASS=18 FAIL=0

python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=21 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=77 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=225 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=256 FAIL=0
```
