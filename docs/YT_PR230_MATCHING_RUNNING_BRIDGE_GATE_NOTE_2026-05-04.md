# PR230 Matching/Running Bridge Gate

Status: open / bridge contract ready; proposal_allowed=false.

This note adds the missing non-chunk gate for converting a certified PR230
lattice-scale readout into `y_t(v)` and `m_t(pole)`.  It does not supply a
physical readout.  It defines the certificate shape that must be present after
production, scalar-LSZ/direct-mass, source-overlap/direct-mass, scale-setting,
and uncertainty gates pass.

## Required Future Certificate

`outputs/yt_pr230_matching_running_bridge_certificate_2026-05-04.json` must
provide:

- a certified physical readout reference;
- one allowed readout kind: direct correlator mass, FH/LSZ source pole,
  source-Higgs Gram route, or same-source W/Z response;
- certified scalar-LSZ or direct-mass authority;
- certified source-overlap or direct-mass authority;
- certified scale anchor;
- `v` declared as substrate input, not derived by this route;
- SM RGE loop order 4 or 5;
- MSbar-to-pole conversion order at least 3;
- statistical, finite-volume, finite-spacing, scale-setting, running-bridge,
  and matching uncertainties;
- false firewall flags for observed selectors, `H_unit`/Ward authority,
  `alpha_LM`/plaquette authority, and `kappa/c2/Z_match` shortcuts.

## Current Result

The candidate certificate is absent, so the gate remains open:

```bash
python3 scripts/frontier_yt_pr230_matching_running_bridge_gate.py
# SUMMARY: PASS=5 FAIL=0
```

The runner performs only a toy arithmetic sanity check for the formula shape.
Those toy values are not evidence and do not enter any PR230 result.

## Claim Boundary

This does not claim `y_t`, `m_t`, retained, or proposed_retained status.  It
only prevents a finished chunk stream from being treated as full closure until
the lattice-to-physical matching/running bridge is certified with non-selector
inputs.
