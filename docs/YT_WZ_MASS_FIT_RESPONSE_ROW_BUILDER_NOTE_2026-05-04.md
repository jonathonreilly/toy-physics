# YT WZ Mass-Fit Response-Row Builder Note

Status: open / W/Z mass-fit adapter contract, not retained and not
proposed_retained.

This note records the next executable adapter in the PR #230 same-source W
route.  The existing W/Z certificate builder consumes

```text
outputs/yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json
```

but the W/Z mass-fit path gate names a lower-level future input:

```text
outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json
```

The new builder bridges that gap.  It converts future W/Z correlator mass fits,
a matched top-response certificate, and a non-observed `g_2` certificate into
the measurement-row schema expected by
`frontier_yt_fh_gauge_mass_response_certificate_builder.py`.

## Runner

```text
scripts/frontier_yt_wz_mass_fit_response_row_builder.py
```

Default status output:

```text
outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json
```

Scout rows:

```text
outputs/yt_wz_mass_fit_response_row_builder_scout_rows_2026-05-04.json
```

## Strict Inputs

Strict mode requires:

```text
outputs/yt_wz_correlator_mass_fit_rows_2026-05-04.json
outputs/yt_same_source_top_response_certificate_2026-05-04.json
outputs/yt_electroweak_g2_certificate_2026-05-04.json
```

The W/Z mass-fit rows must contain negative, zero, and positive source shifts,
correlator-derived W or Z mass fits, fit-window or effective-mass metadata, and
jackknife/bootstrap block counts.

The top-response certificate must contain the matched `dE_top/ds` slope,
uncertainty, covariance against `dM_W/ds`, same-source coordinate metadata, and
the same-source sector / canonical-Higgs / retained-route identity booleans
required by the downstream W/Z response builder.

The top-response certificate is now assigned to
`frontier_yt_same_source_top_response_certificate_builder.py`, whose current
mode remains open until the same-source identity and matched covariance
certificates exist.

The `g_2` certificate must be non-observed-selector provenance.  External
observed `g_2`, W/Z masses, top mass, or `y_t` values are not accepted as proof
selectors.

## Current Result

Scout mode passes and writes only scout-named rows:

```text
python3 scripts/frontier_yt_wz_mass_fit_response_row_builder.py --scout
```

Default/current mode records that the strict inputs are absent and does not
write `outputs/yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json`.
Strict mode is expected to fail until those inputs exist.

## Non-Claims

This note does not claim retained or proposed_retained top-Yukawa closure.  It
does not measure W/Z correlators, does not use static EW algebra as `dM_W/ds`,
does not use observed W/Z/top/`y_t`/`g_2` selectors, and does not use `H_unit`,
`yt_ward_identity`, `alpha_LM`, plaquette/u0, `c2=1`, `Z_match=1`, or
`kappa_s=1`.

## Next Action

Produce the strict W/Z mass-fit rows, matched top-response certificate, and
non-observed `g_2` certificate.  Then rerun this builder in strict mode, rerun
the W/Z response certificate builder, and feed the resulting W/Z response
certificate into the same-source W-response row builder.
