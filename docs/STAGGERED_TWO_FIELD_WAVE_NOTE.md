# Staggered Two-Field Wave Coupling — Rerun-Corrected Note

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-10
**Script:** `frontier_two_field_wave.py`
**Status on current `main`:** bounded wave-field result after the 2026-04-18
clean-family rerun; no longer a retained `5/5` family-robust closure

## Summary

This hardens the earlier two-field proof of concept by replacing the scalar
field relaxation update with a wave equation:

`d²Φ/dt² = -c² (L + μ²) Φ + β |ψ|²`

The matter field `ψ` still evolves by Crank-Nicolson under the corrected
parity coupling `H_diag = (m + Φ) ε`. The
current corrected read is:

- `W1`-`W4` still hold on all three retained cycle-bearing graph families
- `W5` width response is a diagnostic, not a hard gate
- `W6` family robustness is evaluated from fresh `Φ=0`, `dΦ/dt=0` initial
  data for each family, so it is not contaminated by the first branch's
  evolved field history
- with that clean restart, `W6` closes only on the growing family, giving hard
  scores `4/5`, `5/5`, `4/5` on random geometric, growing, and layered cycle

## Hard Gates

| Row | Random Geometric (36) | Growing (48) | Layered Cycle (24) |
|-----|:---:|:---:|:---:|
| W1 Φ responds | ✅ | ✅ | ✅ |
| W2 Inward retained proxy | 30/30 | 30/30 | 30/30 |
| W3 ψ norm | 1.1e-15 | 2.2e-16 | 2.2e-16 |
| W4 Φ bounded | ✅ | ✅ | ✅ |
| W6 Families | 2/3 | 3/3 | 2/3 |
| **Hard score** | **4/5** | **5/5** | **4/5** |

## Width Diagnostic

| Family | Final width ratio vs free |
|-----|-----:|
| Random geometric | `1.0047` |
| Growing | `1.0019` |
| Layered cycle | `0.9923` |

So the wave-field hardening still closes the interaction / norm / bounded-field
story cleanly, but it does **not** close the full state-family battery and it
does **not** give universal contraction on this operating point.

## What This Proves

- a separate scalar field `Φ` can have its own hyperbolic dynamics on the same
  admissible graph families
- the coupled retained proxy stays inward for every iteration on all retained
  families under the corrected parity coupling
- the matter norm stays exact while `Φ` remains bounded
- the growing-family state-robustness row survives the wave-field upgrade even
  when each family is restarted from a fresh zero-field initial condition

## What It Does Not Yet Prove

- retained state-family robustness across all three admissible graph families
- universal wave-mediated contraction
- a retained larger-graph wave battery
- retarded-field closure beyond this first hyperbolic prototype

## Next Seam

The next meaningful experiment is not another score bump. It is to test whether
the wave-field law can be made both:

1. graph-native and retained on larger cycle-bearing families
2. closer to the retained nonlocal / Green-closure force scale without losing
   the current hard `5/5`
