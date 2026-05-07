# PR230 Orthogonal-Neutral Top-Coupling Exclusion Candidate Gate

**Status:** exact negative boundary / candidate rejected on the current PR230
surface

## Purpose

The same-surface neutral multiplicity-one candidate can be repaired by a
genuine selection rule excluding top coupling for the orthogonal neutral
singlet.  This block checks whether the current post-FMS support, finite
two-source taste-radial rows, or primitive-cone support now supplies that
selection rule.

## Result

It does not.

The current finite `C_sx/C_xx` rows are source/complement correlator rows, not
top-coupling tomography.  Their finite off-diagonal entries and positive
finite `C_ss/C_sx/C_xx` blocks support the two-source row program, but they do
not measure or null the top coupling of an orthogonal neutral scalar.

The post-FMS counterfamily still applies: at fixed measured source response,
different canonical `y_t` values are compatible with finite orthogonal
neutral top couplings.  Current same-surface charges and labels also still do
not distinguish a Higgs radial scalar from an orthogonal neutral scalar in a
way that allows `h tbar t` while forbidding `chi tbar t`.

## Non-Claim

This does not claim retained or `proposed_retained` closure.  It does not set
the orthogonal top coupling to zero, does not treat `C_sx/C_xx` as
`C_sH/C_HH`, and does not set `kappa_s`, `c2`, or `Z_match` to one.

## Verification

```bash
python3 scripts/frontier_yt_pr230_orthogonal_top_coupling_exclusion_candidate_gate.py
# SUMMARY: PASS=12 FAIL=0
```

## Exact Next Action

Supply a same-surface charge/representation theorem that forbids orthogonal
neutral top couplings while allowing the Higgs radial top coupling, or
measure/source-Higgs-purify the orthogonal component through real
`C_spH/C_HH` or W/Z response rows.
