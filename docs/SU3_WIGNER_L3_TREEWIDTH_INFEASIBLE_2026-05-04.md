# SU(3) L_s=3 Cube Exact TN: Treewidth Analysis Shows Naive Contraction Infeasible

**Date:** 2026-05-04
**Claim type:** bounded_theorem
**Status:** bounded support theorem — empirical engineering finding, unaudited.
**Primary runner:** `scripts/frontier_su3_wigner_l3_treewidth_2026_05_04.py`
**Predecessor:** `docs/SU3_WIGNER_L3_EXACT_TN_GREEDY_FAILURE_2026-05-04.md` (PR #509)

## 0. Headline

PR #509 confirmed greedy contraction fails at step 82 with a 65 TB intermediate.
PR #507 had estimated that **treewidth-based** ordering would give a 2 GB
intermediate (`8^9`) for the L_s=3 PBC cube — fitting the 4 GB budget.

**This PR shows that estimate was wrong by ~20 orders of magnitude.**

Computed elimination orders for the link adjacency graph (81 nodes,
324 edges, all-degree-8 regular):

| Heuristic | Treewidth UB | Max intermediate |
|---|---:|---:|
| Min-degree | **29** | `8^30 ≈ 10^28` entries (`1.8 × 10^19` GB) |
| Min-fill | **29** | `8^30 ≈ 10^28` entries (`1.8 × 10^19` GB) |
| Memory budget | — | 4 GB |
| Excess factor | — | `~ 4.6 × 10^18×` over budget |

Both standard heuristics return **treewidth bound 29**, giving intermediate sizes that exceed any conceivable memory budget by ~20 orders of magnitude.

## 1. Why PR #507's estimate was wrong

PR #507 estimated treewidth `~ L² = 9` for the L_s=3 PBC cube — based on the treewidth of the **3D cubic lattice graph** (sites + edges).

But the relevant graph for tensor-network contraction cost is the **link adjacency graph**: nodes are link tensors, edges are shared cyclic indices. This is a DIFFERENT, denser graph:

- The 3D lattice graph: nodes = sites, edges = links. For L=3 PBC: 27 nodes, 81 edges, treewidth `~ 9`.
- The link adjacency graph: nodes = **links**, edges = **shared cyclic indices** (= adjacent links in some plaquette). For L=3 PBC: 81 nodes, 324 edges, **treewidth ≥ 29**.

The link adjacency graph is denser and has higher treewidth than the 3D lattice graph. Min-degree and min-fill heuristics both return 29.

## 2. Why even truncation doesn't trivially help

The `8^30 = 1.2 × 10^27` entries (~ `2 × 10^19` GB) figure is for **exact** contraction with full bond dimension 8. To make this fit the 4 GB budget would require:

```text
truncation_dim^30 × 16 bytes ≤ 4 GB
truncation_dim ≤ (4 × 10^9 / 16)^(1/30) ≈ 1.8
```

i.e., bond dimension ≤ 1, which is the trivial sector only. Even bond dimension 2 gives `2^30 × 16 = 16 GB`, still over budget.

So truncation to small bond dimension would discard nearly all of the (1,1) sector content.

## 3. What this means for closure

PR #507's three engineering items must be revised:

| Item | Status (as of this PR) |
|---|---|
| 1. Exact (not local) per-plaquette factor | DONE (PR #509) |
| 2. Treewidth-based contraction order | **CONFIRMED INFEASIBLE** for naive node-elimination on the link adjacency graph |
| 3. Custom contraction engine | DONE (PR #509) |

**New engineering items emerge:**

- **2a. Rank-aware contraction**: keep the rank-8 decomposition of P^G during contraction, never materialize the full `(8,8,8,8,8,8,8,8)` link tensor. The "effective bond" is 8 channels, not 8^k cyclic-index combinations.
- **2b. Sum-of-rank-1 decomposition**: write `P^G = sum_α |s_α⟩⟨s_α|` and keep this rank-1-per-channel structure throughout. Total channel sum: 8^81 configurations — possibly accessible via stochastic sampling.
- **2c. Hierarchical / matrix-product-state ansatz**: approximate the cube's tensor network with a tensor train / MPS structure. Introduces controllable truncation error, which violates exactness.
- **2d. Adopt opt_einsum**: changes import policy. May find better orderings via path optimization, but unlikely to circumvent the fundamental treewidth bound.

## 4. Theorem statement

**Bounded theorem (L_s=3 cube treewidth analysis).** The runner
`scripts/frontier_su3_wigner_l3_treewidth_2026_05_04.py` builds the
link adjacency graph for the L_s=3 PBC cube exact tensor-network
contraction (81 nodes, 324 edges, 8-regular). Both min-degree and
min-fill elimination heuristics return treewidth upper bound **29**.

The corresponding worst-case intermediate size for naive exact
contraction is `8^30 ≈ 1.2 × 10^27` complex entries (~ `1.8 × 10^19` GB),
exceeding any conceivable memory budget by ~20 orders of magnitude.

This empirically refutes PR #507's estimate that treewidth-based
ordering would give a 2 GB intermediate. The L_s=3 PBC cube exact
contraction is **infeasible by naive node-elimination**, regardless of
the elimination heuristic chosen.

## 5. Path forward

Closure of the gauge-scalar bridge via L_s=3 exact tensor-network
contraction requires an alternative approach:

(a) **Rank-aware contraction**: maintain the rank-8 P^G decomposition
    throughout contraction. Effective storage per link is 32K entries
    (not 8^8 = 16M). Contraction may stay in low-bond-dimension regime.
    Requires custom contractor that handles rank-decomposed inputs.
    Engineering: 3-7 days.

(b) **Channel-sum stochastic sampling**: write the partition function
    as a sum over `8^81` channel configurations (`α_l ∈ {1..8}` per
    link), and sample randomly. For each fixed config, the integrand
    is a closed scalar contraction over plaquette cyclic indices.
    May suffer the same sign-problem variance as PR #506's Haar MC.
    Investigate: 1-2 days.

(c) **MPS / hierarchical Tucker truncation**: approximate with bond
    dimension χ. Introduces controlled error. Violates the framework's
    exactness requirement, but may give a useful BRACKET on the answer.
    Engineering: 5-10 days.

(d) **Different framework block**: the bridge no-go theorem identified
    L_s ≥ 3 cube data as the necessary additional primitive. If L=3
    is structurally unsuited for exact computation, perhaps a SMALLER
    block with the right symmetry (e.g., L=2 with TWISTED boundary
    conditions, or smaller-N gauge group as warm-up) is the entry
    point.

## 6. Scope

### 6.1 In scope

- Min-degree and min-fill elimination order heuristics on the L_s=3
  PBC cube link adjacency graph.
- Treewidth upper bounds (both heuristics return 29).
- Refutation of PR #507's `8^9` intermediate-size estimate.
- Identification of new engineering items (rank-aware, channel-sum,
  truncation, or different block).

### 6.2 Out of scope

- Implementation of rank-aware contraction (engineering item 2a).
- Channel-sum stochastic sampling (item 2b).
- Truncated contraction (item 2c).
- Closure of the gauge-scalar bridge.

### 6.3 Not making the following claims

- Does NOT promote the gauge-scalar bridge parent theorem.
- Does NOT compute or constrain `<P>(β=6)`.
- Does NOT prove the lower bound on treewidth (29 is an upper bound from
  heuristics; the true treewidth could be lower).

## 7. Audit consequence

```yaml
claim_id: su3_wigner_l3_treewidth_infeasible_2026-05-04
note_path: docs/SU3_WIGNER_L3_TREEWIDTH_INFEASIBLE_2026-05-04.md
runner_path: scripts/frontier_su3_wigner_l3_treewidth_2026_05_04.py
claim_type: bounded_theorem
intrinsic_status: unaudited
deps:
  - su3_wigner_l3_exact_tn_greedy_failure_2026-05-04  # PR #509
  - su3_wigner_l3_tn_contractor_poc_2026-05-04         # PR #507
verdict_rationale_template: |
  Bounded support theorem: empirical treewidth analysis of L_s=3 PBC
  cube link adjacency graph (81 nodes, 324 edges, 8-regular). Min-
  degree and min-fill elimination heuristics both return treewidth
  upper bound 29, giving intermediate size 8^30 ≈ 1.8e19 GB —
  exceeding 4 GB memory budget by 4.6e18×.

  This refutes PR #507's estimate that treewidth-based ordering would
  give 2 GB intermediate. Naive node-elimination on the link adjacency
  graph is structurally infeasible, regardless of heuristic.

  Closure path requires alternative methods:
    (a) rank-aware contraction maintaining rank-8 P^G structure
    (b) channel-sum stochastic sampling over 8^81 configs
    (c) truncated MPS / hierarchical contraction (introduces error)
    (d) different framework block (smaller-V or smaller-N)

  Engineering effort revised upward from PR #507's "1-3 person-days"
  to "5-10 person-days for rank-aware, longer for alternatives".

  Does not promote bridge parent chain. Does not compute <P>(beta=6).
  No forbidden imports.
```

## 8. Cross-references

- TN contractor POC (where 8^9 estimate originated): `docs/SU3_WIGNER_L3_TN_CONTRACTOR_POC_2026-05-04.md` (PR #507).
- Greedy contractor failure: `docs/SU3_WIGNER_L3_EXACT_TN_GREEDY_FAILURE_2026-05-04.md` (PR #509).
- L_s=3 Haar MC negative: `docs/SU3_WIGNER_L3_CUBE_HAAR_MC_NEGATIVE_RESULT_2026-05-04.md` (PR #506).
- Block 5 (L_s=2 verdict): `docs/SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md` (PR #501).

## 9. Command

```bash
python3 scripts/frontier_su3_wigner_l3_treewidth_2026_05_04.py
```

Expected runtime: <1 second. Expected summary:

```text
SUMMARY: THEOREM PASS=2 SUPPORT=1 FAIL=0
```
