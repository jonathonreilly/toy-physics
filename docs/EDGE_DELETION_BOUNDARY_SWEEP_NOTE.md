# Edge Deletion Boundary Sweep Note

**Status:** bounded - bounded or caveated result note
This note freezes the bounded multi-seed replay of the retained 3D valley-linear family.

The question was whether the edge-deletion boundary seen in earlier graph-requirements work shows up as a stable 80%-90% connectivity transition on the same family when we sweep keep fractions across many seeds.

## Setup

- Family: retained 3D valley-linear family
- Lattice: `h=0.5`, `W=8`, `L=12`, `max_d=3`
- Keep fractions: `1.00`, `0.95`, `0.90`, `0.85`, `0.80`, `0.75`
- Seeds: 12 seeds, `20260404..20260415`
- Controls: one representative `100%` and `80%` Born / `k=0` / no-field sanity check

## Frozen Sweep

| keep fraction | TOWARD | mean delta | std delta |
| --- | ---: | ---: | ---: |
| 1.00 | 12/12 | +3.473338e-05 | 6.776264e-21 |
| 0.95 | 12/12 | +4.884894e-05 | 1.693359e-05 |
| 0.90 | 12/12 | +5.446079e-05 | 2.384982e-05 |
| 0.85 | 12/12 | +5.815760e-05 | 2.112014e-05 |
| 0.80 | 12/12 | +7.655170e-05 | 2.621961e-05 |
| 0.75 | 12/12 | +6.004755e-05 | 2.016072e-05 |

Representative controls:

- `100%`: Born `2.35e-15`, `k=0=+0.000e+00`, no-field `+0.000e+00`
- `80%`: Born `2.42e-15`, `k=0=+0.000e+00`, no-field `+0.000e+00`

## Honest Read

- The sweep is clean, but it does **not** show the expected 80%-90% sign transition on this retained family.
- The deflection stays TOWARD at every tested keep fraction and every tested seed.
- The mean delta stays positive and actually grows slightly as edges are deleted in this bounded range.
- Born, `k=0`, and no-field sanity checks remain clean at the representative seeds.

## Interpretation

This run does **not** support a sharp edge-deletion boundary on the retained 3D valley-linear family.

The safe conclusion is:

- graph damage up to 25% edge deletion is not enough to flip the sign here
- the earlier boundary behavior must depend on a different family, a different observable, or a harsher damage regime
- this replay should be treated as a bounded null result for the sign-flip boundary, not as evidence of a threshold transition

The artifact chain is therefore real, but the retained result is sign stability, not a transition.
