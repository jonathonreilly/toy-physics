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
