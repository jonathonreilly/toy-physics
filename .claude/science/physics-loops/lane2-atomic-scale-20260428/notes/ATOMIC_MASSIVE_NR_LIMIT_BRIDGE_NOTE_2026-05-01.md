# Atomic Massive Nonrelativistic Limit Bridge

**Date:** 2026-05-01
**Loop:** `lane2-atomic-scale-20260428`
**Science block:** 01
**Runner:** `scripts/frontier_atomic_massive_nr_limit_bridge.py`
**Status:** exact conditional kinetic support plus mass-gate boundary. This is
not retained Rydberg closure.

## Question

Does the retained Lorentz/dispersion surface close the physical-unit
Schrodinger kinetic prefactor for Lane 2 atomic physics?

## Verdict

It gives a clean conditional bridge, not closure. If a retained low-energy
one-particle sector supplies the massive relativistic dispersion

```text
E^2 = m^2 + p^2,
```

then rest-energy subtraction gives

```text
E - m = p^2/(2m) + O(p^4/m^3).
```

The Schrodinger kinetic prefactor is therefore fixed once the mass is fixed.
Current Lane 2 does not retain the electron/reduced mass, so the atomic
kinetic prefactor remains mass-gated.

## Relation To Existing Surfaces

The canonical harness index carries a retained Lorentz support packet,
including `EMERGENT_LORENTZ_INVARIANCE_NOTE.md` and the 3+1D boost runner.
Those surfaces support the low-energy relativistic dispersion bridge. This
note only extracts the nonrelativistic kinetic consequence needed by Lane 2.

## Exact Boundary

The conditional bridge is:

```text
retained massive low-energy one-particle dispersion
  + rest-energy subtraction
  + p << m
  => K = p^2/(2m) + higher-order terms.
```

What remains open:

1. retained electron/reduced mass `m`;
2. retained low-energy `alpha(0)` and its threshold/matching moment;
3. retained Coulomb potential/coupling in the same low-energy sector;
4. finite-nuclear-mass/proton inputs for physical hydrogen.

## Verification

Recorded command:

```text
PYTHONPATH=scripts python3 scripts/frontier_atomic_massive_nr_limit_bridge.py
```

Expected summary:

```text
SUMMARY: PASS=22 FAIL=0
STATUS: exact conditional kinetic support plus mass-gate boundary.
```

## Review-Loop Notes

- The proof uses synthetic masses and momenta before the electron-mass
  comparator appears.
- The electron mass appears only to show the size of the comparator kinetic
  coefficient `1/(2m_e)`.
- The note does not derive `m_e`, `alpha(0)`, the Coulomb sector, or the
  Rydberg scale.
