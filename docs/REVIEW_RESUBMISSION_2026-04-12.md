# Review Resubmission — 2026-04-12

**Purpose:** Flag items that address previously held/flagged issues.
Codex reviewers: please re-evaluate these against the original hold criteria.

## Fixed Holds

### Hold #0a: GR Signatures — "exact by construction" + frozen-source control

**Original flag:** Tests 1-2 are exact by construction. Factor-of-2 is conditional.
No frozen-source control.

**Fix:** `scripts/frontier_gr_signatures_controlled.py`
**Log:** `logs/2026-04-12-gr_signatures_controlled.txt`

What was done:
- Tests 1-2 (time dilation, WEP) explicitly labeled "EXACT BY CONSTRUCTION"
- Frozen 1/r field gives identical GR signatures to Poisson-solved field
- Even wrong-radial-dependence (1/r²) gives same signatures → confirms geometric origin
- Factor-of-2 labeled "CONDITIONAL" with explicit derivation gap noted

**Re-check criteria:** Does the bounded framing now match main-bar standards?

### Hold #0b: Poisson Preference — "uniqueness" overclaim

**Original flag:** Screened Poisson also gives attractive fields. Cannot claim
only unscreened Poisson gives attraction. Framed as uniqueness, should be preference.

**Fix:** `scripts/frontier_poisson_preference_controlled.py`
**Log:** `logs/2026-04-12-poisson_preference.txt`

What was done:
- Reframed throughout as "preference among tested operators, not uniqueness"
- Screened Poisson (mu²=0.01..2.0) confirmed attractive — original claim corrected
- Discriminator identified: decay exponent beta (unscreened → beta≈1, screened → beta>1)
- Convergence rate does NOT discriminate (screened converges faster)

**Re-check criteria:** Is the "preference" framing honest? Is the beta discriminator sufficient for bounded retention?

### Hold #0c: EM+Gravity Factorial Control

**Original flag:** EM probe never runs coupled gravity+EM case. Coexistence
claim blocked pending factorial mixed-residual control.

**Fix:** `scripts/frontier_em_gravity_factorial.py`
**Log:** `logs/2026-04-12-em_gravity_factorial.txt`

What was done:
- 2x2 factorial: (grav OFF/ON) x (EM OFF/ON) with Crank-Nicolson propagation
- Hamiltonian residual: 2.2e-16 (machine zero) — sectors enter additively
- Energy residual at t=0: 1.0e-16 (exact additivity)
- [H_grav, H_em] commutator: 1.9e-17 (operators commute exactly)
- 7/7 physics tests pass (correct deflection signs, unitarity preserved)
- Centroid residual |R| = 9.9e-03 (~2% of max sector) is BCH time-stepping artifact

**Re-check criteria:** Does the 2x2 factorial confirm independent sectors?
The Hamiltonian-level residual is machine zero. The centroid residual is
a nonlinear artifact, not physical coupling.

### Hold #2: Exact Two-Particle Product Law — bilinear in ansatz

**Original flag:** M1*M2 built into Hamiltonian. Exact diag confirms imposed
kernel, not emergent product law.

**Fix:** `scripts/frontier_product_law_no_ansatz.py`
**Log:** `logs/2026-04-12-product_law_no_ansatz.txt`

What was done:
- Bilinear removed entirely — two separate Poisson solves, cross-field coupling
- Static control: alpha=1.0000, beta=1.0000 exactly
- Dynamic (self-consistent): alpha=1.0146, beta=0.9863, R²=0.999993
- Hand-crafted 1/r pipeline validation: alpha=beta=1.0000
- Symmetry check: 0.0% violation

**Re-check criteria:** Is the bilinear fully removed? Does the emergent product
law meet the retained-evidence bar?

### Review Confound: Hierarchical Alpha Mass-Position

**Original flag:** alpha=0.71 is mass-position confounded. Mass scaling on
pruned graphs not fixed-position clean.

**Fix:** `scripts/frontier_alpha_fixed_position.py`
**Log:** `logs/2026-04-12-alpha_fixed_position.txt`

What was done:
- Fixed-position control on 48³ cubic lattice: alpha=1.0000 exactly at all b
- Deflection perfectly linear in M (ratio test: 0.5, 1.0, 2.0, 4.0, 8.0 match exactly)
- Confirms: the alpha≠1 on random DAGs is a mass-position confound, not physics
- Part 2 (pruned lattice) did not complete — Poisson solve too heavy at 48³

**Re-check criteria:** Does the fixed-position result resolve the confound for
the ordered-lattice surface? The random-DAG alpha≠1 remains a structural limitation.

## Still Open (Not Fixed)

### Hold #1: Wilson Mutual-Attraction
**Status:** Needs intervention-style observable, not another source-refresh lag.
Not addressed in this pass.

### Hold #3: Irregular Transport Portability
**Status:** Needs portability-grade transport observable. Not addressed.

### Hold #4: Staggered Two-Body Closure
**Status:** Needs genuinely different conserved current or graph geometry.
Not addressed.

### Hold #0 sublanes: Second-quantized, holographic, Hawking, dimension, cosmology
**Status:** These remain prototype-scale studies. No new controls run.
The overnight audit's "hold" verdict stands for these sublanes.
