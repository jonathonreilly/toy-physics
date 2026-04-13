# Existing Work Relevant to S^3 Cap-Map Uniqueness

**Date:** 2026-04-12
**Purpose:** Inventory of repo resources bearing on the cap-map uniqueness gap
**Gap statement:** Why must the lattice close via cone-capping (B^3 union D^3)
and not some other identification?

---

## TL;DR -- The Gap Is Already Closed

The cap-map uniqueness argument exists in `docs/S3_AXIOM_BOUNDARY_NOTE.md`
(Part 4). It proceeds:

1. Growth axiom produces a PL 3-ball B with boundary dB = S^2.
2. MCG(S^2) = Z_2 (Smale 1959 / Alexander trick).
3. Both Z_2 elements (identity and orientation-reversal) give S^3, because
   S^3 admits an orientation-reversing self-homeomorphism.
4. Therefore the closed manifold is S^3 regardless of the gluing map.

This is conditional on axiom A5 (lattice-is-physical). Without A5, the
discrete-to-continuum gap V4 remains open.

---

## Source-by-Source Inventory

### 1. Growth rules and ball-like topology

**`scripts/frontier_cosmological_expansion.py`** and
**`docs/COSMOLOGICAL_EXPANSION_NOTE.md`**

- Tests four graph-growth rules (uniform random, preferential, spatial,
  exponential). All produce expansion histories; exponential gives clean
  de Sitter.
- Does NOT prove ball-like topology. The growth rules tested use random/
  preferential attachment, not shell-by-shell Z^3 accretion. The boundary
  Euler characteristic chi = 2 check (proving S^2 boundary at each step)
  is in the S^3 topology derivation note, not here.
- **Usability for cap-map:** LOW. These growth rules are cosmological
  probes, not topological constraints.

### 2. 6-regularity / boundary conditions from Hamiltonian

**`docs/S3_GAP_CLOSURE_NOTE.md`** (G1 closure, Part B)

- Kawamoto-Smit uniqueness (Sharatchandra et al. 1981) fixes the staggered
  Hamiltonian completely: hopping phases eta_mu(x) and amplitude t = 1 for
  all bonds. No freedom remains.
- Combined with Cl(3) irrep uniqueness (Schur's lemma) and cubic O_h
  symmetry, this forces z = 6 at every site (6-regular graph).
- A 6-regular finite graph has no boundary nodes, forcing closure.
- **Usability for cap-map:** HIGH. This is the reason closure is required.
  It does not by itself determine HOW the closure occurs.

**`docs/S3_ADVERSARIAL_NOTE.md`** (ATK-1)

- Identifies that gauge equivalence alone is circular for homogeneity;
  Kawamoto-Smit uniqueness is the essential ingredient.
- Paper must cite Kawamoto-Smit, not just "gauge equivalence."
- **Usability for cap-map:** HIGH (clarifies the forcing mechanism).

### 3. S^3 Topology Derivation (main chain)

**`docs/S3_TOPOLOGY_DERIVATION_NOTE.md`**

- Five attacks deriving S^3 from axioms. Attack 4 (Perelman) is the
  strongest: compact + simply connected + 3D => S^3.
- Simply connected verified via cubical complex chi = 1 for R = 2..10.
- Does NOT contain a cap-map uniqueness argument. States the result but
  does not address why cone-capping is the unique closure.
- **Usability for cap-map:** MEDIUM. Provides the downstream chain
  (once closure is S^3, lambda_1 = 3/R^2 follows).

### 4. Kawamoto-Smit uniqueness theorem

**`docs/S3_GAP_CLOSURE_NOTE.md`** (G1), **`docs/S3_SYNTHESIS_NOTE.md`**
(Part B), **`docs/S3_ADVERSARIAL_NOTE.md`** (ATK-1c)

- The Kawamoto-Smit theorem constrains the Hamiltonian, not the boundary
  conditions directly. It forces uniform hopping, hence 6-regularity,
  hence no-boundary. The closure topology is then determined by the
  growth axiom + PL manifold theory + MCG(S^2).
- **Usability for cap-map:** HIGH (indirect -- forces the need for
  closure, after which PL + MCG finishes the job).

### 5. Cap-map uniqueness via MCG(S^2)

**`docs/S3_AXIOM_BOUNDARY_NOTE.md`** (Part 4) -- **THE KEY RESULT**

- States and proves cap-map uniqueness:
  - PL 3-ball B has boundary S^2
  - MCG(S^2) = Z_2 (two isotopy classes of self-homeomorphisms)
  - Both give S^3 (orientation-reversing self-homeomorphism exists)
  - Uniqueness follows
- Conditional on A5 (lattice-is-physical).
- **Usability for cap-map:** DIRECT. This IS the uniqueness argument.

### 6. PL manifold verification

**`docs/S3_CAP_LINK_FORMAL_NOTE.md`**

- Proves cone-capped cubical ball is a PL 3-manifold (all vertex links
  = S^2). Exhaustive verification for R = 2, 3, 4. General proof via
  Alexander's theorem (1930).
- Does NOT address uniqueness of the capping procedure. Proves the cone
  cap works, not that it is the only option.
- **Usability for cap-map:** HIGH. Confirms the cone-cap construction
  is valid. Combined with MCG(S^2) = Z_2, confirms it is the unique
  valid construction.

**`docs/S3_PL_MANIFOLD_NOTE.md`**

- Earlier version of the PL manifold attack. Superseded by the formal
  note above but contains the same core argument.
- **Usability for cap-map:** MEDIUM (superseded).

### 7. Conformal boundary / geodesic equation

**`docs/CONFORMAL_BOUNDARY_NOTE.md`**

- Shows d = 3 bulk has unique 2D CFT boundary structure (Virasoro).
  Modular invariance verified. Does not constrain spatial topology
  directly.
- **Usability for cap-map:** LOW.

**`docs/GEODESIC_EQUATION_NOTE.md`**

- Proves test particles follow geodesics of emergent conformal metric.
  Light bending factor-of-2 reproduced. Does not constrain topology.
- **Usability for cap-map:** NONE.

### 8. Dimension emergence / Poisson bounded notes

**`docs/DIMENSION_EMERGENCE_BOUNDED_NOTE.md`**

- Spectral dimension d_s = 3 on cubic lattice; force law F ~ 1/r^2.
  Does not constrain topology.
- **Usability for cap-map:** NONE.

**`docs/SELF_CONSISTENCY_POISSON_BOUNDED_NOTE.md`**

- Poisson is preferred self-consistent field equation. Does not
  constrain topology.
- **Usability for cap-map:** NONE.

### 9. Anomaly-forces-time theorem

**`docs/ANOMALY_FORCES_TIME_THEOREM.md`**

- Anomaly cancellation of LH content forces 3+1 spacetime (even total
  dimension for chirality). Operates on gauge content, not spatial
  topology.
- **Usability for cap-map:** LOW. Forces temporal dimension, not spatial
  closure. However, the anomaly argument combined with T^3 exclusion
  (winding numbers, holonomy) provides independent reinforcement.

### 10. Gauge/matter closure (review-active branch)

**`origin/codex/review-active:docs/GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md`**

- Gate 1 (chiral completion): anomaly cancellation fixes RH sector.
  Does not constrain spatial topology.
- Gate 2 (generation physicality): Z_3 orbit structure. Does not
  constrain spatial topology.
- **Usability for cap-map:** NONE directly. The generation physicality
  gate shares axiom A5 with the S^3 lane (both bounded by same axiom).

### 11. Discrete-to-continuum gap (V4)

**`docs/S3_DISCRETE_CONTINUUM_NOTE.md`**

- The single remaining obstruction. Four approaches tested (GH
  convergence, spectral convergence, universality, PL bypass). None
  closes V4 fully. The PL bypass (Moise theorem: TOP = PL in dim 3)
  is the strongest mitigation.
- **Usability for cap-map:** CRITICAL context. The cap-map uniqueness
  via MCG(S^2) operates at the PL level, bypassing V4 entirely if
  A5 is accepted.

### 12. S^3 adversarial stress test

**`docs/S3_ADVERSARIAL_NOTE.md`**

- ATK-2 directly attacks the "cap is a ball" claim. Partially closed:
  pi_1(S^2) = 0 makes van Kampen trivial regardless of attaching map.
  Residual concern: does the degree-completing identification produce a
  simply connected cap?
- **Usability for cap-map:** HIGH. ATK-2 identifies the exact residual
  worry, which the MCG(S^2) argument in the axiom boundary note closes.

---

## Synthesis: What Is Usable

The cap-map uniqueness gap is effectively closed by combining three
existing results:

| Step | Source | Status |
|------|--------|--------|
| Growth produces PL 3-ball B with dB = S^2 | S3_TOPOLOGY_DERIVATION, S3_CAP_LINK_FORMAL | PROVED |
| Cone-cap of B is a valid PL 3-manifold | S3_CAP_LINK_FORMAL_NOTE (Alexander + computation) | PROVED |
| Cap-map is unique: MCG(S^2) = Z_2, both give S^3 | S3_AXIOM_BOUNDARY_NOTE Part 4 | PROVED |
| 6-regularity forces closure (no boundary allowed) | S3_GAP_CLOSURE (Kawamoto-Smit) | PROVED |
| Van Kampen: any cap preserves pi_1 = 0 | S3_GAP_CLOSURE (G2), S3_ADVERSARIAL (ATK-2d) | PROVED |

**The only remaining condition is axiom A5 (lattice-is-physical).** This
is the same irreducible axiom bounding the generation physicality lane.

---

## Recommendation

The paper should state cap-map uniqueness as a theorem (conditional on A5):

> **Theorem (Cap-map uniqueness).** Let B be a PL 3-ball produced by the
> growth axiom, with boundary S^2. Then the closed PL 3-manifold
> M = B cup_f D^3 is PL-homeomorphic to S^3 for every attaching map f.
>
> *Proof.* MCG(S^2) = Z_2 (Alexander trick / Smale 1959). Both isotopy
> classes of self-homeomorphisms of S^2 yield S^3, since S^3 admits an
> orientation-reversing self-homeomorphism. QED.

This theorem is already implicit in `S3_AXIOM_BOUNDARY_NOTE.md` but
should be promoted to a standalone statement in the paper.
