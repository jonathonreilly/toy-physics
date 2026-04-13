# Codex Review Packet -- 2026-04-12

**Branch:** `claude/youthful-neumann`
**Purpose:** Single review document for today's execution session on the four
high-priority open gates plus CKM and SU(3) support work.

**Authority:** This packet obeys `review.md` as the sole review-state authority.
Statuses here must not exceed what `review.md` permits.

---

## Top-Level Summary

All lanes are **BOUNDED**. None are CLOSED or STRUCTURAL.

| Lane | Status | One-line summary |
|------|--------|------------------|
| 1. Generation physicality | BOUNDED | Closed conditional on the framework's physical-lattice assumption (A5); unconditionally open |
| 2. S^3 compactification | BOUNDED | PL manifold attack narrows V4; cap/link formal proof not yet complete |
| 3. DM relic mapping | BOUNDED | g_bare bounded via Cl(3) normalization; Coulomb derived from lattice; Boltzmann/Friedmann imported |
| 4. Renormalized y_t | BOUNDED | Bare UV theorem closed; renormalized matching step still open |
| 5. CKM | BOUNDED | Sharp analytic obstruction: Higgs Z_3 charge not L-independent |
| 6. Gauge couplings | BOUNDED | SU(2) normalization bounded; U(1) still scan/fitted |
| Bonus: SU(3) | BOUNDED | Canonical closure chain 158/158; no live structural objection |

**Codex finding 19 (generation):** The new axiom-boundary work is a real
upgrade. The safe paper claim is: "generation physicality is closed
conditional on the framework's physical-lattice assumption." This assumption
(A5) is the physical interpretation already built into the framework's working
axiom (Cl(3) on Z^3 as the physical substrate, not a mere regulator). It is
NOT safe to claim generation is unconditionally closed.

**Codex finding 20 (unified A5 story):** The A5/physical-lattice framing is
acceptable for generation (finding 19). It is NOT yet acceptable as a full
collapse of S^3, DM, and renormalized y_t to "only A5," because those lanes
still retain additional mathematical or imported-physics gaps in their own
notes.

---

## Lane 1: Generation Physicality

### Status: BOUNDED

**Paper-safe claim:** Generation physicality is closed conditional on the
framework's physical-lattice assumption (A5). Unconditionally, generation
physicality remains open. The remaining non-derived content is A5 itself,
not an additional missing theorem.

**What A5 is:** The ontological commitment that Cl(3) on Z^3 is the physical
substrate, not a regularization to be removed. This is the same assumption
that underlies every other framework prediction (gauge groups, spacetime
dimension, anomaly cancellation). It is the framework's working axiom, not a
late-stage ad hoc addition.

### Exact results (conditional on A5)

1. **Fermi-point spectral theorem** (`frontier_generation_fermi_point.py`,
   EXACT PASS=7, BOUNDED PASS=1): 8 BZ corners with Wilson mass grouping
   1+3+3+1 by Hamming weight. The 3 lightest nonzero species have degeneracy
   C(3,1)=3, unique to d=3. Species distinguished by lattice momenta (exact
   quantum numbers).

2. **Rooting-undefined theorem** (`frontier_generation_rooting_undefined.py`,
   PASS=37 FAIL=0): Fourth-root trick is not well-defined in the Hamiltonian
   formulation. Three independent obstructions: Cl(3) irreducibility (0/246
   subspaces), taste transitivity (exhaustive), spectral change (27/27
   eigenvalues differ).

3. **Z_3 superselection** (`frontier_generation_physicality_wildcard.py`,
   PASS=48 FAIL=0): Schur's lemma gives block-diagonal structure. 't Hooft
   anomaly: merging any two generations changes Z_3 anomaly from 0 to 2 mod 3.

4. **Axiom boundary theorem** (`frontier_generation_axiom_boundary.py`,
   PASS=31 FAIL=0): Four-part proof that A5 is necessary, sufficient, and
   irreducible for generation physicality. All 17 steps in the generation
   chain classified: 6 theorems, 7 computations, 3 A5-dependent, 1 bounded.

5. **Gauge universality** (`frontier_generation_gauge_universality.py`,
   `GAUGE_UNIVERSALITY_ALGEBRAIC_DERIVATION.md`): All 3 hw=1 species carry
   identical gauge representations. Bounded result that strengthens the
   generation case but does not close it.

6. **Nielsen-Ninomiya extension** (`frontier_generation_nielsen_ninomiya.py`,
   PASS=60 FAIL=0): Poincare-Hopf topological index enforces 1+3+3+1
   decomposition. No single-triplet rooting is possible. Bounded: does not
   address taste-vs-generation interpretive gap.

7. **Discrete anomaly forcing** (`frontier_generation_anomaly_forces_three.py`,
   PASS=51 FAIL=0): Discrete Z_3 anomaly prevents sector merging; continuous
   anomaly alone does NOT force 3 generations (honest negative). Combined
   argument conditional on taste-physicality.

8. **Scattering distinguishability** (`frontier_generation_scattering.py`,
   PASS=16 FAIL=0): Z_3 sectors produce measurably different scattering
   outcomes. Bounded: strengthens case but does not close gate.

9. **Little groups analysis** (`frontier_generation_little_groups.py`,
   PASS=14 FAIL=0): Full Oh symmetry with taste transforms. Documents
   obstruction: free Hamiltonian has too much symmetry to distinguish species
   by crystallographic methods alone. Bounded.

10. **Deep analysis** (`GENERATION_PHYSICALITY_DEEP_ANALYSIS.md`): Maps the
    exact logical gap. The obstruction is irreducibly ontological (A5).

### Honest obstructions documented

- Z_3 is a symmetry of the mass spectrum but NOT of the full Hamiltonian
  (found in axiom-first analysis, `frontier_generation_axiom_first.py` 3 FAILs)
- Berry phase approach: NEGATIVE (`frontier_generation_berry_phase.py` FAIL=10)
- K-theory approach: obstruction documented (`frontier_generation_ktheory.py`)
- Little-group route: sharp negative (too much symmetry)
- Self-duality for g_bare: NEGATIVE (`frontier_g_bare_self_duality.py`)

### Key notes

- `GENERATION_AXIOM_BOUNDARY_THEOREM_NOTE.md` -- primary obstruction theorem
- `GENERATION_FERMI_POINT_THEOREM_NOTE.md` -- primary spectral argument
- `GENERATION_ROOTING_UNDEFINED_NOTE.md` -- rooting obstruction
- `GENERATION_PHYSICALITY_DEEP_ANALYSIS.md` -- logical gap map
- `GAUGE_UNIVERSALITY_ALGEBRAIC_DERIVATION.md` -- gauge universality
- `MASS_HIERARCHY_HONEST_ASSESSMENT_NOTE.md` -- honest mass hierarchy assessment
- `GENERATION_PHYSICALITY_OBSTRUCTION_NOTE.md` -- sharp obstruction
- `GENERATION_LITTLE_GROUPS_NOTE.md` -- little-groups obstruction
- `GENERATION_3FAILS_INVESTIGATION_NOTE.md` -- commutant inequivalence (bounded)
- `GENERATION_NIELSEN_NINOMIYA_NOTE.md` -- topological forcing (bounded)
- `GENERATION_ANOMALY_FORCES_THREE_NOTE.md` -- anomaly forcing (bounded)

### Why the claim is not overstated

The status is BOUNDED, not CLOSED. Every exact result is conditional on A5.
The axiom boundary theorem explicitly proves A5 is irreducible and cannot be
derived from {A1-A4}. The mass hierarchy within the 3 species is explicitly
labeled BOUNDED (order-of-magnitude, not precision). Negative results (Berry
phase, K-theory, little groups) are honestly documented. Per Codex finding 19,
the safe paper claim is "closed conditional on the framework's physical-lattice
assumption." Per Codex finding 20, this framing is acceptable for generation
but not for collapsing S^3, DM, or y_t to "only A5."

---

## Lane 2: S^3 Compactification

### Status: BOUNDED

**Paper-safe claim:** Topology lane is bounded until compactification is
derived. The PL manifold approach is a useful bounded structural attack.
S^3 is not yet forced.

### What has been done

1. **PL manifold attack** (`frontier_s3_pl_manifold.py`, PASS=9 FAIL=0):
   Interior vertex links = octahedron = PL S^2. Boundary surface chi=2.
   Cone-cap closure produces closed PL 3-manifold. pi_1=0 by van Kampen.
   Perelman + Moise => PL S^3. Narrows V4 but does not close it: the
   boundary vertex link argument for general R cites Alexander's theorem
   rather than proving it from scratch.

2. **V4 investigation** (`frontier_s3_discrete_continuum.py`, EXACT PASS=3,
   BOUNDED PASS=1 FAIL=2): Four approaches tested (Gromov-Hausdorff,
   spectral, combinatorial manifold, quasi-isometry). None closes V4.
   The gap is standard in lattice field theory but not a rigorous
   mathematical theorem.

3. **RP^3 vs S^3** (`RP3_VS_S3_NOTE.md`, `frontier_rp3_vs_s3.py`):
   Useful bounded consistency note. RP^3 eigenvalue correction and fiber/base
   distinction are useful. Does NOT close the topology lane or justify saying
   S^3 is fully derived.

4. **Original derivation chain** (`frontier_s3_compactification.py` PASS=10
   FAIL=2, `frontier_s3_gap_closure.py` PASS=18 FAIL=0,
   `frontier_s3_synthesis.py` PASS=29 FAIL=0): Algebraic steps are exact.
   G1/A4 (homogeneity), G2 (van Kampen), T^3 exclusion all addressed.
   The main vulnerability remains the discrete-to-continuum gap (V4).

### Why the claim is not overstated

The status is BOUNDED, not STRUCTURAL or CLOSED. Per review.md: "topology lane
is bounded until compactification is derived." Per Codex finding 20, the
unified A5 story does NOT yet close S^3 because the lane retains its own
mathematical gaps (V4, cap/link formalization). The PL manifold approach is
real progress but the general-R proof is not complete. The earlier "STRUCTURAL"
label that appeared in previous versions of this packet is withdrawn.

---

## Lane 3: DM Relic Mapping

### Status: BOUNDED

**Paper-safe claim:** Structural DM inputs plus universal thermal freeze-out;
bounded consistency, not first-principles relic closure.

### What has been done

1. **Coulomb from lattice** (`frontier_dm_coulomb_from_lattice.py`, PASS=61
   FAIL=0): V(r) = -C_F * g^2 * G(r) derived from lattice Poisson Green's
   function. Reduces import count from 2 to 1 (sigma_v still imported).

2. **Thermodynamic closure** (`frontier_dm_thermodynamic_closure.py`, PASS=15
   FAIL=0): Corrects documentation: "continuum limit" dependencies were
   actually thermodynamic-limit dependencies. Weyl's law on PL manifolds
   guarantees convergence. Finite-size corrections negligible at physical N.

3. **g_bare = 1** (`G_BARE_DERIVATION_NOTE.md`, `G_BARE_SELF_DUALITY_NOTE.md`):
   Cl(3) normalization argument is bounded. Self-duality investigation is an
   honest negative: cannot be elevated to theorem grade. g_bare remains a
   bounded normalization argument, not a theorem-grade elimination of the
   DM coupling assumption (per review.md finding 10).

4. **Relic abundance** (`frontier_dm_relic_synthesis.py`, R=5.48 +/- 0.19):
   Matches to 0.2% central but 3.5% theoretical band. Thermodynamic limit
   assumption is standard but not rigorously proved for this graph family.

### Why the claim is not overstated

The status is BOUNDED, not CLOSED. Per review.md: "graph-native mapping to
physical relic abundance without importing the Boltzmann/Friedmann freeze-out
layer as if it were derived" remains open. g_bare = 1 is bounded (Cl(3)
normalization, not theorem-grade). sigma_v is still imported. The DM relic
lane cannot be collapsed to "only A5" per Codex finding 20 because it retains
imported-physics gaps (Boltzmann/Friedmann).

---

## Lane 4: Renormalized y_t Matching

### Status: BOUNDED

**Paper-safe claim:** Bare theorem closed; renormalized matching still open.

### What has been done

1. **Bare UV theorem** (`frontier_renormalized_yt.py` PASS=33 FAIL=1,
   `frontier_renormalized_yt_wildcard.py` PASS=31 FAIL=0): Tree-level
   normalization surface established. y_t = g_s/sqrt(6) as bare boundary
   condition.

2. **Cl(3) centrality** (d=3 specific): G_5 = iG_1G_2G_3 is in the center
   of Cl(3). Vertex factorization D[G_5] = G_5 * D[I] at all loop orders.
   Verified at 1-loop to 10^-17 on L=8.

3. **Slavnov-Taylor identity** (`frontier_slavnov_taylor_completion.py`,
   PASS=26 FAIL=0): Derived from bipartite anticommutation and G_5
   centrality. No perturbative expansion or weak-coupling assumption needed.

4. **Prediction:** m_t = 174.2 GeV (+0.7% from observed 173.0 GeV). Within
   the 3-5% SM RGE uncertainty band over 17 decades.

### Why the claim is not overstated

The status is BOUNDED, not CLOSED. Per review.md: "bare theorem closed;
renormalized matching still open." The non-renormalization is exact at the
lattice scale, but the renormalized matching step (Z_Y(mu) = Z_g(mu) or
equivalent) is not proved. The alpha_s = 0.092 input comes from a separate
BOUNDED lane (gauge couplings). Per Codex finding 20, y_t cannot be collapsed
to "only A5" because it retains its own mathematical gap (renormalized
matching).

---

## Lane 5: CKM

### Status: BOUNDED

**Paper-safe claim:** Bounded lattice support, not a quantitative CKM theorem.

### What has been done

`frontier_ckm_higgs_z3_universal.py` (PASS=8 FAIL=0): Sharp analytic
obstruction proved. The staggered mass operator eps(x) does NOT carry a
well-defined Z_3 charge. Equal weight on delta=1 and delta=2; vanishes for
L divisible by 6; decays as O(1/L^d). The L=8 "confirmation" in the original
CKM script was a false positive (a tie, not dominance).

### Why the claim is not overstated

The status is BOUNDED. Per review.md: "CKM remains bounded until the Higgs
Z_3 charge is L-independent." The obstruction note proves this specific
mechanism cannot work and documents four potential alternative routes (none
developed).

---

## Lane 6: Gauge Couplings

### Status: BOUNDED

**Paper-safe claim:** SU(2) normalization is at best a bounded consistency
result; U(1) is still scan/fitted.

---

## Bonus: SU(3) Canonical Closure

### Status: BOUNDED (no live structural objection)

`frontier_su3_canonical_closure.py` (PASS=158 FAIL=0): Canonical closure
chain from Z^3 graph shifts through quartic selector to su(3) + u(1)
commutant. Uses KS tensor product structure. Does not derive confinement,
dynamics, or generations.

---

## Latest Additions Referenced

The following honest bounded/negative additions are referenced in this packet
and treated as bounded strengthenings or obstruction notes, not gate closures:

- `GENERATION_AXIOM_BOUNDARY_THEOREM_NOTE.md` / `frontier_generation_axiom_boundary.py`
- `GAUGE_UNIVERSALITY_ALGEBRAIC_DERIVATION.md` / `frontier_generation_gauge_universality.py`
- `GENERATION_PHYSICALITY_DEEP_ANALYSIS.md`
- `MASS_HIERARCHY_HONEST_ASSESSMENT_NOTE.md`
- `REMAINING_CRITIQUE_TARGETS_2026-04-12.md`
- `GENERATION_LITTLE_GROUPS_NOTE.md` / `frontier_generation_little_groups.py`
- `GENERATION_ROOTING_UNDEFINED_NOTE.md` / `frontier_generation_rooting_undefined.py`
- `GENERATION_3FAILS_INVESTIGATION_NOTE.md` / `frontier_generation_3fails_investigation.py`
- `RP3_VS_S3_NOTE.md` / `frontier_rp3_vs_s3.py`
- `G_BARE_SELF_DUALITY_NOTE.md` / `frontier_g_bare_self_duality.py`
- `GENERATION_ANOMALY_FORCES_THREE_NOTE.md` / `frontier_generation_anomaly_forces_three.py`
- `DM_THERMODYNAMIC_CLOSURE_NOTE.md` / `frontier_dm_thermodynamic_closure.py`
- `GENERATION_NIELSEN_NINOMIYA_NOTE.md` / `frontier_generation_nielsen_ninomiya.py`
- `UNIFIED_AXIOM_BOUNDARY_NOTE.md` (acceptable for generation per finding 19;
  NOT acceptable as collapse for S^3, DM, y_t per finding 20)

---

## Test Summary

| Script | PASS | FAIL | Category |
|--------|------|------|----------|
| frontier_generation_fermi_point.py | 8 | 0 | Exact + bounded |
| frontier_generation_rooting_undefined.py | 37 | 0 | Exact |
| frontier_generation_physicality_wildcard.py | 48 | 0 | Exact |
| frontier_generation_axiom_boundary.py | 31 | 0 | Exact + logical |
| frontier_generation_gauge_universality.py | -- | -- | Bounded |
| frontier_generation_nielsen_ninomiya.py | 60 | 0 | Exact |
| frontier_generation_anomaly_forces_three.py | 51 | 0 | Exact |
| frontier_generation_scattering.py | 16 | 0 | Exact |
| frontier_generation_little_groups.py | 14 | 0 | Exact |
| frontier_generation_axiom_first.py | 36 | 3 | Exact + bounded |
| frontier_generation_berry_phase.py | 15 | 10 | Negative |
| frontier_generation_ktheory.py | 21 | 0 | Bounded (obstruction) |
| frontier_generation_physicality.py | 13 | 6 | Exact + bounded |
| frontier_generation_physicality_wildcard.py | 48 | 0 | Exact |
| frontier_generation_gap_closure.py | 10 | 1 | Bounded |
| frontier_generation_physicality_obstruction.py | 24 | 0 | Exact |
| frontier_generation_3fails_investigation.py | -- | -- | Bounded |
| frontier_s3_pl_manifold.py | 9 | 0 | Exact |
| frontier_s3_discrete_continuum.py | 4 | 2 | Exact + bounded |
| frontier_s3_compactification.py | 10 | 2 | Mixed |
| frontier_s3_gap_closure.py | 18 | 0 | Exact |
| frontier_s3_synthesis.py | 29 | 0 | Exact |
| frontier_rp3_vs_s3.py | -- | -- | Bounded |
| frontier_dm_coulomb_from_lattice.py | 61 | 0 | Derived |
| frontier_dm_thermodynamic_closure.py | 15 | 0 | Exact + derived |
| frontier_dm_relic_mapping.py | 9 | 1 | Native + bounded |
| frontier_dm_relic_gap_closure.py | 11 | 0 | Derived |
| frontier_dm_relic_synthesis.py | 4 | 0 | Bounded |
| frontier_renormalized_yt.py | 33 | 1 | Exact + bounded |
| frontier_renormalized_yt_wildcard.py | 31 | 0 | Exact |
| frontier_slavnov_taylor_completion.py | 26 | 0 | Exact |
| frontier_ckm_higgs_z3_universal.py | 8 | 0 | Exact (obstruction) |
| frontier_su3_canonical_closure.py | 158 | 0 | Bounded |
| frontier_g_bare_self_duality.py | 20 | 0 | Negative |
| frontier_mass_hierarchy_synthesis.py | 15 | 0 | Bounded |
| frontier_generation_synthesis.py | 36 | 0 | Exact |

---

## Guardrails Compliance

- No lane is labeled CLOSED or STRUCTURAL
- Every per-lane section matches the top summary (all BOUNDED)
- Generation uses Codex finding 19 language exactly
- S^3, DM, y_t are NOT collapsed to "only A5" per Codex finding 20
- Model-level results are labeled BOUNDED throughout
- Negative results (Berry phase, K-theory, little groups, self-duality) are
  honestly documented
- Mass hierarchy is explicitly order-of-magnitude
- The UNIFIED_AXIOM_BOUNDARY_NOTE.md is referenced only for generation, not
  for S^3/DM/y_t
- g_bare is a bounded normalization argument, not theorem-grade
- DM_RELIC_GAP_CLOSURE_NOTE.md is not cited as closure
- S3_PL_MANIFOLD_NOTE.md is not cited as closing the topology lane
- RENORMALIZED_YT_THEOREM_NOTE.md is not cited as CLOSED
- No "generation physicality gate: closed" language appears anywhere
- No "S^3 forced" or "S^3 derived" language appears anywhere
- No "DM relic mapping closed" language appears anywhere

---

## Findings Register

| # | Finding | Status in this packet |
|---|---------|---------------------|
| 4 | Packet overstates multiple lane statuses | FIXED: all lanes BOUNDED |
| 11 | S^3 as STRUCTURAL, y_t as CLOSED, DM as CLOSED | FIXED: all BOUNDED |
| 12 | Later sections re-promote statuses | FIXED: every section matches top summary |
| 14 | Packet not self-consistent all the way through | FIXED: full rewrite for consistency |
| 15 | Axiom boundary theorem is real upgrade | INCORPORATED: finding 19 language used |
| 16 | Unified A5 overstates for S^3/DM/y_t | INCORPORATED: finding 20 limits applied |
| 19 | Generation closed conditional on A5 | INCORPORATED: exact language used |
| 20 | A5 collapse not accepted for S^3/DM/y_t | INCORPORATED: explicitly excluded |
