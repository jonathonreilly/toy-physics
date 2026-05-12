# PR #230 Source-Higgs Pole-Row Assembly

```yaml
actual_current_surface_status: open / strict source-Higgs pole-row assembly blocked by canonical O_H authority and missing pole rows
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_source_higgs_pole_row_assembly.py`  
**Certificate:** `outputs/yt_source_higgs_pole_row_assembly_2026-05-12.json`  
**Ingestion contract:** `outputs/yt_source_higgs_pole_row_ingestion_contract_2026-05-12.json`

## Purpose

This runner searches existing PR #230 outputs for strict source-Higgs pole-row
evidence:

```text
C_ss, C_sH, C_HH, pole location, residues, and
Res(C_sH)^2 = Res(C_ss) Res(C_HH)
```

It does not launch or duplicate chunk production.  It also does not accept
same-pole coincidence by itself.  Strict use requires a same-surface canonical
`O_H` action/LSZ authority certificate, isolated pole residues, Gram purity,
FV/IR control, model-class or pole-saturation control, and a contact-term
scheme certificate.

## Current Rows

Strict `C_ss/C_sH/C_HH` pole rows do not exist on the current surface.

The strongest current source-Higgs row artifact is
`outputs/yt_source_higgs_unratified_operator_smoke_run_2026-05-03.json`.
It has finite-mode `C_ss/C_sH/C_HH` plumbing rows, but only for the
`unratified_constant_diagonal_smoke_operator_v1`, with two momentum modes and
two configurations.  Those rows are support-only: they are not production
pole residues, they do not certify canonical `O_H`, and they do not pass the
pole-row/Gram-purity acceptance chain.

## Missing Strict Fields

Future production must supply the schema written by the ingestion contract.
The current blockers are exactly:

- production source-Higgs pole-row artifact with `same_surface_cl3_z3`,
  `same_ensemble`, `same_source_coordinate`, `source_coordinate`, and shared
  `surface_id`;
- canonical-Higgs operator fields:
  `operator_id`, `operator_definition`, matching `surface_id`,
  `operator_authority_scope=same_surface_canonical_action_lsz`,
  `canonical_higgs_operator_identity_passed=true`,
  `identity_certificate`, `lsz_normalization_certificate`,
  `same_surface_canonical_action_certificate`,
  `surface_matches_measurement=true`, and explicit false `H_unit`/static-EW
  substitutes;
- pole control:
  `isolated_scalar_pole_passed=true`, finite pole location,
  `model_class_or_pole_saturation_certificate_passed=true`,
  `fv_ir_zero_mode_control_passed=true`, and
  `contact_term_scheme_certificate_passed=true`;
- pole residues:
  `Res_C_ss`, `Res_C_sH`, `Res_C_HH`, plus errors or a 3x3 covariance;
- Gram-purity computation from residues:
  `Res(C_sH)^2 = Res(C_ss) Res(C_HH)`;
- forbidden-import firewall false for observed selectors, `yt_ward_identity`,
  `y_t_bare`, `alpha_LM`, plaquette/u0, `H_unit` matrix-element readout, and
  alias imports.

## K-Prime Compatibility

The ingestion contract mirrors the K-prime row-contract shape by naming a
`partition_certificate`, `pole_control`, `residue_matrix`, `gram_purity`, and
`firewall`.  The source numerator/projection handoff is the
`source_numerator_projection_rows_compatible_with_kprime=true` field under
`partition_certificate`.

## Validation

```text
python3 scripts/frontier_yt_source_higgs_pole_row_assembly.py
# SUMMARY: PASS=12 FAIL=0
```

The output status is intentionally open.  No retained or `proposed_retained`
claim is authorized by this assembly result.
