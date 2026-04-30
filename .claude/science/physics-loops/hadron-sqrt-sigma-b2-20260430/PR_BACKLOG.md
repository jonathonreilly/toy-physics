# PR Backlog

## Block 01

Title candidate:

```text
Lane 1: repair sqrt(sigma) B2 screening gate
```

Summary:

- Adds a runner-backed audit showing the existing rough x0.96 screening
  factor cannot promote `sqrt(sigma)`.
- Splits B2 into B2a observable-definition and B2b bridge-value gates.
- Adds a static-energy bridge scout: TUMQCD finite-window `sigma` is
  useful but convention-split, while CLS `N_f=2+1` `r0`/`r1` force
  scales are clean but do not uniquely map to `sqrt(sigma)`.
- Updates Lane 1 and the canonical harness index.

Test:

```bash
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b2_gate_repair.py
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b2_static_energy_bridge.py
```
