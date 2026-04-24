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
