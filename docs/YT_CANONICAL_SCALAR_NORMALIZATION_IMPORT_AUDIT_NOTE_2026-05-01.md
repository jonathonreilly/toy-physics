# Top-Yukawa Canonical Scalar-Normalization Import Audit

**Date:** 2026-05-01  
**Status:** exact negative boundary / import audit  
**Runner:** `scripts/frontier_yt_canonical_scalar_normalization_import_audit.py`  
**Certificate:** `outputs/yt_canonical_scalar_normalization_import_audit_2026-05-01.json`

```yaml
actual_current_surface_status: exact negative boundary
conditional_surface_status: conditional-support for future scalar-source normalization repair
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Existing EW/Higgs notes assume or structure the canonical scalar field; they do not derive it from the PR230 source."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

After the source-reparametrization boundary, the natural question is whether the
repo already contains a retained canonical scalar-normalization theorem that
the PR #230 auditor missed.

This audit checks the strongest existing candidates:

- EW Higgs gauge-mass diagonalization;
- SM one-Higgs Yukawa gauge selection;
- observable-principle source response;
- `R_conn` / EW color projection.

## Result

```text
python3 scripts/frontier_yt_canonical_scalar_normalization_import_audit.py
# SUMMARY: PASS=7 FAIL=0
```

The result is negative for PR #230 closure:

- the EW gauge-mass note starts from a canonical `|D H|^2` Higgs doublet and
  `<H> = (0, v/sqrt(2))`; it does not derive the source-to-Higgs bridge;
- the SM one-Higgs note selects the allowed Yukawa monomials but explicitly
  leaves Yukawa matrices free;
- the observable-principle row is audited conditional;
- `R_conn` / EW color projection are audited conditional and do not derive
  scalar LSZ normalization.

## Consequence

No hidden retained current-surface theorem fixes `kappa_s` for PR #230.  A
future closure must derive source-to-canonical-Higgs normalization from the
Cl(3)/Z^3 source functional, or directly measure scalar LSZ / physical response
on production ensembles.

## Non-Claims

- This note does not demote the EW structural guardrails.
- This note does not use `H_unit` matrix-element readout.
- This note does not use observed top mass or observed `y_t`.
- This note does not use `alpha_LM`, plaquette, or `u0` as proof input.
