# Atomic Rydberg Dependency Firewall

**Date:** 2026-04-27
**Status:** proposed_retained exact negative boundary for Lane 2 dependency
accounting. This is not an atomic-scale framework prediction and not a
hydrogen closure theorem.
**Script:** `scripts/frontier_atomic_rydberg_dependency_firewall.py`
**Lane:** Lane 2 atomic-scale predictions

## Question

Can the current repo honestly claim a framework-derived hydrogen Rydberg scale
by substituting retained high-energy quantities into the standard formula?

## Result

No.

The standard nonrelativistic formula

```text
E_1 = -m_e alpha(0)^2 / 2
```

is ready as a downstream bridge once its physical inputs are retained. But the
current Lane 2 state does not retain those inputs:

- `m_e` remains an open charged-lepton mass input;
- the repo has a reusable `alpha_EM(M_Z)` value, not a retained atomic
  `alpha(0)` closure;
- the current atomic harness imports the textbook nonrelativistic
  Schrodinger/Coulomb Hamiltonian in physical units.

Directly substituting the retained electroweak-scale value

```text
alpha_EM(M_Z) = 1 / 127.67
```

for the atomic Coulomb coupling gives

```text
E_1 = -15.68 eV
```

with textbook `m_e`, rather than the Rydberg value

```text
E_1 = -13.6057 eV.
```

The difference is about `+15%`. Thus the low-energy QED transport from
`alpha_EM(M_Z)` to `alpha(0)` is load-bearing, not a harmless notation change.

## Theorem

**Theorem (Lane 2 Rydberg dependency firewall).** Assume the current repo
atomic Lane 2 state, including the scaffold hydrogen solver, the retained
electroweak-scale `alpha_EM(M_Z)` value, and the open charged-lepton mass
status. Then a framework-derived Rydberg claim is blocked unless the branch
also supplies:

1. a retained electron mass or charged-lepton Yukawa activation law;
2. a retained low-energy Coulomb coupling `alpha(0)`, or an explicit QED
   running bridge from `alpha_EM(M_Z)` to `alpha(0)`;
3. a retained nonrelativistic Schrodinger/Coulomb limit in physical units.

Without these, the existing hydrogen/helium harness remains scaffold-only.

## What This Retires

This retires one tempting fast-but-wrong upgrade:

```text
retained alpha_EM(M_Z) + textbook hydrogen formula
  => retained Rydberg prediction
```

That implication is false without the low-energy coupling bridge and electron
mass closure.

## What Remains Open

Lane 2 remains open. The exact next gates are:

- charged-lepton/electron mass retention;
- atomic `alpha(0)` or QED-running bridge from the retained EW package;
- physical-unit nonrelativistic atomic limit from the framework substrate.

Once those are supplied, the existing scaffold can become a substitution and
verification theorem. Until then it is not framework evidence.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_atomic_rydberg_dependency_firewall.py
```

Expected result:

```text
PASS=12 FAIL=0
```

## Inputs And Import Roles

| Input | Role | Import class | Source |
|---|---|---|---|
| `alpha_EM(M_Z)=1/127.67` | high-energy retained EW value tested against direct substitution | framework-derived | `docs/publication/ci3_z3/USABLE_DERIVED_VALUES_INDEX.md` |
| textbook `m_e` | sensitivity/comparator for the firewall | observational comparator | existing atomic scaffold convention |
| textbook `alpha(0)` | low-energy Coulomb comparator | standard comparator | existing atomic scaffold convention |
| `E_1=-m_e alpha^2/2` | standard downstream bridge formula | admitted standard bridge | nonrelativistic hydrogen scaffold |

No atomic observed value is used to tune a framework parameter in this note.
The textbook constants are used only to expose which dependencies remain
load-bearing.

## Safe Wording

Can claim:

- current Lane 2 has an exact dependency firewall for Rydberg closure;
- direct `alpha_EM(M_Z)` substitution misses the atomic Rydberg scale by
  order `15%`;
- the existing atomic solver remains scaffold-only until `m_e`, `alpha(0)`,
  and the physical-unit nonrelativistic limit are retained.

Cannot claim:

- hydrogen is derived from the framework;
- the Rydberg constant is retained;
- Lamb shift, fine structure, hyperfine, helium, or larger atoms are closed.
