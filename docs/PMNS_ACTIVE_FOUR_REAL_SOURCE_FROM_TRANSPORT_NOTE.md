# PMNS Active Four-Real Source From Transport

**Status:** open - open or unresolved claim state
## Question
Once the active transport / response profile is derived at lower level, does the
remaining four-real active orbit-breaking source still need a separate theorem
object?

## Exact Result
No.

The non-averaged lower-level active transport / response profile determines the
active block exactly. From that active block:

- `xbar` is read from the `C3`-even diagonal mean
- `sigma` is read from the forward-cycle complex mean
- the residual active source is exactly the four-real vector

`(xi_1, xi_2, rho_1, rho_2)`

with:

- `xi_3 = -xi_1 - xi_2`
- `rho_3 = -rho_1 - rho_2`

So the active block rebuilds exactly from:

- `xbar`
- `sigma`
- `(xi_1, xi_2, rho_1, rho_2)`

Therefore the four-real source is no longer an extra unresolved object on the
lower-level active transport chain. It is just the centered non-averaged part
of the active transport profile.

## Boundary
This does not yet derive the lower-level active transport / response profile
itself from `Cl(3)` on `Z^3` alone. It only closes the residual four-real source
once that lower-level active profile is genuinely available.

## Runner

```bash
PYTHONPATH=scripts python3 scripts/frontier_pmns_active_four_real_source_from_transport.py
```

Last run (2026-05-10): `PASS=7 FAIL=0` on the present worktree. The
runner exercises three parts: (Part 1) non-averaged transport
recovers the active block exactly via
`derive_active_block_from_response_columns` then re-derives the
four-real source `(xi_1, xi_2, rho_1, rho_2)`; (Part 2) the centered
4-real readout matches the direct active-block readout; (Part 3) a
circularity guard verifies the lower-level active derivation function
takes no PMNS-side target values as inputs (the function signature is
checked against the banned-input set
`{d0_trip, dm_trip, delta_d_act, diag_a_pq, m_r}`).

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream authority
candidates the load-bearing transport-profile premise relies on, in
response to the 2026-05-05 audit verdict's `missing_bridge_theorem`
repair target (audit row:
`pmns_active_four_real_source_from_transport_note`). It does not
promote this note or change the audited claim scope, which remains the
conditional algebraic readout that, given a genuinely available
non-averaged lower-level active transport / response profile, the
residual four-real active source is determined by the active block
decomposition.

One-hop authority candidates cited:

- [`PMNS_LOWER_LEVEL_END_TO_END_CLOSURE_NOTE.md`](PMNS_LOWER_LEVEL_END_TO_END_CLOSURE_NOTE.md)
  — currently `audited_conditional` (audit row:
  `pmns_lower_level_end_to_end_closure_note`). Sibling note in the
  same lower-level PMNS cluster whose runner
  (`frontier_pmns_lower_level_end_to_end_closure.py`) supplies the
  active/passive response columns and the corresponding
  `derive_active_block_from_response_columns` reconstruction map.
  Both rows share the `pmns_lower_level_utils.py` helper module and
  the same fixed-input `BANNED_INPUT_NAMES` circularity guard. Because
  this sibling authority is itself `audited_conditional`, the present
  note's effective status is capped at `audited_conditional` under the
  standard cite-chain rule.
- [`PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md`](PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md)
  — currently `audited_renaming` (audit row:
  `pmns_corner_transport_active_block_note`). Adjacent PMNS active-block
  transport candidate authority in the same lower-level cluster. Because
  this candidate is `audited_renaming` rather than retained, it does not
  by itself promote the upstream premise to retained-grade.

Open class D registration targets named by the 2026-05-05 audit verdict
as `missing_bridge_theorem`:

- The non-averaged lower-level active transport / response profile is
  imported as a premise. Closing it requires a retained source note or
  authority deriving that active transport profile from `Cl(3)` on `Z^3`
  alone (the note's "Boundary" section explicitly flags this as the
  remaining sole-axiom gap). The 2026-05-05 audit verdict's
  `notes_for_re_audit_if_any` field names this as
  `missing_bridge_theorem: provide the theorem or retained authority
  deriving the lower-level active transport/response profile and the
  precise active-block readout map`.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with
load-bearing-step class A and `chain_closes=False`, observing that the
algebraic readout is plausible as a conditional decomposition but the
restricted packet provides no derivation or retained authority for the
lower-level active transport / response profile itself. The audit ledger
records `runner_path: None` for this row because the audit was performed
on the text-only restricted packet. The runner
`scripts/frontier_pmns_active_four_real_source_from_transport.py` exists
in the repository and verifies the conditional readout (PASS=7 FAIL=0
on 2026-05-10), but its checks are class A finite-dimensional algebra
on the active-block decomposition `(xbar, sigma, xi_1, xi_2, rho_1,
rho_2)`, not first-principles derivations from the sole axiom. The cite
chain above wires the two adjacent lower-level PMNS authorities and
explicitly registers the missing transport-profile bridge theorem as an
open class D registration target. Effective status remains
`audited_conditional`. The note's `audit_status` is unchanged by this
addendum.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) plus class D
(open-target registration). It does not change any algebraic content,
runner output, or load-bearing step classification. It records the
upstream authority candidates the audit verdict expected, the runner
that exercises the conditional readout, and the missing-bridge-theorem
target named by the verdict's `notes_for_re_audit_if_any` field. It
mirrors the live cite-chain pattern used by the
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md` cluster
(commit `8e84f0c23`).
