# Overnight Claude Audit

**Date:** 2026-04-12
**Scope:** overnight artifacts imported from `claude/youthful-neumann`

## Summary

No overnight artifact is ready for direct promotion to `main`.

The overnight branch does contain useful new work, but the safe read is
substantially narrower than the branch narrative:

- GR-signatures and electromagnetism are bounded consistency checks of the
  chosen discretizations, not GR/Maxwell derivations
- second-quantized and holographic artifacts are finite-size free-fermion or
  single-particle proxy results, not closed many-body field-theory claims
- the Hawking setup is a clean negative on the tested geometry
- dimension and cosmology are toy/proxy studies
- the new dispersion script is still an honest negative with anomalous scaling

## Lane Decisions

### 1. GR-signatures / electromagnetism

Status: `hold`

Files:

- `docs/EMERGENT_GR_SIGNATURES_NOTE.md`
- `scripts/frontier_emergent_gr_signatures.py`
- `docs/ELECTROMAGNETISM_PROBE_NOTE.md`
- `scripts/frontier_electromagnetism_probe.py`

Safe read:

- `S = L(1-f)` reproduces its own time-dilation and k-independence identities
- the tested U(1) edge phases and Coulomb potential give bounded EM-style
  consistency checks on the audited surface

Blockers:

- tests 1 and 2 in the GR note are exact by construction
- the factor-of-2 light-bending row is only conditional on an extra spatial
  metric factor not yet derived from the axioms
- the EM probe does not run a coupled gravity+EM case

### 2. Second-quantized / holographic / Hawking

Status: `hold`

Files:

- `docs/SECOND_QUANTIZED_PROTOTYPE_NOTE.md`
- `scripts/frontier_second_quantized_prototype.py`
- `docs/HOLOGRAPHIC_ENTROPY_NOTE.md`
- `scripts/frontier_holographic_entropy.py`
- `docs/HAWKING_ANALOG_NOTE.md`
- `scripts/frontier_hawking_analog.py`

Safe read:

- the free-fermion prototype gives an overlap-based vacuum-change proxy
- the tested 2D entropy result is area-law-like on modest sizes, not a closed
  many-body area-law claim
- the single-particle propagator entropy is sub-extensive / saturating
- the Hawking setup is a clean negative on the tested geometry

Blockers:

- no dynamical in/out vacuum calculation
- no sharp many-body finite-size closure
- the Hawking mechanism is not a true absorbing thermal horizon

### 3. Dimension / cosmology / dispersion

Status: `hold`

Files:

- `docs/DIMENSION_EMERGENCE_NOTE.md`
- `scripts/frontier_dimension_emergence.py`
- `docs/COSMOLOGICAL_EXPANSION_NOTE.md`
- `scripts/frontier_cosmological_expansion.py`
- `scripts/frontier_dispersion_relation.py`

Safe read:

- the regular-lattice proxy reproduces the expected dimension/force trend
- graph-growth rules produce measurable expansion histories in the chosen proxy
- the dispersion runner still finds a nonzero `k^4` correction

Blockers:

- dimension result is a bounded regular-lattice Poisson proxy, not a universal
  statement that spectral dimension alone determines the force law
- cosmology compares different rules on different clocks and includes a partly
  tautological exponential-growth row
- dispersion scaling is anomalous, so the effective Planck-energy / Fermi-LAT
  reading is not ready for retention

## Promotion Decision

Nothing from this overnight branch is promoted directly to `main` in this pass.

The overnight artifacts are retained on the review branch only, with narrowed
framing, until they either:

1. close their missing controls, or
2. are rewritten into bounded companion notes that meet the current `main` bar
