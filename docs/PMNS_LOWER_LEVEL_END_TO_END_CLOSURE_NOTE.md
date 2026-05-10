# PMNS Lower-Level End-to-End Closure

**Status:** support - structural or confirmatory support note
Starting from lower-level observable packs only:

- active/passive response columns on the retained lepton supports

the lane reconstructs:

- `tau`
- `q`
- passive block and `a_i`
- active block and full active coordinates
- `(D_0^trip, D_-^trip)`
- branch
- sheet
- `H_nu`, `H_e`
- masses
- PMNS

The runner contains a circularity guard: no target PMNS objects appear as
inputs.

## Runner

```bash
PYTHONPATH=scripts python3 scripts/frontier_pmns_lower_level_end_to_end_closure.py
```

Last run (2026-05-10): `PASS=26 FAIL=0` on the present worktree. The
runner exercises three sample patches (`neutrino-active-on-seed`,
`neutrino-active-off-seed`, `charged-lepton-active-off-seed`) plus an
aligned-seed degenerate patch where H-level closure is the invariant
target. For each non-degenerate sample it verifies: circularity guard
passes (no target PMNS values consumed), derived `(D_0^trip, D_-^trip)`
pair matches the reference pair to 1e-12, branch matches, passive offset
and coefficient data `q, a` match to 1e-12, `H_nu` and `H_e` match to
1e-12, masses match to 1e-10, the absolute-value PMNS matrix matches to
1e-10, and the sheet matches.

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream
dependencies the runner imports, in response to the 2026-05-05 audit
verdict's `missing_dependency_edge` repair target (audit row:
`pmns_lower_level_end_to_end_closure_note`). It does not promote this
note or change the audited claim scope, which remains the conditional
end-to-end reconstruction from lower-level active/passive response
columns to PMNS through the documented intermediate objects.

One-hop authority candidate cited:

- [`PMNS_ACTIVE_FOUR_REAL_SOURCE_FROM_TRANSPORT_NOTE.md`](PMNS_ACTIVE_FOUR_REAL_SOURCE_FROM_TRANSPORT_NOTE.md)
  — currently `audited_conditional` (audit row:
  `pmns_active_four_real_source_from_transport_note`). Sibling note in
  the same lower-level PMNS cluster whose decomposition supplies the
  active-block readout `(xbar, sigma, xi_1, xi_2, rho_1, rho_2)` used
  by the present runner's `derive_active_block_from_response_columns`
  call. Because this sibling authority is itself `audited_conditional`,
  the present note's effective status is capped at `audited_conditional`
  under the standard cite-chain rule.

Open class D registration targets named by the 2026-05-05 audit verdict
as `missing_dependency_edge`:

- The `pmns_lower_level_utils.py` helper module supplies the load-bearing
  reconstruction primitives `active_response_columns_from_sector_operator`,
  `passive_response_columns_from_sector_operator`,
  `derive_active_block_from_response_columns`,
  `derive_passive_block_from_response_columns`,
  `classify_tau_and_q_from_response_columns`,
  `effective_block_from_sector_operator`,
  `sector_operator_fixture_from_effective_block`,
  `recover_passive_coeffs`, `masses_and_pmns_from_pair`, plus the
  `BANNED_INPUT_NAMES` circularity guard set
  `{d0_trip, dm_trip, delta_d_act, diag_a_pq, m_r}`. There is no
  dedicated retained audit-clean source note registered as a one-hop
  authority for this helper module's lattice identities.
- The lower-level observable-pack authority — i.e. a retained source
  note proving that the active/passive response columns on the retained
  lepton supports are themselves derivable from `Cl(3)` on `Z^3` alone —
  is imported as a premise rather than registered as an upstream
  retained authority.

The two open class D items together match the 2026-05-05 audit
verdict's `notes_for_re_audit_if_any` field:
"provide the retained lower-level observable-pack authority and a
runner or proof showing each reconstruction step through PMNS without
importing target PMNS objects."

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with
load-bearing-step class B and `chain_closes=False`, observing that the
note asserts an end-to-end reconstruction but the restricted packet
contains no derivation, runner source, or stdout. The audit ledger
records `runner_path: None` for this row because the audit was
performed on the text-only restricted packet. The runner
`scripts/frontier_pmns_lower_level_end_to_end_closure.py` exists in the
repository and verifies each reconstruction step end-to-end (PASS=26
FAIL=0 on 2026-05-10), but its checks are class B closure-of-package
algebra given the retained lepton supports and the
`pmns_lower_level_utils.py` reconstruction primitives. The cite chain
above wires the adjacent active-source sibling and registers both
helper-module and lower-level-observable-pack authority as open class D
registration targets. Effective status remains `audited_conditional`.
The note's `audit_status` is unchanged by this addendum.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) plus class D
(open-target registration). It does not change any algebraic content,
runner output, or load-bearing step classification. It records the
upstream authority the audit verdict expected, the runner that
exercises each reconstruction step, and the helper-module and
observable-pack authority targets named by the verdict's
`notes_for_re_audit_if_any` field. It mirrors the live cite-chain
pattern used by the
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md` cluster
(commit `8e84f0c23`).
