# Gravity-Cosmology Tower Lambda Spectral Bridge Theorem

**Date:** 2026-04-25

**Status:** proposed_retained structural bridge. This note re-expresses the
retained spin-2, spin-1, and spin-0 spectral towers on the retained
`S^3` geometry in pure cosmological-constant units using the retained
identity `Lambda = 3/R^2`.

**Primary runner:**
`scripts/frontier_gravity_cosmology_tower_lambda_spectral_bridge.py`

## Statement

The retained tower formulas are:

```text
m_TT(l)^2     = (l(l+2) - 2) hbar^2/(c^2 R^2),  l >= 2
m_vec(l)^2    = (l(l+2) - 1) hbar^2/(c^2 R^2),  l >= 1
m_scalar(l)^2 = l(l+2)       hbar^2/(c^2 R^2),  l >= 0
```

Substituting `1/R^2 = Lambda/3` gives the pure-Lambda forms:

```text
(L1) m_TT(l)^2     = ((l(l+2) - 2)/3) hbar^2 Lambda/c^2,  l >= 2
(L2) m_vec(l)^2    = ((l(l+2) - 1)/3) hbar^2 Lambda/c^2,  l >= 1
(L3) m_scalar(l)^2 = (l(l+2)/3)       hbar^2 Lambda/c^2,  l >= 0
```

The lowest modes are:

```text
(L4) m_TT(2)  = sqrt(2)   hbar sqrt(Lambda)/c
(L5) m_vec(1) = sqrt(2/3) hbar sqrt(Lambda)/c
(L6) m_scalar(0) = 0
```

The lowest spin-2/spin-1 ratio is Lambda-independent:

```text
(L7) m_TT(2)/m_vec(1) = sqrt(3)
```

The spin-curvature gaps are constant in `l`:

```text
(L8)  m_scalar(l)^2 - m_vec(l)^2 = (1/3) hbar^2 Lambda/c^2,  l >= 1
(L9)  m_vec(l)^2 - m_TT(l)^2    = (1/3) hbar^2 Lambda/c^2,  l >= 2
(L10) m_scalar(l)^2 - m_TT(l)^2 = (2/3) hbar^2 Lambda/c^2,  l >= 2
```

## Retained Inputs

| Input | Authority |
| --- | --- |
| Spin-2 TT tower | [`GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md`](GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md) |
| Spin-1 vector tower | [`VECTOR_GAUGE_FIELD_KK_TOWER_THEOREM_NOTE_2026-04-24.md`](VECTOR_GAUGE_FIELD_KK_TOWER_THEOREM_NOTE_2026-04-24.md) |
| Spin-0 scalar tower | [`SCALAR_HARMONIC_TOWER_THEOREM_NOTE_2026-04-24.md`](SCALAR_HARMONIC_TOWER_THEOREM_NOTE_2026-04-24.md) |
| Cosmological spectral-gap identity `Lambda = 3/R^2` | [`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md) |

No numerical cosmology observation is used in the derivation. Numerical
values below are benchmark evaluations after the symbolic identities
are fixed.

## Derivation

All three retained towers share the spectral unit
`hbar^2/(c^2 R^2)`. The retained cosmological-constant identity gives

```text
hbar^2/(c^2 R^2) = hbar^2 Lambda/(3 c^2).
```

Substitution immediately yields `(L1)-(L3)`.

For the lowest modes:

```text
l = 2 TT:     l(l+2) - 2 = 6, so 6/3 = 2
l = 1 vector: l(l+2) - 1 = 2, so 2/3
l = 0 scalar: l(l+2) = 0
```

Therefore `(L4)-(L6)` follow.

The lowest-mode ratio cancels the full dimensionful unit:

```text
m_TT(2)/m_vec(1)
  = sqrt(2 hbar^2 Lambda/c^2) / sqrt((2/3) hbar^2 Lambda/c^2)
  = sqrt(3).
```

For the gaps, subtract the numerators before substituting:

```text
l(l+2) - (l(l+2) - 1)       = 1
(l(l+2) - 1) - (l(l+2) - 2) = 1
l(l+2) - (l(l+2) - 2)       = 2
```

After dividing by `3`, this gives `(L8)-(L10)`.

## Benchmark Evaluation

Using the cosmology benchmark `Lambda = 1.105e-52 m^-2`:

| Quantity | Value |
| --- | ---: |
| `m_TT(2)` | `2.93e-33 eV/c^2` |
| `m_vec(1)` | `1.69e-33 eV/c^2` |
| `m_scalar(0)` | `0` |
| `m_TT(2)/m_vec(1)` | `sqrt(3) = 1.7321...` |
| `sqrt((2/3) hbar^2 Lambda/c^2)` | `1.69e-33 eV/c^2` |

These numbers are useful scale markers. They are not additional inputs
to the theorem.

## Scope Boundary

This note retains the structural bridge between the gravity spectral
towers and `Lambda = 3/R^2`. It does not promote spectral eigenvalues
to physical particle masses. The parent tower notes keep that physical
particle interpretation bounded, so gravitational-wave graviton-mass
bounds are only conditional comparators here.

If a later theorem promotes the gravity-tower particle interpretation,
then the benchmark value `m_TT(2) = 2.93e-33 eV/c^2` would become a
direct physical prediction. This note does not make that promotion.

## What This Claims

- The pure-Lambda tower forms `(L1)-(L3)`.
- The lowest-mode closed forms `(L4)-(L6)`.
- The Lambda-independent ratio `m_TT(2)/m_vec(1) = sqrt(3)`.
- The constant spin-curvature gaps `(L8)-(L10)`.

## What This Does Not Claim

- It does not derive `Lambda` from the framework alone.
- It does not promote tower eigenvalues to physical particle masses.
- It does not create a direct GW falsification surface without the
  separate particle-interpretation promotion.
- It does not modify the parent scalar, vector, or TT tower theorems.

## Reproduction

```bash
python3 scripts/frontier_gravity_cosmology_tower_lambda_spectral_bridge.py
```

Expected result:

```text
TOTAL: PASS=48, FAIL=0
```
