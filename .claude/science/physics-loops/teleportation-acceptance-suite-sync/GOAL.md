# Goal

Close the missing-derivation prompt for
`docs/TELEPORTATION_ACCEPTANCE_SUITE_NOTE.md`.

The audit failure was documentation drift: the note documented only four
strict-lane additions while
`scripts/frontier_teleportation_acceptance_suite.py --strict-lane --list-probes`
listed additional present-gated probes.

Target outcome: a bounded/meta harness-documentation repair that is ready for
independent re-audit. This branch does not assign an audit verdict.
