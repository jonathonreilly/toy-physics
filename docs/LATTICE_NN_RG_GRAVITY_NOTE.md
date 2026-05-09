# NN Lattice RG-Style Gravity Note

**Date:** 2026-04-03  
**Status:** bounded - bounded or caveated result note
  fine-spacing failures are not schedule-discriminating
**Primary runner:** `scripts/lattice_nn_rg_gravity.py`


This note freezes the RG-style gravity probe on the raw nearest-neighbor lattice.
The question is narrow:

- does a simple spacing-dependent field-strength law preserve a finite gravity
  response under refinement, while keeping the raw Born-clean propagator?

Artifacts:

- [`scripts/lattice_nn_rg_gravity.py`](../scripts/lattice_nn_rg_gravity.py)
- [`logs/2026-04-03-lattice-nn-rg-gravity.txt`](../logs/2026-04-03-lattice-nn-rg-gravity.txt) — cached stdout covering h ∈ {2.0, 1.0, 0.5, 0.25} on all three schedules and the h=0.125 FAIL row
- upstream refinement note:
  [`scripts/lattice_nn_continuum.py`](../scripts/lattice_nn_continuum.py)

## Setup

- raw nearest-neighbor lattice only
- exactly 3 forward edges per node
- standard linear propagator only
- Born companion audit retained from the raw NN harness
- refinement points:
  - `h = 2.0, 1.0, 0.5, 0.25, 0.125`
- schedules:
  - `fixed`
  - `inv_h`
  - `inv_sqrt_h`

The field only changes in the gravity channel; the slit geometry and Born
companion audit are held fixed.

## Canonical Sweep

The three schedules share the same MI / decoherence / `d_TV` values at a given
`h`; only the gravity response changes.

### Fixed strength

| `h` | gravity | MI | `1-pur_cl` | `d_TV` | Born |
|---|---:|---:|---:|---:|---:|
| 2.0 | `-0.775486` | `0.5558` | `0.4215` | `0.7498` | `2.88e-16` |
| 1.0 | `-0.116678` | `0.5022` | `0.4229` | `0.7455` | `6.02e-16` |
| 0.5 | `+0.138226` | `0.7420` | `0.4844` | `0.9072` | `2.26e-16` |
| 0.25 | `+0.077415` | `0.9470` | `0.4989` | `0.9878` | `3.83e-16` |
| 0.125 | `FAIL` | `FAIL` | `FAIL` | `FAIL` | `FAIL` |

Finite-row fit:

```text
|gravity| ~ h^0.973, R^2 = 0.733
```

### `inv_h`

| `h` | strength | gravity | MI | `1-pur_cl` | `d_TV` | Born |
|---|---:|---:|---:|---:|---:|---:|
| 2.0 | `0.00025` | `-0.438446` | `0.5558` | `0.4215` | `0.7498` | `2.88e-16` |
| 1.0 | `0.0005` | `-0.116678` | `0.5022` | `0.4229` | `0.7455` | `6.02e-16` |
| 0.5 | `0.001` | `+0.183567` | `0.7420` | `0.4844` | `0.9072` | `2.26e-16` |
| 0.25 | `0.002` | `+0.139274` | `0.9470` | `0.4989` | `0.9878` | `3.83e-16` |
| 0.125 | `FAIL` | `FAIL` | `FAIL` | `FAIL` | `FAIL` | `FAIL` |

Finite-row fit:

```text
|gravity| ~ h^0.431, R^2 = 0.431
```

### `inv_sqrt_h`

| `h` | strength | gravity | MI | `1-pur_cl` | `d_TV` | Born |
|---|---:|---:|---:|---:|---:|---:|
| 2.0 | `0.000354` | `-0.583594` | `0.5558` | `0.4215` | `0.7498` | `2.88e-16` |
| 1.0 | `0.0005` | `-0.116678` | `0.5022` | `0.4229` | `0.7455` | `6.02e-16` |
| 0.5 | `0.000707` | `+0.159796` | `0.7420` | `0.4844` | `0.9072` | `2.26e-16` |
| 0.25 | `0.001` | `+0.104860` | `0.9470` | `0.4989` | `0.9878` | `3.83e-16` |
| 0.125 | `FAIL` | `FAIL` | `FAIL` | `FAIL` | `FAIL` | `FAIL` |

Finite-row fit:

```text
|gravity| ~ h^0.698, R^2 = 0.623
```

## Interpretation

The raw NN refinement trend is real through `h = 0.25`:

- Born stays machine-clean on the retained window
- MI rises toward `1.0`
- `1-pur_cl` rises toward `0.5`
- `d_TV` rises toward `1.0`
- gravity becomes small and positive at the refined points

But the RG-style strength scalings do **not** solve the fine-spacing problem:

- all three schedules still fail at `h = 0.125`
- in this harness that failure is shared by the field-free branch first, so the
  `h = 0.125` row is a raw-kernel continuation limit rather than a clean test
  of schedule-specific success or failure
- the simple `1/h` scaling changes the finite-row gravity trend but does not
  produce a clean finer-spacing continuation
- the nearby `1/sqrt(h)` scaling is similar: suggestive, but not decisive

So the narrow result is:

- simple spacing-dependent strength laws are **promising but incomplete**
- the continuum / renormalization question is still open
- the safest statement is a **finite-resolution Born-clean refinement law**, not a
  finished RG-fixed-point story

## Safe Conclusion

The nearest-neighbor lattice does support a Born-clean refinement window through
`h = 0.25`, and simple `h`-dependent strength laws slightly reshape the gravity
trend.

But the data do **not** yet justify a promoted renormalization claim.

The fitted exponents above should be read only as descriptive fits across the
finite retained rows. They are not clean refinement laws, because the coarse
rows and refined rows straddle a sign-flip regime.

Use this wording:

- the raw NN lattice shows a Born-clean refinement trend through `h = 0.25`
- simple `1/h`-style strength scaling is suggestive but not sufficient to extend
  the result cleanly to finer spacing
- the continuum / RG question remains open
