# YT Delta-Perp Tomography Correction Builder Note

Status: open / tomography correction contract, not retained and not
proposed_retained.

The same-source W-response route has reduced the physical readout to

```text
y_h = g_2 R_t/(sqrt(2) R_W) - delta_perp
delta_perp = sum_i y_i kappa_i / kappa_h
```

where the sum is over neutral scalar directions orthogonal to the canonical
Higgs radial mode.  This note records the executable contract for measuring
that correction by neutral-scalar top-coupling tomography.

## Runner

The runner is

```text
scripts/frontier_yt_delta_perp_tomography_correction_builder.py
```

with default output

```text
outputs/yt_delta_perp_tomography_correction_builder_2026-05-04.json
```

The future production input is

```text
outputs/yt_delta_perp_tomography_rows_2026-05-04.json
```

and, when strict production validation passes, the builder can emit the
orthogonal-correction certificate expected by the W-response gate:

```text
outputs/yt_same_source_w_response_orthogonal_correction_certificate_2026-05-04.json
```

## Acceptance Contract

The production tomography rows must supply:

- a same-surface neutral scalar basis containing the canonical Higgs radial
  mode and any orthogonal top-coupled directions;
- the same-source overlap vector `kappa`;
- the top-coupling vector `y`;
- a full-rank response matrix for that neutral scalar basis;
- identity certificates for the canonical Higgs mode, the orthogonal basis,
  and same-source sector overlap;
- a firewall excluding observed-value selectors, `H_unit`, Ward authority,
  `y_t_bare`, `alpha_LM`, plaquette/u0, `kappa_s=1`, `c2=1`, `Z_match=1`, and
  `cos(theta)=1`.

The builder computes

```text
delta_perp = (sum_{i != h} y_i kappa_i) / kappa_h
```

with conservative diagonal uncertainty propagation.

## Current Result

Scout mode passes on synthetic rows:

```text
python3 scripts/frontier_yt_delta_perp_tomography_correction_builder.py --scout \
  --output outputs/yt_delta_perp_tomography_correction_scout_2026-05-04.json
# SUMMARY: PASS=11 FAIL=0
```

The planted scout correction is

```text
delta_perp = -0.054444444444444455 +/- 0.004355429588352997
```

Default/current mode passes as an honest open gate:

```text
python3 scripts/frontier_yt_delta_perp_tomography_correction_builder.py
# SUMMARY: PASS=10 FAIL=0
```

Strict mode fails until the production tomography row certificate exists.  The
failed strict probe is not committed as evidence.

## Rejected Shortcuts

The builder rejects source-only rank-one tomography, missing canonical-Higgs
identity, observed-value backsolves, mismatched source coordinates, and zero
canonical source overlap.  It does not set `delta_perp=0`; that requires a
separate one-Higgs completeness, neutral-rank, or Gram-purity certificate.

## Non-Claims

This note does not claim retained or proposed_retained top-Yukawa closure.  It
does not create production tomography rows in scout/current mode, does not use
`H_unit`, `yt_ward_identity`, `y_t_bare`, observed selectors, `alpha_LM`,
plaquette/u0, `kappa_s=1`, `c2=1`, `Z_match=1`, or `cos(theta)=1`, and does not
claim a physical `y_t` readout without the W-response rows and matching/running
bridge.

## Next Action

Supply `outputs/yt_delta_perp_tomography_rows_2026-05-04.json` from real
same-surface full-rank neutral-scalar tomography, rerun the builder in strict
mode with `--emit-correction-certificate`, then rerun the W-response
orthogonal-correction gate.  The emitted correction certificate is one of the
two strict inputs to
`scripts/frontier_yt_same_source_w_response_row_builder.py`, which then writes
the production row file consumed by the lightweight W-response readout
harness.
