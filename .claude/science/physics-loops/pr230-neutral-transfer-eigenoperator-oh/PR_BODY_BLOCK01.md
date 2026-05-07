# Summary

This physics-loop block attacks the PR #230 neutral transfer/eigenoperator
primitive route for the missing `O_H/C_sH/C_HH` bridge.  It lands an exact
negative boundary: the current same-surface Z3/taste eigenoperator primitives
do not certify a physical neutral scalar transfer or canonical `O_H` bridge.

# Science Result

- Adds a runner/certificate showing that the current symmetric taste-polynomial
  Z3-invariant sector contains orthogonal source identity and degree-one
  taste-radial axes in the same trivial Z3 sector.
- Exhibits two positive self-adjoint source-radial kernels compatible with
  current symmetry data: one has zero source-radial bridge while preserving the
  radial eigenoperator, and one has nonzero bridge while breaking radial
  eigenoperator purity.
- Shows that lazy-triplet primitivity does not imply full source-plus-triplet
  primitivity; a new `eta` source-triplet coupling is required and is not
  supplied by current PR230 artifacts.

# Claim Boundary

This PR does not claim retained or `proposed_retained` closure.  It does not
identify taste-radial `x` with canonical `O_H`, does not relabel `C_sx/C_xx`
as `C_sH/C_HH`, and does not import Ward/top, observed, plaquette/u0, unit
normalization, gauge-Perron, entropy, or Markov-laziness shortcuts.

# Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_neutral_transfer_eigenoperator_source_mixing_no_go.py
python3 scripts/frontier_yt_pr230_neutral_transfer_eigenoperator_source_mixing_no_go.py
# SUMMARY: PASS=18 FAIL=0
python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=93 FAIL=0
python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=154 FAIL=0
python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=308 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=341 FAIL=0
```

# Review

Local review-loop pass completed.  The review accepted the exact
negative-boundary claim after two narrow fixes: load-bearing dependency links
were added to the theorem note, and the sector wording was narrowed to the
current symmetric taste-polynomial sector.
