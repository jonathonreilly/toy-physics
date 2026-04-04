# Decoherence is Action-Independent

**Date:** 2026-04-04
**Status:** Confirmed — exact numerical identity across actions

## Finding

On the 3D 1/L^2 lattice, the decoherence observables (d_TV, MI,
CL bath purity, S_norm) are EXACTLY IDENTICAL for the valley-linear
and spent-delay actions at every tested lattice spacing.

| h | d_TV (both) | MI (both) | Decoh (both) | S_norm (both) |
|---|-------------|-----------|--------------|---------------|
| 1.0 | 0.627 | 0.414 | 30.2% | 0.390 |
| 0.5 | 0.786 | 0.588 | 49.4% | 0.701 |
| 0.25 | 0.830 | 0.647 | 49.9% | 0.807 |

## Why

The decoherence test uses zero field (no mass). Both actions reduce
to S = L × const at zero field. The amplitude magnitude at each node
depends only on the kernel (1/L^2) and the angular weight (exp(-βθ²)),
which are shared by both actions. The action only changes the PHASE
(via exp(ikS)), and the CL bath measurement depends on amplitude
MAGNITUDES at intermediate layers.

## Implications

The model cleanly separates:
- **Gravity**: action-dependent (valley-linear → Newtonian, spent-delay → sqrt)
- **Decoherence**: geometry-dependent (lattice structure + slits)
- **Born rule**: linearity-dependent (both actions are linear)

This means the action can be optimized for gravity without affecting
decoherence. The valley-linear action gives Newtonian gravity AND
the same decoherence as spent-delay — no trade-off.

## Convergence

The decoherence converges as h → 0:
- d_TV: 0.63 → 0.79 → 0.83 (approaching 1.0)
- MI: 0.41 → 0.59 → 0.65 (approaching ~0.7?)
- Decoherence: 30% → 49% → 50% (converged to 50%)
- S_norm: 0.39 → 0.70 → 0.81 (approaching 1.0)

This convergence is a property of the LATTICE, not the action.
