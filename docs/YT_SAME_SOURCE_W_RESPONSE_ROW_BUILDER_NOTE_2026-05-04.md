# YT Same-Source W-Response Row Builder Note

Status: open / production-row adapter contract; proposal_allowed=false.

This note records the final adapter needed by the lightweight W-response route
in PR #230.  The adapter turns future same-source W/top response certificates
and a future `delta_perp` correction certificate into the exact row file read by
the lightweight harness:

```text
outputs/yt_same_source_w_response_rows_2026-05-04.json
```

It does not generate W/Z correlators, top correlators, source-shift fits, or
orthogonal neutral-scalar tomography rows.

## Runner

The runner is

```text
scripts/frontier_yt_same_source_w_response_row_builder.py
```

with default status output

```text
outputs/yt_same_source_w_response_row_builder_2026-05-04.json
```

Strict mode requires both inputs:

```text
outputs/yt_fh_gauge_mass_response_certificate_2026-05-02.json
outputs/yt_same_source_w_response_orthogonal_correction_certificate_2026-05-04.json
```

When both strict inputs validate, it writes the production rows consumed by
`frontier_yt_same_source_w_response_lightweight_readout_harness.py`.

## Acceptance Contract

The W/top response input must contain production same-source source shifts,
correlator-based W mass fits, the top source-response slope, the W
source-response slope, their covariance, a certified `g_2`, and identity
certificates for same-source sector overlap and the canonical-Higgs pole.

The correction input must contain a production or exact-support
`delta_perp` certificate from one accepted method:

- tomography correction row;
- source-Higgs Gram purity;
- one-Higgs completeness / orthogonal top null;
- neutral-sector rank-one theorem.

Both inputs must carry firewalls excluding observed-value selectors, `H_unit`,
`yt_ward_identity`, `y_t_bare`, `alpha_LM`, plaquette/u0, and by-fiat
normalizations such as `kappa_s=1`, `c2=1`, `Z_match=1`, or `cos(theta)=1`.

## Current Result

Scout mode passes and writes only scout-named rows:

```text
python3 scripts/frontier_yt_same_source_w_response_row_builder.py --scout
```

Default/current mode passes as an honest open gate while the future production
inputs are absent.  Strict mode intentionally fails until those inputs exist.

## Non-Claims

This note does not claim retained or proposed_retained top-Yukawa closure.  It
does not backfill production rows from scout data, does not set `delta_perp` to
zero, and does not use `H_unit`, `yt_ward_identity`, `y_t_bare`, observed
targets, `alpha_LM`, plaquette/u0, `kappa_s=1`, `c2=1`, `Z_match=1`, or
`cos(theta)=1`.

## Next Action

Produce the two strict inputs above, rerun this row builder in strict mode,
then rerun the lightweight W-response harness in strict mode.  If both pass,
the remaining PR230 blockers are the assembly-level matching/running and
retained-route authorization gates.
