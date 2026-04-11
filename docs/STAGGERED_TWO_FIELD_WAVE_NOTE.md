# Staggered Two-Field Wave Coupling — Retained Note

**Date:** 2026-04-10
**Script:** `frontier_two_field_wave.py`

## Summary

This hardens the earlier two-field proof of concept by replacing the scalar
field relaxation update with a wave equation:

`d²Φ/dt² = -c² (L + μ²) Φ + β |ψ|²`

The matter field `ψ` still evolves by Crank-Nicolson under the prescribed
attractive coupling `V = -m Φ`. The
current retained read is:

- hard score `5/5` on all three retained cycle-bearing graph families
- `W5` width response is a diagnostic, not a hard gate

## Hard Gates

| Row | Random Geometric (36) | Growing (48) | Layered Cycle (24) |
|-----|:---:|:---:|:---:|
| W1 Φ responds | ✅ | ✅ | ✅ |
| W2 Inward retained proxy | 30/30 | 30/30 | 30/30 |
| W3 ψ norm | 1.1e-15 | 2.2e-16 | 2.2e-16 |
| W4 Φ bounded | ✅ | ✅ | ✅ |
| W6 Families | 3/3 | 3/3 | 3/3 |
| **Hard score** | **5/5** | **5/5** | **5/5** |

## Width Diagnostic

| Family | Final width ratio vs free |
|-----|-----:|
| Random geometric | `0.9997` |
| Growing | `1.0006` |
| Layered cycle | `1.0028` |

So the wave-field hardening closes the structural interaction / norm / family
story cleanly, but it does **not** give universal contraction on this retained
operating point.

## What This Proves

- a separate scalar field `Φ` can have its own hyperbolic dynamics on the same
  admissible graph families
- the coupled retained proxy stays inward for every iteration on all retained
  families under the prescribed attractive sign
- the matter norm stays exact while `Φ` remains bounded
- the state-family robustness seen in the static-potential and self-gravity
  probes survives the wave-field upgrade

## What It Does Not Yet Prove

- universal wave-mediated contraction
- a retained larger-graph wave battery
- retarded-field closure beyond this first hyperbolic prototype

## Next Seam

The next meaningful experiment is not another score bump. It is to test whether
the wave-field law can be made both:

1. graph-native and retained on larger cycle-bearing families
2. closer to the retained nonlocal / Green-closure force scale without losing
   the current hard `5/5`
