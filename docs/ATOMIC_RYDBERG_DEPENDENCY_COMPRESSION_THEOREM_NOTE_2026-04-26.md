# Atomic Rydberg Dependency Compression Theorem

**Date:** 2026-04-26

**Status:** standalone positive atomic-scale open-lane theorem. This note
proves the exact dependency chain from a retained nonrelativistic Coulomb
two-body sector to the hydrogenic Rydberg series. It does not claim that the
framework has derived the electron mass, proton mass, fine-structure constant,
Schrodinger limit, Coulomb potential, Lamb shift, hyperfine splitting, helium
correlation energy, time travel, teleportation, or antigravity effect.

**Primary runner:** `scripts/frontier_atomic_rydberg_dependency_compression.py`

## 1. Claim

Assume the low-energy atomic substrate supplies the standard two-body
nonrelativistic Coulomb Hamiltonian for charges `-e` and `+Z e`:

```text
H = p_1^2/(2 m_1) + p_2^2/(2 m_2) - Z alpha hbar c / |x_1 - x_2|.
```

Here `alpha` is the physical fine-structure constant, `m_1` and `m_2` are the
two inertial masses, and `Z` is the nuclear charge. Let

```text
mu = m_1 m_2 / (m_1 + m_2)
```

be the reduced mass. Then every leading nonrelativistic hydrogenic bound-state
energy is fixed by

```text
E_n = - mu c^2 (Z alpha)^2 / (2 n^2),       n = 1, 2, 3, ...
```

and every line wavenumber is fixed by

```text
1/lambda = R_M Z^2 (1/n_f^2 - 1/n_i^2),
R_M      = alpha^2 mu c / (2 h).
```

For hydrogen, with `m_1 = m_e`, `m_2 = m_p`, this becomes

```text
E_n(H) = - m_e c^2 alpha^2 / (2 n^2) * 1/(1 + m_e/m_p),
R_H    = R_infinity * 1/(1 + m_e/m_p).
```

Therefore a future retained derivation of `m_e`, `m_p`, and `alpha` plus a
retained nonrelativistic Coulomb reduction is sufficient to produce the
leading hydrogen Rydberg spectrum with no additional fitted atomic parameter.
The theorem is a dependency-compression theorem, not an atomic-scale closure.

## 2. Why This Moves Lane 2

The open science lane
`docs/lanes/open_science/02_ATOMIC_SCALE_PROGRAM_OPEN_LANE_2026-04-26.md`
asks for the first worker target:

```text
isolate the exact dependency chain from m_e, alpha, and retained
electroweak/QED inputs to the first Rydberg theorem.
```

The existing
`docs/ATOMIC_HYDROGEN_HELIUM_PROBE_NOTE.md` is a useful scaffold, but it
uses textbook constants in atomic units. This theorem extracts the analytic
dependency map that the scaffold must obey when framework-retained inputs are
substituted later.

The load-bearing result is sharper than the textbook slogan "`-13.6 eV` comes
from hydrogen." It identifies the precise future inputs:

- `alpha`, the dimensionless Coulomb coupling;
- `m_e c^2`, the electron rest energy;
- `m_e/m_p`, the finite-nuclear-mass correction;
- the retained nonrelativistic Coulomb Hamiltonian itself.

No separate Rydberg constant, Bohr radius, Hartree, or eV-scale atomic fitting
constant is allowed.

## 3. Center-of-Mass Reduction

Let

```text
R = (m_1 x_1 + m_2 x_2) / (m_1 + m_2),
r = x_1 - x_2,
M = m_1 + m_2,
mu = m_1 m_2 / M.
```

The conjugate momenta can be written

```text
p_1 = (m_1/M) P + p,
p_2 = (m_2/M) P - p.
```

Substituting into the kinetic energy gives

```text
p_1^2/(2m_1) + p_2^2/(2m_2)
  = P^2/(2M) + p^2/(2mu).
```

The cross term cancels exactly:

```text
(m_1/M) P.p / m_1 - (m_2/M) P.p / m_2 = P.p/M - P.p/M = 0.
```

Thus the Hamiltonian separates as

```text
H = P^2/(2M) + H_rel,
H_rel = p^2/(2mu) - Z alpha hbar c / r.
```

Atomic internal spectra are the eigenvalues of `H_rel`; center-of-mass motion
does not change level spacings.

## 4. Dimensionless Coulomb Scaling

Choose the Bohr length for the two-body system

```text
a_M = hbar / (mu c Z alpha),
rho = r/a_M.
```

Then

```text
p = -i hbar grad_r = -i (hbar/a_M) grad_rho
  = -i mu c Z alpha grad_rho.
```

The relative Hamiltonian becomes

```text
H_rel = mu c^2 (Z alpha)^2
        [ -1/2 Delta_rho - 1/rho ].
```

All dimensional information has been compressed into the single prefactor

```text
mu c^2 (Z alpha)^2.
```

The bracketed operator is the universal dimensionless Coulomb operator. Its
bound-state spectrum is

```text
epsilon_n = -1/(2 n^2).
```

Multiplying by the prefactor proves

```text
E_n = - mu c^2 (Z alpha)^2 / (2 n^2).
```

This is the precise sense in which the Rydberg scale contains no additional
atomic parameter.

## 5. Hydrogen and the Reduced-Mass Gate

For hydrogen,

```text
mu_H = m_e m_p/(m_e + m_p)
     = m_e / (1 + m_e/m_p).
```

Hence

```text
E_n(H) = - m_e c^2 alpha^2/(2 n^2) * 1/(1 + m_e/m_p).
```

The infinite-nuclear-mass Rydberg energy is

```text
Ry_infinity = m_e c^2 alpha^2/2.
```

The physical hydrogen Rydberg energy at leading nonrelativistic order is

```text
Ry_H = Ry_infinity/(1 + m_e/m_p).
```

The finite-mass factor is not optional. A proof that uses `m_e` but omits
`m_p` derives the infinite-proton-mass spectrum, not physical hydrogen.
Therefore Lane 2 depends not only on charged-lepton scale retention but also
on hadron/nuclear mass retention for physical isotope-level predictions.

## 6. Wavenumbers and Unit Conversion

Photon energies are level differences:

```text
Delta E = mu c^2 alpha^2 Z^2/2 * (1/n_f^2 - 1/n_i^2).
```

Dividing by `h c` gives a wavenumber:

```text
1/lambda = Delta E/(h c)
         = alpha^2 mu c Z^2/(2 h) * (1/n_f^2 - 1/n_i^2).
```

Thus

```text
R_M = alpha^2 mu c/(2h).
```

The appearances of `h` and `c` here are unit-conversion factors. In an energy
statement written in rest-energy units, the dynamical input is `mu c^2`, not a
separate atomic scale. In SI wavenumber units, `h` and `c` convert energy to
inverse length. They do not supply an adjustable Rydberg fit.

## 7. Sensitivity Certificate

At fixed `Z` and `n`,

```text
|E_n| = (alpha^2/2n^2) * mu c^2 Z^2.
```

The logarithmic sensitivity is

```text
d log |E_n| = 2 d log alpha + d log mu.
```

Because

```text
mu = m_1 m_2/(m_1 + m_2),
```

the mass sensitivities are

```text
partial log mu / partial log m_1 = m_2/(m_1 + m_2),
partial log mu / partial log m_2 = m_1/(m_1 + m_2).
```

For hydrogen this gives

```text
d log |E_n(H)| =
  2 d log alpha
  + [m_p/(m_e+m_p)] d log m_e
  + [m_e/(m_e+m_p)] d log m_p.
```

Since `m_e/m_p` is small, the Rydberg energy is almost linearly sensitive to
`m_e`, weakly sensitive to `m_p`, and quadratically sensitive to `alpha`. This
is a review-facing dependency budget: future framework errors in `alpha` are
doubled in the leading Rydberg energy, while future proton-mass errors enter
only through the reduced-mass correction.

## 8. Exact Corollaries

### 8.1 Hydrogen Ground State

For `Z=1`, `n=1`:

```text
E_1(H) = - Ry_H.
```

Using present textbook constants as a non-claim numerical smoke test gives
approximately `-13.5983 eV` before relativistic, QED, hyperfine, and finite
proton-size corrections. The scaffold note's `-13.6057 eV` target is the
infinite-proton-mass Hartree target used by atomic units.

### 8.2 Hydrogenic Ions

For a one-electron ion with charge `Z`,

```text
E_n(Z,M) = - mu(M) c^2 (Z alpha)^2/(2 n^2).
```

The whole leading spectrum scales as `Z^2` and as the appropriate
electron-nucleus reduced mass.

### 8.3 Isotope Shifts

For two isotopes with nuclear masses `M_A` and `M_B`, the leading isotope
shift of any same transition is controlled by

```text
R_A/R_B = [1/(1 + m_e/M_A)] / [1/(1 + m_e/M_B)].
```

Thus isotope shifts are not a new atomic scale; at leading order they are a
mass-ratio diagnostic.

### 8.4 Atomic Units Are a Change of Variables

The Hartree energy is

```text
E_h(M) = mu c^2 alpha^2.
```

The Bohr radius is

```text
a_M = hbar/(mu c alpha).
```

Using atomic units sets these combinations to one. It does not remove the
need to derive `mu` and `alpha` from the framework if the output is to become
a retained physical prediction.

## 9. What This Does Not Close

This theorem does not derive:

- the electron mass or charged-lepton Koide closure;
- the proton mass or hadron mass lane;
- the fine-structure constant;
- the continuum Schrodinger limit from the discrete substrate;
- the Coulomb potential from a retained QED sector;
- relativistic fine structure, Lamb shift, hyperfine splitting, or finite
  nuclear-size corrections;
- helium, molecules, many-electron atoms, or muon `g-2`;
- any time-travel, teleportation, or antigravity claim.

Therefore it does not close Lane 2. It proves the exact first bridge that Lane
2 needs: once the retained-input gates are supplied, the leading Rydberg
series follows without a new fit.

## 10. Program Consequence

The atomic open lane can now be split cleanly:

```text
Rydberg leading spectrum =
  retained Schrodinger-Coulomb reduction
  + retained alpha
  + retained m_e
  + retained m_p correction.
```

The current blocker list is therefore not vague. A future worker can attack
the missing inputs independently, and the validator in this branch will catch
any later attempt to call the Rydberg constant a derived number while still
using an external electron/proton mass or external `alpha`.
