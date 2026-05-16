# PMNS Graph-First Axis Alignment

**Claim type:** bounded_theorem
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
in response to prior 2026-05-05 audit feedback identifying a
`missing_bridge_theorem` repair target for audit row
`pmns_graph_first_axis_alignment_note`. It does not promote this note
or change the claim scope, which
remains the conditional bounded conclusion that the defined `hw=1`
cube-shift selector has coordinate-axis minima with residual `Z_2` and
that imposing the corresponding `P_23` residual symmetry yields the
aligned Hermitian core form.

One-hop authority candidates cited:

- [`PMNS_GRAPH_AXIS_TO_ACTIVE_LANE_BRIDGE_NOTE.md`](PMNS_GRAPH_AXIS_TO_ACTIVE_LANE_BRIDGE_NOTE.md)
  — audit row: `pmns_graph_axis_to_active_lane_bridge_note`. Newly added
  bridge-theorem source authority deriving, on existing repo-canonical
  objects, that the graph-side residual `Z_2` stabilizer of the selected
  `hw=1` cube axis restricts on the `hw=1` carrier `V_1 = span(X_1, X_2, X_3)`
  to the standard permutation matrix `P_23` (after relabeling so the
  selected axis is `e_1`), so that imposing residual-`Z_2` invariance on a
  Hermitian operator `H : V_1 -> V_1` is the identity `P_23 H P_23 = H`
  rather than an extra premise. This is the bridge step named by the prior
  2026-05-11 `missing_bridge_theorem` audit feedback. Runner
  `scripts/frontier_pmns_graph_axis_to_active_lane_bridge.py` exercises the
  six tensor-factor permutation unitaries, their conjugation action on the
  cube-shift triplet, the carrier invariance of `V_1`, the restriction
  identity `T_sigma|_{V_1} = P_sigma`, and the equivalence between
  residual-`Z_2` invariance on `V_1` and `P_23 H P_23 = H` (`PASS=87
  FAIL=0` on the present worktree). Independent audit owns chain impact.
- [`Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`](Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md)
  — audit row:
  `z2_hw1_mass_matrix_parametrization_note`. Sibling source authority
  establishing that every `Z_2`-invariant Hermitian operator
  on the `hw=1` triplet `V_1 = span(X_1, X_2, X_3)` with `Z_2 = <(12)>`
  fixing axis `3` and swapping axes `1, 2` has, in the ordered basis
  `(X_3, X_1, X_2)`, the canonical form
  `M(a,b,c,d) = [[a,d,d*],[d*,b,c],[d*,c,b]]` with `a, b, c in R` and
  `d in C`. This is a one-hop authority on the canonical form for the
  residual-`Z_2`-invariant Hermitian core, of which the present note's
  aligned form `[[a,b,b],[b,c,d],[b,d,c]]` is the special case
  `d in R`. This supplies cited one-hop support on the canonical normal
  form while independent audit decides chain impact.
- [`SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`](SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
  — audit row:
  `site_phase_cube_shift_intertwiner_note`. Sibling source authority on
  the exact intertwiner `Phi^dagger P_mu Phi = S_mu`
  between the abstract taste-cube `C^8` cube-shifts `S_mu` and the
  BZ-corner site-phase operators `P_mu` on the even-periodic lattice,
  supplying the canonical operator-algebra side of the cube-shift
  selector the present note builds on. This supplies cited one-hop
  support while independent audit decides chain impact.
- [`GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md`](GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md)
  — audit row:
  `graph_first_selector_derivation_note`. Sibling bounded-grade source
  authority on the graph-first selector derivation establishing the
  `hw=1` triplet selector apparatus that the present note's cube-shift
  selector instantiates.
- [`PMNS_GRAPH_FIRST_CYCLE_FRAME_SUPPORT_NOTE.md`](PMNS_GRAPH_FIRST_CYCLE_FRAME_SUPPORT_NOTE.md)
  — audit row:
  `pmns_graph_first_cycle_frame_support_note`. Sibling
  source authority on the graph-first cycle frame on which the aligned
  active block lives, supplying the cycle-frame support consistent with
  the present note's aligned core.

Open class D registration targets named by prior 2026-05-05 audit
feedback as `missing_bridge_theorem`:

- The prior feedback notes stated the missing-bridge target
  explicitly: `missing_bridge_theorem: provide a retained theorem
  deriving the map from the selected hw=1 graph axis and its residual
  Z2 stabilizer to mandatory P23 invariance on the active Hermitian
  triplet lane`. The newly added
  [`PMNS_GRAPH_AXIS_TO_ACTIVE_LANE_BRIDGE_NOTE.md`](PMNS_GRAPH_AXIS_TO_ACTIVE_LANE_BRIDGE_NOTE.md)
  source theorem (paired runner
  `scripts/frontier_pmns_graph_axis_to_active_lane_bridge.py`) supplies
  this bridge as an explicit unitary-restriction identity on
  repo-canonical objects, with no new physical premise. Independent
  audit decides whether this source addition lifts the present note's
  effective status; this addendum does not request promotion or
  verdict change.

## Honest auditor read

The independent 2026-05-05 audit on the previous note revision
recorded this row as conditional with load-bearing-step class A and
`chain_closes=False`, observing that the algebraic implication from
imposed `P_23` invariance to `H = [[a,b,b],[b,c,d],[b,d,c]]` closes,
but that the missing step is the bridge justifying why the selected
graph axis must be pushed onto the active Hermitian triplet lane as a
required residual invariance condition rather than an additional
premise. The runner
`scripts/frontier_pmns_graph_first_axis_alignment.py` is registered
with `runner_check_breakdown = {A: 16, B: 0, C: 0, D: 0,
total_pass: 16}` and performs only internal algebraic and
finite-construction checks (`PASS=16 FAIL=0` on 2026-05-10): defining
the selector, sampling and identifying the axis minima, verifying the
residual swap, and checking a preconstructed aligned Hermitian core.
It does not derive the graph-to-active-Hermitian-lane bridge from an
axiom or cited source authority. The cite chain above wires the
`Z_2`-`hw=1` parametrization authority, the cube-shift intertwiner
support, the graph-first selector derivation, and the cycle-frame
support, and explicitly registers the missing-bridge-theorem target
named by the prior feedback notes. After this source edit, the
independent audit lane owns any current verdict and effective status;
this addendum does not request promotion.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) plus class D
(open-target registration). It does not change any algebraic content,
runner output, or load-bearing step classification. It records the
upstream authority candidates the prior feedback requested, the runner
that exercises the conditional axis-alignment derivation, and the
missing-bridge-theorem target named by the prior feedback notes. It
mirrors the live cite-chain
pattern used by the
`PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md` cluster
(commit `44da750e2`) and the
`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` cluster
(commit `8e84f0c23`). Vocabulary is repo-canonical only.
