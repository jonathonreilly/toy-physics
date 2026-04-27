# Hadron Mass Program — Literature Bridges

**Workstream:** `hadron-mass-program-20260427`
**Literature mode:** not explicitly enabled in user invocation; will
be requested per cycle if needed.

This file records every external literature value, theorem, or
convention used in the workstream, with its role.

## Conventions admitted

- **Standard textbook QCD and hadron physics** (Particle Data Group
  values, lattice QCD methodology, chiral perturbation theory).
  References: PDG (2024), FLAG review (lattice averages), Donoghue-
  Golowich-Holstein *Dynamics of the Standard Model*.
  Role: **admitted convention**. Used as the substrate / methodology
  layer between the retained gauge sector and hadron-mass extraction.

- **Wilson / staggered fermion lattice action.** Reference: Wilson
  (1974); Kogut-Susskind (1975). Role: **admitted convention**;
  explicitly included in the framework's microscopic-dynamics layer
  per `MINIMAL_AXIOMS_2026-04-11.md`.

- **Standard SM running of alpha_s.** Reference: PDG QCD section.
  Role: bridge layer for converting retained `alpha_s(M_Z) = 0.1181`
  to the hadronic-scale `alpha_s(~1 GeV)`. The running itself is
  retained-bridge; the M_Z value is retained.

- **Chiral perturbation theory** (Gasser-Leutwyler framework).
  Reference: Gasser-Leutwyler (1984, 1985). Role: **admitted
  convention**; needed for GMOR-based `m_pi` extraction.

## Comparators (used by runners; never derivation inputs)

- **Particle Data Group hadron masses**: `m_p ≈ 938.272 MeV`,
  `m_n ≈ 939.565 MeV`, `m_pi± ≈ 139.570 MeV`, `m_pi0 ≈ 134.977 MeV`,
  `m_K ≈ 493.677 MeV`, `m_rho ≈ 770 MeV`, etc. Role: numerical
  comparator only. Used by runners' verification phase, not as
  derivation inputs.

- **Lattice average string tension**: `sqrt(sigma)_PDG ≈ 440 ± 20
  MeV` (FLAG / lattice consensus). Role: comparator for R1 (`√σ`
  retained promotion).

- **PDG quark masses (MS-bar at 2 GeV)**: `m_u ≈ 2.16 MeV`, `m_d ≈
  4.67 MeV`, `m_s ≈ 93.4 MeV`, `m_c ≈ 1.27 GeV`, `m_b ≈ 4.18 GeV`.
  Role: comparator for Lane 3; this workstream does not retire these
  (Lane 3 owns), but cross-checks Lane-1 outputs against them.

## Theorems imported

None for Cycle 1 (theorem plan is structural / non-derivational).

If later cycles need imported theorems (e.g., Banks-Casher for the
chiral condensate, GMOR for `m_pi^2`), they will be recorded here
with role: **bridge**, **comparator**, **admitted convention**, or
**non-derivation context**.

## Boundary statement

No literature value is a derivation input on the retained surface.
Comparators are used in runners' verification phase only. Admitted
conventions sit at the QCD-bridge layer between the retained core
and the paper surface; they will be flagged on
`docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md` at integration
time.
