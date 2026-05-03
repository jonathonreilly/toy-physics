# SU(3) L_s=2 Cube Index-Graph Shortcut Open Gate

**Date:** 2026-05-03
**Claim type:** open_gate
**Status:** open gate, unaudited.
**Primary runner:** `scripts/frontier_su3_cube_index_graph_shortcut_open_gate.py`

## 0. Review Boundary

This note salvages the durable part of PR #492 and rejects the overclaim.

The runner gives a reproducible **candidate shortcut** for the L_s=2 cube:
if every two-link Haar pairing in the nontrivial cube sectors reduces to the
same uniform index-identification trace used by the cyclic graph model, then
the trace factor is

```text
T_lambda(candidate) = d_lambda^(N_components - N_links) = d_lambda^(8 - 24).
```

Under that ansatz, the induced source-sector Perron value is
`P_candidate(6) = 0.4291049969`. This is far below the bridge-support
target `0.5935306800`, so it would not close the gauge-scalar temporal
observable bridge.

The review-loop boundary is stricter:

- the graph count `N_components = 8` is runner-backed;
- the candidate Perron value is runner-backed **conditional on** the
  uniform-pairing ansatz;
- the equality between the real SU(3) nontrivial Wigner/intertwiner traces
  and that uniform graph ansatz is **not proved** here.

Therefore this is an `open_gate`, not a bounded theorem for the actual
cube value and not a parent theorem promotion.

## 1. Setup

The current source-sector bridge writes

```text
T_src(6) = exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)
```

as recorded in
[`GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md)
and used by
[`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md).

The prior cube skeleton
[`SU3_CUBE_PERRON_SOLVE_COMBINED_THEOREM_NOTE_2026-05-03.md`](SU3_CUBE_PERRON_SOLVE_COMBINED_THEOREM_NOTE_2026-05-03.md)
already records the safe structural surface:

- 12 unique unoriented spatial plaquettes on the L_s=2 PBC cube;
- 24 directed links;
- each directed link appears in two plaquettes;
- all link incidences are forward-oriented;
- nontrivial sectors still require explicit SU(3) Wigner/intertwiner traces.

This note tests one proposed way to remove that last blocker.

## 2. Candidate Shortcut

For each plaquette, introduce four cyclic indices. Each link shared by two
plaquettes identifies the incoming cyclic indices and the outgoing cyclic
indices. With 12 plaquettes and 24 links this gives

```text
nodes = 4 * 12 = 48
edges = 2 * 24 = 48
```

The runner computes the connected components of this index graph by
union-find:

```text
N_components = 8.
```

If the relevant SU(3) invariant pairings reduce to this index graph with
one independent color choice per connected component, then

```text
T_lambda(candidate) = (1 / d_lambda)^24 * d_lambda^8
                    = d_lambda^(-16).
```

This step is the open gate. It is automatic for the graph model after the
uniform-pairing ansatz is imposed, but it is not yet a derivation of the
actual nontrivial cube Wigner/intertwiner trace.

## 3. Candidate rho and P

The runner forms a candidate boundary-character profile

```text
rho_candidate_(p,q)(6)
  = (d_(p,q) c_(p,q)(6) / c_(0,0)(6))^12 * d_(p,q)^(-16),
```

normalized by `rho_candidate_(0,0)(6) = 1`.

With `NMAX = 4` for the candidate `rho` and `NMAX = 7` for the existing
source-sector Perron solve, the runner reports:

```text
rho_(1,0)(6) = rho_(0,1)(6) = 2.124624e-01
rho_(1,1)(6) = 5.587932e-03
P_candidate(6) = 0.4291049969
```

Comparison:

| Surface | Value | Status |
|---|---:|---|
| Reference B, `rho = delta` | `0.4225317396` | existing structural reference |
| Candidate shortcut in this note | `0.4291049969` | conditional/open |
| Reference A, `rho = 1` | `0.4524071590` | existing structural reference |
| bridge-support target | `0.5935306800` | comparison target |

The candidate is close to the trivial-sector reference and far from the
bridge-support target.

## 4. Open Gate

To turn this into a bounded theorem for the actual L_s=2 cube, a future
audited note must prove or compute the nontrivial topological traces:

```text
T_(n,n)(cube)
T_(lambda, bar(lambda))(cube)
```

with explicit SU(3) invariant tensors, including the orientation and
normalization conventions. Equivalently, it must show that the actual
Wigner/intertwiner contractions collapse to the uniform index graph used
above.

Until then:

- do not quote `P_candidate(6)` as the actual cube Perron value;
- do not use this row to promote the gauge-scalar bridge parent theorem;
- do use it as a reproducible falsifier for the proposed shortcut if future
  Wigner traces disagree with `d_lambda^(-16)`.

## 5. Validation

Runner command:

```bash
python3 scripts/frontier_su3_cube_index_graph_shortcut_open_gate.py
```

Expected summary:

```text
SUMMARY: OPEN PASS=3 SUPPORT=3 FAIL=0
```

The support lines are intentionally not theorem PASS lines: they depend on
the candidate uniform-pairing ansatz.

## 6. Audit Consequence

```yaml
claim_id: su3_cube_index_graph_shortcut_open_gate_note_2026-05-03
note_path: docs/SU3_CUBE_INDEX_GRAPH_SHORTCUT_OPEN_GATE_NOTE_2026-05-03.md
runner_path: scripts/frontier_su3_cube_index_graph_shortcut_open_gate.py
claim_type: open_gate
intrinsic_status: unaudited
deps:
  - gauge_vacuum_plaquette_source_sector_matrix_element_factorization_note
  - gauge_vacuum_plaquette_tensor_transfer_perron_solve_note
  - su3_cube_perron_solve_combined_theorem_note_2026-05-03
verdict_rationale_template: |
  Open gate for the L_s=2 cube shortcut. The runner verifies the cyclic
  index graph has 48 nodes, 48 identifications, and 8 connected components,
  then computes the conditional candidate P_candidate(6)=0.4291049969
  under the uniform-pairing ansatz T_lambda=d_lambda^(-16). The missing
  step is an explicit SU(3) Wigner/intertwiner trace derivation showing
  that the actual nontrivial cube traces equal the candidate graph trace.
  No bridge closure or parent promotion follows from this row.
```
