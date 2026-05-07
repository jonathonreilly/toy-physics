# One-Generation Matter Closure Note

**Date:** 2026-04-14 (audit-prep dependency-status + neutral-singlet
branch-convention disclaimer 2026-05-07)
**Type:** bounded_theorem (audit-pipeline retag from earlier
`proposed_retained` framing; current ledger `claim_type:
bounded_theorem`).

**Status authority:** independent audit lane only. This source note
does not set or predict an audit outcome; later status is generated
by the audit pipeline after independent review. The currently-recorded
ledger verdict for this row is `audited_conditional` (2026-05-05); the
source author does not propose retained / positive_theorem promotion
at this time.

**Scripts:** `scripts/frontier_right_handed_sector.py`,
`scripts/frontier_anomaly_forces_time.py`
**Authority role:** canonical main-branch note for the one-generation
matter-closure row.

## Cited dependencies and their current ledger status (audit-prep 2026-05-07)

The audit-lane verdict on this row (`audited_conditional`, 2026-05-05)
named three residuals:

1. *`LEFT_HANDED_CHARGE_MATCHING_NOTE.md` is `audited_conditional`*
   (ledger status as of audit pass 2026-05-05). That row is itself
   conditional on a `bounded_theorem` narrow-ratio packet plus a
   normalization-convention disclaimer; see
   [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
   for the explicit `β = -1` convention boundary.
2. *`ANOMALY_FORCES_TIME_THEOREM.md` is `unaudited`* (ledger status as
   of audit pass 2026-05-05) **and** is itself conditional on companion
   notes that may not all be present on `main`. Source author does not
   claim retained-grade closure of that authority here; only the
   bounded conditional bridge to `(3,1)` signature is imported.
3. *neutral-singlet branch selection is currently a convention.* See
   the "Neutral-singlet branch-selection boundary" section below.

The three residuals together mean this row should be cited as the
bounded conditional one-generation completion, not as an independent
positive theorem of full-framework one-generation closure.

## Safe statement

On the conditional surface defined by (i) the convention-normalized
left-handed charge surface of
[`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
(ledger `audited_conditional`), (ii) the bounded chirality / `3+1`
admissions imported via
[`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
(ledger `unaudited`), and (iii) the neutral-singlet branch convention
documented below, the framework completes one Standard Model
generation as:

- the graph-first selected-axis surface fixes the convention-normalized
  left-handed gauge/matter sector;
- anomaly-forced time supplies the chirality structure and single-clock
  `3+1` closure (conditional on the cited authority);
- anomaly cancellation, on the neutral-singlet branch, fixes the
  right-handed singlet completion to the Standard Model assignment:

  - `u_R : (1,3)_{+4/3}`
  - `d_R : (1,3)_{-2/3}`
  - `e_R : (1,1)_{-2}`
  - `nu_R : (1,1)_0`

The cubic anomaly equation `Tr[Y^3] = 0` factors into two branches
related by `e_R ↔ nu_R` relabelling; choosing the neutral-singlet
branch (`y_4 = 0`) selects the SM hypercharge assignment shown above.
The other branch is anomaly-consistent but assigns the neutral
singlet to the position conventionally labelled `e_R`. The runner
checks both branches for anomaly-cancellation; only the neutral-
singlet convention selects the conventional SM labelling.

## Neutral-singlet branch-selection boundary (audit-prep 2026-05-07)

The convention `nu_R = (1,1)_0` (i.e. the SU(2)-singlet right-handed
neutrino has hypercharge `Y_4 = 0`) is a **branch-selection
convention**, not a derivation from retained-grade framework primitives in
this row's load-bearing chain. Concretely:

- The anomaly equations admit a discrete `e_R ↔ nu_R` relabelling
  symmetry; the framework's anomaly arithmetic alone does not choose
  between the two branches.
- The "neutral singlet has hypercharge zero" rule is a labelling
  convention matching the conventional SM right-handed neutrino
  assignment, motivated externally by the absence of observed
  electromagnetic interactions of the right-handed neutrino.
- A retained-grade derivation of branch selection from framework
  primitives would require a separate authority (e.g. a structural
  derivation that the framework's neutral-singlet sector must carry
  zero hypercharge); no such authority is currently cited as
  load-bearing for this row.

This is the boundary the audit-lane verdict named when it noted the
"missing companion bridge notes and the neutral-singlet branch
selection" residual. The row is the bounded conditional
one-generation completion under this convention, not an independent
derivation of branch selection.

## Canonical derivation stack

1. [LEFT_HANDED_CHARGE_MATCHING_NOTE.md](./LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
   fixes the safe left-handed selected-axis charge surface.
2. [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md)
   shows that anomaly cancellation requires the opposite-chirality completion
   and that the framework closes on exactly one temporal direction.
3. `frontier_right_handed_sector.py` verifies the concrete completion chain:
   no weak singlets on the purely spatial `C^8` surface, proper chirality only
   on the 4D `C^16` surface, and anomaly cancellation fixing the Standard Model
   right-handed branch.

## Boundary

This note is intentionally narrower than an overclaim:

- bounded conditional: one-generation completion under the cited
  chirality/time authority, left-handed charge surface, and
  neutral-singlet branch convention;
- not claimed: a retained-grade derivation of the right-handed sector
  from the spatial graph alone;
- not claimed: a nonconventional derivation of the neutral-singlet
  branch selection.

The temporal/chirality step remains load-bearing and is cited through
`ANOMALY_FORCES_TIME_THEOREM.md`; this note does not promote that
authority.

## Validation

- [frontier_anomaly_forces_time.py](./../scripts/frontier_anomaly_forces_time.py)
- [frontier_right_handed_sector.py](./../scripts/frontier_right_handed_sector.py)

Current main-branch runner state:

- `frontier_right_handed_sector.py`: `PASS=61`, `FAIL=0`
