# Lattice NN Deterministic Rescale Note

**Date:** 2026-04-03  
**Status:** bounded - bounded or caveated result note
**Primary runner:** [`scripts/lattice_nn_deterministic_rescale.py`](../scripts/lattice_nn_deterministic_rescale.py) (deterministic geometric rescale schedule, Born-clean through h=0.0625)

This note freezes the deterministic-rescale follow-up to the raw nearest-neighbor
lattice continuum harness.

The question is deliberately narrow:

- can a fixed, geometry-only rescale schedule push the NN lattice below
  `h = 0.25` while keeping the Born check clean enough to matter?

Artifacts:

- [`scripts/lattice_nn_deterministic_rescale.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_nn_deterministic_rescale.py)
- [`logs/2026-04-03-lattice-nn-deterministic-rescale.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-nn-deterministic-rescale.txt)
- upstream raw NN refinement:
  [`scripts/lattice_nn_continuum.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_nn_continuum.py)

## Schedule

The schedule is fixed and deterministic:

- raw NN geometry
- 3 forward edges per node
- per-step rescale factor `spacing / sqrt(3)`
- the factor is geometry-only and is applied identically across all propagation
  runs
- no layer normalization and no amplitude-dependent rescaling

## Canonical Rows

| `h` | nodes | `MI` | `1-pur_cl` | `d_TV` | gravity | `k=0` | Born `|I3|/P` |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1.0 | 1,681 | `0.5022` | `0.4229` | `0.7455` | `-0.116678` | `0` | `4.74e-16` |
| 0.5 | 6,561 | `0.7420` | `0.4844` | `0.9072` | `+0.138226` | `0` | `5.09e-16` |
| 0.25 | 25,921 | `0.9470` | `0.4989` | `0.9878` | `+0.077415` | `0` | `6.04e-16` |
| 0.125 | 103,041 | `0.9972` | `0.5000` | `0.9996` | `+0.034466` | `0` | `7.86e-16` |
| 0.0625 | 410,881 | `1.0000` | `0.5000` | `1.0000` | `+0.014810` | `0` | `3.00e-16` |

## Interpretation

The deterministic schedule does what the raw NN branch suggested might be
possible:

- it extends the lattice cleanly below `h = 0.25`
- Born stays at machine precision at every tested spacing
- `k=0` stays exactly zero
- MI rises smoothly toward `1.0` bit
- decoherence rises smoothly toward `50%`
- `d_TV` rises smoothly toward `1.0`
- gravity remains positive, but it shrinks toward zero as the lattice is refined

The key distinction from the earlier periodic-rescale attempt is that this
schedule is fixed by geometry, not by amplitude or by the specific blocked-set
configuration of a given propagation run.

## Safe Conclusion

The review-safe result is:

- **Born-safe deterministic extension works through `h = 0.0625`**
- the observables converge smoothly under the fixed schedule
- the remaining open question is not Born safety, but how to interpret the
  vanishing gravity scale in the finer-spacing limit

Do **not** overstate this as a finished continuum theory. The canonical claim is
the narrower one above: a deterministic, Born-clean refinement path exists on
the raw NN lattice through the tested sub-`0.25` regime.
