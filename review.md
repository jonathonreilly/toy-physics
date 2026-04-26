# Codex Review: `claude/relaxed-wu-a56584`

**Date:** 2026-04-26
**Branch tip reviewed:** `1eaf0160b928f16f97f9b1d55affeb70d423be7a`
**Verdict:** Not ready to land as retained unconditional Planck Target 3 closure.

The new Schur/cubic-bivector algebra is useful object-level structure, and the
new runners pass. The remaining problem is claim strength: the branch still
promotes interpretive/source-normalization moves to retained closure.

Verified:

```bash
python3 scripts/frontier_planck_target3_schur_source_coupling_identity.py
# PASS=34, FAIL=0

python3 scripts/frontier_planck_target3_cubic_bivector_schur_source_principle.py
# PASS=42, FAIL=0

python3 scripts/frontier_planck_target3_gauss_flux_first_order_carrier.py
# PASS=41, FAIL=0

python3 scripts/frontier_planck_target3_forced_coframe_response.py
# PASS=54, FAIL=0

python3 -m py_compile \
  scripts/frontier_planck_target3_schur_source_coupling_identity.py \
  scripts/frontier_planck_target3_cubic_bivector_schur_source_principle.py \
  scripts/frontier_planck_target3_gauss_flux_first_order_carrier.py \
  scripts/frontier_planck_target3_forced_coframe_response.py
```

## Findings

### [P1] `H_first` orbit does not derive the boundary-source selector

File: `docs/PLANCK_TARGET3_SCHUR_SOURCE_COUPLING_IDENTITY_THEOREM_NOTE_2026-04-26.md`
Lines: 82-103

This proves that powers of the chosen uniform first-order operator
`H_first = sum gamma_a` keep the source-free vacuum inside `HW=0+HW=1`.
It does not show that the retained gravitational boundary source must be
this vacuum orbit. The retained `Cl_4` surface still allows other Clifford
words, and the companion Schur theorem verifies that the Hodge-dual `P_3`
packet has the same Schur spectrum. So `P_1` over `P_3` remains selected
only after adopting this source-action reading, not derived as a retained
source principle.

### [P1] Runner assumes the physical source-coupling normalization

File: `scripts/frontier_planck_target3_schur_source_coupling_identity.py`
Lines: 418-448

The runner computes `Tr(chi_eta rho Phi)=1` from the Schur spectrum, then
imposes the disputed physical identification
`Tr(chi_eta rho Phi)=4 c_cell G_Newton,lat` and solves for
`G_Newton,lat`. That identity is not certified from a retained boundary-
source theorem here; it is the exact load-bearing bridge the review asked to
derive. The upstream source-unit note is explicitly a support theorem on the
conditional Planck packet, so this remains a support/control calculation
rather than an unconditional retained closure verifier.

### [P2] Bridge note still carries live conditional wording

File: `docs/PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md`
Lines: 4-21

The note is re-headed as unconditional, but the same header block and
purpose section still state that the bridge is conditional on the
metric-compatible coframe-response premise plus gravitational-boundary
carrier identification, and that retained `Cl(3)/Z^3` does not by itself
prove the active block carries that response. That leaves the package
surface internally mixed even before the source-coupling issue above.

## Recommended Treatment

Keep this branch scoped as a Planck consequence/control packet and
boundary-source no-go/control surface, not retained unconditional Target 3
closure.

To promote it, a retained theorem still needs to:

- derive why the gravitational boundary source is the `H_first` vacuum orbit
  or otherwise select `P_1` over the Hodge-dual `P_3`;
- derive the physical coupling normalization
  `Tr(chi_eta rho Phi)=4 c_cell G_Newton,lat` from accepted retained
  boundary-source content;
- align the bridge/status notes and publication/control-plane surfaces so
  they do not mix conditional and unconditional readings of the same lane.
