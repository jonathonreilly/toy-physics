# Staggered Backreaction Nonlocal Closure Note

**Date:** 2026-04-10
**Status:** retained negative for the force-scale blocker; useful structural improvement over the local screened-Poisson baseline, but not a material win over the best calibrated linear source map

## Question

Can a genuinely different source sector, implemented as a nonlocal / fractional-Green
source-to-field map, reduce the over-smoothing diagnosed in the shell / spectral
probe while preserving the retained staggered battery?

## Harness

- Script: [`frontier_staggered_backreaction_nonlocal_closure.py`](../scripts/frontier_staggered_backreaction_nonlocal_closure.py)
- Families:
  - bipartite random geometric, `n=36` (cycle-bearing)
  - bipartite growing, `n=48` (cycle-bearing)
  - layered bipartite DAG-compatible, `n=36` (holdout)
- Source sector:
  - fractional Green operator in Laplacian spectral space,
    `(L + mu^2 I)^(-alpha)`
  - sweep over `alpha in {1.00, 0.80, 0.60, 0.40, 0.20, 0.10, 0.00}`
- Observable:
  - force remains primary: `F = < -dPhi/dd >`
  - compare to the external-kernel control

## Exact Results

### Calibrated Cycle-Bearing Gap

The source sector is calibrated with one global gain on the two cycle-bearing
families only, then evaluated on the layered holdout.

| alpha | best gain | cycle-bearing mean gap |
|---|---:|---:|
| `1.00` | `9.190` | `1.315e-01` |
| `0.80` | `9.190` | `1.203e-01` |
| `0.60` | `9.190` | `1.104e-01` |
| `0.40` | `9.190` | `1.016e-01` |
| `0.20` | `9.190` | `9.357e-02` |
| `0.10` | `9.190` | `8.972e-02` |
| `0.00` | `9.190` | `8.590e-02` |

Best nonlocal point:

- `alpha = 0.00`
- cycle-bearing calibrated gap `= 8.590e-02`
- improvement vs the local screened-Poisson baseline in this harness:
  `1.53x`

Comparison to the previously best calibrated linear source map:

- prior calibrated linear benchmark: `6.099e-02`
- best nonlocal result here: `8.590e-02`
- result: the nonlocal family **does not beat** the calibrated linear benchmark

## Retained Checks

At the best point (`alpha=0.00`), the retained battery stays intact:

- source-response linearity:
  - cycle-bearing mean `R^2 = 0.9992`
- two-body additivity:
  - max residual `6.433e-16`
- norm stability:
  - max drift `8.882e-16`
- force sign:
  - `3/3` TOWARD on every family

## Holdout

The layered DAG-compatible family remains a holdout, but it is closer under the
best nonlocal map:

- local screened-Poisson baseline holdout gap: `1.446e-01`
- best nonlocal holdout gap: `5.964e-02`

That is a real improvement, but it still does not close the force-scale blocker
on the cycle-bearing families.

## Shell / Spectral Readout

The nonlocal fractional family moves the field shape, but it remains low-mode
heavy relative to the external kernel.

Best candidate shell/spectral summary:

- `bipartite_random_geometric`
  - shell ratio `0.095`
  - shell fit `R^2 = 0.8532`
  - low-mode fraction: solved `0.751`, external `0.453`
  - spectral centroid: solved `7.435e-01`, external `1.574e+00`
- `bipartite_growing`
  - shell ratio `0.096`
  - shell fit `R^2 = 0.9065`
  - low-mode fraction: solved `0.501`, external `0.331`
  - spectral centroid: solved `8.524e-01`, external `1.384e+00`

Interpretation:

- shrinking `alpha` helps the force-scale gap
- but even the best nonlocal point stays flatter and more low-mode dominated
  than the external kernel
- the source-sector miss is therefore not fixed by this fractional-Green family

## Readout

- The nonlocal fractional-Green source sector is a genuine change from the
  local screened-Poisson map.
- It improves the cycle-bearing force gap relative to the local screened
  baseline, and it preserves TOWARD sign, linearity, additivity, and norm
  stability.
- It does **not** materially improve beyond the previously best calibrated
  linear source map.
- The remaining blocker is still structural over-smoothing in the graph source
  sector.

## Next Step

- Try a different source sector again only if it is materially different from
  both the local screened solve and the fractional inverse family.
- Keep the layered holdout in every comparison.
- Keep force as the primary observable.
