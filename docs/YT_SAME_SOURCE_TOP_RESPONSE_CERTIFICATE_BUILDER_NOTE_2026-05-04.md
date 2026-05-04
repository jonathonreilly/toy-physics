# YT Same-Source Top-Response Certificate Builder Note

Status: open / top-response certificate adapter contract, not retained and not
proposed_retained.

This note records the missing top-side certificate needed by the PR #230
same-source W/Z response route.  The repo already has bounded support for the
FH/LSZ common-window top source response, but that support is not a physical
top-Yukawa readout.  The new builder wraps that response only after future
identity and matched top/W covariance certificates validate.

## Runner

```text
scripts/frontier_yt_same_source_top_response_certificate_builder.py
```

Default status output:

```text
outputs/yt_same_source_top_response_certificate_builder_2026-05-04.json
```

Scout certificate:

```text
outputs/yt_same_source_top_response_certificate_builder_scout_certificate_2026-05-04.json
```

Strict production certificate:

```text
outputs/yt_same_source_top_response_certificate_2026-05-04.json
```

## Strict Inputs

Strict mode requires:

```text
outputs/yt_fh_lsz_common_window_response_gate_2026-05-04.json
outputs/yt_fh_lsz_common_window_pooled_response_estimator_2026-05-04.json
outputs/yt_same_source_top_response_identity_certificate_2026-05-04.json
outputs/yt_top_wz_matched_covariance_certificate_2026-05-04.json
```

The common-window response and pooled estimator supply the existing top
`dE_top/ds` support value and empirical uncertainty.  The future identity
certificate must close the same-source sector-overlap and canonical-Higgs pole
identity gates on the same scalar source coordinate.  The future covariance
certificate must supply matched top/W covariance rows from the same
configuration set.

The identity certificate is now assigned to
`frontier_yt_same_source_top_response_identity_certificate_builder.py`.  Its
current mode remains open until sector-overlap, canonical-Higgs pole identity,
one accepted identity route, and retained-route authorization exist.

## Current Result

Scout mode passes and writes only scout-named output:

```text
python3 scripts/frontier_yt_same_source_top_response_certificate_builder.py --scout
```

Default/current mode passes as an open status and does not write
`outputs/yt_same_source_top_response_certificate_2026-05-04.json`.  Strict mode
intentionally fails until the identity and covariance inputs exist.

## Non-Claims

This note does not claim retained or proposed_retained top-Yukawa closure.  It
does not treat source-only `dE_top/ds` as physical `y_t` evidence, does not set
`kappa_s=1`, `c2=1`, `Z_match=1`, or `cos(theta)=1`, and does not use `H_unit`,
`yt_ward_identity`, observed top/`y_t`, `alpha_LM`, plaquette, or u0.

## Next Action

Produce the same-source top-response identity certificate and matched top/W
covariance certificate.  Then rerun this builder in strict mode to emit the
production top-response certificate, rerun the W/Z mass-fit response-row
builder, and continue the W/Z response certificate path.
