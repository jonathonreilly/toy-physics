# PR230 Neutral Rank-One Bypass Post-Block37 Audit

**Status:** support / exact negative boundary on the current PR230 surface

**Runner:** `scripts/frontier_yt_pr230_neutral_rank_one_bypass_post_block37_audit.py`

**Certificate:**
`outputs/yt_pr230_neutral_rank_one_bypass_post_block37_audit_2026-05-12.json`

```yaml
actual_current_surface_status: exact negative boundary / post-Block37 neutral rank-one bypass not closed on the current PR230 surface
conditional_surface_status: conditional-support if a future same-surface neutral transfer, off-diagonal generator, primitive-cone certificate, strict C_ss/C_sH/C_HH pole rows, or strict W/Z physical-response packet lands
proposal_allowed: false
bare_retained_allowed: false
```

## Inputs Checked

This block is the next lane-1 physics-loop move after the action-premise
boundary in
[YT_PR230_LANE1_ACTION_PREMISE_DERIVATION_ATTEMPT_NOTE_2026-05-12.md](YT_PR230_LANE1_ACTION_PREMISE_DERIVATION_ATTEMPT_NOTE_2026-05-12.md).
It checks the completed taste-radial packet in
[YT_PR230_TWO_SOURCE_TASTE_RADIAL_ROW_COMBINER_GATE_NOTE_2026-05-06.md](YT_PR230_TWO_SOURCE_TASTE_RADIAL_ROW_COMBINER_GATE_NOTE_2026-05-06.md),
the top bare-mass response harness in
[YT_PR230_TOP_MASS_SCAN_RESPONSE_HARNESS_GATE_NOTE_2026-05-12.md](YT_PR230_TOP_MASS_SCAN_RESPONSE_HARNESS_GATE_NOTE_2026-05-12.md),
the neutral transfer/source-mixing boundary in
[YT_PR230_NEUTRAL_TRANSFER_EIGENOPERATOR_SOURCE_MIXING_NO_GO_NOTE_2026-05-07.md](YT_PR230_NEUTRAL_TRANSFER_EIGENOPERATOR_SOURCE_MIXING_NO_GO_NOTE_2026-05-07.md),
the rank-one closure attempt in
[YT_PR230_DERIVED_BRIDGE_RANK_ONE_CLOSURE_ATTEMPT_NOTE_2026-05-05.md](YT_PR230_DERIVED_BRIDGE_RANK_ONE_CLOSURE_ATTEMPT_NOTE_2026-05-05.md),
the primitive-route completion gate in
[YT_PR230_NEUTRAL_PRIMITIVE_ROUTE_COMPLETION_NOTE_2026-05-06.md](YT_PR230_NEUTRAL_PRIMITIVE_ROUTE_COMPLETION_NOTE_2026-05-06.md),
the multiplicity-one gate and candidate attempt in
[YT_PR230_SAME_SURFACE_NEUTRAL_MULTIPLICITY_ONE_GATE_NOTE_2026-05-07.md](YT_PR230_SAME_SURFACE_NEUTRAL_MULTIPLICITY_ONE_GATE_NOTE_2026-05-07.md)
and
[YT_PR230_SAME_SURFACE_NEUTRAL_MULTIPLICITY_ONE_CANDIDATE_ATTEMPT_NOTE_2026-05-07.md](YT_PR230_SAME_SURFACE_NEUTRAL_MULTIPLICITY_ONE_CANDIDATE_ATTEMPT_NOTE_2026-05-07.md),
and the hard-residual equivalence gate in
[YT_PR230_CANONICAL_OH_HARD_RESIDUAL_EQUIVALENCE_GATE_NOTE_2026-05-07.md](YT_PR230_CANONICAL_OH_HARD_RESIDUAL_EQUIVALENCE_GATE_NOTE_2026-05-07.md).

## Purpose

After Block37, the best remaining non-chunk route was a true bypass:

```text
source/taste-radial rows + neutral-sector structure
=> unique neutral scalar pole
=> source pole is the physical Higgs readout
```

If that worked, the route would avoid adopting a separate canonical `O_H`
action.  This block asks whether the current post-Block37 PR230 surface
already supplies that rank-one theorem.

## Result

It does not.  The current surface has:

- complete finite `C_ss/C_sx/C_xx` taste-radial rows;
- top bare-mass response schema support;
- conditional Perron/rank-one support theorems;
- exact contracts for primitive-cone and multiplicity-one certificates.

It still lacks:

- same-surface physical neutral transfer or off-diagonal generator;
- primitive-cone / irreducibility certificate;
- canonical scalar LSZ/FV/IR metric;
- strict `C_ss/C_sH/C_HH` pole-overlap rows;
- strict W/Z physical-response rows and `g2` authority.

## Counterfamily

The runner uses the actual combined row means for the zero mode and extends
the measured source/taste-radial subblock to a three-direction neutral space:

```text
source_s, taste_radial_x, orthogonal_neutral_n
```

The measured `C_ss`, `C_sx`, and `C_xx` entries are held fixed.  The would-be
Higgs readout is allowed to rotate as

```text
H(theta) = cos(theta) x + sin(theta) n
```

with the unmeasured entries `C_sn = C_xn = 0` and a positive `C_nn`.  All
current rows and the top bare-mass response support stay unchanged, while the
candidate source-Higgs overlap varies across the family.  Therefore the
current finite rows do not force neutral rank one.

## Boundary

This is a current-surface boundary, not a permanent no-go against the bypass.
It retires if a future artifact supplies one of:

1. same-surface physical neutral transfer or off-diagonal generator;
2. primitive-cone / irreducibility certificate;
3. strict `C_ss/C_sH/C_HH` pole-overlap rows with LSZ/FV/IR authority;
4. strict W/Z physical-response packet with matched covariance and `g2`
   authority.

## Non-Claims

This block does not claim retained or `proposed_retained` y_t closure.  It does
not identify the taste-radial axis with canonical `O_H`, does not relabel
`C_sx/C_xx` as `C_sH/C_HH`, does not treat top bare-mass response as Higgs
response, does not turn positivity into a primitive cone, and does not use
`H_unit`, `yt_ward_identity`, `y_t_bare`, observed targets, `alpha_LM`,
plaquette, `u0`, or unit-overlap conventions.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_neutral_rank_one_bypass_post_block37_audit.py
python3 scripts/frontier_yt_pr230_neutral_rank_one_bypass_post_block37_audit.py
# SUMMARY: PASS=12 FAIL=0
```
