# Minimal Framework Inputs

**Date:** 2026-04-15
**Status:** current front-door framework memo for the `Cl(3)` / `Z^3` package

This file records the smallest input stack the current package actually uses.
It is not a claim that every downstream lane is already closed, and it is not
route history.

## Minimal Accepted Input Stack

1. **Local algebra:** the physical local algebra is `Cl(3)`.
2. **Spatial substrate:** the physical spatial substrate is the cubic lattice
   `Z^3`.
3. **Microscopic dynamics:** the package works with the finite local
   Grassmann / staggered-Dirac partition and the lattice operators built on
   that surface.
4. **Canonical normalization and evaluation surface:** the current package uses
   `g_bare = 1` together with the accepted plaquette / `u_0` surface and the
   minimal APBC hierarchy block where applicable.

These are the framework inputs. Everything else in the current publication
package is either retained, bounded, or still open relative to that stack.

On the canonical-normalization entry, `g_bare = 1` is now carried by two
independent retained structural routes:

- operator-algebra route:
  [G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
  together with
  [G_BARE_RIGIDITY_THEOREM_NOTE.md](G_BARE_RIGIDITY_THEOREM_NOTE.md)
- 1PI amplitude route:
  [G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md](G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md)
  with the load-bearing Rep-B independence theorem
  [G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md)
  and the off-surface same-1PI pinning theorem
  [G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md](G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md)

A complementary retained obstruction
[G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md](G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md)
closes the Grassmann / spectral dynamical-fixation class negatively.
Under both closure routes plus that obstruction, the residual freedom is
narrowly scoped
(Wilson action form, or axiomatic-bundling reading), not a hidden
continuous coupling parameter.

The physical-lattice reading is no longer carried here as a separate live
input. On the accepted one-axiom Hilbert/locality/information surface it is
derived by [PHYSICAL_LATTICE_NECESSITY_NOTE.md](PHYSICAL_LATTICE_NECESSITY_NOTE.md),
while the old reduced-stack witness survives only in
[GENERATION_AXIOM_BOUNDARY_NOTE.md](GENERATION_AXIOM_BOUNDARY_NOTE.md).

## What Already Follows On The Current Package

Retained current consequences:

- exact native `SU(2)`
- graph-first structural `SU(3)`
- anomaly-forced `3+1`
- full-framework one-generation matter closure
- retained three-generation matter structure, with substrate-level
  physical-lattice reading now derived on the accepted one-axiom surface and
  the older reduced-stack witness isolated by
  [GENERATION_AXIOM_BOUNDARY_NOTE.md](GENERATION_AXIOM_BOUNDARY_NOTE.md)
- retained no-import electroweak hierarchy theorem via
  [HIERARCHY_NO_IMPORT_STATUS_NOTE_2026-04-22.md](HIERARCHY_NO_IMPORT_STATUS_NOTE_2026-04-22.md)
- retained gravity and topology stack as captured in the publication package

## Current Quantitative Package Built On The Same Stack

The current canonical quantitative stack is:

- [ALPHA_S_DERIVED_NOTE.md](ALPHA_S_DERIVED_NOTE.md)
- [RCONN_DERIVED_NOTE.md](RCONN_DERIVED_NOTE.md)
- [YT_EW_COLOR_PROJECTION_THEOREM.md](YT_EW_COLOR_PROJECTION_THEOREM.md)
- [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
- [YT_ZERO_IMPORT_AUTHORITY_NOTE.md](YT_ZERO_IMPORT_AUTHORITY_NOTE.md)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](YT_COLOR_PROJECTION_CORRECTION_NOTE.md)
- [YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md](YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md)
- [YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md](YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)
- [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md)

Safe current result:

- retained no-import `a v = (7/8)^(1/4) * alpha_LM^16`
- retained `alpha_s(M_Z) = 0.1181`
- retained `sin^2(theta_W)(M_Z) = 0.2306`
- retained `1/alpha_EM(M_Z) = 127.67`
- retained `g_1(v) = 0.4644`
- retained `g_2(v) = 0.6480`
- retained exact lattice-scale `y_t(M_Pl) / g_s(M_Pl) = 1 / sqrt(6)`
- bounded companion absolute `v = 246.282818290129 GeV` under
  `a^(-1) = M_Pl`
- derived `y_t(v) = 0.9176`
- derived `m_t(pole) = 172.57 GeV` (2-loop),
  `173.10 GeV` (3-loop)
- Yukawa/top lane is carried by the retained exact lattice-scale Ward theorem
  plus standard lattice-matching / SM-running residuals on the primary route;
  the older `1.2147511%` / `0.75500635%` bridge budget remains an independent
  cross-check
- derived `m_H = 119.8 GeV`
  (2-loop support route), `125.1 GeV` (framework-side 3-loop route), with
  vacuum-stability readout inherited from the current `y_t` lane
- derived vacuum-stability readout with inherited YT-lane precision caveat

## Mathematical Infrastructure Versus Physical Inputs

The current package uses ordinary mathematical infrastructure after the
framework inputs are fixed:

- spectral analysis
- lattice Monte Carlo / plaquette evaluation on the accepted surface
- perturbative low-energy EFT running where the package explicitly labels the
  bridge as bounded or bridge-conditioned

Those tools do not automatically promote a bounded lane to retained. The
publication matrix and derivation / validation map control that promotion.

## What This File Is Not

- not a route-history document
- not a replacement for the publication matrix
- not a claim that DM or CKM are already closed
- not permission to route reviewers through stale side notes instead of the
  canonical package
