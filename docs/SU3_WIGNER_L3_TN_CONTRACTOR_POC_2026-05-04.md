# SU(3) Wigner Engine L_s=3 Tensor-Network Contractor (POC)

**Date:** 2026-05-04
**Claim type:** bounded_theorem
**Status:** bounded support theorem — POC infrastructure, unaudited.
**Primary runner:** `scripts/frontier_su3_wigner_l3_tn_contractor_2026_05_04.py`
**Predecessors:**
- `docs/SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md` (PR #501)
- `docs/SU3_WIGNER_L3_CUBE_HAAR_MC_NEGATIVE_RESULT_2026-05-04.md` (PR #506)

## 0. Headline

After Block 5's L_s=2 verdict, the closed-form fan-out (PR #503), and the L_s=3 Haar MC honest negative (PR #506), the only remaining viable route to gauge-scalar bridge closure is **exact tensor-network contraction at L_s ≥ 3**.

This POC ships the **algorithmic infrastructure** for that route:

1. Block 2's rank-8 singlet basis of `V_(1,1)^4 = C^4096` rebuilt (~60s).
2. L_s=3 PBC cube geometry: 81 unique Wilson plaquettes × 81 directed links × 4-fold link incidence — verified.
3. Per-plaquette **local factor table** `f_p[α₁, α₂, α₃, α₄]` — computed for one demo plaquette.
4. Memory scope analysis: worst intermediate at `8^9 = 134M entries (2 GB)`, fits a 4 GB memory limit.

It also names the **three engineering items** still required for full L_s=3 closure:

1. **Exact (not local) per-plaquette factor**: must account for cross-plaquette index threading. Each link's 8 row/col indices thread through 4 different plaquettes, not just one. Requires constructing the full `(4096 × 4096)` link tensor and contracting via plaquette cyclic constraints.
2. **Contraction-order optimization**: greedy heuristic on 81 nodes likely exceeds `8^9`. Need treewidth-based or layer-based contraction order.
3. **Custom contraction engine**: `numpy.einsum`'s `optimize` flag uses `opt_einsum` library, which is NOT in the framework's `numpy + scipy` only environment.

Engineering scope: **~3-5 person-days**; within AI-assisted multi-session work, plausibly 1-2 sessions per item.

Status: **bounded support theorem** — ships infrastructure, does not close the bridge.

## 1. What the POC delivers

### 1.1 Singlet basis of V^4 (Block 2 algorithm)

```text
Shape: (4096, 8)
Build time: ~60s
PASS: rank-8 orthonormal basis
```

8 orthonormal singlet vectors `s_α ∈ V^4 = C^4096` representing the 8 invariant directions in the 4-fold tensor product of adjoint reps. Each `s_α` reshapes to `(8,8,8,8)`.

### 1.2 L_s=3 PBC cube geometry

```text
unique plaquettes: 81
unique directed links used: 81
link incidence: each link in EXACTLY 4 plaquettes (min=max=mean=4.00)
PASS: 81 × 81 × 4 incidence verified
```

This matches Block 3's geometry. Each directed link is shared by exactly 4 plaquettes (the 4 faces meeting along that edge in the 3D cubic lattice with PBC).

### 1.3 Per-plaquette local factor

For one demo plaquette `(0,0,0)` in the `(0,1)` plane with links `[0, 28, 9, 1]` (encoded link IDs), the **local approximation** factor `f_p[α₁, α₂, α₃, α₄]` was computed:

```text
f_p shape: (8, 8, 8, 8) = 4096 entries
Frobenius norm: 9.000e-02
max |entry|: 9.000e-02
min |entry|: 8.467e-66 (machine-precision floor)
```

The local approximation traces out the OTHER 3 row/col indices of each link's singlet vector to identity (assuming the other plaquettes are decoupled). For a single isolated plaquette, this approximation is exact; for the L_s=3 cube where each link threads through 4 plaquettes, the local approximation IS NOT the exact result.

### 1.4 Memory scope analysis

```text
per-link singlet storage:    0.50 MB     (× 81 links = 40.5 MB)
per-link FULL tensor (8^8):  256 MB      (too big to materialize 81 of these)
total FULL link storage:     20.2 GB     (infeasible)
worst intermediate (8^9):    134M entries = 2.00 GB
memory limit (this POC):     4 GB
PASS: worst intermediate fits under memory limit
```

The cube graph has tree-width bounded by `O(L^2) = 9`, so an OPTIMAL contraction order produces intermediates of at most `8^9 = 2 GB`. This fits within a 4 GB memory budget — provided we find the optimal order. Greedy heuristics on the 81-node bipartite graph are not guaranteed to achieve this bound.

## 2. What's missing for full L_s=3 closure

### 2.1 Exact per-plaquette factor

The local approximation is not the actual answer. The true per-plaquette structure cannot be evaluated independently per plaquette because each link's 8 row/col indices thread through 4 different plaquettes (the 4 plaquettes containing that link). The true contraction must be done globally.

Specifically: for each link `l`, the rank-8 4-fold Haar projector
```text
P^G_l = sum_(α=1)^8 |s_α⟩⟨s_α|
```
acts on `V^4 = C^4096`, with 8 row indices and 8 col indices (one row + one col per incident plaquette). The plaquette cyclic constraints then connect these row/col indices across links.

Concretely: for plaquette `p` with cyclic indices `(a, b, c, d)` and links `(l_1, l_2, l_3, l_4)` at signs `(+, +, -, -)`, the constraint identifies:
```text
col_(l_1, slot_(p, l_1)) = a = row_(l_4, slot_(p, l_4))
col_(l_2, slot_(p, l_2)) = c = col_(l_3, slot_(p, l_3))   [l_3 dagger]
col_(l_4, slot_(p, l_4)) = d = row_(l_3, slot_(p, l_3))   [l_3 dagger]
row_(l_1, slot_(p, l_1)) = b = row_(l_2, slot_(p, l_2))
```
across 81 plaquettes simultaneously.

### 2.2 Contraction-order optimization

For the bipartite graph of 81 channel variables × 81 plaquette factors with 4-regular structure, finding an optimal contraction order is a graph-partitioning problem (related to treewidth). Without an industrial library, options are:

- **Layer-based**: contract one xy-plane at a time. Memory governed by the perimeter of partial cube. For L=3 PBC: 9 plaquettes per layer × 4-link boundary between layers = 36 cross-cuts. Intermediate dim `8^9` per layer interface.
- **Treewidth-based**: use exact treewidth decomposition (NP-hard in general but tractable for L=3 cube).
- **Custom greedy**: at each step, find the pair of tensors whose contraction produces the smallest intermediate. May not achieve optimal.

### 2.3 Custom contraction engine

`numpy.einsum`'s `optimize='optimal'` and `'greedy'` flags rely on the `opt_einsum` library, NOT in the framework's `numpy + scipy.special` only environment. Two paths:

(a) **Adopt `opt_einsum`** as a new framework primitive: requires user approval; changes the import policy.

(b) **Write a custom contractor**: 200-500 LOC for a memory-aware greedy algorithm with explicit intermediate-size tracking. Doable in 1 session.

## 3. Theorem statement

**Bounded theorem (L_s=3 cube TN contractor POC).** The runner
`scripts/frontier_su3_wigner_l3_tn_contractor_2026_05_04.py` builds the algorithmic
infrastructure required for exact tensor-network contraction of the L_s=3 PBC
cube partition function in the (1,1) sector. Specifically: (a) the 8-dim
singlet basis of `V_(1,1)^4` is rebuilt from Block 2's algorithm; (b) the
L_s=3 PBC cube geometry (81 plaquettes, 81 directed links, 4-fold link
incidence) is verified; (c) a local-approximation per-plaquette factor table
`f_p[α₁,...,α_4]` of shape `(8,8,8,8)` is computed; (d) memory scope analysis
confirms the worst-case intermediate `8^9 = 2 GB` fits a 4 GB memory budget,
provided an optimal-order contractor is available.

The runner explicitly identifies the THREE engineering items required for
full L_s=3 closure: exact (non-local) per-plaquette factor accounting for
cross-plaquette threading, contraction-order optimization, and a custom
contraction engine independent of `opt_einsum`. Engineering scope estimated
at 3-5 person-days.

This POC delivers infrastructure but does NOT close the gauge-scalar bridge.

## 4. Scope

### 4.1 In scope

- Singlet basis construction (Block 2 algorithm) verified.
- L_s=3 PBC cube geometry verified.
- Per-plaquette local factor table computed for one demo plaquette.
- Memory scope analysis: `8^9 = 2 GB` worst intermediate, fits 4 GB.
- Identification of remaining engineering items.

### 4.2 Out of scope (deferred to future PRs)

- Exact (non-local) per-plaquette factor with cross-plaquette threading.
- Contraction-order optimization.
- Custom contraction engine.
- Full L_s=3 cube partition function evaluation.
- Closure of the gauge-scalar bridge.

### 4.3 Not making the following claims

- Does NOT promote the gauge-scalar bridge parent theorem.
- Does NOT compute or constrain `<P>(β=6)`.
- The local-approximation factor is NOT the L_s=3 result; do not quote.
- No forbidden imports (numpy + scipy.special only).

## 5. Audit consequence

```yaml
claim_id: su3_wigner_l3_tn_contractor_poc_2026-05-04
note_path: docs/SU3_WIGNER_L3_TN_CONTRACTOR_POC_2026-05-04.md
runner_path: scripts/frontier_su3_wigner_l3_tn_contractor_2026_05_04.py
claim_type: bounded_theorem
intrinsic_status: unaudited
deps:
  - su3_wigner_intertwiner_block2_theorem_note_2026-05-03  # PR #498 (singlet basis algorithm)
  - su3_wigner_intertwiner_block3_theorem_note_2026-05-03  # PR #499 (cube geometry)
  - su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03  # PR #501
  - su3_wigner_l3_cube_haar_mc_negative_result_2026-05-04  # PR #506
verdict_rationale_template: |
  Bounded support theorem shipping algorithmic infrastructure for L_s=3
  PBC cube tensor-network contraction. POC deliverables:
    - 8-dim singlet basis of V^4 (Block 2 algorithm) rebuilt
    - L_s=3 PBC cube geometry (81 plaquettes, 81 links, 4-fold incidence)
      verified
    - Per-plaquette local-approximation factor table (8,8,8,8) computed
    - Memory scope: 8^9 = 2 GB worst intermediate, fits 4 GB limit

  Identifies three engineering items for full L_s=3 closure: (1) exact
  per-plaquette factor with cross-plaquette threading, (2) contraction-
  order optimization (graph-partitioning), (3) custom contraction engine
  independent of opt_einsum. Engineering scope ~3-5 person-days.

  Runner SUMMARY: THEOREM PASS=4 SUPPORT=0 FAIL=0.

  Does not close the gauge-scalar bridge. Does not promote the parent
  chain. No forbidden imports.
```

## 6. Cross-references

- Block 5 (L_s=2 verdict): `docs/SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md` (PR #501).
- Closed-form fan-out: `docs/SU3_WILSON_CLOSED_FORM_FANOUT_THEOREM_NOTE_2026-05-04.md` (PR #503).
- L_s=3 Haar MC negative: `docs/SU3_WIGNER_L3_CUBE_HAAR_MC_NEGATIVE_RESULT_2026-05-04.md` (PR #506).
- Bridge no-go: `docs/GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`.

## 7. Command

```bash
python3 scripts/frontier_su3_wigner_l3_tn_contractor_2026_05_04.py
```

Expected runtime: ~60 seconds (singlet-basis build dominates). Expected summary:

```text
SUMMARY: THEOREM PASS=4 SUPPORT=0 FAIL=0
```
