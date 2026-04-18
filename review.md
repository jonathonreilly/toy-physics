# Review: `claude/dreamy-wing-969574`

Reviewed branch tip: `00f49250`

## Verdict

Not cleared for `main` as a retained-status promotion.

The branch is scoped cleanly and the new runner replays at `PASS=16 FAIL=0`, so
this is not a runtime rejection. The blocker is the status upgrade: the new
note promotes `w = -1` to a retained structural corollary even though the
load-bearing vacuum-identification premise is still described by the repo as a
companion/conditional cosmology lane.

## Replay

Verified directly:

- `python3 scripts/frontier_dark_energy_eos_retained_corollary.py`
  -> `PASS=16 FAIL=0`

## Findings

### [P1] The retained-corollary upgrade still rests on a companion-surface premise

The theorem is stated from four inputs, and one of them is the exact status
problem:

- condition (3) is the spectral-gap vacuum identification
  `Lambda = lambda_1(S^3_R) = 3/R^2`,
- that condition is sourced to
  `COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`,
- but that authority note is still explicitly classified as a
  bounded/conditional cosmology companion, not a retained flagship theorem.

The new note then calls the result a retained structural corollary while also
saying, in its own safe-claim boundary, that it does **not** support a
first-principles derivation that the retained spectral gap *is* the
vacuum-energy mechanism, only that it is identified with it on the companion
surface. Those two statements do not fit together. As written, this is a clean
conditional corollary on the fixed-gap vacuum route, not a retained promotion.

Affected surfaces:
- `docs/DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`
- `docs/COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`
- `docs/publication/ci3_z3/PUBLICATION_MATRIX.md`

### [P2] The runner certifies the corollary once the premises are assumed, but not the retained-status step

The new runner is disciplined about scope, but that scope is exactly why it
does not justify the promotion:

- it restates the theorem as "given ... spectral-gap vacuum identification ...
  and fixed `R`",
- it verifies the `w = -1` consequence of those assumptions,
- it does not certify that the vacuum identification itself is retained on
  `main`,
- and it does not certify that the fixed-`R` vacuum surface has been promoted
  beyond the current cosmology companion framing.

So the script supports a conditional theorem packet, not the claim-strength
upgrade from bounded/conditional cosmology companion to retained structural
corollary.

Affected surface:
- `scripts/frontier_dark_energy_eos_retained_corollary.py`

## Best Next Step

There are two honest ways forward:

1. **Derive the missing status step.**
   Promote the spectral-gap vacuum identification / fixed-`R` vacuum surface
   itself onto a retained theorem surface, and then this `w = -1` split can be
   landed as a retained corollary with package updates.

2. **Downgrade the new note/runner packet.**
   Keep the new note as a cleaner conditional corollary on the existing
   cosmology companion lane, keep the publication row bounded/conditional, and
   use the new runner as a support tool rather than a retained promotion.
