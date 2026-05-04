# Counterfactual Pass: Gauge-Scalar Bridge / SU(3) L_s=3 Cube Campaign

**Date:** 2026-05-04
**Claim type:** scoping
**Status:** route-discovery artifact, not a theorem.
**Methodology:** [`docs/ai_methodology/skills/physics-loop/references/assumption-import-audit.md`](ai_methodology/skills/physics-loop/references/assumption-import-audit.md) (Counterfactual Pass section, PR #502)

## 0. Context and trigger

The campaign has shipped 7 PRs ruling out closure paths:
- L_s=2 PBC ([PR #501](https://github.com/jonathonreilly/cl3-lattice-framework/pull/501))
- 4 closed-form approximations ([PR #503](https://github.com/jonathonreilly/cl3-lattice-framework/pull/503))
- Naive Haar MC ([PR #506](https://github.com/jonathonreilly/cl3-lattice-framework/pull/506))
- Greedy contraction ([PR #509](https://github.com/jonathonreilly/cl3-lattice-framework/pull/509))
- Naive treewidth contraction ([PR #510](https://github.com/jonathonreilly/cl3-lattice-framework/pull/510))

The remaining viable engineering item (#2a: rank-aware contraction) is multi-day and compute-heavy. **Per user direction**, run the counterfactual pass to surface algebraic routes that may obviate the need for compute.

## 1. Methodology (allowed outcomes)

Per the no-new-axiom rule (memory: `feedback_no_new_axioms.md`):

**Allowed:**
- (D) Derivation from existing retained primitives
- (I) Take import → bounded retained → retire it
- (M) Demote claim
- (F) Forced finding (no live alternative)

**Forbidden:**
- New axiom adoption
- Hypothetical premise as retained-grade route
- Observed/fitted value as derivation input

## 2. Assumption ledger + counterfactual table

| # | Assumption | What if wrong? | Concrete alternative | Direction it opens | Feasibility | Score |
|---|---|---|---|---|---|---|
| A | L_s=3 PBC is the right block | Smaller works with different boundary | L_s=2 APBC (anti-periodic) | APBC ≠ PBC: cube character measure differs; original "V-invariant minimal block" was APBC, not PBC | live (D) | **3** |
| B | Boundary condition is PBC | Twisted / open boundary | L_s=2 with twisted Wilson loops at boundary | Twisted BC can lift "all-forward" degeneracy of L_s=2 PBC | live (D) | 2 |
| C | (1,1) is the load-bearing sector | Other irreps drive `<P>` | (1,0) + (0,1) fundamentals contribute to character expansion | Lower-rank Haar projectors (rank 1) → much smaller TN; might capture most of `<P>` | live (D) | **3** |
| D | Wilson +d_1+d_2-d_1-d_2 traversal | Different cycle convention | All-forward (PBC) vs +-+- vs symmetric loops | Already explored (Block 5); known to differ at L_s=2 | infeasible (mostly explored) | 1 |
| E | Source-sector NMAX=7 truncation | Need higher | NMAX=10, 15 | Marginal — Perron solve already converges | infeasible (insensitive) | 0 |
| F | Each link in 4 plaquettes | Block-marked sub-cube | Mark a subset of plaquettes; effective incidence = 1-2 | Reduces effective TN size; need to verify that the marked subset is what V-invariance requires | live (D) | **3** |
| G | Wigner-Racah engine path is right | Different mathematical structure | Lattice Gauss law constraint, character group cohomology, eigenvalue distribution | New structure could give closed form via a known SU(3) identity | live (D) | 2 |
| H | Rank-8 P^G is irreducible | Internal structure | Decompose 8 singlets into representation-class subgroups (e.g., 1 + 7, or sym + antisym mixes) | Smaller "effective rank" inside contraction; reduces intermediate sizes | live (D) | 2 |
| I | Independent SU(3) Haar per link | Constrained measure | Axial gauge fixing (set 1 link per cube to identity) | Reduces dim by factor 8^(N_axial); fixes some cyclic indices | live (D) | **3** |
| J | β=6 is the right scale | Different β natural to framework | β chosen by framework's RG fixed point (small) | At small β, character expansion converges fast; closed form may exist | infeasible (β=6 forced by framework prediction chain) | 0 |
| K | `<P>` is the right observable | Different observable | `<tr U_p²>`, plaquette correlator, polyakov loop, string tension | Some observables have closed forms at β=6 even when `<P>` doesn't | live (D) | 2 |
| L | EXACT contraction required | Truncation acceptable | Bounded TN truncation with controlled error | Violates exactness; would need rescope of "retained" claim | infeasible (violates exactness) | 0 |
| M | Cube is the right block geometry | Other geometries | Tetrahedron, octahedron, cylinder | Smaller geometries may have lower effective treewidth | live (D) | 1 |
| N | g_bare=1 (β=6 forced) | Different bare coupling | β=8, β=10, etc. | Each gives different Wilson value; not a path to β=6 closure | infeasible (β=6 fixed) | 0 |
| O | 4-fold Haar projector at L_s=3 | Refactored grouping | Group adjacent links into "super-links"; reduce N_links | Could reduce effective treewidth; trades off rank | live (D) | 2 |
| P | Cyclic-trace plaquette character | Smeared / improved action | Wilson + clover, Symanzik improvement | Different action; could converge faster but different observable | infeasible (different observable) | 1 |
| Q | Engine Blocks 1-5 used correctly | Implementation error | Re-derive from scratch | Forced finding only | live (F) | 1 |
| R | 4 GB memory budget | Larger budget feasible | 64 GB, 256 GB | Even 256 GB ÷ 16 = 16e9 entries < 8^11 = 8.5e9 — would JUST fit at TW=11. Could close to TW=11 with right method | live (D) | 2 |
| S | V-invariant minimal block = cube | Other V-invariant blocks | Triangle on lattice (3-link), bowtie graph | If a smaller V-invariant block exists, contraction is much smaller | live (D) | 2 |
| T | Wilson character expansion basis | Different basis | Eigenvalue (a, b, c) Cartan-torus basis; Vandermonde directly | Cartan-torus integration gives integers (Schur character formula); may give closed-form via finite-volume sum | live (D) | **3** |
| U | opt_einsum forbidden | Adopt as new primitive | `pip install opt_einsum`; allow as numpy companion | Better contraction-path optimization could find lower TW orderings, but treewidth ≥ 29 is structural | infeasible (PR #510 shows naive elim infeasible regardless) | 1 |
| V | Importance-sampled MC forbidden | Constrained MC with derived weight | Sample from Wilson Boltzmann derived from framework primitives | Imports the comparator; breaks no-imports policy | infeasible (forbidden) | 0 |
| W | Need full partition function | Need only a structural quantity | Single ρ-coefficient, spectral moment, lowest-eigenvalue | Could short-circuit if a specific quantity has closed form | live (D) | **3** |
| X | Source-sector factorization required | Direct Z evaluation | Bypass ρ-construction; evaluate Z directly | Not obviously simpler; existing framework uses ρ | infeasible (no obvious simplification) | 0 |
| Y | Adjoint (1,1) the right rep | Fundamental (1,0)/(0,1) | Compute T_(1,0)(L=3 cube): rank-1 2-fold projector for fund⊗fund̄ | Lower rank → much smaller TN; check if (1,0) is dominant in `<P>` expansion | live (D) | **3** |
| Z | Numerical contraction needed | Algebraic identity | Schur orthogonality + cube symmetry → ρ ratios closed form | If cube has 6× symmetry (octahedral group), Schur reduces independent ρ's to ~5; algebraic | live (D) | **3** |

## 3. Top live counterfactuals (score ≥ 3)

Six counterfactuals scored 3 — all (D) outcomes (derivation from existing primitives):

### A. L_s=2 APBC (not PBC)

**Claim:** the framework's "V-invariant minimal block" originally specified APBC (anti-periodic spatial boundaries), not PBC. PR #501 (Block 5) only verified PBC. APBC could give a different cube character measure.

**Why investigate:** if APBC gives `<P> = 0.5935`, closure via existing primitives. The "anti-periodic" twist breaks the "all-forward = degenerate" pattern of L_s=2 PBC.

**Effort:** 30-60 min. Modify the L_s=2 cube geometry to use APBC, recompute the candidate ρ + Perron value.

### C. Lower irreps drive `<P>`

**Claim:** the (1,0) fundamental + (0,1) anti-fundamental contribute the bulk of `<P>(β=6)` via `c_(1,0)/c_(0,0)`. Higher irreps (1,1), (2,0), etc. contribute corrections.

**Why investigate:** rank of N-fold Haar projector for FUNDAMENTAL is rank 1 (single singlet for `(1,0)⊗(0,1)`). At L_s=3 with 4 plaquettes per link, the 4-fold Haar of `(1,0)⊗(0,1)⊗(1,0)⊗(0,1)` has rank determined by `(1,0)⊗(1,0)⊗(0,1)⊗(0,1) → trivials` count. For SU(3) this is the number of singlets in `3⊗3̄⊗3⊗3̄` = 2 (per multinomial counting). So rank-2 instead of rank-8 — exponentially smaller TN.

**Effort:** 1-2 hours. Build (1,0)/(0,1) version of Block 2's projector, recompute.

### F. Block-marked sub-cube

**Claim:** the framework's V-invariance only requires a subset of cube plaquettes to be Wilson-loop-style; the rest can be reduced via additional symmetries.

**Why investigate:** if V-invariance demands only 27 plaquettes (one per site, single direction) instead of 81, the link incidence drops from 4-per-link to 1-per-link. This makes 2-fold Haar (rank 1) sufficient — exactly the L_s=2 PBC structure scaled.

**Effort:** scope check — read existing framework V-invariance docs, identify the actual primitive requirement. 30-60 min to confirm or refute.

### I. Axial gauge fixing

**Claim:** the cube partition function is invariant under "fix one link per closed loop to identity" (axial gauge). For 81 links and 81 plaquettes (81 closed cycles), this fixes 81/cycle-rank-bound = ? links, reducing the integral.

**Why investigate:** axial gauge dramatically reduces the SU(3) integral dimension. If 27 links can be fixed to identity (one per site row), the remaining 54-link Haar integral might be tractable.

**Effort:** 1-3 hours. Verify gauge invariance of the partition function, build the axial-gauge runner.

### T. Cartan-torus integration

**Claim:** SU(3) Haar integration reduces to integration over the Cartan torus T² with the Weyl-Vandermonde measure. For the cube character expansion, each plaquette's character can be written as a polynomial in Cartan torus coordinates (Schur formula). The full integral might reduce to a 162-dimensional polynomial integral over `T²^81` — combinatorial but possibly closed-form.

**Why investigate:** Block 1's CG decomposition + Block 2's Haar projector are tensor-network-based. The Cartan-torus form is a different decomposition that may be more tractable for finite-volume cubes.

**Effort:** 4-8 hours. Build Cartan-torus partition function and attempt closed-form evaluation.

### W. Just need a structural quantity

**Claim:** maybe `<P>(β=6)` can be derived from a SPECIFIC quantity that has closed form (e.g., the lowest eigenvalue of the source-sector transfer matrix, a specific spectral coefficient, a moment of the Perron distribution) without computing the full partition function.

**Why investigate:** the framework's existing Perron solve computes `P` from eigenvector data. If the LOWEST EIGENVALUE or some other extreme spectral quantity is computable algebraically, that could short-circuit the partition function need.

**Effort:** 2-4 hours. Re-examine the Perron solve formula; identify which inputs can be replaced by algebraic identities.

### Y. Fundamental rep instead of adjoint

**Claim:** related to C — the fundamental rep (1,0) has 4-fold Haar rank ~ 2 (vs adjoint's rank 8). Contraction problem is exponentially smaller.

**Why investigate:** if `<P> = (1/3) c_(1,0)(β) / c_(0,0)(β)` (the leading single-plaquette character) is the right observable, then we never needed the adjoint sector — the fundamental sector at L_s=3 would close via much smaller TN.

This is closely related to the closed-form fan-out (PR #503 M1 = 0.4225 = single-plaquette fundamental). Maybe the FUNDAMENTAL sector at L_s=3 (with multi-plaquette correlations) gives `<P> = 0.5935`, while at L_s=2 it gave 0.4225.

**Effort:** 2-4 hours. Repeat Block 2 algorithm for `(1,0)⊗(0,1)⊗(1,0)⊗(0,1) → trivials` (rank ~2), then redo the L_s=3 contraction. With rank 2, intermediate sizes are 2^k × constants — much smaller.

### Z. Algebraic ratios via Schur + cube symmetry

**Claim:** the L_s=3 PBC cube has 48-fold octahedral symmetry. Plus Schur orthogonality bounds the ρ ratios. Maybe the combination determines ρ_(p,q) up to algebraic identities, no numerical contraction needed.

**Why investigate:** symmetry can reduce the number of independent ρ values from "all" to ~5-10 (one per orbit of the symmetry group acting on irrep tuples). With ~5 unknowns and Schur orthogonality identities providing constraints, maybe the system is solvable algebraically.

**Effort:** 4-8 hours. Build the cube symmetry group action on plaquette assignments, count orbits, derive constraints.

## 4. Critical finding from re-reading framework docs

While running this counterfactual pass (specifically item A), re-reading
[`docs/SU3_TENSOR_NETWORK_ENGINE_ROADMAP_NOTE_2026-05-03.md`](SU3_TENSOR_NETWORK_ENGINE_ROADMAP_NOTE_2026-05-03.md)
and [`docs/GAUGE_SCALAR_BRIDGE_3PLUS1_NATIVE_TUBE_STAGING_GATE_2026-05-03.md`](GAUGE_SCALAR_BRIDGE_3PLUS1_NATIVE_TUBE_STAGING_GATE_2026-05-03.md)
shows that the framework's **actual native target geometry** is dramatically
smaller than the L_s=3 PBC cube I have been attacking:

> **Geometry (per the roadmap and staging gate):**
> - 8 sites (2³ at L=2 APBC)
> - **12 directed spatial link uses, corresponding to 6 unique unoriented
>   spatial links under L=2 identifications**
> - **6 unique unoriented spatial plaquettes**, with orientation bookkeeping
> - **1 marked plaquette + 5 unmarked**

The L_s=2 APBC cube has **6 plaquettes × 6 links = 13.5× smaller per dimension** than the L_s=3 PBC cube I attacked (81 × 81). In tensor-network contraction cost, this is **exponentially smaller**:

| Metric | L_s=3 PBC (attacked) | L_s=2 APBC (actual target) |
|---|---:|---:|
| Plaquettes | 81 | **6** |
| Links | 81 | **6** |
| Cyclic indices | 324 | **24** |
| Treewidth bound | ≥ 29 | ≤ 6 |
| Worst intermediate | `8^30 ≈ 10^28` entries | `8^6 = 262K` entries (4 MB) |
| Memory required | `1.8 × 10^19` GB | **4 MB** |

The L_s=2 APBC cube is **trivially tractable**. The entire L_s=3 attack was on the wrong geometry.

This is a pure win: **counterfactual A is not just live — it is the framework's stated target all along**. The PR #501 Block 5 work explored L_s=2 PBC; the framework's native L_s=2 APBC cube was never solved.

## 5. Synthesis

The compute-heavy path (item #2a from PR #510 = rank-aware contraction) was the next move. The counterfactual pass identifies **6 candidate algebraic / smaller-rank routes** that could short-circuit the compute requirement.

Highest-priority order (by effort × impact):

| Rank | Item | Effort | Impact if works |
|---|---|---:|---|
| 1 | **C / Y: fundamental rep at L_s=3** | 2-4h | rank-2 vs rank-8 → 4^81 ≪ 8^81, may be tractable |
| 2 | **A: L_s=2 APBC** | 30-60min | small effort; may close via existing L_s=2 framework |
| 3 | **F: block-marked sub-cube** | 30-60min | scope check; may reduce link incidence to 1-per-link |
| 4 | **W: structural quantity** | 2-4h | re-examine Perron solve for short-circuits |
| 5 | **Z: algebraic ratios via cube symmetry** | 4-8h | high payoff but hard |
| 6 | **T: Cartan-torus integration** | 4-8h | rep-theory canonical approach |
| 7 | **I: axial gauge fixing** | 1-3h | reduces effective SU(3) integral dim |

## 6. Next move

**Route:** with the L_s=2 APBC critical finding (Section 4), the entire L_s=3 PBC engineering investigation (PRs #501 + #506 + #507 + #509 + #510) was the WRONG geometry. The framework's stated target is L_s=2 APBC with 6 plaquettes × 6 links = trivially tractable (4 MB worst intermediate).

**Immediate next step:** build a runner for the actual L_s=2 APBC cube exact solve. Compute `ρ_(p,q)(6)` for the 6-plaquette cube (1 marked + 5 unmarked). Plug into the source-sector factorization. Compute `P(6)`. Compare to bridge target 0.5935 and ε_witness 3e-4.

If `P(6, L_s=2 APBC cube)` lands within ε_witness of 0.5935, **the bridge closes via existing primitives**. If it lands elsewhere, the closure target is reidentified from the actual cube data, not the L_s=3 PBC misadventure.

This counterfactual pass is the methodology required by [PR #502](https://github.com/jonathonreilly/cl3-lattice-framework/pull/502) before committing to multi-day engineering. **It is itself a route-discovery artifact, not a theorem or a closure attempt.** The single most important deliverable is the discovery in Section 4.

## 6. Audit consequence

```yaml
claim_id: su3_bridge_counterfactual_pass_2026-05-04
note_path: docs/SU3_BRIDGE_COUNTERFACTUAL_PASS_2026-05-04.md
runner_path: null  # methodology artifact, no runner
claim_type: scoping
intrinsic_status: not_a_theorem
deps:
  - physics_loop_counterfactual_pass_methodology_pr_502
  - su3_wigner_l3_treewidth_infeasible_2026-05-04  # PR #510
verdict_rationale_template: |
  Methodology artifact applying PR #502's Counterfactual Pass to the
  gauge-scalar bridge / SU(3) cube campaign. Enumerates 26 assumptions,
  identifies 6 high-priority live counterfactuals scoring 3, and
  proposes a route order with item A (L_s=2 APBC) as cheapest-first.

  This is NOT a theorem and does NOT close the bridge. It is the
  required pre-engineering exercise per the no-new-axiom rule and
  Counterfactual Pass methodology shipped in PR #502.
```

## 7. Cross-references

- Methodology (PR #502): `docs/ai_methodology/skills/physics-loop/references/assumption-import-audit.md`
- No-new-axiom rule (memory): `feedback_no_new_axioms.md`
- Treewidth infeasibility (PR #510): `docs/SU3_WIGNER_L3_TREEWIDTH_INFEASIBLE_2026-05-04.md`
- Block 5 (L_s=2 PBC verdict): `docs/SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md`
