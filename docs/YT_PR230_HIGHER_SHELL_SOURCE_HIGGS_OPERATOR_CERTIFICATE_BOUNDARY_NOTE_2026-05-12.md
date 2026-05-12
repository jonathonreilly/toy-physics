# PR230 Higher-Shell Source-Higgs Operator-Certificate Boundary

**Status:** exact negative boundary: higher-shell source-Higgs cross rows use
the taste-radial second-source certificate, not canonical `O_H`

**Runner:**
`scripts/frontier_yt_pr230_higher_shell_source_higgs_operator_certificate_boundary.py`

**Certificate:**
`outputs/yt_pr230_higher_shell_source_higgs_operator_certificate_boundary_2026-05-12.json`

```yaml
actual_current_surface_status: exact negative boundary / higher-shell source-Higgs cross rows use the taste-radial second-source certificate, not canonical O_H
conditional_surface_status: conditional-support if future rows are rerun with a certified canonical O_H operator or a separate same-surface O_H/source-overlap bridge passes
proposal_allowed: false
bare_retained_allowed: false
audit_required_before_effective_retained: true
```

## Purpose

The active higher-shell Schur/LSZ workers include `--source-higgs-cross-modes`
and a `--source-higgs-operator-certificate`.  This block checks the certificate
actually supplied to those commands before any completed rows can be overread.

The supplied certificate is:

```text
outputs/yt_pr230_two_source_taste_radial_action_certificate_2026-05-06.json
```

That certificate realizes the second source as the PR230 taste-radial
hypercube-flip source.  It explicitly records
`canonical_higgs_operator_identity_passed = false`.

## Result

The runner verifies:

- the higher-shell wave launcher is run-control support only;
- the active source/operator cross-correlator commands use the taste-radial
  certificate above;
- the certificate has `operator_id =
  pr230_taste_radial_hypercube_flip_source_v1`;
- the certificate does not use `H_unit`, Ward identity, observed selectors, or
  a taste-radial-as-canonical-`O_H` relabeling;
- the production harness preserves the semantic firewall by emitting
  `C_sx/C_xx` aliases when the supplied operator is taste-radial;
- pending chunks001-002 are run-control only, not row evidence;
- pole-residue and Gram-purity gates still await valid production rows under
  canonical operator authority.

Therefore, if the current higher-shell chunks complete under this certificate,
their cross rows are taste-radial `C_sx/C_xx` support.  They are not strict
canonical-Higgs `C_sH/C_HH` rows unless a separate canonical `O_H` or
source-overlap bridge lands.

## Boundary

This is not a permanent no-go against higher-shell source-Higgs production.  It
is a certificate boundary for the currently launched rows.  The route reopens
only with one of:

- a certified canonical `O_H` operator identity;
- a same-surface source-overlap or physical neutral-transfer bridge;
- strict production `C_ss/C_sH/C_HH(tau)` rows under canonical `O_H` authority;
- pole/FV/IR/model-class and Gram-purity authority.

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.  It
does not use `H_unit`, `yt_ward_identity`, `y_t_bare`, observed top/`y_t`
selectors, `alpha_LM`, plaquette, or `u0`.  It does not treat pending workers
as row evidence, does not treat taste-radial `x` as canonical `O_H`, does not
promote `C_sx/C_xx` aliases to strict `C_sH/C_HH`, and does not treat completed
higher-shell finite rows as pole residues.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_higher_shell_source_higgs_operator_certificate_boundary.py
python3 scripts/frontier_yt_pr230_higher_shell_source_higgs_operator_certificate_boundary.py
# SUMMARY: PASS=16 FAIL=0
```
