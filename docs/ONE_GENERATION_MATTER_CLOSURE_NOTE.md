# One-Generation Matter Closure Note

**Date:** 2026-04-14
**Status:** conditional / support; after this boundary edit the audit ledger
queues the row as `audit_status=unaudited`, `effective_status=unaudited`.
**Claim type:** bounded_theorem proposal; independent audit lane sets the
actual `claim_type`, `audit_status`, and pipeline-derived `effective_status`.
**Scripts:** `scripts/frontier_right_handed_sector.py`, `scripts/frontier_anomaly_forces_time.py`
**Authority role:** canonical main-branch note for the conditional
one-generation matter-closure row

## Safe statement

Under the stated graph-first LH eigenvalue surface, anomaly-forced-time
admissions, neutral-singlet branch convention, and SM electric-charge readout
convention, the framework closes the Standard Model one-generation charge
table in the **full framework**:

- the graph-first selected-axis surface fixes the left-handed gauge/matter sector
- anomaly-forced time supplies the chirality structure and single-clock `3+1` closure
- anomaly cancellation then fixes the right-handed singlet completion once the
  neutral-singlet Standard Model branch is imposed

The conditional full-framework one-generation completion is therefore:

- `u_R : (1,3)_{+4/3}`
- `d_R : (1,3)_{-2/3}`
- `e_R : (1,1)_{-2}`
- `nu_R : (1,1)_0`

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

## Audit Boundary

This note is intentionally narrower than an overclaim:

- exact support: the anomaly arithmetic and runner checks for the stated
  one-generation table;
- conditional: the full Standard Model branch selection because
  `Y(nu_R)=0`, the `Q = T_3 + Y/2` readout, and the SM charge labels are
  load-bearing inputs;
- not claimed: audit-ratified retained closure of one-generation matter;
- not claimed: a derivation of the right-handed sector from the spatial graph
  alone.

The temporal/chirality step and the neutral-singlet branch are load-bearing.
The prior audit verdict treated the row as conditional; after this boundary
edit the row is re-queued for independent audit with those bridges explicit.

## Validation

- [frontier_anomaly_forces_time.py](./../scripts/frontier_anomaly_forces_time.py)
- [frontier_right_handed_sector.py](./../scripts/frontier_right_handed_sector.py)

Current main-branch runner state:

- `frontier_right_handed_sector.py`: `PASS=61`, `FAIL=0`
