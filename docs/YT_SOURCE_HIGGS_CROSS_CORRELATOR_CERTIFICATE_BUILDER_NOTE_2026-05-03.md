# Source-Higgs Cross-Correlator Certificate Builder

**Status:** open / measurement rows absent
**Runner:** `scripts/frontier_yt_source_higgs_cross_correlator_certificate_builder.py`
**Status Certificate:** `outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json`
**Candidate Certificate:** `outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json`

## Purpose

This runner is the concrete production-data input contract for the selected
PR #230 source-Higgs Gram-purity route.  It does not create `O_H`, `C_sH`, or
`C_HH` data.  When same-ensemble measurement rows are available, it validates
the claim firewall, requires the May 6 genuine `O_sp` intake certificate,
computes the pole-residue Gram quantities, and writes the candidate certificate
consumed by
`scripts/frontier_yt_source_higgs_gram_purity_postprocessor.py`.

## Required Measurement Rows

The input row file must provide:

- production phase metadata;
- same-ensemble and same-source-coordinate flags;
- a source coordinate shared by `C_ss`, `C_sH`, and `C_HH`;
- a named certified canonical-Higgs operator, not `H_unit` by fiat;
- nonempty identity and normalization certificate references for that operator;
- pole residue rows containing `Res_C_ss`, `Res_C_sH`, and `Res_C_HH`;
- isolated-pole or model-class/pole-saturation evidence;
- finite-volume, infrared, and zero-mode control;
- firewall flags showing no observed-target selectors, no `yt_ward_identity`,
  no `H_unit` matrix-element readout, and no `alpha_LM` or plaquette authority.

The source side must also attach
`outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json`.  The
builder checks that this intake marks `O_sp` as genuine current-surface support,
same-source, source-rescaling invariant, and contact-term invariant, while also
marking it explicitly as non-closure with no canonical `O_H` identity.

The builder now also requires the May 6 source-Higgs overlap/kappa contract
`outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json`.  For
future rows it emits the same exact readout

```text
kappa_spH = Res(C_sH) / sqrt(Res(C_ss) Res(C_HH)).
```

This is an overlap field in the future row certificate, not a permission to
set `kappa_s = 1`.

## Computed Quantities

For the selected pole row, the builder computes:

```text
Delta = Res(C_ss) Res(C_HH) - Res(C_sH)^2
rho_sH = Res(C_sH) / sqrt(Res(C_ss) Res(C_HH))
kappa_spH = rho_sH after O_sp source-side normalization
```

The builder records the central-value purity check, but it does not authorize
the route.  Final purity evaluation remains in the Gram-purity postprocessor,
and retained-route authorization remains outside this support artifact.

## Current Result

No same-ensemble source-Higgs measurement row file is present.  The builder
therefore writes only the status certificate and does not write a production
candidate certificate.  That is the expected honest state before `O_H/C_sH/C_HH`
rows exist.  The status certificate now records both the older Legendre/LSZ
source-pole construction and the stronger May 6 genuine `O_sp` intake artifact
as required source-side contract inputs for any future candidate rows.

## Claim Boundary

This note and runner do not claim retained or `proposed_retained` `y_t`
closure.  They do not define `O_H` by fiat, do not treat `H_unit` as `O_H`, do
not set `kappa_s = 1` or `cos(theta) = 1`, and do not use `yt_ward_identity`,
observed targets, `alpha_LM`, plaquette, or `u0`.

## Next Action

Produce same-ensemble measurement rows for a certified canonical-Higgs radial
operator, including `C_ss`, `C_sH`, and `C_HH` pole residues.  Then rerun this
builder and the Gram-purity postprocessor.
