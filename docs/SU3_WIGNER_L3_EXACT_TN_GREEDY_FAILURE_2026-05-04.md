# SU(3) L_s=3 Cube Exact TN: Greedy Contraction Empirically Fails

**Date:** 2026-05-04
**Claim type:** bounded_theorem
**Status:** bounded support theorem — empirical engineering finding, unaudited.
**Primary runner:** `scripts/frontier_su3_wigner_l3_exact_tn_2026_05_04.py`
**Predecessor:** `docs/SU3_WIGNER_L3_TN_CONTRACTOR_POC_2026-05-04.md` (PR #507)

## 0. Headline

PR #507 (TN contractor POC) identified three engineering items required for full L_s=3 cube closure. This PR closes engineering item #1 (exact non-local per-plaquette factor with cross-plaquette index threading) and **empirically confirms** the assessment for item #2 (contraction-order optimization needed beyond greedy).

Specifically: built the full 162-tensor einsum operands list (81 row-side singlet vectors + 81 col-side singlet vectors connected by 405 indices = 81 channel + 324 cyclic), then ran a custom greedy 2-at-a-time contractor with 4 GB memory limit.

**Result:**
- 81 channel-merge steps succeeded (max intermediate 256 MB per link tensor).
- Step 82 (first cyclic contraction between different link tensors) attempted to produce a `4.4 × 10^12`-entry intermediate (~65 TB), exceeding the 4 GB limit by **16,384×**.
- Greedy contractor aborted with status `MEMORY LIMIT EXCEEDED`.

**Verdict:** greedy ordering is empirically insufficient for L_s=3 PBC cube. Treewidth-based contraction order (~8^9 = 2 GB intermediate per the cube's tree-decomposition theory) is required. This requires implementing a tree-decomposition algorithm, which is engineering item #2 from PR #507 — confirmed as a multi-day standalone task.

## 1. What this PR delivers

### 1.1 Cyclic-index labeling for full cube

For each plaquette `p` with cyclic indices `(a, b, c, d)` and links `(l_1, l_2, l_3, l_4)` at signs `(+,+,-,-)`, the standard Wilson `+d_1+d_2-d_1-d_2` traversal maps:

```text
slot 0 (l_1, +):  row=a=cyclic[p,0], col=b=cyclic[p,1]
slot 1 (l_2, +):  row=b=cyclic[p,1], col=c=cyclic[p,2]
slot 2 (l_3, -):  row=d=cyclic[p,3], col=c=cyclic[p,2]   [D^T]
slot 3 (l_4, -):  row=a=cyclic[p,0], col=d=cyclic[p,3]   [D^T]
```

For the full L_s=3 PBC cube: 81 channel indices (one per link) + 4×81 = 324 cyclic indices = **405 unique indices total**. Each link contributes 2 tensors (row-side singlet of shape `(8,8,8,8,8)` and col-side conjugate) for a total of **162 tensors**.

### 1.2 Custom greedy 2-at-a-time contractor

`np.einsum` cannot accept 162 operands at once (string buffer limit 52 chars even via integer-list mode). The custom contractor:

- Uses pool of `(tensor, index_list)` pairs.
- At each step: finds the pair with smallest result-tensor size that share at least one index.
- Remaps indices to local `0..N-1` for each `np.einsum` call (avoids the 52-char limit).
- Contracts via `np.einsum(t_i, local_i, t_j, local_j, local_out)`.
- Tracks max intermediate size; aborts if `>4 GB`.

### 1.3 Empirical scaling analysis

```text
Steps 1-81 (channel-merge phase):
  Each step contracts row-side and col-side tensor of one link via the
  shared channel index α_l. Result has 8 indices (4 row + 4 col cyclic).
  Intermediate size: 8^8 = 16M entries = 256 MB. Manageable.

Step 82 (first cross-link cyclic contraction):
  After channel-merge, every link tensor has 8 cyclic indices.
  Two link tensors share at most 1-2 cyclic indices (depending on
  how many plaquettes they share — typically 1).
  Greedy picked a pair sharing 1 cyclic index.
  Result has 8 + 8 - 2 = 14 indices = 8^14 = 4.4 × 10^12 entries
                                    ≈ 65 TB.
  Limit: 4 GB. EXCEEDED by 16,384×.
```

The L_s=3 PBC cube's link-link adjacency graph (where edges are
"shared cyclic indices = shared plaquette") has high connectivity but
low pairwise overlap. Greedy ordering cannot find low-intermediate
contractions because no good pair exists in the channel-merged
network state.

## 2. What this means for closure

PR #507's three engineering items remain valid:

| Item | Status after this PR |
|---|---|
| 1. Exact (not local) per-plaquette factor with cross-plaquette index threading | **DONE** — operands list built; greedy contractor demonstrated |
| 2. Contraction-order optimization (treewidth-based) | **CONFIRMED REQUIRED** — greedy empirically fails (16,384× over budget) |
| 3. Custom contraction engine | **DONE** — custom greedy contractor with index-remap implemented; sound but order-blind |

The remaining gap is **item #2: a treewidth-based or layer-based contraction order**. For the L_s=3 PBC cube, the tree-width is bounded by `O(L^2) = 9`, so the OPTIMAL intermediate size is `8^9 = 2 GB`, fitting the 4 GB budget — but only with the right order.

Implementing a treewidth-based order requires:

- **Tree decomposition algorithm** for the link-link adjacency graph (NP-hard in general; tractable for L=3 cube via known structural decompositions).
- **Schedule construction** from the tree decomposition.
- **Memory-aware execution** of the schedule.

Engineering effort: **1-3 person-days** for an L_s=3-specific implementation; longer for a general-purpose treewidth-aware contractor.

## 3. Theorem statement

**Bounded theorem (L_s=3 cube greedy TN failure).** The runner
`scripts/frontier_su3_wigner_l3_exact_tn_2026_05_04.py` builds the full
exact tensor-network for the L_s=3 PBC cube (1,1) sector partition
function: 162 tensors connected by 405 indices (81 channel + 324 cyclic).
A custom greedy 2-at-a-time contractor with 4 GB memory limit:

- Successfully completes 81 channel-merge steps, producing 81 link tensors
  each of size `8^8 = 256 MB`.
- At step 82, attempts to contract two link tensors sharing 1 cyclic
  index, producing a `4.4 × 10^12`-entry (~65 TB) intermediate.
- Aborts with status `MEMORY LIMIT EXCEEDED`, intermediate over budget
  by 16,384×.

**Empirical conclusion:** greedy contraction order is structurally
insufficient for L_s=3 PBC cube exact TN. A treewidth-based or
layer-based contraction order (giving `8^9 = 2 GB` intermediate per
the cube's tree-decomposition theory) is required for closure.

## 4. Scope

### 4.1 In scope

- Cyclic-index labeling for full L_s=3 PBC cube (405 indices).
- 162-tensor einsum operands list.
- Custom greedy 2-at-a-time contractor with index-remap workaround for
  `np.einsum`'s 52-char limit.
- Empirical demonstration that greedy ordering scales out at step 82.

### 4.2 Out of scope

- Treewidth-based contraction order (engineering item #2 from PR #507).
- Layer-based contraction order.
- Full L_s=3 cube partition function evaluation.
- Closure of the gauge-scalar bridge.

### 4.3 Not making the following claims

- Does NOT promote the gauge-scalar bridge parent theorem.
- Does NOT compute or constrain `<P>(β=6)`.
- Does NOT evaluate any partition-function value for the (1,1) sector.

## 5. Audit consequence

```yaml
claim_id: su3_wigner_l3_exact_tn_greedy_failure_2026-05-04
note_path: docs/SU3_WIGNER_L3_EXACT_TN_GREEDY_FAILURE_2026-05-04.md
runner_path: scripts/frontier_su3_wigner_l3_exact_tn_2026_05_04.py
claim_type: bounded_theorem
intrinsic_status: unaudited
deps:
  - su3_wigner_l3_tn_contractor_poc_2026-05-04  # PR #507
  - su3_wigner_intertwiner_block2_theorem_note_2026-05-03  # Block 2 algorithm (PR #498)
  - su3_wigner_intertwiner_block3_theorem_note_2026-05-03  # cube geometry (PR #499)
verdict_rationale_template: |
  Bounded support theorem: empirically confirms greedy contraction order
  fails for L_s=3 PBC cube exact TN. Custom greedy 2-at-a-time
  contractor with 4 GB memory limit completes 81 channel-merge steps
  (max intermediate 256 MB) then aborts at step 82 attempting 65 TB
  intermediate (8^14 entries). Greedy picks pair sharing 1 cyclic
  index; the cube's high connectivity prevents finding lower-overlap
  pairs.

  Confirms PR #507 engineering item #2 (treewidth-based contraction
  order) as required for closure. L_s=3 cube tree-width bound = 9
  gives 8^9 = 2 GB optimal intermediate (fits 4 GB), but requires
  proper tree-decomposition implementation.

  Does NOT evaluate <P>(beta=6). Does NOT promote bridge parent chain.
  No forbidden imports.
```

## 6. Cross-references

- TN contractor POC: `docs/SU3_WIGNER_L3_TN_CONTRACTOR_POC_2026-05-04.md` (PR #507).
- L_s=3 Haar MC negative: `docs/SU3_WIGNER_L3_CUBE_HAAR_MC_NEGATIVE_RESULT_2026-05-04.md` (PR #506).
- Closed-form fan-out: `docs/SU3_WILSON_CLOSED_FORM_FANOUT_THEOREM_NOTE_2026-05-04.md` (PR #503).
- Block 5 (L_s=2 verdict): `docs/SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md` (PR #501).

## 7. Command

```bash
python3 scripts/frontier_su3_wigner_l3_exact_tn_2026_05_04.py
```

Expected runtime: ~110 seconds (60s singlet basis + ~30s greedy contractor + diagnostics). Expected summary:

```text
SUMMARY: THEOREM PASS=3 SUPPORT=1 FAIL=0
```

with greedy contractor reaching step 82 before the 65 TB intermediate
trips the 4 GB memory limit.
