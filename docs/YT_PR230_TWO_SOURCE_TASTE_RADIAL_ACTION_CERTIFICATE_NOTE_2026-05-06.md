# PR230 Two-Source Taste-Radial Action Certificate Note

**Date:** 2026-05-06  
**Status:** exact-support / same-surface two-source taste-radial action source vertex realized; canonical `O_H` and production pole rows absent  
**Claim type:** support_boundary  
**Runner:** `scripts/frontier_yt_pr230_two_source_taste_radial_action_certificate.py`  
**Certificate:** `outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json`

```yaml
actual_current_surface_status: exact-support / same-surface two-source taste-radial action source vertex realized; canonical O_H and production pole rows absent
conditional_surface_status: conditional-support for future measured C_sx/C_xx rows if the taste-radial source is run in production and a separate canonical O_H/source-overlap or physical-response bridge closes
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
bare_retained_allowed: false
```

## Purpose

The previous two-source chart certificate identified the exact abstract
source/taste-radial pair
`I_8/sqrt(8), (S0+S1+S2)/sqrt(24)`.  This note records the next concrete
artifact: the production harness can now represent the second source as a
gauge-covariant blocked-hypercube vertex rather than as prose.

The implemented source vertex is

```text
X = (X_1 + X_2 + X_3)/sqrt(3)
```

where `X_i` flips the spatial parity bit inside each `2^3` `Cl(3)/Z^3` block
and uses the connecting `SU(3)` link for gauge covariance.  On the cold
same-surface check, each `X_i` is Hermitian, squares to identity, is
Hilbert-Schmidt orthogonal to the other two axes, and `X` has the same
Hilbert-Schmidt norm as the uniform source `I` while remaining orthogonal to
it.

## Boundary

This is not a canonical-Higgs certificate.  The normalization is
`source_norm_matched` against the uniform lattice source, not scalar LSZ or
canonical Higgs normalization.  The runner deliberately sets
`canonical_higgs_operator_identity_passed=false`, does not set `kappa_s=1`, and
does not write production `C_sx/C_xx` rows.

The certificate can be supplied to the existing source-Higgs cross-correlator
harness as a source-vertex certificate for future bounded or production
measurements, but any resulting finite-mode rows remain non-closure evidence
until the canonical `O_H`/source-overlap, scalar-LSZ, FV/IR, and retained-route
gates pass.

## Validation

```text
python3 scripts/frontier_yt_pr230_two_source_taste_radial_action_certificate.py
# SUMMARY: PASS=15 FAIL=0
```

The runner also executes an internal one-mode finite smoke through the same
stochastic source-Higgs estimator to verify the sparse vertex is accepted by
the harness and emits finite values under the existing `C_ss/C_sH/C_HH` schema.
For this certificate those are only source/source-operator smoke fields; they
are not promoted to measured `C_sx/C_xx` production rows.  The smoke row is
instrumentation only and is not production or pole evidence.
