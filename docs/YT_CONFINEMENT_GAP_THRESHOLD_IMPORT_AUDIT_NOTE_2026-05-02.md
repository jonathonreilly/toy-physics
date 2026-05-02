# PR #230 Confinement-Gap Threshold Import Audit

```yaml
actual_current_surface_status: exact negative boundary / confinement gap not scalar LSZ threshold
proposal_allowed: false
bare_retained_allowed: false
```

This block checks whether qualitative confinement or mass-gap language in the
`Cl(3)/Z^3` substrate can supply the uniform same-source scalar continuum
threshold required by the FH/LSZ pole-residue gate.  It cannot.

The substrate pin note mentions confinement/mass-gap constraints only as
qualitative spectrum and representation information.  It explicitly does not
pin a numerical Yukawa coefficient or scalar-pole normalization.  The runner
also keeps a colored-sector confinement gap fixed while allowing the
same-source color-singlet scalar continuum threshold to approach the scalar
pole, showing why the sector gap cannot be imported as the LSZ threshold
premise.

## Runner

```text
python3 scripts/frontier_yt_confinement_gap_threshold_import_audit.py
# SUMMARY: PASS=13 FAIL=0
```

Output:

```text
outputs/yt_confinement_gap_threshold_import_audit_2026-05-02.json
```

## Claim Firewall

This block does not claim retained or `proposed_retained` closure.  It does not
infer scalar pole saturation from confinement, does not use observed masses or
target values, and does not set `kappa_s`, `c2`, or `Z_match` to one.

## Exact Next Action

Continue seed-controlled production chunks or derive a genuine same-source
scalar denominator/threshold theorem.  Do not use generic confinement-gap
language as the FH/LSZ threshold premise.
