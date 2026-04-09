# NN Lattice Mass-Response Note

**Date:** 2026-04-03  
**Status:** retained positive mass response under the Born-safe refinement path;
narrow alpha-scaled law is promising but still bounded

This note freezes the nearest-neighbor lattice mass-response follow-up.

## Mass Encoding

In this harness, "mass" is encoded as a **scalar field-strength multiplier on one
fixed mass node**.

- node count is held fixed
- mass placement is held fixed
- only the field-strength scale is changed

That keeps the question focused on response strength rather than on mass-size or
placement confounds.

Artifacts:

- [`scripts/lattice_nn_mass_response.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_nn_mass_response.py)
- [`logs/2026-04-03-lattice-nn-mass-response.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-nn-mass-response.txt)
- upstream refinement notes:
  - [`docs/LATTICE_NN_CONTINUUM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_NN_CONTINUUM_NOTE.md)
  - [`docs/LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md)
  - [`docs/LATTICE_NN_RG_GRAVITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LATTICE_NN_RG_GRAVITY_NOTE.md)

## Deterministic Refinement Path

The Born-safe deterministic refinement path keeps the nearest-neighbor lattice
clean all the way through the currently retained sub-`0.25` window.

Canonical rows:

| `h` | gravity | `MI` | `1 - pur_cl` | `d_TV` | Born |
|---|---:|---:|---:|---:|---:|
| 1.0 | `-0.116678` | `0.5022` | `0.4229` | `0.7455` | `4.74e-16` |
| 0.5 | `+0.138226` | `0.7420` | `0.4844` | `0.9072` | `5.09e-16` |
| 0.25 | `+0.077415` | `0.9470` | `0.4989` | `0.9878` | `6.04e-16` |
| 0.125 | `+0.034466` | `0.9972` | `0.5000` | `0.9996` | `7.86e-16` |
| 0.0625 | `+0.014810` | `1.0000` | `0.5000` | `1.0000` | `3.00e-16` |

Safe read:

- gravity flips positive by `h = 0.5`
- the mass response remains positive on the retained Born-safe path
- `MI` rises smoothly toward `1.0`
- `1 - pur_cl` rises smoothly toward `0.5`
- `d_TV` rises smoothly toward `1.0`
- gravity shrinks toward zero as refinement continues
- Born stays at machine precision at every retained spacing

## Narrow Alpha-Scaled Probe

A narrow alpha-scaled strength law makes the gravity response noticeably more
stable between `h = 0.5` and `h = 0.25`, but it does not justify a promoted
`F∝M` claim.

| `alpha` | `g(h=0.5)` | `g(h=0.25)` | ratio | read |
|---|---:|---:|---:|---|
| 0.0 | `+0.138` | `+0.077` | `0.56` | decaying |
| 0.5 | `+0.160` | `+0.105` | `0.66` | decaying |
| 1.0 | `+0.184` | `+0.139` | `0.76` | nearly h-independent |
| 1.5 | `+0.209` | `+0.180` | `0.86` | nearly h-independent |

Born spot-check on the narrow alpha probe:

- `alpha = 1.0` and `alpha = 1.5` stayed at machine precision on the checked
  rows
- that is enough to say the alpha-scaling is Born-compatible in this narrow
  window, but not enough to promote a continuum law

## Interpretation

The NN mass-response story is now narrower and cleaner:

- the mass response stays positive on the Born-safe deterministic refinement path
- the response becomes cleaner under refinement, but gravity still fades toward
  zero at the finest retained deterministic point
- the narrow alpha-scaled probe makes gravity less spacing-sensitive, with
  `alpha ~ 1.5` the cleanest checked value
- the response is positive but bounded/sub-linear and still refinement-sensitive

## Safe Conclusion

Use this wording:

- the nearest-neighbor lattice has a retained positive mass response under the
  Born-safe refinement path
- a narrow alpha-scaled strength law makes the response cleaner over the tested
  window
- the response is not promoted as `F∝M`; it is positive but bounded/sub-linear
  and the continuum-side gravity question remains open

