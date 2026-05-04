# SU(3) Wigner Engine — Block 3: L_s=3 PBC Cube Geometry + Tensor-Network Setup

**Date:** 2026-05-03
**Claim type:** bounded_theorem
**Status:** bounded support — finite-graph encoding of the L_s=3 PBC
spatial cube + tensor-network index structure for Block 4 to consume.
Pure combinatorics + lattice-geometry primitives; numpy only;
unaudited. The note proposes the bounded support tier for audit
consideration.

**PR #484 lessons applied** (per
`docs/work_history/repo/review_feedback/PR484_KZ_EXTERNAL_LIFT_REVIEW_2026-05-03.md`):
status vocabulary uses `bounded support` / `unaudited` (no pre-written
retained); runner depends only on numpy; no external numeric brackets;
no parent-chain promotion claimed.

**Primary runner:** `scripts/frontier_su3_wigner_l3_cube_geometry.py`
**Block in campaign:** 3 of N (cube-closure campaign for gauge-scalar
bridge no-go #477)
**Prior blocks:**
- Block 1: [`SU3_WIGNER_INTERTWINER_BLOCK1_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK1_THEOREM_NOTE_2026-05-03.md) (PR #495 — fusion engine)
- Block 2: [`SU3_WIGNER_INTERTWINER_BLOCK2_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK2_THEOREM_NOTE_2026-05-03.md) (PR #498 — 4-fold Haar projector)

## 0. Headline

Block 3 delivers the geometric and tensor-network infrastructure
needed for Block 4 (partition function computation) and Block 5 (final
P_cube vs ε_witness verdict). Key results:

- **L_s=3 PBC cube geometry encoded**: 27 sites, 81 directed links,
  81 unique unoriented plaquettes (no L=2 PBC collapse — standard 3D
  lattice geometry).
- **Each link is in exactly 4 plaquettes** (verified by exhaustive
  enumeration), confirming this is the regime where Block 2's 4-fold
  Haar projector applies.
- **Plaquette adjacency graph**: 486 edges, every plaquette has
  degree 12 (= 4 boundary links × 3 other plaquettes per link).
- **Tensor-network index structure** built and verified, ready for
  Block 4 to consume.
- **Memory estimate**: with rank-8 decomposed projectors, total
  tensor-network state is **~44 MB** — well within commodity laptop
  scope for Block 4.

## 1. L_s=3 PBC cube geometry

### 1.1 Site / link / plaquette counts

For a 3D PBC lattice at L_s = 3:

| Object | Count | Formula |
|---|---|---|
| Sites | 27 | L^d = 3^3 |
| Directed links | 81 | d × L^d = 3 × 27 |
| Unique unoriented plaquettes | 81 | (d choose 2) × L^d = 3 × 27 |

Sites are at positions `(x, y, z)` with `x, y, z ∈ {0, 1, 2}`. Each
directed link is identified by `(start_x, start_y, start_z, dir)`
with `dir ∈ {0, 1, 2}` for `{+x, +y, +z}`. Each unique unoriented
plaquette is identified by `(start_site, plane_dir1, plane_dir2)`
with `plane_dir1 < plane_dir2` (so 3 planes: xy, xz, yz).

### 1.2 No L=2 PBC collapse

Unlike L=2 PBC (where each directed link is in only 2 plaquettes due
to a special degeneracy when `n+1 ≡ n-1 mod L` for L=2), at L=3 PBC
the standard 3D lattice geometry holds: **each directed link is in
exactly 4 plaquettes** (2 plaquettes per orthogonal plane, on either
side of the link).

This is verified by exhaustive enumeration in the runner: 81 directed
links × 4 plaquettes/link = 324 total link-plaquette incidences =
81 plaquettes × 4 boundary links. ✓

### 1.3 Plaquette boundary links

For plaquette at `(start, dir1, dir2)`:

```text
link 1: U_+dir1(start)             — segment start → start + dir1
link 2: U_+dir2(start + dir1)      — segment start + dir1 → start + dir1 + dir2
link 3: U_+dir1(start + dir2)      — segment start + dir2 → start + dir1 + dir2 (used as dagger in plaquette product)
link 4: U_+dir2(start)             — segment start → start + dir2 (used as dagger in plaquette product)
```

The plaquette holonomy is:
```text
U_p = U_+dir1(start) · U_+dir2(start + dir1)
      · U_+dir1(start + dir2)†
      · U_+dir2(start)†
```

This convention uses each link variable in its forward orientation
in the lattice's link-variable database, but with appropriate `†`
applied at the plaquette-product level for links 3 and 4.

## 2. Plaquette adjacency graph

Two plaquettes are adjacent iff they share a directed boundary link.
At L=3 PBC each link is in 4 plaquettes, so each link contributes
`C(4, 2) = 6` plaquette-pair adjacency edges:

| Quantity | Value | Verification |
|---|---|---|
| Adjacency edges | 486 | 81 links × 6 pairs/link |
| Plaquette degree (uniform) | 12 | 4 boundary links × 3 others/link |
| Edge count cross-check | 486 | 81 plaquettes × 12 / 2 |

Every plaquette has exactly degree 12; the degree sequence is uniform
(all 81 plaquettes have the same degree). This is verified by
`plaquette_degrees` in the runner.

## 3. Tensor-network index structure for Block 4

For the all-`(1,1)`-irrep sector on the L=3 cube:

- Each plaquette `p` carries an irrep label `λ_p = (1,1)` (assumed
  for this sector).
- Each plaquette has 4 boundary slots, each holding an 8-dim index
  (= `d_(1,1) = 8`).
- Each plaquette is therefore a tensor in `V_(1,1)^⊗4 = C^(8^4) = C^4096`.
- At each directed link `l`, the 4 plaquettes meeting at `l`
  contribute one tensor slot each. Block 2's `P^G_((1,1)^⊗4)`
  projector acts on these 4 slots, projecting onto the 8-dim
  SU(3)-invariant subspace.

Block 3 builds:
- `plaquette_index_map`: dict mapping each plaquette index to a list
  of `(link, slot_idx)` pairs (4 entries per plaquette).
- `link_to_slots_map`: dict mapping each directed link to a list of
  `(plaq_idx, slot_idx)` pairs (4 entries per link, since each link
  is in 4 plaquettes).
- Total tensor index count: 4 × 81 = 324 (verified).

These data structures are the input for Block 4's contraction.

## 4. Memory + complexity estimates for Block 4

Critical observation: the per-link Haar projector `P^G_((1,1)^⊗4)`
has **rank 8** (per Block 2). This means the projector decomposes as
a sum of 8 outer products of 4096-dim singlet vectors:

```text
P^G = Σ_α |singlet_α⟩⟨singlet_α|     (α = 1..8)
```

| Storage scheme | Memory | Notes |
|---|---|---|
| Per-plaquette tensor (rank-4, 8-dim) | 5.1 MB total (81 × 4096 × 16 B) | base storage |
| Naive dense projector at each link (8^8 entries) | 20.3 GB total (81 × 16M × 16 B) | infeasible |
| Rank-8 decomposed projectors (8 × 4096 entries) | 40.5 MB total (81 × 8 × 4096 × 16 B) | tractable |
| **Total tensor-network state (decomposed)** | **~44 MB** | |

Block 4 will use rank-8 decomposed projectors to keep memory in check.

**Contraction complexity**: each link's projector application reduces
the 4 plaquette indices (each 8-dim, total `8^4 = 4096` configurations)
to a sum over 8 singlet basis vectors. The full contraction order on
the 81-plaquette graph is a graph-partitioning problem; Block 4 will
use either heuristic ordering (greedy by smallest-intermediate-tensor)
or established libraries (`opt_einsum`, `ncon`, `jax`).

Expected runtime for Block 4: minutes to hours depending on contraction
order. Memory peak: ~few GB at most.

## 5. Validation results

`SUMMARY: THEOREM PASS=7 FAIL=0`

| # | Check | Result |
|---|---|---|
| V1 | Site/link/plaquette counts (27/81/81) | exact match |
| V2 | Each link in exactly 4 plaquettes | 81 of 81 verified |
| V3 | Total link-plaquette incidences = 324 | exact |
| V4 | Plaquette adjacency edges = 486 | exact |
| V5 | Plaquette degree uniform = 12 | all 81 plaquettes |
| V6 | Total tensor indices = 324 | exact |
| V7 | Each link contracts exactly 4 plaquette-slot pairs | exact |

All 7 substantive verifications pass.

## 6. Theorem statement

**Theorem (L_s=3 PBC cube geometry, Block 3).** The L_s=3 PBC
spatial cube in 3D has:

- 27 sites at integer coordinates `(x, y, z)` with `x, y, z ∈ {0, 1, 2}`.
- 81 directed links, each labeled by `(start_x, start_y, start_z, dir)`.
- 81 unique unoriented spatial plaquettes, each labeled by
  `(start_site, plane_dir1, plane_dir2)` with `plane_dir1 < plane_dir2`.
- Each directed link is in exactly 4 unique unoriented plaquettes
  (no L=2 PBC collapse).
- Each plaquette has exactly 4 boundary directed links.
- Total link-plaquette incidences: 324.

The plaquette adjacency graph (two plaquettes adjacent iff they share
a boundary link) has 486 edges; every plaquette has degree 12.

For the SU(3) lattice gauge theory in the all-`(1,1)`-irrep sector,
the tensor-network index structure has 324 indices (4 per plaquette,
each 8-dim) with 81 link-contractions via the rank-8 4-fold Haar
projector `P^G_((1,1)^⊗4)` from Block 2.

**Proof sketch.** All quantities are computed by exhaustive enumeration
in the runner (Python `for` loops on finite sets); each verification
is a deterministic equality check. ∎

## 7. Block 3 API (importable for Block 4)

| Function | Returns | Used by Block 4 |
|---|---|---|
| `all_sites()` | List of 27 site tuples | yes |
| `all_directed_links()` | List of 81 directed-link tuples | yes |
| `all_unique_plaquettes()` | List of 81 plaquette tuples | yes |
| `plaquette_links(plaq)` | 4 boundary link tuples | yes |
| `link_to_plaquettes(plaqs)` | dict link → 4 plaquette indices | yes |
| `verify_link_incidence(plaqs, links)` | (bool, issues, in_4, in_2) | sanity check |
| `plaquette_adjacency(plaqs)` | List of (p_a, p_b, link) edges | optional |
| `plaquette_degrees(edges, n)` | List of 81 integers (= 12 each) | sanity |
| `build_tensor_network_index(plaqs)` | (plaq_map, link_map, total_idx) | **direct input for Block 4** |
| `memory_estimate_block4(...)` | dict of MB/GB estimates | sanity |

## 8. Audit-lane handoff

```yaml
claim_id: su3_wigner_intertwiner_block3_theorem_note_2026-05-03
note_path: docs/SU3_WIGNER_INTERTWINER_BLOCK3_THEOREM_NOTE_2026-05-03.md
runner_path: scripts/frontier_su3_wigner_l3_cube_geometry.py
proposed_claim_type: bounded_theorem
proposed_intrinsic_status: unaudited
deps:
  - su3_wigner_intertwiner_block2_theorem_note_2026-05-03
  - su3_wigner_intertwiner_block1_theorem_note_2026-05-03
audit_authority: independent audit lane only
runner_environment_dependencies: |
  Python 3 + numpy only. No optional dependencies. Pure combinatorics +
  lattice-geometry computations. Reproducible in standard repo env.
verdict_rationale_template: |
  Block 3 of the cube-closure campaign. Encodes the L_s=3 PBC spatial
  cube geometry (27 sites, 81 directed links, 81 unique unoriented
  plaquettes; each link in exactly 4 plaquettes, no L=2 PBC collapse;
  plaquette adjacency graph has 486 edges with uniform degree 12) and
  builds the tensor-network index structure for Block 4 to consume
  (4 indices per plaquette × 81 plaquettes = 324 total indices,
  contracted by 81 link-projectors at the rank-8 Block 2 P^G primitive).
  Memory estimate using rank-8 decomposed projectors: ~44 MB total
  tensor-network state. All 7 validation checks pass exactly. No
  external numeric brackets, no parent-chain promotion claimed,
  no optional dependencies. Pure infrastructure for Block 4.

lessons_applied_from_pr484_review:
  - status_vocabulary: bounded support / unaudited (not retained)
  - runner_dependencies: numpy + Python stdlib only (no CVXPY, no Mosek)
  - external_imports: none (pure combinatorics)
  - parent_chain_promotion: none claimed
```

## 9. Cross-references

- Block 1 (CG decomposition): [`SU3_WIGNER_INTERTWINER_BLOCK1_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK1_THEOREM_NOTE_2026-05-03.md)
- Block 2 (4-fold Haar projector): [`SU3_WIGNER_INTERTWINER_BLOCK2_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK2_THEOREM_NOTE_2026-05-03.md)
- Continued: future Block 4 (cube partition function) + Block 5 (verdict)
- Eventual target: [`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md)
- L_s=2 cube structural skeleton (separate route, on main): commit `e7365f2d2`
- PR #484 review feedback (lessons learned): `docs/work_history/repo/review_feedback/PR484_KZ_EXTERNAL_LIFT_REVIEW_2026-05-03.md`

## 10. Command

```bash
python3 scripts/frontier_su3_wigner_l3_cube_geometry.py
```

Expected summary:

```text
SUMMARY: THEOREM PASS=7 FAIL=0
```

Runtime: < 1 second on commodity hardware. Memory: < 100 MB.
