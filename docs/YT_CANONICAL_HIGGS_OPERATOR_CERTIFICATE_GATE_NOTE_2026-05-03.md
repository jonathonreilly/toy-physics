# Canonical-Higgs Operator Certificate Gate

**Status:** open / canonical-Higgs operator certificate absent
**Runner:** `scripts/frontier_yt_canonical_higgs_operator_certificate_gate.py`
**Certificate:** `outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json`

## Purpose

The source-Higgs Gram-purity route needs an audit-acceptable same-surface
operator certificate for canonical `O_H`.  The production harness can now
measure finite-mode `C_ss/C_sH/C_HH` rows, but only after such a certificate is
supplied.

This gate defines the acceptance schema for that future certificate and audits
the current repository surfaces for a hidden existing authority.  The broader
repo-wide authority audit is recorded in
`outputs/yt_canonical_higgs_repo_authority_audit_2026-05-03.json`.

The Legendre/LSZ source-pole construction in
`outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json` is now
recognized as positive support: it gives a normalized source-pole operator
`O_sp`.  It is not accepted as canonical `O_H` because the source-pole /
canonical-Higgs overlap remains open.

## Acceptance Schema

A future certificate must provide:

- `certificate_kind == canonical_higgs_operator`;
- same Cl(3)/Z3 source surface and same source coordinate flags;
- nonempty `operator_id` and `operator_definition`;
- `canonical_higgs_operator_identity_passed: true`;
- nonempty identity and normalization certificate references;
- a diagonal vertex kind supported by the harness;
- `hunit_used_as_operator: false`;
- `static_ew_algebra_used_as_operator: false`;
- firewall flags rejecting observed targets, `yt_ward_identity`,
  `alpha_LM`/plaquette authority, and `H_unit` matrix-element readout.

## Current Result

No canonical-Higgs operator certificate is present.  Existing EW/Higgs/YT
surfaces are not hidden certificates:

- the EW Higgs gauge-mass theorem assumes canonical `H` after it is supplied;
- the SM one-Higgs theorem selects allowed monomials but leaves Yukawa values
  free;
- the `H_unit` candidate gate rejects using `H_unit` as `O_H` without purity
  and normalization certificates;
- the source-Higgs harness extension is measurement instrumentation only.
- the repo-wide authority audit finds no hidden accepted `O_H` certificate in
  the Higgs/taste/Ward/source/EW surfaces.
- the Legendre/LSZ source-pole construction supplies `O_sp`, not the physical
  canonical `O_H` identity.

## Claim Boundary

This gate does not claim retained or `proposed_retained` `y_t` closure.  It
does not define `O_H` by fiat, does not treat `H_unit` or static EW algebra as
`O_H`, and does not use observed targets, `yt_ward_identity`, `alpha_LM`,
plaquette, or `u0`.

## Next Action

Derive or supply a real same-surface canonical-Higgs operator certificate
satisfying this schema, or upgrade the constructed source-pole operator with
source-Higgs `C_sH/C_HH` pole residues and Gram purity.

## Verification

```bash
python3 scripts/frontier_yt_canonical_higgs_operator_certificate_gate.py
# SUMMARY: PASS=11 FAIL=0
```
