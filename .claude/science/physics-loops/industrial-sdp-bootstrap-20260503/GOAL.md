# GOAL — Industrial-SDP Bootstrap Campaign

**Slug:** `industrial-sdp-bootstrap-20260503`
**Date launched:** 2026-05-03
**Mode:** campaign (12h budget, literature allowed)
**Predecessor:** unblocked by infra PR [#430](https://github.com/jonathonreilly/cl3-lattice-framework/pull/430) (CVXPY venv setup)

## Context

Prior `plaquette-bootstrap-closure-20260503` campaign blocks 01 (PR
[#420](https://github.com/jonathonreilly/cl3-lattice-framework/pull/420))
and 02 (PR [#423](https://github.com/jonathonreilly/cl3-lattice-framework/pull/423))
established the framework integration (Lemmas BB1, BB1', BB3) but were
forced to small-truncation **analytical** bounds because CVXPY install
was blocked by PEP 668. With the venv now working (cvxpy 1.8.2 +
CLARABEL/SCS), we can run **actual SDP-based** bootstrap.

## Realistic 12h scope (with CLARABEL/SCS, not Mosek)

CLARABEL/SCS suffice for L_max ≤ 8 / matrices ~100×100. Industrial
precision (Kazakov-Zheng 2022 at L_max=16, ~6505×6505 matrices reduced
via 20-irrep symmetry, requires Mosek) is out of reach without Mosek
academic license + ~3-month engineering. This campaign targets the
**reachable subset**:

- Real CVXPY-based moment-problem bootstrap on the framework's
  V-singlet Wilson-loop subalgebra
- Validation on SU(2) single-plaquette where Bessel-function reference
  gives exact answer
- SU(3) ⟨P⟩(β=6) bracket via SDP at small L_max
- Honest precision: ~5–15% wide bracket from L_max ≤ 6 with CLARABEL/SCS

## Targets

**Block 01 (PRIMARY):** SU(2) baseline + CVXPY infrastructure
- Implement CVXPY-based moment bootstrap on SU(N) plaquette
- Validate on SU(2) at small β (Bessel reference for single-plaquette;
  Kazakov-Zheng SU(2) for finite lattice)
- Document the bootstrap workflow as reusable infrastructure

**Block 02 (SECONDARY):** SU(3) ⟨P⟩(β=6) bracket
- Extend SU(2) infrastructure to SU(3)
- Apply Hamburger / Hausdorff moment constraints + framework's
  mixed-cumulant audit + RP-derived PSD
- Get a real (loose) bracket on ⟨P⟩(β=6)
- Compare to bridge-support stack analytic upper-bound (0.59353) and
  canonical MC (0.5934) and prior named-obstruction stretch (PRs
  [#420](https://github.com/jonathonreilly/cl3-lattice-framework/pull/420),
  [#423](https://github.com/jonathonreilly/cl3-lattice-framework/pull/423))

## Stop conditions

- Runtime exhaustion (12h)
- Volume cap (5 PRs / 24h)
- Cluster cap (2 PRs per `gauge_vacuum_plaquette_*` family per campaign;
  this is a fresh campaign so cap resets — but plan for max 2 PRs)
- Corollary exhaustion or value-gate exhaustion

## Forbidden imports

- PDG values
- Lattice-MC `⟨P⟩=0.5934` as load-bearing (comparator only)
- Hard-coded bootstrap brackets from literature
- Same-surface family arguments
