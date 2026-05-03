# PR #230 Source-Overlap Route Selection

**Status:** bounded-support / route-selection certificate
**Runner:** `scripts/frontier_yt_pr230_source_overlap_route_selection.py`
**Certificate:** `outputs/yt_pr230_source_overlap_route_selection_2026-05-03.json`

## Purpose

PR #230's measured same-source FH/LSZ quantity can identify a source-pole
coupling, but source-only data do not identify the canonical-Higgs overlap
needed to convert that source-pole coupling into physical `y_t`.

This note selects the next engineering lane for that blocker.

## Selection

The selected primary lane is the same-surface source-Higgs Gram-purity route:

```text
Delta = Res(C_ss) Res(C_HH) - Res(C_sH)^2
rho_sH = Res(C_sH) / sqrt(Res(C_ss) Res(C_HH))
```

At the isolated pole, `Delta = 0` and `|rho_sH| = 1` certify that the measured
source pole and the canonical Higgs radial operator create the same one-pole
state, up to normalization/sign.

This is the best first route because it directly attacks the missing
source-pole/canonical-Higgs overlap and reuses the existing same-source `C_ss`
and `dE_top/ds` production stream.

## Fallback

The fallback physical-observable lane is the same-source W/Z mass-response
route:

```text
y_t = (g2 / sqrt(2)) * (dE_top/ds) / (dM_W/ds)
```

That route is attractive, but it currently requires a new electroweak
gauge-response harness plus sector-overlap and canonical-Higgs identity
certificates.

## Current Boundary

This route selection is not closure.  The current surface still lacks:

- a same-surface canonical-Higgs radial operator `O_H`;
- `C_sH` and `C_HH` pole-residue rows;
- a passing Gram-purity gate;
- a same-source W/Z response certificate;
- retained-route authorization.

## Claim Firewall

This note does not claim retained or `proposed_retained` `y_t` closure.  It
does not treat `H_unit` as `O_H`, does not set `kappa_s = 1`, does not set
`cos(theta) = 1`, and does not use `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, or `u0` as proof authority.

## Next Action

Implement or audit a canonical `O_H` operator on the PR #230 surface, then add
same-ensemble `C_sH` and `C_HH` pole-residue rows and run the Gram-purity gate.
Keep same-source W/Z response as the fallback physical-observable route.
