# YT Same-Source W-Response Lightweight Readout Harness Note

Status: open / executable scout contract, not retained and not proposed_retained.

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
`outputs/yt_same_source_w_response_rows_2026-05-04.json` from a same-source EW/W
mass-response measurement, or supply a theorem certificate that sets
`delta_perp=0` through one-Higgs completeness or neutral rank one.  After that,
rerun the lightweight readout harness, matching/running bridge, retained-route
certificate, and full PR230 assembly gate.
