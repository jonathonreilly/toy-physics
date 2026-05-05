# YT Same-Source W-Response Lightweight Readout Harness Note

Status: open / executable scout contract; proposal_allowed=false.

This note records the small-compute route for PR #230.  The route replaces a
full direct top-mass lattice campaign with same-source response rows, provided
the scalar source coordinate is common to the top and W measurements and the
orthogonal neutral-scalar correction is either measured or proven zero.

## Readout Contract

The same-source W-response decomposition already gives

```text
g_2 R_t / (sqrt(2) R_W) = y_h + delta_perp
delta_perp = y_x kappa_x / kappa_h
```

The lightweight harness validates the production row contract for the corrected
physical readout

```text
y_h = g_2 R_t / (sqrt(2) R_W) - delta_perp
```

where `R_t` is the same-source top response, `R_W` is the same-source W
mass-response, and `delta_perp` is supplied by one accepted authority:

- measured orthogonal/top tomography correction;
- source-Higgs Gram-purity correction;
- one-Higgs completeness;
- neutral-sector rank-one theorem.

## Runner

The runner is

```text
scripts/frontier_yt_same_source_w_response_lightweight_readout_harness.py
```

with default output

```text
outputs/yt_same_source_w_response_lightweight_readout_harness_2026-05-04.json
```

Scout mode builds synthetic same-source rows and verifies:

- the corrected readout recovers the planted `y_h`;
- uncertainty propagation through `g_2`, `R_t`, `R_W`, and `delta_perp`;
- weighted combination across multiple rows;
- rejection of missing `delta_perp` authority;
- rejection of mismatched-source rows;
- rejection of observed-value backsolves;
- rejection of static EW algebra used as a measurement.

Strict mode requires the future production row certificate

```text
outputs/yt_same_source_w_response_rows_2026-05-04.json
```

and fails honestly while that certificate is absent.

The row file is assembled by

```text
scripts/frontier_yt_same_source_w_response_row_builder.py
```

from a strict same-source W/top response certificate plus a strict
orthogonal-correction certificate.  Scout mode for that builder writes only
scout-named rows so it cannot satisfy this production harness by accident.

## Current Result

The scout command passes:

```text
python3 scripts/frontier_yt_same_source_w_response_lightweight_readout_harness.py --scout
```

The current/default gate records that no production row certificate exists.  It
therefore does not authorize closure.  The full PR230 assembly gate now treats
this lightweight readout as the concrete W-route production contract.

## Non-Claims

This note does not claim retained or proposed_retained top-Yukawa closure.  It
does not generate W/Z production rows, does not use `H_unit`,
`yt_ward_identity`, `y_t_bare`, observed selectors, `alpha_LM`, plaquette/u0,
`kappa_s=1`, `c2=1`, `Z_match=1`, or `cos(theta)=1`, and does not set
`delta_perp` to zero without a one-Higgs, rank-one, tomography, or Gram-purity
certificate.

## Next Action

The reduced compute target is now explicit: write
`outputs/yt_fh_gauge_mass_response_certificate_2026-05-02.json` from a
same-source EW/W mass-response measurement and
`outputs/yt_same_source_w_response_orthogonal_correction_certificate_2026-05-04.json`
from tomography, Gram purity, one-Higgs completeness, or neutral rank one.
Then run the row builder to emit
`outputs/yt_same_source_w_response_rows_2026-05-04.json`, rerun the
lightweight readout harness, matching/running bridge, retained-route
certificate, and full PR230 assembly gate.
