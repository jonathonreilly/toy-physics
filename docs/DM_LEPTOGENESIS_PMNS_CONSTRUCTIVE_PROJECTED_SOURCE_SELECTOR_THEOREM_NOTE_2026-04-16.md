# DM Leptogenesis PMNS Constructive Projected-Source Selector Theorem

**Date:** 2026-04-16  
**Status:** exact constructive theorem on the open PMNS comparator gate  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_constructive_projected_source_selector_theorem.py`

## Question

Is the constructive projected-source sign chamber on the current PMNS branch
actually empty or transport-incompatible, or does there already exist an exact
`D_- / dW_e^H` witness with

- `gamma > 0`
- `E1 > 0`
- `E2 > 0`

on the fixed native `N_e` seed surface?

## Bottom line

It already exists.

The constructive sign chamber is not only nonempty. It already intersects the
current transport-extremal class.

An explicit witness on the fixed native seed surface is:

- `x = (1.174161560603, 0.462544348009, 0.053294091387)`
- `y = (0.758741415897, 0.026904299513, 0.134354284590)`
- `delta = 1.882595756164`

Its projected-source / breaking-triplet data are:

- `gamma = 0.150147244666`
- `E1 = 0.296562850784`
- `E2 = 1.986407435174`
- `(cp1, cp2) = (-0.029685396610, +0.198835735450)`

and its exact flavored transport values are:

- `eta/eta_obs = (0.929320928295, 1.052220313052, 0.801490032771)`

So the current PMNS branch is **not** blocked by incompatibility between
constructive CP and transport closure.

## Exact projected-source read

For that same witness the projected Hermitian response pack on `E_e` is

- `(R11, R22, R33, S12, A12, S13, A13, S23, A23)`
- `= (1.954343906595, 0.214671115208, 0.020891333964, 0.701903107048, 0, -0.096788733600, 0.300294489332, 0.002867680394, 0)`

So directly at `dW_e^H` level:

- `gamma = A13 / 2 = 0.150147244666 > 0`
- `E1 = (R22 - R33)/2 + (S12 - S13)/4 = 0.296562850784 > 0`
- `E2 = R11 + (S12 + S13)/4 - (R22 + R33)/2 - S23/2 = 1.986407435174 > 0`

The constructive sheet is therefore already exact on `dW_e^H`, not only in the
off-seed PMNS coordinates.

## Why this matters

The previous exact selector-bank theorem said the current PMNS selector laws
are transport-constructive but CP-sheet blind.

This theorem sharpens that.

The issue is **not**:

- impossibility of `gamma > 0`, `E1 > 0`, `E2 > 0`
- incompatibility of that sign system with `eta > 1`

Those are now closed positively.

The actual remaining problem is narrower:

- derive the microscopic `D_- / dW_e^H` selector law that chooses this
  constructive sheet uniquely rather than leaving the transport-extremal class
  CP-sheet blind

## Exact selector consequence

On the current branch, the clean constructive selector can now be stated
directly:

- maximize exact flavored transport over the projected-source sign chamber
  `gamma > 0`, `E1 > 0`, `E2 > 0`

This sign-constrained selector already saturates the unconstrained
transport-extremal value

- `eta/eta_obs = 1.052220313052`

so it is not transport-inferior on the current PMNS branch.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_constructive_projected_source_selector_theorem.py
```
