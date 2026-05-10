# PMNS Graph-First Axis Alignment

**Status:** bounded - bounded or caveated result note
**Script:** [`frontier_pmns_graph_first_axis_alignment.py`](../scripts/frontier_pmns_graph_first_axis_alignment.py)

## Question

Can a genuinely graph-native selector on the `hw=1` corner triplet derive any
positive PMNS law without returning to the old full microscopic decomposition
route?

## Answer

Yes, partially.

The canonical cube-shift selector on the `hw=1` triplet has exactly three
coordinate-axis minima, each with residual `Z_2` stabilizer. Pushing that
selected axis onto the active Hermitian triplet lane forces the aligned law

`P_23 H P_23 = H`,

and therefore the active aligned Hermitian core

`H = [[a,b,b],[b,c,d],[b,d,c]]`.

## Theorem

**Theorem (graph-first axis alignment).**

On the graph-first `hw=1` route:

1. the normalized cube-shift selector has exactly three axis minima,
2. each selected axis has exact residual `Z_2` stabilizer,
3. residual `Z_2` invariance on the active Hermitian triplet lane forces
   `P_23 H P_23 = H`,
4. hence the active aligned Hermitian core is exactly
   `[[a,b,b],[b,c,d],[b,d,c]]`.

## What This Gives

This is a real positive native law:

- it derives weak-axis selection,
- it derives the aligned active Hermitian grammar,
- it does so from the graph-native `hw=1` corner structure rather than from
  the old PMNS packaging route.

## What It Does Not Yet Give

This route does **not** by itself determine:

- the aligned-core values `(a,b,c,d)`,
- which lepton sector carries the active block,
- the full off-seed microscopic value law.

So it is a positive partial closure route, not full closure.

## Role In The Overall Neutrino Lane

This route shows the microscopic no-go theorem is not saying “nothing further
can be derived natively.” A different native route can still produce genuine
partial laws.

The graph-first route derives:

- axis selection
- alignment

but leaves:

- aligned-core values
- active-sector choice

open.

## Runner

```bash
PYTHONPATH=scripts python3 scripts/frontier_pmns_graph_first_axis_alignment.py
```

Last run (2026-05-10): `PASS=16 FAIL=0` on the present worktree. The
runner exercises class A finite-dimensional algebra: construction of
the normalized cube-shift selector on the `hw=1` triplet, axis-minimum
identification, residual `Z_2` stabilizer verification on each
selected axis, the swap action on the active Hermitian triplet lane,
and explicit construction of the aligned core
`H = [[a,b,b],[b,c,d],[b,d,c]]` consistent with `P_23 H P_23 = H`.

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream authority
candidates the load-bearing axis-to-active-lane bridge step relies on,
in response to the 2026-05-05 audit verdict's `missing_bridge_theorem`
repair target (audit row: `pmns_graph_first_axis_alignment_note`). It
does not promote this note or change the audited claim scope, which
remains the conditional bounded conclusion that the defined `hw=1`
cube-shift selector has coordinate-axis minima with residual `Z_2` and
that imposing the corresponding `P_23` residual symmetry yields the
aligned Hermitian core form.

One-hop authority candidates cited:

- [`Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`](Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md)
  — currently `retained` (audit row:
  `z2_hw1_mass_matrix_parametrization_note`). Sibling retained
  authority establishing that every `Z_2`-invariant Hermitian operator
  on the `hw=1` triplet `V_1 = span(X_1, X_2, X_3)` with `Z_2 = <(12)>`
  fixing axis `3` and swapping axes `1, 2` has, in the ordered basis
  `(X_3, X_1, X_2)`, the canonical form
  `M(a,b,c,d) = [[a,d,d*],[d*,b,c],[d*,c,b]]` with `a, b, c in R` and
  `d in C`. This is a one-hop authority on the canonical form for the
  residual-`Z_2`-invariant Hermitian core, of which the present note's
  aligned form `[[a,b,b],[b,c,d],[b,d,c]]` is the special case
  `d in R`. Under the cite-chain rule a `retained` one-hop authority
  on the canonical normal form supports but does not by itself promote
  the present row, since the bridge from the cube-shift selector axis
  to the active Hermitian triplet lane remains a class A premise.
- [`SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`](SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
  — currently `retained` (audit row:
  `site_phase_cube_shift_intertwiner_note`). Sibling retained
  authority on the exact intertwiner `Phi^dagger P_mu Phi = S_mu`
  between the abstract taste-cube `C^8` cube-shifts `S_mu` and the
  BZ-corner site-phase operators `P_mu` on the even-periodic lattice,
  supplying the canonical operator-algebra side of the cube-shift
  selector the present note builds on. Under the cite-chain rule a
  `retained` one-hop authority on the cube-shift intertwiner supports
  but does not by itself promote the present row.
- [`GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md`](GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md)
  — currently `retained_bounded` (audit row:
  `graph_first_selector_derivation_note`). Sibling bounded-grade
  authority on the graph-first selector derivation establishing the
  `hw=1` triplet selector apparatus that the present note's cube-shift
  selector instantiates.
- [`PMNS_GRAPH_FIRST_CYCLE_FRAME_SUPPORT_NOTE.md`](PMNS_GRAPH_FIRST_CYCLE_FRAME_SUPPORT_NOTE.md)
  — currently `audited_conditional` (audit row:
  `pmns_graph_first_cycle_frame_support_note`). Sibling
  bounded-conditional authority on the graph-first cycle frame on
  which the aligned active block lives, supplying the cycle-frame
  support consistent with the present note's aligned core.

Open class D registration targets named by the 2026-05-05 audit
verdict as `missing_bridge_theorem`:

- A retained source-note theorem deriving the bridge from the selected
  `hw=1` graph axis and its residual `Z_2` stabilizer to mandatory
  `P_23` invariance on the active Hermitian triplet lane remains
  required to lift the bounded-grade alignment conclusion to chain
  closure. The audit verdict's `notes_for_re_audit_if_any` field
  states this explicitly:
  `missing_bridge_theorem: provide a retained theorem deriving the map
  from the selected hw=1 graph axis and its residual Z2 stabilizer to
  mandatory P23 invariance on the active Hermitian triplet lane`.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with
load-bearing-step class A and `chain_closes=False`, observing that the
algebraic implication from imposed `P_23` invariance to
`H = [[a,b,b],[b,c,d],[b,d,c]]` closes, but that the missing step is
the bridge justifying why the selected graph axis must be pushed onto
the active Hermitian triplet lane as a required residual invariance
condition rather than an additional premise. The runner
`scripts/frontier_pmns_graph_first_axis_alignment.py` is registered
with `runner_check_breakdown = {A: 16, B: 0, C: 0, D: 0,
total_pass: 16}` and performs only internal algebraic and
finite-construction checks (`PASS=16 FAIL=0` on 2026-05-10): defining
the selector, sampling and identifying the axis minima, verifying the
residual swap, and checking a preconstructed aligned Hermitian core.
It does not derive the graph-to-active-Hermitian-lane bridge from an
axiom or cited retained authority. The cite chain above wires the
retained `Z_2`-`hw=1` parametrization authority, the retained
cube-shift intertwiner support, the retained graph-first selector
derivation, and the audited-conditional cycle-frame support, and
explicitly registers the missing-bridge-theorem target named by the
verdict's `notes_for_re_audit_if_any` field. Effective status remains
`audited_conditional`. The note's `audit_status` is unchanged by this
addendum.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) plus class D
(open-target registration). It does not change any algebraic content,
runner output, or load-bearing step classification. It records the
upstream authority candidates the audit verdict expected, the runner
that exercises the conditional axis-alignment derivation, and the
missing-bridge-theorem target named by the verdict's
`notes_for_re_audit_if_any` field. It mirrors the live cite-chain
pattern used by the
`PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md` cluster
(commit `44da750e2`) and the
`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` cluster
(commit `8e84f0c23`). Vocabulary is repo-canonical only.
