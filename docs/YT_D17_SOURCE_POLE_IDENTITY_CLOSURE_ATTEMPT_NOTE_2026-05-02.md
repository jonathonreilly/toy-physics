# PR #230 D17 Source-Pole Identity Closure Attempt

```yaml
actual_current_surface_status: open / D17 source-pole identity closure attempt blocked
proposal_allowed: false
bare_retained_allowed: false
```

This block tests whether D17 single-scalar uniqueness can close the remaining
source-pole-to-canonical-Higgs identity gate.  The attempt fails honestly.

D17 and the Class #3 SUSY/2HDM analysis supply useful carrier support:

- one retained `(1,1)` scalar-singlet carrier on the `Q_L` block;
- no retained fundamental second scalar;
- no retained 2HDM species split.

Those are not enough for the PR #230 LSZ readout.  Carrier uniqueness does not
fix the source operator overlap `<0|O_s|h>`, the source two-point pole residue,
the inverse-propagator derivative at the pole, or the canonical kinetic metric
used by `v`.

## Single-Carrier Residue Family

The runner keeps these facts fixed:

```text
D17 Q_L scalar-singlet dimension = 1
second retained scalar present = false
canonical Higgs pole residue = 1
canonical y_h = 1
```

It then varies only the source operator overlap `Z_s`.  The source two-point
pole residue and source-response slope move while the D17 carrier facts stay
fixed.  This shows why D17 uniqueness is not itself a source-pole LSZ
normalization theorem.

## Claim Firewall

This block does not claim retained or `proposed_retained` closure.  It does
not use `H_unit` matrix-element readout, `yt_ward_identity`, observed target
values, `alpha_LM`, plaquette, `u0`, `c2 = 1`, `Z_match = 1`, or
`kappa_s = 1`.

## Runner

```text
python3 scripts/frontier_yt_d17_source_pole_identity_closure_attempt.py
# SUMMARY: PASS=17 FAIL=0
```

Output:

```text
outputs/yt_d17_source_pole_identity_closure_attempt_2026-05-02.json
```

## Exact Next Action

Either derive the missing source-overlap / `D'(pole)` theorem from the scalar
denominator, or wait for seed-controlled FH/LSZ chunks and measure same-source
pole residue under the model-class, FV/IR, and Higgs-identity gates.
