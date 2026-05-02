# Minimal Framework Inputs

**Date:** 2026-04-15 (last citation-graph repair: 2026-05-02)
**Status:** current public framework memo for the `Cl(3)` / `Z^3` package

This file records the smallest input stack the current package actually uses.
It is not a claim that every downstream lane is already closed, and it is not
route history.

## Audit-graph note (2026-05-02)

This note's body lists *both* the four-axiom input stack (A1–A4) and a number
of supporting / consilience / downstream-consequence references for reader
navigation. The Apr 30 audit of `minimal_axioms_2026-04-11` flagged that the
markdown-linked references were being parsed by the citation-graph builder
as one-hop upstream dependencies, which inflated A_min's apparent dep set
to 18 nodes (most of them genuine *downstream* consequences) and propagated
`audited_conditional` status. This repair (2026-05-02) restructures the
note so that supporting and consequence references are recorded in plain
text (filenames in backticks) rather than markdown links. The four axioms
A1–A4 below are self-contained and do not depend on any other source note.

The plain-text references here are not load-bearing for A_min itself; they
are pointers for readers who want to follow the framework chain.

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

These four are the framework inputs. Everything else in the current
publication package is either retained, bounded, or still open relative to
that stack.

## Consilience Evidence for A4 (Plain-Text Pointers, Not Strict Prerequisites)

The choice `g_bare = 1` in A4 is a normalization axiom — it is adopted by
fiat, not derived. Several independent retained structural arguments
provide supporting *consilience* evidence that this is the right choice:

- operator-algebra route: see `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`
  together with `G_BARE_RIGIDITY_THEOREM_NOTE.md`
- 1PI amplitude route: see `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md` with
  the load-bearing Rep-B independence statement in
  `G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md` and the
  off-surface same-1PI pinning theorem in
  `G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`
- complementary retained obstruction:
  `G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md` closes the
  Grassmann / spectral dynamical-fixation class negatively

Under both closure routes plus that obstruction, the residual freedom in
A4's normalization choice is narrowly scoped (Wilson action form, or
axiomatic-bundling reading) — not a hidden continuous coupling parameter.

The physical-lattice reading is no longer carried as a separate live input.
On the accepted one-axiom Hilbert/locality/information surface it is derived
in `PHYSICAL_LATTICE_NECESSITY_NOTE.md`, while the older reduced-stack
witness survives only in `GENERATION_AXIOM_BOUNDARY_NOTE.md`. Neither is
load-bearing for A_min's identity.

## Downstream Consequences (Plain-Text Pointers)

The following are *consequences* that follow from A_min plus admissible
mathematical infrastructure. They are listed here for reader navigation.
They are *not* upstream dependencies of A_min:

Retained current consequences (prose-level):

- exact native `SU(2)`
- graph-first structural `SU(3)`
- anomaly-forced `3+1`
- full-framework one-generation matter closure
- retained three-generation matter structure, with substrate-level
  physical-lattice reading on the accepted one-axiom surface and the older
  reduced-stack witness isolated by `GENERATION_AXIOM_BOUNDARY_NOTE.md`
- retained electroweak hierarchy / `v` via
  `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
- retained gravity and topology stack as captured in the publication package

Current quantitative package built on the same stack (plain-text
references; downstream of A_min, not load-bearing for it):

- `ALPHA_S_DERIVED_NOTE.md`
- `RCONN_DERIVED_NOTE.md`
- `YT_EW_COLOR_PROJECTION_THEOREM.md`
- `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
- `YT_ZERO_IMPORT_AUTHORITY_NOTE.md`
- `YT_COLOR_PROJECTION_CORRECTION_NOTE.md`
- `YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md`
- `YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`
- `HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md`

Safe current quantitative results (downstream consequences):

- retained `v = 246.282818290129 GeV`
- retained `alpha_s(M_Z) = 0.1181`
- retained `sin^2(theta_W)(M_Z) = 0.2306`
- retained `1/alpha_EM(M_Z) = 127.67`
- retained `g_1(v) = 0.4644`
- retained `g_2(v) = 0.6480`
- retained exact lattice-scale `y_t(M_Pl) / g_s(M_Pl) = 1 / sqrt(6)`
- derived `y_t(v) = 0.9176`
- derived `m_t(pole) = 172.57 GeV` (2-loop), `173.10 GeV` (3-loop)
- Yukawa/top lane is carried by the retained exact lattice-scale Ward
  theorem plus standard lattice-matching / SM-running residuals on the
  primary route; the older `1.2147511%` / `0.75500635%` bridge budget
  remains an independent cross-check
- derived `m_H = 119.8 GeV` (2-loop support route), `125.1 GeV`
  (framework-side 3-loop route), with vacuum-stability readout inherited
  from the current `y_t` lane
- derived vacuum-stability readout with inherited YT-lane precision caveat

## Mathematical Infrastructure Versus Physical Inputs

The current package uses ordinary mathematical infrastructure after the
framework inputs are fixed:

- spectral analysis
- lattice Monte Carlo / plaquette evaluation on the accepted surface
- perturbative low-energy EFT running where the package explicitly labels
  the bridge as bounded or bridge-conditioned

Those tools do not automatically promote a bounded lane to retained. The
publication matrix and derivation / validation map control that promotion.

## What This File Is Not

- not a route-history document
- not a replacement for the publication matrix
- not a claim that DM or CKM are already closed
- not permission to route reviewers through stale side notes instead of
  the canonical package
