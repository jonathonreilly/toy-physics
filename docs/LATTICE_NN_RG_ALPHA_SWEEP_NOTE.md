# NN Lattice RG Alpha Sweep Note

**Date:** 2026-04-03  
**Status:** bounded - bounded or caveated result note
  the closest to h-stability on the tested grid

This note freezes the alpha-sweep follow-up to the Born-safe nearest-neighbor
lattice refinement path.

The question is narrow:

- if the mass proxy is scaled as `strength = s0 / h^alpha`, is there an alpha
  that makes the gravity response nearly h-independent between `h = 0.5` and
  `h = 0.25`, while keeping the deterministic Born-safe refinement path intact?

Artifacts:

- [`scripts/lattice_nn_rg_alpha_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_nn_rg_alpha_sweep.py)
- [`logs/2026-04-03-lattice-nn-rg-alpha-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-nn-rg-alpha-sweep.txt)
- upstream deterministic refinement:
  [`docs/LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md)

## Setup

- raw nearest-neighbor lattice with exactly 3 forward edges per node
- deterministic, geometry-only rescale schedule
- Born companion audit retained from the deterministic NN harness
- `h` values: `1.0`, `0.5`, `0.25`
- alpha sweep:
  - `0.0`
  - `0.5`
  - `1.0`
  - `1.5`

The observable comparison is deliberately focused on the pair `h = 0.5` vs.
`h = 0.25`, since that is where the near-fixed-point behavior is supposed to
show up.

## Canonical Sweep

The shared Born companion audit stays machine-clean throughout the sweep.

| alpha | gravity@h=0.5 | gravity@h=0.25 | ratio `g(0.25)/g(0.5)` | pair exponent | Born |
|---|---:|---:|---:|---:|---:|
| `0.0` | `+0.138226` | `+0.077415` | `0.560` | `0.836` | `4.74e-16` / `5.09e-16` / `6.04e-16` |
| `0.5` | `+0.159796` | `+0.104860` | `0.656` | `0.608` | `4.74e-16` / `5.09e-16` / `6.04e-16` |
| `1.0` | `+0.183567` | `+0.139274` | `0.759` | `0.398` | `4.74e-16` / `5.09e-16` / `6.04e-16` |
| `1.5` | `+0.209207` | `+0.179561` | `0.858` | `0.220` | `4.74e-16` / `5.09e-16` / `6.04e-16` |

The same deterministic path keeps:

- `k = 0` exactly zero
- `MI`, `1-pur_cl`, and `d_TV` on the same Born-safe refinement trend as the
  underlying deterministic NN lattice

## Interpretation

The alpha sweep does support the fixed-point-style claim that stronger
`h`-dependent coupling makes the gravity response *less* sensitive to refinement.

- alpha `0.0` has the strongest decay between `h = 0.5` and `h = 0.25`
- alpha `1.5` is the closest to h-independence among the measured values
- the measured ratio at alpha `1.5` is `0.858`, which is close but not flat

So the safe conclusion is:

- within the scanned grid, the strongest checked alpha is `1.5`
- the gravity response is **nearly** stable between `h = 0.5` and `h = 0.25`
- but the result is still a **fixed-point style probe**, not a promoted
  renormalization theorem

This should not be read as an optimized or final exponent:

- the trend improves monotonically across the scanned alpha grid
- `h = 1.0` remains negative for every scanned alpha
- so the current result is a bounded scan edge, not a solved RG closure

## Safe Conclusion

Use this wording:

- the Born-safe deterministic NN refinement path supports a narrow RG-style
  alpha sweep
- within the scanned grid, the strongest checked alpha is `1.5`
- at that alpha, gravity is nearly h-independent between `h = 0.5` and
  `h = 0.25`, with ratio `0.858`
- the evidence is promising but not yet strong enough to call the continuum
  theory renormalized

Do **not** use:

- renormalizable continuum theory
- fixed point established
- RG solved
- h-independence proven
