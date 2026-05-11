# Gauge-Vacuum Plaquette First-Sector Minimal-Bulk Completion Principle

**Date:** 2026-04-19 (originally); 2026-05-10 (scope-narrowed per audit verdict)
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
  mass, weighted tail mass, squared `l2` mass, support size).

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

These citations are the upstream authorities the runner inspects via
substring import. The substring import is not a closed-input mechanism;
the auditor verdict explicitly noted "those imported premises cannot
count as closed inputs". The dependencies are therefore tracked here as
conditional-dependency citations. The current effective status of each
upstream is tracked by the audit ledger; this note does not promote any
of them.

- [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TRUNCATED_ENVIRONMENT_PACKET_NOTE_2026-04-19.md](GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TRUNCATED_ENVIRONMENT_PACKET_NOTE_2026-04-19.md)
  for the retained first-sector packet `rho_ret = (1, 0.267139..., 0.267139..., 0)`.
- [GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_ZERO_EXTENSION_FACTORIZED_CLASS_THEOREM_NOTE_2026-04-19.md](GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_ZERO_EXTENSION_FACTORIZED_CLASS_THEOREM_NOTE_2026-04-19.md)
  for the existence of one explicit factorized-class extension of `rho_ret`
  by zero on every higher weight, providing the local-factor diagonal
  used by the runner.
- The historical tail-underdetermination note that the runner inspects
  by substring lives at
  `archive_unlanded/gauge-vacuum-plaquette-missing-runners-2026-04-30/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_TAIL_UNDERDETERMINATION_THEOREM_NOTE_2026-04-19.md`;
  this note records that the conditional dependency is on archived
  prose, not on a live retained-grade authority.

These are imported authorities for a bounded theorem. The row's
effective status is set by the independent audit lane.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_principle_theorem_2026_04_19.py
```

Expected:

```text
PASS=7 FAIL=0
```

The seven runner checks certify the witness-family-restricted
statement above; they do not certify the universal Loewner-monotonicity
step that the audit verdict flagged as the load-bearing failure.
