# Quark Lane 3 Stuck Fan-Out Synthesis

**Date:** 2026-04-28
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).

**Status:** support / exact current-bank synthesis / no-route-passes boundary for Lane 3.
This block-13 artifact is the required stuck fan-out after the deep 3B/3C
RPSR work. It does not claim retained `m_u`, `m_d`, `m_s`, `m_c`, or `m_b`,
and it does not claim that no future theorem can exist. It records that no
route currently passes without adding new theorem content.

**Primary runner:**
`scripts/frontier_quark_lane3_stuck_fanout_synthesis.py`

## 1. Question

After blocks 01 through 12, the loop has exact support and exact boundaries
for:

1. one-Higgs gauge selection;
2. CKM as mixing rather than mass singular values;
3. Route-2 endpoint/readout support;
4. down-type `5/6` scale selection;
5. `S_3` and oriented `C3[111]` generation Ward carriers;
6. `C3` circulant/A1/P1 readout support;
7. STRC/RPSR up-amplitude support;
8. RPSR single-scalar and RPSR+C3 joint readout rank boundaries.

This block asks:

```text
Does any current-bank route now reach retained non-top quark masses, or does
every orthogonal frame require new source/readout theorem content?
```

## 2. Fan-Out Frames

The synthesis checks six frames.

| Frame | Current-bank result | Reopen condition |
|---|---|---|
| Gauge/operator | one-Higgs selection gives the SM Dirac operator skeleton but leaves generation matrices free | species-differentiated Ward/source theorem |
| Ward-normalization | top Ward is top-channel scoped; species-uniform reuse fails | non-top Ward primitive or sector bridge |
| CKM/singular-value | CKM atlas supplies mixing, not quark Yukawa singular values | retained mass-basis bridge |
| Endpoint/source | Route-2 and `R_conn` support are exact, but the source-domain edge is missing | typed Route-2 source theorem |
| C3/RPSR readout | C3 represents the two-ratio surface and RPSR supplies one scalar, but no coefficient/readout law exists | C3 coefficient law, channel assignment, two-ratio readout |
| Down-type NP/scale | exact `5/6 = C_F - T_F` plus the strong threshold match is not a scale theorem | non-perturbative exponentiation plus scale-selection/RG transport |

## 3. Typed-Edge Synthesis

The current support graph has exact and retained nodes such as:

```text
one_Higgs_gauge_selection
CKM_atlas
top_Ward_anchor
Route2_endpoint_support
R_conn_8_9
C3_Fourier_carrier
RPSR_reduced_amplitude
five_sixths_Casimir
```

but it has no current typed path to:

```text
retained_non_top_quark_masses.
```

Adding one or more of the missing theorem edges would reopen the lane:

```text
C3_coefficient_source_law
physical_channel_assignment
two_ratio_readout
five_sixths_NP_scale_theorem
Route2_source_domain_bridge
species_differentiated_non_top_Ward
```

Those edges are not latent in the current support bank. They are exactly the
human-science theorem content that remains open.

## 4. Theorem

**Theorem (Lane 3 current-bank stuck fan-out).** Under the assumptions and
imports recorded in the Lane 3 loop pack after blocks 01 through 12, no
current typed route reaches retained non-top quark masses. Each orthogonal
fan-out frame terminates at a named missing theorem edge. Therefore the
best honest status is open, with retained closure withheld.

This is not a theorem that future Lane 3 closure is impossible. It is a
current-bank exhaustion result: the next retained movement requires a new
source/readout theorem, not another promotion of existing support.

## 5. Stop Implication

This synthesis justifies a supervisor stop for human science judgment if no
new theorem premise is being added in the current run:

```text
all viable current-bank routes are blocked after deep-work and fan-out;
the remaining progress requires choosing or deriving new theorem content.
```

## 6. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_lane3_stuck_fanout_synthesis.py
```

Expected result:

```text
TOTAL: PASS=68, FAIL=0
VERDICT: no current-bank Lane 3 route reaches retained non-top masses; new
source/readout theorem content is required.
```


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [staggered_dirac_realization_gate_note_2026-05-03](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
- [sm_one_higgs_yukawa_gauge_selection_theorem_note_2026-04-26](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md)
- [quark_lane3_bounded_companion_retention_firewall_note_2026-04-27](QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md)
- [quark_route2_source_domain_bridge_no_go_note_2026-04-28](QUARK_ROUTE2_SOURCE_DOMAIN_BRIDGE_NO_GO_NOTE_2026-04-28.md)
- [quark_five_sixths_scale_selection_boundary_note_2026-04-28](QUARK_FIVE_SIXTHS_SCALE_SELECTION_BOUNDARY_NOTE_2026-04-28.md)
- [quark_generation_equivariant_ward_degeneracy_no_go_note_2026-04-28](QUARK_GENERATION_EQUIVARIANT_WARD_DEGENERACY_NO_GO_NOTE_2026-04-28.md)
- [quark_c3_oriented_ward_splitter_support_note_2026-04-28](QUARK_C3_ORIENTED_WARD_SPLITTER_SUPPORT_NOTE_2026-04-28.md)
- [quark_rpsr_c3_joint_readout_rank_boundary_note_2026-04-28](QUARK_RPSR_C3_JOINT_READOUT_RANK_BOUNDARY_NOTE_2026-04-28.md)
