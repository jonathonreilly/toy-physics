# SU(3) Wigner Engine Blocks 4+5: L_s=3 Partition Staging + L_s=2 Orientation Diagnostics

**Date:** 2026-05-03
**Claim type:** bounded_theorem
**Status:** bounded support theorem — finite-box engine staging (Block 4) and L_s=2 PBC orientation diagnostics (Block 5), unaudited.

**Scope narrowing 2026-05-16 (science-fix, scope_too_broad repair).** The load-bearing claim is narrowed to the finite combinatorial / algebraic core: Block 4 L_s=3 PBC cube partition staging (trivial sector exact, single-irrep character coefficient, 4-fold Haar singlet basis import, per-plaquette `(8,8,8,8)` cyclical-trace tensor structure, full-cube contraction-scope analysis) and Block 5 L_s=2 PBC orientation diagnostics (all-forward plaquette/link enumeration, standard-Wilson `+d1+d2-d1-d2` link-multiplicity degeneracy at L_s=2 PBC). The bridge-gap closure limb — including the imported P_candidate, the bridge-support target, the epsilon_witness threshold, and the "no L_s=2 PBC convention closes the bridge gap" verdict — is explicitly NOT part of the load-bearing claim; it carries through only conditionally on the unaudited open-gate row (see Section 3.1 and the "Audit-conditional scope narrowing 2026-05-10" subsection at the end of this note).
**Primary runners:**
  - Block 4: `scripts/frontier_su3_wigner_l3_cube_partition.py`
  - Block 5: `scripts/frontier_su3_wigner_l2_cube_orientation_verification.py`
**Engine roadmap:** Blocks 1, 2, 3 are landed in this review-loop path:
[`SU3_WIGNER_INTERTWINER_BLOCK1_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK1_THEOREM_NOTE_2026-05-03.md),
[`SU3_WIGNER_INTERTWINER_BLOCK2_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK2_THEOREM_NOTE_2026-05-03.md),
and [`SU3_WIGNER_INTERTWINER_BLOCK3_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK3_THEOREM_NOTE_2026-05-03.md).

## 0. Headline

This note delivers the **closing pair of blocks** in the SU(3) Wigner-
intertwiner engine campaign that began with Blocks 1-3:

- **Block 4** stages the L_s=3 PBC cube partition function: the trivial
  sector `Z_(0,0)(L=3 cube, beta=6) = c_(0,0)(6)^81` is computed exactly,
  the (1,1) sector character coefficient `c_(1,1)(6)` is computed, the
  Block 2 4-fold Haar singlet basis (rank 8) is rebuilt, the per-
  plaquette tensor structure is encoded, and the FULL 81-link contraction
  scope (worst intermediate ~ 8^9 = 134M complex entries, ~2 GB) is
  documented.

- **Block 5** enumerates the L_s=2 PBC cube plaquette/link structure
  under two natural Wilson plaquette conventions:
  - **All-forward `+d1+d2+d1+d2`:** 12 unique unordered plaquettes,
    24 directed links, each link in exactly 2 plaquettes, index graph
    with 48 nodes / 48 edges / 8 connected components. This enumeration
    is independently recomputed inside the Block 5 runner.
  - **Standard Wilson `+d1+d2-d1-d2`:** exhibits structural link-
    multiplicity degeneracies `{1: 4, 2: 8, 3: 4, 4: 4}` (24 forward
    leg occurrences and 24 backward leg occurrences) that prevent
    direct application of the source-sector factorization at this
    finite volume.

**Narrowed bounded verdict (Block 4 staging + Block 5 orientation
diagnostics):** the finite combinatorial / algebraic Block 4 partition-
staging facts and the L_s=2 PBC orientation/index-graph enumeration are
checkable from the Blocks 1-3 retained packet plus the supplied runners.
This narrowed verdict makes no L_s=2 PBC bridge-gap closure claim.

**Audit-conditional bridge-gap limb (NOT load-bearing here).** The
numerical comparison `|P_all-forward,L=2 - bridge_target|`, the closing
verdict "no L_s=2 PBC convention closes the bridge gap", and the
"L_s ≥ 3 Wigner-Racah work is the next required route" motivation all
rely on imported constants from the unaudited open-gate row
`su3_cube_index_graph_shortcut_open_gate_note_2026-05-03`
(`P_CANDIDATE_REPORTED`, `BRIDGE_SUPPORT_TARGET`, `EPSILON_WITNESS`).
These are reported here for cross-reference only and are NOT part of the
load-bearing audited claim. See Section 3.1 for the per-item conditional
breakdown.

## 1. Block 4 — L_s=3 cube partition function infrastructure

### 1.1 Trivial sector exact

For lambda = (0,0): `chi_(0,0)(U) = 1` for all U. Each plaquette
contributes `c_(0,0)(beta=6)` (Bessel-determinant evaluation); link
integrations give factor 1 (singlet trivial). Total partition:

```text
Z_(0,0)(L=3 cube, beta=6) = c_(0,0)(6)^81
                          = 3.4414403550^81
                          = 2.99 x 10^43.
```

This is the normalization baseline.

### 1.2 (1,1) sector character coefficient

```text
c_(1,1)(beta=6) = 4.4672593754
d_(1,1) = 8
d_(1,1) c_(1,1)(6) = 35.738
c_(1,1)(6) / c_(0,0)(6) = 1.298  (sector ratio)
```

### 1.3 4-fold Haar singlet basis (Block 2 import)

Block 2's Casimir-diagonalization algorithm rebuilt: 8-dimensional
singlet basis of `V_(1,1)^4 = C^4096`, computed in ~60s by simultaneous
diagonalization of total quadratic Casimir on the full 4096 x 4096
Hermitian matrix.

Verified: `singlet_basis.shape == (4096, 8)`, sum of column norms =
8.000000 (orthonormality), rank = 8 (matches Block 2 result).

### 1.4 Per-plaquette tensor structure

The (1,1) plaquette character `chi_(1,1)(U_p) = tr(D(U_l1) D(U_l2)
D(U_l3)^T D(U_l4)^T)` defines a 4-leg tensor in `(8, 8, 8, 8)` shape.
For the cyclical-trace structure with all-(1,1) link assignment, the
tensor's nonzero entries are the 8 diagonal `T[i,i,i,i] = 1` entries,
giving Frobenius norm sqrt(8) = 2.828.

### 1.5 Full-cube contraction scope

For the L_s=3 PBC cube with 81 unique unoriented plaquettes and 81
directed links (each link in 4 plaquettes):

```text
plaquette tensor entries:    81 x 8^4   = 331,776
link projector entries:      81 x 8 x 8^4 (decomposed)  = 2,654,208
total tensor-network state:  ~ 45.6 MB
worst intermediate:          8^9         = 134 M entries (~2 GB)
expected runtime:            10-180 minutes (depends on contraction
                                               order)
```

Without an industrial tensor-network library (opt_einsum or ncon —
neither available in the framework's `numpy + scipy.special` only
environment), the full 81-link contraction is multi-day engineering
(graph partitioning + memory-aware contraction-order optimization).

### 1.6 Block 4 runner output

```text
SUMMARY: THEOREM PASS=5 FAIL=0
```

## 2. Block 5 — L_s=2 cube orientation verification

### 2.1 Two plaquette traversal conventions

On L_s=2 PBC, two natural Wilson plaquette conventions exist:

**Convention 1: all-forward (+d1 +d2 +d1 +d2).** Used by the
framework's candidate runner. Each plaquette traversal closes after
4 forward legs via PBC wraparound. All 4 link matrices appear
un-daggered in the trace. Each unique unordered plaquette uses 4
distinct directed links.

**Convention 2: standard Wilson (+d1 +d2 -d1 -d2).** Standard Wilson
plaquette convention used in continuum QCD. Two forward legs (matrices
appear as `D(U_l)`) and two backward legs (matrices appear as
`D(U_l)^dagger = D(U_l)^T` for the adjoint).

### 2.2 Convention 1 verification (matches candidate)

```text
unique unordered plaquettes:   12
unique directed links:         24
each link in 2 plaquettes:     YES
index identification graph:    48 nodes, 48 edges
connected components:          8
T_(1,1) candidate:             8^(-16) = 4.34 x 10^(-15)
P_candidate(L=2, beta=6):      0.4291049969  (matches reported value)
```

The candidate ansatz `T_lambda = d_lambda^(N_components - N_links) =
d_lambda^(8 - 24) = d_lambda^(-16)` is verified consistent with the
all-forward enumeration's index graph.

### 2.3 Convention 2 — standard Wilson on L_s=2 PBC has degeneracies

```text
unique unordered plaquettes:   12
unique directed links:         20  (NOT 24)
link multiplicities:           {1: 4, 2: 8, 3: 4, 4: 4}
forward leg occurrences:       24
backward leg occurrences:      24
```

The standard Wilson +-+- traversal on L_s=2 PBC produces an irregular
link multiplicity distribution: 4 link IDs appear in only 1 plaquette,
8 appear in 2 plaquettes, 4 appear in 3 plaquettes, and 4 appear in 4
plaquettes. This is because on L_s=2 PBC, the backward legs (-d1, -d2)
can land on either the same forward link (going around the 2-cycle) or
on a different forward link (going forward once vs PBC-wrap), depending
on the start site.

This **structural degeneracy of the standard Wilson convention at
L_s=2 PBC** prevents direct application of the source-sector
factorization (which assumes uniform link multiplicity for the cube
graph trace). The L_s=2 lattice is intrinsically too small to host the
standard Wilson convention cleanly.

### 2.4 P-value comparison

Both conventions, when their compatible source-sector factorization is
applied, give:

```text
P_all-forward (this Block, matches candidate):      0.4291049969
P_standard-Wilson (this Block, deg. structure):     not directly comparable
P_triv (rho = delta, existing reference):           0.4225317396
P_loc (rho = 1, existing reference):                0.4524071590
bridge-support target:                              0.5935306800
epsilon_witness:                                    3.030e-04
```

```text
|P_all-forward - target| = 0.1644 = 543 x epsilon_witness
```

### 2.5 Block 5 runner output

```text
SUMMARY: THEOREM PASS=4 SUPPORT=1 FAIL=0
```

## 3. Combined theorem statement (narrowed 2026-05-16)

**Bounded support theorem (narrowed, SU(3) Wigner-Racah engine Blocks
4+5).** The runners
`scripts/frontier_su3_wigner_l3_cube_partition.py` and
`scripts/frontier_su3_wigner_l2_cube_orientation_verification.py`
deliver the following load-bearing facts (each independently checkable
from the Blocks 1-3 retained packet plus pure `numpy + scipy.special`):

(a) The L_s=3 PBC cube partition function trivial sector
`Z_(0,0)(L=3 cube, beta=6) = c_(0,0)(6)^81 = 2.99 x 10^43` exactly, the
(1,1) sector character coefficient `c_(1,1)(beta=6) = 4.467`, the
4-fold Haar singlet basis of `V_(1,1)^4` (rank 8, dim 4096), and the
per-plaquette `(8,8,8,8)` cyclical-trace tensor;

(b) The L_s=3 contraction-scope analysis: 81 plaquettes × 81 links,
worst intermediate 8^9 ~ 2 GB, expected runtime 10-180 minutes with
a memory-aware contraction-order optimizer (not available within the
`numpy + scipy.special` only constraint); the full L_s=3 contraction
is explicitly deferred and out of audited scope;

(c) The all-forward L_s=2 PBC plaquette enumeration recomputed inside
the Block 5 runner: 12 unique unordered plaquettes, 24 unique directed
links, each link in exactly 2 plaquettes, index graph with 48 nodes /
48 edges / 8 connected components;

(d) The structural finding that the **standard Wilson +d1+d2-d1-d2
plaquette convention has degenerate link multiplicities
`{1: 4, 2: 8, 3: 4, 4: 4}` on L_s=2 PBC**, preventing direct
application of the source-sector factorization at that finite volume.

**Narrowed verdict (load-bearing here):** the Block 1-4 partition-
staging infrastructure (CG decomposition, 4-fold Haar projector, L_s=3
cube geometry, partition staging) plus the Block 5 L_s=2 PBC
orientation/index-graph diagnostics form a consistent finite
combinatorial / algebraic core. This narrowed verdict makes no
bridge-gap closure claim; in particular it does NOT claim that "no
L_s=2 PBC convention closes the bridge gap" and does NOT load-bear on
the "L_s ≥ 3 Wigner-Racah work is the next required route" motivation
beyond the engineering-cost statement in (b).

### 3.1 Audit-conditional bridge-gap limb (NOT load-bearing)

The following items rely on numerical constants imported from the
unaudited open-gate row
`su3_cube_index_graph_shortcut_open_gate_note_2026-05-03`
(`P_CANDIDATE_REPORTED = 0.4291049969`,
`BRIDGE_SUPPORT_TARGET = 0.5935306800`,
`EPSILON_WITNESS = 3.03e-4`,
`P_TRIV_REFERENCE`, `P_LOC_REFERENCE`). They are recorded here for
cross-reference only; they are NOT promoted by this note's narrowed
audit scope and they carry the open-gate conditional until that row is
itself audited:

(e-conditional) The numerical equality `P_all-forward(L=2) = 0.4291049969`
(re-used as the imported `P_CANDIDATE_REPORTED`; independent computation
of the Perron value lives in the open-gate row's runner, not in the
Block 5 runner).

(f-conditional) The numerical comparison `|P_all-forward,L=2 -
bridge_target| = 0.16 = 543 x epsilon_witness`, which depends on
imported `BRIDGE_SUPPORT_TARGET` and `EPSILON_WITNESS`.

(g-conditional) The closing verdict "no L_s=2 PBC convention closes
the gauge-scalar temporal observable bridge gap" and the motivational
statement that "L_s ≥ 3 Wigner-Racah engine work is the next required
route", both of which carry the open-gate conditional via (f).

## 4. Scope

### 4.1 In scope (this PR, narrowed 2026-05-16)

- L_s=3 cube partition function trivial-sector exact, (1,1)-sector
  character coefficient, 4-fold Haar singlet basis import, plaquette
  tensor structure, full-cube contraction-scope analysis (Block 4).
- L_s=2 PBC cube orientation/index-graph enumeration: all-forward
  convention `+d1+d2+d1+d2` recomputed by the Block 5 runner (12
  plaquettes, 24 directed links, 48-node index graph with 8 connected
  components); standard Wilson `+d1+d2-d1-d2` convention exhibits link-
  multiplicity degeneracies `{1: 4, 2: 8, 3: 4, 4: 4}` at L_s=2 PBC
  (Block 5).

### 4.1.1 Explicitly NOT in scope of the narrowed claim

- Any verdict that "no L_s=2 PBC convention closes the bridge gap".
  This relies on imported open-gate constants (see Section 3.1) and is
  not load-bearing here.
- The numerical equality `P_all-forward(L=2) = 0.4291049969` and the
  bridge-gap inequality `|P_all-forward,L=2 - bridge_target| =
  543 x epsilon_witness`. Both re-use imported constants and are
  reported for cross-reference only.

### 4.2 Out of scope

- The full 81-link L_s=3 cube contraction (multi-day to multi-week
  engineering): the partition function staging is in scope here; the
  full contraction itself is reserved for a future engineering PR with
  proper memory-aware contraction-order optimization (or a tensor-
  network library like opt_einsum).
- Closing of the gauge-scalar temporal observable bridge: this PR
  does NOT close the bridge no-go. It identifies the L_s ≥ 3 path as
  the genuine route.

### 4.3 Not making the following claims

- This PR does NOT promote the gauge-scalar bridge parent theorem.
- This PR does NOT compute or constrain `<P>(beta=6)` for the
  thermodynamic-limit Wilson plaquette.
- This PR does NOT use any forbidden imports (no fitted `beta_eff`,
  no PDG/lattice MC plaquette as derivation input, no perturbative
  beta-function shortcut).

## 5. Audit consequence

```yaml
claim_id: su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03
note_path: docs/SU3_WIGNER_INTERTWINER_BLOCK4_BLOCK5_THEOREM_NOTE_2026-05-03.md
runner_paths:
  - scripts/frontier_su3_wigner_l3_cube_partition.py
  - scripts/frontier_su3_wigner_l2_cube_orientation_verification.py
claim_type: bounded_theorem
intrinsic_status: unaudited
deps:
  - su3_wigner_intertwiner_block1_theorem_note_2026-05-03  # PR #495
  - su3_wigner_intertwiner_block2_theorem_note_2026-05-03  # PR #498
  - su3_wigner_intertwiner_block3_theorem_note_2026-05-03  # PR #499
  - gauge_scalar_temporal_observable_bridge_no_go_theorem_note_2026-05-03
  - su3_cube_index_graph_shortcut_open_gate_note_2026-05-03
verdict_rationale_template: |
  Bounded support theorem (narrowed 2026-05-16): Block 4 L_s=3 PBC
  cube partition staging plus Block 5 L_s=2 PBC orientation/index-
  graph diagnostics. Does NOT load-bear on any bridge-gap closure
  conclusion or the "no L_s=2 PBC convention closes the bridge gap"
  verdict; those are split out as an explicit audit-conditional limb
  carrying the open-gate row's conditional (see Section 3.1).

  Block 4 (L_s=3 PBC cube partition staging, load-bearing):
  trivial sector Z_(0,0)(L=3, beta=6) = c_(0,0)(6)^81 EXACT, (1,1)
  sector character coefficient c_(1,1)(6) computed, 4-fold Haar
  singlet basis of V^4 rank 8 verified (Block 2 algorithm), per-
  plaquette (8,8,8,8) tensor structure encoded, full-cube contraction
  scope analysis (worst intermediate 2 GB at 8^9; full contraction
  deferred). 5/5 PASS, 0 FAIL.

  Block 5 (L_s=2 PBC cube orientation/index-graph diagnostics,
  load-bearing core only): all-forward `+d1+d2+d1+d2` plaquette/link
  enumeration recomputed inside the runner (12 plaquettes, 24
  directed links, 48-node index graph with 8 connected components).
  Standard Wilson `+d1+d2-d1-d2` traversal at L_s=2 PBC verified to
  have degenerate link multiplicities {1:4, 2:8, 3:4, 4:4},
  preventing direct application of source-sector factorization at
  that finite volume. Combinatorial / algebraic core: 4/4 PASS,
  1 SUPPORT, 0 FAIL.

  Audit-conditional limb (NOT load-bearing here): the P_candidate
  value 0.4291049969, the bridge-support target 0.5935306800, the
  epsilon_witness 3.03e-4, and the closing "no L_s=2 PBC convention
  closes the bridge gap" verdict are imported from / depend on the
  unaudited open-gate row
  su3_cube_index_graph_shortcut_open_gate_note_2026-05-03 and are
  recorded here for cross-reference only.

  This PR does not close or promote the gauge-scalar bridge parent
  chain. The cross-reference to the gauge-scalar bridge no-go
  theorem (gauge_scalar_temporal_observable_bridge_no_go_theorem_note_2026-05-03)
  is contextual and not a load-bearing dependency of the narrowed
  claim.

  No forbidden imports (numpy + scipy.special only).
```

## 6. Cross-references

- Engine roadmap blocks (preceding):
  [`SU3_WIGNER_INTERTWINER_BLOCK1_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK1_THEOREM_NOTE_2026-05-03.md),
  [`SU3_WIGNER_INTERTWINER_BLOCK2_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK2_THEOREM_NOTE_2026-05-03.md),
  and [`SU3_WIGNER_INTERTWINER_BLOCK3_THEOREM_NOTE_2026-05-03.md`](SU3_WIGNER_INTERTWINER_BLOCK3_THEOREM_NOTE_2026-05-03.md).
- Open gate context, not a load-bearing dependency:
  `SU3_CUBE_INDEX_GRAPH_SHORTCUT_OPEN_GATE_NOTE_2026-05-03.md` — the
  candidate ansatz is verified consistent with the all-forward
  index graph. The "open gate" remains open for the standard Wilson
  convention (which requires L_s ≥ 3 to escape the L_s=2 degeneracies).
- Bridge no-go context, not a load-bearing dependency:
  `GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`
  — Block 5 verdict aligns with the no-go's identification of L_s ≥ 3
  data as the necessary additional primitive.

## 7. Commands

```bash
python3 scripts/frontier_su3_wigner_l3_cube_partition.py
python3 scripts/frontier_su3_wigner_l2_cube_orientation_verification.py
```

Expected summaries:

```text
SUMMARY: THEOREM PASS=5 FAIL=0
SUMMARY: THEOREM PASS=4 SUPPORT=1 FAIL=0
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- `su3_cube_index_graph_shortcut_open_gate_note_2026-05-03` (open-gate
  cross-reference — body explicitly disclaims this as a load-bearing
  dependency at section 6; backticked to avoid length-3 cycle through
  the gauge-vacuum-plaquette tensor-transfer Perron-solve note)

## Audit-conditional scope narrowing 2026-05-10

The 2026-05-08 audit pass on this row recorded
`audited_conditional` (verdict by
`codex-audit-loop-gpt55-xhigh-019e056f-ff7e-78b0-bbfe-9ff7a3d79555`,
load-bearing step class B) with the explicit repair target:

> `missing_dependency_edge`: provide the Block 5 runner source/stdout
> and retained packet entries for the L_s=2 candidate ansatz plus
> bridge target/epsilon witness, or **narrow this claim to Block 4
> staging only**.

This subsection takes the second branch of the auditor's repair
directive — narrowing the audited scope — without modifying the
audit JSON or the load-bearing step class. It is additive
cite-chain hygiene only.

### Imported numerics declared (Block 5 runner)

The Block 5 runner
`scripts/frontier_su3_wigner_l2_cube_orientation_verification.py`
declares these numerical constants at module scope (lines 39-43):

- `EPSILON_WITNESS = 3.03e-4`
- `BRIDGE_SUPPORT_TARGET = 0.5935306800`
- `P_CANDIDATE_REPORTED = 0.4291049969`
- `P_TRIV_REFERENCE = 0.4225317396`
- `P_LOC_REFERENCE = 0.4524071590`

None of these values is computed inside the Block 5 runner. They are
imported from the unaudited `open_gate` row
`su3_cube_index_graph_shortcut_open_gate_note_2026-05-03` (current
ledger `intrinsic_status: unaudited`,
`note_path: docs/SU3_CUBE_INDEX_GRAPH_SHORTCUT_OPEN_GATE_NOTE_2026-05-03.md`).
The L_s=2 candidate ansatz `T_lambda = d_lambda^(-16)` and the
all-forward index-graph component count `N_components = 8` ARE
recomputed by the Block 5 runner; the numerical bridge target
`0.5935...`, the witness threshold `epsilon_witness = 3.03e-4`, and
the reported candidate Perron value `0.4291049969` are all imported.

### Audit-conditional core (retained for re-audit)

For the next re-audit cycle, the load-bearing scope of this row is
narrowed to the following finite combinatorial / algebraic claims,
which are independently checkable from the Blocks 1-3 retained
packet plus pure `numpy + scipy.special`:

**Block 4 staging core (retained for re-audit):**

1. The trivial-sector exact identity
   `Z_(0,0)(L=3 cube, beta=6) = c_(0,0)(6)^81` for the L_s=3 PBC
   cube, with `c_(0,0)(6) = 3.4414403550` computed from the Wilson
   character coefficient Bessel-determinant evaluation.

2. The single-irrep coefficient `c_(1,1)(6) = 4.4672593754` and the
   sector ratio `c_(1,1)(6) / c_(0,0)(6) = 1.298`, computed by the
   same Bessel-determinant scheme.

3. The 4-fold Haar singlet basis of `V_(1,1)^4 = C^4096` rebuilt by
   Block 2's Casimir simultaneous-diagonalization algorithm to rank
   8, with `singlet_basis.shape == (4096, 8)`, sum of column norms =
   8.000000, rank = 8.

4. The per-plaquette `(1,1)` cyclical-trace tensor structure as a
   `(8, 8, 8, 8)`-shape leg tensor with the documented Frobenius
   norm `sqrt(8)`.

5. The L_s=3 contraction-scope analysis: `81` plaquettes x `81`
   directed links, worst intermediate `8^9 = 134M` complex entries
   (~2 GB), expected runtime 10-180 minutes with a memory-aware
   contraction-order optimizer. The full L_s=3 cube contraction is
   explicitly deferred and out of audited scope.

**Block 5 orientation diagnostics core (retained for re-audit):**

6. The all-forward L_s=2 PBC plaquette enumeration: 12 unique
   unordered plaquettes, 24 unique directed links, each link in
   exactly 2 plaquettes, index graph (48 nodes, 48 edges, 8
   connected components).

7. The structural finding that the standard Wilson `+d1+d2-d1-d2`
   plaquette traversal at L_s=2 PBC has degenerate link
   multiplicities `{1: 4, 2: 8, 3: 4, 4: 4}` (24 forward leg
   occurrences and 24 backward leg occurrences), preventing direct
   application of the source-sector factorization that assumes
   uniform multiplicity.

### Audit-conditional limb (carries through with explicit conditional)

The following inferences carry through the run only conditionally on
the unaudited open-gate row
`su3_cube_index_graph_shortcut_open_gate_note_2026-05-03`. They are
NOT in the narrowed re-audit scope above:

- The numerical equality
  `P_all-forward(L=2) = 0.4291049969` (the runner re-uses the
  imported `P_CANDIDATE_REPORTED`; an independent computation of the
  Perron value is in the open-gate row's runner, not in the Block 5
  runner).

- The bridge-gap inequality
  `|P_all-forward(L=2) - 0.5935306800| = 0.16 = 543 x 3.03e-4`,
  because both the bridge-support target and the witness threshold
  are imported.

- The closing verdict that "no L_s=2 PBC convention closes the
  bridge gap" (this carries the same conditional, since it relies on
  the imported bridge target and witness).

### Effective-status read

Until the open-gate row
`su3_cube_index_graph_shortcut_open_gate_note_2026-05-03` is itself
audited (or replaced by a retained authority for the L_s=2
all-forward Perron value plus a retained authority for
`BRIDGE_SUPPORT_TARGET` and `EPSILON_WITNESS`), the effective status
of this row remains `audited_conditional`. The narrowed Block 4
staging + Block 5 orientation-diagnostics core (claims 1-7 above) is
checkable from the retained Blocks 1-3 packet plus the supplied
runners; the bridge-gap limb carries the open-gate conditional.

This subsection is informational reuse-discipline only; it does not
promote the audit verdict, does not alter the recorded
`load_bearing_step_class: B`, and does not amend the audit JSON
ledger.
- `su3_cube_index_graph_shortcut_open_gate_note_2026-05-03`
  (`SU3_CUBE_INDEX_GRAPH_SHORTCUT_OPEN_GATE_NOTE_2026-05-03.md`; context-only
  open-gate reference, not a load-bearing dependency of the narrowed claim)
