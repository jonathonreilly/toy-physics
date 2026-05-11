# Staggered Backreaction Shell / Spectral Note

**Date:** 2026-04-10  
**Status:** proposed_retained structural diagnostic
**Claim type:** positive_theorem

**Audit-conditional perimeter (2026-04-26):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
positive_theorem`. The audit chain-closure explanation is exact: "The
live runner reproduces the shell/spectral over-smoothing diagnosis,
including shell span ratios 0.123 and 0.229 and solved/external low-
mode fractions 0.958/0.453 and 0.809/0.355, but the note's exact
force readouts are stale against current output." This rigorization
edit only sharpens the boundary of the conditional perimeter; nothing
here promotes audit status. The supported content of this note is
the structural shell/spectral over-smoothing diagnosis itself: the
shell span ratios (0.123 cycle-bearing, 0.229 layered) and the low-
mode fractions (0.958/0.453 and 0.809/0.355) match the live runner
output exactly. The numerical force readouts (`F_ext`, `F_solve`,
`force gap`) are stale against current output and are bounded
finite-snapshot values rather than load-bearing structural conclusions
of this note. A future runner-source rerun would refresh those force
columns; the structural diagnosis (over-smoothing direction, low-mode
concentration) is unchanged.

## Question

Why is the source-generated staggered `Phi` too weak relative to the
external-kernel control on the cycle-bearing graph families, even though the
force sign, linearity, additivity, and norm stability all survive?

## Harness

- Script: [`frontier_staggered_backreaction_shell_spectral.py`](../scripts/frontier_staggered_backreaction_shell_spectral.py)
- Families:
  - bipartite random geometric, `n=36` (cycle-bearing)
  - layered bipartite DAG-compatible, `n=36` (layered holdout)
- Observable:
  - `phi_solved(depth)` vs `phi_ext(depth)` shell profiles
  - low-mode content of `rho`, `phi_solved`, and `phi_ext`
  - force remains the primary gravity observable

## Exact Diagnostics

### Cycle-Bearing Family: `bipartite_random_geometric`

| depth | count | `rho_drop` | `phi_solved` | `phi_ext` | solve/ext |
|---|---:|---:|---:|---:|---:|
| 0 | 1 | `0.000e+00` | `0.000e+00` | `0.000e+00` | `0.000` |
| 1 | 2 | `1.750e-01` | `1.319e-01` | `3.454e+00` | `0.038` |
| 2 | 3 | `3.204e-01` | `2.666e-01` | `3.744e+00` | `0.071` |
| 3 | 4 | `3.707e-01` | `3.620e-01` | `3.869e+00` | `0.094` |
| 4 | 5 | `3.781e-01` | `4.157e-01` | `3.923e+00` | `0.106` |
| 5 | 6 | `3.789e-01` | `4.458e-01` | `3.953e+00` | `0.113` |
| 6 | 5 | `3.790e-01` | `4.606e-01` | `3.965e+00` | `0.116` |
| 7 | 4 | `3.790e-01` | `4.722e-01` | `3.974e+00` | `0.119` |
| 8 | 3 | `3.790e-01` | `4.814e-01` | `3.982e+00` | `0.121` |
| 9 | 2 | `3.790e-01` | `4.878e-01` | `3.987e+00` | `0.122` |
| 10 | 1 | `3.790e-01` | `4.914e-01` | `3.991e+00` | `0.123` |

Summary:

- `F_ext = +3.247e-01`
- `F_solve = +4.002e-02`
- force gap `= 8.767e-01`
- shell slope: solve `+4.355e-02`, ext `+2.096e-01`
- shell span ratio `= 0.123`
- shell fit `R² = 0.6700`
- low-mode fractions: `rho = 0.751`, solved `0.958`, external `0.453`
- spectral centroids: `rho = 7.435e-01`, solved `3.980e-01`, external `1.574e+00`

### Layered Family: `layered_bipartite_dag`

| depth | count | `rho_drop` | `phi_solved` | `phi_ext` | solve/ext |
|---|---:|---:|---:|---:|---:|
| 0 | 1 | `0.000e+00` | `0.000e+00` | `0.000e+00` | `0.000` |
| 1 | 1 | `3.912e-01` | `4.540e-01` | `3.824e+00` | `0.119` |
| 2 | 1 | `3.929e-01` | `6.211e-01` | `3.828e+00` | `0.162` |
| 3 | 1 | `4.108e-01` | `7.806e-01` | `3.913e+00` | `0.200` |
| 4 | 1 | `4.116e-01` | `8.642e-01` | `3.952e+00` | `0.219` |
| 5 | 1 | `4.116e-01` | `8.933e-01` | `3.977e+00` | `0.225` |
| 6 | 1 | `4.116e-01` | `9.051e-01` | `3.986e+00` | `0.227` |
| 7 | 1 | `4.116e-01` | `9.123e-01` | `3.991e+00` | `0.229` |

Summary:

- `F_ext = +1.714e+00`
- `F_solve = +2.127e-01`
- force gap `= 8.759e-01`
- shell slope: solve `+1.136e-01`, ext `+3.480e-01`
- shell span ratio `= 0.229`
- shell fit `R² = 0.7799`
- low-mode fractions: `rho = 0.379`, solved `0.809`, external `0.355`
- spectral centroids: `rho = 5.457e-01`, solved `1.741e-01`, external `4.884e-01`

## Readout

- The solved field preserves sign and linearity, but it is much flatter in
  depth than the external-kernel control on both families.
- The cycle-bearing family is the clearest structural miss: the shell span is
  only `12.3%` of the external control, and the solved spectrum is strongly
  concentrated in the lowest modes.
- The layered family is less flattened than the cycle-bearing family, but it
  still shows the same direction of miss: smaller shell slope, smaller span,
  and lower spectral centroid than the external kernel.
- The source density itself is already shell-localized, but the screened graph
  Poisson solve pushes the field farther into the low-mode regime than the
  external kernel does.

## Interpretation

The force-scale gap is not just a normalization constant.

It is a structural over-smoothing of the source-to-field map:

- the source density is localized
- `phi_solved` is smoother and more low-mode dominated
- the external kernel stays much steeper in depth
- the force therefore comes out positive but too weak

This explains why the iterative and scale-closure probes moved the gap only
partially: they can rescale the field, but they do not remove the underlying
flattening of the graph-Poisson solve on cycle-bearing families.

## Next Step

- Try a different source-to-field map or a genuinely nonlinear iterative
  closure that preserves the retained force battery while recovering more depth
  contrast on cycle-bearing graphs.
- Keep the layered family as the holdout for whether a proposed normalization
  is universal or cycle-specific.
