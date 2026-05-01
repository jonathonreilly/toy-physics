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
and momentum pilot scaling certificate plus assumption/import stress and free
staggered kinetic-coefficient support plus interacting kinetic background
sensitivity plus scalar LSZ normalization cancellation plus Feshbach
operator-response boundary plus bridge-stack import audit, scalar spectral
saturation no-go, large-Nc pole-dominance boundary, and production resource
projection plus Feynman-Hellmann source-response route
and reduced mass-response bracket certificate plus source-reparametrization
gauge no-go plus canonical scalar-normalization import audit
plus source-to-Higgs LSZ closure attempt
plus scalar-source response harness extension
plus Feynman-Hellmann production protocol certificate
plus same-source scalar two-point LSZ measurement primitive
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
- open assumption/import stress certificate forbidding shortcut imports;
- exact support for the free Wilson-staggered kinetic coefficient, not
  interacting closure;
- bounded-support interacting kinetic background sensitivity; free `c2` is not
  an interacting stand-in without ensemble evidence or a theorem;
- conditional-support scalar LSZ normalization cancellation; source-scaling
  covariance works only if the interacting denominator and residue are derived
  together;
- exact-support Feshbach operator-response boundary; exact projection preserves
  responses but does not equate distinct scalar and gauge residues;
- refreshed retained-closure route certificate; strict production/matching and
  microscopic scalar residue/common-dressing remain the shortest honest routes;
- exact negative boundary for the existing bridge stack as PR230 closure;
  transport support imports accepted endpoints/surfaces and is not a direct
  y_t proof;
- exact negative boundary for scalar spectral saturation from positivity and
  low-order curvature alone;
- exact negative boundary for large-`N_c` pole dominance as finite-`N_c=3`
  closure;
- bounded-support production resource projection; the direct route is a
  concrete planned multi-day compute campaign, not a 12-hour foreground
  production certificate;
- bounded-support Feynman-Hellmann source-response route; additive rest mass
  can cancel in top-energy slopes, but scalar source-to-Higgs normalization and
  production response data remain open;
- bounded-support reduced mass-response bracket; existing correlator data show
  positive `dE/dm_bare`, but this is not production `dE/dh` evidence;
- exact negative boundary for source-only analytic closure under scalar-source
  reparametrization; canonical scalar normalization remains required;
- exact negative boundary that existing EW/Higgs structural notes do not hide a
  retained PR230 source-to-canonical-Higgs normalization theorem;
- open closure-attempt result: no allowed current-surface premise fixes
  `kappa_s`; a scalar LSZ/source-normalization theorem remains required;
- bounded-support scalar-source response harness extension: the production
  harness now emits `dE/ds`, but physical `dE/dh` still requires production
  data and derived `kappa_s`;
- bounded-support Feynman-Hellmann production protocol: common-ensemble
  symmetric source shifts and correlated `dE/ds` fits are specified, but
  scalar LSZ/canonical-normalization and response matching remain open;
- bounded-support same-source scalar two-point measurement: `C_ss(q)` and
  `Gamma_ss(q)` are executable for the source used in `dE/ds`, but no
  controlled pole/continuum LSZ residue is derived;
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
# SUMMARY: PASS=8 FAIL=0

python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=8 FAIL=0

python3 scripts/frontier_yt_free_staggered_kinetic_coefficient.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_interacting_kinetic_background_sensitivity.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=17 FAIL=0

python3 scripts/frontier_yt_scalar_lsz_normalization_cancellation.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=18 FAIL=0

python3 scripts/frontier_yt_feshbach_operator_response_boundary.py
# SUMMARY: PASS=5 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=19 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=12 FAIL=0

python3 scripts/frontier_yt_bridge_stack_import_audit.py
# SUMMARY: PASS=7 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=20 FAIL=0

python3 scripts/frontier_yt_scalar_spectral_saturation_no_go.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=21 FAIL=0

python3 scripts/frontier_yt_large_nc_pole_dominance_boundary.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=22 FAIL=0

python3 scripts/frontier_yt_production_resource_projection.py
# SUMMARY: PASS=7 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=23 FAIL=0

python3 scripts/frontier_yt_feynman_hellmann_source_response_route.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=24 FAIL=0

python3 scripts/frontier_yt_mass_response_bracket_certificate.py
# SUMMARY: PASS=7 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=25 FAIL=0

python3 scripts/frontier_yt_source_reparametrization_gauge_no_go.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=26 FAIL=0

python3 scripts/frontier_yt_canonical_scalar_normalization_import_audit.py
# SUMMARY: PASS=7 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=27 FAIL=0

python3 scripts/frontier_yt_source_to_higgs_lsz_closure_attempt.py
# SUMMARY: PASS=7 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=28 FAIL=0

python3 scripts/frontier_yt_scalar_source_response_harness_certificate.py
# SUMMARY: PASS=8 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=29 FAIL=0

python3 scripts/frontier_yt_fh_production_protocol_certificate.py
# SUMMARY: PASS=9 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=30 FAIL=0

python3 scripts/frontier_yt_same_source_scalar_two_point_lsz_measurement.py
# SUMMARY: PASS=8 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=31 FAIL=0

python3 scripts/frontier_yt_scalar_bs_kernel_residue_degeneracy.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=32 FAIL=0

python3 scripts/yt_direct_lattice_correlator_production.py --volumes 3x6 --masses 0.75 --therm 0 --measurements 1 --separation 0 --ape-steps 0 --engine python --scalar-two-point-modes '0,0,0;1,0,0' --scalar-two-point-noises 2 --output outputs/yt_direct_lattice_correlator_scalar_two_point_lsz_smoke_2026-05-01.json

python3 scripts/frontier_yt_scalar_two_point_harness_certificate.py
# SUMMARY: PASS=9 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=33 FAIL=0

python3 scripts/yt_direct_lattice_correlator_production.py --volumes 3x6 --masses 0.75 --therm 0 --measurements 1 --separation 0 --ape-steps 0 --engine python --scalar-source-shifts=-0.02,0.0,0.02 --scalar-two-point-modes '0,0,0;1,0,0' --scalar-two-point-noises 2 --output outputs/yt_direct_lattice_correlator_fh_lsz_joint_smoke_2026-05-01.json

python3 scripts/frontier_yt_fh_lsz_joint_harness_certificate.py
# SUMMARY: PASS=10 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=34 FAIL=0

python3 scripts/frontier_yt_fh_lsz_joint_resource_projection.py
# SUMMARY: PASS=7 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=35 FAIL=0

python3 scripts/frontier_yt_fh_lsz_invariant_readout_theorem.py
# SUMMARY: PASS=7 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=36 FAIL=0

python3 scripts/frontier_yt_scalar_pole_determinant_gate.py
# SUMMARY: PASS=7 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=37 FAIL=0
```
