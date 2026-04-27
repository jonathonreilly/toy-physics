# Atomic Hydrogen and Helium Probe --- Standard-QM Scaffold Lane

**Date:** 2026-04-19
**Status:** **bounded exploratory scaffold lane.** This is **not** a proposed_retained
framework derivation. The script uses standard non-relativistic quantum
mechanics with textbook inputs (`m_e`, `e`, `hbar`, `4 pi epsilon_0`, `Z = 1`
for hydrogen and `Z = 2` for helium). No `Cl(3)` on `Z^3` framework input is
used anywhere. The lane's role is to open a working scaffold against the
atomic-scale gap so that future framework-internal inputs (electron mass in
MeV, Coulomb coupling in physical units, single-particle Schrodinger from the
discrete-wave / path-sum surface) can be substituted into the same numerical
harness without re-deriving the eigensolver.

**Script:** `scripts/frontier_atomic_hydrogen_helium_probe.py`

## Why this lane exists

The atomic scale (`~10^-10 m`, `~eV`) sits between the framework's retained
high-energy surface (Planck, electroweak, QCD, cosmology) and a regime that
mainstream physics treats as the cleanest sanity check imaginable. A
framework that derives `Lambda_vac` and `m_g` but cannot reproduce
`-13.6 eV` invites the obvious "then why believe the cosmology number?"
response. The interest map's harshest-critique tracker explicitly tracks this
as one of the open vulnerabilities; this lane scopes it without claiming to
close it.

The closest existing prior on `main` is the bounded
`frontier_bound_state_selection.py` script
([BOUND_STATE_SELECTION_NOTE.md](BOUND_STATE_SELECTION_NOTE.md)),
which uses Coulomb scaling as a dimension-selection diagnostic in
dimensionless lattice units. That script does not produce eV-scale spectra
and does not target real atoms. This lane is structurally separate: it works
in physical units and targets real atomic spectra, but using textbook inputs
rather than framework-derived ones.

## Method

### Hydrogen

Direct diagonalization of the radial Schrodinger Hamiltonian for `u(r) = r
R(r)`, in Hartree atomic units:

```
H_l = -1/2 d^2/dr^2 + l(l+1) / (2 r^2) - Z / r
```

Discretized on a uniform grid with `n_grid = 8000` interior points,
`r_max = 200` Bohr, Dirichlet boundary conditions, three-point Laplacian.
Eigenvalues from `scipy.sparse.linalg.eigsh` (`which='SA'`). Energies
converted to eV via `1 Hartree = 27.211386 eV`. Reference: analytic Bohr
spectrum `E_n = -13.6057 eV / n^2`.

### Helium

No closed-form solution exists (three-body). Two textbook benchmarks are
reported:

1. **Independent-electron baseline** --- two non-interacting `1s` electrons
   at `Z = 2`:
   `E_0 = 2 * (-Z^2 / 2) = -4 Hartree = -108.85 eV`.
   Far below experiment because electron-electron repulsion is omitted.
2. **Single-parameter variational** --- trial wavefunction
   `psi(r_1, r_2) = exp(-Z_eff r_1) exp(-Z_eff r_2)` gives
   `E(Z_eff) = Z_eff^2 - 2 Z Z_eff + (5/8) Z_eff` Hartree, minimized at
   `Z_eff = Z - 5/16 = 27/16 = 1.6875`, yielding
   `E_min = -(27/16)^2 Hartree = -77.49 eV`.

Reference: experimental ground-state energy `E_exp = -79.005 eV` (NIST).

## Results

### Hydrogen --- numerical vs analytic, all eV

```
   l   n      E_num [eV]   E_exact [eV]   |err| [eV]    rel_err
   0   1      -13.603568     -13.605693     2.12e-03  -1.56e-04
   0   2       -3.401290      -3.401423     1.33e-04  -3.90e-05
   0   3       -1.511717      -1.511744     2.62e-05  -1.74e-05
   0   4       -0.850348      -0.850356     8.30e-06  -9.76e-06
   0   5       -0.544224      -0.544228     3.40e-06  -6.25e-06
   1   2       -3.401468      -3.401423     4.43e-05   1.30e-05
   1   3       -1.511764      -1.511744     2.04e-05   1.35e-05
   1   4       -0.850366      -0.850356     1.05e-05   1.24e-05
   1   5       -0.544234      -0.544228     6.03e-06   1.11e-05
   1   6       -0.377940      -0.377936     3.75e-06   9.93e-06
   2   3       -1.511745      -1.511744     1.75e-06   1.16e-06
   2   4       -0.850357      -0.850356     1.66e-06   1.95e-06
   2   5       -0.544229      -0.544228     1.26e-06   2.32e-06
   2   6       -0.377937      -0.377936     9.21e-07   2.44e-06
   2   7       -0.277668      -0.277667     6.75e-07   2.43e-06
```

Worst relative error vs analytic Bohr spectrum: `1.56e-4` (the `1s` ground
state, where the wavefunction is most sensitive to grid spacing near `r = 0`).
All other rows agree to `<= 4e-5` relative error. The `l = 2` channel is the
cleanest because `u(r) ~ r^(l+1)` near the origin makes those states least
sensitive to the `r = 0` regularization.

### Helium

```
  reference (NIST experimental):     E_exp = -79.0052 eV
  independent-electron baseline   = -108.8455 eV  (err -29.84 eV)
  one-parameter variational       =  -77.4887 eV  (err  +1.52 eV, rel -1.92%)
  optimal Z_eff                   =   1.6875  (= 27/16)
```

The `1.92%` variational gap is the textbook three-body residual; it is
closed (slowly) by Hartree-Fock (`-77.87 eV`), Hylleraas-style explicitly
correlated trial functions (`<= 0.01 eV` from experiment), and modern QMC.
None of those refinements are in this script --- the variational benchmark
is included only as the simplest non-trivial three-body reference any future
framework-internal helium calculation would have to beat.

## Bounded claims

The script demonstrates that:

1. on this codebase, with `numpy + scipy` already in `requirements.txt`,
   standard QM with textbook inputs reproduces the hydrogen spectrum to
   `~10^-4` relative error and the helium ground state to `~2%` (variational)
   /  exact (within available basis), in physical eV units;
2. the harness is structurally ready to accept framework-derived inputs in
   place of textbook constants, if and when those become available.

The script does **not** claim that the framework derives any of:

- the electron mass `m_e`;
- the Coulomb coupling `e^2 / (4 pi epsilon_0)`;
- the single-particle Schrodinger equation as a sector of `Cl(3)` on `Z^3`;
- the spin-statistics theorem or the Pauli exclusion principle that picks the
  helium singlet ground state;
- any atomic-scale prediction at all.

## Where this sits in the publication matrix

Bounded exploratory scaffold lane. **Not** a retained framework result. **Not**
a retained reproduction of atomic spectra. **Not** a discriminator. The lane is
a diagnostic that the atomic-scale gap is real, scoped, and harness-ready.

## Gap map --- what it would take to convert this into a retained lane

A real framework-internal hydrogen retention would require, in order:

1. **A retained electron sector.** The current charged-lepton program targets
   the Koide mass-ratio relation
   ([CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md](CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md))
   but does not yet retain `m_e` in MeV. Closing the open microscopic scalar
   selector law would deliver `m_e` as a derived quantity.
2. **A retained Coulomb sector.** The current electrostatics surface retains
   sign, superposition, and dipole response on the discrete-lattice signed-
   charge proxy, but does not retain a calibrated `e^2 / (4 pi epsilon_0) r`
   in physical units. A retained QED-scale effective theory derived from the
   framework, with the fine-structure constant emerging as a derived scale
   ratio, would deliver this.
3. **A retained single-particle Schrodinger limit.** The current discrete-wave
   / path-sum surface produces Born statistics, gauge structure, and bounded
   weak-field gravity windows, but the non-relativistic single-particle limit
   is not retained as a derived sector. A retained reduction from the
   discrete-wave surface to a one-body Schrodinger equation in physical units
   would deliver this.
4. **A retained two-body / antisymmetrization sector.** Helium additionally
   requires the Pauli principle to select the spin-singlet ground state, and
   either a Hartree-Fock or explicitly correlated route to the residual `1.5
   eV` of correlation energy. Spin-statistics is not currently a retained
   feature.

Steps (1) and (2) are blockers. Step (3) is the structural gap that makes the
atomic-scale lane different from the cosmology / gravity / particle-mass
lanes the framework currently retains. Step (4) is the helium-specific
refinement that turns the lane from "hydrogen retrodiction" into a genuine
three-body discriminator.

## Why hydrogen is a sanity check and helium is the discriminator

Hydrogen has a closed-form solution. Reproducing `-13.6 eV / n^2` from
framework-internal inputs would be a clean retrodiction --- significant for
calibration but not a novel result, since the spectrum has been derivable
since 1926. Helium is the first system where standard quantum mechanics
itself requires numerics, because the three-body problem has no closed form.
A framework-internal helium calculation that competes with Hartree-Fock or
Hylleraas accuracy would be a genuine new computational route to many-body
bound states, and would carry weight precisely because there is no analytic
result to overfit to.

## Why this lane does not change the interest scores

This lane is honestly bounded: it adds no retained content to the framework,
it does not move the bridge-to-known-physics surface, and it does not close
any open flagship gate. It does sharpen one thing for the harshest-critique
tracker --- the atomic-scale gap is now scoped, harness-ready, and explicitly
in the program rather than implicit. That is a procedural improvement, not a
score improvement. The interest map should be updated only when a retained
input from steps (1)-(3) above flows into this harness and produces a
framework-internal hydrogen number.

## Reproducing

```
python scripts/frontier_atomic_hydrogen_helium_probe.py
```

Requires `numpy >= 1.24` and `scipy >= 1.10` (already in
`requirements.txt`). Runs in a few seconds on a single core. No GPU, no MPI,
no external data.
