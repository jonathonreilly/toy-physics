# YT Top/WZ Matched Covariance Certificate Builder Note

Status: open / matched covariance contract; proposal_allowed=false.

This note records the covariance object required by the PR #230 same-source
top-response certificate.  The top-response route needs covariance between the
top source response and W/Z source response on a matched configuration set; an
aggregate top slope alone is not enough.

## Runner

```text
scripts/frontier_yt_top_wz_matched_covariance_certificate_builder.py
```

Default status output:

```text
outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json
```

Scout covariance certificate:

```text
outputs/yt_top_wz_matched_covariance_certificate_builder_scout_certificate_2026-05-04.json
```

Strict production covariance certificate:

```text
outputs/yt_top_wz_matched_covariance_certificate_2026-05-04.json
```

## Strict Input

Strict mode requires:

```text
outputs/yt_top_wz_matched_response_rows_2026-05-04.json
```

The row file must contain matched same-source top and W/Z response rows with
negative/zero/positive source-shift provenance, correlator-derived W/Z mass
fits, a matched configuration set, and clean firewalls excluding observed
top/`y_t`/W/Z selectors, `H_unit`, Ward authority, `alpha_LM`, plaquette/u0,
and by-fiat `c2`/`Z_match` choices.

## Current Result

Scout mode passes and writes only scout-named output:

```text
python3 scripts/frontier_yt_top_wz_matched_covariance_certificate_builder.py --scout
```

Default/current mode passes as an open status and does not write
`outputs/yt_top_wz_matched_covariance_certificate_2026-05-04.json`.  Strict
mode intentionally fails until matched top/W response rows exist.

The derivation-first shortcut from separate top and W marginals is now closed
negatively by
[`YT_TOP_WZ_COVARIANCE_MARGINAL_DERIVATION_NO_GO_NOTE_2026-05-05.md`](YT_TOP_WZ_COVARIANCE_MARGINAL_DERIVATION_NO_GO_NOTE_2026-05-05.md):
matched covariance is joint information and is not determined by marginal
response certificates.

## Non-Claims

This note does not claim retained or proposed_retained top-Yukawa closure.  It
does not produce W/Z mass fits, does not use observed W/Z/top/`y_t` selectors,
and does not use `H_unit`, `yt_ward_identity`, `alpha_LM`, plaquette, u0,
`kappa_s=1`, `c2=1`, `Z_match=1`, or `k_top/k_gauge=1`.

## Next Action

Produce matched same-source top/W response rows from the future W/Z response
measurement stream, or derive a same-surface factorization/independence
theorem fixing the joint covariance.  Then rerun this builder in strict mode
and rerun the same-source top-response certificate builder.
