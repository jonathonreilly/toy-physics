# Two-Field Retarded/Hybrid Probe Note

**Date:** 2026-04-10
**Script:** `frontier_two_field_retarded_probe.py`

## Summary

This probe tests one concrete next field-law candidate beyond the current
wave prototype:

- a causal memory accumulator `m` that lags the matter density `|ψ|²`
- a damped wave equation for `Φ`
- matter evolution via staggered CN with `V = -m · Φ`

The field law is graph-native and runs only on the retained admissible
cycle-bearing bipartite families:

- random geometric
- growing
- layered cycle

**Measurement note:** on these irregular graph families, the sign rows use the
same BFS-depth shell-radial proxy as the cycle battery, not the exact
lattice-coordinate force from the cubic canonical card. The later two-sign
audit shows these irregular sign measures are not sign-selective and therefore
cannot by themselves support an attractive-gravity claim.

## Battery Results

| Row | Random Geometric (36) | Growing (48) | Layered Cycle (24) |
|---|---:|---:|---:|
| R1 Zero-source | PASS | PASS | PASS |
| R2 Linearity | `R²=1.000000` | `R²=1.000000` | `R²=1.000000` |
| R3 Additivity | `1.80e-16` | `1.91e-16` | `1.63e-16` |
| R4 Force TOWARD | `+8.17e-03` | `+2.08e-03` | `+1.68e-02` |
| R5 Iterative stability | `30/30` TOWARD | `30/30` TOWARD | `30/30` TOWARD |
| R6 Norm | `4.44e-16` | `0.00e+00` | `2.22e-16` |
| R7 Families | `2/3` | `3/3` | `2/3` |
| R8 Gauge | `J_range=1.60e-02`, `sin R²=0.9999` | `J_range=3.08e-03`, `sin R²=0.9500` | `J_range=4.00e-02`, `sin R²=0.9736` |
| R9 Gap | `G_eff=157.8`, `shell_grad_ratio=0.005`, `spectral_ratio=0.020` | `G_eff=215.4`, `shell_grad_ratio=0.004`, `spectral_ratio=0.017` | `G_eff=99.5`, `shell_grad_ratio=0.009`, `spectral_ratio=0.021` |

## What Holds

- The coupled trajectory stays inward under the prescribed attractive sign on
  all three families, but the two-sign audit shows this is a field-profile
  diagnostic rather than standalone evidence of attractive gravity.
- Linearity and additivity remain machine-clean.
- Norm stays machine-clean.
- Native gauge closure still lands on actual graph cycles.

## What Breaks

- Family-family robustness is not universal yet.
- The `color-0` state is the failure mode on the random geometric and
  layered-cycle families.
- The force-scale gap remains structural: the graph-solved field is still
  smoother than the external kernel at these sizes.

## Interpretation

This is a genuine next-step field law, not just a re-labeled wave prototype.
The retarded memory channel preserves the core force battery on admissible
graph families, but it does not yet close the family-robustness row across
all initial-state sectors.

The retained takeaway is narrower than the wave prototype:

- graph-native causal memory is viable
- the force battery stays intact on the main coupled evolution
- sector robustness remains the next blocker
- on irregular graphs, the current sign rows are about an audited radial proxy,
  not an exact coordinate-force expectation or a sign-selection result
