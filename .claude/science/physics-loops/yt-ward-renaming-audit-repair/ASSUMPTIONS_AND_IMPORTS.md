# Assumptions And Imports

## Direct source imports after repair

`yt_ward_identity_derivation_theorem` now seeds these graph dependencies:

| claim_id | audit boundary after pipeline |
|---|---|
| `native_gauge_closure_note` | `claim_type: bounded_theorem`; `audit_status: audited_clean`; `effective_status: retained_bounded` |
| `left_handed_charge_matching_note` | `claim_type: decoration`; `audit_status: audited_decoration`; `effective_status: decoration_under_lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02` |
| `yukawa_color_projection_theorem` | `claim_type: decoration`; `audit_status: audited_decoration`; `effective_status: decoration_under_ew_current_fierz_channel_decomposition_note_2026-05-01` |
| `yt_ew_color_projection_theorem` | `claim_type: positive_theorem`; `audit_status: unaudited`; `effective_status: unaudited` |
| `yt_vertex_power_derivation` | `claim_type: open_gate`; `audit_status: unaudited`; `effective_status: unaudited` |
| `minimal_axioms_2026-04-11` | `claim_type: meta`; `audit_status: unaudited`; `effective_status: meta` |

## Open imports

- The physical readout map from the normalized `H_unit` matrix element to the
  Standard Model top Yukawa remains an identification, not a first-principles
  derivation.
- The common tadpole/readout bridge depends on `YT_VERTEX_POWER_DERIVATION.md`,
  which is still unaudited on the current pipeline surface.
- `YT_EW_COLOR_PROJECTION_THEOREM.md` is also unaudited and therefore blocks
  clean propagation.

## Runner evidence

`python3 scripts/frontier_yt_ward_identity_derivation.py` passes 45 checks and
0 failures. Those checks support the algebraic coefficient surface only.
