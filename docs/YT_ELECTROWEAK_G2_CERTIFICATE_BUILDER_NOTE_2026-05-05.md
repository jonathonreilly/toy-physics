# PR #230 Electroweak g2 Certificate Builder Gate

Date: 2026-05-05

actual_current_surface_status: open / electroweak g2 certificate builder inputs absent
proposal_allowed: false
bare_retained_allowed: false

## Scope

The same-source W/Z route requires a strict non-observed `g2` certificate at:

```text
outputs/yt_electroweak_g2_certificate_2026-05-04.json
```

This block adds an executable builder gate for that missing input.  It does not
write the strict certificate on the current surface.  Instead, it audits the
available authority candidates and records why none is acceptable under the PR
#230 claim firewall.

## Runner

```text
python3 scripts/frontier_yt_electroweak_g2_certificate_builder.py
# SUMMARY: PASS=12 FAIL=0
```

Output:

```text
outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json
```

## Result

Rejected candidates:

- the strict certificate file is absent;
- the package `g_2(v)` surface is tied to plaquette, `u0`, `R_conn`, running,
  or audit-caveated EW authority that PR #230 cannot use as load-bearing proof;
- bare `g2^2 = 1/4` is not a low-scale physical `g2` certificate without an
  allowed running/matching bridge;
- the W-mass companion route reuses the existing EW `g2` lane and observed
  comparison context;
- response-only W/Z self-normalization is blocked by
  `outputs/yt_wz_g2_response_self_normalization_no_go_2026-05-05.json`.

## Claim Boundary

This is a builder/gate, not a retained proof.  It does not claim retained or
proposed_retained top-Yukawa closure, and it does not use observed `g2`,
observed W/Z/top/`y_t`, `H_unit`, `yt_ward_identity`, `alpha_LM`, plaquette,
`u0`, package `g2`, `c2=1`, `Z_match=1`, or `kappa_s=1` as proof authority.

## Next Action

Build a real allowed authority path for `g2`, such as a non-plaquette absolute
EW normalization theorem or a strict measurement/certificate satisfying the
builder's required fields.  Then rerun the W/Z mass-fit response-row builder
and full PR #230 assembly gate.
