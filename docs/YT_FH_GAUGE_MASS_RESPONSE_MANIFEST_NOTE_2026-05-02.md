# PR #230 Same-Source W/Z Gauge-Mass Response Manifest

```yaml
actual_current_surface_status: bounded-support / same-source WZ gauge-mass response manifest
proposal_allowed: false
bare_retained_allowed: false
```

This block records the concrete physical-response observable that would cancel
`kappa_s` in a Feynman-Hellmann ratio:

```text
y_t = (g2 / sqrt(2)) * (dE_top/ds) / (dM_W/ds)
```

The manifest requires top energies and W/Z masses measured under the same
scalar source shifts, correlated symmetric slope fits, retained electroweak
coupling normalization, and a same-source sector-overlap / canonical-Higgs
identity certificate.

The current production harness has top `dE/ds` support but no W/Z
mass-response path.  This is planning support only, not evidence.

## Runner

```text
python3 scripts/frontier_yt_fh_gauge_mass_response_manifest.py
# SUMMARY: PASS=11 FAIL=0
```

Output:

```text
outputs/yt_fh_gauge_mass_response_manifest_2026-05-02.json
```

## Claim Firewall

This block does not claim retained or `proposed_retained` closure.  It does
not use observed W/Z masses, observed top mass, observed `y_t`, `H_unit`,
`yt_ward_identity`, or `kappa_s = 1`.

## Exact Next Action

Either implement the W/Z response harness named here together with sector-
overlap and Higgs-pole identity certificates, or continue the scalar-
denominator / production FH-LSZ route.
