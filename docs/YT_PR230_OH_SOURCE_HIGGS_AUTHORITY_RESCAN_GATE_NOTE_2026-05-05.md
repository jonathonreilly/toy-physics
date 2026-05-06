# PR230 O_H / Source-Higgs Authority Rescan Gate

Status: exact negative boundary / no current same-surface `O_H` or `C_sH/C_HH` row authority

This note records a narrow rescan of the PR230 source-Higgs route.  The
question is whether the branch already contains a same-surface canonical
Higgs operator certificate, or production source-Higgs pole rows, that earlier
closure gates failed to consume.

## Result

The rescan found no current same-surface canonical `O_H` identity/normalization
certificate and no production `C_ss/C_sH/C_HH` pole-row certificate.  Existing
FMS, action-first, invariant-ring, GNS, holonomic, Perron, positivity, and
determinant/reflection-positivity artifacts remain useful certificate engines
or future-theorem shapes only.  They do not supply the missing operator or
rows on the actual PR230 surface.

The rescan also explicitly consumes the unratified source-Higgs smoke operator
certificate.  That file is useful estimator plumbing, but it marks the operator
as smoke-only, lacks identity and normalization certificates, and sets
`proposal_allowed: false`.

## Counterfamily

The executable gate includes the minimal source-Higgs projection counterfamily:

```text
C_ss = 1, C_HH = 1, C_sH = rho,  rho in {1, 0.8, 0.5, 0, -0.5}.
```

All members keep the source-only row fixed and positive semidefinite, but they
assign different source-Higgs overlaps and Gram determinants.  Therefore
source-only PR230 data plus positivity do not select the physical `O_H`
overlap.  A real bridge still needs either a same-surface canonical `O_H`
certificate or the production `C_sH/C_HH` rows and the existing Gram-purity
postprocessor.

## Claim Firewall

This rescan does not use `H_unit`, the old `yt_ward_identity` readout,
observed `m_t` or `y_t`, `alpha_LM`/plaquette/`u0`, `kappa_s=1`, or
`y_t_bare`.  It does not claim retained or proposed-retained closure.

## Next Artifact

The next positive artifact must be one of:

- same-surface canonical `O_H` identity and normalization certificate;
- production `C_ss/C_sH/C_HH` pole rows for a certified `O_H`;
- a different bridge that bypasses `O_H`, such as genuine same-source W/Z
  rows with identity/covariance/strict `g2`, Schur rows, strict scalar-LSZ
  denominator authority, or a neutral primitive/off-diagonal-generator
  certificate.

Until such an artifact exists, the source-Higgs route remains open and no
retained/proposed-retained wording is authorized.

## Verification

```bash
python3 scripts/frontier_yt_pr230_oh_source_higgs_authority_rescan_gate.py
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=36 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=271 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=91 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=239 FAIL=0
```
