# PR230 W/Z Harness Probe Refresh

Status: bounded-support / W/Z audit-probe maintenance only; no top-Yukawa
closure claim.

This refresh keeps the W/Z path gates aligned with the current
`scripts/yt_direct_lattice_correlator_production.py` harness after the FH/LSZ
selected-mass and normal-cache optimization.  The harness now contains a
default-off synthetic W/Z smoke-schema path with `--wz-source-shifts`; that
flag is not a production W/Z correlator path.

Updated checks:

- `scripts/frontier_yt_wz_response_row_production_attempt.py` now distinguishes
  the smoke-schema W/Z plumbing from a genuine W/Z correlator/mass-fit path.
- `scripts/frontier_yt_wz_correlator_mass_fit_path_gate.py` now recognizes the
  current `wz_mass_response` absent guard even though the metadata string is
  assembled in Python rather than present as one literal JSON fragment.

The physical boundary is unchanged.  The current PR230 surface still has no
same-source EW/Higgs action certificate, no W/Z correlator mass-fit rows, no
same-source top/W covariance rows, no strict non-observed `g2`, and no
canonical-Higgs identity.  Synthetic W/Z smoke rows, static EW algebra, and
`--wz-source-shifts` in the smoke harness remain non-evidence.

Validation:

```text
python3 scripts/frontier_yt_wz_response_row_production_attempt.py
# SUMMARY: PASS=12 FAIL=0
python3 scripts/frontier_yt_wz_correlator_mass_fit_path_gate.py
# SUMMARY: PASS=17 FAIL=0
python3 -m py_compile scripts/frontier_yt_wz_response_row_production_attempt.py scripts/frontier_yt_wz_correlator_mass_fit_path_gate.py
# OK
python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=200 FAIL=0
python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=325 FAIL=0
python3 scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# SUMMARY: PASS=79 FAIL=0
python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=427 FAIL=0
python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=111 FAIL=0
bash docs/audit/scripts/run_pipeline.sh
# OK, 5 existing warnings
python3 docs/audit/scripts/audit_lint.py --strict
# OK, 5 existing warnings
git diff --check
# OK
```

Claim firewall:

- does not claim retained or `proposed_retained` closure;
- does not write or synthesize W/Z production rows;
- does not treat smoke-schema rows as physical W/Z evidence;
- does not use `H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`,
  plaquette/`u0`, `c2=1`, `Z_match=1`, or `kappa_s=1`.

Exact next action: positive closure still requires one fresh strict artifact:
accepted same-surface `O_H` plus `C_ss/C_sH/C_HH` pole rows, a genuine W/Z
response packet with action/covariance/`g2` authority, strict Schur/scalar-LSZ
pole authority, or neutral H3/H4 primitive-transfer authority.

