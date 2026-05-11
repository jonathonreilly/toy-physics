# PMNS `C3` Nontrivial-Character Current Boundary

**Status:** support - structural or confirmatory support note
## Question
Once the retained PMNS lane has been reduced to the native `C3`-character
family, what is the exact smallest remaining sole-axiom source object?

## Answer
It is **one native complex nontrivial-character current**, not a larger value
family.

Let `h_0, h_1, h_2` be the exact native `C3`-character holonomies at phases

```text
0, 2 pi / 3, 4 pi / 3.
```

Define the native current

```text
J_chi(A) := (h_0 + omega h_1 + omega^2 h_2) / 3.
```

On the reduced graph-first PMNS family

```text
A_fwd(u, v, w) = (u + i v) E12 + w E23 + (u - i v) E31
```

one has exactly

```text
J_chi(A_fwd) = chi = u + i v.
```

So the PMNS value-selection problem is not a vague `3`-real problem anymore.
It is exactly the production of one complex native current.

## Boundary
The current exact bank still annihilates this current on every current
sole-axiom retained route:

- the free route
- the sole-axiom `hw=1` source/transfer route
- the retained scalar route

In symbols:

```text
J_chi = 0
```

on all of those routes.

## Consequence
The strongest honest next positive target is now fully explicit:

> derive a sole-axiom law producing nonzero `J_chi` on the retained `hw=1`
> response family.

That is the smallest remaining PMNS-side source object on the current bank.

## Runner

```bash
PYTHONPATH=scripts python3 scripts/frontier_pmns_c3_nontrivial_current_boundary.py
```

Last run (2026-05-10): `PASS=16 FAIL=0` on the present worktree. The
runner exercises five parts: (Part 1) construction of the native C3
character holonomies `h_0, h_1, h_2` at phases `0, 2pi/3, 4pi/3`;
(Part 2) the Fourier-projection identity
`J_chi(A) = (h_0 + omega h_1 + omega^2 h_2) / 3` evaluated on
`A_fwd(u, v, w)` to recover `chi = u + i v`; (Part 3) the
route-annihilation checks `J_chi = 0` on the free, sole-axiom
`hw=1` source/transfer, and cited scalar routes; (Part 4) the
downstream PMNS reduced-data link to `chi`; (Part 5) circularity
guards confirming the native character phases and current take no
PMNS-side target values as inputs.

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream authority
candidates the load-bearing C3 holonomy / route boundary premise
relies on, in response to the 2026-05-05 audit verdict's
`missing_bridge_theorem` repair target (audit row:
`pmns_c3_nontrivial_current_boundary_note`). It does not promote this
note or change the audited claim scope, which remains the conditional
algebraic identification of the smallest remaining sole-axiom source
object as one native complex C3-nontrivial-character current.

One-hop authority candidates cited:

- [`PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE.md`](PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE.md)
  — currently `unaudited` (audit row:
  `pmns_c3_character_holonomy_closure_note`). Sibling support note
  constructing the exact native C3 character holonomies at phases
  `0, 2pi/3, 4pi/3` on the cited `hw=1` triplet via the projected
  forward-cycle matrix `C`. Provides the holonomy readout
  `(h_0, h_1, h_2)` that the present note's Fourier projection
  `J_chi := (h_0 + omega h_1 + omega^2 h_2) / 3` post-composes with.
  Because this sibling is `unaudited`, it does not by itself lift
  the present note's effective status under the cite-chain rule.
- [`PMNS_C3_CHARACTER_MODE_REDUCTION_NOTE.md`](PMNS_C3_CHARACTER_MODE_REDUCTION_NOTE.md)
  — currently `unaudited` (audit row:
  `pmns_c3_character_mode_reduction_note`). Sibling support note
  showing that on the graph-first reduced forward-cycle channel the
  C3 Fourier modes are exactly `z_0 = w`, `z_1 = u - i v`,
  `z_2 = u + i v` with `z_1 = conjugate(z_2)` on the residual
  graph-first antiunitary slice. Supplies the precise readout
  `J_chi(A_fwd) = chi = u + i v` that the present note imports as a
  premise.
- [`PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md`](PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md)
  — currently `audited_conditional` (audit row:
  `pmns_hw1_source_transfer_boundary_note`). Adjacent boundary-grade
  authority for the sole-axiom `hw=1` source/transfer route on which
  the present note's annihilation claim `J_chi = 0` is one of three
  components.
- [`PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md`](PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md)
  — currently `unaudited` (audit row:
  `pmns_selector_current_stack_zero_law_note`). Sibling support note
  recording the current-stack zero law on the cited bank,
  consistent with the present note's `J_chi = 0` annihilation claim
  on all three listed cited routes.
- [`DM_PMNS_GRAPH_FIRST_ORDERED_CHAIN_NONZERO_CURRENT_ACTIVATION_THEOREM_NOTE_2026-04-21.md`](DM_PMNS_GRAPH_FIRST_ORDERED_CHAIN_NONZERO_CURRENT_ACTIVATION_THEOREM_NOTE_2026-04-21.md)
  — currently `unaudited` (audit row:
  `dm_pmns_graph_first_ordered_chain_nonzero_current_activation_theorem_note_2026-04-21`).
  Downstream activation theorem constructing one explicit sole-axiom
  nonzero-current law (`A_ord = diag(1,2,3) + (E12 + E23 + E31)`,
  `J_chi = 1`) that lands the very target named by the present
  note's "Consequence" section.

Open class D registration targets named by the 2026-05-05 audit
verdict as `missing_bridge_theorem`:

- The exact native C3 holonomy readout on `A_fwd` is imported via the
  Fourier projection definition. Closing it requires a retained-grade
  source note proving that the holonomies `h_0, h_1, h_2` constructed
  on the cited `hw=1` triplet evaluate the Fourier projection
  `J_chi(A_fwd)` to `chi = u + i v` from primitives rather than from
  notation, as named in the 2026-05-05 audit verdict's
  `notes_for_re_audit_if_any` field:
  `missing_bridge_theorem: provide a retained-grade derivation of the C3
  holonomy readout on A_fwd and the proof that the free, hw=1
  source/transfer, and cited scalar routes force J_chi=0`.
- The route-wise annihilation `J_chi = 0` on the free, sole-axiom
  `hw=1` source/transfer, and cited scalar routes is imported as
  a premise. Closing it requires a retained-grade source note proving
  this annihilation route-by-route.
- Minimality of "exactly one complex current" as the smallest
  remaining sole-axiom source object is asserted but not derived in
  the present note. Closing it requires a minimality theorem on the
  reduced graph-first PMNS family.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with
load-bearing-step class A and `chain_closes=False`, observing that
the algebraic Fourier-projection identity is plausible as algebra
over specified holonomies but the restricted packet does not provide
the holonomy/readout formulas or a proof that the listed sole-axiom
routes annihilate `J_chi`. The runner
`scripts/frontier_pmns_c3_nontrivial_current_boundary.py` exists in
the repository and verifies the conditional readout (`PASS=16 FAIL=0`
on 2026-05-10), but its checks are class A finite-dimensional algebra
on the projected forward-cycle algebra, not first-principles
derivations of the C3 holonomy bridge or the route-annihilation
theorem from the sole axiom. The cite chain above wires the two
adjacent C3-character sibling authorities, the `hw=1` source-transfer
boundary, the current-stack zero-law support, and the downstream
nonzero-current activation theorem; it explicitly registers the three
missing-bridge-theorem targets named by the verdict's
`notes_for_re_audit_if_any` field. Because this source note is being
edited, the audit lane must re-ratify it from the regenerated ledger;
this addendum does not apply an `audit_status` or promote effective
status.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) plus class D
(open-target registration). It does not change any algebraic content,
runner output, or load-bearing step classification. It records the
upstream authority candidates the audit verdict expected, the runner
that exercises the conditional readout, and the missing-bridge-theorem
targets named by the verdict's `notes_for_re_audit_if_any` field. It
mirrors the live cite-chain pattern used by the
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md` cluster
(commit `8e84f0c23`) and the PMNS active-source cluster (commit
`be5a06dbf`).
