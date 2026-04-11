# Wilson Test-Mass / Continuum Companion

**Date:** 2026-04-11  
**Status:** bounded-retained Wilson companion  
**Scope:** same-convention open-boundary Wilson runners only

## Purpose

Freeze the late-2026-04-11 Wilson Newton-strengthening batch in its honest
form.

This note is intentionally narrower than a global Newton claim. It preserves:

- the weak-field **test-mass** result
- the first-order **perturbative mass-law** result
- the open-Wilson **continuum-limit** distance-law result

It does **not** close:

- full Hartree both-masses closure
- action-reaction / third-law closure
- architecture-independent Newton closure
- the broader normalization debate across mixed Wilson runners

## What Was Run

- [`scripts/frontier_test_mass_limit.py`](scripts/frontier_test_mass_limit.py)
- [`scripts/frontier_perturbative_mass_law.py`](scripts/frontier_perturbative_mass_law.py)
- [`scripts/frontier_continuum_limit.py`](scripts/frontier_continuum_limit.py)
- [`scripts/frontier_newton_systematic.py`](scripts/frontier_newton_systematic.py)

All four share the same open-Wilson convention:

- open 3D cubic Wilson surface
- complex Wilson hopping with `WILSON_R = 1`
- Poisson solve with `-4*pi*G*rho`
- low-screening regime `mu^2 = 0.001`

That common convention matters. These runners should be read as a **within-lane
Wilson calibration package**, not as a reconciliation of every older Wilson
script in the repo.

## Retained Read

### 1. Test-mass limit passes cleanly

On the weak-field audited surface (`G = 0.002`), the heavy-source / light-test
setup gives:

- source-mass exponent `1.002` with `R^2 = 1.000`
- distance exponent `-2.197` with `R^2 = 0.984`
- inward acceleration on every audited configuration

This is the cleanest mass-law result on the Wilson lane because the field is
sourced by the heavy packet only, avoiding Hartree self-field contamination in
the light packet.

### 2. First-order perturbative mass law is exact by construction

The perturbative Green-function extraction gives:

- source-mass exponent `1.0000` with `R^2 = 1.000`
- `G` exponent `1.0000`
- distance exponent `-1.916` with `R^2 = 0.9995`

This is useful as a same-convention theory companion, not as a standalone
headline. The linear mass and coupling exponents are exact at first order, so
the real content is:

- the clean separation of partner-force from self-field at weak coupling
- the comparison against the full Hartree lane, where higher-order corrections
  are visibly non-negligible

### 3. Open-Wilson continuum fit converges to `-2`

The size sweep on the same open-Wilson surface gives:

| `L` | `alpha(L)` | `R^2` |
|---|---:|---:|
| 12 | `-1.827` | `0.9991` |
| 15 | `-1.932` | `0.9993` |
| 18 | `-1.973` | `0.9997` |
| 20 | `-1.965` | `0.9999` |
| 22 | `-1.982` | `0.9999` |
| 25 | `-2.002` | `0.9999` |

The fitted continuum extrapolation is:

- `alpha_inf = -2.009 +/- 0.019`

That is strong evidence that the **distance-law side** of the Wilson lane is
Newton-compatible in the low-screening continuum-like regime.

## What This Does Not Close

### 1. Not full Newton closure

This note does **not** promote `F ∝ M1 M2 / r^2` as a retained repo truth.

Why:

- the valid Hartree both-masses lane still fails clean closure
- the test-mass setup only closes the source-mass half of the law
- the continuum result closes the distance exponent on the Wilson side lane,
  not the full two-body law on the same surface

### 2. Not a normalization verdict across all Wilson scripts

The same `-4*pi*G*rho` convention is used across this batch. That means these
results are internally coherent **within this lane**, but they do not by
themselves prove that earlier discrepancies elsewhere were solely a
normalization mistake.

Use this note with:

- [`scripts/frontier_newton_systematic.py`](scripts/frontier_newton_systematic.py)
- [`docs/WILSON_NORMALIZATION_RECONCILIATION_NOTE_2026-04-11.md`](WILSON_NORMALIZATION_RECONCILIATION_NOTE_2026-04-11.md)

and read that runner exactly as labeled: a same-convention sweep, not a global
normalization adjudicator.

### 3. Not primary-architecture closure

The primary staggered architecture already has its own bounded open-cubic
trajectory companions:

- [`docs/STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md`](STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md)
- [`docs/STAGGERED_NEWTON_BLOCKING_SENSITIVITY_NOTE_2026-04-11.md`](STAGGERED_NEWTON_BLOCKING_SENSITIVITY_NOTE_2026-04-11.md)

This Wilson note strengthens the cross-architecture picture, but it does not
replace the primary staggered bounded story.

## Safe Claim

The safe retained reading is:

> On the low-screening open-Wilson surface, the **test-mass** and
> **continuum-limit** companions support a Newton-compatible distance law and
> exact source-mass scaling within the shared Wilson convention, while full
> both-masses closure remains open.

## Promotion Boundary

Promote only as:

- a **bounded Wilson companion**
- paired with the existing Wilson open/two-body notes
- with explicit caveats that:
  - both-masses closure is still open
  - action-reaction remains unresolved
  - this is a same-convention Wilson result, not a global architecture claim
