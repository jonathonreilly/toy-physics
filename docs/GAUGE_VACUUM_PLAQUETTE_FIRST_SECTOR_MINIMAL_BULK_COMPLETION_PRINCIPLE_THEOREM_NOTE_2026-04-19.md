# Gauge-Vacuum Plaquette First-Sector Minimal-Bulk Completion Principle

**Date:** 2026-04-19 (originally); 2026-05-10 (scope-narrowed per audit verdict); 2026-05-16 (substring-import mechanism removed from runner per audit verdict)
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only.
**Primary runner:** [`scripts/frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_principle_theorem_2026_04_19.py`](../scripts/frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_principle_theorem_2026_04_19.py)

## Claim

Fix the retained packet `rho_ret` on the first-symmetric support inside the
canonical Wilson factorized class.

Inside the canonical Wilson factorized cone, the coefficient-order
zero-extension `rho_0` is the unique zero-coefficient lift of `rho_ret`
that adds zero mass to every higher-weight slot. Equivalently, on the
explicit witness families exercised by the runner, every nonzero
nonnegative tail strictly increases at least one positive bulk-tail
functional (total tail mass, weighted tail mass, squared `l2` mass, or
support size) and adds a positive-semidefinite Loewner increment to the
factorized-Wilson transfer.

This is the runner-certified part of the first-sector minimal-bulk
completion picture. It does not promote a new axiom and does not change
the framework-point Wilson environment packet that is still open.

## Scope

This note is restricted to the runner-tested witness families:

- the explicit zero-extension packet `rho_0` of `rho_ret` to the
  retained first-symmetric weights `(0,0), (1,0), (0,1), (1,1)`;
- two explicit nonnegative tails inside the audited factorized cone,
  the `(2,0) + (0,2)` witness with mass `0.05 + 0.05` and the
  `(2,1) + (1,2) + (2,2)` witness with mass `0.03 + 0.03 + 0.02`;
- the four positive bulk-tail functionals listed above (total tail
  mass, weighted tail mass, squared `l2` mass, support size);
- a randomized sweep (n = 64) of admissible nonnegative
  conjugation-symmetric tails inside the cone, used solely to certify
  the algebraic identity `delta >= 0 ==> rho_0 + delta >= rho_0`
  coefficientwise. The sweep does **not** certify universal Loewner
  monotonicity.

For these explicit witness families the runner certifies coefficient-
order minimality of `rho_0` and a positive-semidefinite Loewner
increment for both tested tails inside the canonical factorized cone.

## Open derivation gap

For arbitrary admissible nonnegative conjugation-symmetric tails inside
the canonical Wilson factorized cone, the universal Loewner-monotonicity
/ unique-minimality theorem is **not** established by this note or by
the runner's finite witness checks. The auditor verdict was explicit:

> The coefficient-order zero-extension result is valid on its own
> terms, but the claimed equivalence to unique Loewner-minimality for
> all admissible extensions is not established by the provided note and
> code.

Closing the universal-tail step would require an analytic proof that
`T(rho_0 + delta) - T(rho_0)` is positive-semidefinite for every
admissible `delta >= 0` inside the cone, plus a precise definition of
the class of positive bulk-tail functionals on which strict
monotonicity is claimed. That remains genuine open derivation work and
is **not** closed by this note.

## Dependencies

The runner does **not** import upstream notes via substring matching on
prose. The previous audit verdict explicitly flagged that mechanism as
not establishing closed inputs, and that mechanism has been removed.
The numeric facts used by the runner are now verified directly on the
packet and on the transfer matrix:

- `rho_ret` is consumed as the numeric vector returned by the local
  Python helper `completed_sector_data` (an in-tree Python module
  import). The runner directly checks that this vector is normalized,
  conjugation-symmetric, nonnegative on `(1,0)/(0,1)`, and zero on
  `(1,1)`.
- The local-factor diagonal used in the transfer assembly is consumed
  from the in-tree Python helper `local_factor_diagonal`. The runner
  directly checks that the assembled zero-extension transfer is
  self-adjoint on the truncated dominant-weight box.

The two source notes that originally provided this material are still
the conceptual references for the underlying retained packet and
factorized-class existence, and remain conditional-dependency citations
for that conceptual role; they are NOT treated as closed retained-grade
inputs by this note. The current effective status of each upstream is
tracked by the audit ledger; this note does not promote any of them.

- [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TRUNCATED_ENVIRONMENT_PACKET_NOTE_2026-04-19.md](GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TRUNCATED_ENVIRONMENT_PACKET_NOTE_2026-04-19.md)
  for the conceptual retained first-sector packet
  `rho_ret = (1, 0.267139..., 0.267139..., 0)`.
- [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_ZERO_EXTENSION_FACTORIZED_CLASS_THEOREM_NOTE_2026-04-19.md](GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_ZERO_EXTENSION_FACTORIZED_CLASS_THEOREM_NOTE_2026-04-19.md)
  for the conceptual existence of one explicit factorized-class
  extension of `rho_ret` by zero on every higher weight, providing the
  local-factor diagonal used by the runner.

The row's effective status is set by the independent audit lane.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_principle_theorem_2026_04_19.py
```

Expected:

```text
PASS=8 FAIL=0
```

The eight runner checks certify the witness-family-restricted
statement above; they do not certify the universal Loewner-monotonicity
step that the audit verdict flagged as the load-bearing failure.
