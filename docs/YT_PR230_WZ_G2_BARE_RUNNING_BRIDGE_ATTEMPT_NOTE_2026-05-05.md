# PR #230 W/Z G2 Bare-Running Bridge Attempt Note

Date: 2026-05-05

Status: exact negative boundary / WZ `g2` bare-to-low-scale running bridge not derivable on the current PR230 surface.

## Question

Can the current PR230 surface use a bare or structural SU(2) coupling plus beta-function running to supply the strict non-observed low-scale `g2` certificate needed by the same-source W/Z response route?

## Result

No.  The current surface contains structural SU(2) and EW dictionary support, but it does not contain the load-bearing data needed to convert a bare or structural coupling into a physical low-scale `g2`:

- same-source SU(2)xU(1)/Higgs action and gauge kinetic normalization;
- accepted bare electroweak coupling boundary condition in that action;
- lattice-cutoff/readout-scale ratio;
- threshold content and limiting order;
- finite matching scheme and constants;
- strict forbidden-import firewall.

The runner constructs a running/matching counterfamily: the same structural bare coupling and one-loop beta coefficient give different low-scale `g2` values when the unprovided scale ratio or finite matching shift is varied.  Therefore beta-function formula names and `g2^2=1/4` do not write the required PR230 `g2` certificate.

## Claim Boundary

This block writes no strict electroweak `g2` certificate and no W/Z response rows.  It does not claim retained or proposed-retained PR230 closure.  It does not use observed values, package `g_2(v)`, `alpha_LM`, plaquette, `u0`, `R_conn`, `H_unit`, Ward authority, or unit `c2/Z_match/kappa_s` as proof inputs.

Certificate:

```text
outputs/yt_pr230_wz_g2_bare_running_bridge_attempt_2026-05-05.json
```

Runner:

```text
scripts/frontier_yt_pr230_wz_g2_bare_running_bridge_attempt.py
```
