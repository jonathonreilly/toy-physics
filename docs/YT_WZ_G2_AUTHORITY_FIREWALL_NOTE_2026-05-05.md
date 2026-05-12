# PR #230 W/Z g2 Authority Firewall

Date: 2026-05-05

actual_current_surface_status: exact negative boundary / WZ response g2 authority absent for PR230
proposal_allowed: false
bare_retained_allowed: false

## Scope

The same-source W/Z response route uses the ratio

```text
y_t = (g2 / sqrt(2)) * (dE_top/ds) / (dM_W/ds)
```

after the same-source overlap and canonical-Higgs identity gates pass.  The
ratio cancels a common source-coordinate normalization, but it does not remove
the multiplicative electroweak coupling `g2`.

This block therefore adds a firewall for `g2` authority.  It prevents the PR
#230 W/Z route from silently importing the repo-level EW package value as the
missing strict input.

## Runner

```text
python3 scripts/frontier_yt_wz_g2_authority_firewall.py
# SUMMARY: PASS=7 FAIL=0
```

Output:

```text
outputs/yt_wz_g2_authority_firewall_2026-05-05.json
```

## Result

The runner records:

- `outputs/yt_electroweak_g2_certificate_2026-05-04.json` is absent.
- The W/Z mass-fit response-row builder already records `g2_validation.present=false`.
- The repo-level `g_2(v)` package surface exists, but is not an allowed PR #230
  proof input under the current firewall because it is not a same-source W/Z
  response measurement row and its authority path is entangled with inputs
  forbidden here as load-bearing proof inputs.
- Holding the same-source response ratio fixed while changing `g2` changes
  the inferred `y_t`; therefore `g2` remains an independent input unless a new
  cancellation theorem is supplied.

## Claim Boundary

This note does not claim retained or proposed_retained top-Yukawa closure.  It
does not use observed `g2`, observed W/Z/top/`y_t` selectors, `H_unit`,
`yt_ward_identity`, `alpha_LM`, plaquette, `u0`, `kappa_s=1`, `c2=1`,
`Z_match=1`, or `k_top/k_gauge=1`.

This is a current-surface PR #230 authority firewall, not a theorem that
`g2` can never be supplied by a different route.  A future audit-clean
non-observed `g2` certificate, if explicitly admitted as a PR #230 input, or a
same-source W/Z response theorem that cancels `g2`, retires this blocker.  The
negative result here is only that the present W/Z route may not silently import
the existing repo-level EW package value as its missing strict evidence.

## Next Action

Supply a strict non-observed `g2` certificate from an allowed authority, or
derive a same-source W/Z response theorem that cancels `g2`.  Then rerun the
W/Z mass-fit response-row builder, same-source top/W covariance builder, and
full PR #230 assembly gate.
