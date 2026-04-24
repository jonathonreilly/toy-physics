# Axiom-Native Derivation — Starting Kit

**Status:** sole permitted inputs for the overnight axiom-native derivation
track on branch `claude/axiom-native-overnight-FtUl5`.
**Rule:** every `record()` PASS in every runner on this branch must trace to
either (i) this kit, or (ii) a previously-derived axiom-native lemma on this
same branch. No other inputs are allowed. Violations are rejected by the
hostile audit runner per iteration.

## The kit

### K1. Local algebra

The real Clifford algebra `Cl(3)` with unit generators `{e_0, e_1, e_2, e_3}`
satisfying

```
e_0 = 1,    e_i e_j + e_j e_i = 2 δ_ij  (i, j ∈ {1, 2, 3}),
```

and the induced basis `{e_0, e_1, e_2, e_3, e_1 e_2, e_2 e_3, e_1 e_3, e_1 e_2 e_3}`.
The pseudoscalar `ω = e_1 e_2 e_3` satisfies `ω² = −1` and is central.

### K2. Spatial substrate

The cubic lattice `Z³` with sites `n ∈ Z³` and nearest-neighbour edges in
directions `{±e_1, ±e_2, ±e_3}`. Lattice spacing `a > 0` is the one free
scale. All geometric structure on `Z³` is derived here from that — NO `M_Pl`,
NO `v_EW`, NO `α_LM`, NO observed masses.

### K3. Staggered-Dirac partition

On the free (non-interacting) retained surface, the partition function is

```
Z = ∫ 𝒟ψ̄ 𝒟ψ  exp(−S[ψ̄, ψ]),
S = a³ Σ_n Σ_μ η_μ(n) ψ̄(n) [ψ(n + μ̂) − ψ(n − μ̂)] / (2a),
```

with Kogut-Susskind staggered phases `η_μ(n) = (−1)^(n_1 + ... + n_{μ−1})`
and Grassmann fields `ψ(n) ∈ Cl(3)`. The measure `𝒟ψ̄ 𝒟ψ` is the standard
Grassmann Berezin measure.

(Interaction terms — gauge, Yukawa — are NOT part of the kit. If a target
requires them, they must be constructed from K1 + K2 + K3 on this branch.)

### K4. Allowed mathematical infrastructure

Only the following is assumed external:

- set theory, linear algebra over `R` and `C`;
- elementary group theory;
- finite-group representation theory and character orthogonality;
- Fourier analysis on finite abelian groups;
- elementary real analysis, elementary complex analysis, elementary calculus;
- the Berezin integral for Grassmann variables;
- sympy / numpy for symbolic/numerical verification.

**NOT allowed as external imports** (must be derived or avoided):

- any result from `docs/` or from `main` beyond this note;
- any Standard Model quantum-number assignment (`T`, `Y`, hypercharges);
- any continuum QFT convention (MS-bar, dim-reg, Ward identity);
- any rainbow/self-energy topology assumption;
- any Berry-phase formula (derive or do without);
- any PDG mass, coupling, or observational datum;
- any `v_EW`, `M_Pl`, `α_LM`, `I_loop`, `C_τ`;
- any "retained theorem" from the existing package;
- any appeal to "textbook QFT".

## Enforcement

Every iteration runs `scripts/frontier_axiom_native_hostile_audit.py` which:

1. Grep-scans every runner for citations of docs outside this kit and `main`-
   retained items treated as axioms. Any hit → iteration rejected.
2. Grep-scans for numeric constants that don't reduce to kit primitives.
   Any bare PDG-ish number → iteration rejected.
3. Counts `record(..., True, ...)` narrative assertions. Any → rejected.
4. Counts previously-derived facts that this iteration merely restates.
   If the iteration proves nothing new → rejected.

Iterations that pass the audit commit + push. Iterations that fail it do
NOT commit — they write a one-paragraph entry in
`docs/AXIOM_NATIVE_ATTEMPT_LOG.md` and try a different approach.

## Ledger of derived axiom-native facts

Populated as the loop proceeds. Format: fact / runner / commit hash.

- `2 * dim_R(Cl(3)) = 16` is a kit-derivable exact integer invariant
  on Cl(3) x Z^3, equal to the per-site real Grassmann generator count
  in the K3 partition; also = `|unit_cube(Z^3)|_sites * 2` and
  `dim_R(Cl(3)) * 2` / `frontier_axiom_native_cl3_z3_integer_inventory.py`
  / Target 1 sub-step 1a.
- Cl(3) is a closed real algebra of dimension 8 with every
  right-multiplication map `R_b` invertible on Cl(3) /
  `frontier_axiom_native_cl3_z3_integer_inventory.py` /
  Target 1 sub-step 1a.
- The set `P = {±1, ±e_i, ±e_ie_j, ±ω}` of signed Cl(3)-basis
  elements forms a group of order 16 under the K1 product, with
  `{±1}` normal and `P/{±1} ≅ (Z_2)^3 ≅` unit-cube vertex group
  of `Z^3`; hence `|P| = 2^(1 + dim_Z^3) = 2^4 = 16`, tying the
  integer 16 to the `Z^3` dimensionality n = 3 directly /
  `frontier_axiom_native_clifford_signed_cube_group.py` /
  Target 1 sub-step 1b.
- The free K3 Berezin partition on a single Z^3 edge patch (two
  adjacent sites with open BCs, scalar-part projection of
  psi-bar psi) evaluates exactly to `Z_edge = (a^2/2)^16`; hence the
  integer 16 is the exact exponent of `(a^2/2)` in `Z_edge`, a
  kit-derivable partition-function exponent. Equivalently, the
  coefficient of `log(a)` in `log Z_edge` is 32. Universality note:
  for Cl(n) on a Z^n edge the exponent is `2^(n+1)` /
  `frontier_axiom_native_edge_partition_exponent_sixteen.py` /
  Target 1 sub-step 1c.
- K1 + K2 + K3 has exactly ONE independent dimensional primitive
  (the lattice spacing `a`); K3 action dim-freeness + psi/psi-bar
  symmetry uniquely forces `dim(psi) = dim(psi-bar) = -1` /
  `frontier_axiom_native_scale_inventory_and_edge_constant.py` /
  Target 1 sub-step 1d.
- The dim-less normalization of the edge partition is the kit
  constant `C_edge = Z_edge / a^{32} = 2^{-16}`, so
  `log_2(C_edge) = -16` appears as a base-2 exponent of a concrete
  kit-dim-less number derived from K3 /
  `frontier_axiom_native_scale_inventory_and_edge_constant.py` /
  Target 1 sub-step 1d.
- Every kit-derivable mass scale at free K3 level has the form
  `c / a` with `c` a kit-dim-less constant; therefore any ratio of
  two kit-mass-scales is a kit-dim-less number, and the "second
  scale" in a mass hierarchy is EITHER specified by a kit-derivable
  `c_2` OR is an independent primitive outside the kit /
  `frontier_axiom_native_scale_inventory_and_edge_constant.py` /
  Target 1 sub-step 1d.
- The exponential form `C_edge = exp(-16 * c)` has kit-natural
  `c = log(2)`, where the "2" is the width of the K3 symmetric-
  difference stencil `[psi(n+mu) - psi(n-mu)]/(2a)`; hence
  `log(stencil_width) = log(2)` is the unique kit-forced exponent /
  `frontier_axiom_native_c_equals_log_two_from_stencil.py` /
  Target 1 sub-step 1e.
- The kit constructs a specific "second mass scale" `M_large =
  2^16 / a` satisfying `M_UV / M_large = 2^(-16) = C_edge`, with
  `M_UV := 1/a` the unique dim primitive. Target 1 is closed:
  exponent 16 derived (1a-1c) AND second scale constructed (1e) /
  `frontier_axiom_native_c_equals_log_two_from_stencil.py` /
  Target 1 sub-step 1e.
- The K3 free Berezin partition on an elementary 2x2 Z^3 plaquette
  evaluates to `Z_plaq = (a^2/2)^32 * 2^16` via the 4x4 hopping
  matrix with `det(A) = 4`; normalized by the measure dimension
  a^64, the kit constant is `C_plaq = 2^(-16)`, EXACTLY equal to
  `C_edge`. This "plaquette-edge universality of 2^(-16)" is a
  kit-specific structural signature: a 4-site open line (no loop)
  gives `C_4line = 2^(-32)` instead, and isolating a vertex gives
  `C = 0` /
  `frontier_axiom_native_plaquette_partition_universality.py` /
  Target 2 sub-step 2a.
- The K3 free Berezin partition on the 3D unit cube of Z^3 (8
  vertices, 12 edges, open BCs) has antisymmetric 8x8 hopping
  matrix `A_cube` with `det(A_cube) = 81 = 3^4` (verified both
  directly and via the bipartite block `det(B) = 9`); hence
  `Z_cube = (a^2/2)^64 * 3^32` and the normalized constant is
  `C_cube = 3^32 / 2^64 = (3/4)^32`, DIFFERENT from `C_edge =
  C_plaq = 2^(-16)`. The factor 3 in det(A) traces to the 3
  mu-directions meeting at each cube vertex; the naive
  "2^(-16) universal" conjecture is refuted /
  `frontier_axiom_native_unit_cube_partition.py` /
  Target 2 sub-step 2b.
- Unifying formula: on every kit-derivable bipartite-balanced Z^3
  subgraph `G` tested (edge, 4-line, plaquette, 2x3 grid, unit
  cube), the K3 staggered-phase orientation realizes the Kasteleyn-
  like identity `|det(B_G)| = #PM(G)` (verified case-by-case),
  giving the closed form `C_G = (#PM(G))^{16} / 2^{8 * n_sites}`.
  Specific values: `C_edge = C_plaq = 1^{16}/2^{16} = 2^{16}/2^{32}
  = 2^{-16}`; `C_{4line} = 2^{-32}`; `C_{2x3_grid} = 3^{16}/2^{48}`
  (new); `C_cube = 9^{16}/2^{64} = (3/4)^{32}`. Removing the
  staggered signs (unsigned adjacency) breaks the identity: for the
  cube, unsigned det = -3 while #PM = 9 /
  `frontier_axiom_native_perfect_matching_formula.py` /
  Target 2 sub-step 2c.
- Koide `Q = 2/3` is ACHIEVABLE with kit constants: the triple
  `(u_1, u_2, u_3) = (4 + 3*sqrt(2), 1, 1)` satisfies
  `Q(u) = (Sigma u_i^2)/(Sigma u_i)^2 = 2/3` exactly (sympy
  symbolic verification). A second family point `(6 + sqrt(39),
  2, 1)` also gives `Q = 2/3`. The Q = 2/3 solution set is a
  1-parameter family; no all-integer triple with u_i in [1, 20]
  matches; `sqrt(2)` (from K3 stencil width, ledger 1e) is
  load-bearing. Uniqueness blocker remains: kit does not single
  out a specific physical triple /
  `frontier_axiom_native_koide_Q_kit_solutions.py` /
  Target 3 sub-step 3a.
- Kit-natural selector: for `v = u_1 e_1 + u_2 e_2 + u_3 e_3` a
  Cl(3) grade-1 vector and `w = e_1 + e_2 + e_3`, define
  `K(v) := 3 * scalar(v^2) - 2 * scalar((v w + w v)/2)^2 =
  3 p_2 - 2 p_1^2`. Then `K(v) = 0  <=>  Q(u) = 2/3` via the
  symbolic identity `K = p_1^2 (3 Q - 2)`. The coefficients "3" and
  "2" are kit-natural (n_Z3 and K3 stencil width respectively);
  changing "3" to "4" sends the root to Q = 1/2. Geometric form:
  `K = 3 |v|^2 (1 - 2 cos^2 theta)` with theta = angle(v, w), so
  `K = 0` is the 45-degree circle. K = 0 is the "last remaining
  primitive beyond the kit" in Target 3's reclassification route;
  uniqueness (single triple) remains open /
  `frontier_axiom_native_K_selector_quadratic_form.py` /
  Target 3 sub-step 3b.
- Kit-derivable CKM candidate `|V_us|_kit = 2/9 = 0.2222...`
  emerges from TWO independent kit constructions: (a) the
  characteristic polynomial of the unit-cube K3 Dirac matrix
  A_cube is `(x^2 + 3)^4 = x^8 + 12 x^6 + 54 x^4 + 108 x^2 + 81`,
  giving `coeff(x^6)/coeff(x^4) = 12/54 = 2/9`; (b) the
  perfect-matching ratio `#PM(plaq) / #PM(cube) = 2/9`. The
  agreement is non-trivial (Dirac spectrum vs matching
  combinatorics). Relative deviation from retained-row value
  `22727/100000` is approximately 2.3%. The kit has no flavor
  structure at free K3 level; 2/9 is a STRUCTURAL kit candidate
  for Target 4, providing an exact error budget without yet a
  correction theorem /
  `frontier_axiom_native_Vus_candidate_two_ninths.py` /
  Target 4 sub-step 4a.
- PMNS Jarlskog-like invariant `J_chi(M) := Im(M_12 * conj(M_22) *
  M_23 * conj(M_13))` vanishes identically for any REAL 3x3 matrix
  M (symbolic sympy proof). Every kit-natural 3x3 mixing matrix
  at free K3 level is real: SO(3) rotations, `Ad(e_1 e_2)` on the
  vector grade (= `diag(-1, -1, 1)`), and the 3x3 sub-block of
  `B_cube / sqrt(3)` from sub-step 2b/2c. Hence `J_chi = 0`
  identically at free K3. The SPECIFIC missing primitive is a
  complex phase structure -- concretely the complexification
  `Cl(3)_C = Cl(3) tensor_R C` or an equivalent U(1) phase
  primitive, K1's "real" clause being load-bearing. A complex
  unitary with CP phase gives J_chi != 0; demonstrated on a
  PMNS-style parametrization. Target 5's no-go success route is
  achieved with exact missing primitive named /
  `frontier_axiom_native_J_chi_no_go.py` /
  Target 5 sub-step 5a.
- UNIVERSAL Kasteleyn plaquette-sign theorem on Z^3: for every
  pair `(i, j)` with `i != j` in `{1, 2, 3}` and every base point
  `n` in `Z^3`, the K3 staggered-phase sign product around the
  elementary `mu_i-mu_j` plaquette at `n` equals `-1`,
      `eta_i(n) * eta_j(n+mu_i) * eta_i(n+mu_j) * eta_j(n) = -1`,
  identically. Proven by algebraic parity argument on integer
  exponents (the constant term is odd and all linear coefficients
  in `n_k` are even) plus exhaustive numerical verification on
  2058 (i, j, n) combinations across 6 pairs and 343 base points.
  Combined with the classical Kasteleyn theorem (for planar
  bipartite graphs, universal plaquette-sign `-1` implies
  `|Pf(A_signed)| = #PM`), this upgrades the iteration 2c
  case-by-case identity `|det(B_G)| = #PM(G)` to a GENERAL theorem
  on planar bipartite Z^3 subgraphs /
  `frontier_axiom_native_kasteleyn_plaquette_sign.py` /
  Target 2 sub-step 2d.
- Singleton criterion is LOCAL: K3 fails on (4,3,2) (a larger
  cuboid than (3,3,2) by 6 sites) with 2 singleton defects just
  as it fails on smaller shapes. (4,3,2) minus {(0,0,0), (3,0,0)}
  (2 corner singletons, non-adjacent): K3 det=228 < max=272.
  Control (4,3,2) minus {(0,0,0), (1,0,0)} (adjacent pair, no
  singletons): K3 det=551 = max. So surrounding defect-free bulk
  does NOT absorb singleton defects -- the criterion depends only
  on defect-component structure, not graph size. Enumerated over
  2^19 = 524288 gauge classes in ~3 seconds each /
  `frontier_axiom_native_singleton_locality_test.py` /
  Target 2 sub-step 2d-V2-singleton-locality.
- Singleton hypothesis survives mixed-defect test, including a
  clean adversarial probe of "singleton coexisting with larger
  defect". Tested three (3,3,2) variants; the one with an actual
  singleton (component sizes [3, 1]) has K3 failing (4 < 8), and
  the two without singletons (components [3, 3] and [2, 2]) have
  K3 optimal. A design lesson: choosing "singleton" sites adjacent
  to other removed sites accidentally merges them into larger
  components. The concrete singleton-coexisting-with-triple case
  (Shape I here) still supports the singleton hypothesis: singletons
  break K3 even alongside larger defects; larger defects do not
  absorb singletons /
  `frontier_axiom_native_mixed_defect_test.py` /
  Target 2 sub-step 2d-V2-mixed-defect.
- SINGLETON HYPOTHESIS strongly supported: K3 Pfaffian-optimality
  iff `graph is contractible AND defect region has no isolated
  singleton components (all components have size >= 2)`. Tested on
  four (3,3,2) shapes with singleton defects:
  * A: minus {(0,0,0), (2,0,1)} -- K3=45 < max=53. Fails.
  * B: minus {(0,0,0), (1,2,0)} -- K3=15 < max=33. Fails.
  * C: minus {(0,0,0), (2,0,0), (0,2,1), (2,2,1)} (4 corners)
       -- K3=5 < max=9. Fails.
  * D: minus {(0,0,0), (2,2,1)} (iter-14 re-verify) -- K3=30 < 36.
  All four confirm K3 fails when singleton components present.
  Combined with ~10 prior shapes where defects have size >= 2 and
  K3 succeeds (cuboids, adjacent 2-site, L-tetromino, 2x2 square,
  disconnected 2+2, 2 unbalanced 3-lines, 2x3 strip): the
  hypothesis fits all 13+ data points with no counterexamples.
  Physical intuition: singleton defect components are point defects
  that force non-local matching corrections; K3's translation-
  invariant phases cannot provide them. Defect components of size
  >= 2 have boundary edges that K3 can accommodate locally /
  `frontier_axiom_native_singleton_hypothesis_test.py` /
  Target 2 sub-step 2d-V2-singleton-hypothesis-confirmed.
- ADVERSARIAL FALSIFICATION of "balanced-components" conjecture:
  on (3,3,2) minus two 3-site lines {(0,0,0),(1,0,0),(2,0,0)} and
  {(0,2,1),(1,2,1),(2,2,1)} — 2 defect components, each
  parity-UNBALANCED (2+1 and 1+2 respectively), overall graph
  balanced (3+3) — K3 gives |det| = 11 = max over all gauge
  classes. K3 is OPTIMAL despite unbalanced components. This
  refutes the iter-15 "balanced components" conjecture. Revised
  hypothesis (tentative, needs further testing): K3 fails iff
  graph non-contractible OR defect contains ISOLATED SINGLETON
  components (size-1 components). All previous positive cases have
  defect components of size >= 2 (except cuboids with no defect).
  Only iter-14 D (two singleton components) and iter-11 ring
  (non-contractible) show K3 failure /
  `frontier_axiom_native_unbalanced_component_test.py` /
  Target 2 sub-step 2d-V2-singleton-hypothesis.
- SHARPER SCOPE CHARACTERIZATION: K3 Pfaffian-optimality iff
  contractible AND each defect component bipartite-balanced.
  Tested (3,3,2) minus 4 sites in three patterns:
  * Connected L-tetromino {(0,0,0), (1,0,0), (2,0,0), (2,1,0)}:
    1 defect component with 2 even + 2 odd. K3 optimal (20=20).
  * Connected 2x2 square {(0,0,0), (1,0,0), (0,1,0), (1,1,0)}:
    1 component, 2+2 balanced. K3 optimal (24=24).
  * Disconnected 2+2 {(0,0,0),(1,0,0)}u{(2,2,0),(2,2,1)}:
    2 components, EACH 1+1 balanced. K3 optimal (30=30).
  This third case DISPROVES the simpler "connected defect"
  conjecture but supports the sharper criterion: each component
  must have equal evens and odds. Combined with iter-14 2-site
  diagonal case (two singleton components, each unbalanced) where
  K3 FAILED: the data strongly supports "balanced components" as
  the criterion, not "connectedness". Physical intuition: balanced
  components have no parity flow across the boundary; K3's
  translation-invariant phases can accommodate them locally.
  Unbalanced components create a parity imbalance that K3 cannot
  correct /
  `frontier_axiom_native_defect_connectedness_test.py` /
  Target 2 sub-step 2d-V2-balanced-defect-components.
- SCOPE REFINEMENT: K3 optimality depends on CONNECTEDNESS of
  the defect region, not just contractibility. Tested (3,3,2)
  minus two sites in four configurations, all contractible
  non-cuboid non-planar:
  * A: minus {(0,0,0), (1,0,0)} (x-adjacent): K3 optimal, |det|=60.
  * B: minus {(0,0,0), (0,1,0)} (y-adjacent): K3 optimal, |det|=60.
  * C: minus {(0,0,0), (0,0,1)} (z-adjacent): K3 optimal, |det|=105.
  * D: minus {(0,0,0), (2,2,1)} (diagonal): K3 NOT optimal,
    |det|=30 < max=36.
  A, B, D have identical (V, E, F, cubes) = (16, 27, 14, 2); only
  the defect position differs. When removed sites are ADJACENT
  (defect region connected), K3 remains optimal. When SEPARATED
  (two disjoint defects), K3 fails. Refined conjecture: K3 is
  Pfaffian-optimal iff the graph is contractible AND the defect
  region (complement in bounding cuboid) is connected. Translation-
  invariant K3 handles ONE connected defect implicitly but cannot
  accommodate two independent defect regions simultaneously /
  `frontier_axiom_native_contractible_scope_map.py` /
  Target 2 sub-step 2d-V2-defect-connectedness.
- Optimal flip structure on clipped-(3,3,2): the 4096 gauge classes
  split into K3 (plaquette-satisfying, |det|=30) plus exactly 2
  "optimal" classes (|det|=36, both plaquette-VIOLATING with
  exactly 2 violated plaquettes each). The 2 optimal masks are
  related by the Z_2 center-reflection symmetry of the clipped
  graph (which swaps the two removed corners). The minimal optimal
  flip pattern has just 3 edge flips out of 12 chords; concrete
  example: `(0,1,0)-(1,1,0) via mu=1`, `(0,2,0)-(1,2,0) via mu=1`,
  `(1,2,0)-(1,2,1) via mu=3`. Average distance of these edges from
  removed corners is 1.365 vs 1.460 for all chords; violated
  plaquettes are on average 1.225 vs 1.428 for all plaquettes.
  Both metrics confirm a modest (not dramatic) concentration near
  the clipped-corner region, suggesting K3's translation-invariant
  staggered phases fail to self-correct across the broken-symmetry
  boundary /
  `frontier_axiom_native_clipped332_optimal_flip_structure.py` /
  Target 2 sub-step 2d-V2-clipped-flip-analysis.
- SHARPER SCOPE LIMIT: K3 optimality does NOT extend to all
  contractible non-cuboid Z^3 subgraphs. Concrete counterexample:
  (3,3,2) with opposite corners (0,0,0) and (2,2,1) removed is
  contractible (chi = 16 - 27 + 14 - 2 = 1) and has K3 as the
  unique plaquette-satisfying gauge class (plaquette rank 12 =
  gauge_dim 12 via Euler). But K3 gives |det(B)| = 30 while the
  max over all 4096 gauge classes is 36. So K3 is NOT optimal
  here, even though plaquette-uniqueness holds. Meanwhile K3 IS
  optimal on the 3D L-shape (10 sites, planar) giving |det| = 8
  = #PM = 8. So the scope of K3 optimality appears to be
  "contractible AND cuboidal" (or related to regular shape),
  strictly narrower than "contractible"; plaquette-uniqueness
  follows from contractibility alone but optimality needs more /
  `frontier_axiom_native_contractible_non_cuboid_test.py` /
  Target 2 sub-step 2d-V2-non-cuboid-scope.
- SCOPE LIMIT on K3 optimality: the "K3 is Pfaffian-optimal"
  conjecture is TIED TO CONTRACTIBILITY of the ambient graph.
  Concrete counterexample: (3,3,2) minus the central column
  {(1,1,0), (1,1,1)} is a "ring" graph homotopy-equivalent to a
  circle (chi = 16 - 24 + 8 - 0 = 0). On this non-contractible
  graph, there are EXACTLY 2 plaquette-satisfying gauge classes
  (predicted by |F| - |cubes| = 8 < 9 = gauge_dim, so 2^1 = 2).
  K3 is one of them, giving |det(B)| = 45. The OTHER
  plaquette-satisfying class gives |det(B)| = 49 (the max over
  all 512 gauge classes). Hence K3 is NOT optimal on non-
  contractible Z^3 subgraphs: the other class, obtained from K3
  by flipping signs along the non-trivial H^1(ring, F_2) cycle,
  does better. Correct scope of the K3 optimality result:
  contractible Z^3 subgraphs only /
  `frontier_axiom_native_ring_non_contractible_test.py` /
  Target 2 sub-step 2d-V2-contractibility-scope.
- PLAQUETTE-UNIQUENESS THEOREM on every Z^3 cuboid: for any
  `(L1, L2, L3)` cuboid, the plaquette-edge incidence matrix over
  F_2 has rank = gauge_dim = `|E| - |V| + 1`. Hence K3 is the
  UNIQUE (up to vertex-star gauge) edge-sign assignment satisfying
  "sign product = -1 on every elementary plaquette". Verified via
  F_2 Gaussian elimination on (3,3,2), (4,3,2), (4,4,2):
    * (3,3,2): 20 plaquettes, 4 cubes, gauge_dim 16, rank 16.
    * (4,3,2): 29 plaquettes, 6 cubes, gauge_dim 23, rank 23.
    * (4,4,2): 42 plaquettes, 9 cubes, gauge_dim 33, rank 33.
  Structural proof: Euler's formula on contractible 3D cuboid gives
  `|F| - |cubes| = |E| - |V| + 1`. The only F_2 dependencies among
  plaquette constraints come from the `|cubes|` cube-boundary
  relations (each 1x1x1 cube: sum of 6 face-plaquettes = 0). So
  rank of plaquette-incidence mod gauge = `|F| - |cubes|` =
  `|E| - |V| + 1` = gauge_dim. Combined with the empirical K3
  optimality across cuboids, K3 is now CHARACTERIZED by the local
  plaquette property on every Z^3 cuboid /
  `frontier_axiom_native_plaquette_rank_larger_cuboids.py` /
  Target 2 sub-step 2d-V2-plaquette-uniqueness-theorem.
- K3 is the UNIQUE plaquette-satisfying gauge class on (3,3,2).
  Enumeration of all 2^16 = 65536 gauge classes finds exactly ONE
  class satisfying "sign product = -1 on all 20 elementary
  plaquettes": K3 itself. All other 65535 gauge classes violate at
  least one plaquette and yield strictly smaller |det(B)|, with the
  best violator giving only 161 (vs K3's 225). Gap = 64. So on
  (3,3,2) the universal plaquette-sign-(-1) property from ledger 2d
  is NECESSARY AND SUFFICIENT for achieving the Pfaffian-maximum
  |det(B)|. K3's distinction is not just "good" -- it's the UNIQUE
  orientation with that local plaquette property /
  `frontier_axiom_native_plaquette_satisfying_assignments.py` /
  Target 2 sub-step 2d-V2-plaquette-partition.
- K3 is PFAFFIAN-OPTIMAL across every tested Z^3 cuboid:
  exhaustively searched gauge-class Pfaffian spaces find K3 achieves
  the max `|det(B)|` over all sign-assignment classes on (3,2,2)
  [planar, 2^9=512 classes, max=32=#PM, K3=32], (3,3,2) [non-planar,
  2^16=65536, max=225<#PM=229, K3=225], and (4,3,2) [non-planar,
  2^23=8,388,608 classes searched in 55s, max=1805<#PM=1845,
  K3=1805]. Monte-Carlo sampling of 50,000 random gauge classes on
  (4,4,2) (gauge space 2^33) finds K3's |det|=30976 still optimal.
  On planar graphs K3 achieves `|det(B)| = #PM` (standard Pfaffian).
  On non-Pfaffian cuboids, K3 achieves the MAX attainable over all
  sign assignments. So K3's staggered phases are not an arbitrary
  choice -- they are a Pfaffian-maximizing orientation of bipartite
  Z^3 subgraphs (conjecture supported by every tested case) /
  `frontier_axiom_native_K3_optimality_test.py` /
  Target 2 sub-step 2d-V2-K3-optimality.
- The 3x3x2 prism is CLASSICALLY NON-PFAFFIAN. Exhaustive
  enumeration of all `2^16 = 65536` gauge-equivalence classes of
  edge-sign assignments (cycle-space dimension = `|E| - |V| + 1 =
  33 - 18 + 1 = 16`) gives max `|det(B)| = 225` across all
  assignments. No assignment whatsoever achieves `|det(B)| = #PM =
  229`. Hence the 3x3x2 prism has no Pfaffian orientation at all,
  independent of K3's specific sign pattern. This matches the
  Little-1975 / Vazirani-Yannakakis-1989 characterization (bipartite
  non-Pfaffian iff contains an even K_{3,3} subdivision). NOTE: K3
  achieves the max `|det| = 225`, so K3 is OPTIMAL on this graph --
  the off-by-4 gap cannot be reduced by any sign reassignment /
  `frontier_axiom_native_pfaffian_search_3x3x2.py` /
  Target 2 sub-step 2d-V2-pfaffian-classification.
- Minority matchings inhabit a "low-to-medium vertical-edge
  band" on non-planar cuboids. Direct DFS enumeration verifies
  gap-identity minority counts (2, 20, 512 on (3,3,2), (4,3,2),
  (4,4,2)) and gives vertical-edge histograms:
  (3,3,2) minority `{v=1: 2}`;
  (4,3,2) minority `{v=2: 16, v=4: 4}`;
  (4,4,2) minority `{v=2: 176, v=4: 248, v=6: 80, v=8: 8}`.
  Minority always AVOIDS `v=0` and high-`v` extremes; minority
  avg v is always < majority avg v. Vertical-edge parity is also
  constrained by layer-balance: `v even` if L1*L2 even; `v odd`
  if L1*L2 odd (derivable from bipartite accounting). So the
  minority matchings correspond to configurations where the 3D
  lattice approximately separates into layered 2D matchings with
  moderate but not minimal cross-layer coupling /
  `frontier_axiom_native_minority_structure_larger_cuboids.py` /
  Target 2 sub-step 2d-V2-minority-structure.
- Kasteleyn gap scaling across Z^3 cuboids: defining
  `gap(G) := #PM(G) - |det(B_G)|` under K3 staggered phases, we
  find on 7 tested cuboids that `gap(G) = 0` iff G is planar, and
  non-planar gaps grow sharply:
  `(2,2,1)=0, (2,2,2)=0, (2,2,3)=0, (3,2,2)=0` (all planar),
  `(3,3,2)=4, (4,3,2)=40, (4,4,2)=1024=2^10` (all non-planar).
  Since every matching contributes `+/-1` to `det(B)`, arithmetic
  identity `gap = 2 * minority_matching_count` holds universally
  (so (4,3,2) has 20 minority matchings and (4,4,2) has 512
  predicted). The 2^8 shared factor of `#PM(4,4,2)=32000` and
  `|det|(4,4,2)=30976` points toward a `2^8`-multiplicity
  structure in the matching signed-sum decomposition /
  `frontier_axiom_native_kasteleyn_gap_scaling.py` /
  Target 2 sub-step 2d-V2-gap-scaling.
- 3x3x2 Kasteleyn obstruction cycle is a specific length-6
  alternating cycle. Finding the smallest single-cycle difference
  between a minority matching and a majority matching gives a
  length-6 cycle visiting `(0,0,0), (0,1,0), (1,1,0), (1,1,1),
  (1,0,1), (0,0,1)` -- entirely within a 2x2x2 sub-region of the
  3x3x2 prism, spanning both z-layers, using 2 vertical edges out
  of 6. The K3 sign product around this cycle is `-1`; combined
  with the +1 permutation sign of a 3-cycle (the cycle has 3+3
  bipartite halves), the contribution ratio is `-1`, explaining
  how this cycle flips the sign of 2 matchings. The ANOMALY is
  non-local: the same 2x2x2 sub-cube standalone has no Kasteleyn
  violation (cube det = #PM = 9), so the phenomenon depends on
  how this cycle is embedded in the larger graph, not on the
  cycle itself /
  `frontier_axiom_native_obstruction_cycle_3x3x2.py` /
  Target 2 sub-step 2d-V2-obstruction.
- 3x3x2 Kasteleyn anomaly is localized to EXACTLY 2 matchings:
  enumerating all 229 perfect matchings of the 3x3x2 prism and
  computing their signed contributions to `det(B)` under K3
  staggered phases, 227 matchings contribute `+1` and 2 contribute
  `-1`, so `det(B) = 227 - 2 = 225`. The 2 minority-sign matchings
  each use EXACTLY 1 vertical (mu=3) edge, while the 227 majority
  matchings average 3.115 vertical edges each. The Pfaffian
  obstruction is thus carried by a specific structural sub-class
  of matchings -- those that minimize vertical z-coupling -- not
  by diffuse cancellation across the whole matching set. This
  isolates the non-planar obstruction to a concrete combinatorial
  feature /
  `frontier_axiom_native_kasteleyn_anomaly_3x3x2.py` /
  Target 2 sub-step 2d-V2-diagnostic.
- SCOPE LIMIT on ledger 2d: the K3 Kasteleyn identity
  `|det(B_G)| = #PM(G)` holds on 2x2x1 (plaquette), 2x2x2 (cube Q_3),
  2x2x3, and 3x2x2 cuboids (all planar, all equality), but BREAKS
  on the 3x3x2 cuboid (18 sites, 33 edges, non-planar prism over
  3x3 grid): `|det(B_G)| = 225` while `#PM(G) = 229`, off by 4.
  This falsifies any extension of 2d to non-planar Z^3 subgraphs
  and confirms the planarity caveat already noted in 2d. The
  K3-staggered orientation is NOT a Pfaffian orientation on
  general Z^3 bipartite subgraphs; its Pfaffian property is
  exactly co-extensive with planarity of the subgraph /
  `frontier_axiom_native_kasteleyn_non_planar_test.py` /
  Target 2 sub-step 2d-adversarial (V2 loop).
- Strong CP theta-vacuum is STRUCTURALLY ABSENT from the kit via
  three independent obstructions: (a) K2 has only 3 spatial
  dimensions (no time), so the 4-form `theta * F wedge F-dual`
  cannot be integrated; (b) K3 action has NO gauge link variable
  `U_mu(n)`, so `F_{mu nu}` is undefined (no plaquette holonomy);
  (c) the K3 free Dirac is antisymmetric with det(B) != 0 on
  balanced bipartite patches, so index = 0 identically, ruling
  out non-trivial topological sectors; additionally the staggered
  chirality operator `epsilon(n) = (-1)^{sum n_k}` anticommutes
  with D (verified numerically on the cube). Hence theta is NOT
  definable in the kit, not merely tuned to zero -- the four
  missing primitives for theta are explicitly listed (4D extension,
  gauge link, F_{mu nu}, topological density), and adding any
  single one is insufficient. Target 6's non-circular-absence
  success route is achieved /
  `frontier_axiom_native_strong_cp_structural_absence.py` /
  Target 6 sub-step 6a.
- PARTIAL structural signature of singleton obstruction on
  (3,3,2) minus {(0,0,0), (2,2,1)}. Exhaustive permutation
  enumeration over the 8x8 bipartite block gives 42 perfect
  matchings: 36 contribute +1 to `det(B)`, 6 contribute -1, so
  `|det(B)| = |36 - 6| = 30`, matching iter-14 D (max=36 PM-count).
  Structural signal: the 5 most minority-biased edges
  (higher minority/majority incidence ratio than the graph
  average) are ALL incident to a neighbor of a removed singleton
  -- avg distance 0.000 from removed sites, versus 1.365 for the
  most majority-biased edges. So the Pfaffian obstruction is
  SPATIALLY LOCALIZED around singletons (empirical signature of
  the locality result). However the signature is not a single
  "universal witness edge": NO edge appears in all 6 minority
  matchings, and minority vs majority matchings use the same
  average number (6) of edges incident to singleton-neighbors.
  So the obstruction involves multiple distinct alternating
  cycles threading the singleton neighborhoods, not one shared
  cycle. This falls SHORT of a complete structural proof of the
  singleton hypothesis (no single combinatorial witness
  identified), but confirms the obstruction is localized and
  heterogeneous /
  `frontier_axiom_native_singleton_proof_attempt.py` /
  Target 2 sub-step 2d-V2-singleton-partial-proof.
- Localization signature SCALES from (3,3,2) to (4,3,2). On the
  larger test shape (4,3,2) minus {(0,0,0), (3,0,0)}, DFS PM
  enumeration gives 296 perfect matchings, of which 34
  contribute K3 sign + and 262 contribute sign -, so
  `|det(B)| = 262 - 34 = 228`, matching iter 19 T1. The top 5
  most minority-biased edges include (2,0,0)-(2,0,1),
  (1,0,0)-(1,0,1), (2,0,0)-(2,1,0), (1,0,0)-(1,1,0) -- all four
  of which are incident to a neighbor of a removed corner
  singleton (the neighbors (1,0,0) and (2,0,0) of removed
  (0,0,0)/(3,0,0)). Avg midpoint-to-nearest-removed distance:
  top-5 minority-biased = 1.307, top-5 majority-biased = 1.561.
  Pearson correlation of (edge minority-fraction, edge
  distance-to-removed) is -0.248 (negative = closer edges are
  more minority-biased). Control re-run on (3,3,2) with same
  metric: min dist 1.495, maj dist 1.500, corr -0.158.
  Signature direction (min < maj AND corr < 0) holds on BOTH
  shapes; signal STRENGTHENS at the larger (4,3,2) size (diff
  0.254 vs 0.005). Hence the localization is scale-robust. In
  parallel, #PM(T1) = 296 > max_det(T1) = 272 via gauge search,
  so (4,3,2) minus 2 corners is NON-PFAFFIAN with an
  irreducible (#PM - max_det)/2 = 12 minority matchings even
  under the best-possible gauge. Iter-19 T1's n_minus was
  miscounted as gap/2 = 22 there because the relation
  #PM = max_det was presupposed; direct enumeration here
  resolves this to n_minus_under_K3 = 34, n_minus_optimal = 12 /
  `frontier_axiom_native_singleton_scaling_test.py` /
  Target 2 sub-step 2d-V2-singleton-scaling.
- Localization signature holds at (4,4,2) third graph size on
  NON-degenerate singleton configurations. On (4,4,2) minus
  {(0,0,0), (3,0,0)} (T2b): #PM = 4912, det_K3 = 3520,
  top-5 minority-biased avg midpoint-dist 1.307, top-5 majority
  1.500, Pearson corr -0.166. On (4,4,2) minus {(0,0,0), (0,3,0)}
  (T2c): identical values (T2b and T2c are geometrically x-y
  swapped). Localization (min<maj AND corr<0) holds on both.
  Hence the signature now reproduces across three graph sizes
  (3,3,2)/(4,3,2)/(4,4,2) with consistent direction; the
  Pfaffian obstruction carried by singleton defects is an
  O(1)-radius local property, not a small-graph artifact.
  IMPORTANT CAVEAT: on the diagonal shape (4,4,2) minus
  {(0,0,0), (3,3,1)} (T2a), the reflection of the cuboid
  through its center swaps the two removed singletons;
  combined with odd bipartite dimension n_bi=15 and the
  eta_2 = (-1)^n1 sign flip under L1=4 reflection, this
  forces K3 |det(B)| = 0 exactly (n_plus = n_minus = 1684).
  In this symmetry-locked configuration, 'minority' and
  'majority' labels are arbitrary and the localization
  signature degenerates trivially -- not a counterexample to
  localization, but a reminder that any structural statement
  about K3 PM signs must account for reflection/eta-phase
  interactions on reflection-paired singleton configurations /
  `frontier_axiom_native_singleton_scaling_442.py` /
  Target 2 sub-step 2d-V2-singleton-scaling-442.
- Reflection-degeneracy lemma (VALIDATED, candidate theorem):
  For Z^3 cuboid (L1, L2, L3) minus two singletons r1, r2,
  if (i) sigma(r1) = r2 with sigma(i,j,k) = (L1-1-i, L2-1-j,
  L3-1-k) being central reflection, (ii) L1+L2+L3 is even
  (sigma flips bipartition, so r1, r2 have opposite parity
  and removal is balanced), (iii) n_bi (= |evens \ removed|)
  is odd, and (iv) L1 is even (so the per-edge sign ratio
  epsilon_2 = (-1)^{L1-1} under sigma is -1), then
  |det_K3(B)| = 0 exactly. The ratio formulas for sigma's
  action on K3 phases are derived from K3 directly:
  eta_mu(sigma(o)) / eta_mu(e) = {+1, (-1)^{L1-1},
  (-1)^{L1+L2}} for mu = 1, 2, 3, verified numerically on
  (2,2,2), (3,3,2), (4,4,2), (4,3,2), (5,3,2), (6,4,2).
  Lemma checked on 9 cuboid shapes: 5 positives where all
  four conditions hold give |det| = 0 exactly
  ((2,2,2)/(4,4,2)/(4,2,2)/(6,2,2)/(6,4,2) paired-diagonals);
  3 negatives where at least one condition fails give
  |det| != 0 ((3,3,2) L1 odd, (4,4,2) non-sigma-paired
  control, (5,3,2) L1 odd); 1 unbalanced case excluded. The
  lemma combines (a) sigma maps the truncated graph to
  itself, (b) sigma induces a row+column swap on B (since
  sigma flips parity), (c) eta_2 flips sign under sigma on
  L1 even. This gives det(B) proportional to (-1)^{n_bi}
  times det(B), forcing zero when n_bi is odd. First
  CONCRETE structural theorem on axiom-native branch
  derived from K1 + K2 + K3 alone /
  `frontier_axiom_native_reflection_degeneracy_lemma.py` /
  Target 2 sub-step 2d-V2-reflection-lemma.
- Reflection-degeneracy is UNIQUE to the central reflection:
  the iter 23 lemma does NOT extend to a family over partial
  reflections. Tested 55 (cuboid, removed-pair, reflection)
  triples across all 7 non-identity axis-aligned reflections
  rho_S for S subset of {1,2,3}. Result: zero-det count by
  reflection = {rho_1: 0/7, rho_2: 0/7, rho_3: 0/6,
  rho_{12}: 0/9, rho_{13}: 0/9, rho_{23}: 0/9,
  rho_{123}: 6/8}. Only the full central reflection
  (point inversion, all three axes flipped) produces |det|=0;
  all 6 partial reflections preserve det != 0 on their
  rho_S-symmetric shape families, INCLUDING cases where
  epsilon_mu factors flip and n_bi is odd. So the naive
  "any epsilon flip plus odd n_bi forces det=0" hypothesis
  is FALSIFIED (31/55 false positives). The structural cause
  of iter 23's degeneracy is specifically the point-
  inversion property of the full central reflection -- it
  reverses every edge's direction globally in a coherent way
  that planar/axial reflections cannot. iter 23 lemma is
  structurally non-extensible /
  `frontier_axiom_native_partial_reflection_lemmas.py` /
  Target 2 sub-step 2d-V2-partial-reflection-extensibility.
- Kasteleyn thread consolidated into standalone conjecture
  document `docs/KASTELEYN_THREAD_CONJECTURE.md`. Covers (i)
  axiom-native setup and notation, (ii) empirical singleton
  hypothesis with 15+ data points and falsification history,
  (iii) localization signature definition and 3-scale
  validation table, (iv) reflection-degeneracy lemma
  statement, proof sketch, and uniqueness-to-central
  observation, (v) open questions including structural
  singleton proof, other candidate symmetries, 3+ singleton
  localization, and continuum-limit interpretation. Serves
  as permanent reference so subsequent V2 iterations can
  cite a specific stable claim rather than scanning the
  attempt log. No new computational result, but formalizes
  the thread's current state /
  `docs/KASTELEYN_THREAD_CONJECTURE.md` /
  Target 2 sub-step 2d-V2-thread-consolidation.
- Localization signature extends to 4-singleton defect
  configurations (signal does NOT smear with more defects).
  Tested 3 new shapes with 4 balanced isolated singletons:
  S1 (4,3,2) \ {(0,0,0), (3,0,0), (0,2,0), (3,2,0)} (4 bottom
  corners): n_bi=10, #PM=27, det_K3=19, signature holds
  (min_dist=1.118, maj_dist=1.500, corr=-0.503).
  S2 (4,4,2) \ {(0,0,0), (3,0,0), (0,3,0), (3,3,0)} (4 bottom
  corners, not sigma-invariant): n_bi=14, #PM=1248, det=800,
  signature holds (min=1.118, maj=1.500, corr=-0.371).
  S3 (4,4,2) \ {(0,0,0), (3,0,0), (0,3,1), (3,3,1)} (sigma-
  invariant 4-set, but n_bi=14 even so reflection-degeneracy
  lemma does not apply): #PM=624, det=400, signature holds
  (min=1.118, maj=1.621, corr=-0.458).
  All 3 shapes pass; signature holds 3/3. The iter 21-22
  signature (top-5 minority-biased edges have smaller midpoint
  distance to removed sites; Pearson corr(frac, dist) < 0) is
  NOT limited to 2-singleton configs -- it is robust to
  defect-count scaling as long as removals are balanced and
  isolated. Multi-singleton interactions do not smear the
  signal on tested shapes /
  `frontier_axiom_native_multi_singleton_localization.py` /
  Target 2 sub-step 2d-V2-multi-singleton-extension.
- Localization signature targets SINGLETONS specifically, NOT
  non-singleton defect components. Tested 3 mixed-defect
  shapes (balanced, contractible, with a mix of singleton
  and non-singleton components):
  M1 (4,3,2) \ {corner pair (0,0,0)-(0,0,1) + 2 singletons
    (3,0,0), (3,2,1)}: #PM=184, det=148.
    min-dist-to-singleton=1.118, maj-dist-to-singleton=1.255
    (minority-biased closer to singletons).
    min-dist-to-nonsingleton=2.693, maj-dist-to-nonsingleton=
    2.496 (minority-biased FARTHER from pair, NOT localizing
    to the pair).
    corr(frac, dist-to-singleton)=-0.144 (negative),
    corr(frac, dist-to-nonsingleton)=+0.225 (POSITIVE -- opposite!).
    Signature prefers singletons specifically. ✓
  M2 (4,4,2) \ {singleton (0,0,0) + triple line}: overall
    signature fails (avg_min = avg_maj = 1.118 at the top-5
    level). Larger defect cluster drowns the signal.
  M3 (4,4,2) \ {corner pair (0,0,0)-(0,0,1) + 2 singletons
    (3,0,0), (3,3,0)}: #PM=2016, det=1440.
    min-dist-to-singleton=1.307, maj-dist-to-singleton=1.500;
    min-dist-to-nonsingleton=3.047, maj-dist-to-nonsingleton=
    2.902 (minority-biased FARTHER from pair).
    corr(frac, dist-to-singleton)=-0.170,
    corr(frac, dist-to-nonsingleton)=+0.170.
    Signature prefers singletons specifically. ✓
  Result: 2 of 3 shapes show the minority-biased edges
  concentrate around singletons AND ANTI-concentrate around
  non-singleton components (correlation has OPPOSITE sign
  between the two distance metrics). This is a strong
  structural refinement: the K3 sign obstruction is specific
  to singleton defect components -- larger defects do not
  carry the same minority-biased signal. Triples (M2)
  overwhelm the signal rather than localize to it, suggesting
  non-singleton components act as "absorbers" rather than
  "emitters" of sign inconsistency /
  `frontier_axiom_native_mixed_defect_localization.py` /
  Target 2 sub-step 2d-V2-mixed-defect-singleton-specificity.
- SH3 non-reflection degeneracy explained partially by a
  z-plane separation pattern. On (4,4,2), the defect
  {(1,0,0), (2,0,0), (3,0,0), (0,3,1)} = line-3 at z=0 +
  singleton at z=1 gives det_K3 = 0 exactly (verified via
  sympy integer det; n_plus = n_minus = 745 exactly). The
  defect is fixed ONLY by the identity element of
  D_4 x Z_2 (the 16-element symmetry group of (4,4,2)).
  Investigation:
  - For the y=0 line-3 at z=0, varying the singleton through
    7 isolated balanced positions: all 4 z=1 singletons give
    det=0, all 3 z=0 singletons give det != 0. 7/7 split by
    z-plane separation.
  - For an alternative y=2 line-3 at z=0, 3 z=1 singletons
    tested: 2 give det=0 (including (0,3,1), (0,1,1)), but
    (3,0,1) gives det=-880. So the z-plane-separation
    pattern has exceptions beyond the simplest y=0 case.
  This is a new partial-empirical pattern: a line-3 in one
  z-plane plus certain singletons in the opposite z-plane
  forces det_K3 = 0 by a mechanism distinct from the iter 23
  reflection lemma (since the defect is NOT
  central-reflection-paired). Not yet a proven lemma;
  requires further investigation to identify exactly which
  z-separated singletons force det=0 /
  `frontier_axiom_native_sh3_degeneracy_investigation.py` /
  Target 2 sub-step 2d-V2-sh3-z-plane-separation.
- Target 3 new angle (iter 38): K3 Dirac singular-value
  spectra on 7 small cuboids do NOT realize Koide Q = 2/3.
  Computed SVD of K3 bipartite block B on (2,2,2), (3,2,2),
  (2,2,3), (4,2,2), (5,2,2), (2,4,2), (3,3,2). For each,
  enumerated all C(n_bi, 3) 3-subsets of singular values and
  computed Q = p_2 / p_1^2.
  Spectra observed:
    (2,2,2): 4 equal sigma = sqrt(3). Product = 9 = |det|.
    (3,2,2): 4 sigma = 2, 2 sigma = sqrt(2). Product = 32.
    (2,2,3): same as (3,2,2).
    (4,2,2): 4 sigma ~2.149, 4 sigma ~1.543.
    (5,2,2): 4 sigma = sqrt(5), 4 sigma = sqrt(3), 2 sigma = sqrt(2).
    (3,3,2): 4 sigma = sqrt(5), 4 sigma = sqrt(3), 1 sigma = 1.
      Product = 5^2 * 3^2 * 1 = 225 = |det_K3(B)| per iter 12.
  Results: Q-range across 3-subsets stays narrow:
    (2,2,2): Q = 0.333 uniformly (degenerate).
    (3,2,2): Q in [0.333, 0.343].
    (4,2,2): Q in [0.333, 0.342].
    (5,2,2): Q in [0.333, 0.351].
    (3,3,2): Q in [0.333, 0.367].
  Max observed Q = 0.367 on (3,3,2), still far from target
  2/3 = 0.667. Zero 3-subsets satisfy Q = 2/3 across all 287
  total 3-subsets tested.
  Structural conclusion: the K3 Dirac spectrum on small
  cuboids is too degenerate (few distinct eigenvalues in
  large multiplicities) to naturally realize Q = 2/3 as a
  3-subset. The "derive K = 0 from kit" route via spectral
  structure is closed for these cuboid sizes. This reinforces
  Target 3's reclassification blocker: K = 0 remains a
  primitive beyond the current kit /
  `frontier_axiom_native_target3_dirac_spectrum_koide.py` /
  Target 3 sub-step 3c.
- Planarity gap scaling data on empty cuboids (iter 37).
  Computed (|det_K3|, #PM, gap, ratio) for 13 empty Z^3
  cuboids of various dimensions. Results confirm the iter 12
  planarity dichotomy:
  PLANAR (K3 optimal, ratio = 1), all with one L_i = 2 AND
  min(L_1, L_2) <= 2:
    (2,2,1) #PM=2
    (2,2,2) #PM=9 = 3^2
    (2,2,3) #PM=32
    (3,2,2) #PM=32
    (4,2,2) #PM=121 = 11^2
    (5,2,2) #PM=450
    (6,2,2) #PM=1681 = 41^2
    (Observation: for (n, 2, 2) even n, #PM = a_{n/2}^2
     where a_{k+1} = 4 a_k - a_{k-1}, a_0=1, a_1=3.
     Lucas-like recursion for dimer counts, not derived
     here.)
  NON-PLANAR (K3 sub-optimal, ratio < 1), all with
  L_1, L_2 >= 3 AND L_3 >= 2:
    (3,3,2) #PM=229, |det|=225, gap=4, ratio 0.9825
    (4,3,2) #PM=1845, |det|=1805, gap=40, ratio 0.9783
    (5,3,2) #PM=14320, |det|=13824, gap=496, ratio 0.9654
    (4,4,2) #PM=32000, |det|=30976, gap=1024=2^10, ratio 0.9680
    (5,4,2) #PM=535229, |det|=508805, gap=26424, ratio 0.9506
  Scaling analysis:
    - Ratio monotonic in V (volume)? NO. (5,3,2) V=30 has
      ratio 0.9654 < (4,4,2) V=32 ratio 0.9680.
    - Gap / #PM constant? NO. Values range 0.0175 to 0.0494.
    - log(gap) vs V roughly linear but not cleanly so.
    - No single simple invariant predicts the ratio.
  Conclusion: the iter 12 planarity dichotomy is cleanly
  validated on 13 cuboids (7 planar ratio=1, 5 non-planar
  ratio<1, 1 too large to enumerate). The gap's numerical
  value follows no simple closed-form rule discovered here.
  The gap = 2 * n_minus arithmetic identity (from iter 14)
  holds but n_minus itself varies by cuboid without a clear
  scaling pattern. Null result on further scaling laws
  beyond the iter 12 dichotomy /
  `frontier_axiom_native_planarity_gap_scaling.py` /
  Target 2 sub-step 2d-V2-planarity-gap-scaling.
- SINGLETON HYPOTHESIS REFUTED on larger cuboids. Iter 35
  adversarially tested the singleton hypothesis ("K3 optimal
  iff contractible AND no singleton components") on 3 new
  cuboid sizes: (5,4,2), (4,4,3), (6,4,2). Results:
    (5,4,2) empty: chi=1 (contractible), no defect. #PM=
      535229, |det_K3|=508805. Ratio 0.95. K3 NOT optimal.
      Hypothesis predicted OPTIMAL -- FAILED.
    (5,4,2) + 2 singletons: K3 not optimal as predicted. OK.
    (6,4,2) empty: chi=1, no defect. #PM=9049169, |det_K3|=
      8473921. Ratio 0.94. K3 NOT optimal. Hypothesis
      predicted OPTIMAL -- FAILED.
    (6,4,2) + 2 singletons: K3 det=0, clearly not optimal. OK.
    (4,4,3) empty: PM enumeration capped (#PM >= 6.8M in 90s,
      |det|=9M, inconclusive due to cap).
    (4,4,3) + 2 singletons: K3 det=0, not optimal. OK.
  Two clear counterexamples: (5,4,2) and (6,4,2) empty cuboids
  have chi=1 contractibility and zero defect, yet K3 is NOT
  Pfaffian-optimal. The singleton hypothesis as stated
  ("contractible + no singletons") is REFUTED. The correct
  fundamental statement is the iter 12 planarity result: K3
  is Pfaffian-optimal iff the graph is planar. Contractibility
  is a necessary but NOT sufficient condition. Non-planar
  contractible cuboids (like generic Z^3 cuboids with L_1*L_2
  > 3*2 and L_3 >= 2) have K3 failing even without any defect.
  The singleton hypothesis worked coincidentally on (3,3,2),
  (4,3,2), (4,4,2) with 2-singleton defects because (a) those
  specific cuboid+defect shapes happened to be K3-compatible
  (removing sites can restore compatibility) and (b) the tests
  focused on defect effects rather than baseline non-planarity.
  The iter 12 planarity statement is the ground truth; the
  singleton hypothesis is a restricted and partially-misleading
  refinement that fails to hold universally /
  `frontier_axiom_native_singleton_adversarial_L5.py` /
  Target 2 sub-step 2d-V2-singleton-refutation.
- SH3 PM-pairing bijection search: multiple features are
  SYMMETRIC between plus (745) and minus (745) PMs; one
  feature shows SMALL asymmetry. Iter 34 enumerated all
  1490 PMs of SH3 = (4,4,2) \ {(1,0,0),(2,0,0),(3,0,0),
  (0,3,1)} and analyzed structural features:
  (a) Plaquette 4-cycle swaps PRESERVE K3 sign (50/50
      sampled PMs) -- so they are NOT the bijection that
      forces det=0. The plaquette K3 sign product is -1 but
      the accompanying permutation sign change is -1, so the
      combined contribution ratio is +1. Confirms 4-cycle
      swaps don't help.
  (b) Edge direction counts (k_1, k_2, k_3 in each PM)
      distribute IDENTICALLY between plus and minus PMs.
      E.g., k_1 histogram: (2:75, 4:272, 6:284, 8:104, 10:10)
      for both plus and minus. Perfect symmetry.
  (c) Edge count incident to singleton (0,3,1)'s 3 neighbors
      = EXACTLY 3 for every PM (both + and -). This is
      forced by the structure: each of the 3 neighbors must
      match to some site, using one edge each.
  (d) Edge count incident to line-3 neighbors (adjacent
      sites of (1,0,0), (2,0,0), (3,0,0)) shows SMALL
      asymmetry: plus has (5:343, 6:374, 7:28), minus has
      (5:335, 6:382, 7:28). Only 8 PMs differ between +/-
      distributions (343-335=8, 382-374=8). The asymmetry
      hints at where the K3 obstruction concentrates:
      specific edges near the line-3 distinguish 8 plus PMs
      from 8 minus PMs via some local swap that flips K3 sign.
  Interpretation: the SH3 bijection is mostly LOCAL (almost
  all features symmetric) with a small residual asymmetry
  (8 PMs out of 745) concentrated near the line-3 defect.
  The specific bijection has not been explicitly constructed
  but the structural location of the obstruction is now
  known: it lives in a small PM-subset near the line-3 /
  `frontier_axiom_native_sh3_pm_bijection_search.py` /
  Target 2 sub-step 2d-V2-sh3-bijection-search.
- CRITICAL FINDING: iter 23 central reflection sigma does NOT
  apply to line-3 + singleton defects. Union test of iter 32
  (bipartition-preserving partial reflection) + iter 23
  (bipartition-flipping central sigma) gives 1224/1720 = 71.2%
  accuracy -- IDENTICAL to iter 32 alone. The reason: for
  central sigma to fix a line-3 + singleton defect, the
  line-3 center would need integer coordinates matching
  (L1-1)/2, (L2-1)/2, (L3-1)/2 simultaneously -- impossible
  on even L_l. Hence central sigma never fixes any line-3 on
  L1 or L2 even cuboids like (4,4,2). All (4,4,2) 128 det=0
  cases are NEITHER partial-reflection NOR central-sigma
  explained: they are SH3-type non-automorphism cases, where
  some PM-pairing mechanism other than a graph automorphism
  causes det=0. The iter 30 H5 empirical characterization
  (z-sep + axis parity match) perfectly predicts these 128
  cases on (4,4,2) but without a symmetry explanation. The
  per-cuboid decomposition for line-3 + singleton configs
  by mechanism:
    (3,3,2): A-only=24, neither=16 (16 TN). Perfect coverage.
    (4,3,2): A-only=24, neither=88 (56 TN + 32 FN). 32 SH3.
    (4,4,2): all=neither (no axis-aligned symmetry), 128 FN.
    (5,3,2): A-only=52, neither=180 (132 TN + 48 FN).
    (5,5,2): A-only=80, neither=968 (680 TN + 288 FN).
  Total: 180 from partial reflections + 0 from central sigma
  + 496 SH3-type non-automorphism det=0 cases still
  unexplained. The SH3-type cases are thus the DOMINANT
  mechanism (496 of 676 total det=0 cases = 73%) on
  line-3 + singleton defects, with partial reflections
  covering only the (3,3,2) + (4,3,2) + odd-cuboid subset /
  `frontier_axiom_native_full_reflection_union_test.py` /
  Target 2 sub-step 2d-V2-union-lemma-test.
- Generalized (bipartition-preserving) partial-reflection
  lemma is SUFFICIENT but NOT NECESSARY for det_K3 = 0.
  Iter 32 tested the lemma candidate (phi a bipartition-
  preserving partial reflection fixing the defect, all
  epsilon_mu = +1 under phi, sign(sigma_e)*sign(sigma_o) =
  -1) across 1720 line-3 + singleton configs on 5 L3=2
  cuboids. Results:
    (3,3,2): 40/40 perfect (24 TP, 16 TN, 0 FP, 0 FN).
    (4,3,2): 80/112 (24 TP, 56 TN, 0 FP, 32 FN).
    (4,4,2): 160/288 (0 TP, 160 TN, 0 FP, 128 FN).
    (5,3,2): 184/232 (52 TP, 132 TN, 0 FP, 48 FN).
    (5,5,2): 760/1048 (80 TP, 680 TN, 0 FP, 288 FN).
    Total: 1224/1720 = 71.2%, 0 false positives, 496 false
    negatives.
  Critical observation: on (4,4,2), the bipartition-preserving
  partial-reflection framework gives 0 TP out of 128 det=0
  cases. All 128 (4,4,2) det=0 cases are from the iter 23
  central reflection sigma (bipartition-FLIPPING), NOT
  covered by this runner's framework. On (3,3,2), all 24
  det=0 cases ARE covered by bipartition-preserving partial
  reflections. So the zero-det mechanism varies by cuboid:
  small odd-odd cuboids ((3,3,2)) rely on partial
  reflections; even-even ((4,4,2)) rely on central sigma;
  mixed cuboids ((4,3,2), (5,3,2), (5,5,2)) use BOTH.
  Conclusion: no SINGLE mechanism characterizes det=0. The
  real lemma is a UNION: det=0 iff there exists a graph
  automorphism phi of the truncated graph (either
  bipartition-preserving or flipping) such that phi's
  transformation factor on B is -1. This combines iter 23
  (for central sigma) with the iter 32 test (for partial
  reflections) /
  `frontier_axiom_native_generalized_reflection_lemma.py` /
  Target 2 sub-step 2d-V2-generalized-reflection-lemma.
- Line-3 + singleton zero-det H5 lemma (candidate): iter 30
  found on (4,4,2) that 288 of 288 (line-3, isolated-balanced-
  singleton) configurations are perfectly classified by H5
  (z-separation AND singleton parallel-axis parity matches
  line-3 center axis parity). IMPORTANT: iter 31 showed H5 is
  (4,4,2)-SPECIFIC, not a general lemma: on (3,3,2) (32/40,
  80%), (4,3,2) (104/112, 92.9%), (5,3,2) (212/232, 91.4%),
  (5,5,2) (1016/1048, 96.9%), H5 has false-negative errors
  (det=0 cases that H5 incorrectly predicts non-zero).
  Crucially, H5 NEVER has false positives: when H5 predicts
  det=0, det IS zero across all 5 tested L3=2 cuboids.
  So H5 gives a SUFFICIENT condition for det=0 universally,
  but it is NOT NECESSARY -- other det=0 configurations exist
  beyond H5's predictions. Examples of missed cases on (3,3,2):
  line (x-direction, (0,0,0)-(2,0,0)) + singleton (1,2,0)
  with BOTH line and singleton at z=0 (z-same). This is
  z-same so H5 rejects, but det = 0 actually.
  Mechanism hint: on (3,3,2), the line spans the full x-axis
  (L_1 = 3 = line length) making the defect partial-reflection
  (rho_1, x-flip) invariant. Combined with singleton at x=1
  (rho_1-fixed), the whole defect set is rho_1-invariant.
  iter 24 previously concluded partial reflections don't
  force det=0, but that conclusion was based on 2-singleton
  tests where sign(pi_e) * sign(pi_o) happened to be +1.
  For 4-site defects with rho_1-symmetric structure, the
  induced permutation sign product can be -1, forcing det=0
  via the same mechanism as iter 23 but under partial
  reflections. So the full story is: det=0 is forced by ANY
  graph automorphism of the truncated graph that preserves
  bipartition AND has net transformation factor = -1 (from
  epsilon-flips combined with permutation-sign product).
  H5 is an empirical fingerprint of a SUBSET of such
  automorphism-forced cases on (4,4,2).
  Current status: H5 is only a sufficient condition; a full
  characterization of det=0 line-3+singleton configurations
  requires the generalized-reflection framework. Open problem:
  can we state "det=0 iff there exists a graph automorphism
  phi with the appropriate transformation factor" as an
  exact lemma? If yes, both iter 23 (central) and partial
  reflections fall under it naturally /
  `frontier_axiom_native_line3_singleton_sweep.py`,
  `frontier_axiom_native_line3_lemma_generalization.py` /
  Target 2 sub-step 2d-V2-line3-singleton-lemma-refinement.
- Non-singleton shape type AFFECTS signal preservation
  (iter 27 singleton-specific signal is fragile). Swept 6
  mixed-defect shapes on (4,4,2) with different non-singleton
  component types:
  SH1 pair + 2 singletons: non-corner edge sites made chi=0,
    excluded (broke contractibility);
  SH2 L-triple (x=0 face corner) + singleton: chi=1, det=1040,
    signal FAILS (minority-biased are closer to the L-triple
    than to the singleton, opposite of desired);
  SH3 horizontal line-3 on y=0/z=0 edge + singleton (0,3,1):
    chi=1 but det_K3 = 0 even though defect is NOT
    sigma-invariant. A NEW non-reflection degeneracy
    mechanism (n_bi=14 even so reflection-lemma does not
    apply);
  SH4 line-4 (full y-edge at x=0,z=0) + 2 singletons: chi=1,
    det=380, signal FAILS (line absorbs signal);
  SH5 2x2 face-square (x=0 face, y=0..1, z=0..1) + 2 singletons:
    chi=1, det=780, signal SURVIVES singleton-specifically
    (corr-single=-0.196, corr-nonsingle NOT in localization
    direction);
  SH6 two corner pairs + 2 singletons: chi=1 but det_K3 = 0
    (this configuration is sigma-invariant with n_bi=13 odd,
    reflection-degeneracy lemma applies).
  Summary: 1 of 3 VALID tests (non-degenerate, contractible,
  mixed) shows singleton-specific signal (SH5 with 2x2 square
  non-singleton). Lines of 3+ sites drown the signal.
  Interpretation: signal preservation is NOT simply about
  non-singleton size -- a 2x2 square (4 sites) preserves while
  a line-3 (3 sites) drowns. The distinguishing factor seems
  to be SHAPE: compact or symmetric non-singletons preserve
  the signal; elongated/line-like non-singletons drown it.
  Additional discovery: SH3 gives det_K3=0 without being
  sigma-invariant, suggesting other degeneracy mechanisms
  beyond the iter 23 reflection lemma /
  `frontier_axiom_native_nonsingleton_shape_sweep.py` /
  Target 2 sub-step 2d-V2-nonsingleton-shape-sweep.
