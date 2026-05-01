# Atomic Nonrelativistic Coulomb Scale Bridge Stretch

**Date:** 2026-05-01
**Loop:** `lane2-atomic-scale-20260428`
**Science block:** 01
**Status:** branch-local exact conditional support theorem plus
underdetermination boundary. This is not a retained Rydberg theorem and not an
atomic-scale framework prediction.
**Runner:** `scripts/frontier_atomic_nr_coulomb_scale_bridge.py`

## Question

Can the existing dimensionless lattice atomic companion supply the missing
physical-unit nonrelativistic Coulomb/Schrodinger bridge by itself?

The relevant existing companion is the retained-operator-surface lattice
problem

```text
H_g = -Delta_x - g / |x|
```

with coupling-relative spectrum and Rydberg-style level ratios. The open Lane
2 gate is stronger: it asks for physical eV units and ultimately for the
hydrogen ground-state scale, not only for dimensionless ratios.

## Minimal Premises For This Stretch

Allowed premises:

1. The Lane 2 atomic lattice companion surface: `H_g = -Delta_x - g/|x|`.
2. The current firewall/open-lane status: `m_e`, `alpha(0)`, and physical unit
   mapping are not retained on Lane 2.
3. Standard nonrelativistic Coulomb Hamiltonian algebra as an admitted bridge
   context:

   ```text
   H_phys = -(1 / 2 mu) Delta_r - Z alpha / r
   ```

Forbidden proof inputs:

1. observed Rydberg energy as a derivation input;
2. observed `alpha(0)` as a derivation input;
3. Lane 6 electron-mass closure work;
4. any hidden fit of lattice spacing to `-13.6 eV`.

Comparator-only values may be printed after the abstract theorem is proved.

## Theorem

**Theorem (Lane 2 nonrelativistic Coulomb scale bridge).** On the current Lane
2 surface, the dimensionless Coulomb Hamiltonian `H_g = -Delta_x - g/|x|`
has the continuum scaled spectrum

```text
lambda_n = -g^2 / (4 n^2).
```

If a physical reduced/electron mass `mu`, a low-energy Coulomb coupling
`alpha`, nuclear charge `Z`, and a physical length unit `a` are supplied with

```text
g = 2 mu a Z alpha,
```

then the physical energy conversion

```text
E = lambda / (2 mu a^2)
```

gives

```text
E_n = -mu (Z alpha)^2 / (2 n^2).
```

The arbitrary dimensionless coupling `g` cancels. Therefore the lattice
companion already has the correct exact scale algebra once the physical mass,
low-energy coupling, and unit map are supplied.

Conversely, without `mu`, `alpha`, and the unit map `a`, the same
dimensionless lattice eigenvalue maps to a one-parameter family of physical
energies proportional to `1/a^2`. The dimensionless companion alone cannot
determine an absolute eV Rydberg scale.

## Proof

Let the physical coordinate be `r = a x`. Then

```text
Delta_r = a^-2 Delta_x
1 / r = a^-1 / |x|
```

so

```text
[-(1 / 2 mu a^2) Delta_x - (Z alpha / a) 1/|x|] psi = E psi.
```

Multiplying by `2 mu a^2` gives

```text
[-Delta_x - (2 mu a Z alpha) / |x|] psi = (2 mu a^2 E) psi.
```

Identifying `g = 2 mu a Z alpha` and
`lambda = 2 mu a^2 E` maps this exactly to the dimensionless companion
Hamiltonian. Substituting `lambda_n = -g^2/(4 n^2)` gives

```text
E_n
= [-g^2 / (4 n^2)] / (2 mu a^2)
= -[2 mu a Z alpha]^2 / [8 mu a^2 n^2]
= -mu (Z alpha)^2 / (2 n^2).
```

No observed Rydberg value is used in the identity. The result is an exact
conditional support bridge, not a derivation of `mu`, `alpha(0)`, or `a`.

## Runner Result

The runner checks four things:

1. the repo surfaces for the Rydberg firewall, standard-QM scaffold, and
   lattice atomic companion are present;
2. dimensionless level ratios are independent of `g`;
3. the scale map gives the Bohr formula for synthetic non-observed parameter
   choices and cancels arbitrary `g`;
4. if `a` is left free, the same dimensionless eigenvalue gives distinct eV
   energies.

Verification output:

```text
PYTHONPATH=scripts python3 scripts/frontier_atomic_nr_coulomb_scale_bridge.py
=> SUMMARY: PASS=42 FAIL=0
```

The comparator section also prints that the scaffold constants
`m_e c^2 = 510998.95000 eV` and `1/alpha(0) = 137.035999084` reproduce
`-13.605693123 eV`, matching the existing scaffold Hartree/2 value. This is
comparator context only.

## Claim-State Movement

This stretch sharpens the third Lane 2 Rydberg gate:

```text
dimensionless lattice Coulomb companion
  + retained mu/m_e
  + retained alpha(0)
  + retained physical unit map a = g/(2 mu Z alpha)
  => exact nonrelativistic Coulomb scale formula
```

The bridge shows that, once the physical inputs are retained, no additional
fit to the Rydberg target is needed to convert the companion scaling law to
the standard nonrelativistic Coulomb spectrum.

What remains open:

1. retained electron/reduced mass `mu` for the atomic problem;
2. retained low-energy `alpha(0)` or threshold-resolved QED transport;
3. a framework-native derivation of the physical unit map / kinetic
   prefactor, rather than admitting the standard nonrelativistic Hamiltonian
   as bridge context;
4. finite-nuclear-mass and proton-sector corrections for actual hydrogen,
   which depend on Lane 1 and are not worked in this Lane 2 loop.

## Import Ledger

| Item | Role | Class | Disposition |
|---|---|---|---|
| `H_g = -Delta_x - g/|x|` | dimensionless lattice Coulomb companion | bounded support / retained-operator-surface companion | usable for ratios and conditional scale algebra |
| `lambda_n = -g^2/(4 n^2)` | continuum scaled Coulomb spectrum | admitted standard Coulomb theorem / exact support bridge | used for the algebraic scale identity |
| `mu` | electron or reduced mass in the physical Hamiltonian | unsupported import for Lane 2 closure | still open; Lane 6/Lane 1 dependency only |
| `alpha(0)` | low-energy Coulomb coupling | unsupported import for Lane 2 closure | still open after QED threshold firewall |
| `a = g/(2 mu Z alpha)` | physical lattice length map | admitted unit map in this theorem | exact conditional map; not framework-derived here |
| comparator `m_e`, `alpha(0)`, Hartree/2 | physical-scale illustration | comparator / non-derivation context | not used to prove the theorem |

## Status Boundary

Safe branch-local statement:

> The current lattice atomic companion has an exact conditional scale bridge to
> the nonrelativistic Coulomb spectrum once `mu`, `alpha(0)`, and the physical
> unit map are supplied; without those inputs, it cannot determine an absolute
> eV Rydberg scale.

Not safe:

1. `alpha(0)` is derived;
2. `m_e` or reduced mass is derived;
3. the Rydberg constant is retained;
4. the physical-unit Schrodinger limit is fully framework-native;
5. the existing hydrogen/helium scaffold is promoted to framework evidence.

## Review Guardrail

The artifact should fail review if it is used to claim retained Rydberg
closure. Its value is narrower: it isolates the exact physical-unit scale
identity and proves the remaining unit/mass/coupling blockers are real rather
than optional wording caveats.
