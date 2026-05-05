# PR #230 W/Z g2 Response Self-Normalization No-Go

Date: 2026-05-05

actual_current_surface_status: exact negative boundary / WZ response-only g2 self-normalization no-go
proposal_allowed: false
bare_retained_allowed: false

## Scope

The previous W/Z `g2` authority firewall showed that the same-source top/W
response ratio still contains a multiplicative `g2` input.  This block tests
the most direct escape route: whether top/W/Z response rows alone can
self-normalize `g2`.

They cannot.

For a shared scalar source coordinate `s`,

```text
dE_top/ds = k y_t / sqrt(2)
dM_W/ds   = k g2 / 2
dM_Z/ds   = k sqrt(g2^2 + gY^2) / 2
```

the scaling

```text
k -> lambda k
y_t -> y_t / lambda
g2 -> g2 / lambda
gY -> gY / lambda
```

leaves all three slopes and the top/W/Z response ratios invariant while
changing the absolute values of `y_t`, `g2`, and `gY`.  Therefore response-only
W/Z data determine ratios such as `y_t/g2` and `gY/g2`, not the absolute
physical top Yukawa.

## Runner

```text
python3 scripts/frontier_yt_wz_g2_response_self_normalization_no_go.py
# SUMMARY: PASS=9 FAIL=0
```

Output:

```text
outputs/yt_wz_g2_response_self_normalization_no_go_2026-05-05.json
```

## Result

The runner constructs a three-member countermodel family with identical
`dE_top/ds`, `dM_W/ds`, `dM_Z/ds`, `dE_top/dM_W`, and `dM_Z/dM_W`, while
`y_t`, `g2`, `gY`, and the source coordinate normalization all vary.  It also
loads the current W/Z `g2` firewall and W/Z response-row builder, which still
record that the strict non-observed `g2` certificate is absent.

## Claim Boundary

This is a no-go for response-only `g2` self-normalization, not a no-go against
future W/Z closure.  Allowed escape routes remain:

- supply a strict non-observed `g2` certificate from an allowed authority;
- derive an absolute electroweak normalization theorem outside response-only rows;
- derive a separate theorem where `g2` cancels against another already-certified physical observable.

This note does not claim retained or proposed_retained top-Yukawa closure.  It
does not use observed `g2`, observed W/Z/top/`y_t` selectors, `H_unit`,
`yt_ward_identity`, `alpha_LM`, plaquette, `u0`, `kappa_s=1`, `c2=1`,
`Z_match=1`, or a packaged `g2` value.

## Next Action

Do not spend another block on response-only `g2` cancellation.  Either build an
allowed electroweak `g2` certificate, add absolute EW normalization data or a
theorem outside response-only rows, or continue the source-Higgs, Schur-row,
rank-one neutral-scalar, or production-chunk routes.
