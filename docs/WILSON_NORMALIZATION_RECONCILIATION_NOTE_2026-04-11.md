# Wilson Normalization / Comparison Reconciliation

**Date:** 2026-04-11  
**Status:** support - methodological control note
**Scope:** late-2026-04-11 Wilson Newton-strengthening batch
**Primary runner:** [`scripts/frontier_test_mass_limit.py`](../scripts/frontier_test_mass_limit.py) (mass exp 1.002, distance exp -2.197, all PASS)

## Purpose

Prevent future summaries from collapsing several different Wilson runners into a
single story like:

> “the bad exponent came from a `4*pi` normalization mistake.”

That statement is too strong for the current evidence.

## What Is Actually True

The late Wilson batch is internally coherent **within one shared convention**:

- open 3D cubic Wilson surface
- complex Wilson hopping
- Poisson solve with `-4*pi*G*rho`
- low-screening regime `mu^2 = 0.001`

Within that convention, the following are all consistent with each other:

- [`scripts/frontier_newton_systematic.py`](../scripts/frontier_newton_systematic.py)
- [`scripts/frontier_test_mass_limit.py`](../scripts/frontier_test_mass_limit.py)
- [`scripts/frontier_perturbative_mass_law.py`](../scripts/frontier_perturbative_mass_law.py)
- [`scripts/frontier_continuum_limit.py`](../scripts/frontier_continuum_limit.py)

The safe conclusion is:

> within this same-convention open-Wilson lane, the weak-field test-mass and
> continuum companions support Newton-compatible scaling.

## What Is Not Proven

The current repo does **not** prove that `4*pi` alone caused every earlier
Wilson discrepancy.

Why not:

- older runners differed in more than Poisson source convention
- some also differed in:
  - screening regime
  - observable definition
  - geometry / boundary conditions
  - hopping convention
  - strong- vs weak-field operating point

So cross-runner disagreements cannot be attributed to the `4*pi` factor alone
unless all other differences are controlled simultaneously.

## Valid And Invalid Comparisons

### Valid

- compare the late Wilson batch **to itself**
- compare weak-field vs stronger-field behavior on the same open-Wilson surface
- compare screened vs low-screening exponents on the same observable family

### Invalid without further controls

- treating a mixed-runner exponent mismatch as a pure normalization diagnosis
- using the test-mass or perturbative runner as if it independently closes the
  both-masses Hartree lane
- reading the bounded Wilson companion as an architecture-wide Newton closure

## Reading Rule

If a Wilson summary uses one of:

- `frontier_test_mass_limit.py`
- `frontier_perturbative_mass_law.py`
- `frontier_continuum_limit.py`
- `frontier_newton_systematic.py`

then it must also preserve this sentence or an equivalent one:

> This is a same-convention open-Wilson calibration result, not a global
> normalization verdict across mixed Wilson runners.
