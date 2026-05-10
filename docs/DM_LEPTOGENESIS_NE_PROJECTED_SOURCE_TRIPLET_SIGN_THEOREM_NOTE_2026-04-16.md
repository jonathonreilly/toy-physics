# DM Leptogenesis `N_e` Projected-Source Triplet Sign Theorem

**Date:** 2026-04-16  
**Status:** support - structural or confirmatory support note
to the baryogenesis-side triplet sign target  
**Script:** `scripts/frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem.py`

## Question

Can the baryogenesis-side triplet target be written directly at the DM-lane
endpoint `dW_e^H`, rather than only through the intermediate off-seed PMNS
coordinates?

## Bottom line

Yes.

If the projected Hermitian response pack on the charged support `E_e` is
written as

`(R11, R22, R33, S12, A12, S13, A13, S23, A23)`,

where:

- `Rii` are the diagonal Hermitian responses,
- `Sij = 2 Re(H_ij)`,
- `Aij` are the antisymmetric Hermitian responses with
  `H_ij = (Sij - i Aij)/2`,

then the baryogenesis triplet channels are exact linear functionals of that
same projected source pack:

- `gamma = A13 / 2`
- `E1 = delta + rho = (R22 - R33)/2 + (S12 - S13)/4`
- `E2 = A + b - c - d = R11 + (S12 + S13)/4 - (R22 + R33)/2 - S23/2`

So the live PMNS constructive gate can be stated directly at `dW_e^H` level:

- `gamma > 0`
- `E1 > 0`
- `E2 > 0`

## What this closes

This closes the bridge-shape ambiguity raised by the DM lane.

The DM route had already reduced the PMNS-assisted problem to:

`D -> D_- -> dW_e^H -> H_e -> packet -> eta`.

What was still missing was the baryogenesis-side translation of that endpoint.

This theorem supplies it:

- the DM-lane endpoint `dW_e^H` already carries the baryogenesis triplet
  channels,
- and it carries them by exact linear formulas.

So the next PMNS-side baryogenesis step no longer needs to be described as
“derive some better full-`D` law” in the abstract.

It is specifically:

- derive a microscopic law whose projected Hermitian source pack satisfies
  `gamma > 0`, `E1 > 0`, `E2 > 0`

equivalently

- derive `dW_e^H` with
  `A13 > 0`,
  `(R22 - R33)/2 + (S12 - S13)/4 > 0`,
  `R11 + (S12 + S13)/4 - (R22 + R33)/2 - S23/2 > 0`.

## Canonical comparator read

On the canonical near-closing `N_e` sample, the projected Hermitian source pack
already yields:

- `gamma > 0`
- `E1 < 0`
- `E2 < 0`

So the canonical DM/PMNS comparator already has the right odd source sign but
still misses the constructive baryogenesis sheet on both real interference
channels.

## Consequence for the live target

The PMNS-side comparator target is now explicit in two equivalent ways:

- off-seed source form:
  `sin(delta) > 0`, `E1 > 0`, `E2 > 0`
- projected-source form:
  `gamma > 0`, `E1 > 0`, `E2 > 0`
  with `gamma`, `E1`, `E2` given by the linear `dW_e^H` formulas above

So the live remaining comparator task is:

- derive a full-`D` / `D_-` / `dW_e^H` law that lands on that sign system

or else

- prove a sharper exact no-go on the current PMNS branch.

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream authorities
the runner imports when constructing the projected Hermitian response
pack `(R11, R22, R33, S12, A12, S13, A13, S23, A23)` and the canonical
`dW_e^H` triplet read, in response to the 2026-05-05 audit verdict's
`missing_bridge_theorem` repair target. It does not promote the note or
change the audited claim scope, which remains the linear translation
from the projected response pack to `(gamma, E1, E2)` conditional on
the imported endpoint definitions.

The runner
[`scripts/frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem.py`](../scripts/frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem.py)
imports three helper symbols from sibling runners:

- `hermitian_linear_responses` from
  [`scripts/frontier_dm_leptogenesis_ne_projected_source_law_derivation.py`](../scripts/frontier_dm_leptogenesis_ne_projected_source_law_derivation.py)
  with source note
  [`DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_NE_PROJECTED_SOURCE_LAW_DERIVATION_NOTE_2026-04-16.md)
  — defines the projected Hermitian response pack on the charged
  support `E_e`. Currently `unaudited`.
- `breaking_triplet_coordinates` from
  [`scripts/frontier_dm_leptogenesis_pmns_cp_bridge_boundary.py`](../scripts/frontier_dm_leptogenesis_pmns_cp_bridge_boundary.py)
  with source note
  [`DM_LEPTOGENESIS_PMNS_CP_BRIDGE_BOUNDARY_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_CP_BRIDGE_BOUNDARY_NOTE_2026-04-16.md)
  — defines the breaking-triplet coordinates `(gamma, E1, E2)` on the
  PMNS-side endpoint. Currently `unaudited`.
- `canonical_h` from
  [`scripts/frontier_dm_leptogenesis_pmns_projector_interface.py`](../scripts/frontier_dm_leptogenesis_pmns_projector_interface.py)
  with source note
  [`DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md)
  — provides the canonical near-closing PMNS Hermitian sample used in
  the comparator read. Currently `audited_conditional`.

None of the three upstream helpers carries `audited_clean` retained
status, so effective-status propagation correctly caps this row at
`audited_conditional`. The audit-clean part of this note is the
projected-source linear functional identity:

- `gamma = A13 / 2`
- `E1 = (R22 - R33) / 2 + (S12 - S13) / 4`
- `E2 = R11 + (S12 + S13) / 4 - (R22 + R33) / 2 - S23 / 2`

verified by the runner against the imported helper definitions.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with
the substantive observation that the load-bearing linear formulas are
class-A algebra once the response-pack coordinates and breaking-triplet
coordinates are accepted, but those definitions are imported from
sibling runner modules whose source notes are not closed in the audit
ledger. The three imported helper surfaces are now explicitly cited in
the section above. The note's audit status is unchanged by this
addendum.

The runner's classified output continues to read PASS=12 / FAIL=0; the
canonical comparator read `gamma > 0, E1 < 0, E2 < 0` continues to
miss the constructive baryogenesis sheet on both real interference
channels, exactly as recorded by the runner.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_ne_projected_source_triplet_sign_theorem.py
```
