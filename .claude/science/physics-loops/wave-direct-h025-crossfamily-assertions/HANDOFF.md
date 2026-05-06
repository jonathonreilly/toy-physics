# Handoff

## Block Result

`wave_direct_dm_h025_seed0_crossfamily_note` is now a bounded-support note with a registered runner:

- `scripts/wave_direct_dm_h025_seed0_crossfamily_assertions.py`
- `outputs/wave_direct_dm_h025_seed0_crossfamily_assertions_2026-05-06.txt`

The runner checks:

- exact null rows for Fam1/Fam2;
- negative nonzero sign pattern;
- weak-field spread summaries;
- the selected strength-`0.004` cross-family ordering;
- explicit non-claims for portability and stable amplitude law.

## Audit State

The target row is reset to `unaudited`, with `claim_type=bounded_theorem`, and the prior `audited_numerical_match` row is archived in `previous_audits`.

## Remaining Work

- Audit the Fam1/Fam2 H=0.25 seed-0 control notes.
- Add or audit source runners for broader control surfaces before making wider claims.
- Keep Fam3 and amplitude-law language out of this note until separate evidence exists.

## PR

Opened:

- https://github.com/jonathonreilly/cl3-lattice-framework/pull/571
