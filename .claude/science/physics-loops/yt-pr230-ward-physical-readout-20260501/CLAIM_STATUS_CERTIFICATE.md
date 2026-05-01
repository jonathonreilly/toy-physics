# Claim Status Certificate

**Block:** `yt-pr230-ward-physical-readout-20260501`  
**Artifacts:** global proof audit, Ward repair audit, operator-matching
candidate, source/Higgs SSB bridge reduction, kappa residue obstruction, scalar
LSZ residue bridge obstruction, chirality selector support, and common dressing
obstruction, current-surface scalar pole-residue no-go, retained-closure route
certificate, direct-measurement scale requirements, key-blocker closure
attempt, scalar source two-point stretch, stuck fan-out, HS/RPA pole-condition
attempt, scalar ladder-kernel scout, scalar ladder kernel input audit,
scalar ladder projector-normalization obstruction, HQET direct-route
requirements, static mass matching obstruction, Legendre kappa gauge-freedom
obstruction, free scalar two-point pole absence, same-1PI scalar-pole
boundary, campaign status certificate, and scalar ladder IR zero-mode
obstruction, and heavy kinetic-mass route scout
plus nonzero-momentum correlator scout
and momentum harness extension certificate
and heavy kinetic matching obstruction
and momentum pilot scaling certificate
**PR:** #230 draft branch

```yaml
actual_current_surface_status: open / exact-support plus exact negative boundaries
conditional_surface_status: "Tree-level normalizations meet at 1/sqrt(6) if the physical-readout bridges are repaired; scalar source curvature and scalar/gauge kinematics are exact support but still lack interacting projector, pole-residue, common-dressing, and heavy-mass matching theorems."
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Open imports remain: scalar projector/source normalization, scalar-channel ladder kernel/eigenvalue crossing, scalar carrier, scalar LSZ residue, chirality selector, common dressing, and HQET/static heavy-mass matching."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

Allowed wording:

- exact negative boundary on hidden-proof inventory;
- open repair map for Ward physical readout;
- conditional-support operator-matching candidate;
- bounded-support scalar source curvature and ladder-kernel scout;
- exact-support input audit for reusable staggered/Wilson formulae;
- exact negative boundary for scalar source/projector normalization shortcut;
- route requirement / no-go for HQET as a zero-import absolute-mass shortcut;
- exact negative boundary for static residual-mass matching without an
  independent physical matching condition;
- exact negative boundary for selecting `kappa_H` from the Legendre transform
  alone;
- exact negative boundary for extracting a scalar pole from the free logdet
  source bubble alone;
- exact negative boundary for using same-1PI/four-fermion coefficient equality
  as a scalar LSZ/Yukawa readout;
- exact negative boundary for using a finite scalar ladder eigenvalue crossing
  before the IR/zero-mode and finite-volume limiting theorem is derived;
- bounded-support heavy kinetic-mass route using nonzero-momentum energy
  splittings, still requiring production data and matching;
- bounded-support nonzero-momentum correlator scout on a tiny cold gauge field;
- bounded-support production-harness extension for momentum modes, validated
  only by a reduced-scope smoke certificate;
- exact negative boundary for using kinetic energy splittings as SM top mass
  without deriving `c2` and lattice-to-SM matching;
- bounded-support momentum-enabled cold pilot with large finite-volume drift;
- PR #230 remains draft and not retained.

Forbidden wording:

- retained top-Yukawa closure;
- proposed-retained Ward theorem;
- audit-clean `y_t` derivation;
- any sentence implying the old `H_unit` matrix-element readout is now allowed.

Verification:

```bash
PYTHONPATH=scripts python3 scripts/frontier_yt_pr230_global_proof_audit.py
# SUMMARY: PASS=9 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_ward_physical_readout_repair_audit.py
# SUMMARY: PASS=12 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_ward_operator_matching_candidate.py
# SUMMARY: PASS=9 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_source_higgs_legendre_ssb_bridge.py
# SUMMARY: PASS=7 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_source_higgs_kappa_residue_obstruction.py
# SUMMARY: PASS=7 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_scalar_lsz_residue_bridge.py
# SUMMARY: PASS=6 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_chirality_selector_bridge.py
# SUMMARY: PASS=8 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_common_dressing_obstruction.py
# SUMMARY: PASS=6 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_scalar_pole_residue_current_surface_no_go.py
# SUMMARY: PASS=7 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=9 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_direct_measurement_scale_requirements.py
# SUMMARY: PASS=7 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_key_blocker_closure_attempt.py
# SUMMARY: PASS=14 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_scalar_source_two_point_stretch.py
# SUMMARY: PASS=12 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_scalar_residue_stuck_fanout.py
# SUMMARY: PASS=6 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_hs_rpa_pole_condition_attempt.py
# SUMMARY: PASS=9 FAIL=0

python3 scripts/frontier_yt_scalar_ladder_kernel_scout.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_scalar_ladder_kernel_input_audit.py
# SUMMARY: PASS=9 FAIL=0

python3 scripts/frontier_yt_scalar_ladder_projector_normalization_obstruction.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_hqet_direct_route_requirements.py
# SUMMARY: PASS=7 FAIL=0

python3 scripts/frontier_yt_static_mass_matching_obstruction.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_legendre_kappa_gauge_freedom.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_free_scalar_two_point_pole_absence.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_same_1pi_scalar_pole_boundary.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=14 FAIL=0

python3 scripts/frontier_yt_scalar_ladder_ir_zero_mode_obstruction.py
# SUMMARY: PASS=7 FAIL=0

python3 scripts/frontier_yt_heavy_kinetic_mass_route.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_nonzero_momentum_correlator_scout.py
# SUMMARY: PASS=7 FAIL=0

python3 scripts/frontier_yt_momentum_harness_extension_certificate.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_heavy_kinetic_matching_obstruction.py
# SUMMARY: PASS=5 FAIL=0

python3 scripts/frontier_yt_momentum_pilot_scaling_certificate.py
# SUMMARY: PASS=6 FAIL=0
```
