# SU(3) Tensor-Network Engine Roadmap (5-PR Plan)

**Date:** 2026-05-03
**Claim type:** meta
**Status:** roadmap document, unaudited
**Eventual target:** explicit `rho_(p,q)(6)` for the unmarked spatial Wilson
environment on the L_s=2 APBC spatial cube, to support future review of
the open native bridge gate
([`GAUGE_SCALAR_BRIDGE_3PLUS1_NATIVE_TUBE_STAGING_GATE_2026-05-03.md`](GAUGE_SCALAR_BRIDGE_3PLUS1_NATIVE_TUBE_STAGING_GATE_2026-05-03.md)).

## 0. Why this engine

The framework's source-sector factorization

```text
T_src(6) = exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)
```

reduces the gauge-scalar temporal observable bridge to one missing
non-perturbative datum: the boundary character measure `rho_(p,q)(6)`
of the unmarked 3D spatial Wilson environment with marked-plaquette
boundary holonomy held fixed
([`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md)).

On the V-invariant minimal block (L_s = 2 APBC spatial cube) this is
a finite, explicit lattice-gauge problem — but evaluating it requires
contracting an SU(3) tensor network for the one-marked-plus-five-unmarked
spatial plaquette geometry recorded in the native staging gate, with all
the SU(3) Wigner intertwiner algebra it entails. The framework's existing
scripts implement only:

- single-link Haar integrals (1-plaquette block computations)
- the 6-neighbor Pieri recurrence for the source operator `J`
- character-truncated tensor-transfer support packets (no actual
  contraction at `beta = 6`)

The general Wigner intertwiner engine — Clebsch-Gordan coefficients,
multi-link Haar integrals, generic tensor-network contraction on
lattice graphs — has never been built in this framework.

This roadmap lays out a **5-PR plan** to build it deliberately, with
each PR self-contained, well-tested, and reviewable. The engine is
intended as a permanent piece of framework infrastructure, useful far
beyond the immediate cube Perron solve.

## 1. Plan at a glance

| PR | Deliverable | Self-contained? | Validation |
|---|---|---|---|
| 1 | Fusion multiplicities `N^ν_(λ,μ)` via Cartan-torus character orthogonality | yes | 9 standard SU(3) fusion identities |
| 2 | Wigner intertwiners / Clebsch-Gordan coefficients via Gel'fand-Tsetlin basis | depends on PR 1 | orthogonality, completeness, group identities |
| 3 | Haar integral primitives (1-link and multi-link) | depends on PRs 1, 2 | analytic formulas in known cases |
| 4 | Generic tensor-network contraction engine | depends on PRs 1-3 | small-graph reference computations |
| 5 | L_s=2 APBC cube geometry + `rho_(p,q)(6)` + P(6) bridge-gate check | depends on PRs 1-4 | NMAX convergence, comparison to existing reference solves |

Each PR should produce its own source note, runner, and audit-pipeline row.

## 2. PR 1 — Fusion engine (this commit)

**Status:** bounded support theorem delivered in this commit
([`SU3_FUSION_ENGINE_PR1_THEOREM_NOTE_2026-05-03.md`](SU3_FUSION_ENGINE_PR1_THEOREM_NOTE_2026-05-03.md);
runner `scripts/frontier_su3_fusion_engine.py`).

**Deliverable:** for all triples in the default dominant-weight box
`{0 <= p,q <= 4}`, compute the fusion multiplicities
`N^nu_(lambda, mu)` returned by the finite Cartan-grid engine.

**Algorithm:** numerical character orthogonality on the SU(3) Cartan
torus with Weyl-Vandermonde measure. Schur character formula for SU(3)
irreps; integer-rounding with residual diagnostic.

**Validation:** 9 identity checks (V1: 3⊗3̄, V2: 3⊗3, V3: 8⊗8, V4: 6⊗6̄,
V5: commutativity, V6: singlet selection, V7: dimension count, V8:
crossing, V9: fundamental Pieri). All PASS at NMAX=4, n_grid=80;
machine-precision integer-rounding residual `5.2e-15`.

**API:** importable functions `dim_su3`, `conjugate_irrep`,
`dominant_weights_box`, `cartan_grid`, `vandermonde_squared`,
`haar_measure_normalized`, `schur_character`, `character_table`,
`fusion_multiplicity`, `fusion_table`, `fusion_decomposition`.

**Scope explicitly excluded from PR 1:** Wigner intertwiner
coefficients (operators `C^nu_(lambda, mu): V_lambda ⊗ V_mu -> V_nu`);
Haar integrals; tensor-network contractions; lattice-gauge claims.

## 3. PR 2 — Wigner intertwiner / Clebsch-Gordan engine (planned)

**Goal:** for each fusion channel `lambda ⊗ mu = ⊕_nu N^nu_(lambda, mu)
nu`, compute the explicit intertwiner operators

```text
C^(nu, alpha)_(lambda, mu): V_lambda ⊗ V_mu -> V_nu,
    alpha = 1, 2, ..., N^nu_(lambda, mu)
```

with `alpha` indexing the multiplicity. The Wigner-Eckart theorem
guarantees these operators exist and are unique up to a unitary in the
multiplicity space.

**Algorithm options:**

1. **Gel'fand-Tsetlin basis.** Standard explicit basis for SU(N) irreps
   indexed by GT patterns. Clebsch-Gordan coefficients computed via
   Wigner-Racah algebra and explicit recursion. Most general but most
   complex.
2. **Direct diagonalization of Casimirs.** Construct the tensor product
   space `V_lambda ⊗ V_mu` and diagonalize the SU(3) Casimir operators
   to extract the irreducible subspaces. Simpler to implement; gives
   the intertwiners as eigenvector projectors.
3. **Recursive build via Pieri.** Build up `C^nu_(lambda, mu)` by
   iterating the fundamental Pieri rule and tracking explicit
   intertwiner data at each step.

**Validation:**
- Unitarity: `C^(nu, alpha)_(lambda, mu)` is an isometry from `V_nu` to
  `V_lambda ⊗ V_mu`.
- Orthogonality between multiplicity copies: `<C^(nu, alpha), C^(nu, beta)> = delta_(alpha, beta)`.
- Completeness: `sum_(nu, alpha) C^(nu, alpha) C^(nu, alpha)† = I` on
  `V_lambda ⊗ V_mu`.
- Reproduce standard CG coefficients for `3 ⊗ 3̄` and `3 ⊗ 3`
  (compare to published tables).
- Group identity: `C` intertwines the SU(3) action on both sides.

**API exposed for PRs 3-5:**
- `intertwiner(lam, mu, nu, alpha)` returns the explicit isometry.
- `intertwiner_basis(lam, mu)` returns all intertwiners for a fusion
  channel.
- `apply_intertwiner(C, vec_lam, vec_mu)` returns the `nu`-irrep
  component of `vec_lam ⊗ vec_mu`.

**Estimated complexity:** ~500-800 lines of code plus extensive
validation.

## 4. PR 3 — Haar integral primitives (planned)

**Goal:** compute single-link and multi-link Haar integrals of products
of SU(3) representation matrices, expressed as contractions of Wigner
intertwiners (PR 2 output).

**Single-link identity (well-known):**

```text
integral dU [D^lambda(U)]_ij [D^mu(U^†)]_kl
    = (1/d_lambda) delta_(lambda, mu) delta_il delta_jk
```

This is built into the engine as a primitive.

**Multi-link identities:** for products like

```text
integral dU [D^lambda(U V_1)]_ij [D^mu(U V_2)]_kl ... [D^xi(U V_n)]_mn
```

express in terms of intertwiners and the `V_alpha` matrices. The result
is a sum over tensor invariants weighted by intertwiner contractions.

**Algorithm:**
1. Use the formula `int dU prod_a D^(rep_a)(U) = projector onto invariant subspace`
2. Decompose the n-fold tensor product `rep_1 ⊗ ... ⊗ rep_n` into
   irreducible components via repeated PR 1 fusion.
3. The integral equals the projection onto the trivial (singlet)
   component of the total tensor product, expressed via PR 2
   intertwiners.

**Validation:**
- 1-link case: reduces to the known single-link identity.
- 2-link case for `(lambda, mu) = (1, 0), (0, 1)`: should give the
  trivial singlet projector, computable analytically.
- 3-link case for `(1, 0)^3`: should reproduce the SU(3) epsilon-tensor
  invariant.
- Sum rule: integrating with the constant function should give 1
  (Haar measure normalization).

**API exposed for PRs 4-5:**
- `haar_integral_1link(reps, link_data)` returns the contracted
  intertwiner result.
- `haar_integral_nlink(reps_list, link_data_list)` for general n-link
  integrals.

**Estimated complexity:** ~300-500 lines of code.

## 5. PR 4 — Tensor-network contraction engine (planned)

**Goal:** generic contraction engine for tensor networks on lattice
graphs: given a graph (sites, links, plaquettes), an irrep assignment
to each plaquette, and Wilson-action weights, evaluate the partition
function via PR 3's Haar primitives.

**Architecture:**
- `LatticeGraph`: encodes sites, oriented links, plaquette loops
  (each plaquette is a list of (link, orientation) pairs).
- `IrrepAssignment`: maps each plaquette to an SU(3) irrep `(p, q)`.
- `evaluate_assignment(graph, assignment, character_coefs)`: sums over
  link integrations using PR 3 primitives. Returns the contribution to
  the partition function from this irrep configuration.
- `partition_function(graph, character_coefs, nmax)`: sums
  `evaluate_assignment` over all irrep assignments in the dominant-weight
  box (with Haar selection rules pruning).

**Validation:**
- Single-plaquette case (1 site, 4 links wrapping the plaquette): should
  reproduce the standard one-plaquette character expansion.
- 2-plaquette adjacent case: should reproduce known closed-form
  evaluations.
- Compare to brute-force Cartan-torus integration on small graphs.

**Performance considerations:**
- Sparse irrep assignments (most contributions vanish by selection rules).
- Memoization of repeated intertwiner contractions.
- Numerical thresholding to discard vanishingly small contributions.

**API exposed for PR 5:**
- `LatticeGraph` constructor for arbitrary graph data.
- `ZboundaryClass(graph, character_coefs, marked_plaquette, holonomy)`:
  computes `Z_beta^env(W)` for marked-plaquette holonomy `W`.
- `extract_rho(graph, character_coefs, marked_plaquette)`: extracts
  the boundary character measure `rho_(p,q)(beta)` via Peter-Weyl
  projection.

**Estimated complexity:** ~500-800 lines of code.

## 6. PR 5 — L_s=2 APBC cube + P(6) bridge-gate check (planned)

**Goal:** apply the engine to the L_s=2 APBC spatial cube to compute
`rho_(p,q)(6)` explicitly, then plug into the source-sector
factorization to compute `P(6)` and report the bridge-gate outcome for
independent audit.

**Geometry:**
- 8 sites (2^3 at L=2 APBC).
- 12 directed spatial link uses, corresponding to 6 unique unoriented
  spatial links under L=2 identifications.
- 6 unique unoriented spatial plaquettes, with orientation bookkeeping.
- 1 marked plaquette + 5 unmarked, matching the native staging gate.

**Computation:**
1. Construct the cube `LatticeGraph` (PR 4 input).
2. Extract `rho_(p,q)(6)` via `extract_rho` (PR 4 output).
3. Build the source-sector operator
   `T_src(6) = exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)` using
   `rho_(p,q)(6)`.
4. Solve the Perron eigenvector and compute
   `P(6) = <psi_Perron, J psi_Perron>`.
5. Report the bracket `[P(6) - tolerance, P(6) + tolerance]` from NMAX
   convergence.

**Validation:**
- NMAX convergence study (super-polynomial expected).
- Comparison to the existing reference Perron solves
  (`P_loc = 0.4524`, `P_triv = 0.4225`) — the cube `rho_(p,q)(6)`
  should be a SPECIFIC sequence, neither uniformly 1 nor delta.
- Comparison to the bridge-support upper bound `0.59353` — the cube
  result should land below this.
- Comparison to the canonical MC value `0.5934` (audit comparator only,
  NOT a derivation input).

**Gate logic:**
- If a future audited cube computation produces a decisive bracket
  compatible with the bridge-support target, queue the parent dependency
  chain for re-audit with the cube result as a bounded dependency.
- Otherwise, preserve the achieved narrowing and keep the parent bridge
  chain open.

**Estimated complexity:** ~500-1000 lines of code (geometry + glue).

## 7. Total scope estimate

| PR | LOC estimate | Validation effort | Cumulative time |
|---|---|---|---|
| 1 | ~400 | 9 identities | 1 session (this) |
| 2 | 500-800 | ~10 identities | 2-4 sessions |
| 3 | 300-500 | ~6 identities | 1-2 sessions |
| 4 | 500-800 | ~5 graph cases | 2-3 sessions |
| 5 | 500-1000 | NMAX + reference + comparator | 1-2 sessions |
| **Total** | **2200-3500** | **~30 checks** | **7-12 sessions** |

This is a multi-week project for a single developer. Each PR is
designed to be independently mergeable and reviewable.

## 8. What this engine enables (beyond the cube Perron solve)

The same engine, once built, will be useful for:

1. **Other small-volume SU(3) lattice computations** (e.g., the L_s=3
   spatial cube for finite-size scaling).
2. **String tension** (Wilson loop expectation values for larger
   loops via tensor-network contraction).
3. **Other gauge-scalar bridge instances** (the engine is gauge-group-
   agnostic; the SU(3) specialization is in the character data).
4. **Bootstrap sanity checks** at small-volume instances where exact
   results are computable and any external source brackets are explicitly
   available.

## 9. Audit consequence

```yaml
claim_id: su3_tensor_network_engine_roadmap_note_2026-05-03
note_path: docs/SU3_TENSOR_NETWORK_ENGINE_ROADMAP_NOTE_2026-05-03.md
claim_type: meta
intrinsic_status: unaudited
deps: []
verdict_rationale_template: |
  Roadmap meta-document laying out the 5-PR plan to build a bounded
  SU(3) tensor-network engine for a future explicit cube Perron solve.
  PR 1 delivered in this commit as a finite-box bounded support theorem.
  PRs 2-5 are planned as separate sessions with explicit interface
  contracts and validation criteria. Estimated total scope: ~2200-3500
  LOC, 7-12 sessions. Engine is permanent infrastructure useful beyond
  the immediate cube Perron application (other small-volume SU(3)
  computations, string tension, and external-bracket sanity checks when
  source brackets are available).
```

## 10. Cross-references

- PR 1 deliverable: [`SU3_FUSION_ENGINE_PR1_THEOREM_NOTE_2026-05-03.md`](SU3_FUSION_ENGINE_PR1_THEOREM_NOTE_2026-05-03.md)
- Open bridge gate: [`GAUGE_SCALAR_BRIDGE_3PLUS1_NATIVE_TUBE_STAGING_GATE_2026-05-03.md`](GAUGE_SCALAR_BRIDGE_3PLUS1_NATIVE_TUBE_STAGING_GATE_2026-05-03.md)
- Source-sector factorization: [`GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md)
- Existing tensor-transfer support packet: [`GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md)
- Reference Perron solves: [`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md)
