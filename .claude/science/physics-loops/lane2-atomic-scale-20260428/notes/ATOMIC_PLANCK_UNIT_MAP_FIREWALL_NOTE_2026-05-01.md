# Atomic Planck-Unit Map Firewall

**Date:** 2026-05-01  
**Loop:** `lane2-atomic-scale-20260428`  
**Science block:** 01  
**Runner:** `scripts/frontier_atomic_planck_unit_firewall.py`  
**Status:** exact negative boundary / conditional support for Lane 2. This is
not retained Rydberg closure.

## Question

Does the current Planck/source-unit package close the Lane 2 physical-unit
nonrelativistic Coulomb map?

## Verdict

No. The Planck/source-unit package can supply a gravitational lattice
length/source unit on its conditional carrier surface. It does not supply the
atomic effective coupling or kinetic map needed by the hydrogen Hamiltonian.

The Lane 2 scale bridge requires

```text
H_g = -Delta_x - g/r_x
r = a_lat x
E = lambda / (2 mu a_lat^2)
g = 2 mu a_lat Z alpha(0)
```

Thus a fixed lattice length anchor, including the Planck package pin
`a_lat = 1/M_Pl`, still leaves the atomic dimensionless coupling

```text
g_atomic = 2 (mu/M_Pl) Z alpha(0)
```

undetermined unless `mu` and `alpha(0)` are already supplied. Current Lane 2
does not retain either of those inputs.

## Exact Boundary

The prior NR Coulomb bridge proved that the dimensionless companion maps
exactly to the Bohr formula after the standard map is admitted:

```text
lambda_n = -g^2/(4 n^2)
E_n = lambda_n/(2 mu a_lat^2)
g = 2 mu a_lat Z alpha
=> E_n = -mu (Z alpha)^2/(2 n^2)
```

This note sharpens the remaining unit-map ambiguity:

1. The Planck source-unit support theorem separates the bare Green coefficient
   `1/(4 pi)` from conditional `G_Newton,lat = 1`.
2. That is a gravitational source/action normalization statement.
3. The atomic Hamiltonian still needs the electromagnetic low-energy coupling
   and kinetic mass to form `g_atomic`.
4. Setting the numerical companion's convenient `g=1` equal to the Planck
   lattice coupling is an extra cross-sector selector, not a repo theorem.

## Comparator Illustration

Using the repo's existing comparator values only as a check:

```text
M_Pl = 1.2209e19 GeV
m_e = 510998.95 eV
1/alpha(0) = 137.035999084
```

the matched Planck-lattice hydrogen coupling is tiny:

```text
g_atomic = 2 m_e alpha(0) / M_Pl ~= 6.11e-25
r_B ~= 2/g_atomic ~= 3.27e24 lattice sites
```

With that tiny `g_atomic`, the scale bridge reproduces the ordinary Bohr
energy after textbook `m_e` and `alpha(0)` are supplied. But if one instead
sets `g=1` at Planck spacing while keeping the electron kinetic mass, the
ground energy is super-Planckian on the atomic scale and misses the Rydberg
by more than `10^40`.

This comparator does not prove Rydberg closure. It shows why the Planck unit
anchor cannot be substituted for the missing atomic low-energy map.

## Import Ledger

| Item | Role | Status in this artifact |
|---|---|---|
| Planck package pin `a^(-1)=M_Pl` | fixed physical-lattice length anchor | package pin / conditional support context |
| Source-unit theorem `G_Newton,lat=1` | gravitational source normalization | conditional Planck support, not atomic coupling |
| `mu` / electron or reduced mass | kinetic mass in the NR Hamiltonian | open Lane 2 import; Lane 6 dependency recorded only |
| `alpha(0)` | low-energy Coulomb coupling | open Lane 2 import |
| `g_atomic = 2 mu a_lat Z alpha(0)` | dimensionless atomic coupling on the lattice | exact conditional bridge; not retained without `mu` and `alpha(0)` |
| `g=1` in the old finite-box companion | convenient coupling-relative numerical choice | useful scaffold value; not the Planck-lattice atomic coupling |

## No-Go Statement

The route

```text
Planck lattice unit + source-unit normalization => retained atomic Rydberg
```

does not pass. At best it gives a length anchor for the lattice coordinate.
The atomic map still requires a low-energy effective-theory statement:

```text
Cl(3)/Z^3 physical lattice
  -> low-energy one-particle NR kinetic mass mu
  -> low-energy Coulomb alpha(0)
  -> dimensionless lattice coupling g_atomic
  -> Bohr/Rydberg scale
```

Current branch artifacts prove the algebra once these inputs are supplied;
they do not derive the inputs.

## Verification

Recorded command:

```text
PYTHONPATH=scripts python3 scripts/frontier_atomic_planck_unit_firewall.py
```

Expected summary:

```text
SUMMARY: PASS=31 FAIL=0
STATUS: exact negative boundary / conditional-support firewall.
```

## Review-Loop Notes

- The proof uses synthetic masses, couplings, lattice anchors, and levels
  before mentioning hydrogen comparator values.
- Comparator values are used only to show the scale of the hidden-selector
  problem.
- The note does not promote the conditional Planck packet or the atomic
  companion into retained Rydberg closure.
- Lane 6 appears only as the upstream mass dependency; no charged-lepton or
  Koide work is performed here.
