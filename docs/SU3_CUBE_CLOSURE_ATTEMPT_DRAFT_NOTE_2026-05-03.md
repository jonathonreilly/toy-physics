# SU(3) Cube Perron Solve — Closure Attempt Scaffolding (DRAFT)

**Date:** 2026-05-03
**Claim type:** open_gate
**Status:** DRAFT — closure attempt scaffolding; the SU(3) Wigner intertwiner
machinery for non-trivial sectors is OUT OF SCOPE for this PR but the
architecture is laid out for the follow-up PR.
**Primary runner:** `scripts/frontier_su3_cube_closure_attempt.py`
**Companion:** [`SU3_CUBE_PERRON_SOLVE_COMBINED_THEOREM_NOTE_2026-05-03.md`](SU3_CUBE_PERRON_SOLVE_COMBINED_THEOREM_NOTE_2026-05-03.md)
(commit e7365f2d2 on main; trivial-sector cube partition function)
**Previous cleanup:** PR #490 (audit-pipeline cleanup for cube row)

## 0. Headline (DRAFT PR)

This is a **DRAFT PR** documenting the closure-attempt path for the
gauge-scalar bridge no-go (PR #477) toward positive-retained-grade
status, beyond the structural-skeleton work already on main.

This PR ships:

1. SU(3) adjoint (1,1) representation construction via Gell-Mann basis
   (verified: identity, unitarity, group homomorphism).
2. Cube tensor-network architecture documentation: precise statement of
   what `T_lambda(cube)` is, what it requires, and why the trivial
   sector is the only one currently computable.
3. Stub for `T_lambda(cube)` returning NaN for non-trivial irreps with
   honest documentation of the deferred work.
4. Recommended next-PR scope for closure (estimated 3-5 sessions of
   focused intertwiner work).

The PR does **NOT** close the no-go quantitatively. The trivial-sector
`P_trivial(6) = 0.4225` from commit e7365f2d2 remains the framework's
best derivable lower bound; the gap to the bridge-support upper bound
`0.5935` (gap `~ 0.171`) cannot be closed without the non-trivial
sector contributions.

## 1. Why DRAFT

The full SU(3) Wigner intertwiner machinery for computing
`T_lambda(cube)` for non-trivial self-conjugate `lambda = (n, n)` and
bipartite-alternating `(lambda, bar(lambda))` sectors requires
implementing:

- SU(3) Wigner-Racah algebra (3j and 6j symbols) for arbitrary irreps
- Explicit intertwiner operators `C^(nu, alpha)_(lambda, mu): V_lambda
  ⊗ V_mu -> V_nu`
- Multi-link Haar integrals via intertwiner contractions
- Topological tensor-network contraction on the L=2 cube graph
  (24 directed links, 12 plaquettes, 8 sites)

Estimated implementation cost: ~500-800 LOC + careful validation against
published SU(3) Wigner-Racah tables. Realistically 3-5 focused sessions.
Not achievable in a single session alongside the audit-pipeline cleanup
and theorem-note work.

## 2. What this DRAFT PR delivers

### 2.1 SU(3) adjoint (1,1) representation construction

Standard Gell-Mann basis `{lambda_1, ..., lambda_8}` of 3x3 traceless
Hermitian matrices, normalized `Tr[lambda_a lambda_b] = 2 delta_(ab)`.

The adjoint representation matrix `D^(1,1)(g)` for g in SU(3) is:

```text
D^(1,1)(g)_{ab} = (1/2) Tr[lambda_a g lambda_b g^dagger]
```

Verified properties:

- `D^(1,1)(I) = I_8` (identity)
- `D^(1,1)(g) D^(1,1)(g)^dagger = I_8` (unitarity)
- `D^(1,1)(g h) = D^(1,1)(g) D^(1,1)(h)` (group homomorphism)

All checks PASS in the runner.

### 2.2 Cube tensor-network architecture

For all-same-self-conjugate `lambda` assignment to the 12 cube
plaquettes, the partition function is:

```text
Z_lambda(cube, all-same) = (c_lambda(6) d_lambda)^12 × T_lambda(cube)
```

where `T_lambda(cube)` is the topological factor computed from:

1. **Plaquette characters**: each plaquette `chi_lambda(U_p) =
   Tr[D^lambda(U_l1) D^lambda(U_l2) D^lambda(U_l3) D^lambda(U_l4)]`.
2. **Link integrations**: each of the 24 links contributes a 2-link
   Haar integral. With both incidences forward and self-conjugate
   `lambda`, the integral collapses to `(1/d_lambda) ×
   (epsilon-tensor index structure)`.
3. **After all 24 link integrations**: `T_lambda(cube)` is the
   topological invariant that depends on the cube graph structure
   and `lambda`-specific intertwiner data.

### 2.3 T_lambda(cube) stub

For each irrep `lambda`, the runner reports:

| lambda | T_lambda(cube) | Status |
|---|---|---|
| (0, 0) | 1.0 | exact (trivial) |
| (1, 1) | NaN | requires intertwiner contraction |
| (2, 2) | NaN | requires intertwiner contraction |

The trivial sector is exact and was used in commit e7365f2d2 to
recover Reference B `P_trivial = 0.4225`. The non-trivial sectors
remain undetermined.

## 3. Recommended next-PR scope (closure path)

To achieve positive-retained-grade closure of the gauge-scalar bridge
no-go, a follow-up PR should implement:

1. **SU(3) Wigner-Racah algebra**: 3j symbols (Clebsch-Gordan
   coefficients) and 6j symbols for arbitrary SU(3) irreps. Implement
   via Pieri iteration starting from fundamental `(1, 0)` ⊗
   intertwiners. Validate against published SU(3) Racah tables.
   (~500 LOC)
2. **Cube tensor-network contraction**: explicit implementation of
   the 24-link Haar integration with intertwiner contractions for a
   given `lambda`. Use the Wigner-Racah primitives from step 1.
   (~300 LOC)
3. **T_(1,1)(L=2 cube)**: explicit numerical value for the adjoint
   sector on the cube. (~50 LOC + extensive validation against
   small-volume SU(3) lattice gauge results in the literature)
4. **Higher self-conjugate sectors**: T_(2,2), T_(3,3), ... up to
   convergence. (Truncation behavior expected to be super-polynomial.)
5. **Bipartite-alternating sectors**: T_(lambda, bar(lambda))
   contributions for non-self-conjugate `lambda`. Requires
   additional intertwiner structure for the bipartite case.
6. **Final source-sector Perron solve**: assemble the full
   `rho_(p,q)(6)` from all sectors, plug into
   `T_src(6) = exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)`, compute
   `P_cube(6)`.
7. **Verdict**: compare `P_cube(6)` to bridge-support upper bound
   `0.5935`. If within `epsilon_witness ~ 3e-4`: HONEST PATH B
   (closure). Otherwise: HONEST PATH A (narrowing only).

Estimated total scope: ~1000 LOC + 3-5 sessions.

## 4. Honest assessment

This DRAFT PR is **infrastructure preparation only**. It does not
advance the no-go closure quantitatively beyond what's already on main
(commit e7365f2d2 + PR #490). The value is in:

- Providing a verified SU(3) adjoint representation as a building
  block for the next PR
- Documenting the precise architecture of the cube tensor-network
  contraction
- Estimating realistic scope for the closure work

The reviewer should:

1. Decide whether to merge this DRAFT as scoping documentation, OR
   keep it open as a scratchpad for the follow-up PR
2. If positive-retained closure is the priority, schedule the
   ~3-5 session intertwiner-engine work as a dedicated multi-PR
   campaign

## 5. Audit consequence (if merged)

```yaml
claim_id: su3_cube_closure_attempt_draft_note_2026-05-03
note_path: docs/SU3_CUBE_CLOSURE_ATTEMPT_DRAFT_NOTE_2026-05-03.md
runner_path: scripts/frontier_su3_cube_closure_attempt.py
claim_type: open_gate
intrinsic_status: unaudited
deps:
  - su3_cube_perron_solve_combined_theorem_note_2026-05-03
  - su3_fusion_engine_pr1_theorem_note_2026-05-03
  - gauge_scalar_temporal_observable_bridge_no_go_theorem_note_2026-05-03
verdict_rationale_template: |
  DRAFT PR shipping the SU(3) adjoint (1,1) representation construction
  (Gell-Mann basis, verified: identity, unitarity, group homomorphism)
  + cube tensor-network architecture documentation + T_lambda(cube) stub.
  Does NOT compute non-trivial sector contributions to rho_(p,q)(6);
  these remain the explicit out-of-scope item requiring multi-week
  Wigner-Racah engine implementation. Trivial-sector P(6) = 0.4225 from
  commit e7365f2d2 stands as the framework's best derivable lower bound.
  Status: open_gate (closure path is structured but not executed).
```

## 6. Cross-references

- Combined PR theorem note (on main): [`SU3_CUBE_PERRON_SOLVE_COMBINED_THEOREM_NOTE_2026-05-03.md`](SU3_CUBE_PERRON_SOLVE_COMBINED_THEOREM_NOTE_2026-05-03.md)
- Fusion engine: [`SU3_FUSION_ENGINE_PR1_THEOREM_NOTE_2026-05-03.md`](SU3_FUSION_ENGINE_PR1_THEOREM_NOTE_2026-05-03.md)
- Engine roadmap: [`SU3_TENSOR_NETWORK_ENGINE_ROADMAP_NOTE_2026-05-03.md`](SU3_TENSOR_NETWORK_ENGINE_ROADMAP_NOTE_2026-05-03.md)
- No-go target: [`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md)
- K-Z external lift companion: [`GAUGE_SCALAR_BRIDGE_KZ_EXTERNAL_LIFT_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_BRIDGE_KZ_EXTERNAL_LIFT_THEOREM_NOTE_2026-05-03.md) (PR #484)

## 7. Command

```bash
python3 scripts/frontier_su3_cube_closure_attempt.py
```

Expected summary:

```text
SUMMARY: THEOREM PASS=4 FAIL=0
```
