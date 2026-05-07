## Summary

This physics-loop block resumes PR #230's neutral transfer/eigenoperator
campaign after block01's exact source-mixing no-go.  It pivots to the requested
canonical `O_H` / source-Higgs bridge and W/Z accepted-action response routes.

The block lands an exact support/boundary certificate: the strict common root
vertex for both priority pivots is a non-shortcut same-surface canonical
`O_H` / accepted EW-Higgs action certificate.  Existing source-Higgs and W/Z
contracts remain support only.

## Claim Boundary

Actual current-surface status is exact support/boundary.  `proposal_allowed`
is false.  This PR does not claim retained or `proposed_retained` closure.

It does not identify `C_sx/C_xx` with `C_sH/C_HH`, does not use formal GEVP
smoke as pole authority, does not use `H_unit`, `yt_ward_identity`, observed
targets, `alpha_LM`, plaquette, `u0`, or unit conventions for `kappa_s`,
`c2`, `Z_match`, or `g2`, and did not touch the live chunk worker.

## Artifacts

- `scripts/frontier_yt_pr230_canonical_oh_wz_common_action_cut.py`
- `outputs/yt_pr230_canonical_oh_wz_common_action_cut_2026-05-07.json`
- `docs/YT_PR230_CANONICAL_OH_WZ_COMMON_ACTION_CUT_NOTE_2026-05-07.md`
- `.claude/science/physics-loops/pr230-neutral-transfer-eigenoperator-oh/`

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_canonical_oh_wz_common_action_cut.py
python3 scripts/frontier_yt_pr230_canonical_oh_wz_common_action_cut.py
# SUMMARY: PASS=10 FAIL=0
```

## Next Action

Attack the common root vertex directly: derive or supply a non-shortcut
same-surface canonical `O_H` / accepted EW-Higgs action certificate.  If it
lands, fork to production `C_ss/C_sH/C_HH` rows or W/Z response/covariance /
strict-`g2` rows on that accepted action.
