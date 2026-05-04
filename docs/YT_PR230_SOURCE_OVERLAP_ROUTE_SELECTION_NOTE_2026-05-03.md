# PR #230 Source-Overlap Route Selection

**Status:** bounded-support / route-selection certificate
**Runner:** `scripts/frontier_yt_pr230_source_overlap_route_selection.py`
**Certificate:** `outputs/yt_pr230_source_overlap_route_selection_2026-05-03.json`

## Purpose

PR #230's measured same-source FH/LSZ quantity can identify a source-pole
coupling, but source-only data do not identify the canonical-Higgs overlap
needed to convert that source-pole coupling into physical `y_t`.

This note selects the next engineering lane for that blocker.

The source side is now sharpened by
`YT_LEGENDRE_SOURCE_POLE_OPERATOR_CONSTRUCTION_NOTE_2026-05-03.md`: the
Legendre/LSZ construction derives a normalized source-pole operator `O_sp`.
The remaining blocker is the identity or measured overlap between `O_sp` and
canonical `O_H`.

`YT_OSP_OH_IDENTITY_STRETCH_ATTEMPT_NOTE_2026-05-03.md` tried to derive that
identity from the current source-only, taste, EW, and rank-one surfaces.  It
did not close: a counterfamily keeps `O_sp` normalized and the same-source top
readout fixed while changing the `O_sp/O_H` overlap.

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
source-pole/canonical-Higgs overlap, uses `O_sp` as the normalized source side,
and reuses the existing same-source `C_ss` and `dE_top/ds` production stream.
After `YT_FMS_OH_CERTIFICATE_CONSTRUCTION_ATTEMPT_NOTE_2026-05-04.md`, this
selection is explicitly blocked on the current PR230 surface until a
same-surface EW gauge-Higgs/`O_H` certificate exists.

## Fallback

The fallback physical-observable lane is the same-source W/Z mass-response
route:

```text
y_t = (g2 / sqrt(2)) * (dE_top/ds) / (dM_W/ds)
```

That route is attractive, but it currently requires a new same-source
electroweak action, W/Z correlator mass-fit path, matched top/W/Z covariance
rows, plus sector-overlap and canonical-Higgs identity certificates.

## Current Boundary

This route selection is not closure.  The current surface still lacks:

- a same-surface canonical-Higgs radial operator `O_H`;
- a same-surface EW gauge-Higgs production action for that `O_H`;
- the identity or measured pole overlap `O_sp = O_H`;
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

Do not cycle back to source-only `O_sp/O_H`.  The next positive source-Higgs
action is a same-surface EW gauge-Higgs/`O_H` certificate plus same-ensemble
`C_sH` and `C_HH` pole-residue rows.  If that new surface is not in scope,
continue FH/LSZ production and pursue W/Z, Schur, or rank-one alternatives
only where they add real rows or theorems.
