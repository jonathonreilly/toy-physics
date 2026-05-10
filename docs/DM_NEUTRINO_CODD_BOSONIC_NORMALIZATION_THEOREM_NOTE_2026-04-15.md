# DM Neutrino `c_odd` Bosonic Normalization Theorem

**Date:** 2026-04-15  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_dm_neutrino_codd_bosonic_normalization_theorem.py`

## Framework sentence

In this note, “axiom” means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else is a derived atlas row.

## Question

Can the odd transfer coefficient in

- `gamma = c_odd a_sel`

be fixed from the single axiom plus the current atlas?

## Bottom line

Yes, canonically.

On their exact minimal blocks, the reduced selector generator

`S_cls = diag(0,0,1,-1)`

and the DM odd triplet generator

`T_gamma = [[0,0,-i],[0,0,0],[i,0,0]]`

have the same exact bosonic source-response law under the unique additive
CPT-even scalar generator

`W[J] = log|det(D+J)| - log|det D|`.

Therefore the canonical odd normalization is

- `|c_odd| = 1`

and on the source-oriented branch convention we record

- `c_odd = +1`.

## Exact reason

The two generators have the same nonzero odd spectrum:

- `S_cls` has eigenvalues `{+1,-1,0,0}`
- `T_gamma` has eigenvalues `{+1,-1,0}`

so they differ only by null multiplicity.

After subtracting the zero-source baseline in `W`, that null multiplicity
drops out. On a scalar baseline `m I`, both source families satisfy

- `W = log|1 - j^2/m^2|`.

So they have:

- the same exact source-response curve
- the same exact small-source bosonic curvature

and therefore the same canonical odd normalization.

## Why this matters

This closes the odd normalization part of the weak-to-triplet transfer law.

The branch no longer has to say:

- “both `c_odd` and `M_even` are still open”

It can now say:

- the odd normalization is fixed canonically: `c_odd = +1`
- the remaining coefficient blocker is the even response matrix `M_even`

## What this does not close

This note does **not** derive:

- the activation law for the selector amplitude `a_sel`
- the even response matrix `M_even`
- the microscopic two-channel readout replacing the current bounded weak tensor
  readout

So this is an odd-normalization theorem, not full transfer-coefficient closure.

## Benchmark consequence

The benchmark stays

- `eta = 1.81e-10`
- `eta / eta_obs ~= 0.30`

because that benchmark was not limited by an unresolved odd normalization
factor. The live remaining gap is the even response law, not `c_odd`.

## Command

```bash
python3 scripts/frontier_dm_neutrino_codd_bosonic_normalization_theorem.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope, which remains the algebraic isospectrality + identical bosonic-response claim on the `S_cls` / `T_gamma` minimal blocks plus the imported observable-principle premise.

One-hop authorities cited:

- [`PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md`](PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md)
  — currently `unaudited` (audit row: `pmns_selector_unique_amplitude_slot_note`).
  Upstream authority candidate for the single exact reduced amplitude slot
  `a_sel` on `S_cls`.
- [`PMNS_SELECTOR_SIGN_TO_BRANCH_REDUCTION_NOTE.md`](PMNS_SELECTOR_SIGN_TO_BRANCH_REDUCTION_NOTE.md)
  — currently `unaudited` (audit row:
  `pmns_selector_sign_to_branch_reduction_note`). Upstream authority
  candidate for the source-oriented branch convention recording
  `c_odd = +1` rather than only `|c_odd| = 1`.
- [`DM_NEUTRINO_TRIPLET_CHARACTER_SOURCE_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_TRIPLET_CHARACTER_SOURCE_THEOREM_NOTE_2026-04-15.md)
  — currently `unaudited` (audit row:
  `dm_neutrino_triplet_character_source_theorem_note_2026-04-15`).
  Upstream authority candidate for the exact odd source `gamma` on the
  triplet generator `T_gamma`.
- [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  — currently `audited_conditional` (audit row:
  `observable_principle_from_axiom_note`). Upstream conditional
  authority for the load-bearing premise that physical local scalar
  observables are exact source derivatives of the unique additive
  CPT-even scalar generator `W[J] = log|det(D+J)| - log|det D|`, given
  premises P1 (scalar additivity), P2 (CPT-even phase blindness),
  P3 (continuity / minimal regularity), and P4 (normalization choice).

Because three of the four cited upstream authorities are `unaudited`
and the fourth is `audited_conditional`, the canonical odd normalization
selection here cannot lift past `audited_conditional` under the standard
cite-chain rule once this row is itself audited. This matches the live
audit row's current `unaudited` status and does not require any audit
JSON edit.

The runner-checked content of this note (Part 1 algebra: `S_cls` and
`T_gamma` exact spectra, equal nonzero spectrum after subtracting null
multiplicity; Part 2: `W[S_cls] = W[T_gamma] = log|1 - j^2/m^2|`,
identical small-source curvature; Part 3: `|c_odd| = 1` from equal
bosonic response, source-oriented `c_odd = +1`) is exact
finite-dimensional matrix algebra on the minimal odd blocks and is
independent of the cited upstream authorities. The cite chain is what
supplies the physical selection rule that makes the equal-response
identification an admissible normalization statement rather than only
an algebraic comparator.

## Honest auditor read

A future audit pass on this row will see four upstream authority
citations: `pmns_selector_unique_amplitude_slot_note` (unaudited),
`pmns_selector_sign_to_branch_reduction_note` (unaudited),
`dm_neutrino_triplet_character_source_theorem_note_2026-04-15`
(unaudited), and `observable_principle_from_axiom_note`
(audited_conditional). The runner closes A=12 algebraic checks once the
observable-principle premise is accepted, but the canonical odd
normalization `|c_odd| = 1` selection over the bare equal-spectrum
comparator does not follow from the runner alone — it requires the
upstream theorem that physical local scalar observables are exact `W[J]`
source-response coefficients. The cite-chain repair above wires
`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE` (`audited_conditional`) as that
upstream authority and the three PMNS / triplet-character authorities as
the source-side companions. Effective status will be capped at
`audited_conditional` because the strongest upstream is itself
conditional on the four admitted premises P1-P4. The note's
`audit_status` is unchanged by this addendum.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation). It does not
change any algebraic content, runner output, or load-bearing step
classification. It records the upstream authorities the audit citation
graph expects and matches the live cite-chain pattern used by the
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md` rigorize
(commit `8e84f0c23`) and the `DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md`
cluster rigorize (commit `02ad4fadd`).
