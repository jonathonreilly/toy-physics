# Claim Status Certificate

**Block:** `yt-pr230-ward-physical-readout-20260501`  
**Artifacts:** global proof audit, Ward repair audit, operator-matching
candidate, source/Higgs SSB bridge reduction, kappa residue obstruction, scalar
LSZ residue bridge obstruction, chirality selector support, and common dressing
obstruction, current-surface scalar pole-residue no-go, retained-closure route
certificate, and direct-measurement scale requirements
**PR:** #230 draft branch

```yaml
actual_current_surface_status: open / conditional-support
conditional_surface_status: "Tree-level normalizations meet at 1/sqrt(6) if the physical-readout bridges are later repaired."
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Open imports remain: source/HS normalization, chirality selector, scalar carrier, scalar LSZ, and common dressing."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

Allowed wording:

- exact negative boundary on hidden-proof inventory;
- open repair map for Ward physical readout;
- conditional-support operator-matching candidate;
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
# SUMMARY: PASS=7 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_direct_measurement_scale_requirements.py
# SUMMARY: PASS=7 FAIL=0
```
