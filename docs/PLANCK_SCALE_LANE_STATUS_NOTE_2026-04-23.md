# Planck-Scale Lane Status Note

**Date:** 2026-04-23  
**Purpose:** canonical package note for the absolute lattice-scale posture on
`main`.

## 1. Current package stance

The accepted package already treats `Cl(3)` on `Z^3` as a **physical lattice**,
not a disposable regulator family. On that package reading, the current public
surface now tracks the absolute lattice scale by one explicit package pin:

> `a^(-1) = M_Pl`

This is the cleanest honest package statement for the current tree.

It means:

- the physical-lattice reading is accepted on the package boundary;
- the absolute lattice spacing is presently carried by one explicit Planck
  scale pin;
- that pin is **not yet** derived from the minimal accepted theorem stack.

So the current lane status is:

- **physical lattice:** accepted package posture
- **absolute scale `a^(-1) = M_Pl`:** current package pin
- **derivation of that pin from the accepted stack:** open program

## 2. Why this lane exists

Older notes in the repository often speak in the stronger shorthand
`a = l_Planck`. Newer publication-facing notes correctly separate the absolute
scale from the internal dimensionless structure.

This lane exists to make those two postures consistent:

- the package may use the Planck-sized physical lattice as its current
  quantitative anchor;
- the repo should not describe that anchor as already derived when the live
  theorem stack still stops at lattice units.

The main load-bearing boundary notes are:

- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- [GRAVITY_CLEAN_DERIVATION_NOTE.md](./GRAVITY_CLEAN_DERIVATION_NOTE.md)
- [ACTION_NORMALIZATION_NOTE.md](./ACTION_NORMALIZATION_NOTE.md)
- [BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md](./BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md)

## 3. What the Planck-scale pin cleans up now

Once this pin is carried explicitly as a package lane, the following repo-wide
semantics become cleaner and more uniform:

- hierarchy / electroweak absolute-scale bookkeeping;
- the literal UV meaning of the lattice endpoint `M_Pl` in the YT / Higgs
  lanes;
- neutrino / DM mass-ladder language built from Planck-down staircases;
- the anti-regulator / physical-lattice ontology boundary;
- Planck-suppressed gravity and cosmology companion estimates;
- compact-object hard-floor language in Planck units.

This lane does **not** by itself close:

- charged-lepton Koide,
- quark endpoint/readout issues,
- broader DM uniqueness beyond the exact-target package,
- or the conditional Planck-unit GW-echo exponent lane.

## 4. Exact current obstruction

The current gravity/action package closes only to **lattice units**.

The strongest existing gravity statement is:

> `G_N = 1/(4π)` in lattice units.

That is not yet the same thing as deriving the physical lattice spacing.

The exact remaining calibration step is the physical unit map:

> `G_phys = a^2 G_lat`

with `G_lat = 1/(4π)` on the retained gravity surface.

Until that map is derived internally, the package still needs one explicit
absolute-scale pin.

## 5. Active derivation program

The current open derivation program has three theorem targets.

### Target 1: gravity/action unit-map uniqueness

Best current route.

Goal:

- derive the unique physical normalization map from the already-closed
  discrete/canonical geometric-action family to the physical Einstein-Hilbert
  prefactor, without external Cavendish or light-bending calibration.

Current blocker:

- [ACTION_NORMALIZATION_NOTE.md](./ACTION_NORMALIZATION_NOTE.md) still exhibits
  a real rescaling degeneracy, and
- [GRAVITY_CLEAN_DERIVATION_NOTE.md](./GRAVITY_CLEAN_DERIVATION_NOTE.md)
  explicitly stops at lattice units.

### Target 2: horizon entropy carrier with exact `1/4`

Alternative route.

Goal:

- construct a physical horizon entropy carrier whose asymptotic entropy law is
  exactly `S = A / (4 a^2)`, or prove a broader no-go for the current carrier
  class.

Current blocker:

- the retained carrier already lands on the Widom coefficient `1/6`, not
  `1/4`, via
  [BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md](./BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md).

### Target 3: one-axiom information/action bridge

Framework-compression route.

Goal:

- derive one irreducible physical action/phase unit from the accepted
  information/Hilbert reduction and connect that unit to the gravity/action
  normalization.

Current blocker:

- the one-axiom notes reduce structure and physical-lattice ontology, but do
  not yet fix an absolute unit map.

## 6. Package rule on `main`

Until one of the three targets closes, the correct package statement is:

- `a^(-1) = M_Pl` is a **current package pin on the physical-lattice reading**
- it is **not yet** a theorem of the minimal accepted stack

That is the canonical posture to use when wiring hierarchy, YT/Higgs,
neutrino/DM mass ladders, gravity/cosmology companions, and compact-object
Planck-floor language across the public/package surfaces.
