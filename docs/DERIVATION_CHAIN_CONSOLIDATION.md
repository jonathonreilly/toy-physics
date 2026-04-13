# Derivation Chain Consolidation: Cl(3) on Z^3

**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`
**Purpose:** Complete audit of the logical dependency structure from the
single axiom system to all derived results.

---

## 1. The Complete Derivation Tree (DAG)

The single axiom system is **Cl(3) algebra on the Z^3 lattice** (staggered
fermions with Hamiltonian dynamics on a cubic graph).  Every result below
traces back to this root plus at most one or two ancillary physical inputs.

```
AXIOM: Cl(3) on Z^3
  |
  +--[A] KS tensor decomposition: V = C^2 x C^2 x C^2
  |    |
  |    +--[B] Cl(3) generators: Gamma_mu = sigma_z^{x(mu-1)} x sigma_x x I^{x(3-mu)}
  |    |    |
  |    |    +--[C] Gamma_5 = iG1G2G3 is CENTRAL in Cl(3) [d=3 odd]
  |    |    |    |
  |    |    |    +--[L1] Vertex factorization: D[G5] = G5 * D[I]   --+
  |    |    |    |                                                     |
  |    |    |    +--[L2] Self-energy in even subalgebra                |
  |    |    |                                                          |
  |    |    +--[D] Bipartite structure: {eps, D_hop} = 0               |
  |    |    |    |                                                     |
  |    |    |    +--[E] Ward identity: {eps, D_stag} = 2mI             |
  |    |    |    |    |                                                |
  |    |    |    |    +--[F] ST identity: {eps, Lambda_mu} = 0    ----+
  |    |    |    |                                                     |
  |    |    |    +--[G] No fourth-root trick (Hamiltonian, no det)     |
  |    |    |                                                          v
  |    |    +--[H] Staggered mass = Gamma_5 (taste basis)    [LANE 4: y_t CLOSURE]
  |    |         |                                             y_t = g_s/sqrt(6) exact
  |    |         +--[I] Chiral projector P+ trace = 1/2        at UV; SM RGE below
  |    |         |    |                                        => m_t = 174.2 GeV
  |    |         |    +--[J] y_t = g_s / sqrt(2*N_c)
  |    |         |         (Yukawa-gauge trace identity)
  |    |         |
  |    |         +--[K] Wilson mass m_W(s) = 2r|s|/a
  |    |              |
  |    |              +--- see [T] below (generation mass levels)
  |    |
  |    +--[M] Graph shifts S_i = sigma_x on factor i
  |    |    |
  |    |    +--[N] Quartic selector V_sel = Tr H^4 - (Tr H^2)^2/8
  |    |         |   has 3 axis minima => spontaneous S3 -> Z2 breaking
  |    |         |
  |    |         +--[O] Selected axis => unique su(2) on that factor
  |    |              |
  |    |              +--[P] SWAP of remaining 2 factors (forced)
  |    |                   |
  |    |                   +--[Q] Commutant = su(3) + u(1)
  |    |                        |   Sym^2(C^2) = C^3 (quarks)
  |    |                        |   Anti^2(C^2) = C^1 (leptons)
  |    |                        |
  |    |                        +--[R] Hypercharge Y = +1/3, -1
  |    |                             |
  |    |                             +--- [LANE: GAUGE ALGEBRA CLOSED]
  |    |                             |    su(2) + su(3) + u(1) with
  |    |                             |    (2,3)_{+1/3} + (2,1)_{-1}
  |    |                             |
  |    |                             +--- feeds [ANOMALY] below
  |    |
  |    +--[S] Z_3 cyclic permutation of 3 tensor factors
  |         |   (Oh point group element)
  |         |
  |         +--[T] Orbit decomposition: 8 = 1+3+3+1 by Hamming weight
  |         |    |   (Burnside's lemma; d=3 uniquely gives two size-3 orbits)
  |         |    |
  |         |    +--[U] Wilson mass levels: 0, 2r, 4r, 6r
  |         |    |    |
  |         |    |    +--[V] Inter-orbit mass splitting (exact)
  |         |    |    +--[W] No continuum limit => splittings physical
  |         |    |         (see [NCL] below)
  |         |    |
  |         |    +--[X] Distinct gauge quantum numbers per orbit
  |         |    |    (T3 multiplicity distributions reversed)
  |         |    |
  |         |    +--[Y] Radiative distinction: Delta_g ~ hw/pi^2
  |         |    |    (inter-orbit ratio exactly 2)
  |         |    |
  |         |    +--[Z] Bit-flip C = sigma_x^{x3}: T1 <-> T2
  |         |    |    (weak-isospin conjugation)
  |         |    |
  |         |    +--[AA] Anomaly forcing: opposite chirality
  |         |    |    required for T1 vs T2
  |         |    |    (=> matter vs antimatter assignment)
  |         |    |
  |         |    +--[AB] EWSB breaks Z3 -> Z2: 1+2 split
  |         |    |    (heavy generation couples directly to VEV)
  |         |    |
  |         |    +--[AC] CP phase delta = 2pi/3 from Z3 rep theory
  |         |    |    => J(Z3)/J(PDG) = 2.48 (parameter-free)
  |         |    |
  |         |    +--- [LANE 1: GENERATION PHYSICALITY -- BOUNDED]
  |         |
  |         +--[AD] Z3 singlet states: (0,0,0) and (1,1,1)
  |              |
  |              +--- DM candidate identification (see DM lane)
  |
  +--[NCL] No-Continuum-Limit Theorem   *** SHARED NODE ***
  |    |   (5 independent arguments)
  |    |
  |    |   (i)   No tunable bare coupling => no LCP => no a->0
  |    |   (ii)  Forced continuum limit => 8 degenerate massless fermions
  |    |   (iii) No path-integral det => no fourth-root trick [= node G]
  |    |   (iv)  Hamiltonian formulation => all 8 tastes physical
  |    |   (v)   Lattice spacing a is the unique dimensionful parameter
  |    |
  |    |   FEEDS INTO:
  |    +--------> [W] taste splittings are physical (generations)
  |    +--------> [g1] g_bare = 1 (no running, see below)
  |    +--------> [PL] PL manifold argument (no continuum limit needed)
  |    +--------> [DM-prov] DM provenance (lattice IS the theory)
  |
  +--[ANOMALY] Anomaly cancellation chain   *** MAJOR JUNCTION ***
  |    |   Input: LH content (2,3)_{+1/3} + (2,1)_{-1} from [R]
  |    |
  |    +--[AN1] Tr[Y^3] != 0 => gauge anomaly
  |    |
  |    +--[AN2] Anomaly cancellation fixes RH content uniquely:
  |    |    u_R=(1,3)_{4/3}, d_R=(1,3)_{-2/3}, e_R=(1,1)_{-2}, nu_R=(1,1)_0
  |    |    (SM hypercharges exactly)
  |    |
  |    +--[AN3] Chirality => d_total even => d_t odd
  |    |    (Cl(d): omega central iff d odd; chirality needs omega anti-central)
  |    |
  |    +--[AN4] d_t = 1 uniquely (unitarity + causality + convergence)
  |    |
  |    +--- [LANE: TIME / 3+1 CLOSURE -- CLOSED]
  |    +--- [LANE: RH MATTER -- CLOSED (full-framework)]
  |
  +--[g1] g_bare = 1 from Cl(3) normalization
  |    |   {G_mu, G_nu} = 2 delta => holonomy normalization fixes g=1
  |    |   + single scale (a = l_Pl) + no continuum limit [NCL]
  |    |
  |    +--[g2] beta = 2*N_c = 6 for SU(3)
  |    +--[g3] alpha_plaq = 0.092 (V-scheme)
  |    |
  |    +--- feeds y_t prediction (Lane 4) via g_s input
  |    +--- feeds DM lane via alpha_s input
  |
  +--[PL] PL Manifold Argument (S^3 topology)
  |    |   Cubical ball on Z^3 IS a PL 3-manifold
  |    |   (vertex links = octahedra = PL S^2)
  |    |
  |    +--[PL1] Interior links = octahedron (Bruggesser-Mani)
  |    +--[PL2] Boundary chi = 2 => PL S^2
  |    +--[PL3] Cone-cap closure => closed PL 3-manifold
  |    +--[PL4] pi_1 = 0 (van Kampen)
  |    +--[PL5] Perelman + Moise => PL S^3
  |    |
  |    +--- [LANE 2: S^3 COMPACTIFICATION -- STRUCTURAL]
  |
  +--[DM] Dark Matter Relic Mapping
       |   Inputs from multiple nodes:
       |   - Z3 singlet states [AD] => DM candidate (mass = 6r/a)
       |   - alpha_plaq [g3] => sigma_v = pi * alpha^2 / m^2
       |   - taste spectrum => g_* = 106.75
       |   - graph growth (H > 0) => PHYSICAL INPUT
       |   - Boltzmann eq from lattice master eq (thermo limit)
       |   - Friedmann eq from Poisson coupling
       |
       +--[DM1] R = 5.48 (0.2% from observed 5.47)
       |
       +--- [LANE 3: DM RELIC -- BOUNDED]
```

### Ancillary lanes (BOUNDED, lower priority)

```
  [J] y_t = g_s/sqrt(6) + [g3] alpha_s
       |
       +--[CKM] CKM interpretation
            |   Z3 CP phase + mixing structure
            |   BLOCKER: Higgs Z3 charge is NOT L-independent
            |   (sharp analytic obstruction proved)
            |
            +--- [LANE 5: CKM -- BOUNDED]

  [g3] alpha_plaq = 0.092
       |
       +--[GC] Gauge couplings
            |   SU(2) normalization = bounded consistency
            |   U(1) = scan/fitted
            |
            +--- [LANE 6: GAUGE COUPLINGS -- BOUNDED]
```

---

## 2. Shared Nodes (Intermediate Results Used by Multiple Lanes)

These are the critical consolidation targets: intermediate results that
appear in two or more derivation lanes.

### 2A. No-Continuum-Limit Theorem [NCL]

**Used by:**
1. **Generation physicality** -- taste splittings are physical, not artifacts
2. **g_bare = 1** -- coupling cannot run (no LCP), must be algebraic
3. **DM provenance** -- lattice quantities are physical observables
4. **S^3 topology** -- PL manifold approach bypasses continuum limit entirely
5. **y_t non-renormalization** -- UV boundary condition is exact (no a->0 ambiguity)

**Current state:** Derived in GENERATION_GAP_CLOSURE_NOTE.md (5 arguments).
Also referenced in G_BARE_DERIVATION_NOTE.md, DM_RELIC_MAPPING_THEOREM_NOTE.md,
S3_PL_MANIFOLD_NOTE.md, and GENERATION_AXIOM_FIRST_NOTE.md. Each note
re-derives or re-states portions independently.

**Consolidation opportunity:** This should be a SINGLE standalone theorem
(Theorem 1 of the paper) with a clean proof, cited everywhere else.

### 2B. Cl(3) Gamma_5 Centrality [C]

**Used by:**
1. **y_t non-renormalization** -- vertex factorization D[G5] = G5*D[I]
2. **Slavnov-Taylor completion** -- ST identity as corollary
3. **Anomaly/time derivation** -- chirality operator properties in d=3 vs d=4
4. **Staggered mass term** -- Gamma_5 IS the mass operator in taste basis

**Current state:** Proved in RENORMALIZED_YT_WILDCARD_NOTE.md. Re-proved
in SLAVNOV_TAYLOR_COMPLETION_NOTE.md. Referenced in ANOMALY_FORCES_TIME_THEOREM.md.

**Consolidation opportunity:** Extract as a standalone lemma (Lemma: Cl(d)
center structure). The d=3-specific centrality and the d=4 anti-centrality
are both needed and should be stated once.

### 2C. KS Tensor Product Structure [A]

**Used by:**
1. **SU(3) commutant** -- the tensor factors define the multiplicity space
2. **Z3 orbit decomposition** -- orbits are Hamming-weight classes on {0,1}^3
3. **Graph shifts** -- S_i acts as sigma_x on factor i
4. **Gamma matrices** -- KS construction gives explicit Gamma_mu
5. **Matter assignment** -- gauge quantum numbers from tensor factor structure

**Current state:** Proved in SU3_FORMAL_THEOREM_NOTE.md Step 1. Re-stated
in SU3_CANONICAL_CLOSURE_NOTE.md Step 1. Used implicitly in
MATTER_ASSIGNMENT_THEOREM_NOTE.md and GENERATION_PHYSICALITY_THEOREM_NOTE.md.

**Consolidation opportunity:** Should be Theorem 0 or Lemma 0 -- the
canonical identification of taste space with (C^2)^{x3}.

### 2D. Anomaly Cancellation [ANOMALY]

**Used by:**
1. **3+1 derivation** -- forces temporal dimension
2. **RH matter completion** -- fixes hypercharges uniquely
3. **Generation matter assignment** -- forces opposite chirality for T1/T2
4. **Generation synthesis** -- removing doublers breaks anomaly cancellation

**Current state:** Full proof in ANOMALY_FORCES_TIME_THEOREM.md. Also used
in MATTER_ASSIGNMENT_THEOREM_NOTE.md (Attack 5). Referenced in
GENERATION_SYNTHESIS_NOTE.md.

**Consolidation opportunity:** The anomaly calculation is done at least twice
(once for the time theorem, once for matter assignment). A single canonical
anomaly-trace computation should be cited by both.

### 2E. Gauge Algebra su(2) + su(3) + u(1) with Hypercharge [Q + R]

**Used by:**
1. **Anomaly/time theorem** -- input LH content
2. **Matter assignment** -- T3, Y quantum numbers for orbits
3. **DM lane** -- Casimir factors, color channels
4. **y_t lane** -- N_c = 3 in trace identity
5. **g_bare lane** -- beta = 2*N_c

**Current state:** Derived in SU3_CANONICAL_CLOSURE_NOTE.md (full chain).
Also in SU3_FORMAL_THEOREM_NOTE.md (formal proof). Used downstream in
every other lane.

### 2F. Bipartite Structure / Ward Identity [D, E]

**Used by:**
1. **ST identity** -- {eps, Lambda_mu} = 0 derived from {eps, D_hop} = 0
2. **y_t non-renormalization** -- Ward identity constrains renormalization
3. **No-continuum-limit theorem** -- argument (iii) (no path-integral det)

**Current state:** Proved in frontier_renormalized_yt.py, re-verified in
frontier_slavnov_taylor_completion.py.

---

## 3. Missing Links (Same Result Derived Independently Without Cross-Reference)

### 3A. No-continuum-limit: generation lane vs g_bare lane

The GENERATION_GAP_CLOSURE_NOTE.md proves 5 arguments for no continuum limit.
The G_BARE_DERIVATION_NOTE.md uses "no continuum limit" as Assumption 3 but
cites the taste-physicality theorem only in passing, not the specific 5-argument
proof. These two notes should explicitly cross-reference. The g_bare derivation
DEPENDS on the generation-lane no-continuum-limit theorem -- this dependency
is currently implicit.

### 3B. Gamma_5 centrality: y_t wildcard vs ST completion vs anomaly theorem

Three notes independently use the fact that G5 commutes with all Cl(3) elements:
- RENORMALIZED_YT_WILDCARD_NOTE.md (proves it, uses for factorization)
- SLAVNOV_TAYLOR_COMPLETION_NOTE.md (re-proves it, uses for ST identity)
- ANOMALY_FORCES_TIME_THEOREM.md (uses the d-dependent commutation rule)

None explicitly cite each other for this shared mathematical fact.

### 3C. Anomaly traces: time theorem vs matter assignment

ANOMALY_FORCES_TIME_THEOREM.md computes Tr[Y], Tr[Y^3], Tr[SU(3)^2 Y],
Tr[SU(2)^2 Y] for the LH content. MATTER_ASSIGNMENT_THEOREM_NOTE.md
(Attack 5) computes the same traces for four chirality assignments. These
are the same calculation with different framing. Neither references the other.

### 3D. Wilson mass structure: generation theorem vs generation gap closure

GENERATION_PHYSICALITY_THEOREM_NOTE.md derives Wilson masses m_W = 2r|s|/a
as Level B conditional results. GENERATION_GAP_CLOSURE_NOTE.md uses the
same Wilson masses but frames them as consequences of the no-continuum-limit
theorem (promoted from conditional to theorem). The gap closure note
effectively supersedes the generation theorem note's Level B, but does not
say so explicitly.

### 3E. Graph shifts vs Gamma matrices

SU3_CANONICAL_CLOSURE_NOTE.md carefully distinguishes graph shifts S_i from
KS Gamma matrices (S_1 = Gamma_1, but S_2 != Gamma_2 due to staggered
phases). GENERATION_AXIOM_FIRST_NOTE.md discovers that Gamma matrices do NOT
commute with Z3, while the mass matrix does. These two observations are
related -- the staggered-phase mismatch between S_i and Gamma_i is exactly
why Z3 commutes with masses but not with hopping. This connection is not
made in either note.

---

## 4. Consolidation Opportunities

### 4A. SINGLE "No-Continuum-Limit" Theorem (HIGH PRIORITY)

**Replace:** Scattered arguments across GENERATION_GAP_CLOSURE_NOTE.md,
G_BARE_DERIVATION_NOTE.md, DM notes, and S3 notes.

**With:** One clean theorem proving: Cl(3) on Z^3 has no tunable bare
coupling, no Line of Constant Physics, no path-integral determinant, and
no fourth-root trick. The lattice spacing is a physical UV cutoff. The
forced continuum limit gives a trivial theory.

**Downstream references:** Every lane cites this single theorem.

### 4B. SINGLE "Cl(3) Center" Lemma (HIGH PRIORITY)

**Replace:** Independent proofs in the y_t wildcard note, ST completion note,
and anomaly theorem.

**With:** One lemma: In Cl(d), the volume element omega commutes with all
generators iff d is odd. In d=3: omega = iG1G2G3 is central, span{I, omega}
is the full center. In d=4: omega anticommutes with all generators.

**Downstream consequences:**
- Vertex factorization (y_t lane)
- ST identity (y_t lane)
- Chirality structure (anomaly/time lane)
- Non-renormalization of UV boundary condition

### 4C. UNIFIED Anomaly Computation (MEDIUM PRIORITY)

**Replace:** Separate anomaly trace calculations in the time theorem and the
matter assignment theorem.

**With:** One canonical computation of all anomaly traces for the gauge
content (2,3)_{+1/3} + (2,1)_{-1}, then cite it from:
- Time theorem (Step 1: LH content is anomalous)
- Matter assignment (Attack 5: opposite chirality forced)
- Generation synthesis (removing doublers breaks anomaly cancellation)

### 4D. UNIFIED Taste-Space Structure Theorem (MEDIUM PRIORITY)

**Replace:** Multiple notes that independently establish properties of the
KS tensor product structure, Z3 orbits, Hamming weight, and Wilson masses.

**With:** One theorem covering: (i) canonical tensor decomposition,
(ii) Z3 orbit structure 1+3+3+1, (iii) Wilson mass levels 0:2r:4r:6r,
(iv) Z3 is a mass-spectrum symmetry (not a full Hamiltonian symmetry),
(v) d=3 uniqueness of two size-3 orbits.

### 4E. g_bare + alpha_s Chain (LOW PRIORITY)

The path from Cl(3) normalization to g_bare = 1 to alpha_plaq = 0.092 is
currently spread across G_BARE_DERIVATION_NOTE.md and
DM_SIGMA_V_LATTICE_NOTE.md. A single short derivation would serve both
the y_t lane (which needs alpha_s for the RGE input) and the DM lane
(which needs alpha_s for sigma_v).

---

## 5. Minimal Axiom Count

The FULL derivation chain from Cl(3) on Z^3 to all results requires the
following independent assumptions:

### Tier 0: The Single Framework Axiom

**A0. Cl(3) algebra on Z^3 with Hamiltonian dynamics.**
Staggered fermions on the 3D cubic lattice with nearest-neighbor hopping.
This is the axiom. Everything else should follow or be honestly labeled.

### Tier 1: Physical Identifications (2 items)

**A1. a = l_Planck (single-scale identification).**
The lattice spacing is the Planck length. This converts lattice-unit
quantities to physical units. It is a physical identification, not a
mathematical derivation. Combined with the no-continuum-limit theorem,
this makes the lattice the fundamental structure.

**A2. The universe expands (H > 0).**
Required only for the DM relic lane. The graph framework does not predict
expansion; it only tells you what happens IF the graph grows. The sign of
H (expansion vs contraction) is selected by the 2nd law.

### Tier 2: Definitional Choices (2 items, arguably not axioms)

**D1. Cubical ball as the spatial region.**
The S^3 topology derivation uses the cubical ball (union of complete cubes)
rather than the Euclidean ball (set of lattice points within radius R).
This is the natural PL object on Z^3 and follows from the growth axiom
("space grows by local attachment of unit cells"). Arguably not a separate
assumption.

**D2. Quartic selector as the symmetry-breaking potential.**
The SU(3) derivation uses the first nontrivial even trace invariant of
graph shifts. Higher-order invariants have the same axis minima, so the
result is robust. Arguably not a separate assumption but a canonical choice.

### Tier 3: Bounded/Model Inputs (items that are used but not derived)

**M1. Wilson parameter r ~ O(1).**
Sets mass ratios within orbits. The ratios 1:2:3 are r-independent, but
absolute scale depends on r. Not derived from the axiom.

**M2. Anisotropy t_x != t_y != t_z.**
Required for intra-orbit (intra-generation) mass splitting. Origin not
derived. EWSB provides the primary Z3 breaking (1+2 split), but the
further Z2 breaking is a free parameter.

**M3. SM RGE running from M_Pl to M_Z.**
Used for the m_t prediction and gauge coupling matching. This is standard
physics, not a framework assumption, but it IS external input.

### Summary Count

| Tier | Count | Items |
|------|-------|-------|
| Framework axiom | 1 | Cl(3) on Z^3 |
| Physical identifications | 2 | a = l_Pl, H > 0 |
| Definitional choices | 2 | Cubical ball, quartic selector |
| Model inputs | 3 | Wilson r, anisotropy, SM RGE |

**Minimal for the closed lanes (time, gauge algebra, RH matter, y_t):** 1 axiom + 1 physical identification (a = l_Pl) = **2 independent inputs**.

**Minimal for the bounded lanes (generations, S^3, DM):** adds H > 0 and at least one model input = **3-4 independent inputs**.

---

## 6. Suggested Paper Structure

The cleanest presentation orders results by logical dependency, not by
historical discovery order. Each section should cite only previously
established results.

### Proposed Order

**Part I: The Framework (2 theorems, 1 lemma)**

1. **Axiom statement.** Cl(3) on Z^3, Hamiltonian dynamics, a = l_Pl.

2. **Theorem 1: No continuum limit.** [NCL] -- consolidation target 4A.
   Five arguments. The lattice IS the fundamental theory.

3. **Lemma: Cl(d) center structure.** [C] -- consolidation target 4B.
   omega central iff d odd. In d=3: center = span{I, G5}.

4. **Theorem 2: KS tensor decomposition and taste structure.**
   -- consolidation target 4D. V = (C^2)^{x3}, Z3 orbits 1+3+3+1,
   Wilson mass levels, graph shifts.

**Part II: Gauge Algebra and Matter (3 theorems)**

5. **Theorem 3: Gauge algebra derivation.**
   Graph shifts -> quartic selector -> su(2) -> SWAP -> su(3) + u(1).
   Hypercharge Y = +1/3, -1. Content: (2,3)_{+1/3} + (2,1)_{-1}.

6. **Theorem 4: Anomaly cancellation and 3+1 spacetime.**
   LH content anomalous -> RH content fixed -> chirality requires d_t odd
   -> d_t = 1. (Single consolidated anomaly computation, target 4C.)

7. **Theorem 5: Matter assignment.**
   Z3 orbits carry distinct quantum numbers. Anomaly forces opposite
   chirality. Bit-flip C gives charge conjugation.

**Part III: Quantitative Predictions (2 theorems + bounded results)**

8. **Theorem 6: g_bare = 1 and alpha_s.**
   Cl(3) normalization + no continuum limit + single scale.
   alpha_plaq = 0.092. (Consolidation target 4E.)

9. **Theorem 7: y_t = g_s/sqrt(6) non-renormalization.**
   Cl(3) centrality -> vertex factorization -> ST identity -> BC protection.
   SM RGE -> m_t = 174.2 GeV (+0.7%).

10. **Bounded: Generation physicality.**
    No-continuum-limit theorem promotes taste-physicality from axiom to
    theorem. Z3 superselection. EWSB 1+2 split. Mass hierarchy
    order-of-magnitude via EWSB cascade + strong-coupling RG.
    CP phase delta = 2pi/3. Honest obstructions documented.

11. **Bounded: S^3 spatial topology.**
    PL manifold argument. Interior links = octahedra. Boundary = PL S^2.
    Cone-cap closure. Van Kampen + Perelman + Moise.

12. **Bounded: DM relic ratio.**
    Graph-native freeze-out. All inputs native/derived except H > 0.
    R = 5.48 (0.2% from observed). Provenance table.

**Appendix: Obstructions and Open Problems**

- Generation physicality interpretive gap
- CKM sharp obstruction (Higgs Z3 charge)
- Gauge coupling matching (U(1) fitted)
- Quantitative mass hierarchy precision
- Anisotropy origin

### Why This Order

- Theorems 1-2 are prerequisites for everything else (shared nodes).
- The Cl(d) center lemma is needed for both the time theorem (Part II)
  and the y_t theorem (Part III), so it must come first.
- The gauge algebra (Theorem 3) must precede anomaly cancellation
  (Theorem 4), which must precede matter assignment (Theorem 5).
- g_bare (Theorem 6) must precede y_t (Theorem 7) because alpha_s is
  an input to the RGE prediction.
- Bounded results come after all closed theorems, ordered by strength
  of evidence (generations > S^3 > DM).

### Key Narrative Arc

The paper tells the story: **one algebraic structure (Cl(3) on Z^3) forces
the Standard Model gauge group, determines spacetime dimension, fixes the
top quark mass, and provides a dark matter candidate** -- all from the same
axiom plus one physical identification. The bounded results (generations,
topology, relic abundance) extend the reach with honest caveats.

---

## Summary of Findings

**Shared nodes identified:** 6 intermediate results serve 2-5 downstream lanes each. The no-continuum-limit theorem and Gamma_5 centrality are the two highest-leverage shared nodes.

**Missing links identified:** 5 places where parallel lanes derive or use the same result without cross-reference. The most significant is the no-continuum-limit theorem, which is proved in the generation lane but used (often implicitly) by 4 other lanes.

**Consolidation opportunities identified:** 5, of which 2 are high priority (no-continuum-limit theorem and Cl(d) center lemma), 2 are medium priority (anomaly computation and taste-space structure), and 1 is low priority (g_bare + alpha_s chain).

**Minimal axiom count:** 1 framework axiom + 2 physical identifications for the closed lanes; add 1 more physical input + model parameters for the bounded lanes.
