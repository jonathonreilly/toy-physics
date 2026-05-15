# PR230 W/Z Explicit-v Authority Firewall

Status: exact negative boundary / PR230 W/Z explicit-v authority absent.
This note is a claim firewall, not top-Yukawa closure.

## Purpose

Block68 identified three possible absolute-normalization pins for a future
same-source W/Z physical-response Jacobian:

- strict non-observed `g2`;
- explicit `v` authority;
- canonical source-response normalization.

This block tests the explicit-`v` pin.  The current repository surface contains
a package hierarchy value for `v`, but PR230 cannot use it as a load-bearing W/Z
absolute pin because its visible derivation chain includes the forbidden
`alpha_LM` / plaquette / `u0` normalization surface and observed-comparator
context.

## Result

The runner writes
`outputs/yt_pr230_wz_v_authority_firewall_2026-05-15.json` and checks:

- `outputs/yt_electroweak_v_authority_certificate_2026-05-12.json` is absent;
- the package surface contains `v = 246.282818290129 GeV`;
- the same package surface exposes `alpha_LM`, `M_Pl * alpha_LM^16`,
  plaquette, and `u_0` dependencies;
- Block68 explicitly records the `explicit_v_authority_certificate` future root
  as absent;
- the W/Z packet roots are also absent: accepted same-source EW/Higgs action,
  production W/Z rows, same-source top rows, matched covariance,
  `delta_perp`, and strict non-observed `g2`;
- existing FH/WZ manifests already record that static electroweak `v` does not
  identify the substrate source coordinate.

Therefore the package `v` value is rejected as a PR230 W/Z absolute-normalization
authority.  It remains a separate package/hierarchy surface and is not imported
as proof input here.

## Claim Boundary

This block does not use `H_unit`, `yt_ward_identity`, observed top mass,
observed `y_t`, observed `v`, observed `g2`, `alpha_LM`, plaquette, or `u0` as
proof authority.  It does not set `c2=1`, `Z_match=1`, `kappa_s=1`, `g2=1`, or
`v=1`.  It does not treat W/Z smoke/schema rows as production evidence.

No retained or `proposed_retained` top-Yukawa closure is authorized.
PR #230 remains draft/open.

## Exact Next Action

To reopen this W/Z absolute-pin subroute, supply
`outputs/yt_electroweak_v_authority_certificate_2026-05-12.json` from an allowed
non-observed, non-`alpha_LM`/plaquette/`u0` authority, or replace the absolute
pin with a strict non-observed `g2` certificate or canonical source-response
normalization.  Then rerun the W/Z physical-response packet and full PR230
assembly gates.

## Verification

```text
python3 -m py_compile scripts/frontier_yt_pr230_wz_v_authority_firewall.py
# OK
python3 scripts/frontier_yt_pr230_wz_v_authority_firewall.py
# SUMMARY: PASS=12 FAIL=0
```
