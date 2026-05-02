# PR #230 Latest Higgs-Pole Identity Blocker Certificate

```yaml
actual_current_surface_status: open / latest Higgs-pole identity blocker certificate
proposal_allowed: false
bare_retained_allowed: false
```

This block consolidates the current source-pole/canonical-Higgs blockers after
the D17 source-pole identity attempt, no-orthogonal-top-coupling import audit,
source-pole mixing obstruction, and source-overlap spectral sum-rule no-go.

The runner checks that the latest certificates still do not identify the
measured same-source scalar pole with the canonical Higgs radial mode whose
kinetic normalization defines `v`.  A witness family keeps the measured
source-pole top coupling fixed while varying the physical canonical-Higgs
Yukawa, so the missing identity cannot be bypassed by D17 carrier uniqueness,
no-retained-2HDM support, or finite source-overlap moments.

## Runner

```text
python3 scripts/frontier_yt_higgs_pole_identity_latest_blocker_certificate.py
# SUMMARY: PASS=14 FAIL=0
```

Output:

```text
outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json
```

## Claim Firewall

This block does not claim retained or `proposed_retained` closure.  It does not
set `kappa_s = 1`, `cos(theta) = 1`, or an orthogonal scalar top coupling to
zero.  It does not use `H_unit`, `yt_ward_identity`, observed target values,
`alpha_LM`, plaquette, `u0`, `c2 = 1`, or `Z_match = 1`.

## Exact Next Action

Either derive the source-pole-to-canonical-Higgs identity including source
residue and `D'(pole)`, or let seed-controlled production chunks accumulate
and process them through the combiner, pole-fit, model-class, FV/IR, and
Higgs-identity gates.
