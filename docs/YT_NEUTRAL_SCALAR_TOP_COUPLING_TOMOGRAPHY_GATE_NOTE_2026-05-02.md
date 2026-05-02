# PR #230 Neutral Scalar Top-Coupling Tomography Gate

```yaml
actual_current_surface_status: open / neutral scalar top-coupling tomography gate not passed
proposal_allowed: false
bare_retained_allowed: false
```

Complete source-spectrum data identify a source-overlap row, and
`dE_top/ds` supplies one linear equation for the neutral-scalar top-coupling
vector.  If the neutral scalar sector has an orthogonal component, that rank is
not enough to recover the canonical-Higgs component.

The runner constructs the current rank-one response matrix

```text
source row = (cos(theta), sin(theta))
dE_top/ds = source row . (y_h, y_chi)
```

and moves along the null direction `(sin(theta), -cos(theta))`.  The
same-source response stays fixed, while the canonical-Higgs component `y_h`
varies by more than a factor of four with finite positive `y_chi`.

## Runner

```bash
python3 scripts/frontier_yt_neutral_scalar_top_coupling_tomography_gate.py
# SUMMARY: PASS=14 FAIL=0
```

Certificate:

```text
outputs/yt_neutral_scalar_top_coupling_tomography_gate_2026-05-02.json
```

## Claim Firewall

This does not claim retained or `proposed_retained` closure.  It does not set
`kappa_s = 1`, `cos(theta) = 1`, or the orthogonal scalar top coupling to zero.
It does not use `H_unit`, `yt_ward_identity`, observed target values,
`alpha_LM`, plaquette, `u0`, `c2 = 1`, or `Z_match = 1`.

## Exact Next Action

Add an independent non-source response row: same-surface `O_H/C_sH/C_HH`
Gram-purity data, W/Z response with sector-overlap identity certificates, or a
rank-one/no-orthogonal-coupling theorem.
