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
4. **Physical-lattice reading:** the lattice is treated as physical rather
   than as a regulator. This is the axiom boundary that makes the
   three-generation and low-energy matching discussions physically meaningful.
5. **Canonical normalization and evaluation surface:** the current package uses
   `g_bare = 1` together with the accepted plaquette / `u_0` surface and the
   minimal APBC hierarchy block where applicable.

These are the framework inputs. Everything else in the current publication
package is either retained, bounded, or still open relative to that stack.

## What Already Follows On The Current Package

Retained current consequences:

- exact native `SU(2)`
- graph-first structural `SU(3)`
- anomaly-forced `3+1`
- full-framework one-generation matter closure
- retained three-generation matter structure, with the physical-lattice axiom
  made explicit by
  [GENERATION_AXIOM_BOUNDARY_NOTE.md](GENERATION_AXIOM_BOUNDARY_NOTE.md)
- retained electroweak hierarchy / `v` via
  [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- retained gravity and topology stack as captured in the publication package

## Current Quantitative Package Built On The Same Stack

The current canonical quantitative stack is:

- [ALPHA_S_DERIVED_NOTE.md](ALPHA_S_DERIVED_NOTE.md)
- [RCONN_DERIVED_NOTE.md](RCONN_DERIVED_NOTE.md)
- [YT_EW_COLOR_PROJECTION_THEOREM.md](YT_EW_COLOR_PROJECTION_THEOREM.md)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](YT_COLOR_PROJECTION_CORRECTION_NOTE.md)
- [YT_QFP_INSENSITIVITY_THEOREM.md](YT_QFP_INSENSITIVITY_THEOREM.md)
- [HIGGS_VACUUM_PROMOTED_NOTE.md](HIGGS_VACUUM_PROMOTED_NOTE.md)

Safe current result:

- retained `v = 246.282818290129 GeV`
- retained `alpha_s(M_Z) = 0.1181`
- retained `sin^2(theta_W)(M_Z) = 0.2306`
- retained `1/alpha_EM(M_Z) = 127.67`
- retained `g_1(v) = 0.4644`
- retained `g_2(v) = 0.6480`
- bounded `y_t(v) = 0.9176`
- bounded `m_t(pole) = 172.57 GeV` (2-loop), `173.10 GeV` (3-loop)
- bounded `m_H = 119.8 GeV` (2-loop support route), `125.3 GeV` (framework-side 3-loop route)
- bounded vacuum-stability readout

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
